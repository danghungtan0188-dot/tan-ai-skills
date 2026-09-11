#!/usr/bin/env python3
"""Xuất phụ đề từ bilingual.json theo 4 chế độ.

    python export_subtitles.py bilingual.json --mode ass|srt-vi|srt-en|vtt|all --out-dir DIR [--stem TEN]

  ass     ASS song ngữ để đốt vào hình, EN trên VI dưới — mặc định bản tin ATT NEWS.
  srt-vi  SRT tiếng Việt rời (tên .vi_VN.srt — Facebook yêu cầu đúng dạng ten.ma_QUOCGIA.srt).
  srt-en  SRT tiếng Anh rời (.en_US.srt).
  vtt     WebVTT song ngữ 2 dòng cho web/YouTube.

SRT một thứ tiếng tự ngắt dòng dài hơn --max-chars thành 2 dòng ở khoảng trắng gần giữa.
Chạy check_subtitles.py trên file SRT/VTT vừa xuất trước khi giao.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_bilingual_ass import build_ass  # noqa: E402


def tc(t: float, sep: str) -> str:
    h, r = divmod(round(float(t) * 1000), 3_600_000)
    m, r = divmod(r, 60_000)
    s, ms = divmod(r, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def wrap(line: str, max_chars: int) -> list[str]:
    if len(line) <= max_chars or " " not in line:
        return [line]
    i = min((k for k, c in enumerate(line) if c == " "), key=lambda k: abs(k - len(line) // 2))
    return [line[:i].strip(), line[i + 1:].strip()]


def srt(segs: list[dict], key: str, max_chars: int = 42) -> str:
    return "\n".join(f"{n}\n{tc(s['start'], ',')} --> {tc(s['end'], ',')}\n"
                     + "\n".join(wrap(s[key], max_chars)) + "\n"
                     for n, s in enumerate(segs, 1))


def vtt(segs: list[dict]) -> str:
    return "WEBVTT\n\n" + "\n".join(f"{tc(s['start'], '.')} --> {tc(s['end'], '.')}\n{s['en']}\n{s['vi']}\n"
                                    for s in segs)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("--mode", choices=["ass", "srt-vi", "srt-en", "vtt", "all"], default="all")
    ap.add_argument("--out-dir", type=Path, default=Path("."))
    ap.add_argument("--stem", default="phu-de")
    ap.add_argument("--aspect", choices=["16:9", "9:16"], default="16:9")
    ap.add_argument("--max-chars", type=int, default=42)
    a = ap.parse_args()
    segs = json.loads(a.input.read_text(encoding="utf-8"))["segments"]
    a.out_dir.mkdir(parents=True, exist_ok=True)
    viec = {"ass": (f"{a.stem}.song-ngu.ass", lambda: build_ass(segs, a.aspect)),
            "srt-vi": (f"{a.stem}.vi_VN.srt", lambda: srt(segs, "vi", a.max_chars)),
            "srt-en": (f"{a.stem}.en_US.srt", lambda: srt(segs, "en", a.max_chars)),
            "vtt": (f"{a.stem}.song-ngu.vtt", lambda: vtt(segs))}
    for mode in (viec if a.mode == "all" else [a.mode]):
        ten, tao = viec[mode]
        (a.out_dir / ten).write_text(tao(), encoding="utf-8")
        print(a.out_dir / ten)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
