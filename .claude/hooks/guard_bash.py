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
import posixpath
import re
import shlex
import sys

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

# Dich xoa de quy nguy hiem: o dia, home, thu muc ho so nguoi dung,
# thu muc hien tai / cha, ky tu dai dien.
_NGUY_HIEM = (r"[A-Za-z]:[/\\]?|[A-Za-z]:[/\\]Users([/\\][^/\\\s\"']+)?[/\\]?"
              r"|~[/\\]?|\$HOME|\$env:USERPROFILE|\.{1,2}([/\\]\*?)?|\*")

DENY = [
    (re.compile(r"\brm\s+-[a-zA-Z]*[rR][a-zA-Z]*\s+(-[a-zA-Z]+\s+)*"
                r"(/|~|\*|\$HOME|[A-Za-z]:[/\\]|\.{1,2}/?\*?)\s*($|;|&)"),
     "Xoa de quy thu muc goc / home / thu muc hien tai"),
    (re.compile(r"\bRemove-Item\b(?=[^\n;|]*-Recurse)[^\n;|]*?\s[\"']?(" + _NGUY_HIEM
                + r")[\"']?(?=\s|$|;|\|)", re.I),
     "Remove-Item -Recurse vao o dia / home / thu muc hien tai"),
    (re.compile(r"(^|[;&|]\s*|\bcmd\s+/c\s+)(del|erase|rd|rmdir)\s[^\n;&|]*/s\b", re.I),
     "Xoa de quy kieu cmd (del /s, rd /s)"),
    (re.compile(r"(^|[;&|]\s*)format(\.com)?\s+[A-Za-z]:|\bFormat-Volume\b", re.I),
     "Format o dia"),
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
    (re.compile(r"\bgit\s+push\b[^\n]*(--force(?!-with-lease)|\s-[a-zA-Z]*f\b)", re.I),
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
    (re.compile(r"\bgit\s+add\s+([^\n;&|]*\s)?(-A|--all|\.)(?=\s|$|;|&)"),
     "git add tat ca (de lo file cua phien khac; nen add tung duong dan)"),
    (re.compile(r"\bgit\s+commit\s+([^\n;&|]*\s)?-[b-zA-Z]*a[a-zA-Z]*(?=\s|$)"),
     "git commit -a (de lo file cua phien khac; nen add tung duong dan)"),
]

_LENH_CO_LOI_NHAN = re.compile(r"\bgit\s+commit\b|\bgh\s+(pr|issue|release)\s+create\b")
_THAM_SO_LOI_NHAN = re.compile(
    r"(?<=\s)(-m|--message|--title|--body|--notes)(=|\s+)(\"(\\.|[^\"\\])*\"|'[^']*')")
_HEREDOC = re.compile(r"<<-?\s*(['\"]?)(\w+)\1")


def bo_loi_nhan(command: str) -> str:
    """Bo noi dung loi nhan commit/PR (chi la chu, khong chay) truoc khi so khop."""
    if not _LENH_CO_LOI_NHAN.search(command):
        return command
    ket_qua, dong_ket = [], None
    for dong in command.split("\n"):
        if dong_ket is not None:
            if dong.strip() == dong_ket:
                dong_ket = None
                ket_qua.append(dong)
            continue
        heredoc = _HEREDOC.search(dong)
        if heredoc and _LENH_CO_LOI_NHAN.search(dong):
            dong_ket = heredoc.group(2)
        ket_qua.append(_THAM_SO_LOI_NHAN.sub(r'\1\2""', dong)
                       if _LENH_CO_LOI_NHAN.search(dong) else dong)
    return "\n".join(ket_qua)


_SHELL_C = re.compile(r"\b(?:bash|sh|zsh|pwsh|powershell)(?:\.exe)?\b(?:\s+-\w+)*?\s+-(?:c|Command)\s+"
                      r"(?:\"((?:\\.|[^\"\\])*)\"|'([^']*)')", re.I)
_CMD_C = re.compile(r"\bcmd(?:\.exe)?\s+/c\s+(?:\"([^\"]*)\"|([^\n]+))", re.I)
_HEREDOC_SHELL = re.compile(r"\b(?:bash|sh|zsh|pwsh)\b[^\n]*<<-?\s*(['\"]?)(\w+)\1")


def lenh_long(command: str) -> list[str]:
    """Lenh nam trong bash -c "...", powershell -Command "...", cmd /c, heredoc dua vao shell."""
    ket_qua = [m.group(1) if m.group(1) is not None else m.group(2)
               for m in _SHELL_C.finditer(command)]
    ket_qua += [m.group(1) if m.group(1) is not None else m.group(2)
                for m in _CMD_C.finditer(command)]
    dong_ket = None
    for dong in command.split("\n"):
        if dong_ket is not None:
            if dong.strip() == dong_ket:
                dong_ket = None
            else:
                ket_qua.append(dong)
            continue
        heredoc = _HEREDOC_SHELL.search(dong)
        if heredoc:
            dong_ket = heredoc.group(2)
    return ket_qua


MEDIA_EXT = (".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v",
             ".mp3", ".wav", ".m4a", ".aac")


def ffmpeg_ghi_de_nguon(command: str) -> str | None:
    """Tra ve file bi ghi de neu mot lenh ffmpeg xuat ra chinh file dau vao."""
    for doan in re.split(r"&&|\|\||[;|\n]", command):
        if not re.search(r"\bffmpeg\b", doan):
            continue
        try:
            tokens = shlex.split(doan, posix=False)
        except ValueError:
            tokens = doan.split()
        vao, ra, sau_i = set(), [], False
        for token in tokens:
            if token == "-i":
                sau_i = True
                continue
            ten = posixpath.normpath(token.strip("\"'").replace("\\", "/")).lower()
            if sau_i:
                vao.add(ten)
                sau_i = False
            elif ten.endswith(MEDIA_EXT):
                ra.append(ten)
        for ten in ra:
            if ten in vao:
                return ten
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    command = (payload.get("tool_input") or {}).get("command")
    if not isinstance(command, str) or not command.strip():
        return 0
    command = bo_loi_nhan(command)
    ung_vien = [command, *lenh_long(command)]

    for pattern, label in DENY:
        if any(pattern.search(lenh) for lenh in ung_vien):
            print(
                f"CHAN BOI HOOK guard_bash (rules/security.md): {label}.\n"
                "Lenh nay pha du lieu hoac vo hieu hoa bao mat. "
                "Neu that su can, hay de nguoi dung tu chay thu cong.",
                file=sys.stderr,
            )
            return 2

    bi_de = next(filter(None, map(ffmpeg_ghi_de_nguon, ung_vien)), None)
    if bi_de:
        print(
            f"CHAN BOI HOOK guard_bash (rules/video.md): ffmpeg ghi de file goc {bi_de}.\n"
            "Khong ghi de video goc; xuat ra file moi ten khac.",
            file=sys.stderr,
        )
        return 2

    for pattern, label in ASK:
        if any(pattern.search(lenh) for lenh in ung_vien):
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
