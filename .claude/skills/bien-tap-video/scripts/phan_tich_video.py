#!/usr/bin/env python3
"""Phan tich nhanh 1 file video: metadata (ffprobe) + anh contact sheet
cac khung hinh trich dinh ky (ffmpeg) - giup nhan dien chu de va cach dung
ma khong can xem toan bo video theo thoi gian thuc.

Yeu cau: ffmpeg va ffprobe co san tren PATH.

Cach dung:
    python phan_tich_video.py duong/dan/video.mp4
    python phan_tich_video.py duong/dan/video.mp4 --out thu_muc_output --frames 36
"""

import argparse
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def check_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise RuntimeError(
            f"Không tìm thấy '{name}' trên PATH. Cài ffmpeg trước "
            "(ví dụ: winget install Gyan.FFmpeg)."
        )


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Lệnh thất bại: {' '.join(cmd)}\n{result.stderr}")
    return result.stdout


def get_raw_metadata(video_path: Path) -> dict:
    check_tool("ffprobe")
    out = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(video_path),
        ]
    )
    return json.loads(out)


def summarize(meta: dict) -> dict:
    fmt = meta.get("format", {})
    duration = float(fmt.get("duration", 0) or 0)
    video_stream = next(
        (s for s in meta.get("streams", []) if s.get("codec_type") == "video"), {}
    )
    audio_stream = next(
        (s for s in meta.get("streams", []) if s.get("codec_type") == "audio"), {}
    )
    return {
        "duration_sec": round(duration, 1),
        "size_mb": round(int(fmt.get("size", 0) or 0) / (1024 * 1024), 1),
        "width": video_stream.get("width"),
        "height": video_stream.get("height"),
        "orientation": (
            "ngang"
            if (video_stream.get("width") or 0) >= (video_stream.get("height") or 0)
            else "dọc"
        ),
        "video_codec": video_stream.get("codec_name"),
        "fps": video_stream.get("avg_frame_rate"),
        "audio_codec": audio_stream.get("codec_name"),
        "has_audio": bool(audio_stream),
    }


def make_contact_sheet(
    video_path: Path, out_path: Path, duration: float, target_frames: int
) -> dict:
    check_tool("ffmpeg")
    target_frames = max(6, min(target_frames, 48))
    duration = max(duration, 1.0)
    interval = max(1.0, duration / target_frames)
    cols = max(1, math.ceil(math.sqrt(target_frames * 16 / 9)))
    rows = max(1, math.ceil(target_frames / cols))
    vf = f"fps=1/{interval:.3f},scale=320:-1,tile={cols}x{rows}"
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video_path),
            "-vf",
            vf,
            "-frames:v",
            "1",
            "-update",
            "1",
            str(out_path),
        ]
    )
    return {
        "interval_sec": round(interval, 1),
        "cols": cols,
        "rows": rows,
        "max_frames": cols * rows,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Phân tích video: metadata + contact sheet khung hình để nhận diện chủ đề/cách dựng."
    )
    parser.add_argument("video", help="Đường dẫn file video cần phân tích")
    parser.add_argument(
        "--out",
        default=None,
        help="Thư mục lưu kết quả (mặc định: cùng thư mục với video)",
    )
    parser.add_argument(
        "--frames",
        type=int,
        default=30,
        help="Số khung hình mục tiêu trong contact sheet (6-48, mặc định 30)",
    )
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    video_path = Path(args.video).resolve()
    if not video_path.exists():
        print(f"Lỗi: không tìm thấy file {video_path}", file=sys.stderr)
        return 2

    out_dir = Path(args.out).resolve() if args.out else video_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        raw_meta = get_raw_metadata(video_path)
    except RuntimeError as exc:
        print(f"Lỗi: {exc}", file=sys.stderr)
        return 2

    summary = summarize(raw_meta)
    contact_sheet_path = out_dir / f"{video_path.stem}_contact_sheet.png"

    sheet_info = None
    try:
        sheet_info = make_contact_sheet(
            video_path, contact_sheet_path, summary["duration_sec"], args.frames
        )
    except RuntimeError as exc:
        print(f"Lỗi khi tạo contact sheet: {exc}", file=sys.stderr)

    report = {
        "video": str(video_path),
        "metadata": summary,
        "contact_sheet": str(contact_sheet_path) if sheet_info else None,
        "contact_sheet_info": sheet_info,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
