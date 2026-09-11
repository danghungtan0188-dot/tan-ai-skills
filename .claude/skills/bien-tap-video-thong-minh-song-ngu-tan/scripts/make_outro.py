#!/usr/bin/env python3
"""Outro động ATT NEWS: dãy khung PNG 30 fps để render_att.py nối vào cuối.

    python make_outro.py --title "DÒNG 1" "DÒNG 2" --sub "Địa điểm · Ngày" \
        --logo att_news.png --out-dir outro_frames [--seconds 4]

Nhịp: sáng lên 0,35 s → tiêu đề trượt lên lệch nhịp hai dòng → gạch vàng mở từ giữa →
dòng phụ → dòng kêu gọi trượt từ trái → logo bung (quá đà nhẹ) → like nảy → tối dần 0,35 s.
Nền: chuyển sắc navy, quầng sáng, hạt bay, đường mạch nhấp nháy, sóng trôi, vệt sáng quét.
Đồ hoạ tự dựng bằng công thức; chỉ mượn bố cục, không lấy nhận diện kênh khác.
Outro im lặng — chỉ thêm nhạc khi người dùng đưa bản nhạc có quyền dùng.
"""
from __future__ import annotations
import argparse
import math
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1920, 1080, 30
BOLD, REG = "C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"
NAVY_TREN, NAVY_DUOI = (0, 22, 78), (10, 60, 146)
VANG, XANH_NHAT = (255, 205, 45), (168, 198, 245)
CTA = "Theo dõi ATT NEWS để nhận bản tin của xã mỗi ngày"
CREDIT = "Thực hiện: Hùng Tấn — Trung tâm Cung ứng dịch vụ công xã An Thạnh Thủy"


