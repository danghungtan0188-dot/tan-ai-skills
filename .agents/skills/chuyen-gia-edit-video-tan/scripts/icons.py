#!/usr/bin/env python3
"""Bộ icon truyền thông vector thống nhất: lưới 24, nét 2, đầu nét tròn, cùng kiểu bo góc.

    python icons.py --out-dir ../assets/broadcast/icons                 # ghi SVG
    python icons.py --out-dir DIR --png 96 --color "#FFFFFF"             # thêm PNG nền trong suốt

Mỗi icon là danh sách nguyên tố hình học, vẽ ra cả SVG lẫn PNG từ cùng một định nghĩa —
nên nét, bo góc và kích thước luôn đồng bộ.
Quy tắc: không trộn emoji với icon này trong đồ hoạ truyền hình; không trích xuất logo hay
icon từ ảnh chụp của các đài; logo nền tảng (Facebook, Zalo, YouTube, TikTok) chỉ dùng file
chính thức do người dùng cung cấp.
"""
from __future__ import annotations
import argparse
import math
from pathlib import Path
from PIL import Image, ImageDraw


def cung(cx, cy, r, a0, a1, n=24):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]


def dam_may():
    return (cung(7, 15.5, 3.5, 90, 270) + cung(12, 12.5, 4.5, 200, 340)
            + cung(17, 15.5, 3.5, 270, 450))


# nguyên tố: line(x1,y1,x2,y2) rect(x,y,w,h,rx) circle(cx,cy,r) ellipse(cx,cy,rx,ry)
#            dot(cx,cy,r) — tô đặc; path(điểm, kín?)
ICONS: dict[str, list] = {
    "live": [("dot", (12, 12, 2.6)), ("path", (cung(12, 12, 6, -40, 40), False)),
             ("path", (cung(12, 12, 6, 140, 220), False)), ("path", (cung(12, 12, 9.5, -40, 40), False)),
             ("path", (cung(12, 12, 9.5, 140, 220), False))],
    "time": [("circle", (12, 12, 9)), ("line", (12, 12, 12, 7)), ("line", (12, 12, 15.5, 14))],
    "date": [("rect", (3, 5, 18, 16, 2)), ("line", (3, 10, 21, 10)), ("line", (8, 3, 8, 7)), ("line", (16, 3, 16, 7))],
    "location": [("path", (cung(12, 10, 7, 150, 390) + [(12, 21.5)], True)), ("circle", (12, 10, 2.6))],
    "map": [("path", ([(3, 6), (9, 4), (15, 6), (21, 4), (21, 18), (15, 20), (9, 18), (3, 20)], True)),
            ("line", (9, 4, 9, 18)), ("line", (15, 6, 15, 20))],
    "weather": [("circle", (16, 7, 2.8)), ("line", (16, 2, 16, 3)), ("line", (21, 7, 20, 7)),
                ("line", (19.5, 3.5, 18.8, 4.2)), ("path", (dam_may(), True))],
    "traffic": [("rect", (8, 2, 8, 20, 3)), ("dot", (12, 7, 1.7)), ("dot", (12, 12, 1.7)), ("dot", (12, 17, 1.7))],
    "document": [("path", ([(6, 3), (14, 3), (19, 8), (19, 21), (6, 21)], True)),
                 ("path", ([(14, 3), (14, 8), (19, 8)], False)), ("line", (9, 12, 16, 12)), ("line", (9, 16, 16, 16))],
    "data": [("line", (4, 20, 20, 20)), ("rect", (6, 12, 3, 8, .5)), ("rect", (11, 8, 3, 12, .5)),
             ("rect", (16, 5, 3, 15, .5))],
    "medical": [("rect", (3, 3, 18, 18, 4)), ("line", (12, 7.5, 12, 16.5)), ("line", (7.5, 12, 16.5, 12))],
    "education": [("path", ([(2, 9), (12, 4), (22, 9), (12, 14)], True)),
                  ("path", ([(6, 11), (6, 16), (12, 19), (18, 16), (18, 11)], False)), ("line", (22, 9, 22, 15))],
    "tech": [("rect", (7, 7, 10, 10, 1.5)), ("rect", (10, 10, 4, 4, .5))]
            + [("line", p) for v in (10, 14) for p in ((v, 3.5, v, 7), (v, 17, v, 20.5), (3.5, v, 7, v), (17, v, 20.5, v))],
    "archive": [("rect", (3, 4, 18, 5, 1)), ("path", ([(5, 9), (5, 20), (19, 20), (19, 9)], False)),
                ("line", (10, 13, 14, 13))],
    "stock": [("rect", (3, 5, 18, 14, 2)), ("circle", (8.5, 10, 1.6)),
              ("path", ([(3, 17), (9, 12), (13, 15.5), (16, 13), (21, 17)], False))],
    "ai": [("path", ([(12, 3), (13.8, 10.2), (21, 12), (13.8, 13.8), (12, 21), (10.2, 13.8), (3, 12), (10.2, 10.2)], True)),
           ("line", (19, 3.5, 19, 7.5)), ("line", (17, 5.5, 21, 5.5))],
    "microphone": [("rect", (9, 3, 6, 11, 3)), ("path", (cung(12, 11, 6, 0, 180), False)),
                   ("line", (12, 17, 12, 21)), ("line", (8.5, 21, 15.5, 21))],
    "camera": [("rect", (3, 7, 13, 10, 2)), ("path", ([(16, 10.5), (21, 7.5), (21, 16.5), (16, 13.5)], True))],
    "quote": [("dot", (8, 9, 2.4)), ("line", (10.2, 9.8, 7.6, 15.5)), ("dot", (16, 9, 2.4)), ("line", (18.2, 9.8, 15.6, 15.5))],
    "phone": [("rect", (7, 2, 10, 20, 2.5)), ("line", (11, 18.5, 13, 18.5))],
    "website": [("circle", (12, 12, 9)), ("ellipse", (12, 12, 4, 9)), ("line", (3, 12, 21, 12))],
    "email": [("rect", (3, 6, 18, 12, 2)), ("path", ([(3.5, 7), (12, 13), (20.5, 7)], False))],
    "warning": [("path", ([(12, 3), (22, 20), (2, 20)], True)), ("line", (12, 9, 12, 14)), ("dot", (12, 17, 1.2))],
}


