#!/usr/bin/env python3
"""Chep media vao public va tao input props cho composition AttNews."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ASSETS = ROOT / "public" / "assets"


class PrepareError(RuntimeError):
    pass


def _time_ms(value: str) -> int:
    match = re.fullmatch(r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})", value.strip())
    if not match:
        raise PrepareError(f"Moc SRT khong hop le: {value}")
    hours, minutes, seconds, millis = (int(part) for part in match.groups())
    return ((hours * 60 + minutes) * 60 + seconds) * 1000 + millis


def parse_srt(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    cues: list[dict] = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        timing_index = next((i for i, line in enumerate(lines) if "-->" in line), None)
        if timing_index is None:
            continue
        start_raw, end_raw = (part.strip() for part in lines[timing_index].split("-->", 1))
        start_ms = _time_ms(start_raw)
        end_ms = _time_ms(end_raw)
        if end_ms <= start_ms:
            raise PrepareError(f"Cue SRT co moc ket thuc khong lon hon moc dau: {block[:80]}")
        caption = "\n".join(lines[timing_index + 1 :]).strip()
        if caption:
            cues.append(
                {
                    "text": caption,
                    "startMs": start_ms,
                    "endMs": end_ms,
                    "timestampMs": start_ms,
                    "confidence": 1,
                }
            )
    return cues


def copy_asset(source: Path) -> str:
    if not source.is_file():
        raise PrepareError(f"Khong tim thay media: {source}")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()[:10]
    safe_name = re.sub(r"[^A-Za-z0-9._-]+", "-", source.name).strip("-")
    target = PUBLIC_ASSETS / f"{digest}-{safe_name}"
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        shutil.copy2(source, target)
    return target.relative_to(ROOT / "public").as_posix()


def probe_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise PrepareError(f"ffprobe khong doc duoc thoi luong {path}: {result.stderr.strip()}")
    try:
        duration = float(result.stdout.strip())
    except ValueError as exc:
        raise PrepareError(f"ffprobe tra ve thoi luong khong hop le cho {path}") from exc
    if duration <= 0:
        raise PrepareError(f"Media co thoi luong khong hop le: {path}")
    return duration


def build_props(args: argparse.Namespace) -> dict:
    if args.video and args.image:
        raise PrepareError("Chi chon mot trong --video hoac --image.")
    duration = args.duration
    duration_source = args.audio or args.video
    if duration is None:
        duration = probe_duration(duration_source) if duration_source else 8.0
    captions = parse_srt(args.captions) if args.captions else []
    return {
        "title": args.title,
        "subtitle": args.subtitle,
        "kicker": args.kicker,
        "durationSeconds": duration,
        "width": args.width,
        "height": args.height,
        "backgroundColor": args.background_color,
        "accentColor": args.accent_color,
        "backgroundImage": copy_asset(args.image) if args.image else None,
        "backgroundVideo": copy_asset(args.video) if args.video else None,
        "voiceover": copy_asset(args.audio) if args.audio else None,
        "captions": captions,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Tao props Remotion tu media/audio/SRT cua pipeline Tan.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--kicker", default="ATT NEWS")
    parser.add_argument("--video", type=Path)
    parser.add_argument("--image", type=Path)
    parser.add_argument("--audio", type=Path)
    parser.add_argument("--captions", type=Path, help="File SRT")
    parser.add_argument("--duration", type=float)
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--background-color", default="#031a3a")
    parser.add_argument("--accent-color", default="#e31b23")
    parser.add_argument("--output", type=Path, default=ROOT / "props" / "generated.json")
    args = parser.parse_args()
    try:
        props = build_props(args)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(props, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Da tao props: {args.output}")
        return 0
    except (PrepareError, OSError) as exc:
        print(f"LOI: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
