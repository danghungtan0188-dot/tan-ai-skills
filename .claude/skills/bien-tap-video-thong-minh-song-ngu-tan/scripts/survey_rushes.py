#!/usr/bin/env python3
"""Khảo sát cả thư mục video thô: đo từng clip, tách cảnh, chấm nét/sáng/động từng cảnh.

    python survey_rushes.py FOLDER --out rushes.json --sheet contact.jpg [--threshold 0.12] [--min-shot 1.2]

Xuất `rushes.json` (số liệu) và `contact.jpg` (ảnh bảng, mỗi ô một cảnh, có nhãn `clip.cảnh  t=…  dài…`).
Cảnh dài hơn `--anh-them` giây được lấy thêm 2 ảnh ở 1/4 và 3/4 cảnh — một khung giữa cảnh
không đủ để biết cảnh dài quay những gì.
Máy chỉ ĐO. Cảnh nào nói về cái gì thì phải nhìn contact sheet mà xác định, không suy từ số liệu.

Cột số liệu mỗi cảnh:
  net   phương sai Laplacian — dưới ~60 là mờ/mất nét, cần xem lại trước khi đưa vào bản tin
  sang  độ sáng trung bình 0–255 — dưới 45 là tối, trên 215 là cháy sáng
  dong  chênh lệch hai khung cách nhau 0,5 s — cao là máy rung, lia nhanh HOẶC chủ thể
        chuyển động mạnh. Đây là tín hiệu để xem lại, không phải kết luận máy rung.

Cảnh báo (không chặn): clip khác tỉ lệ/fps so với đa số, clip câm, cảnh tối/mờ/rung.
Bước sau: build_edit_plan.py.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from detect_scenes import detect  # noqa: E402

CAN_CO = (("cv2", "opencv-python"), ("numpy", "numpy"), ("PIL", "Pillow"))


def kiem_moi_truong() -> None:
    """Báo thiếu thư viện/ffmpeg ngay từ đầu, thay vì chết giữa chừng sau khi đã quét nửa kho."""
    import importlib.util
    import shutil
    thieu = [goi for mo, goi in CAN_CO if importlib.util.find_spec(mo) is None]
    if thieu:
        raise SystemExit("Thiếu thư viện: pip install " + " ".join(thieu))
    khong = [x for x in ("ffmpeg", "ffprobe") if not shutil.which(x)]
    if khong:
        raise SystemExit("Không thấy " + ", ".join(khong) + " trong PATH")

DUOI = {".mp4", ".mov", ".mts", ".m4v", ".avi", ".mkv", ".mpg", ".mpeg", ".wmv"}
BO_QUA = {".git", "node_modules", "outputs", "output", "render", "renders", "edit", "thumbs", "cache", "__pycache__"}
NET_THAP, SANG_TOI, SANG_CHAY, DONG_CAO = 60.0, 45.0, 215.0, 28.0
THUMB_W, THUMB_H, COT = 320, 180, 6


def tim_clip(folder: Path, recursive: bool = False) -> list[Path]:
    """Tìm video trong đúng kho được chỉ định; không đi vào thư mục đầu ra/cache."""
    if folder.is_file():
        return [folder.resolve()] if folder.suffix.lower() in DUOI else []
    iterator = folder.rglob("*") if recursive else folder.iterdir()
    return sorted(
        (p.resolve() for p in iterator
         if p.is_file() and p.suffix.lower() in DUOI
         and not any(part.lower() in BO_QUA for part in p.relative_to(folder).parts[:-1])),
        key=lambda p: str(p).lower(),
    )


FONT_UNG_VIEN = ("C:/Windows/Fonts/arial.ttf",
                 "/System/Library/Fonts/Supplemental/Arial.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")


def font(co: int):
    from PIL import ImageFont
    for f in FONT_UNG_VIEN:
        if Path(f).exists():
            return ImageFont.truetype(f, co)
    return ImageFont.load_default()


def probe(p: Path) -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration:stream=codec_type,width,height,avg_frame_rate:stream_side_data=rotation",
                        "-of", "json", str(p)], text=True, capture_output=True, check=True)
    d = json.loads(r.stdout)
    v = next((s for s in d["streams"] if s.get("codec_type") == "video"), None)
    if v is None:
        raise SystemExit(f"{p.name}: không có luồng hình")
    a, b = (v.get("avg_frame_rate") or "0/1").split("/")
    xoay = 0
    for sd in v.get("side_data_list", []):
        if "rotation" in sd:
            xoay = int(sd["rotation"]) % 360
    return {"duration": float(d["format"]["duration"]), "width": v["width"], "height": v["height"],
            "fps": round(float(a) / float(b or 1), 3) if float(b or 0) else 0.0, "rotation": xoay,
            "audio": any(s.get("codec_type") == "audio" for s in d["streams"])}


def do_am(p: Path) -> float | None:
    """LUFS tích hợp của clip — để biết clip nào quá nhỏ tiếng trước khi ghép."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(p), "-vn", "-af",
                        "loudnorm=print_format=json", "-f", "null", "-"],
                       text=True, capture_output=True, encoding="utf-8", errors="replace")
    try:
        return float(json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])["input_i"])
    except (ValueError, KeyError):
        return None


