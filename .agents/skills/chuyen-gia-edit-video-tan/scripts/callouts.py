#!/usr/bin/env python3
"""Hệ thống chú thích: mũi tên, vòng tròn, ngoặc, spotlight, kính lúp, ghim số, biểu đồ,
bộ đếm, quy trình nhiều bước, và chú thích bám theo vật thể (OpenCV tracker MIL).

    python callouts.py demo --style national-modern --out demo_callouts.png [--frame khung.png]
    python callouts.py track VIDEO --box x,y,w,h --start 3 --end 6 --out track.json [--sendcmd move.txt]

Hàm vẽ lên khung trả ảnh RGBA đúng cỡ khung (ghép bằng overlay=0:0); biểu đồ/bước/bộ đếm trả thẻ.
Quy tắc tránh: không đặt lên mặt, tay, micro, phụ đề (20% dưới) hay UI nền tảng (khung dọc).
validate_graphics.py kiểm các vùng này; tracker chỉ gợi ý vị trí — xem lại từng giây.
"""
from __future__ import annotations
import argparse
import json
import math
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from broadcast_kit import Kit, _ease, _wrap  # noqa: E402

VIEN = (0, 0, 0, 170)          # viền tối dưới nét sáng — nổi trên nền nào cũng đọc được


def _canvas(W: int, H: int) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def arrow(W, H, p0, p1, color, width=8):
    im, d = _canvas(W, H)
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    head = width * 3.2
    base = (p1[0] - head * math.cos(ang), p1[1] - head * math.sin(ang))
    tri = [p1, (base[0] + head * .6 * math.sin(ang), base[1] - head * .6 * math.cos(ang)),
           (base[0] - head * .6 * math.sin(ang), base[1] + head * .6 * math.cos(ang))]
    for col, w in ((VIEN, width + 6), (tuple(color) + (255,), width)):
        d.line([p0, base], fill=col, width=w)
        d.polygon(tri, fill=col, outline=col)
    return im


def circle_mark(W, H, center, r, color, width=8):
    im, d = _canvas(W, H)
    cx, cy = center
    for col, w in ((VIEN, width + 6), (tuple(color) + (255,), width)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=w)
    return im


def bracket(W, H, box, color, width=8, leg=0.22):
    """Bốn góc ngoặc quanh vật thể — nhẹ hơn khung kín, không che vật."""
    im, d = _canvas(W, H)
    x, y, w, h = box
    lx, ly = w * leg, h * leg
    goc = [((x, y + ly), (x, y), (x + lx, y)), ((x + w - lx, y), (x + w, y), (x + w, y + ly)),
           ((x, y + h - ly), (x, y + h), (x + lx, y + h)), ((x + w - lx, y + h), (x + w, y + h), (x + w, y + h - ly))]
    for col, wd in ((VIEN, width + 6), (tuple(color) + (255,), width)):
        for g in goc:
            d.line(g, fill=col, width=wd, joint="curve")
    return im


def spotlight(W, H, center, r, darkness=0.55):
    """Làm tối toàn khung, chừa một vùng tròn mềm."""
    mask = Image.new("L", (W, H), int(255 * darkness))
    cx, cy = center
    ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=0)
    mask = mask.filter(ImageFilter.GaussianBlur(r * .12))
    im = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    im.putalpha(mask)
    return im


def magnifier(frame: Image.Image, src_box, dst_center, zoom=2.0, ring=(255, 255, 255)):
    x, y, w, h = src_box
    r = round(max(w, h) * zoom / 2)
    lens = frame.convert("RGBA").crop((x, y, x + w, y + h)).resize((r * 2, r * 2), Image.LANCZOS)
    m = Image.new("L", (r * 2, r * 2), 0)
    ImageDraw.Draw(m).ellipse([0, 0, r * 2 - 1, r * 2 - 1], fill=255)
    lens.putalpha(m)
    im, d = _canvas(*frame.size)
    cx, cy = dst_center
    d.line([(x + w / 2, y + h / 2), (cx, cy)], fill=ring + (220,), width=4)
    d.rectangle([x, y, x + w, y + h], outline=ring + (230,), width=4)
    im.alpha_composite(lens, (cx - r, cy - r))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ring + (255,), width=7)
    return im


