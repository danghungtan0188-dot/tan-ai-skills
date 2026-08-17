#!/usr/bin/env python3
"""Tu kiem tra file video da xuat bang ffprobe (Buoc H trong SKILL.md).

Doi chieu do phan giai, thoi luong va su ton tai cua audio/video track
voi ke hoach da duyet. Khong tu sua video — chi bao PASS/FAIL ro rang
de quyet dinh co can lap lai buoc nao trong pipeline hay khong.

Yeu cau: ffprobe phai co san tren PATH (di kem cai dat ffmpeg, von la
yeu cau co san cua skill video-use).

Vi du:
    python kiem_tra_dau_ra.py SP001_tiktok.mp4 --do-phan-giai 1080x1920 \
        --thoi-luong-toi-thieu 12 --thoi-luong-toi-da 40
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Tu kiem tra do phan giai/thoi luong/audio track cua video da xuat."
    )
    parser.add_argument("video", type=Path, help="Duong dan file video can kiem tra.")
    parser.add_argument("--do-phan-giai", help="Do phan giai ky vong, dang WxH (vd. 1080x1920).")
    parser.add_argument("--thoi-luong-toi-thieu", type=float, default=None, help="Giay, thoi luong toi thieu chap nhan duoc.")
    parser.add_argument("--thoi-luong-toi-da", type=float, default=None, help="Giay, thoi luong toi da chap nhan duoc.")
    return parser


def run_ffprobe(video: Path) -> dict:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "stream=codec_type,width,height",
        "-show_entries", "format=duration",
        "-of", "json",
        str(video),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe loi: {result.stderr.strip()}")
    return json.loads(result.stdout)


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.video.exists():
        print(f"Loi: khong tim thay file {args.video}", file=sys.stderr)
        return 2

    if shutil.which("ffprobe") is None:
        print(
            "Loi: khong tim thay ffprobe tren PATH. Khong the tu kiem tra — "
            "bao cho nguoi dung thay vi bo qua buoc nay.",
            file=sys.stderr,
        )
        return 2

    try:
        info = run_ffprobe(args.video)
    except RuntimeError as exc:
        print(f"Loi: {exc}", file=sys.stderr)
        return 2

    streams = info.get("streams", [])
    has_video = any(s.get("codec_type") == "video" for s in streams)
    has_audio = any(s.get("codec_type") == "audio" for s in streams)
    video_stream = next((s for s in streams if s.get("codec_type") == "video"), {})
    duration = float(info.get("format", {}).get("duration", 0) or 0)
    width = video_stream.get("width")
    height = video_stream.get("height")

    checks = []

    checks.append(("Co video track", has_video))
    checks.append(("Co audio track", has_audio))

    if args.do_phan_giai:
        try:
            exp_w, exp_h = (int(v) for v in args.do_phan_giai.lower().split("x"))
        except ValueError:
            print(f"Loi: --do-phan-giai phai dang WxH, nhan duoc '{args.do_phan_giai}'", file=sys.stderr)
            return 2
        checks.append((
            f"Do phan giai = {exp_w}x{exp_h} (thuc te: {width}x{height})",
            width == exp_w and height == exp_h,
        ))

    if args.thoi_luong_toi_thieu is not None:
        checks.append((
            f"Thoi luong >= {args.thoi_luong_toi_thieu}s (thuc te: {duration:.1f}s)",
            duration >= args.thoi_luong_toi_thieu,
        ))

    if args.thoi_luong_toi_da is not None:
        checks.append((
            f"Thoi luong <= {args.thoi_luong_toi_da}s (thuc te: {duration:.1f}s)",
            duration <= args.thoi_luong_toi_da,
        ))

    print(f"Kiem tra: {args.video}")
    all_pass = True
    for label, passed in checks:
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_pass = False
        print(f"  [{status}] {label}")

    print()
    print("KET QUA: " + ("PASS — co the giao video." if all_pass else "FAIL — sua roi render lai, xem chi tiet o tren."))

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
