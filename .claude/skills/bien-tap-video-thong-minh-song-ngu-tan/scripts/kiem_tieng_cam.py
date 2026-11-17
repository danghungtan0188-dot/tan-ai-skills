"""Kiem video/am thanh khong co doan bi cam giua chung (tieng mat tu mot moc den het).

Bai hoc 17/11/2026 (phong su "80 nam Van hoa soi duong"): bo tron tieng asplit + apad + sidechain bi ket,
tieng cam tu phut 2:30 den het ma tong do to van -14 LUFS nen kiem tong khong bat duoc; nguoi dung phat hien.
Chay sau moi lan tron tieng / xuat ban giao, TRUOC khi bao xong.

    python skills/bien-tap-video-thong-minh-song-ngu-tan/scripts/kiem_tieng_cam.py BAN_GIAO.mp4              # moi doan 5 s, cam neu < -45 dB
    python skills/bien-tap-video-thong-minh-song-ngu-tan/scripts/kiem_tieng_cam.py tieng.wav --doan 10 --nguong -50

Exit 0 = khong doan nao cam; 1 = co doan cam (in moc phut:giay).
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


def do_dai(f: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                       capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def muc_tb(f: Path, bd: float, dai: float) -> float:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-ss", f"{bd:.2f}", "-t", f"{dai:.2f}", "-i", str(f),
                        "-vn", "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True)
    m = re.search(r"mean_volume:\s*(-?[\d.]+|-inf) dB", r.stderr)
    return -120.0 if not m or m.group(1) == "-inf" else float(m.group(1))


def doan_cam(f: Path, doan: float = 5.0, nguong: float = -45.0, bo_cuoi: float = 1.0) -> list[float]:
    het = do_dai(f) - bo_cuoi
    cam, t = [], 0.0
    while t < het:
        if muc_tb(f, t, min(doan, het - t)) < nguong:
            cam.append(t)
        t += doan
    return cam


def main() -> int:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tep", type=Path)
    ap.add_argument("--doan", type=float, default=5.0, help="do dai moi doan do (giay)")
    ap.add_argument("--nguong", type=float, default=-45.0, help="duoi muc nay (dB trung binh) la cam")
    a = ap.parse_args()
    cam = doan_cam(a.tep, a.doan, a.nguong)
    if cam:
        print("CAM tai:", ", ".join(f"{int(t // 60)}:{int(t % 60):02d}" for t in cam))
        return 1
    print(f"PASS: khong doan {a.doan:g} s nao cam (nguong {a.nguong} dB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
