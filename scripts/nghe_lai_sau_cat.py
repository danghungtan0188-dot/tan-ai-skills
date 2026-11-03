#!/usr/bin/env python3
"""Nghe lai ban da cat bang whisper, ghi toan bo loi ra file va bao cum tu lap sat nhau.

  python scripts/nghe_lai_sau_cat.py <video da cat> --ra edit/nghe_lai.txt [--ngon-ngu vi]

Lan nghe dau hay gop cau lap, nen sau khi cat phai doc lai ca file nay. Cum lap chi la nghi van:
tieng Viet co cach noi lap co chu y, nguoi/AI doc roi moi quyet dinh.
Exit 0 = khong thay cum lap; 1 = co cum lap can doc; 2 = khong nghe duoc.
"""

import argparse
import re
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

CUM_NGAN_NHAT = 2  # lap 1 chu thuong la lay tu ("tu tu"), khong bao
CUM_DAI_NHAT = 30
CUM_DAI_TU = 5  # tu do dai nay cho phep lech chu va co chu xen giua hai lan
TY_LE_GIONG = 0.8
CHU_XEN_TOI_DA = 2
KHUC_NGHE = 6  # giay; khuc dai 30 giay lam whisper gop hai lan noi thanh mot


def chuan(chu):
    return re.sub(r"[^\w]", "", unicodedata.normalize("NFC", chu.lower()))


def _giong(a, b):
    """Cum ngan phai giong het; cum dai cho phep whisper nghe lech vai chu giua hai lan."""
    if len(a) != len(b):
        return False
    if len(a) < CUM_DAI_TU:
        return a == b
    return sum(x == y for x, y in zip(a, b)) / len(a) >= TY_LE_GIONG


def tim_lap(tu):
    """tu = [(chu, giay bat dau)]. Tra ve [(giay, cum tu)] cho cum lap lien tiep, uu tien cum dai."""
    sach = [(chuan(c), g) for c, g in tu if chuan(c)]
    chu = [c for c, _ in sach]
    ket_qua = []
    i = 0
    while i < len(chu):
        buoc = 1
        for n in range(CUM_DAI_NHAT, CUM_NGAN_NHAT - 1, -1):
            khe = range(CHU_XEN_TOI_DA + 1) if n >= CUM_DAI_TU else (0,)
            k = next((k for k in khe if _giong(chu[i:i + n], chu[i + n + k:i + 2 * n + k])), None)
            if k is not None:
                ket_qua.append((sach[i][1], " ".join(chu[i:i + n])))
                buoc = 2 * n + k
                break
        i += buoc
    return ket_qua


def ghi_loi(doan):
    """doan = [(giay, loi)]. Tra ve noi dung file doc lai."""
    return "".join(f"[{int(g) // 60:02d}:{g % 60:04.1f}] {loi.strip()}\n" for g, loi in doan)


def nghe(video, ngon_ngu):
    """Tra ve (doan, tu). Mot luong, model small: may hay sap khi chay nang."""
    from faster_whisper import WhisperModel

    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "a.wav"
        kq = subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", str(wav)],
            capture_output=True,
        )
        if kq.returncode != 0:
            raise ValueError(f"khong doc duoc am thanh tu {video}")
        m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=1)
        # condition_on_previous_text=False: giu cau lap thay vi lam muot di
        # vad_filter: khong tu "nghe" ra loi tu doan khong co tieng nguoi
        phan, _ = m.transcribe(str(wav), language=ngon_ngu, word_timestamps=True,
                               condition_on_previous_text=False, vad_filter=True,
                               chunk_length=KHUC_NGHE)
        doan, tu = [], []
        for p in phan:
            doan.append((p.start, p.text))
            tu.extend((w.word, w.start) for w in (p.words or []))
    return doan, tu


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("video")
    p.add_argument("--ra", required=True)
    p.add_argument("--ngon-ngu", default="vi")
    a = p.parse_args()
    try:
        doan, tu = nghe(a.video, a.ngon_ngu)
        if not doan:
            raise ValueError("whisper khong nghe duoc loi nao")
        Path(a.ra).write_text(ghi_loi(doan), encoding="utf-8")
    except (OSError, ValueError, ImportError) as e:
        print(f"LOI: {e}")
        return 2
    lap = tim_lap(tu)
    for giay, cum in lap:
        print(f"NGHI LAP {giay:.1f}s: \"{cum}\"")
    print(f"Doc ca file: {a.ra}")
    return 1 if lap else 0


if __name__ == "__main__":
    sys.exit(main())
