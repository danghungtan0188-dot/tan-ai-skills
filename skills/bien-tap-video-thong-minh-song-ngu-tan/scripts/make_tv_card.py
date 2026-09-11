#!/usr/bin/env python3
"""Thẻ ảnh đặt vào màn hình TV của trường quay ATT NEWS (phần MC dẫn).

    python make_tv_card.py ANH.jpg --label "AN THẠNH THỦY · 7–8/9/2026" \
        --title "KHÁM SỨC KHỎE" "ĐỊNH KỲ, SÀNG LỌC" "CHO 2.500 NGƯỜI DÂN" \
        --footer "Trạm Y tế xã" "An Thạnh Thủy" --out screen_card.png [--preview studio.png]

Khung TV đo pixel ở 1920×1080, phông dùng chung mọi bản tin: màn hình x 889–1920,
y 231–646 (mép dưới bị bàn dẫn che). Thẻ 1000×394 đặt tại CARD_POS, chỉ hiện trước studio_end.
Ảnh phủ phần phải 600×394 — ảnh 3:2 chỉ xén ~1,5%, không cắt đầu người.
Dòng tiêu đề cuối in nhỏ hơn; mọi dòng tự thu nhỏ cho lọt panel.
Footer đừng lặp ý đã có trên màn hình (video 06 bị trùng "Chào mừng Quốc khánh" với banner đỏ).
"""
from __future__ import annotations
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

CARD_POS = (900, 240)
W, H, PANEL, PAD = 1000, 394, 400, 26
BOLD, REG = "C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"
NAVY, NAVY2, VANG, DO = (0, 28, 100), (12, 58, 148), (255, 205, 45), (198, 22, 30)


def _vua(chu: str, co: int, rong: int, path: str = BOLD) -> ImageFont.FreeTypeFont:
    do = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    while co > 16 and do.textlength(chu, font=ImageFont.truetype(path, co)) > rong:
        co -= 1
    return ImageFont.truetype(path, co)


def make_card(image: Path, label: str, title: list[str], footer: list[str]) -> Image.Image:
    im = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (PANEL, y)], fill=tuple(round(NAVY[i] + (NAVY2[i] - NAVY[i]) * t) for i in range(3)))
    w_anh = W - PANEL
    a = Image.open(image).convert("RGB")
    ty = max(w_anh / a.width, H / a.height)
    a = a.resize((round(a.width * ty), round(a.height * ty)), Image.LANCZOS)
    ox, oy = (a.width - w_anh) // 2, (a.height - H) // 2
    im.paste(a.crop((ox, oy, ox + w_anh, oy + H)), (PANEL, 0))

    rong = PANEL - PAD * 2
    d.rectangle([0, 0, 5, H], fill=DO)
    y = 40
    d.text((PAD, y), label, font=_vua(label, 21, rong), fill=VANG)
    y += 46
    for k, dong in enumerate(title):
        font = _vua(dong, 31 if k == len(title) - 1 and len(title) > 1 else 40, rong)
        d.text((PAD, y), dong, font=font, fill=(255, 255, 255))
        y += font.size + 14
    if footer:
        d.line([(PAD, y + 8), (PAD + 120, y + 8)], fill=VANG, width=4)
        y += 30
        for dong in footer:
            d.text((PAD, y), dong, font=_vua(dong, 22, rong, REG), fill=(206, 220, 245))
            y += 28
    d.rectangle([0, 0, W - 1, H - 1], outline=(236, 244, 252), width=3)
    return im


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("image", type=Path)
    ap.add_argument("--label", required=True)
    ap.add_argument("--title", nargs="+", required=True)
    ap.add_argument("--footer", nargs="*", default=[])
    ap.add_argument("--out", type=Path, default=Path("screen_card.png"))
    ap.add_argument("--preview", type=Path, help="khung trường quay 1920×1080 để ghép thử")
    a = ap.parse_args()
    card = make_card(a.image, a.label, a.title, a.footer)
    card.save(a.out)
    print(a.out, card.size)
    if a.preview:
        nen = Image.open(a.preview).convert("RGB").resize((1920, 1080))
        nen.paste(card, CARD_POS)
        xem = a.out.with_name(a.out.stem + "_xem.png")
        nen.resize((960, 540)).save(xem)
        print("ghép thử:", xem)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
