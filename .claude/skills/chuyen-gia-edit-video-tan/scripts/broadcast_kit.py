#!/usr/bin/env python3
"""Hệ thống banner truyền hình: dựng component thành PNG trong suốt, motion vào–giữ–ra thành
chuỗi khung PNG, kèm manifest để validate_graphics.py kiểm.

    python broadcast_kit.py demo --style national-modern --aspect 16:9 --out-dir demo
    python broadcast_kit.py render spec.json --out-dir gfx

spec.json: {"style": "...", "aspect": "16:9", "items": [{"id": "lt1", "type": "lower_third",
            "start": 12.4, "end": 17.0, "args": {"name": "...", "title": "..."}}, ...]}
Mỗi item ra thư mục gfx/<id>/f_%04d.png + mục manifest (vị trí, khung giờ, màu chữ/nền, cỡ chữ).
Ghép vào video: -framerate 30 -i gfx/<id>/f_%04d.png rồi
  [k:v]setpts=PTS-STARTPTS+<start>/TB[g];[base][g]overlay=<overlay_x>:<overlay_y>:eof_action=pass
Manifest ghi `x,y` = chỗ đồ hoạ ĐỨNG YÊN (để kiểm bố cục) và `overlay_x,overlay_y` = chỗ đặt
chuỗi khung khi ghép (lùi ra ngoài một đoạn nếu kiểu motion là trượt vào).
Tin khẩn (urgent-alert) không có kiểu nhấp nháy, và bị từ chối nếu thiếu verified/source.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from icons import to_png  # noqa: E402

STYLES = json.loads((HERE.parent / "assets" / "broadcast" / "styles.json").read_text(encoding="utf-8"))
FRAMES = {"16:9": (1920, 1080), "9:16": (1080, 1920), "1:1": (1080, 1080)}
FPS = 30
NHAN = {"ai": "HÌNH ẢNH AI", "archive": "TƯ LIỆU", "stock": "ẢNH MINH HOẠ", "simulation": "MÔ PHỎNG"}


def safe_rect(aspect: str) -> tuple[int, int, int, int]:
    """Vùng an toàn: 5% mỗi mép; khung dọc chừa UI nền tảng (trên 12%, dưới 20%, phải 15%)."""
    W, H = FRAMES[aspect]
    if aspect == "9:16":
        return round(W * .05), round(H * .12), round(W * .85), round(H * .80)
    return round(W * .05), round(H * .05), round(W * .95), round(H * .95)


class Kit:
    def __init__(self, style: str, aspect: str = "16:9"):
        if style not in STYLES or style == "chung":
            raise SystemExit(f"Không có phong cách '{style}'. Có: {[s for s in STYLES if s[0] != '_' and s != 'chung']}")
        self.name, self.aspect = style, aspect
        self.s, self.c = STYLES[style], STYLES["chung"]
        self.W, self.H = FRAMES[aspect]
        self.safe = safe_rect(aspect)
        self.m = {k: _rgb(v) for k, v in self.s["mau"].items()}
        # ô cố định vùng trên: hàng 0 slug | nhãn · hàng 1 chip | nguồn · hàng 3+ thẻ số liệu
        self.hang = round(self.H * .06)

    # ---------- tiện ích ----------
    def px(self, loai: str) -> int:
        return max(self.c["co_chu_toi_thieu_px_1080"] * self.H // 1080, round(self.c["co_chu"][loai] * self.H))

    def on(self, bg) -> tuple:
        """Chữ trắng hay đen — chọn cái tương phản hơn với nền."""
        return (255, 255, 255) if _contrast((255, 255, 255), bg) >= _contrast((17, 17, 17), bg) else (17, 17, 17)

    def tuong_phan_du(self, bg):
        """Trả (nền, chữ) đạt ≥ 4,5:1 — làm tối nền dần nếu cả trắng lẫn đen đều không đạt."""
        for _ in range(6):
            fg = self.on(bg)
            if _contrast(fg, bg) >= self.c["tuong_phan_toi_thieu"]:
                return bg, fg
            bg = tuple(round(v * .7) for v in bg)
        return bg, (255, 255, 255)

    def giua_an_toan(self, w: int) -> int:
        """Căn giữa theo VÙNG AN TOÀN, không theo bề ngang khung — khung dọc sẽ lòi ra ngoài."""
        return self.safe[0] + (self.safe[2] - self.safe[0] - w) // 2

    def font(self, size: int, dam: bool = True) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(self.c["font"]["dam" if dam else "thuong"], size)

    def fit(self, text: str, size: int, max_w: int, dam: bool = True) -> ImageFont.FreeTypeFont:
        d = ImageDraw.Draw(Image.new("RGB", (8, 8)))
        while size > self.c["co_chu_toi_thieu_px_1080"] * self.H // 1080 and d.textlength(text, font=self.font(size, dam)) > max_w:
            size -= 1
        return self.font(size, dam)

    def plate(self, w: int, h: int, color, accent: bool = True) -> Image.Image:
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, w - 1, h - 1], radius=self.s["bo_goc"], fill=tuple(color) + (238,))
        if accent:
            d.rectangle([0, 0, max(6, h // 14), h - 1], fill=self.m["nhan"] + (255,))
        return im

    def meta(self, im, x, y, text, fg, bg, font_px, **extra) -> dict:
        return {"x": int(x), "y": int(y), "w": im.width, "h": im.height, "text": text,
                "fg": _hex(fg), "bg": _hex(bg), "font_px": font_px, **extra}

    # ---------- banner ----------
    def headline_strap(self, title: str, sub: str = ""):
        sx0, _, sx1, sy1 = self.safe
        w, pad = sx1 - sx0, round(self.H * .018)
        f1 = self.font(self.px("headline"))
        dong = _wrap(title, f1, w - pad * 3)[:2]
        f2 = self.font(self.px("chuc_danh"), False) if sub else None
        h = pad * 2 + len(dong) * (f1.size + 6) + ((f2.size + pad // 2) if sub else 0)
        im = self.plate(w, h, self.m["nen"])
        d = ImageDraw.Draw(im)
        for k, ln in enumerate(dong):
            d.text((pad * 2, pad + k * (f1.size + 6)), ln, font=f1, fill=self.m["chu"])
        if sub:
            d.text((pad * 2, pad + len(dong) * (f1.size + 6) + pad // 2), sub, font=f2, fill=self.m["chu_phu"])
        y = sy1 - h - round(self.H * (.06 if self.aspect == "9:16" else .17))
        return im, self.meta(im, sx0, y, title, self.m["chu"], self.m["nen"], f1.size)

    def topic_slug(self, text: str):
        sx0, sy0, _, _ = self.safe
        f = self.font(self.px("chip"))
        pad = f.size // 2
        w = int(ImageDraw.Draw(Image.new("RGB", (8, 8))).textlength(text.upper(), font=f)) + pad * 2
        im = self.plate(w, f.size + pad * 2, self.m["nhan"], accent=False)
        fg = self.on(self.m["nhan"])
        ImageDraw.Draw(im).text((pad, pad * .8), text.upper(), font=f, fill=fg)
        return im, self.meta(im, sx0, sy0, text, fg, self.m["nhan"], f.size)

    def lower_third(self, name: str, title: str = ""):
        sx0, _, sx1, _ = self.safe
        w = round((sx1 - sx0) * (.72 if self.aspect == "16:9" else 1))   # khung dọc: rộng hết vùng an toàn
        pad = round(self.H * .016)
        f1 = self.fit(name, self.px("ten"), w - pad * 4)
        f2 = self.font(self.px("chuc_danh"), False)
        dong = _wrap(title, f2, w - pad * 4)[:2] if title else []
        h = pad * 2 + f1.size + len(dong) * (f2.size + pad // 2)
        im = self.plate(w, h, self.m["nen"])
        d = ImageDraw.Draw(im)
        d.text((pad * 2, pad), name, font=f1, fill=self.m["chu"])
        for k, ln in enumerate(dong):
            d.text((pad * 2, pad + f1.size + pad // 2 + k * (f2.size + pad // 2)), ln, font=f2, fill=self.m["chu_phu"])
        d.rectangle([0, h - 5, w - 1, h - 1], fill=self.m["phu"] + (255,))
        y = round(self.H * (.60 if self.aspect == "9:16" else .63))
        return im, self.meta(im, sx0, y, f"{name} {title}".strip(), self.m["chu"], self.m["nen"], f1.size)

    def chip(self, kind: str, text: str, corner: str = "left"):
        sx0, sy0, sx1, _ = self.safe
        f = self.font(self.px("chip"))
        pad, icon = f.size // 2, f.size
        tw = int(ImageDraw.Draw(Image.new("RGB", (8, 8))).textlength(text, font=f))
        w, h = pad * 3 + icon + tw, f.size + pad * 2
        bg, fg = self.tuong_phan_du(self.m["nen_2"])
        im = self.plate(w, h, bg, accent=False)
        ic = to_png(kind, icon, _hex(self.m["nhan"] if kind == "live" else fg))
        im.alpha_composite(ic, (pad, pad))
        ImageDraw.Draw(im).text((pad * 2 + icon, pad * .8), text, font=f, fill=fg)
        x = sx0 if corner == "left" else sx1 - w
        return im, self.meta(im, x, sy0 + self.hang, text, fg, bg, f.size)

    def label_chip(self, kind: str):
        """Nhãn phân biệt tư liệu thật / AI / tư liệu cũ / minh hoạ / mô phỏng — góc trên phải."""
        _, sy0, sx1, _ = self.safe
        f = self.font(self.px("chip"))
        text, pad = NHAN[kind], f.size // 2
        tw = int(ImageDraw.Draw(Image.new("RGB", (8, 8))).textlength(text, font=f))
        im = self.plate(tw + pad * 2, f.size + pad * 2, (20, 20, 20), accent=False)
        ImageDraw.Draw(im).text((pad, pad * .8), text, font=f, fill=(255, 255, 255))
        return im, self.meta(im, sx1 - im.width, sy0, text, (255, 255, 255), (20, 20, 20), f.size, label=kind)

    def breaking_bar(self, text: str, verified: bool = False, source: str = ""):
        if self.name == "urgent-alert" and not (verified and source):
            raise SystemExit("Tin khẩn phải có verified=true và source trước khi dựng")
        f = self.fit(text, self.px("headline"), self.W - round(self.W * .30))
        h, tag = f.size + round(self.H * .03), "TIN KHẨN"
        im = Image.new("RGBA", (self.W, h), self.m["nen"] + (245,))
        d = ImageDraw.Draw(im)
        ft = self.font(self.px("chip"))
        tw = int(d.textlength(tag, font=ft)) + ft.size
        d.rectangle([0, 0, tw + ft.size, h], fill=self.m["nhan"] + (255,))
        d.text((ft.size, (h - ft.size) / 2), tag, font=ft, fill=self.on(self.m["nhan"]))
        d.text((tw + ft.size * 2, (h - f.size) / 2), text, font=f, fill=self.m["chu"])
        y = self.safe[3] - h - round(self.H * .045)
        return im, self.meta(im, 0, y, text, self.m["chu"], self.m["nen"], f.size, verified=verified, source=source)

    def status_bar(self, text: str):
        f = self.font(self.px("chip"), False)
        h = f.size + round(self.H * .012)
        bg, fg = self.tuong_phan_du(self.m["nen_2"])
        im = Image.new("RGBA", (self.W, h), bg + (230,))
        ImageDraw.Draw(im).text((self.safe[0], (h - f.size) / 2), text, font=f, fill=fg)
        return im, self.meta(im, 0, 0, text, fg, bg, f.size)

    def source_strap(self, text: str):
        label = f"Nguồn: {text}"
        rong_toi_da = self.safe[2] - self.safe[0]
        f = self.fit(label, self.px("chip"), rong_toi_da - self.px("chip") * 2, dam=False)
        pad = f.size // 2
        tw = int(ImageDraw.Draw(Image.new("RGB", (8, 8))).textlength(label, font=f))
        im = self.plate(tw + pad * 3, f.size + pad * 2, (15, 15, 15))
        ImageDraw.Draw(im).text((pad * 2, pad * .8), label, font=f, fill=(235, 235, 235))
        if self.aspect == "9:16":                # khung dọc hẹp: xuống hàng 2 bên trái, dưới chip
            x, y = self.safe[0], self.safe[1] + self.hang * 2
        else:                                    # hàng 1 bên phải, dưới nhãn tư liệu
            x, y = self.safe[2] - im.width, self.safe[1] + self.hang
        return im, self.meta(im, x, y, label, (235, 235, 235), (15, 15, 15), f.size)

    def ticker_strip(self, items: list[str]):
        f = self.font(self.px("ticker"), False)
        sep = "   •   "
        text = sep.join(items) + sep
        tw = int(ImageDraw.Draw(Image.new("RGB", (8, 8))).textlength(text, font=f))
        h = f.size + round(self.H * .016)
        bg, fg = self.tuong_phan_du(self.m["nen_2"])
        im = Image.new("RGBA", (tw, h), bg + (240,))
        ImageDraw.Draw(im).text((0, (h - f.size) / 2), text, font=f, fill=fg)
        return im, self.meta(im, 0, self.safe[3] - h, " | ".join(items), fg, bg, f.size)

    # ---------- thẻ ----------
    def _card(self, w: int, h: int) -> Image.Image:
        im = self.plate(w, h, self.m["nen"], accent=False)
        ImageDraw.Draw(im).rectangle([0, 0, w - 1, 7], fill=self.m["nhan"] + (255,))
        return im

    def quote_card(self, quote: str, author: str, role: str = ""):
        w = round((self.safe[2] - self.safe[0]) * (.9 if self.aspect != "16:9" else .62))
        pad, fq = round(self.H * .03), self.font(self.px("chuc_danh") + 6, False)
        lines = _wrap(quote, fq, w - pad * 2 - fq.size * 2)
        h = pad * 3 + fq.size * 2 + len(lines) * (fq.size + 10) + self.px("chuc_danh") * 2
        im = self._card(w, h)
        d = ImageDraw.Draw(im)
        im.alpha_composite(to_png("quote", fq.size * 2, _hex(self.m["phu"])), (pad, pad))
        y = pad + fq.size * 2
        for ln in lines:
            d.text((pad + fq.size, y), ln, font=fq, fill=self.m["chu"])
            y += fq.size + 10
        fa = self.font(self.px("chuc_danh"))
        d.text((pad + fq.size, y + pad // 2), f"— {author}", font=fa, fill=self.m["phu"])
        if role:
            d.text((pad + fq.size, y + pad // 2 + fa.size + 4), role, font=self.font(self.px("chip"), False), fill=self.m["chu_phu"])
        return im, self.meta(im, self.giua_an_toan(w), (self.H - h) // 2, quote, self.m["chu"], self.m["nen"], fq.size)

    def fact_card(self, number: str, label: str, note: str = ""):
        w = round((self.safe[2] - self.safe[0]) * (.9 if self.aspect != "16:9" else .40))
        fn, fl = self.fit(number, self.px("the_so_lieu"), w - 60), self.font(self.px("chuc_danh"))
        pad = round(self.H * .03)
        lines = _wrap(label, fl, w - pad * 2)
        h = pad * 3 + fn.size + len(lines) * (fl.size + 8) + (self.px("chip") + 8 if note else 0)
        im = self._card(w, h)
        d = ImageDraw.Draw(im)
        d.text((pad, pad), number, font=fn, fill=self.m["phu"])
        y = pad * 2 + fn.size
        for ln in lines:
            d.text((pad, y), ln, font=fl, fill=self.m["chu"])
            y += fl.size + 8
        if note:
            d.text((pad, y), note, font=self.font(self.px("chip"), False), fill=self.m["chu_phu"])
        x = self.safe[2] - w if self.aspect == "16:9" else self.giua_an_toan(w)
        return im, self.meta(im, x, self.safe[1] + self.hang * 3, f"{number} {label}", self.m["phu"], self.m["nen"], fn.size)

    def comparison(self, left: tuple[str, str], right: tuple[str, str]):
        w = round((self.safe[2] - self.safe[0]) * .8)
        pad, fh, fv = round(self.H * .03), self.font(self.px("chuc_danh")), self.font(self.px("the_so_lieu"))
        h = pad * 3 + fh.size + fv.size
        im = self._card(w, h)
        d = ImageDraw.Draw(im)
        d.line([(w // 2, pad), (w // 2, h - pad)], fill=self.m["chu_phu"] + (160,), width=2)
        for k, (t, v) in enumerate((left, right)):
            x0 = pad + k * w // 2
            d.text((x0, pad), t, font=fh, fill=self.m["chu_phu"])
            d.text((x0, pad * 2 + fh.size), v, font=self.fit(v, fv.size, w // 2 - pad * 2), fill=self.m["phu"] if k else self.m["chu"])
        return im, self.meta(im, self.giua_an_toan(w), (self.H - h) // 2, f"{left} | {right}", self.m["chu"], self.m["nen"], fh.size)

    def timeline(self, events: list[tuple[str, str]]):
        w = round((self.safe[2] - self.safe[0]) * .9)
        pad, ft, fl = round(self.H * .03), self.font(self.px("chip")), self.font(self.px("chip"), False)
        h = pad * 4 + ft.size * 3
        im = self._card(w, h)
        d = ImageDraw.Draw(im)
        yl = pad + ft.size + pad // 2
        d.line([(pad, yl), (w - pad, yl)], fill=self.m["chu_phu"] + (200,), width=3)
        step = (w - pad * 2) / max(1, len(events) - 1)
        for k, (t, lab) in enumerate(events):
            x = pad + k * step
            d.ellipse([x - 9, yl - 9, x + 9, yl + 9], fill=self.m["phu"] + (255,))
            d.text((x - d.textlength(t, font=ft) / 2, pad), t, font=ft, fill=self.m["chu"])
            lab_f = self.fit(lab, fl.size, int(step * .95), dam=False)
            d.text((x - d.textlength(lab, font=lab_f) / 2, yl + pad), lab, font=lab_f, fill=self.m["chu_phu"])
        return im, self.meta(im, self.giua_an_toan(w), (self.H - h) // 2, " / ".join(e[1] for e in events), self.m["chu"], self.m["nen"], fl.size)

    def map_card(self, image: str, pin: tuple[float, float], label: str):
        """Bản đồ do người dùng cung cấp (không tự tải bản đồ trên mạng) + ghim + nhãn."""
        w = round((self.safe[2] - self.safe[0]) * (.9 if self.aspect != "16:9" else .5))
        src = Image.open(image).convert("RGBA")
        h = round(w * src.height / src.width)
        im = src.resize((w, h), Image.LANCZOS)
        px, py = pin[0] * w, pin[1] * h
        icon = to_png("location", self.px("chip") * 2, _hex(self.m["nhan"]))
        im.alpha_composite(icon, (int(px - icon.width / 2), int(py - icon.height)))
        lab, _ = self.topic_slug(label)
        im.alpha_composite(lab, (int(min(w - lab.width, px + 12)), int(max(0, py - icon.height - lab.height))))
        return im, self.meta(im, self.safe[2] - w, self.safe[1] + round(self.H * .08), label, self.m["chu"], self.m["nhan"], self.px("chip"))

    def end_card(self, title: str, cta: str, handles: list[str]):
        im = Image.new("RGBA", (self.W, self.H), self.m["nen"] + (255,))
        d = ImageDraw.Draw(im)
        f1 = self.fit(title, self.px("headline") + 12, self.safe[2] - self.safe[0])
        d.text(((self.W - d.textlength(title, font=f1)) / 2, self.H * .36), title, font=f1, fill=self.m["chu"])
        f2 = self.font(self.px("chuc_danh"))
        d.text(((self.W - d.textlength(cta, font=f2)) / 2, self.H * .36 + f1.size * 1.6), cta, font=f2, fill=self.m["phu"])
        fh = self.font(self.px("chip"), False)
        line = "   ".join(handles)
        d.text(((self.W - d.textlength(line, font=fh)) / 2, self.H * .36 + f1.size * 1.6 + f2.size * 2), line, font=fh, fill=self.m["chu_phu"])
        return im, self.meta(im, 0, 0, f"{title} {cta}", self.m["chu"], self.m["nen"], f2.size)


# ---------- motion: vào – giữ – ra ----------
def animate(img: Image.Image, out_dir: Path, seconds: float, kieu: str, vao: float, ra: float,
            dist: int = 60, fps: int = FPS) -> dict:
    """Ghi chuỗi khung cố định cỡ để overlay không phải đổi toạ độ. Không có kiểu nhấp nháy."""
    out_dir.mkdir(parents=True, exist_ok=True)
    slide = kieu == "slide"
    cw = img.width + (dist if slide else 0)
    n = max(1, round(seconds * fps))
    for i in range(n):
        t = i / fps
        a = _ease(t / vao if vao else 1) * _ease((seconds - t) / ra if ra else 1)
        fr = Image.new("RGBA", (cw, img.height), (0, 0, 0, 0))
        if kieu == "mask":
            vis = img.crop((0, 0, max(1, round(img.width * _ease(t / vao if vao else 1))), img.height))
            fr.alpha_composite(_alpha(vis, _ease((seconds - t) / ra if ra else 1)), (0, 0))
        else:
            off = round(dist * _ease(t / vao if vao else 1)) if slide else 0
            fr.alpha_composite(_alpha(img, a), (off, 0))
        fr.save(out_dir / f"f_{i:04d}.png")
    return {"frames": n, "dx": -dist if slide else 0}


def ticker_frames(strip: Image.Image, width: int, out_dir: Path, seconds: float, speed: float = 140) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    n = round(seconds * FPS)
    loop = Image.new("RGBA", (strip.width * 2, strip.height))
    loop.paste(strip, (0, 0)), loop.paste(strip, (strip.width, 0))
    for i in range(n):
        x = int(i / FPS * speed) % strip.width
        loop.crop((x, 0, x + width, strip.height)).save(out_dir / f"f_{i:04d}.png")
    return n


# ---------- tiện ích chung ----------
def _rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _contrast(a, b) -> float:
    def lum(c):
        def k(v):
            v /= 255
            return v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4
        return .2126 * k(c[0]) + .7152 * k(c[1]) + .0722 * k(c[2])
    x, y = sorted((lum(a), lum(b)), reverse=True)
    return (x + .05) / (y + .05)


def _hex(c) -> str:
    return "#%02X%02X%02X" % tuple(c[:3])


def _ease(p: float) -> float:
    p = min(1.0, max(0.0, p))
    return 1 - (1 - p) ** 3


def _alpha(img: Image.Image, a: float) -> Image.Image:
    if a >= .999:
        return img
    r, g, b, al = img.split()
    return Image.merge("RGBA", (r, g, b, al.point(lambda v: int(v * a))))


def _wrap(text: str, font, max_w: int) -> list[str]:
    d, lines, cur = ImageDraw.Draw(Image.new("RGB", (8, 8))), [], ""
    for word in text.split():
        nxt = f"{cur} {word}".strip()
        if d.textlength(nxt, font=font) <= max_w or not cur:
            cur = nxt
        else:
            lines.append(cur)
            cur = word
    return lines + ([cur] if cur else [])


def render_spec(spec: dict, out_dir: Path) -> list[dict]:
    kit = Kit(spec["style"], spec.get("aspect", "16:9"))
    mo = kit.s["motion"]
    manifest = []
    for it in spec["items"]:
        fn = getattr(kit, it["type"], None)
        if fn is None or it["type"].startswith("_"):
            raise SystemExit(f"Không có component '{it['type']}'")
        im, meta = fn(**it.get("args", {}))
        seconds = it["end"] - it["start"]
        if it["type"] == "ticker_strip":
            ticker_frames(im, kit.W, out_dir / it["id"], seconds)
            meta.update(w=kit.W, overlay_x=meta["x"], overlay_y=meta["y"])
        else:
            info = animate(im, out_dir / it["id"], seconds, mo["kieu"], mo["vao"], mo["ra"])
            meta.update(overlay_x=meta["x"] + info["dx"], overlay_y=meta["y"])
        manifest.append({"id": it["id"], "type": it["type"], "style": kit.name, "aspect": kit.aspect,
                         "start": it["start"], "end": it["end"], **meta})
    (out_dir / "manifest.json").write_text(json.dumps({"aspect": kit.aspect, "items": manifest},
                                                      ensure_ascii=False, indent=1), encoding="utf-8")
    return manifest


DEMO = [
    ("topic_slug", {"text": "Y tế"}), ("chip", {"kind": "location", "text": "Xã An Thạnh Thủy"}),
    ("label_chip", {"kind": "archive"}), ("headline_strap", {"title": "KHÁM SÀNG LỌC CHO 2.500 NGƯỜI DÂN", "sub": "Trạm Y tế xã · 7–8/9/2026"}),
    ("lower_third", {"name": "Bác sĩ Trạm Y tế xã", "title": "Khám, tư vấn sức khỏe cho người dân"}),
    ("source_strap", {"text": "UBND xã An Thạnh Thủy"}), ("fact_card", {"number": "2.500", "label": "người dân được khám, sàng lọc", "note": "dự kiến"}),
]


def demo(style: str, aspect: str, out_dir: Path) -> Path:
    kit = Kit(style, aspect)
    out_dir.mkdir(parents=True, exist_ok=True)
    nen = Image.new("RGBA", (kit.W, kit.H), (96, 104, 112, 255))
    d = ImageDraw.Draw(nen)
    sx0, sy0, sx1, sy1 = kit.safe
    d.rectangle([sx0, sy0, sx1, sy1], outline=(255, 255, 0, 120), width=2)
    items = []
    for kind, args in DEMO:
        im, meta = getattr(kit, kind)(**args)
        im.save(out_dir / f"{kind}.png")
        rieng = kind == "headline_strap"        # cùng dải dưới với lower_third → hiện ở lượt khác
        if not rieng:
            nen.alpha_composite(im, (meta["x"], meta["y"]))
        items.append({"id": kind, "type": kind, "style": style, "aspect": aspect,
                      "start": 6 if rieng else 0, "end": 11 if rieng else 5, **meta})
    (out_dir / "manifest.json").write_text(json.dumps({"aspect": aspect, "items": items}, ensure_ascii=False, indent=1), encoding="utf-8")
    p = out_dir / f"demo_{style}_{aspect.replace(':', 'x')}.png"
    nen.convert("RGB").save(p)
    return p


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("demo")
    d.add_argument("--style", default="national-modern")
    d.add_argument("--aspect", choices=list(FRAMES), default="16:9")
    d.add_argument("--out-dir", type=Path, default=Path("demo"))
    r = sub.add_parser("render")
    r.add_argument("spec", type=Path)
    r.add_argument("--out-dir", type=Path, default=Path("gfx"))
    a = ap.parse_args()
    if a.cmd == "demo":
        print(demo(a.style, a.aspect, a.out_dir))
    else:
        m = render_spec(json.loads(a.spec.read_text(encoding="utf-8")), a.out_dir)
        print(f"{len(m)} component -> {a.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
