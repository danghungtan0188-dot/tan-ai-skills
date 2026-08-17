#!/usr/bin/env python3
"""PostToolUse hook: sau moi lenh ffmpeg, tu kiem tra file vua render.

Day la kiem tra nhanh (lenient) — chi bao FAIL khi file that su hong.
Kiem tra day du chay o /review-video qua scripts/video_qa.py --strict.

Exit 0 = khong co van de (hoac khong lien quan).
Exit 2 = file render hong, stderr tra ve cho Claude de tu sua.

Xem rules/video.md.
"""

import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

MEDIA_EXT = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v",
             ".mp3", ".wav", ".m4a", ".aac"}
QA_SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "video_qa.py"


def output_files(command: str) -> list[Path]:
    """Doan file dau ra cua lenh ffmpeg: token media khong dung sau -i."""
    try:
        tokens = shlex.split(command, posix=False)
    except ValueError:
        tokens = command.split()
    outputs, skip_next = [], False
    for index, raw in enumerate(tokens):
        if skip_next:
            skip_next = False
            continue
        if raw == "-i":
            skip_next = True
            continue
        token = raw.strip("\"'")
        if Path(token).suffix.lower() in MEDIA_EXT and index > 0:
            outputs.append(Path(token))
    return outputs


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    command = (payload.get("tool_input") or {}).get("command", "")
    if not isinstance(command, str) or not re.search(r"\bffmpeg\b", command):
        return 0
    if not QA_SCRIPT.exists():
        return 0

    failures, summaries = [], []
    for target in output_files(command):
        if not target.exists():
            continue
        result = subprocess.run(
            [sys.executable, str(QA_SCRIPT), str(target), "--quiet"],
            text=True, capture_output=True, encoding="utf-8", errors="replace",
        )
        line = result.stdout.strip()
        if result.returncode == 1:
            failures.append(line)
        elif line:
            summaries.append(line)

    if failures:
        print("HOOK check_render — file render KHONG dat (rules/video.md):",
              file=sys.stderr)
        for item in failures:
            print(item, file=sys.stderr)
        print("Sua lenh ffmpeg roi render lai truoc khi bao hoan tat.",
              file=sys.stderr)
        return 2

    for item in summaries:
        print(f"[check_render] {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
