#!/usr/bin/env python3
"""Doc lai phu de tren khung hinh bang OCR roi so voi file SRT, de AI khoi phai xem tung anh.

  python scripts/kiem_phu_de_ocr.py <video> <phu_de.srt> [--nguong 0.6] [--toi-da 12]

Chu phai dung ca dau tieng Viet moi tinh la khop. Chi lay mau toi da --toi-da cau, trai deu cho nhe may.
Exit 0 = dat; 1 = co cau khong doc ra dung; 2 = khong doc duoc dau vao;
3 = may chua co Tesseract kem du lieu tieng Viet (coi nhu NOT RUN, khong phai PASS).
"""

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

DUONG_TESSERACT_WINDOWS = Path("C:/Program Files/Tesseract-OCR/tesseract.exe")
MOC_GIO = re.compile(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)")


class ThieuTesseract(Exception):
    pass


def doc_srt(noi_dung):
    """Tra ve danh sach (giay giua cau, chu cua cau)."""
    cau = []
    for khoi in re.split(r"\n\s*\n", noi_dung.replace("\r\n", "\n").strip()):
        dong = khoi.split("\n")
        for i, d in enumerate(dong):
            m = MOC_GIO.search(d)
            if m:
                s = [int(x) for x in m.groups()]
                dau = s[0] * 3600 + s[1] * 60 + s[2] + s[3] / 1000
                cuoi = s[4] * 3600 + s[5] * 60 + s[6] + s[7] / 1000
                chu = re.sub(r"<[^>]+>|\{[^}]+\}", "", " ".join(dong[i + 1:])).strip()
                if chu:
                    cau.append(((dau + cuoi) / 2, chu))
                break
    return cau


def tach_tu(chu):
    """Tach tu, giu dau tieng Viet: "mat" va "mặt" la hai tu khac nhau."""
    return re.findall(r"\w+", unicodedata.normalize("NFC", chu).lower())


def ty_le_khop(cau, chu_doc_duoc):
    tu = tach_tu(cau)
    if not tu:
        return 1.0
    co = set(tach_tu(chu_doc_duoc))
    return sum(t in co for t in tu) / len(tu)


def chon_mau(cau, toi_da):
    if len(cau) <= toi_da:
        return cau
    return [cau[i * len(cau) // toi_da] for i in range(toi_da)]


def tim_tesseract():
    lenh = shutil.which("tesseract") or (str(DUONG_TESSERACT_WINDOWS) if DUONG_TESSERACT_WINDOWS.exists() else None)
    if not lenh:
        raise ThieuTesseract("chua cai Tesseract")
    kq = subprocess.run([lenh, "--list-langs"], capture_output=True, text=True)
    if "vie" not in (kq.stdout + kq.stderr).split():
        raise ThieuTesseract("Tesseract chua co du lieu tieng Viet (vie)")
    return lenh


def doc_chu_khung(video, giay, thu_muc, tesseract):
    anh = Path(thu_muc) / "khung.png"
    kq = subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-ss", f"{giay:.3f}", "-i", str(video), "-frames:v", "1", str(anh)],
        capture_output=True,
    )
    if kq.returncode != 0 or not anh.exists():
        raise ValueError(f"khong lay duoc khung hinh tai {giay:.2f}s")
    kq = subprocess.run([tesseract, str(anh), "-", "-l", "vie"], capture_output=True)
    if kq.returncode != 0:
        raise ValueError(f"Tesseract loi tai {giay:.2f}s")
    return kq.stdout.decode("utf-8", errors="replace")


def kiem(cau, doc_chu, nguong):
    """doc_chu(giay) tra ve chu doc duoc tren khung hinh. Tra ve cac cau khong dat."""
    loi = []
    for giay, chu in cau:
        ty_le = ty_le_khop(chu, doc_chu(giay))
        if ty_le < nguong:
            loi.append((giay, chu, ty_le))
    return loi


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("video")
    p.add_argument("srt")
    p.add_argument("--nguong", type=float, default=0.6)
    p.add_argument("--toi-da", type=int, default=12)
    a = p.parse_args()
    try:
        tesseract = tim_tesseract()
    except ThieuTesseract as e:
        print(f"NOT RUN: {e}")
        return 3
    try:
        cau = chon_mau(doc_srt(Path(a.srt).read_text(encoding="utf-8-sig")), a.toi_da)
        if not cau:
            raise ValueError("file SRT khong co cau nao")
        with tempfile.TemporaryDirectory() as tmp:
            loi = kiem(cau, lambda g: doc_chu_khung(a.video, g, tmp, tesseract), a.nguong)
    except (OSError, ValueError, UnicodeDecodeError) as e:
        print(f"LOI: {e}")
        return 2
    for giay, chu, ty_le in loi:
        print(f"FAIL {giay:.2f}s: khop {ty_le:.0%} - \"{chu}\"")
    if loi:
        return 1
    print(f"PASS {len(cau)} cau mau, nguong {a.nguong:.0%}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
