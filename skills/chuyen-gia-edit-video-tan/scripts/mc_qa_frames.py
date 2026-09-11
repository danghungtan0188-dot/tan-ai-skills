#!/usr/bin/env python3
"""Bảng khung QA cho MC AI / lip-sync: phóng to vùng mặt ở những điểm dễ lộ lỗi nhất.

    python mc_qa_frames.py VIDEO asr_words.json --face x,y,w,h --out qa_mc.jpg [--max 24] [--every 3]

Chọn khung:
- Từ mở đầu bằng b / m / p (môi phải KHÉP hẳn) — lệch lip-sync lộ rõ nhất ở đây. "ph" là âm /f/,
  không khép môi nên bỏ qua.
- Thêm một khung mỗi --every giây để soi mắt, tóc, viền ghép và ánh sáng có trôi theo thời gian.
Mỗi ô ghi mốc giờ + từ. Xem cùng checklist trong references/mc-ai-lip-sync.md.
asr_words.json: từ build_bilingual.py transcribe (skill song ngữ) — [{"s","e","w"}].
"""
from __future__ import annotations
import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def pick(words: list[dict], every: float, limit: int) -> list[tuple[float, str]]:
    moi = [(round(w["s"] + 0.04, 2), w["w"]) for w in words
           if w["w"][:1].lower() in "bmp" and not w["w"].lower().startswith("ph")]
    if words:
        t, end = 0.5, words[-1]["e"]
        while t < end:
            moi.append((round(t, 2), "·"))
            t += every
    moi.sort()
    if len(moi) > limit:                      # rải đều thay vì lấy dồn đầu video
        step = len(moi) / limit
        moi = [moi[int(k * step)] for k in range(limit)]
    return moi


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("words", type=Path)
    ap.add_argument("--face", required=True, help="x,y,w,h vùng mặt MC ở khung gốc")
    ap.add_argument("--out", type=Path, default=Path("qa_mc.jpg"))
    ap.add_argument("--max", type=int, default=24)
    ap.add_argument("--every", type=float, default=3.0)
    a = ap.parse_args()
    x, y, w, h = (int(v) for v in a.face.split(","))
    diem = pick(json.loads(a.words.read_text(encoding="utf-8")), a.every, a.max)
    cao, cot = 260, 6
    rong = round(cao * w / h)
    bang = Image.new("RGB", (cot * rong, ((len(diem) + cot - 1) // cot) * (cao + 28)), (20, 20, 20))
    d = ImageDraw.Draw(bang)
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 18)
    with tempfile.TemporaryDirectory() as tmp:
        for k, (t, tu) in enumerate(diem):
            p = Path(tmp) / f"{k}.png"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", a.video, "-frames:v", "1",
                            "-vf", f"crop={w}:{h}:{x}:{y},scale={rong}:{cao}", str(p)], check=True)
            ox, oy = (k % cot) * rong, (k // cot) * (cao + 28)
            bang.paste(Image.open(p), (ox, oy))
            d.text((ox + 6, oy + cao + 4), f"{t:.2f}s  {tu}", font=f, fill=(255, 220, 80) if tu != "·" else (200, 200, 200))
    bang.save(a.out)
    print(f"{len(diem)} khung -> {a.out}  (vàng = âm môi khép b/m/p, xám = mẫu đều)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