def cham_canh(cap, t0: float, t1: float):
    """Nét, sáng, động của một cảnh + ảnh thu nhỏ ở giữa cảnh."""
    import cv2
    import numpy as np
    giua = (t0 + t1) / 2
    cap.set(cv2.CAP_PROP_POS_MSEC, giua * 1000)
    ok, fr = cap.read()
    if not ok:
        return None, None
    xam = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    cap.set(cv2.CAP_PROP_POS_MSEC, min(giua + 0.5, t1 - 0.02) * 1000)
    ok2, fr2 = cap.read()
    dong = float(np.mean(cv2.absdiff(xam, cv2.cvtColor(fr2, cv2.COLOR_BGR2GRAY)))) if ok2 else 0.0
    so = {"net": round(float(cv2.Laplacian(xam, cv2.CV_64F).var()), 1),
          "sang": round(float(xam.mean()), 1), "dong": round(dong, 2)}
    return so, cv2.resize(fr, (THUMB_W, THUMB_H))


def anh_them(cap, t0: float, t1: float) -> list:
    """Hai ảnh ở 1/4 và 3/4 cảnh — cảnh dài thường chứa nhiều nội dung khác nhau."""
    import cv2
    ra = []
    for r in (0.25, 0.75):
        cap.set(cv2.CAP_PROP_POS_MSEC, (t0 + (t1 - t0) * r) * 1000)
        ok, fr = cap.read()
        if ok:
            ra.append(cv2.resize(fr, (THUMB_W, THUMB_H)))
    return ra


def khao_sat(files: list[Path], threshold: float, min_shot: float, thumb_dir: Path,
             anh_them_giay: float = 10.0) -> dict:
    import cv2
    thumb_dir.mkdir(parents=True, exist_ok=True)
    clips, canh_bao = [], []
    for i, f in enumerate(files):
        m = probe(f)
        d = detect(f, threshold, fast=True)
        moc = [0.0] + [c for c in d["cuts"] if 0 < c < m["duration"]] + [m["duration"]]
        cap = cv2.VideoCapture(str(f))
        shots = []
        for k in range(len(moc) - 1):
            t0, t1 = moc[k], moc[k + 1]
            if t1 - t0 < min_shot:               # cảnh quá ngắn thường là nháy sáng, không dùng được
                continue
            so, thumb = cham_canh(cap, t0, t1)
            if so is None:
                continue
            sid = f"{i}.{len(shots) + 1}"
            tp = thumb_dir / f"{sid}.jpg"
            cv2.imwrite(str(tp), thumb)
            them = []
            if t1 - t0 >= anh_them_giay:
                for j, im in enumerate(anh_them(cap, t0, t1)):
                    q = thumb_dir / f"{sid}_{'ab'[j]}.jpg"
                    cv2.imwrite(str(q), im)
                    them.append(q)
            shots.append({"id": sid, "start": round(t0, 2), "end": round(t1, 2),
                          "dur": round(t1 - t0, 2), **so, "thumb": str(tp.resolve()),
                          "them": [str(x.resolve()) for x in them]})
            if so["net"] < NET_THAP:
                canh_bao.append(f"{sid} ({f.name}) mờ: net={so['net']}")
            if so["sang"] < SANG_TOI or so["sang"] > SANG_CHAY:
                canh_bao.append(f"{sid} ({f.name}) sáng lệch: {so['sang']}")
            if so["dong"] > DONG_CAO:
                canh_bao.append(f"{sid} ({f.name}) rung/lia mạnh: dong={so['dong']}")
        cap.release()
        clips.append({"idx": i, "file": str(f.resolve()), "name": f.name, **m,
                      "lufs": do_am(f) if m["audio"] else None, "shots": shots})
        if not m["audio"]:
            canh_bao.append(f"{f.name}: clip câm — không có tiếng hiện trường")
    khung = [(c["width"], c["height"]) for c in clips]
    fps = [c["fps"] for c in clips]
    for c in clips:                              # lệch chuẩn so với đa số thì phải chuẩn hoá khi ghép
        if khung.count((c["width"], c["height"])) < max(khung.count(k) for k in khung):
            canh_bao.append(f"{c['name']}: khung {c['width']}x{c['height']} khác đa số")
        if fps.count(c["fps"]) < max(fps.count(k) for k in fps):
            canh_bao.append(f"{c['name']}: {c['fps']} fps khác đa số")
        if c["rotation"]:
            canh_bao.append(f"{c['name']}: cờ xoay {c['rotation']}° — kiểm lại chiều hình")
    return {"clips": clips, "canh_bao": canh_bao,
            "tong_canh": sum(len(c["shots"]) for c in clips),
            "tong_thoi_luong": round(sum(c["duration"] for c in clips), 2)}


