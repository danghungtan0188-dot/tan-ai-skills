#!/usr/bin/env python3
"""PreToolUse hook: kiem soat lenh Bash nguy hiem.

Hai muc do:
  DENY  -> exit 2, chan han (pha du lieu, tat bao mat, chay code tai ve).
  ASK   -> tra JSON permissionDecision=ask, de nguoi dung tu quyet
           (thao tac huong ra ngoai: push, deploy, publish).

Exit 0 = cho phep.

Xem rules/security.md.
"""

import json
import re
import sys

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

DENY = [
    (re.compile(r"\brm\s+-[a-zA-Z]*[rR][a-zA-Z]*\s+(-[a-zA-Z]+\s+)*"
                r"(/|~|\*|\$HOME|[A-Za-z]:[/\\])\s*($|;|&)"),
     "Xoa de quy thu muc goc / home"),
    (re.compile(r"\bDROP\s+(DATABASE|SCHEMA)\b", re.I), "DROP DATABASE/SCHEMA"),
    (re.compile(r"\bTRUNCATE\s+TABLE\b", re.I), "TRUNCATE TABLE"),
    (re.compile(r"\bDELETE\s+FROM\s+[A-Za-z0-9_.\"]+\s*(;|$)", re.I),
     "DELETE FROM khong co WHERE"),
    (re.compile(r"\bDISABLE\s+ROW\s+LEVEL\s+SECURITY\b", re.I),
     "Tat Row Level Security"),
    (re.compile(r"\bsupabase\s+db\s+reset\b", re.I), "Reset database Supabase"),
    (re.compile(r"\b(curl|wget|iwr|Invoke-WebRequest)\b[^|]*\|\s*"
                r"(sudo\s+)?(ba)?sh\b", re.I), "Tai ve va chay script tu Internet"),
    (re.compile(r"\bInvoke-Expression\b|\biex\b\s*\(", re.I),
     "Thuc thi chuoi tai ve bang Invoke-Expression"),
    (re.compile(r"\bgit\s+push\b[^\n]*--force(?!-with-lease)", re.I),
     "git push --force (ghi de lich su tren remote)"),
]

ASK = [
    (re.compile(r"\bgit\s+push\b", re.I), "day code len remote GitHub"),
    (re.compile(r"\bgh\s+(pr|release)\s+create\b", re.I), "tao PR / release tren GitHub"),
    (re.compile(r"\bnpm\s+publish\b|\byarn\s+publish\b|\bpnpm\s+publish\b", re.I),
     "publish package len registry"),
    (re.compile(r"\bvercel\b[^\n]*--prod|\bnetlify\s+deploy\b[^\n]*--prod|"
                r"\bfirebase\s+deploy\b|\bwrangler\s+(publish|deploy)\b", re.I),
     "deploy len production"),
    (re.compile(r"\bdocker\s+push\b", re.I), "day image len registry"),
    (re.compile(r"\bsupabase\s+(db\s+push|link|functions\s+deploy)\b", re.I),
     "thay doi du an Supabase tu xa"),
    (re.compile(r"\bgit\s+reset\s+--hard\b", re.I),
     "git reset --hard (mat thay doi chua commit)"),
    (re.compile(r"\bgit\s+clean\s+-[a-zA-Z]*[fd]", re.I),
     "git clean (xoa file chua tracked)"),
]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    command = (payload.get("tool_input") or {}).get("command")
    if not isinstance(command, str) or not command.strip():
        return 0

    for pattern, label in DENY:
        if pattern.search(command):
            print(
                f"CHAN BOI HOOK guard_bash (rules/security.md): {label}.\n"
                "Lenh nay pha du lieu hoac vo hieu hoa bao mat. "
                "Neu that su can, hay de nguoi dung tu chay thu cong.",
                file=sys.stderr,
            )
            return 2

    for pattern, label in ASK:
        if pattern.search(command):
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "ask",
                    "permissionDecisionReason": (
                        f"Thao tac huong ra ngoai: {label}. "
                        "rules/security.md yeu cau nguoi dung xac nhan truoc."
                    ),
                }
            }, ensure_ascii=False))
            return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
