#!/usr/bin/env python3
"""Tạo mẫu WAV riêng tư và manifest đồng ý từ MP4 do chính chủ cung cấp."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import subprocess
from pathlib import Path


def run(command: list[str]) -> str:
    result = subprocess.run(command, check=True, text=True, capture_output=True)
    return result.stdout


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--consent-scope", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    if not args.input.is_file():
        parser.error(f"Không tìm thấy tệp: {args.input}")
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        parser.error("Cần cài FFmpeg và ffprobe")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    wav = args.output_dir / "reference.wav"
    probe = json.loads(run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,codec_name,sample_rate,channels",
        "-of", "json", str(args.input),
    ]))

    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-i", str(args.input), "-vn", "-ac", "1", "-ar", "48000",
        "-af", "highpass=f=70,lowpass=f=12000,afftdn=nf=-25,loudnorm=I=-18:TP=-2:LRA=7",
        "-c:a", "pcm_s16le", str(wav),
    ], check=True)

    manifest = {
        "schema_version": 1,
        "subject": args.subject,
        "self_attested": True,
        "consent_scope": args.consent_scope,
        "consent_recorded_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source": {"filename": args.input.name, "probe": probe},
        "reference_audio": "reference.wav",
        "provider_voice_profile_id": None,
        "requires_confirmation_per_script": True,
        "public_git_allowed": False,
    }
    (args.output_dir / "profile.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"wav": str(wav), "profile": str(args.output_dir / "profile.json")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
