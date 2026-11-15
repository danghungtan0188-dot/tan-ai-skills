#!/usr/bin/env python3
"""Bố cục 65/35 cho tin dựng từ ảnh nhỏ (bản tin 13/11/2026, người dùng đã duyệt).

Khung ảnh 16:9 1216×684 viền vàng (65%) đổi bên trái/phải theo từng cảnh, ảnh trôi chậm (zoom ≤ 12%);
khung chữ 35%: tên vàng kim không bao giờ ngắt dòng lẻ, số đếm chạy 1,3 s, chip vàng, địa điểm, trích dẫn.
Nền men gốm xanh ngọc đậm. Tin lãnh đạo Trung ương → hiệu ứng nhẹ, trang trọng, không chữ nhấp nháy.
Thông số: references/phong-cach-att-news.md mục 10. Mẫu kịch bản: mau_tin_65_35.json.

  python khung6535.py tin.json --xem          # ảnh lưới xem thử các cảnh (+ "xem_lon": khung PNG lớn)
  python khung6535.py tin.json [--chia 0/2]   # chuỗi khung JPG 30 fps vào thư mục "ra"; chạy lại bỏ qua khung đã có
  ffmpeg -framerate 30 -i ra/k_%05d.jpg -c:v libx264 -preset faster -crf 18 -pix_fmt yuv420p tin.mp4

Kịch bản JSON (đường dẫn tính từ thư mục chứa JSON):
  "ra": thư mục khung, "moc_file": mốc câu {"moc": {cid: [bd, kt]}, "het": giây}, "canh": [...]
  cảnh: "bd"/"kt" (giây hoặc "cid", "cid+0.4", "cid-0.3", "cid$" = hết câu), "ben": "T"|"P", "anh": [...], "muc": [...]
  mục: loai = nhan | tieu_de | ten | so | so_muc | nguoi | chip | dia_diem | trich, "t" = lúc hiện.
  Tin có video: "video" + "hop": [giây thu vào khung, giây bung ra] — cảnh không có "anh" để lỗ đen cho video.
"""

import argparse
import json
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1920, 1080, 30
BW, BH, BY = 1216, 684, 150   # khung ảnh 65%
CHU_Y_MIN = 240               # chữ bắt đầu dưới logo ATT góc phải trên
TRANG, VANG_SO, VANG_NHAT = (255, 255, 255), (255, 214, 64), (255, 236, 170)
THU_MUC_FONT = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
_FONT_FILE = {"bl": "seguibl.ttf", "b": "segoeuib.ttf", "sb": "seguisb.ttf", "r": "segoeui.ttf"}

ease = lambda x: 1 - (1 - min(1, max(0, x))) ** 3
mem = lambda x: 0.5 - 0.5 * math.cos(math.pi * min(1, max(0, x)))
_font = {}


def font(size, kieu="b"):
    k = (size, kieu)
    if k not in _font:
        try:
            _font[k] = ImageFont.truetype(str(THU_MUC_FONT / _FONT_FILE[kieu]), size)
        except OSError:   # máy không có Segoe UI: font mặc định của Pillow (vẫn đủ dấu tiếng Việt)
            _font[k] = ImageFont.load_default(size)
    return _font[k]


def bo_cuc(ben):
    """("T") ảnh trái, chữ phải; ("P") ảnh phải, chữ trái. Trả ((x, y) khung ảnh, (x0, x1) khung chữ)."""
    if ben == "T":
        return (60, BY), (1330, 1864)
    return (W - 60 - BW, BY), (64, 600)


# ---- đo chữ ----
_do = ImageDraw.Draw(Image.new("L", (1, 1)))


def vua_dong(text, co, rong, kieu):
    """Thu cỡ chữ tới khi vừa một dòng (tên người không bao giờ ngắt dòng)."""
    while co > 30 and _do.textlength(text, font=font(co, kieu)) > rong:
        co -= 2
    return font(co, kieu)


def ngat(text, f, rong):
    dong = []
    for p in text.split("\n"):
        cur = ""
        for w in p.split():
            th = (cur + " " + w).strip()
            if _do.textlength(th, font=f) <= rong or not cur:
                cur = th
            else:
                dong.append(cur)
                cur = w
        dong.append(cur)
    return dong


