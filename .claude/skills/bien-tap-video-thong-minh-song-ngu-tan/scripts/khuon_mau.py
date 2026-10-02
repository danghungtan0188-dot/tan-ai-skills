#!/usr/bin/env python3
"""Lấy khuôn từ video đã dựng rồi áp cho video mới — khỏi chỉnh lại kiểu chữ, logo, màu từ đầu.

    # 1. trích khuôn từ project cũ
    python khuon_mau.py trich --ass cu/cap.song-ngu.ass --ass cu/lt.ass \
        --lenh cu/lenh-render.txt --out khuon-att.json

    # 2. áp cho video mới
    python khuon_mau.py ap khuon-att.json --cues moi/bilingual.json --out-ass moi/cap.ass
    python khuon_mau.py lenh khuon-att.json moi/rough.mp4 moi/final.mp4

`trich` đọc **style thật** trong file ASS cũ (font, cỡ, màu chữ, màu viền, độ dày viền, canh lề,
MarginV) và các tham số đã dùng trong dòng lệnh render cũ (vị trí thẻ TV, logo phụ, outro, LUFS,
chuỗi lọc âm). Không đoán từ ảnh — chỉ đọc cái đã ghi ra file.

`ap` sinh ASS mới **giữ nguyên khối style cũ**, chỉ thay lời. `lenh` in lại lệnh render_att.py với
đúng tham số cũ.

Khuôn giữ thứ **lặp lại ở mọi video**: kiểu chữ, màu, vị trí, logo, intro/outro, bộ lọc.
Thứ phải chỉnh theo từng đoạn — tốc độ, zoom, scale, chọn cảnh — không nằm trong khuôn.
"""
from __future__ import annotations
import argparse
import json
import re
import shlex
from pathlib import Path

# Chuyển động khung hình dùng lại được. Thứ này phụ thuộc nội dung từng đoạn nên KHÔNG
# tự áp — phải gọi tên trong chon-canh.json. Hỏng hình thì bỏ tên đi là xong.
HINH_SAN = {
    "tinh":      {"zoom_tu": 1.0,  "zoom_den": 1.0,  "day": "giua", "toc_do": 1.0},
    "zoom_cham": {"zoom_tu": 1.0,  "zoom_den": 1.08, "day": "giua", "toc_do": 1.0},
    "zoom_ra":   {"zoom_tu": 1.08, "zoom_den": 1.0,  "day": "giua", "toc_do": 1.0},
    "day_phai":  {"zoom_tu": 1.08, "zoom_den": 1.08, "day": "trai_sang_phai", "toc_do": 1.0},
    "day_trai":  {"zoom_tu": 1.08, "zoom_den": 1.08, "day": "phai_sang_trai", "toc_do": 1.0},
    "nhanh_12":  {"zoom_tu": 1.0,  "zoom_den": 1.0,  "day": "giua", "toc_do": 1.2},
    "cham_80":   {"zoom_tu": 1.0,  "zoom_den": 1.0,  "day": "giua", "toc_do": 0.8},
}
TOC_DO_MIN, TOC_DO_MAX = 0.5, 2.0      # giới hạn của atempo

LENH_GIU = ("--card-pos", "--extra-logo", "--outro-dir", "--bugs-dir", "--audio-pre",
            "--lufs", "--tp", "--card", "--card-video")


def doc_ass(p: Path) -> dict:
    """Đọc PlayRes + nguyên khối [V4+ Styles] của một file ASS."""
    text = p.read_text(encoding="utf-8")
    res = {k: int(v) for k, v in re.findall(r"^PlayRes([XY]):\s*(\d+)", text, re.M)}
    fmt = re.search(r"^Format:\s*(Name.*)$", text, re.M)
    styles = re.findall(r"^Style:\s*(.+)$", text, re.M)
    if not fmt or not styles:
        raise SystemExit(f"{p.name}: không thấy khối [V4+ Styles]")
    ten = [s.split(",", 1)[0].strip() for s in styles]
    return {"file": p.name, "width": res.get("X"), "height": res.get("Y"),
            "format": fmt.group(1).strip(), "styles": [s.strip() for s in styles], "ten_style": ten}