def _n(v: float) -> str:
    return f"{round(v, 2):g}"


def to_svg(name: str) -> str:
    out = []
    for kind, p in ICONS[name]:
        if kind == "line":
            out.append(f'<line x1="{_n(p[0])}" y1="{_n(p[1])}" x2="{_n(p[2])}" y2="{_n(p[3])}"/>')
        elif kind == "rect":
            out.append(f'<rect x="{_n(p[0])}" y="{_n(p[1])}" width="{_n(p[2])}" height="{_n(p[3])}" rx="{_n(p[4])}"/>')
        elif kind == "circle":
            out.append(f'<circle cx="{_n(p[0])}" cy="{_n(p[1])}" r="{_n(p[2])}"/>')
        elif kind == "ellipse":
            out.append(f'<ellipse cx="{_n(p[0])}" cy="{_n(p[1])}" rx="{_n(p[2])}" ry="{_n(p[3])}"/>')
        elif kind == "dot":
            out.append(f'<circle cx="{_n(p[0])}" cy="{_n(p[1])}" r="{_n(p[2])}" fill="currentColor" stroke="none"/>')
        elif kind == "path":
            pts = " ".join(f"{_n(x)},{_n(y)}" for x, y in p[0])
            out.append(f'<{"polygon" if p[1] else "polyline"} points="{pts}"/>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" '
            f'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            f'<title>{name}</title>{"".join(out)}</svg>\n')


def to_png(name: str, size: int = 96, color: str = "#FFFFFF") -> Image.Image:
    ss = 4
    k = size * ss / 24
    w = max(1, round(2 * k))
    col = Image.new("RGB", (1, 1), color).getpixel((0, 0)) + (255,)
    im = Image.new("RGBA", (size * ss, size * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    h = w / 2

    def mu(x, y):
        d.ellipse([x - h, y - h, x + h, y + h], fill=col)

    for kind, p in ICONS[name]:
        if kind == "line":
            a, b = (p[0] * k, p[1] * k), (p[2] * k, p[3] * k)
            d.line([a, b], fill=col, width=w)
            mu(*a), mu(*b)
        elif kind == "rect":
            d.rounded_rectangle([p[0] * k - h, p[1] * k - h, (p[0] + p[2]) * k + h, (p[1] + p[3]) * k + h],
                                radius=p[4] * k + h, outline=col, width=w)
        elif kind in ("circle", "ellipse"):
            rx, ry = (p[2], p[2]) if kind == "circle" else (p[2], p[3])
            d.ellipse([(p[0] - rx) * k - h, (p[1] - ry) * k - h, (p[0] + rx) * k + h, (p[1] + ry) * k + h],
                      outline=col, width=w)
        elif kind == "dot":
            d.ellipse([(p[0] - p[2]) * k, (p[1] - p[2]) * k, (p[0] + p[2]) * k, (p[1] + p[2]) * k], fill=col)
        elif kind == "path":
            pts = [(x * k, y * k) for x, y in p[0]] + ([(p[0][0][0] * k, p[0][0][1] * k)] if p[1] else [])
            d.line(pts, fill=col, width=w, joint="curve")
            for q in pts:
                mu(*q)
    return im.resize((size, size), Image.LANCZOS)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--png", type=int, help="thêm PNG cỡ này (px)")
    ap.add_argument("--color", default="#FFFFFF")
    a = ap.parse_args()
    a.out_dir.mkdir(parents=True, exist_ok=True)
    for name in ICONS:
        (a.out_dir / f"{name}.svg").write_text(to_svg(name), encoding="utf-8")
        if a.png:
            to_png(name, a.png, a.color).save(a.out_dir / f"{name}.png")
    print(f"{len(ICONS)} icon -> {a.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