def can_dong(text, f, rong):
    """Chia dòng cân đối: dòng cuối không còn một chữ lẻ."""
    ds = ngat(text, f, rong)
    if len(ds) < 2 or len(ds[-1].split()) > 1:
        return ds
    for r in range(int(rong) - 10, int(rong * 0.5), -10):
        thu = ngat(text, f, r)
        if len(thu) == len(ds) and len(thu[-1].split()) > 1:
            return thu
    return ds


# ---- nền men gốm xanh ngọc + tia sáng xoay rất chậm + lưới mạng mờ ----
_nen = {}


def _nen0():
    if "0" not in _nen:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - W * 0.42) / W) ** 2 + ((yy - H * 0.38) / H) ** 2)
        g = np.zeros((H, W, 3), np.float32)
        for c, (a, b) in enumerate(zip((22, 104, 70), (4, 38, 26))):   # #16683F → #04261A
            g[..., c] = a + (b - a) * np.clip(r / 0.9, 0, 1) ** 1.2
        bong = np.exp(-(((xx - W * 0.30) / (W * 0.30)) ** 2 + ((yy - H * 0.12) / (H * 0.28)) ** 2))
        bong2 = np.exp(-(((xx - W * 0.85) / (W * 0.22)) ** 2 + ((yy - H * 0.95) / (H * 0.25)) ** 2)) * 0.35
        g += (bong * 0.55 + bong2)[..., None] * np.array([150, 210, 180], np.float32) * 0.45
        van = np.random.default_rng(3).normal(0, 1, (H // 4, W // 4)).astype(np.float32)   # vân men mịn
        van = np.array(Image.fromarray(((van * 18) + 128).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
                       .filter(ImageFilter.GaussianBlur(2)), np.float32) - 128
        g += van[..., None] * 0.12
        _nen["0"] = Image.fromarray(g.clip(0, 255).astype(np.uint8))
        rng = np.random.default_rng(7)
        _nen["diem"] = [(rng.uniform(-100, W + 100), rng.uniform(-100, H + 100), rng.uniform(-8, 8), rng.uniform(-6, 6))
                        for _ in range(34)]
    return _nen["0"], _nen["diem"]


_tia = {}


def nen(t):
    k = int(t * 10)   # đổi 10 lần/giây là đủ mượt vì xoay rất chậm
    if k not in _tia:
        if len(_tia) > 4:
            _tia.clear()
        nen0, diem = _nen0()
        lop = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(lop)
        cx, cy, R = W * 0.5, -260, 3000
        for i in range(28):
            g0 = math.radians(i * 360 / 28 + k * 0.05)
            g1 = g0 + math.radians(4.2)
            d.polygon([(cx, cy), (cx + R * math.cos(g0), cy + R * math.sin(g0)), (cx + R * math.cos(g1), cy + R * math.sin(g1))],
                      fill=12)
        im = nen0.copy()
        im.paste((190, 240, 215), (0, 0), lop.filter(ImageFilter.GaussianBlur(6)))
        d = ImageDraw.Draw(im)
        P = [((x + vx * k / 10) % (W + 200) - 100, (y + vy * k / 10) % (H + 200) - 100) for x, y, vx, vy in diem]
        for i, a in enumerate(P):
            for b in P[i + 1:]:
                if math.dist(a, b) < 260:
                    d.line([a, b], fill=(40, 112, 82), width=1)
            d.ellipse([a[0] - 2, a[1] - 2, a[0] + 2, a[1] + 2], fill=(90, 160, 125))
        _tia[k] = im
    return _tia[k].copy()


# ---- chữ vàng kim: tô màu dọc bằng mặt nạ (không dùng clip-text) ----
_vg = np.zeros((400, 1, 3), np.float32)
for _c, (_a, _m, _b) in enumerate(zip((255, 246, 196), (240, 196, 132), (172, 120, 34))):
    _vg[:200, 0, _c] = np.linspace(_a, _m, 200)
    _vg[200:, 0, _c] = np.linspace(_m, _b, 200)


def chu_vang(im, xy, text, f, a=1.0, bong=True):
    if a <= 0:
        return
    x0, y0, x1, y1 = ImageDraw.Draw(im).textbbox(xy, text, font=f)
    w, h = x1 - x0 + 4, y1 - y0 + 4
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).text((xy[0] - x0 + 2, xy[1] - y0 + 2), text, font=f, fill=255)
    if bong:
        im.paste((10, 50, 20), (x0 + 3, y0 + 5), mask.filter(ImageFilter.GaussianBlur(4)).point(lambda v: int(v * 0.75 * a)))
    mau = Image.fromarray(np.repeat(_vg, w, 1).astype(np.uint8)).resize((w, h))
    im.paste(mau, (x0 - 2, y0 - 2), mask.point(lambda v: int(v * a)))


def chu(im, xy, text, f, fill=TRANG, a=1.0, bong=True):
    if a <= 0:
        return
    lop = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lop)
    if bong:
        d.text((xy[0] + 2, xy[1] + 3), text, font=f, fill=(5, 40, 15, int(150 * a)))
    d.text(xy, text, font=f, fill=fill + (int(255 * a),))
    im.paste(lop, (0, 0), lop)


# ---- khung ảnh viền vàng + bóng ----
_khung = {}


def ve_khung(im, x, y, a=1.0):
    if not _khung:
        pad = 40
        s = Image.new("L", (BW + 2 * pad, BH + 2 * pad), 0)
        ImageDraw.Draw(s).rectangle([pad - 6, pad - 6, pad + BW + 6, pad + BH + 6], fill=200)
        _khung["bong"] = s.filter(ImageFilter.GaussianBlur(16))
        v = Image.new("L", (BW + 16, BH + 16), 0)
        dv = ImageDraw.Draw(v)
        dv.rectangle([0, 0, BW + 15, BH + 15], fill=255)
        dv.rectangle([8, 8, BW + 7, BH + 7], fill=0)   # viền 8 px
        _khung["vien"] = v
        _khung["mau"] = Image.fromarray(np.repeat(_vg, BW + 16, 1).astype(np.uint8)).resize((BW + 16, BH + 16))
    im.paste((5, 35, 12), (x - 30, y - 26), _khung["bong"].point(lambda v: int(v * 0.8 * a)))
    im.paste(_khung["mau"], (x - 8, y - 8), _khung["vien"].point(lambda v: int(v * a)))


_anh = {}


def anh_ken_burns(src, p, huong, lech):
    if src not in _anh:
        if len(_anh) > 6:
            _anh.clear()
        a = Image.open(src).convert("RGB")
        s = max(BW * 1.18 / a.width, BH * 1.18 / a.height)
        _anh[src] = a.resize((int(a.width * s), int(a.height * s)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 60, 2))
    a = _anh[src]
    z = 1.0 + 0.12 * (mem(p) if huong > 0 else 1 - mem(p))   # zoom vào hoặc ra, tối đa 12%
    s = min(a.width / BW, a.height / BH) / z
    cw, ch = BW * s, BH * s
    cx = a.width / 2 + lech[0] * (a.width - cw) / 2 * (mem(p) * 2 - 1)
    cy = a.height / 2 + lech[1] * (a.height - ch) / 2
    return a.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize((BW, BH), Image.BILINEAR)


# ---- các mục trong khung 35% ----
def muc(im, m, t, x0, x1, y):
    """Vẽ một mục, trả y kế tiếp. m["t"] = giây xuất hiện."""
    a = ease((t - m["t"]) / 0.6)
    rong, dy, k = x1 - x0, int((1 - a) * 24), m["loai"]
    if k == "so_muc":   # "01" to + gạch vàng
        chu_vang(im, (x0, y + dy), m["so"], font(132, "bl"), a)
        ImageDraw.Draw(im).rectangle([x0 + 4, y + 165, x0 + 4 + int(120 * a), y + 171], fill=VANG_SO)
        return y + 196
    if k == "nhan":   # nhãn nhỏ chữ hoa vàng nhạt
        ds = can_dong(m["text"].upper(), font(30, "sb"), rong)
        for i, l in enumerate(ds):
            chu(im, (x0, y + dy + i * 40), l, font(30, "sb"), VANG_NHAT, a)
        return y + 40 * len(ds) + 10
    if k == "tieu_de":
        f = font(m.get("co", 54), "bl")
        ds, lh = can_dong(m["text"], f, rong), int(f.size * 1.18)
        for i, l in enumerate(ds):
            chu(im, (x0, y + dy + i * lh), l, f, TRANG, a)
        return y + lh * len(ds) + 22
    if k == "ten":   # chức danh nhỏ + tên to vàng kim
        f1, ten = font(30, "sb"), m["ten"].upper()
        f2, dong = vua_dong(ten, m.get("co", 58), rong, "bl"), [ten]
        if f2.size < 50:   # tên dài: chia 2 dòng cân đối, giữ chữ to
            w_ = ten.split()
            i = min(range(1, len(w_)), key=lambda i: max(_do.textlength(" ".join(w_[:i]), font=font(64, "bl")),
                                                         _do.textlength(" ".join(w_[i:]), font=font(64, "bl"))))
            dong = [" ".join(w_[:i]), " ".join(w_[i:])]
            f2 = vua_dong(max(dong, key=len), 66, rong, "bl")
        for l in can_dong(m["chuc"].upper(), f1, rong):   # chức danh viết đủ, không viết tắt
            chu(im, (x0, y + dy), l, f1, VANG_NHAT, a)
            y += 40
        for l in dong:
            chu_vang(im, (x0, y + dy), l, f2, a)
            y += int(f2.size * 1.2)
        ImageDraw.Draw(im).rectangle([x0 + 2, y + 10, x0 + 2 + int(180 * a), y + 14], fill=VANG_SO)
        for l in can_dong(m["phu"], font(30, "sb"), rong) if m.get("phu") else []:
            chu(im, (x0, y + 30 + dy), l, font(30, "sb"), TRANG, a)
            y += 40
        return y + 46
    if k == "so":   # số đếm chạy 1,3 s + đơn vị + nhãn
        n = m["so"] * ease((t - m["t"]) / 1.3)
        s = f"{n:,.0f}".replace(",", ".") if m["so"] >= 1000 else f"{n:.0f}"
        f = font(m.get("co", 96), "bl")
        if m.get("tren"):
            chu(im, (x0, y + dy), m["tren"], font(28, "sb"), VANG_NHAT, a)
            y += 36
        chu(im, (x0, y + dy - 10), s, f, VANG_SO, a)
        chu(im, (x0 + _do.textlength(s, font=f) + 14, y + dy + f.size * 0.42), m.get("don_vi", ""), font(40, "b"), VANG_SO, a)
        y += int(f.size * 1.1)
        for l in can_dong(m["nhan"], font(32, "sb"), rong):
            chu(im, (x0, y + dy), l, font(32, "sb"), TRANG, a)
            y += 42
        return y + 26
    if k == "nguoi":   # người tham dự: tên vàng + chức danh đầy đủ
        f2 = vua_dong(m["ten"], 40, rong, "bl")
        chu_vang(im, (x0, y + dy), m["ten"], f2, a)
        y += int(f2.size * 1.25)
        for l in can_dong(m["chuc"], font(28, "sb"), rong):
            chu(im, (x0, y + dy), l, font(28, "sb"), VANG_NHAT, a)
            y += 37
        return y + 18
    if k == "chip":   # nhãn nền vàng chữ xanh đậm (nhà tài trợ)
        f = font(32, "b")
        w = _do.textlength(m["text"], font=f) + 48
        lop = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dl = ImageDraw.Draw(lop)
        dl.rounded_rectangle([x0, y + dy, x0 + w, y + dy + 58], radius=29, fill=VANG_SO + (int(240 * a),))
        dl.text((x0 + 24, y + dy + 8), m["text"], font=f, fill=(10, 70, 30, int(255 * a)))
        im.paste(lop, (0, 0), lop)
        return y + 80
    if k == "dia_diem":   # ghim vị trí + địa điểm
        f, cx = font(30, "sb"), x0 + 16
        lop = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dl = ImageDraw.Draw(lop)
        dl.ellipse([cx - 14, y + dy, cx + 14, y + dy + 28], fill=VANG_SO + (int(255 * a),))
        dl.polygon([(cx - 12, y + dy + 20), (cx + 12, y + dy + 20), (cx, y + dy + 42)], fill=VANG_SO + (int(255 * a),))
        dl.ellipse([cx - 5, y + dy + 9, cx + 5, y + dy + 19], fill=(14, 92, 40, int(255 * a)))
        im.paste(lop, (0, 0), lop)
        for l in can_dong(m["text"], f, rong - 48):
            chu(im, (x0 + 44, y + dy), l, f, TRANG, a)
            y += 40
        return y + 24
    if k == "trich":   # ý chính phát biểu: ngoặc kép vàng + dòng chữ
        chu_vang(im, (x0 - 4, y - 30 + dy), "“", font(130, "bl"), a)
        y += 70
        for l in can_dong(m["text"], font(36, "b"), rong):
            chu(im, (x0, y + dy), l, font(36, "b"), TRANG, a)
            y += 48
        return y + 20
    raise ValueError(f"loại mục không biết: {k}")


def chu_mo_lon(im, text, t, t0):   # chữ to mờ phía sau, trôi chậm
    a = ease((t - t0) / 1.0) * 0.16
    lop = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    f = font(230, "bl")
    ImageDraw.Draw(lop).text(((W - _do.textlength(text, font=f)) / 2 - (t - t0) * 12, H - 330), text, font=f,
                             fill=(255, 255, 255, int(255 * a)))
    im.paste(lop, (0, 0), lop)


def khung(KB, t, vf=None):
    """Vẽ khung hình tại giây t. vf: khung video (tin có video) để thu vào/bung ra khỏi khung 65%."""
    im = nen(t)
    for c in KB["canh"]:
        if not (c["bd"] - 0.01 <= t < c["kt"]):
            continue
        (bx, by), (x0, x1) = bo_cuc(c["ben"])
        a = min(ease((t - c["bd"]) / 0.55), ease((c["kt"] - t) / 0.45)) if c.get("mo", True) else 1.0
        dx = int((1 - a) * (40 if c["ben"] == "T" else -40))
        if c.get("chu_mo"):
            chu_mo_lon(im, c["chu_mo"], t, c["bd"])
        ve_khung(im, bx + dx, by, a)
        if c.get("anh"):   # ảnh đổi trong khung, mờ chồng 0,5 s; zoom vào/ra xen kẽ
            n = len(c["anh"])
            dai = (c["kt"] - c["bd"]) / n
            i = min(n - 1, int((t - c["bd"]) / dai))
            p = (t - c["bd"] - i * dai) / dai
            cur = anh_ken_burns(c["anh"][i], p, 1 if i % 2 == 0 else -1, (0.6 if i % 2 else -0.6, -0.15))
            if i + 1 < n and p > 1 - 0.5 / dai:
                nx = anh_ken_burns(c["anh"][i + 1], 0, -1 if i % 2 == 0 else 1, (0.6 if i % 2 == 0 else -0.6, -0.15))
                cur = Image.blend(cur, nx, (p - (1 - 0.5 / dai)) / (0.5 / dai))
            if a < 1:
                cur = Image.blend(Image.new("RGB", cur.size, (10, 60, 40)), cur, a)
            im.paste(cur, (bx + dx, by))
        elif vf is None:   # xem thử không có video: để lỗ đen
            im.paste((0, 0, 0), (bx + dx, by, bx + dx + BW, by + BH))
        if "_cao" not in c:   # đo chiều cao khối chữ một lần để canh giữa theo khung ảnh
            nhap, yy0 = Image.new("RGB", (W, H)), 0
            for m in c["muc"]:
                yy0 = muc(nhap, m, 1e6, x0, x1, yy0)
            c["_cao"] = yy0
        y = max(CHU_Y_MIN, int(BY + BH / 2 - c["_cao"] / 2))
        hop = (x0 - 30, 160, x1 + 40, H - 40)
        nen_chu = im.crop(hop)
        for m in c["muc"]:
            if t < m["t"]:
                break
            y = muc(im, m, t, x0, x1, y)
        ra = ease((c["kt"] - t) / 0.4)
        if ra < 1:
            im.paste(Image.blend(nen_chu, im.crop(hop), ra), hop[:2])
    if vf is not None:   # video toàn màn hình ↔ thu vào khung 65% (0,7 s), viền vàng đi theo
        v0, v1 = KB["hop"]
        d_ = KB.get("chuyen", 0.7)
        u = min(1, max(0, (t - v0) / d_)) - min(1, max(0, (t - (v1 - d_)) / d_))
        p = u * u * (3 - 2 * u)
        w = int(round(W - (W - BW) * p))
        h = int(round(w * 9 / 16))
        x, y = int(round(60 * p)), int(round(BY * p))
        if p > 0:
            im.paste((5, 35, 12), (x + 10, y + 14, x + w + 18, y + h + 22))
            ImageDraw.Draw(im).rectangle([x - 8, y - 8, x + w + 7, y + h + 7], fill=(226, 180, 84))
        im.paste(vf if p == 0 else vf.resize((w, h), Image.BILINEAR), (x, y))
    return im


def doi_moc(v, moc):
    """Mốc ghi bằng tên câu → giây: "d2_01" (đầu câu), "d2_01$" (hết câu), thêm "+0.4"/"-0.3"."""
    if not isinstance(v, str):
        return v
    lech = 0.0
    if "+" in v[1:]:
        v, s = v.split("+", 1)
        lech = float(s)
    elif "-" in v[1:]:
        v, s = v.rsplit("-", 1)
        lech = -float(s)
    return (moc[v[:-1]][1] if v.endswith("$") else moc[v][0]) + lech


def giai_moc(KB, goc=Path(".")):
    """Đổi mọi "bd"/"kt"/"t" dạng tên câu ra giây theo KB["moc_file"] (đường dẫn tính từ goc)."""
    if "moc_file" not in KB:
        return KB
    M = json.loads((Path(goc) / KB["moc_file"]).read_text(encoding="utf-8"))
    moc = M.get("moc", M)
    KB.setdefault("het", M.get("het"))
    for c in KB["canh"]:
        c["bd"], c["kt"] = doi_moc(c["bd"], moc), doi_moc(c["kt"], moc)
        for m in c["muc"]:
            m["t"] = doi_moc(m["t"], moc)
    return KB


def doc_kich_ban(duong_dan):
    p = Path(duong_dan).resolve()
    KB = giai_moc(json.loads(p.read_text(encoding="utf-8")), p.parent)
    for c in KB["canh"]:
        c["anh"] = [str(p.parent / a) for a in c.get("anh", [])]
    for khoa in ("ra", "video"):
        if khoa in KB:
            KB[khoa] = str(p.parent / KB[khoa])
    return KB


def _ha_uu_tien():
    if sys.platform == "win32":   # máy hay sập khi chạy nặng
        import ctypes

        ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x40)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Dựng khung hình bố cục 65/35 cho tin ảnh.")
    ap.add_argument("kich_ban")
    ap.add_argument("--xem", action="store_true", help="chỉ xuất ảnh lưới xem thử")
    ap.add_argument("--chia", default="0/1", help="i/n: tiến trình này dựng khung thứ i, i+n, ... (chỉ tin ảnh)")
    args = ap.parse_args(argv)
    _ha_uu_tien()
    KB = doc_kich_ban(args.kich_ban)
    out = Path(KB["ra"])
    out.mkdir(parents=True, exist_ok=True)
    if args.xem:
        ts = KB.get("xem") or [c["bd"] + 2.5 for c in KB["canh"]]
        tile = Image.new("RGB", (640 * 3, 360 * ((len(ts) + 2) // 3)))
        with tempfile.TemporaryDirectory() as tmp:
            for i, t in enumerate(ts):
                vf = None
                if "video" in KB:   # dán khung video thật vào lỗ để thấy giống bản cuối
                    png = Path(tmp) / "v.png"
                    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", KB["video"], "-frames:v", "1",
                                    "-s", f"{W}x{H}", str(png)], check=True)
                    vf = Image.open(png).convert("RGB")
                tile.paste(khung(KB, t, vf).resize((640, 360)), ((i % 3) * 640, (i // 3) * 360))
        tile.save(out.parent / f"{out.name}_xem.jpg", quality=88)
        for t in KB.get("xem_lon", []):
            khung(KB, t).save(out.parent / f"{out.name}_{t:.1f}.png")
        print("đã lưu", out.parent / f"{out.name}_xem.jpg")
        return 0
    tu = KB.get("tu", 0.0)
    N = int(round((KB["het"] - tu) * FPS))
    i0, n_chia = (int(v) for v in args.chia.split("/"))
    doc = None
    if "video" in KB:   # đọc tuần tự từng khung video từ giây "tu" (khớp khung)
        doc = subprocess.Popen(["ffmpeg", "-v", "error", "-threads", "1", "-ss", f"{tu:.3f}", "-i", KB["video"], "-frames:v", str(N),
                                "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-"], stdout=subprocess.PIPE)
    for n in range(N):
        if doc is None and n % n_chia != i0:
            continue
        vf = Image.frombytes("RGB", (W, H), doc.stdout.read(W * H * 3)) if doc else None
        p = out / f"k_{n:05d}.jpg"
        if p.exists():   # chạy lại bỏ qua khung đã có
            continue
        khung(KB, tu + n / FPS, vf).save(p, quality=92)
        if n % 300 == 0:
            print(f"{n}/{N}", flush=True)
    print("KHUNG XONG", out, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
