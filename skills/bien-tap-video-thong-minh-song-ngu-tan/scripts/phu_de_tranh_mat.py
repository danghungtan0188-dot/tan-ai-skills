#!/usr/bin/env python3
"""Dời phụ đề khỏi mặt người: dò mặt suốt video, cue nào đè lên mặt thì đặt lại.

    python phu_de_tranh_mat.py VIDEO captions.ass [--out captions.tranh-mat.ass]

Thứ tự thử cho mỗi cue đè mặt: dưới cằm → trên đầu → thu nhỏ chữ (tới 70%) rồi thử lại.
Không chỗ nào đủ (mặt chiếm gần hết khung) thì giữ cỡ chữ, hạ sát đáy vùng an toàn và báo
"VẪN CHE" — xem lại khung đó bằng mắt, cân nhắc cắt cảnh rộng hơn.
Chỉ đụng cue căn đáy (Alignment 1–3) không có \\pos/\\move; lower-third, chữ đặt tay giữ nguyên.
Các dòng cùng mốc giờ (EN trên + VI dưới) dời cùng nhau, giữ khoảng cách giữa hai dòng.
Dò mặt bằng YuNet (OpenCV, MIT; assets/models/). ASS phải cùng mốc giờ với VIDEO.
Ý tưởng từ kurbaitaev/ghost-editor (face_track + safezone).
"""
from __future__ import annotations

import argparse
import math
import re
from pathlib import Path

MODEL = Path(__file__).resolve().parents[1] / "assets" / "models" / "face_detection_yunet_2023mar.onnx"
BUOC = 0.2  # giây giữa hai lần dò mặt
TOC, CAM = 0.30, 0.03  # nới hộp mặt theo chiều cao mặt: tóc phía trên; hộp YuNet đã gồm cằm nên chỉ nới ít
CACH = 0.015  # khoảng hở giữa phụ đề và mặt (theo chiều cao khung)
AN_TOAN = {"ngang": (0.05, 0.04), "doc": (0.12, 0.10)}  # (trên, dưới): chừa chỗ logo / nút của nền tảng
CO_CHU = (1.0, 0.9, 0.8, 0.7)


def doc_ass(text: str):
    """Trả (PlayResX, PlayResY, styles, các dòng). Mỗi dòng Dialogue: dict có chỉ số dòng trong file."""
    lines = text.splitlines()
    w = int(re.search(r"PlayResX:\s*(\d+)", text).group(1))
    h = int(re.search(r"PlayResY:\s*(\d+)", text).group(1))
    styles, events, fmt_s, fmt_e = {}, [], None, None
    for i, ln in enumerate(lines):
        if ln.startswith("Format:"):
            cols = [c.strip() for c in ln[7:].split(",")]
            if "Fontsize" in cols:
                fmt_s = cols
            else:
                fmt_e = cols
        elif ln.startswith("Style:") and fmt_s:
            v = dict(zip(fmt_s, [c.strip() for c in ln[6:].split(",", len(fmt_s) - 1)]))
            styles[v["Name"]] = {k: float(v[k]) for k in ("Fontsize", "Alignment", "MarginL", "MarginR", "MarginV",
                                                         "Outline", "BorderStyle")}
        elif ln.startswith("Dialogue:") and fmt_e:
            v = dict(zip(fmt_e, ln[9:].split(",", len(fmt_e) - 1)))
            events.append({"i": i, "v": v, "start": giay(v["Start"]), "end": giay(v["End"])})
    return w, h, styles, lines, fmt_e, events


def giay(ts: str) -> float:
    hh, mm, ss = ts.strip().split(":")
    return int(hh) * 3600 + int(mm) * 60 + float(ss)


def hop_chu(ev, st, w, h, ti_le=1.0):
    """Hộp ước lượng (x0, y0, x1, y1) của một dòng phụ đề, đơn vị = PlayRes."""
    fs = st["Fontsize"] * ti_le
    chu = re.sub(r"\{[^}]*\}", "", ev["v"]["Text"]).split("\\N")
    rong = w - st["MarginL"] - st["MarginR"]
    so_dong = sum(max(1, math.ceil(len(c) * 0.55 * fs / rong)) for c in chu)
    dem = st["Outline"] * 2 if st["BorderStyle"] == 3 else st["Outline"]
    cao = so_dong * fs * 1.2 + dem * 2
    ngang = min(rong, max(len(c) for c in chu) * 0.55 * fs) + dem * 2
    mv = float(ev["v"]["MarginV"]) or st["MarginV"]
    day = h - mv
    cx = st["MarginL"] + rong / 2
    return [cx - ngang / 2, day - cao, cx + ngang / 2, day]


def quet_mat(video: str, buoc: float = BUOC) -> list[tuple[float, list[tuple[float, float, float, float]]]]:
    """[(giây, [(x0, y0, x1, y1) chuẩn hoá 0–1 đã nới tóc/cằm])] — đọc tuần tự, chỉ giải mã khung cần dò."""
    import cv2
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    W, H = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    w = 480
    h = round(w * H / W)
    det = cv2.FaceDetectorYN.create(str(MODEL), "", (w, h), 0.7)
    moi = max(1, round(buoc * fps))
    out, n = [], 0
    while cap.grab():
        if n % moi == 0:
            ok, fr = cap.retrieve()
            if ok:
                _, F = det.detect(cv2.resize(fr, (w, h)))
                hop = []
                for x, y, bw, bh in ([] if F is None else F[:, :4]):
                    if bh / h > 0.75:  # mặt phủ gần hết khung: nền mờ phóng to, không né được
                        continue
                    hop.append((x / w, (y - TOC * bh) / h, (x + bw) / w, (y + bh * (1 + CAM)) / h))
                out.append((n / fps, hop))
        n += 1
    if not out:
        raise SystemExit(f"Không đọc được khung hình nào từ {video}")
    return out


