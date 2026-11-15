#!/usr/bin/env python3
"""Vá một đoạn trong video đã giao: chỉ dựng lại đoạn giữa hai khung chìa khóa, phần còn lại giữ nguyên bằng -c copy.

Bản tin 13/11/2026 (v10): đổi một con số → dựng lại 13,7 s thay vì cả tin + bản cuối: ~5 phút thay vì ~35 phút,
số khung bằng đúng bản cũ. Cách làm:
  đoạn đầu  = bản gốc từ 0 tới khung chìa khóa K1, `-c copy -frames:v N` (`-to` lấy thừa khung chìa khóa của đoạn sau)
  đoạn giữa = bản dựng lại K1→K2, mã hoá lại cho khớp thông số bản gốc
  đoạn sau  = bản gốc từ khung chìa khóa K2, `-ss K2 -c copy`
  nối bằng concat demuxer, gắn dải tiếng (của bản gốc, hoặc dải tiếng làm lại `--tieng`), kiểm số khung bằng bản gốc.

  python scripts/va_doan_video.py GOC.mp4 --tu 150 --den 160 --chi-tim
      → in K1, K2 và số khung đoạn giữa phải dựng (dựng đúng khoảng K1→K2 của dòng thời gian bản gốc)
  python scripts/va_doan_video.py GOC.mp4 --tu 150 --den 160 --doan-giua GIUA.mp4 [--tieng TIENG.wav] --ra RA.mp4

Mỗi lệnh ffmpeg chỉ `-i` một file một lần; x264 `-preset faster`, 1 luồng, ưu tiên thấp (máy hay sập khi chạy nặng).
Exit 0 = xong và số khung khớp; 1 = số khung lệch; 2 = lỗi đầu vào.
"""

import argparse
import json
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def _chay(lenh):
    subprocess.run([str(x) for x in lenh], check=True)