def f(p: str, s: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(p, s)


def ease_out(t: float) -> float:
    t = min(1.0, max(0.0, t))
    return 1 - (1 - t) ** 3


def ease_back(t: float) -> float:
    t, c = min(1.0, max(0.0, t)), 1.70158
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2


def khoang(t: float, bd: float, dai: float) -> float:
    return ease_out((t - bd) / dai)


def vua(chu: str, co: int, rong: int) -> ImageFont.FreeTypeFont:
    do = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    while co > 20 and do.textlength(chu, font=f(BOLD, co)) > rong:
        co -= 2
    return f(BOLD, co)


def lop_giua(chu: str, font, mau) -> Image.Image:
    im = Image.new("RGBA", (W, 170), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text(((W - d.textlength(chu, font=font)) / 2, 20), chu, font=font, fill=mau)
    return im


def dat(nen: Image.Image, lop: Image.Image, x: float, y: float, alpha: float) -> None:
    if alpha <= 0.003:
        return
    if alpha < 0.999:
        lop = Image.blend(Image.new("RGBA", lop.size, (0, 0, 0, 0)), lop, alpha)
    nen.alpha_composite(lop, (int(x), int(y)))


def ngon_tay(d: ImageDraw.ImageDraw, x: float, y: float, cao: float) -> None:
    b, m = cao / 100, (255, 255, 255, 255)
    d.rounded_rectangle([x, y + 34 * b, x + 22 * b, y + 100 * b], radius=5 * b, fill=m)
    d.rounded_rectangle([x + 28 * b, y + 30 * b, x + 78 * b, y + 100 * b], radius=9 * b, fill=m)
    d.polygon([(x + 30 * b, y + 42 * b), (x + 48 * b, y + 2 * b), (x + 60 * b, y + 4 * b),
               (x + 56 * b, y + 34 * b), (x + 78 * b, y + 34 * b), (x + 78 * b, y + 48 * b)], fill=m)


def render(title: list[str], sub: str, logo: Path, out: Path, seconds: float = 4.0,
           cta: str = CTA, credit: str = CREDIT) -> int:
    out.mkdir(parents=True, exist_ok=True)
    nen_goc = Image.new("RGB", (W, H))
    d0 = ImageDraw.Draw(nen_goc)
    for y in range(H):
        t = y / H
        d0.line([(0, y), (W, y)], fill=tuple(round(NAVY_TREN[i] + (NAVY_DUOI[i] - NAVY_TREN[i]) * t) for i in range(3)))
    nen_goc = nen_goc.convert("RGBA")
    quang = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(quang).ellipse([W / 2 - 700, H / 2 - 430, W / 2 + 700, H / 2 + 430], fill=(40, 110, 220, 70))
    nen_goc.alpha_composite(quang.filter(ImageFilter.GaussianBlur(150)))

    mach, nut, r = Image.new("RGBA", (W, H), (0, 0, 0, 0)), [], random.Random(9)
    dm = ImageDraw.Draw(mach)
    for _ in range(26):
        x, y = r.randrange(0, 780), r.randrange(0, 430)
        for _ in range(r.randrange(2, 4)):
            n = r.randrange(40, 130)
            x2, y2 = (x + n, y) if r.random() < .5 else (x, y + n)
            dm.line([(x, y), (x2, y2)], fill=(120, 180, 255, 48), width=2)
            x, y = x2, y2
        dm.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(150, 205, 255, 75))
        nut.append((x, y))
    rh = random.Random(4)
    hat = [(rh.randrange(0, W), rh.randrange(0, H), rh.uniform(1.4, 3.4), rh.uniform(14, 46), rh.uniform(0, 6.3))
           for _ in range(90)]

    dong = [lop_giua(c, vua(c, 82, 1560), (255, 255, 255, 255)) for c in title[:2]]
    lop_sub = lop_giua(sub, f(REG, 38), XANH_NHAT + (255,))
    lop_cta = Image.new("RGBA", (W, 120), (0, 0, 0, 0))
    dc = ImageDraw.Draw(lop_cta)
    dc.text((150, 8), cta, font=f(BOLD, 40), fill=VANG + (255,))
    dc.text((150, 64), credit, font=f(REG, 26), fill=XANH_NHAT + (255,))
    lg0 = Image.open(logo).convert("RGBA")
    lg0 = lg0.resize((round(lg0.width * 128 / lg0.height), 128), Image.LANCZOS)
    lx, ly = W - 150 - lg0.width, 842

    n_khung = int(FPS * seconds)
    for i in range(n_khung):
        t = i / FPS
        im = nen_goc.copy()
        dyn = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(dyn)
        for k in range(9):
            pha = t * (0.55 + k * 0.08)
            d.line([(x, 860 + k * 22 + (26 + k * 7) * math.sin(x / 300 + k * .45 + pha)) for x in range(0, W + 8, 8)],
                   fill=(120, 190, 255, 40 + k * 4), width=2)
        for hx, hy, hr, hv, hp in hat:
            y = (hy - hv * t) % (H + 60) - 30
            d.ellipse([hx - hr, y - hr, hx + hr, y + hr], fill=(170, 215, 255, max(0, int(60 + 55 * math.sin(t * 1.9 + hp)))))
        im.alpha_composite(dyn)
        im.alpha_composite(mach)
        dn = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ddn = ImageDraw.Draw(dn)
        for j, (nx, ny) in enumerate(nut):
            ddn.ellipse([nx - 6, ny - 6, nx + 6, ny + 6], fill=(170, 220, 255, int(70 + 90 * max(0, math.sin(t * 2.4 + j * 0.7)))))
        im.alpha_composite(dn.filter(ImageFilter.GaussianBlur(2)))
        if t < 1.3:
            cx = -400 + t / 1.3 * (W + 800)
            vs = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(vs).polygon([(cx, 0), (cx + 190, 0), (cx - 70, H), (cx - 260, H)], fill=(255, 255, 255, 26))
            im.alpha_composite(vs.filter(ImageFilter.GaussianBlur(28)))
        for k, lop in enumerate(dong):
            a = khoang(t, 0.20 + 0.15 * k, 0.60)
            dat(im, lop, 0, 302 + 112 * k + (1 - a) * 46, a)
        a3 = khoang(t, 0.62, 0.45)
        if a3 > 0:
            ImageDraw.Draw(im).line([(W / 2 - 92 * a3, 558), (W / 2 + 92 * a3, 558)], fill=VANG + (255,), width=5)
        a4 = khoang(t, 0.80, 0.50)
        dat(im, lop_sub, 0, 566 + (1 - a4) * 18, a4)
        a5 = khoang(t, 1.05, 0.55)
        dat(im, lop_cta, -70 + 70 * a5, 898, a5)
        a6 = min(1.0, max(0.0, (t - 1.15) / 0.55))
        if a6 > 0:
            s = 0.72 + 0.28 * ease_back(a6)
            lw, lh = max(2, round(lg0.width * s)), max(2, round(lg0.height * s))
            dat(im, lg0.resize((lw, lh), Image.LANCZOS), lx + (lg0.width - lw) / 2, ly + (lg0.height - lh) / 2, min(1.0, a6 * 1.6))
        a7 = min(1.0, max(0.0, (t - 1.45) / 0.45))
        if a7 > 0:
            lt = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ngon_tay(ImageDraw.Draw(lt), lx + lg0.width - 74, ly + 116 + (1 - ease_back(a7)) * 26, 92)
            im.alpha_composite(lt)
        kh = min(1.0, t / 0.35, max(0.0, (seconds - t) / 0.35))
        rgb = im.convert("RGB")
        if kh < 0.999:
            rgb = Image.blend(Image.new("RGB", (W, H)), rgb, kh)
        rgb.save(out / f"f_{i:04d}.png")
    return n_khung


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", nargs="+", required=True, help="tối đa 2 dòng")
    ap.add_argument("--sub", required=True)
    ap.add_argument("--logo", type=Path, default=Path("att_news.png"))
    ap.add_argument("--out-dir", type=Path, default=Path("outro_frames"))
    ap.add_argument("--seconds", type=float, default=4.0)
    ap.add_argument("--cta", default=CTA)
    ap.add_argument("--credit", default=CREDIT)
    a = ap.parse_args()
    if a.seconds < 3:
        raise SystemExit("Outro cần ≥ 3 giây: dòng kêu gọi hiện ở 1,05 s, logo ở 1,15 s, cần thời gian giữ để đọc")
    n = render(a.title, a.sub, a.logo, a.out_dir, a.seconds, a.cta, a.credit)
    print(f"{n} khung ({n / FPS:.2f} s) -> {a.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