def pin(kit: Kit, xy, n: int):
    im, d = _canvas(kit.W, kit.H)
    r = kit.px("chip") * .9
    x, y = xy
    d.ellipse([x - r - 4, y - r - 4, x + r + 4, y + r + 4], fill=(255, 255, 255, 255))
    d.ellipse([x - r, y - r, x + r, y + r], fill=kit.m["nhan"] + (255,))
    f = kit.font(round(r * 1.2))
    s = str(n)
    d.text((x - d.textlength(s, font=f) / 2, y - f.size * .62), s, font=f, fill=(255, 255, 255))
    return im


def bar_chart(kit: Kit, values: list[float], labels: list[str], title: str, unit: str = ""):
    w, h, pad = round(kit.W * .42), round(kit.H * .46), round(kit.H * .03)
    im = kit._card(w, h)
    d = ImageDraw.Draw(im)
    ft, fl = kit.font(kit.px("chuc_danh")), kit.font(kit.px("chip"), False)
    d.text((pad, pad), title, font=ft, fill=kit.m["chu"])
    top, bot = pad * 2 + ft.size, h - pad - fl.size * 2
    vmax = max(values) or 1
    bw = (w - pad * 2) / len(values)
    for k, (v, lab) in enumerate(zip(values, labels)):
        x0 = pad + k * bw + bw * .18
        y0 = bot - (bot - top - fl.size) * v / vmax
        d.rounded_rectangle([x0, y0, x0 + bw * .64, bot], radius=4, fill=(kit.m["phu"] if k == len(values) - 1 else kit.m["chu_phu"]) + (255,))
        val = f"{v:g}{unit}"
        d.text((x0 + bw * .32 - d.textlength(val, font=fl) / 2, y0 - fl.size - 4), val, font=fl, fill=kit.m["chu"])
        lf = kit.fit(lab, fl.size, int(bw * .95), dam=False)
        d.text((x0 + bw * .32 - d.textlength(lab, font=lf) / 2, bot + 6), lab, font=lf, fill=kit.m["chu_phu"])
    return im


def steps_card(kit: Kit, steps: list[str], active: int | None = None):
    w, pad = round((kit.safe[2] - kit.safe[0]) * .5), round(kit.H * .025)
    fs = kit.font(kit.px("chuc_danh"), False)
    r = fs.size * .75
    rows = [_wrap(s, fs, w - pad * 3 - r * 2) for s in steps]
    h = pad * 2 + sum(len(x) * (fs.size + 6) + pad for x in rows)
    im = kit._card(w, round(h))
    d = ImageDraw.Draw(im)
    y = pad
    for k, lines in enumerate(rows):
        cx, cy = pad + r, y + fs.size * .6
        on = active is None or k <= active
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(kit.m["nhan"] if on else kit.m["nen_2"]) + (255,))
        f = kit.font(round(r * 1.1))
        d.text((cx - d.textlength(str(k + 1), font=f) / 2, cy - f.size * .6), str(k + 1), font=f, fill=(255, 255, 255))
        for ln in lines:
            d.text((pad * 2 + r * 2, y), ln, font=fs, fill=kit.m["chu"] if on else kit.m["chu_phu"])
            y += fs.size + 6
        y += pad
    return im


def counter_frames(kit: Kit, value: int, label: str, seconds: float, out_dir: Path, fps: int = 30) -> int:
    """Bộ đếm tăng dần tới giá trị thật trong 60% đầu, giữ nguyên phần còn lại."""
    out_dir.mkdir(parents=True, exist_ok=True)
    n = round(seconds * fps)
    for i in range(n):
        v = round(value * _ease(i / fps / (seconds * .6)))
        card, _ = kit.fact_card(f"{v:,}".replace(",", "."), label)
        card.save(out_dir / f"f_{i:04d}.png")
    return n