def _probe(*tham_so):
    r = subprocess.run(["ffprobe", "-v", "error", *map(str, tham_so), "-of", "json"], capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def thong_so(p):
    s = _probe("-select_streams", "v:0", "-show_entries",
               "stream=codec_name,width,height,pix_fmt,r_frame_rate,time_base,start_time,profile", p)["streams"][0]
    s["fps"] = Fraction(s["r_frame_rate"])
    s["start_time"] = float(s.get("start_time") or 0)
    return s


def dem_khung(p):
    s = _probe("-select_streams", "v:0", "-count_packets", "-show_entries", "stream=nb_read_packets", p)["streams"][0]
    return int(s["nb_read_packets"])


def tim_khung_khoa(p, start=0.0):
    """Giây (tính từ đầu video) của mọi khung chìa khóa."""
    d = _probe("-select_streams", "v:0", "-skip_frame", "nokey", "-show_entries", "frame=pts_time", p)
    return sorted(float(f["pts_time"]) - start for f in d["frames"] if f.get("pts_time") not in (None, "N/A"))


def chon_cat(khoa, tu, den):
    """K1 = khung chìa khóa cuối cùng ≤ tu; K2 = khung chìa khóa đầu tiên ≥ den (None = tới hết video)."""
    if den <= tu:
        raise ValueError("--den phải lớn hơn --tu")
    truoc = [k for k in khoa if k <= tu + 1e-6]
    sau = [k for k in khoa if k >= den - 1e-6]
    if not truoc:
        raise ValueError(f"không có khung chìa khóa nào trước giây {tu}")
    return truoc[-1], (sau[0] if sau else None)


def _ha_uu_tien():
    if sys.platform == "win32":
        import ctypes

        ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x40)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Vá một đoạn trong video đã giao (cắt tại khung chìa khóa, phần còn lại -c copy).")
    ap.add_argument("goc", help="video đã giao (H.264)")
    ap.add_argument("--tu", type=float, required=True, help="giây bắt đầu chỗ cần sửa")
    ap.add_argument("--den", type=float, required=True, help="giây kết thúc chỗ cần sửa")
    ap.add_argument("--chi-tim", action="store_true", help="chỉ in K1, K2 và số khung đoạn giữa")
    ap.add_argument("--doan-giua", help="video đoạn giữa đã dựng lại, phủ đúng K1→K2")
    ap.add_argument("--tieng", help="dải tiếng làm lại cho cả video (mặc định: giữ tiếng bản gốc)")
    ap.add_argument("--ra", help="file kết quả (không được trùng bản gốc)")
    args = ap.parse_args(argv)

    goc = Path(args.goc).resolve()
    try:
        ts = thong_so(goc)
        if ts["codec_name"] != "h264":
            raise ValueError(f"bản gốc là {ts['codec_name']}, script chỉ vá H.264")
        k1, k2 = chon_cat(tim_khung_khoa(goc, ts["start_time"]), args.tu, args.den)
    except (ValueError, subprocess.CalledProcessError, KeyError, IndexError) as e:
        print(f"LOI: {e}", file=sys.stderr)
        return 2
    fps = ts["fps"]
    tong = dem_khung(goc)
    n1 = round(k1 * fps)
    n2 = (round(k2 * fps) if k2 is not None else tong) - n1
    print(f"K1 = {k1:.3f} s (khung {n1}), K2 = {'hết video' if k2 is None else f'{k2:.3f} s'}; "
          f"đoạn giữa {n2} khung = {float(n2 / fps):.3f} s; bản gốc {tong} khung", flush=True)
    if args.chi_tim:
        return 0
    if not args.doan_giua or not args.ra:
        print("LOI: cần --doan-giua và --ra (hoặc dùng --chi-tim)", file=sys.stderr)
        return 2
    ra = Path(args.ra).resolve()
    if ra == goc:
        print("LOI: không ghi đè bản gốc — chọn --ra khác", file=sys.stderr)
        return 2
    giua = Path(args.doan_giua).resolve()
    if dem_khung(giua) < n2:
        print(f"LOI: đoạn giữa chỉ có {dem_khung(giua)} khung, cần {n2}", file=sys.stderr)
        return 2

    _ha_uu_tien()
    tb = Fraction(ts["time_base"]).denominator
    ffmpeg = ["ffmpeg", "-v", "error", "-y", "-threads", "1"]
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        phan = []
        if n1 > 0:
            phan.append(tmp / "a.mp4")
            _chay([*ffmpeg, "-i", goc, "-map", "0:v:0", "-c", "copy", "-frames:v", n1, phan[-1]])
        phan.append(tmp / "b.mp4")
        _chay([*ffmpeg, "-i", giua, "-map", "0:v:0", "-frames:v", n2,
               "-vf", f"scale={ts['width']}:{ts['height']},fps={fps},setsar=1",
               "-c:v", "libx264", "-preset", "faster", "-crf", "18", "-x264-params", "threads=1",
               "-pix_fmt", ts["pix_fmt"], "-video_track_timescale", tb, phan[-1]])
        if k2 is not None:
            phan.append(tmp / "c.mp4")
            _chay([*ffmpeg, "-ss", f"{k2:.6f}", "-i", goc, "-map", "0:v:0", "-c", "copy", phan[-1]])
        ds = tmp / "ds.txt"
        ds.write_text("".join(f"file '{p.as_posix()}'\n" for p in phan), encoding="utf-8")
        hinh = tmp / "hinh.mp4"
        _chay([*ffmpeg, "-f", "concat", "-safe", "0", "-i", ds, "-c", "copy", hinh])
        tieng = Path(args.tieng).resolve() if args.tieng else goc
        ma_tieng = ["-c:a", "aac", "-b:a", "192k", "-ar", "48000"] if args.tieng else ["-c:a", "copy"]
        _chay([*ffmpeg, "-i", hinh, "-i", tieng, "-map", "0:v:0", "-map", "1:a:0?", "-c:v", "copy", *ma_tieng,
               "-t", f"{float(tong / fps):.6f}", "-movflags", "+faststart", ra])

    moi = dem_khung(ra)
    print(f"{ra.name}: {moi} khung (bản gốc {tong})", flush=True)
    if moi != tong:
        print("LOI: số khung lệch bản gốc — kiểm lại đoạn giữa", file=sys.stderr)
        return 1
    print("Xong. Chạy tiếp: python scripts/video_qa.py", ra, "--strict --audio")
    return 0


if __name__ == "__main__":
    sys.exit(main())
