#!/usr/bin/env python3
"""Tim nhip (beat) cua ban nhac, roi goi y doi chuyen canh / do hoa vao nhip gan nhat.

  python scripts/tim_nhip_nhac.py <nhac> [--bat-dau 2.0] [--moc moc.json] [-o nhip.json]

--bat-dau: giay tren video ma ban nhac bat dau phat. --moc: danh sach giay can khop, dang [12.3, 30.1]
hoac {"moc": [...]}. Chi doi chuyen canh va diem vao cua do hoa; diem cat loi noi giu theo cau noi.
Exit 0 = xong; 2 = khong doc duoc dau vao.
"""

import argparse
import json
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

SAI_SO = 0.15  # chi doi khi nhip nam trong 0,15 giay, xa hon thi giu nguyen


def tim_nhip(duong_dan):
    """Tra ve (bpm, [giay cua tung nhip]) tinh tu dau ban nhac."""
    import librosa

    y, sr = librosa.load(str(duong_dan), sr=22050, mono=True)
    if y.size == 0:
        raise ValueError(f"ban nhac rong: {duong_dan}")
    bpm, nhip = librosa.beat.beat_track(y=y, sr=sr, units="time")
    return float(sum(bpm) / len(bpm) if hasattr(bpm, "__len__") else bpm), [round(float(g), 3) for g in nhip]


def goi_y(moc, nhip, sai_so=SAI_SO):
    """Voi moi moc, tra ve (moc, nhip gan nhat) neu lech trong sai so va chua trung nhip; khong thi bo qua."""
    ket_qua = []
    for m in moc:
        gan = min(nhip, key=lambda b: abs(b - m), default=None)
        if gan is not None and 0 < abs(gan - m) <= sai_so:
            ket_qua.append((m, gan))
    return ket_qua


def doc_moc(duong_dan):
    with open(duong_dan, encoding="utf-8") as f:
        du_lieu = json.load(f)
    moc = du_lieu["moc"] if isinstance(du_lieu, dict) else du_lieu
    return [float(m) for m in moc]


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("nhac")
    p.add_argument("--bat-dau", type=float, default=0.0)
    p.add_argument("--moc")
    p.add_argument("-o", "--ra")
    a = p.parse_args()
    try:
        bpm, nhip = tim_nhip(a.nhac)
        nhip = [round(g + a.bat_dau, 3) for g in nhip]
        moc = doc_moc(a.moc) if a.moc else []
    except (OSError, ValueError, KeyError, TypeError, ImportError, json.JSONDecodeError) as e:
        print(f"LOI: {e}")
        return 2
    if not nhip:
        print("LOI: khong tim thay nhip (nhac qua nhe hoac khong co phach ro)")
        return 2
    print(f"{bpm:.0f} BPM, {len(nhip)} nhip, tu {nhip[0]}s den {nhip[-1]}s tren video")
    for m, b in goi_y(moc, nhip):
        print(f"DOI {m}s -> {b}s")
    if a.ra:
        Path(a.ra).write_text(json.dumps({"bpm": round(bpm, 1), "nhip": nhip}, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
