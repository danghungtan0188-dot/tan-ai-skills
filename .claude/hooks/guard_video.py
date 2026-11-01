#!/usr/bin/env python3
"""PreToolUse hook: bai hoc dung video bien thanh chot chan cho lenh ffmpeg.

Chan (exit 2) khi:
  - loudnorm mot luot khong linear=true -> bop dai dong, giong "vo tieng"
    (luot do co print_format + -f null thi cho qua).
  - nen libx264/libx265 thieu -preset hoac preset cham hon "faster" -> nong may.
  - dang co ffmpeg.exe khac chay -> may hay sap khi chay hai viec nang.

Bien TAN_HOOK_GIA_LAP_FFMPEG=<so> thay cho tasklist, chi dung trong test.
Xem rules/video.md va docs/bai-hoc-va-chot-chan.md.
"""

import json
import os
import re
import shlex
import subprocess
import sys

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

PRESET_NHANH = {"ultrafast", "superfast", "veryfast", "faster"}
_NEN_X26X = re.compile(r"(?:^|\s)-(?:c:v|vcodec|codec:v|c)(?::\d+)?\s+lib(?:x264|x265)\b")
_PRESET = re.compile(r"(?:^|\s)-preset(?::v)?\s+(\S+)")


def doan_ffmpeg(command: str) -> list[str]:
    """Cac doan lenh ma chuong trinh chay chinh la ffmpeg."""
    ket_qua = []
    for doan in re.split(r"&&|\|\||[;|\n]", command):
        try:
            tokens = shlex.split(doan, posix=False)
        except ValueError:
            tokens = doan.split()
        if tokens and re.split(r"[/\\]", tokens[0].strip("\"'"))[-1].lower() in ("ffmpeg", "ffmpeg.exe"):
            ket_qua.append(doan)
    return ket_qua


def so_ffmpeg_dang_chay() -> int:
    gia_lap = os.environ.get("TAN_HOOK_GIA_LAP_FFMPEG")
    if gia_lap is not None:
        return int(gia_lap or 0)
    try:
        out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq ffmpeg.exe", "/NH", "/FO", "CSV"],
                             capture_output=True, text=True, timeout=5).stdout
    except (OSError, subprocess.SubprocessError):
        return 0
    return sum(1 for dong in out.splitlines() if dong.lower().startswith('"ffmpeg.exe"'))


def ly_do_chan(doan: str) -> str | None:
    if "loudnorm" in doan and "linear=true" not in doan and not (
            "print_format" in doan and re.search(r"-f\s+null\b", doan)):
        return ("loudnorm mot luot se bop dai dong (LRA). Do luot 1 voi print_format=json -f null -, "
                "roi luot 2 truyen measured_* va linear=true; hoac gain tinh + alimiter ghim 1-3 dB.")
    if _NEN_X26X.search(doan):
        preset = _PRESET.search(doan)
        if not preset or preset.group(1).strip("\"'").lower() not in PRESET_NHANH:
            return ("nen x264/x265 phai co -preset faster (hoac nhanh hon) de khong lam nong may; "
                    "bu chat luong bang -crf 20. Can preset cham hon thi de nguoi dung tu chay.")
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    command = (payload.get("tool_input") or {}).get("command")
    if not isinstance(command, str):
        return 0
    cac_doan = doan_ffmpeg(command)
    if not cac_doan:
        return 0

    ly_do = next(filter(None, map(ly_do_chan, cac_doan)), None)
    if ly_do is None and so_ffmpeg_dang_chay() > 0:
        ly_do = ("dang co ffmpeg khac chay; may hay sap khi chay hai viec nang cung luc. "
                 "Cho viec truoc xong (hoac kiem tra tien trinh ffmpeg treo) roi moi chay.")
    if ly_do:
        print(f"CHAN BOI HOOK guard_video (rules/video.md): {ly_do}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
