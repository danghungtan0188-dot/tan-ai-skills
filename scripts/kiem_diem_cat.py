#!/usr/bin/env python3
"""Kiem diem cat theo song am: co cat giua tieng noi khong, co mat lan nao sau khi cat khong.

  python scripts/kiem_diem_cat.py <video nguon> <edit_plan.json> [--ra <video da cat>]

<edit_plan.json> la EditPlan (co "segments") hoac danh sach {"start", "end"}, tinh giay tren nguon.
Exit 0 = dat; 1 = co diem cat loi (in giay + goi y doi diem cat); 2 = khong doc duoc dau vao.
"""

import argparse
import json
import subprocess
import sys

import numpy as np

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

TAN_SO = 16000
CUA_SO = 0.01  # moi o do 10 ms
NUA_VUNG_CAT = 0.03  # xet 30 ms hai ben diem cat
TAM_GOI_Y = 0.3  # chi goi y doi diem cat trong 0.3 giay
LECH_THOI_LUONG = 0.1


def do_rms(duong_dan):
    """Tra ve muc am (RMS) tung o 10 ms cua am thanh trong file."""
    kq = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(duong_dan), "-vn", "-ac", "1", "-ar", str(TAN_SO),
         "-f", "s16le", "-"],
        capture_output=True,
    )
    if kq.returncode != 0 or not kq.stdout:
        raise ValueError(f"khong doc duoc am thanh tu {duong_dan}")
    mau = np.frombuffer(kq.stdout, dtype=np.int16).astype(np.float64)
    co = int(TAN_SO * CUA_SO)
    so_o = len(mau) // co
    if so_o == 0:
        raise ValueError(f"am thanh qua ngan: {duong_dan}")
    return np.sqrt(np.mean(mau[:so_o * co].reshape(so_o, co) ** 2, axis=1))


def nguong_tieng(rms):
    """Nguong phan biet tieng noi va khoang lang, tinh theo chinh file do."""
    return max(float(np.percentile(rms, 10)) * 3, float(np.percentile(rms, 95)) * 0.1)


def _o(giay):
    return int(round(giay / CUA_SO))


def _co_tieng(rms, tu, den, nguong):
    doan = rms[max(0, _o(tu)):max(0, _o(den))]
    return doan.size > 0 and float(doan.max()) >= nguong


def goi_y_diem_cat(rms, giay, nguong):
    """Diem lang gan nhat trong tam goi y; None neu khong co."""
    tam = _o(TAM_GOI_Y)
    goc = _o(giay)
    for lech in range(tam + 1):
        for o in (goc - lech, goc + lech):
            if 0 <= o < rms.size and rms[o] < nguong:
                return round(o * CUA_SO, 2)
    return None


def kiem_doan(rms, doan):
    """Tra ve danh sach loi. Chi cat giua tieng khi ca hai ben diem cat deu co tieng."""
    nguong = nguong_tieng(rms)
    tong = rms.size * CUA_SO
    loi = []
    for i, d in enumerate(doan, 1):
        for ten, giay in (("dau", d["start"]), ("cuoi", d["end"])):
            if giay <= 0 or giay >= tong:
                continue
            if _co_tieng(rms, giay - NUA_VUNG_CAT, giay, nguong) and _co_tieng(rms, giay, giay + NUA_VUNG_CAT, nguong):
                loi.append({"doan": i, "bien": ten, "giay": giay, "goi_y": goi_y_diem_cat(rms, giay, nguong)})
    return loi


def do_thoi_luong(duong_dan):
    kq = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(duong_dan)],
        capture_output=True, text=True,
    )
    if kq.returncode != 0 or not kq.stdout.strip():
        raise ValueError(f"khong do duoc thoi luong: {duong_dan}")
    return float(kq.stdout.strip())


def doc_doan(duong_dan):
    with open(duong_dan, encoding="utf-8") as f:
        du_lieu = json.load(f)
    doan = du_lieu["segments"] if isinstance(du_lieu, dict) else du_lieu
    for d in doan:
        if not 0 <= d["start"] < d["end"]:
            raise ValueError(f"doan sai: {d}")
    return doan


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("nguon")
    p.add_argument("doan")
    p.add_argument("--ra", help="video da cat, de doi chieu tong thoi luong")
    a = p.parse_args()
    try:
        doan = doc_doan(a.doan)
        loi = kiem_doan(do_rms(a.nguon), doan)
        lech = None
        if a.ra:
            ky_vong = sum(d["end"] - d["start"] for d in doan)
            thuc = do_thoi_luong(a.ra)
            if abs(thuc - ky_vong) > LECH_THOI_LUONG:
                lech = (ky_vong, thuc)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as e:
        print(f"LOI: {e}")
        return 2
    for x in loi:
        goi_y = f"doi sang {x['goi_y']}s" if x["goi_y"] is not None else "khong co cho lang gan day, chon cau khac"
        print(f"FAIL doan {x['doan']} bien {x['bien']} {x['giay']}s: cat giua tieng noi; {goi_y}")
    if lech:
        print(f"FAIL tong thoi luong: ky vong {lech[0]:.2f}s, video da cat {lech[1]:.2f}s")
    if loi or lech:
        return 1
    print(f"PASS {len(doan)} doan, khong cat giua tieng noi")
    return 0


if __name__ == "__main__":
    sys.exit(main())