def dat_lai(khoi, mat, w, h, doc: bool):
    """khoi: [(ev, style)] cùng mốc giờ. mat: hộp mặt (PlayRes) trong khoảng giờ đó.
    Trả (quyết định, dy, tỉ lệ chữ). dy > 0 là dời xuống."""
    tren, duoi = (v * h for v in AN_TOAN["doc" if doc else "ngang"])
    gap = CACH * h

    def hop(ti_le, dy=0.0):
        bs = [hop_chu(ev, st, w, h, ti_le) for ev, st in khoi]
        return [[b[0], b[1] + dy, b[2], b[3] + dy] for b in bs]

    def de(bs):
        return [m for m in mat for b in bs if b[0] < m[2] and m[0] < b[2] and b[1] < m[3] and m[1] < b[3]]

    if not de(hop(1.0)):
        return "giu", 0.0, 1.0
    for ti_le in CO_CHU:
        bs = hop(ti_le)
        if not de(bs):  # chữ nhỏ lại đã hết đè, không cần dời
            return "thu_nho", 0.0, ti_le
        y0, y1 = min(b[1] for b in bs), max(b[3] for b in bs)
        cham = [m for m in mat if any(b[0] < m[2] and m[0] < b[2] for b in bs)]
        dy = max(m[3] for m in cham) + gap - y0  # dưới cằm
        if y1 + dy <= h - duoi and not de(hop(ti_le, dy)):
            return ("duoi_cam" if ti_le == 1 else "thu_nho"), dy, ti_le
        dy = min(m[1] for m in cham) - gap - y1  # trên đầu
        if y0 + dy >= tren and not de(hop(ti_le, dy)):
            return ("tren_dau" if ti_le == 1 else "thu_nho"), dy, ti_le
    # không né được: giữ cỡ chữ gốc (chữ nhỏ mà vẫn đè thì chỉ tệ hơn), hạ sát đáy vùng an toàn cho đè ít nhất
    dy = max(0.0, h - duoi - max(b[3] for b in hop(1.0)))
    return "van_che", dy, 1.0


def tranh_mat(video: str, ass_in: Path, ass_out: Path, mat_theo_giay=None) -> list[dict]:
    w, h, styles, lines, fmt_e, events = doc_ass(ass_in.read_text(encoding="utf-8-sig"))
    mat_theo_giay = quet_mat(video) if mat_theo_giay is None else mat_theo_giay
    doc = h > w
    khoi: dict[tuple[float, float], list] = {}
    for ev in events:
        st = styles.get(ev["v"]["Style"].strip())
        if st and st["Alignment"] in (1, 2, 3) and not re.search(r"\\(pos|move)\(", ev["v"]["Text"]):
            khoi.setdefault((ev["start"], ev["end"]), []).append((ev, st))
    bao_cao = []
    for (t0, t1), ds in sorted(khoi.items()):
        mat = [(x0 * w, y0 * h, x1 * w, y1 * h) for t, hs in mat_theo_giay if t0 - BUOC <= t <= t1 for x0, y0, x1, y1 in hs]
        qd, dy, ti_le = dat_lai(ds, mat, w, h, doc)
        bao_cao.append({"bat_dau": round(t0, 2), "ket_thuc": round(t1, 2), "quyet_dinh": qd,
                        "doi_px": round(dy), "co_chu": ti_le})
        if qd == "giu":
            continue
        for ev, st in ds:
            v = dict(ev["v"])
            mv = (float(v["MarginV"]) or st["MarginV"]) - dy
            v["MarginV"] = str(max(1, round(mv)))
            if ti_le < 1:
                v["Text"] = f"{{\\fscx{ti_le * 100:.0f}\\fscy{ti_le * 100:.0f}}}" + v["Text"]
            lines[ev["i"]] = "Dialogue:" + ",".join(v[k] for k in fmt_e)
    ass_out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return bao_cao


def chay(video: str, ass: Path, out: Path | None = None) -> Path:
    """Ghi bản tránh mặt cạnh file gốc (*.tranh-mat.ass), in tóm tắt; render.py/render_att.py gọi hàm này."""
    out = out or ass.with_suffix(".tranh-mat.ass")
    bc = tranh_mat(video, ass, out)
    dem = {k: sum(1 for b in bc if b["quyet_dinh"] == k) for k in ("giu", "duoi_cam", "tren_dau", "thu_nho", "van_che")}
    print(f"{out}  ({len(bc)} cue: " + ", ".join(f"{k} {v}" for k, v in dem.items()) + ")")
    for b in bc:
        if b["quyet_dinh"] == "van_che":
            print(f"  VẪN CHE {b['bat_dau']}–{b['ket_thuc']}s: không đủ chỗ, xem lại khung này")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("ass", type=Path)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    chay(a.video, a.ass, a.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
