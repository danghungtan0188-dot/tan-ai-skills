#!/usr/bin/env python3
"""PreToolUse hook: dich vu tra phi (HeyGen) phai hoi nguoi dung tung lan.

Hoi (permissionDecision=ask) khi:
  - goi cong cu MCP heygen (mcp__heygen__*),
  - goi skill heygen-* qua cong cu Skill,
  - lenh Bash/PowerShell goi api.heygen.com hoac CLI heygen.
Moi truong hop khac -> cho qua. Xem docs/bai-hoc-va-chot-chan.md.
"""

import json
import re
import sys

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

_LENH_HEYGEN = re.compile(r"api\.heygen\.com|(^|[;&|(]\s*|\n\s*)heygen(\.exe)?\s", re.I)


def dich_vu(tool_name: str, tool_input: dict) -> str | None:
    if tool_name.lower().startswith("mcp__heygen"):
        return f"cong cu {tool_name}"
    if tool_name == "Skill" and "heygen" in str(tool_input.get("skill", "")).lower():
        return f"skill {tool_input.get('skill')}"
    if tool_name in ("Bash", "PowerShell") and _LENH_HEYGEN.search(str(tool_input.get("command", ""))):
        return "lenh goi HeyGen"
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    ten = dich_vu(str(payload.get("tool_name") or ""), payload.get("tool_input") or {})
    if ten:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": (
                    f"Dich vu tra phi HeyGen ({ten}) ton credit cua nguoi dung; "
                    "chi chay khi nguoi dung dong y lan nay."
                ),
            }
        }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
