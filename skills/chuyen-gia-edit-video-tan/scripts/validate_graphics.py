#!/usr/bin/env python3
"""Kiểm đồ hoạ tự động theo manifest (broadcast_kit.py render/demo sinh ra) trước khi render.

    python validate_graphics.py manifest.json [--video VIDEO] [--scenes scenes.json]
                                [--protect x,y,w,h ...] [--frames DIR]

LỖI (exit 1): ra ngoài vùng an toàn · che mặt/vùng bảo vệ · chữ nhỏ hơn mức tối thiểu ·
tương phản < 4,5:1 · logo méo > 2% · tin khẩn thiếu verified/source · trùng id ·
hai đồ hoạ đè nhau cùng lúc · banner tràn qua mốc cắt cảnh.
CẢNH BÁO: chữ quá dài để đọc kịp trong thời gian hiện.

--video: tự dò mặt (OpenCV Haar) ở giữa khung giờ của từng đồ hoạ — thay cho việc chỉ xem mắt.
--frames: xuất khung giữa mỗi đồ hoạ, vẽ khung đồ hoạ (đỏ) và mặt dò được (vàng) để duyệt nhanh.
Dò mặt có thể sót mặt nghiêng/nhỏ; vẫn phải xem ảnh ở --frames.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from broadcast_kit import FRAMES, STYLES, safe_rect  # noqa: E402

TRAN_NGANG = {"breaking_bar", "status_bar", "ticker_strip", "end_card"}   # được phép tràn hết bề ngang
BO_QUA_MAT = {"end_card"}                                                # thẻ toàn khung, không có người
DAI_TOI_DA = 70


def _lum(hexc: str) -> float:
    def kenh(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    h = hexc.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * kenh(r) + 0.7152 * kenh(g) + 0.0722 * kenh(b)


def contrast(fg: str, bg: str) -> float:
    a, b = sorted((_lum(fg), _lum(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def giao(a, b) -> bool:
    return a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]


def faces_at(video: str, t: float, scale: float) -> list[tuple[int, int, int, int]]:
    import cv2
    cap = cv2.VideoCapture(video)
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, fr = cap.read()
    if not ok:
        return []
    gray = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    cc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    found = cc.detectMultiScale(gray, 1.1, 5, minSize=(int(fr.shape[0] * .05),) * 2)
    out = []
    for x, y, w, h in found:          # nới 15% để tính cả tóc và cằm
        m = .15
        out.append(tuple(int(v / scale) for v in (x - w * m, y - h * m, w * (1 + 2 * m), h * (1 + 2 * m))))
    return out


def validate(man: dict, video: str | None = None, cuts: list[float] | None = None,
             protect: list[tuple] = ()) -> tuple[list[str], list[str], dict]:
    aspect = man.get("aspect", "16:9")
    W, H = FRAMES[aspect]
    sx0, sy0, sx1, sy1 = safe_rect(aspect)
    chung = STYLES["chung"]
    min_px = chung["co_chu_toi_thieu_px_1080"] * H / 1080
    loi, canh, mat = [], [], {}
    ids = [it["id"] for it in man["items"]]
    for d in {i for i in ids if ids.count(i) > 1}:
        loi.append(f"trùng id '{d}'")
    scale = 1.0
    if video:
        r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width",
                            "-of", "csv=p=0", video], capture_output=True, text=True, check=True)
        scale = int(r.stdout.strip()) / W
    for it in man["items"]:
        i, box = it["id"], (it["x"], it["y"], it["w"], it["h"])
        if it["type"] in TRAN_NGANG:
            if it["y"] < 0 or it["y"] + it["h"] > H:
                loi.append(f"{i}: ra ngoài khung theo chiều dọc")
        elif not (sx0 <= it["x"] and sy0 <= it["y"] and it["x"] + it["w"] <= sx1 and it["y"] + it["h"] <= sy1):
            loi.append(f"{i}: ra ngoài vùng an toàn {aspect} ({sx0},{sy0})–({sx1},{sy1})")
        if it.get("font_px", 999) < min_px:
            loi.append(f"{i}: chữ {it['font_px']}px < tối thiểu {min_px:.0f}px")
        if it.get("fg") and it.get("bg") and (c := contrast(it["fg"], it["bg"])) < chung["tuong_phan_toi_thieu"]:
            loi.append(f"{i}: tương phản {c:.2f}:1 < {chung['tuong_phan_toi_thieu']}:1 ({it['fg']} trên {it['bg']})")
        if it.get("src_w") and it.get("src_h"):
            lech = abs((it["w"] / it["h"]) / (it["src_w"] / it["src_h"]) - 1)
            if lech > .02:
                loi.append(f"{i}: logo bị kéo méo {lech:.1%}")
        if it["type"] == "breaking_bar" and it.get("style") == "urgent-alert" and not (it.get("verified") and it.get("source")):
            loi.append(f"{i}: tin khẩn chưa xác minh (thiếu verified/source)")
        text, dai = it.get("text", ""), it.get("end", 0) - it.get("start", 0)
        if it["type"] != "ticker_strip" and len(text) > DAI_TOI_DA:
            canh.append(f"{i}: chữ {len(text)} ký tự — rút gọn dưới {DAI_TOI_DA}")
        if dai > 0 and it["type"] not in ("ticker_strip", "end_card") and len(text) / dai > 15:
            canh.append(f"{i}: {len(text)} ký tự trong {dai:.1f}s — không kịp đọc (> 15 ký tự/giây)")
        if cuts:
            cat = [c for c in cuts if it["start"] < c < it["end"]]
            if cat and it["type"] in ("lower_third", "headline_strap", "chip", "label_chip", "source_strap"):
                loi.append(f"{i}: tràn qua mốc cắt cảnh {cat[0]}s")
        vung = [("vùng bảo vệ", p) for p in protect]
        if video and it["type"] not in BO_QUA_MAT:
            mat[i] = faces_at(video, (it["start"] + it["end"]) / 2, scale)
            vung += [("mặt người", f) for f in mat[i]]
        for ten, v in vung:
            if giao(box, v):
                loi.append(f"{i}: che {ten} tại {tuple(int(x) for x in v)}")
    for k, a in enumerate(man["items"]):
        for b in man["items"][k + 1:]:
            if a["start"] < b["end"] and b["start"] < a["end"] and giao((a["x"], a["y"], a["w"], a["h"]),
                                                                        (b["x"], b["y"], b["w"], b["h"])):
                loi.append(f"{a['id']} và {b['id']}: đè nhau cùng lúc")
    return loi, canh, mat


def frames(man: dict, video: str, out: Path, mat: dict) -> None:
    from PIL import Image, ImageDraw
    out.mkdir(parents=True, exist_ok=True)
    W, H = FRAMES[man.get("aspect", "16:9")]
    for it in man["items"]:
        p = out / f"{it['id']}.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str((it["start"] + it["end"]) / 2), "-i", video,
                        "-frames:v", "1", "-vf", f"scale={W}:{H}", str(p)], check=True)
        im = Image.open(p).convert("RGB")
        d = ImageDraw.Draw(im)
        d.rectangle([it["x"], it["y"], it["x"] + it["w"], it["y"] + it["h"]], outline=(255, 40, 40), width=4)
        for x, y, w, h in mat.get(it["id"], []):
            d.rectangle([x, y, x + w, y + h], outline=(255, 220, 0), width=4)
        im.save(p)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest", type=Path)
    ap.add_argument("--video")
    ap.add_argument("--scenes", type=Path)
    ap.add_argument("--protect", nargs="*", default=[], help="x,y,w,h vùng không được che (tay, micro, màn hình)")
    ap.add_argument("--frames", type=Path)
    a = ap.parse_args()
    man = json.loads(a.manifest.read_text(encoding="utf-8"))
    cuts = json.loads(a.scenes.read_text(encoding="utf-8"))["cuts"] if a.scenes else None
    loi, canh, mat = validate(man, a.video, cuts, [tuple(int(v) for v in p.split(",")) for p in a.protect])
    for x in loi:
        print("LỖI      ", x)
    for x in canh:
        print("CẢNH BÁO ", x)
    if a.frames and a.video:
        frames(man, a.video, a.frames, mat)
        print("khung duyệt:", a.frames)
    print(f"{'FAIL' if loi else 'PASS'} — {len(man['items'])} đồ hoạ, {len(loi)} lỗi, {len(canh)} cảnh báo")
    return 1 if loi else 0


if __name__ == "__main__":
    raise SystemExit(main())
