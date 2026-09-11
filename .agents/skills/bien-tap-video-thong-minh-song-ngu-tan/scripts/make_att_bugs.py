#!/usr/bin/env python3
"""Tạo logo góc ATT NEWS và cụm icon Facebook/Zalo cho phong cách ATT NEWS.

Xem references/phong-cach-att-news.md. Màu lấy từ khung hình gốc của kênh.

    python make_att_bugs.py --out-dir thu_muc_lam_viec
"""
from __future__ import annotations
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT_DAM = "C:/Windows/Fonts/arialbd.ttf"

NEN_ATT = (232, 242, 244, 255)
NEN_NEWS = (0, 28, 100, 255)
MAU_ATT = [(206, 32, 39, 255), (0, 122, 61, 255), (26, 60, 170, 255)]
MAU_FB = (24, 119, 242, 255)
MAU_ZALO = (0, 104, 255, 255)


def _font(co: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(FONT_DAM, co)
    except OSError:
        return ImageFont.truetype("arialbd.ttf", co)


def _giua(d: ImageDraw.ImageDraw, hop, chu, font, mau, lech_y=0):
    x0, y0, x1, y1 = hop
    l, t, r, b = d.textbbox((0, 0), chu, font=font)
    d.text((x0 + (x1 - x0 - (r - l)) / 2 - l,
            y0 + (y1 - y0 - (b - t)) / 2 - t + lech_y), chu, font=font, fill=mau)


def logo_att(cao: int = 78) -> Image.Image:
    f_att = _font(round(cao * 0.59))
    f_news = _font(round(cao * 0.51))
    do = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    rong_chu = [do.textlength(c, font=f_att) for c in "ATT"]
    dem = round(cao * 0.17)
    bk = max(3, round(cao * 0.064))
    r_att = int(sum(rong_chu)) + dem * 2
    r_news = int(do.textlength("NEWS", font=f_news)) + dem * 2 + 6
    im = Image.new("RGBA", (r_att + r_news, cao), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([r_att - bk, 0, im.width - 1, cao - 1], radius=bk, fill=NEN_NEWS)
    _giua(d, (r_att, 0, im.width, cao), "NEWS", f_news, (255, 255, 255, 255))
    d.rounded_rectangle([0, 0, r_att - 1, cao - 1], radius=bk, fill=NEN_ATT)
    d.rounded_rectangle([0, 0, r_att - 1, cao - 1], radius=bk,
                        outline=(255, 255, 255, 255), width=2)
    l0, t0, r0, b0 = d.textbbox((0, 0), "A", font=f_att)
    y = (cao - (b0 - t0)) / 2 - t0
    x = dem
    for i, c in enumerate("ATT"):
        d.text((x, y), c, font=f_att, fill=MAU_ATT[i])
        x += rong_chu[i]
    return im


def _huy_hieu(chu, nen, rong, cao, co_chu, lech_y=0):
    im = Image.new("RGBA", (rong, cao), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, rong - 1, cao - 1], radius=max(3, round(cao * 0.23)), fill=nen)
    _giua(d, (0, 0, rong, cao), chu, _font(co_chu), (255, 255, 255, 255), lech_y)
    return im


def icon_mxh(cao: int = 62) -> Image.Image:
    """Huy hiệu chữ, không sao chép tạo hình logo gốc của hai nền tảng."""
    ke = round(cao * 0.23)
    fb = _huy_hieu("f", MAU_FB, cao, cao, round(cao * 0.71), -round(cao * 0.03))
    za = _huy_hieu("Zalo", MAU_ZALO, round(cao * 1.9), cao, round(cao * 0.48))
    im = Image.new("RGBA", (fb.width + ke + za.width, cao), (0, 0, 0, 0))
    im.paste(fb, (0, 0), fb)
    im.paste(za, (fb.width + ke, 0), za)
    return im


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", type=Path, default=Path("."))
    ap.add_argument("--logo-height", type=int, default=78)
    ap.add_argument("--icon-height", type=int, default=62)
    a = ap.parse_args()
    a.out_dir.mkdir(parents=True, exist_ok=True)
    att = logo_att(a.logo_height)
    ico = icon_mxh(a.icon_height)
    att.save(a.out_dir / "att_news.png")
    ico.save(a.out_dir / "icons.png")
    print(f"att_news.png {att.width}x{att.height}")
    print(f"icons.png    {ico.width}x{ico.height}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
