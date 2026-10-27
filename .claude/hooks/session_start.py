#!/usr/bin/env python3
"""SessionStart hook: nap phan dau PROGRESS.md cua du an vao ngu canh.

Tim PROGRESS.md o goc du an, khong co thi docs/PROGRESS.md.
Khong co file nao -> im lang. Moi loi -> exit 0 (khong bao gio chan phien).

--toan-cuc: lenh trong ~/.claude/settings.json. Dang o trong chinh repo nay
thi bo qua, vi .claude/settings.json cua repo da chay hook nay roi.
"""

import json
import os
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

GIOI_HAN = 4000
REPO = Path(__file__).resolve().parents[2]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        payload = {}

    goc = Path(payload.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
    if "--toan-cuc" in sys.argv and goc.resolve().is_relative_to(REPO):
        return 0
    for ung_vien in (goc / "PROGRESS.md", goc / "docs" / "PROGRESS.md"):
        if ung_vien.is_file():
            break
    else:
        return 0

    try:
        noi_dung = ung_vien.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0
    if len(noi_dung) > GIOI_HAN:
        noi_dung = noi_dung[:GIOI_HAN] + "\n...(da cat bot; doc file de xem day du)"

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": (
                f"Tien do du an (tu dong nap tu {ung_vien.relative_to(goc).as_posix()}):\n\n"
                + noi_dung
            ),
        }
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