def track(video: str, box, start: float, end: float) -> list[dict]:
    """Bám vật thể bằng TrackerMIL (có sẵn trong OpenCV thường). Mất dấu thì dừng, không đoán."""
    import cv2
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    cap.set(cv2.CAP_PROP_POS_MSEC, start * 1000)
    ok, fr = cap.read()
    if not ok:
        raise SystemExit("Không đọc được khung ở mốc start")
    tr = cv2.TrackerMIL_create()
    tr.init(fr, tuple(int(v) for v in box))
    out, t = [{"t": round(start, 3), "x": box[0], "y": box[1], "w": box[2], "h": box[3]}], start
    while t < end:
        ok, fr = cap.read()
        t += 1 / fps
        if not ok:
            break
        found, b = tr.update(fr)
        if not found:
            out.append({"t": round(t, 3), "lost": True})
            break
        out.append({"t": round(t, 3), "x": int(b[0]), "y": int(b[1]), "w": int(b[2]), "h": int(b[3])})
    return out


def sendcmd(points: list[dict], name: str = "co", dx: int = 0, dy: int = 0) -> str:
    """Tệp sendcmd để overlay@<name> chạy theo vật thể: ... sendcmd=f=move.txt, ... overlay@co=..."""
    return "".join(f"{p['t']} overlay@{name} x {p['x'] + dx}, overlay@{name} y {p['y'] + dy};\n"
                   for p in points if not p.get("lost"))


def demo(style: str, out: Path, frame: Path | None):
    kit = Kit(style, "16:9")
    nen = (Image.open(frame).convert("RGBA").resize((kit.W, kit.H)) if frame
           else Image.new("RGBA", (kit.W, kit.H), (110, 118, 126, 255)))
    # thẻ trước, dấu chú thích sau — dấu phải nằm trên cùng
    nen.alpha_composite(bar_chart(kit, [1800, 2100, 2500], ["2024", "2025", "2026"], "Người được khám"), (kit.safe[0], kit.safe[1]))
    nen.alpha_composite(steps_card(kit, ["Tiếp nhận", "Đo huyết áp", "Lấy mẫu máu", "Bác sĩ tư vấn"], active=2),
                        (kit.safe[0], round(kit.H * .52)))
    nen.alpha_composite(spotlight(kit.W, kit.H, (1400, 420), 170, .35))
    nen.alpha_composite(arrow(kit.W, kit.H, (1080, 260), (1300, 380), kit.m["phu"]))
    nen.alpha_composite(circle_mark(kit.W, kit.H, (1400, 420), 110, kit.m["phu"]))
    nen.alpha_composite(bracket(kit.W, kit.H, (1100, 620, 250, 200), kit.m["phu"]))
    nen.alpha_composite(pin(kit, (1700, 230), 1))
    nen.alpha_composite(pin(kit, (1180, 560), 2))
    nen.alpha_composite(magnifier(nen.copy(), (1330, 360, 140, 120), (1650, 800), 1.8))
    nen.convert("RGB").save(out)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("demo")
    d.add_argument("--style", default="national-modern")
    d.add_argument("--out", type=Path, default=Path("demo_callouts.png"))
    d.add_argument("--frame", type=Path)
    t = sub.add_parser("track")
    t.add_argument("video")
    t.add_argument("--box", required=True, help="x,y,w,h ở mốc start")
    t.add_argument("--start", type=float, required=True)
    t.add_argument("--end", type=float, required=True)
    t.add_argument("--out", type=Path, default=Path("track.json"))
    t.add_argument("--sendcmd", type=Path)
    a = ap.parse_args()
    if a.cmd == "demo":
        print(demo(a.style, a.out, a.frame))
        return 0
    pts = track(a.video, [int(v) for v in a.box.split(",")], a.start, a.end)
    a.out.write_text(json.dumps(pts), encoding="utf-8")
    if a.sendcmd:
        a.sendcmd.write_text(sendcmd(pts), encoding="utf-8")
    lost = any(p.get("lost") for p in pts)
    print(f"{len(pts)} điểm{' — MẤT DẤU, rút ngắn đoạn bám' if lost else ''} -> {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
