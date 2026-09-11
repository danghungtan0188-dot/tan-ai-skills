#!/usr/bin/env python3
"""Kiểm tra tự động file phụ đề SRT/VTT.

    python check_subtitles.py FILE.srt|FILE.vtt [--aspect 16:9|9:16] [--max-chars N]
                              [--max-cps 17] [--min-dur 0.8] [--song-ngu] [--strict]

LỖI (luôn exit 1): timecode sai định dạng/giá trị, bắt đầu >= kết thúc, cue rỗng, cue chồng lấn.
CẢNH BÁO (exit 1 khi --strict): cue quá ngắn, dòng quá dài, quá 2 dòng, tốc độ đọc quá nhanh.

--song-ngu: mỗi cue là 2 thứ tiếng, người xem đọc một thứ — tốc độ đọc tính theo dòng dài
nhất thay vì tổng số chữ.
"""
from __future__ import annotations
import argparse
import re
from pathlib import Path

TC = {"srt": re.compile(r"^(\d{2}):(\d{2}):(\d{2}),(\d{3})$"),
      "vtt": re.compile(r"^(?:(\d{2,}):)?(\d{2}):(\d{2})\.(\d{3})$")}
ARROW = re.compile(r"^\s*(\S+)\s+-->\s+(\S+)")
TAG = re.compile(r"<[^>]+>|\{[^}]*\}")


def to_sec(s: str, kind: str) -> float | None:
    m = TC[kind].match(s)
    if not m:
        return None
    h, mi, se, ms = (int(g) if g else 0 for g in m.groups())
    if mi > 59 or se > 59:
        return None
    return h * 3600 + mi * 60 + se + ms / 1000


def parse(text: str, kind: str) -> list[dict]:
    text = text.replace("﻿", "").replace("\r\n", "\n").strip()
    cues = []
    for block in re.split(r"\n\s*\n", text):
        lines = block.split("\n")
        if kind == "vtt" and lines[0].startswith(("WEBVTT", "NOTE", "STYLE", "REGION")):
            continue
        so = len(cues) + 1
        i = next((k for k, l in enumerate(lines) if "-->" in l), None)
        if i is None:
            cues.append({"so": so, "start": None, "end": None, "lines": [],
                         "loi": [f"không có dòng timecode: {lines[0][:40]}"]})
            continue
        m = ARROW.match(lines[i])
        a = to_sec(m.group(1), kind) if m else None
        e = to_sec(m.group(2), kind) if m else None
        cue = {"so": so, "start": a, "end": e, "loi": [],
               "lines": [TAG.sub("", l).strip() for l in lines[i + 1:] if TAG.sub("", l).strip()]}
        if a is None or e is None:
            cue["loi"].append(f"timecode sai: {lines[i].strip()}")
        cues.append(cue)
    return cues


def check(cues: list[dict], max_chars: int = 42, max_cps: float = 17.0,
          min_dur: float = 0.8, song_ngu: bool = False) -> tuple[list[str], list[str]]:
    loi, canh_bao, prev_end = [], [], None
    for c in cues:
        n = c["so"]
        loi += [f"cue {n}: {x}" for x in c["loi"]]
        if not c["lines"] and not c["loi"]:
            loi.append(f"cue {n}: cue rỗng")
        a, e = c["start"], c["end"]
        if a is None or e is None:
            continue
        if a >= e:
            loi.append(f"cue {n}: bắt đầu {a:.3f}s không nhỏ hơn kết thúc {e:.3f}s")
            continue
        if prev_end is not None and a < prev_end - 1e-3:
            loi.append(f"cue {n}: chồng lên cue trước {prev_end - a:.3f}s")
        prev_end = e if prev_end is None else max(prev_end, e)
        dur = e - a
        if dur < min_dur:
            canh_bao.append(f"cue {n}: quá ngắn {dur:.2f}s (< {min_dur}s)")
        if len(c["lines"]) > 2:
            canh_bao.append(f"cue {n}: {len(c['lines'])} dòng (> 2)")
        for l in c["lines"]:
            if len(l) > max_chars:
                canh_bao.append(f"cue {n}: dòng {len(l)} ký tự (> {max_chars}): {l[:40]}…")
        chu = max(map(len, c["lines"]), default=0) if song_ngu else sum(map(len, c["lines"]))
        if chu / dur > max_cps:
            canh_bao.append(f"cue {n}: đọc quá nhanh {chu / dur:.1f} ký tự/giây (> {max_cps})")
    return loi, canh_bao


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file", type=Path)
    ap.add_argument("--aspect", choices=["16:9", "9:16"], default="16:9")
    ap.add_argument("--max-chars", type=int, help="mặc định 42 (16:9), 30 (9:16)")
    ap.add_argument("--max-cps", type=float, default=17.0)
    ap.add_argument("--min-dur", type=float, default=0.8)
    ap.add_argument("--song-ngu", action="store_true")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    kind = a.file.suffix.lower().lstrip(".")
    if kind not in TC:
        raise SystemExit("Chỉ nhận .srt hoặc .vtt")
    cues = parse(a.file.read_text(encoding="utf-8"), kind)
    loi, canh_bao = check(cues, a.max_chars or (42 if a.aspect == "16:9" else 30),
                          a.max_cps, a.min_dur, a.song_ngu)
    for x in loi:
        print("LỖI      ", x)
    for x in canh_bao:
        print("CẢNH BÁO ", x)
    hong = bool(loi) or (a.strict and bool(canh_bao))
    print(f"{'FAIL' if hong else 'PASS'} — {len(cues)} cue, {len(loi)} lỗi, {len(canh_bao)} cảnh báo")
    return 1 if hong else 0


if __name__ == "__main__":
    raise SystemExit(main())
