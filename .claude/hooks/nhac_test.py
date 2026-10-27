#!/usr/bin/env python3
"""Stop hook: nhac chay test khi luot nay da sua code ma chua kiem.

Doc transcript tu loi nhan gan nhat cua nguoi dung. Neu co Write/Edit vao
file code ma sau lan sua cuoi khong co lenh test/lint/build nao -> chan mot
lan (decision=block) de Claude chay test hoac ghi ro NOT RUN.

Lan thu hai (stop_hook_active) va moi loi doc transcript -> cho qua.
Xem rules/global.md (NO TEST = NO PASS).

--toan-cuc: lenh trong ~/.claude/settings.json. Dang o trong chinh repo nay
thi bo qua, vi .claude/settings.json cua repo da chay hook nay roi.
"""

import json
import os
import re
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

DUOI_CODE = {".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".css", ".html",
             ".sql", ".ps1", ".sh"}
CONG_CU_SUA = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
CONG_CU_LENH = {"Bash", "PowerShell"}
LENH_KIEM = re.compile(
    r"\b(unittest|pytest|vitest|jest|playwright|tsc|video_qa\.py)\b"
    r"|\b(npm|pnpm|yarn)\s+(run\s+)?(test|lint|typecheck|build)"
    r"|\b(flutter|cargo|go|dotnet)\s+test\b")
REPO = Path(__file__).resolve().parents[2]


def la_loi_nguoi_dung(entry: dict) -> bool:
    if entry.get("type") != "user" or entry.get("isMeta"):
        return False
    content = (entry.get("message") or {}).get("content")
    if isinstance(content, str):
        return True
    return isinstance(content, list) and not any(
        isinstance(b, dict) and b.get("type") == "tool_result" for b in content)


def file_chua_kiem(transcript: Path) -> list[str]:
    """File code da sua trong luot nay ma sau do chua co lenh kiem."""
    da_sua: list[str] = []
    for dong in transcript.read_text(encoding="utf-8").splitlines():
        if not dong.strip():
            continue
        entry = json.loads(dong)
        if entry.get("isSidechain"):
            continue
        if la_loi_nguoi_dung(entry):
            da_sua = []
            continue
        if entry.get("type") != "assistant":
            continue
        for block in (entry.get("message") or {}).get("content") or []:
            if not isinstance(block, dict) or block.get("type") != "tool_use":
                continue
            ten, vao = block.get("name"), block.get("input") or {}
            if ten in CONG_CU_SUA:
                duong_dan = str(vao.get("file_path") or vao.get("notebook_path") or "")
                if Path(duong_dan).suffix.lower() in DUOI_CODE and duong_dan not in da_sua:
                    da_sua.append(duong_dan)
            elif ten in CONG_CU_LENH and LENH_KIEM.search(str(vao.get("command") or "")):
                da_sua = []
    return da_sua


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    if payload.get("stop_hook_active"):
        return 0
    goc = Path(payload.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
    if "--toan-cuc" in sys.argv and goc.resolve().is_relative_to(REPO):
        return 0

    try:
        chua_kiem = file_chua_kiem(Path(payload.get("transcript_path") or ""))
    except (OSError, ValueError, AttributeError, TypeError):
        return 0
    if not chua_kiem:
        return 0

    ds = ", ".join(Path(p).name for p in chua_kiem[:5])
    if len(chua_kiem) > 5:
        ds += f" (+{len(chua_kiem) - 5} file)"
    print(json.dumps({
        "decision": "block",
        "reason": (
            f"Luot nay da sua code ({ds}) nhung chua chay test/lint/build nao sau lan sua cuoi. "
            "Hay chay lenh kiem tra cua du an roi bao PASS/FAIL; neu khong chay duoc thi "
            "ghi ro NOT RUN va ly do (rules/global.md: NO TEST = NO PASS)."
        ),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
