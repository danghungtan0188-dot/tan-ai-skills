#!/usr/bin/env python3
"""Biến danh sách cảnh Claude chọn thành kịch bản dựng khớp đúng độ dài người dùng yêu cầu.

    python build_edit_plan.py rushes.json chon-canh.json --target 180 --out edit-plan.json

`chon-canh.json` do Claude viết SAU KHI xem contact sheet của survey_rushes.py:

    {"tieu_de": "...",
     "muc": [{"id": "mo-dau", "ten": "Toàn cảnh buổi lễ",
              "canh": [{"shot": "0.1", "co": "toan", "ly_do": "đặt bối cảnh sân lễ"},
                       {"shot": "1.3", "co": "trung", "in": 2.0, "out": 7.0, "ly_do": "..."}]}]}

`co`: toan | trung | can.  `loai`: broll (mặc định) | phat_bieu.  `ly_do` bắt buộc — không có
lý do thì đừng đưa cảnh vào bản tin. `in`/`out` tính theo giây trong clip gốc, bỏ trống thì lấy
trọn cảnh.

LỖI (exit 1): shot không có thật · in/out ra ngoài clip · đoạn b-roll trùm qua mốc cắt cảnh ·
b-roll ngắn hơn 2,5 s hoặc dài quá 8 s · phát biểu dưới 4 s · hai đoạn liền nhau cùng clip cùng
cỡ cảnh · đoạn đầu không phải cảnh toàn · thiếu lý do · không co giãn được về đúng độ dài.

Co giãn chỉ đụng b-roll, không bao giờ cắt ngắn phát biểu. Xong bước này phải đưa bảng cho
người dùng duyệt rồi mới chạy assemble.py — mặc định `cut_authorized=false`.
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from khuon_mau import lay_hinh  # noqa: E402

BROLL_MIN, BROLL_MAX, PHAT_BIEU_MIN, SAI_SO = 2.5, 8.0, 4.0, 2.0
CO_HOP_LE = ("toan", "trung", "can")
LOAI_HOP_LE = ("broll", "phat_bieu")


def nap(rushes: dict) -> dict:
    return {s["id"]: (c, s) for c in rushes["clips"] for s in c["shots"]}


def dung_doan(chon: dict, bang: dict, khuon: dict | None = None) -> tuple[list[dict], list[str]]:
    doan, loi = [], []
    for muc in chon["muc"]:
        for c in muc["canh"]:
            sid = c["shot"]
            if sid not in bang:
                loi.append(f"{sid}: không có trong rushes.json")
                continue
            clip, shot = bang[sid]
            t0 = float(c.get("in", shot["start"]))
            t1 = float(c.get("out", shot["end"]))
            if not 0 <= t0 < t1 <= clip["duration"] + 1e-6:
                loi.append(f"{sid}: in/out {t0}–{t1} ra ngoài clip ({clip['duration']}s)")
                continue
            if not str(c.get("ly_do", "")).strip():
                loi.append(f"{sid}: thiếu lý do chọn cảnh")
            if c.get("co") not in CO_HOP_LE:
                loi.append(f"{sid}: cỡ cảnh '{c.get('co')}' phải là {'/'.join(CO_HOP_LE)}")
            toc = 1.0
            if c.get("hinh"):
                if khuon is None:
                    loi.append(f"{sid}: có kiểu hình '{c['hinh']}' nhưng chưa đưa --khuon")
                else:
                    try:
                        toc = float(lay_hinh(khuon, c["hinh"]).get("toc_do", 1.0))
                    except SystemExit as e:
                        loi.append(f"{sid}: {e}")
            loai = c.get("loai", "broll")
            if loai not in LOAI_HOP_LE:          # gõ sai sẽ lọt qua luật b-roll, thành cắt bừa
                loi.append(f"{sid}: loại '{loai}' phải là {'/'.join(LOAI_HOP_LE)}")
                loai = "broll"
            # nới dài nhất có thể: b-roll không được trùm sang cảnh khác, phát biểu chỉ giới hạn bởi clip
            # tốc độ nhanh ăn nhiều vật liệu hơn: 5 giây hình ở tốc độ 1,2 cần 6 giây nguồn
            toi_da = ((shot["end"] if loai == "broll" else clip["duration"]) - t0) / toc
            doan.append({"n": len(doan) + 1, "muc": muc["id"], "ten_muc": muc.get("ten", ""),
                         "shot": sid, "clip": clip["idx"], "file": clip["file"], "name": clip["name"],
                         "in": round(t0, 2), "out": round(t1, 2), "dur": round(t1 - t0, 2),
                         "co": c.get("co"), "loai": loai, "ly_do": c.get("ly_do", ""),
                         "hinh": c.get("hinh"), "toc_do": toc,
                         "_max": round(min(toi_da, BROLL_MAX if loai == "broll" else toi_da), 2)})
    return doan, loi


def kiem_luat(doan: list[dict], bang: dict) -> list[str]:
    loi = []
    if doan and doan[0]["co"] != "toan":
        loi.append(f"đoạn 1 ({doan[0]['shot']}) là cảnh '{doan[0]['co']}' — mở đầu phải có cảnh toàn")
    for d in doan:
        clip, shot = bang[d["shot"]]
        if d["loai"] == "broll" and not (shot["start"] - 0.05 <= d["in"] and d["out"] <= shot["end"] + 0.05):
            loi.append(f"đoạn {d['n']} ({d['shot']}): {d['in']}–{d['out']} trùm qua mốc cắt cảnh "
                       f"(cảnh {shot['start']}–{shot['end']}) — sẽ có cú nhảy hình giữa đoạn")
        if d["loai"] == "phat_bieu" and d["dur"] < PHAT_BIEU_MIN:
            loi.append(f"đoạn {d['n']} ({d['shot']}): phát biểu {d['dur']}s < {PHAT_BIEU_MIN}s — câu nói bị cụt")
    for a, b in zip(doan, doan[1:]):
        if a["clip"] == b["clip"] and a["co"] == b["co"]:
            loi.append(f"đoạn {a['n']}–{b['n']}: cùng clip {a['name']} cùng cỡ '{a['co']}' — nhảy hình")
    return loi


def co_gian(doan: list[dict], target: float) -> tuple[list[dict], str | None]:
    """Kéo/nén b-roll cho khớp độ dài yêu cầu. Phát biểu giữ nguyên, không bao giờ bị cắt ngắn."""
    for _ in range(40):
        tong = sum(d["dur"] for d in doan)
        lech = target - tong
        if abs(lech) <= 0.01:
            break
        mem = [d for d in doan if d["loai"] == "broll"
               and (d["dur"] < d["_max"] - 1e-6 if lech > 0 else d["dur"] > BROLL_MIN + 1e-6)]
        if not mem:
            break
        moi = lech / len(mem)
        for d in mem:
            d["dur"] = round(min(d["_max"], max(BROLL_MIN, d["dur"] + moi)), 2)
            d["out"] = round(d["in"] + d["dur"], 2)
    tong = round(sum(d["dur"] for d in doan), 2)
    pos = 0.0
    for d in doan:
        d["pos"] = round(pos, 2)
        pos += d["dur"]
        d.pop("_max", None)
    if abs(tong - target) > SAI_SO:
        thieu = target - tong
        return doan, (f"tổng {tong}s lệch {thieu:+.1f}s so với yêu cầu {target}s — "
                      + (f"cần thêm khoảng {thieu / 5:.0f} cảnh nữa"
                         if thieu > 0 else f"cần bỏ bớt khoảng {-thieu / 5:.0f} cảnh"))
    return doan, None


def kiem_do_dai(doan: list[dict]) -> list[str]:
    return [f"đoạn {d['n']} ({d['shot']}): b-roll {d['dur']}s ngoài khoảng {BROLL_MIN}–{BROLL_MAX}s"
            for d in doan if d["loai"] == "broll" and not BROLL_MIN - 0.01 <= d["dur"] <= BROLL_MAX + 0.01]


def muc_am(file: str, t: float, cua: float = 0.25) -> float | None:
    """Mức âm trung bình quanh một mốc cắt, dBFS. None khi clip câm hoặc đo không được."""
    # không đặt -v error: volumedetect in kết quả ở mức info
    r = subprocess.run(["ffmpeg", "-hide_banner", "-ss", f"{max(0.0, t - cua):.3f}", "-t", f"{cua * 2:.3f}",
                        "-i", file, "-vn", "-af", "volumedetect", "-f", "null", "-"],
                       text=True, capture_output=True, encoding="utf-8", errors="replace")
    m = re.search(r"mean_volume:\s*(-?[0-9.]+) dB", r.stderr)
    return float(m.group(1)) if m else None


def kiem_tieng_tai_moc(doan: list[dict], nguong: float) -> list[str]:
    """Cảnh báo khi cắt ngay lúc đang có tiếng to — thường là cắt vào giữa câu nói.

    Máy không phân biệt được tiếng nói với tiếng máy nổ; đây là CẢNH BÁO để nghe lại,
    không phải lỗi chặn.
    """
    canh = []
    for d in doan:
        for ten, t in (("vào", d["in"]), ("ra", d["out"])):
            v = muc_am(d["file"], t)
            if v is not None and v > nguong:
                canh.append(f"đoạn {d['n']} ({d['shot']}): mốc {ten} {t}s đang có tiếng {v:.1f} dB "
                            f"> {nguong} dB — nghe lại xem có cắt giữa câu nói không")
    return canh


def bang_duyet(plan: dict) -> str:
    d = ["  #  mục          cảnh   cỡ     loại       vào→ra (clip)      dài   vị trí   lý do",
         "  " + "-" * 104]
    for s in plan["segments"]:
        d.append(f"  {s['n']:>2}  {s['muc'][:12]:<12}  {s['shot']:<5}  {s['co'] or '?':<5}  "
                 f"{s['loai']:<9}  {s['in']:>6.2f}→{s['out']:<6.2f}  {s['dur']:>5.2f}  "
                 f"{s['pos']:>6.2f}   {s['ly_do'][:34]}")
    d.append(f"  Tổng {plan['tong']}s / yêu cầu {plan['target']}s — {len(plan['segments'])} đoạn")
    return "\n".join(d)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("rushes", type=Path)
    ap.add_argument("chon", type=Path)
    ap.add_argument("--target", type=float, required=True, help="độ dài người dùng yêu cầu, tính bằng giây")
    ap.add_argument("--out", type=Path, default=Path("edit-plan.json"))
    ap.add_argument("--approved", action="store_true",
                    help="người dùng đã yêu cầu/cho phép tự động cắt ghép trong yêu cầu hiện tại")
    ap.add_argument("--khuon", type=Path, help="khuon.json — bắt buộc khi cảnh có kiểu hình")
    ap.add_argument("--kiem-tieng", action="store_true", help="đo mức âm tại mốc vào/ra (cần ffmpeg)")
    ap.add_argument("--nguong-tieng", type=float, default=-30.0, help="dBFS, trên mức này thì cảnh báo")
    a = ap.parse_args()
    if a.target <= 0:
        raise SystemExit("--target phải lớn hơn 0 giây")
    rushes = json.loads(a.rushes.read_text(encoding="utf-8"))
    chon = json.loads(a.chon.read_text(encoding="utf-8"))
    bang = nap(rushes)
    khuon = json.loads(a.khuon.read_text(encoding="utf-8")) if a.khuon else None
    doan, loi = dung_doan(chon, bang, khuon)
    if not doan:
        raise SystemExit("Không có đoạn nào hợp lệ")
    loi += kiem_luat(doan, bang)
    doan, loi_dai = co_gian(doan, a.target)
    loi += kiem_do_dai(doan)
    if loi_dai:
        loi.append(loi_dai)
    plan = {"tieu_de": chon.get("tieu_de", ""), "target": a.target,
            "tong": round(sum(d["dur"] for d in doan), 2), "cut_authorized": bool(a.approved),
            "valid": not loi,
            "segments": doan}
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
    print(bang_duyet(plan))
    for x in (kiem_tieng_tai_moc(doan, a.nguong_tieng) if a.kiem_tieng else []):
        print("CẢNH BÁO ", x)
    for x in loi:
        print("LỖI      ", x)
    print(f"{'FAIL' if loi else 'PASS'} -> {a.out}")
    if not loi and not a.approved:
        print("Đưa bảng trên cho người dùng duyệt TRƯỚC khi chạy assemble.py.")
    elif not loi:
        print("Yêu cầu hiện tại đã cho phép tự động cắt ghép; có thể chạy assemble.py.")
    return 1 if loi else 0


if __name__ == "__main__":
    raise SystemExit(main())