def doc_lenh(p: Path) -> dict:
    """Nhặt các tham số dùng lại được từ dòng lệnh render cũ đã lưu."""
    arg = shlex.split(p.read_text(encoding="utf-8").replace("\\\n", " "), posix=False)
    ra = {}
    for i, x in enumerate(arg):
        if x in LENH_GIU and i + 1 < len(arg):
            ra[x] = arg[i + 1].strip('"')
    return ra


def trich(ass: list[Path], lenh: Path | None, ghi_chu: str, hinh: dict | None = None) -> dict:
    return {"ghi_chu": ghi_chu, "ass": [doc_ass(p) for p in ass],
            "lenh": doc_lenh(lenh) if lenh else {},
            "hinh": hinh if hinh is not None else dict(HINH_SAN)}


def lay_hinh(khuon: dict, ten: str) -> dict:
    h = (khuon.get("hinh") or HINH_SAN).get(ten)
    if h is None:
        co = ", ".join(sorted(khuon.get("hinh") or HINH_SAN))
        raise SystemExit(f"Khuôn không có kiểu hình '{ten}'. Có: {co}")
    t = float(h.get("toc_do", 1.0))
    if not TOC_DO_MIN <= t <= TOC_DO_MAX:
        raise SystemExit(f"'{ten}': tốc độ {t} ngoài khoảng {TOC_DO_MIN}–{TOC_DO_MAX}")
    return h


def loc_hinh(h: dict, giay: float, W: int, H: int, fps: int) -> str:
    """Chuỗi lọc hình cho một đoạn. Trả chuỗi rỗng khi đoạn đó không có chuyển động.

    Zoom/đẩy dùng zoompan vì crop không đổi được kích thước theo từng khung.
    Tốc độ đổi bằng setpts; đoạn vẫn dài đúng `giay` vì lấy thêm/bớt vật liệu ở nguồn.
    """
    z0, z1 = float(h.get("zoom_tu", 1.0)), float(h.get("zoom_den", 1.0))
    toc = float(h.get("toc_do", 1.0))
    loc = []
    if abs(z0 - 1.0) > 1e-3 or abs(z1 - 1.0) > 1e-3:
        n = max(1, round(giay * toc * fps))      # số khung NGUỒN mà zoompan đi qua
        z = f"{z0}" if abs(z1 - z0) < 1e-6 else f"{z0}+({z1}-{z0})*on/{n}"
        day = h.get("day", "giua")
        if day == "trai_sang_phai":
            x = f"(iw-iw/zoom)*on/{n}"
        elif day == "phai_sang_trai":
            x = f"(iw-iw/zoom)*(1-on/{n})"
        else:
            x = "iw/2-(iw/zoom/2)"
        # zoompan sinh PTS sai hẳn (một đoạn 4 giây ra 4096 giây) — phải dựng lại mốc theo số khung
        loc.append(f"zoompan=z='{z}':d=1:x='{x}':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={fps}")
        loc.append(f"setpts=N/{fps}/TB")
    if abs(toc - 1.0) > 1e-3:                    # đổi tốc độ SAU khi mốc đã đúng
        loc.append(f"setpts=PTS/{toc}")
    return ",".join(loc)


def loc_tieng(h: dict) -> str:
    toc = float(h.get("toc_do", 1.0))
    return "" if abs(toc - 1.0) < 1e-3 else f"atempo={toc}"


def chon_ass(khuon: dict, ten_file: str | None) -> dict:
    if ten_file:
        for a in khuon["ass"]:
            if a["file"] == ten_file:
                return a
        raise SystemExit(f"Khuôn không có ass '{ten_file}'. Có: " +
                         ", ".join(a["file"] for a in khuon["ass"]))
    return khuon["ass"][0]


def ts(v: float) -> str:
    cs = round(float(v) * 100)
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def esc(s: object) -> str:
    return str(s).replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}").replace("\n", "\\N")