def contact_sheet(data: dict, out: Path) -> None:
    from PIL import Image, ImageDraw
    shots = []
    for c in data["clips"]:
        for s in c["shots"]:
            shots.append((c, s, s["id"], s["thumb"]))
            for j, x in enumerate(s.get("them", [])):
                shots.append((c, s, s["id"] + "·" + "ab"[j], x))
    if not shots:
        return
    hang = (len(shots) + COT - 1) // COT
    o = 26
    bang = Image.new("RGB", (COT * THUMB_W, hang * (THUMB_H + o)), (18, 18, 20))
    d = ImageDraw.Draw(bang)
    ft = font(15)
    for k, (c, s, nhan, anh) in enumerate(shots):
        x, y = (k % COT) * THUMB_W, (k // COT) * (THUMB_H + o)
        bang.paste(Image.open(anh), (x, y))
        xau = f"{nhan}  t={s['start']:.1f}s  {s['dur']:.1f}s  {c['name'][:14]}"
        kem = s["net"] < NET_THAP or s["sang"] < SANG_TOI or s["dong"] > DONG_CAO
        d.text((x + 5, y + THUMB_H + 4), xau, font=ft, fill=(255, 120, 90) if kem else (225, 225, 225))
    bang.save(out, quality=88)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", type=Path, help="thư mục chứa clip thô (hoặc một file)")
    ap.add_argument("--out", type=Path, default=Path("rushes.json"))
    ap.add_argument("--sheet", type=Path, help="ảnh bảng cảnh để xem bằng mắt")
    ap.add_argument("--threshold", type=float, default=0.12)
    ap.add_argument("--min-shot", type=float, default=1.2, help="bỏ cảnh ngắn hơn ngần này")
    ap.add_argument("--anh-them", type=float, default=10.0,
                    help="cảnh dài hơn ngần này thì lấy thêm 2 ảnh ở 1/4 và 3/4 cảnh")
    ap.add_argument("--recursive", action="store_true",
                    help="quét cả các thư mục con trong kho; tự bỏ qua output/render/edit/cache")
    a = ap.parse_args()
    kiem_moi_truong()
    files = tim_clip(a.folder, a.recursive)
    if not files:
        raise SystemExit(f"Không thấy clip nào trong {a.folder}")
    thumb_dir = a.out.parent / "thumbs"
    data = khao_sat(files, a.threshold, a.min_shot, thumb_dir, a.anh_them)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    if a.sheet:
        a.sheet.parent.mkdir(parents=True, exist_ok=True)
        contact_sheet(data, a.sheet)
    print(f"{len(files)} clip, {data['tong_canh']} cảnh, {data['tong_thoi_luong']:.1f}s -> {a.out}"
          + (f" + {a.sheet}" if a.sheet else ""))
    for x in data["canh_bao"]:
        print("CẢNH BÁO ", x)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
