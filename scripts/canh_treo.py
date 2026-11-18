#!/usr/bin/env python3
"""Chó canh lệnh treo: chạy một lệnh con, đứng yên quá lâu thì dừng và báo TREO.

Bài học 13/11/2026: lệnh ghép bản tin treo hơn 3 giờ (CPU ffmpeg đứng yên) mà không ai biết.
Cứ mỗi `--moi` giây (mặc định 30) kiểm thời gian CPU của tiến trình và kích thước file đầu ra (`--file`, nếu có).
Cả hai đều không nhúc nhích liên tục quá `--phut` phút (mặc định 3) → dừng cả cây tiến trình, in "TREO".

  python scripts/canh_treo.py --file RA.mp4 -- ffmpeg -i VAO.mp4 ... RA.mp4
  python scripts/canh_treo.py --phut 5 -- python -m tan_studio chay du-an.json

Lệnh bọc (python gọi ffmpeg bên trong) thì CPU của lệnh bọc đứng yên trong lúc ffmpeg chạy → luôn đưa `--file`.
Exit: mã thoát của lệnh con; 124 = TREO (đã dừng); 2 = lỗi đầu vào.
"""

import argparse
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

MA_TREO = 124

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def thoi_gian_cpu(proc):
    """Tổng giây CPU (user + kernel) tiến trình đã dùng; None nếu không đọc được."""
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes

        tao, thoat, nhan, nguoi_dung = (wintypes.FILETIME() for _ in range(4))
        ok = ctypes.windll.kernel32.GetProcessTimes(
            wintypes.HANDLE(int(proc._handle)),
            ctypes.byref(tao), ctypes.byref(thoat), ctypes.byref(nhan), ctypes.byref(nguoi_dung),
        )
        if not ok:
            return None
        doi = lambda ft: ((ft.dwHighDateTime << 32) | ft.dwLowDateTime) / 1e7  # noqa: E731
        return doi(nhan) + doi(nguoi_dung)
    try:
        truong = Path(f"/proc/{proc.pid}/stat").read_text().rsplit(")", 1)[1].split()
        return (int(truong[11]) + int(truong[12])) / os.sysconf("SC_CLK_TCK")
    except (OSError, IndexError, ValueError):
        return None


def kich_thuoc(duong_dan):
    try:
        return Path(duong_dan).stat().st_size if duong_dan else None
    except OSError:
        return None


def dung_ca_cay(proc):
    """Dừng tiến trình và mọi tiến trình con của nó (ffmpeg do lệnh bọc gọi)."""
    if os.name == "nt":
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True)
    else:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except OSError:
            proc.kill()
    proc.wait()


def canh(lenh, file_ra=None, nguong_giay=180.0, moi_giay=30.0, cpu_toi_thieu=None):
    """Chạy `lenh`, trả (mã thoát, có_treo). CPU tăng < cpu_toi_thieu giây trong một lần kiểm = đứng yên."""
    if cpu_toi_thieu is None:
        cpu_toi_thieu = 0.01 * moi_giay  # dưới 1 % một nhân
    kieu = {"start_new_session": True} if os.name != "nt" else {}
    proc = subprocess.Popen(lenh, **kieu)
    cpu_cu, co_cu = thoi_gian_cpu(proc), kich_thuoc(file_ra)
    dung_yen_tu = time.monotonic()
    while True:
        try:
            return proc.wait(timeout=moi_giay), False
        except subprocess.TimeoutExpired:
            pass
        cpu, co = thoi_gian_cpu(proc), kich_thuoc(file_ra)
        cpu_chay = cpu is not None and cpu_cu is not None and cpu - cpu_cu >= cpu_toi_thieu
        file_lon = co is not None and co != co_cu
        cpu_cu, co_cu = cpu, co
        bay_gio = time.monotonic()
        if cpu_chay or file_lon:
            dung_yen_tu = bay_gio
        elif bay_gio - dung_yen_tu >= nguong_giay:
            dung_ca_cay(proc)
            return MA_TREO, True


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--phut", type=float, default=3.0, help="đứng yên quá bấy nhiêu phút thì coi là treo (mặc định 3)")
    ap.add_argument("--moi", type=float, default=30.0, help="kiểm mỗi bấy nhiêu giây (mặc định 30)")
    ap.add_argument("--file", help="file đầu ra để theo dõi kích thước (nên có với ffmpeg / lệnh bọc)")
    ap.add_argument("lenh", nargs=argparse.REMAINDER, help="-- rồi lệnh cần chạy")
    a = ap.parse_args(argv)
    lenh = a.lenh[1:] if a.lenh[:1] == ["--"] else a.lenh
    if not lenh or a.phut <= 0 or a.moi <= 0:
        ap.print_usage(sys.stderr)
        print("Thiếu lệnh (đặt sau --) hoặc --phut/--moi không dương.", file=sys.stderr)
        return 2
    try:
        ma, treo = canh(lenh, a.file, nguong_giay=a.phut * 60, moi_giay=a.moi)
    except FileNotFoundError as e:
        print(f"Không chạy được lệnh: {e}", file=sys.stderr)
        return 2
    if treo:
        print(f"TREO: CPU và file đầu ra đứng yên quá {a.phut:g} phút — đã dừng lệnh: {' '.join(lenh)}", file=sys.stderr)
    return ma


if __name__ == "__main__":
    sys.exit(main())
