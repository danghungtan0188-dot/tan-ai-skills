#!/usr/bin/env python3
"""Kiem cho lo chop hinh nguoi noi giua do hoa va cu cat, tinh giay tren video da cat.

  python scripts/kiem_chop_hinh.py <moc.json>

moc.json: {"cuts": [12.0, 30.5], "overlays": [{"start": 12.2, "end": 15.0}]}
Exit 0 = dat; 1 = co cho chop (in giay + cach sua); 2 = khong doc duoc dau vao.
"""

import json
import sys

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

KHOANG_CHOP = 0.5


def kiem(cuts, overlays):
    """Tra ve danh sach loi, moi loi la mot cau neu cho sai va cach sua."""
    cuts = sorted(cuts)
    overlays = sorted(overlays, key=lambda o: o["start"])
    loi = []
    for o in overlays:
        if not 0 <= o["start"] < o["end"]:
            raise ValueError(f"do hoa sai: {o}")
        for c in cuts:
            if 0 < o["start"] - c < KHOANG_CHOP:
                loi.append(f"do hoa {o['start']}s bat dau sat sau cu cat {c}s: doi diem dau ve {c}s")
            if 0 < c - o["end"] < KHOANG_CHOP:
                loi.append(f"do hoa ket thuc {o['end']}s sat truoc cu cat {c}s: keo den {c}s")
    for a, b in zip(overlays, overlays[1:]):
        if 0 < b["start"] - a["end"] < KHOANG_CHOP:
            loi.append(f"hai do hoa cach nhau duoi {KHOANG_CHOP}s ({a['end']}s - {b['start']}s): noi lien lai")
    return loi


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            du_lieu = json.load(f)
        loi = kiem(du_lieu["cuts"], du_lieu["overlays"])
    except (OSError, ValueError, KeyError, TypeError) as e:
        print(f"LOI: {e}")
        return 2
    for x in loi:
        print(f"FAIL {x}")
    if loi:
        return 1
    print(f"PASS {len(du_lieu['overlays'])} do hoa, khong co cho chop")
    return 0


if __name__ == "__main__":
    sys.exit(main())