def ap(khuon: dict, segs: list[dict], ten_file: str | None = None) -> str:
    a = chon_ass(khuon, ten_file)
    thieu = [t for t in ("EN", "VI") if t not in a["ten_style"]]
    if thieu:
        raise SystemExit(f"Khuôn {a['file']} thiếu style {thieu} — chỉ áp được cho phụ đề song ngữ")
    head = ("[Script Info]\nScriptType: v4.00+\n"
            f"PlayResX: {a['width']}\nPlayResY: {a['height']}\n"
            "WrapStyle: 0\nScaledBorderAndShadow: yes\n\n"
            f"[V4+ Styles]\nFormat: {a['format']}\n"
            + "\n".join(f"Style: {s}" for s in a["styles"])
            + "\n\n[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n")
    rows = []
    for i, x in enumerate(segs):
        if not x.get("en") or not x.get("vi"):
            raise SystemExit(f"Cue {i} thiếu một ngôn ngữ")
        if float(x["start"]) >= float(x["end"]):
            raise SystemExit(f"Cue {i} mốc thời gian không hợp lệ")
        for lop, ten, chu in ((0, "EN", x["en"]), (1, "VI", x["vi"])):
            rows.append(f"Dialogue: {lop},{ts(x['start'])},{ts(x['end'])},{ten},,0,0,0,,{esc(chu)}")
    return head + "\n".join(rows) + "\n"


def lenh_render(khuon: dict, inp: str, out: str, them: list[str]) -> list[str]:
    cmd = ["python", "scripts/render_att.py", inp]
    for k, v in khuon["lenh"].items():
        cmd += [k, v]
    return cmd + them + ["--out", out]


def main() -> int:
    ap_ = argparse.ArgumentParser()
    sub = ap_.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("trich", help="lấy khuôn từ project cũ")
    t.add_argument("--ass", type=Path, action="append", required=True, help="lặp lại được nhiều lần")
    t.add_argument("--lenh", type=Path, help="file text chứa dòng lệnh render_att.py đã dùng")
    t.add_argument("--ghi-chu", default="")
    t.add_argument("--hinh", type=Path, help="JSON kiểu chuyển động riêng; bỏ trống thì dùng bộ sẵn")
    t.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("ap", help="áp khuôn cho cue mới")
    p.add_argument("khuon", type=Path)
    p.add_argument("--cues", type=Path, required=True, help="bilingual.json")
    p.add_argument("--ass-goc", help="tên file ass trong khuôn muốn dùng")
    p.add_argument("--out-ass", type=Path, required=True)
    h = sub.add_parser("hinh", help="in chuỗi lọc của một kiểu chuyển động")
    h.add_argument("khuon", type=Path)
    h.add_argument("--ten", required=True)
    h.add_argument("--giay", type=float, required=True)
    h.add_argument("--size", default="1920x1080")
    h.add_argument("--fps", type=int, default=30)
    l = sub.add_parser("lenh", help="in lại lệnh render với tham số cũ")
    l.add_argument("khuon", type=Path)
    l.add_argument("input")
    l.add_argument("output")
    l.add_argument("--them", nargs=argparse.REMAINDER, default=[])
    a = ap_.parse_args()

    if a.cmd == "trich":
        k = trich(a.ass, a.lenh, a.ghi_chu,
                  json.loads(a.hinh.read_text(encoding="utf-8")) if a.hinh else None)
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(json.dumps(k, ensure_ascii=False, indent=1), encoding="utf-8")
        for x in k["ass"]:
            print(f"  {x['file']}: {x['width']}x{x['height']}, style " + ", ".join(x["ten_style"]))
        print(f"  lệnh: {k['lenh'] or 'không có'}")
        print("  kiểu hình: " + ", ".join(sorted(k["hinh"])))
        print("->", a.out)
        return 0
    khuon = json.loads(a.khuon.read_text(encoding="utf-8"))
    if a.cmd == "hinh":
        W, H = (int(v) for v in a.size.split("x"))
        kieu = lay_hinh(khuon, a.ten)
        print("video:", loc_hinh(kieu, a.giay, W, H, a.fps) or "(không đổi)")
        print("tiếng:", loc_tieng(kieu) or "(không đổi)")
        print(f"vật liệu cần ở nguồn: {a.giay * float(kieu.get('toc_do', 1.0)):.2f}s")
        return 0
    if a.cmd == "ap":
        d = json.loads(a.cues.read_text(encoding="utf-8"))
        a.out_ass.parent.mkdir(parents=True, exist_ok=True)
        a.out_ass.write_text(ap(khuon, d.get("segments", []), a.ass_goc), encoding="utf-8")
        print(a.out_ass)
        return 0
    print(" ".join(shlex.quote(x) for x in lenh_render(khuon, a.input, a.output, a.them)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
