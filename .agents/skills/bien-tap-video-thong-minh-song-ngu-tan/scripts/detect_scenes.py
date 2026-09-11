#!/usr/bin/env python3
"""Dò mốc cắt cảnh, ghi scenes.json cho banner và logo dùng chung.

    python detect_scenes.py INPUT --out scenes.json [--threshold 0.12]

`studio_end` = mốc cắt đầu tiên — với bản tin ATT NEWS đó là lúc hết cảnh MC trường quay
(video 06: 30,4 s; sk2: 26,3 s). Đừng ghi cứng mốc này: mỗi video một khác.
Xem một khung ngay trước và sau mốc để chắc chắn trước khi dùng.
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
from pathlib import Path


def detect(path: Path, threshold: float = 0.12) -> dict:
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-v", "error", "-i", str(path), "-an", "-vf",
         f"select='gt(scene,{threshold})',metadata=print:file=-", "-f", "null", "-"],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    cuts = [round(float(x), 3) for x in re.findall(r"pts_time:([0-9.]+)", r.stdout)]
    dur = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True).stdout.strip()
    return {"duration": float(dur), "threshold": threshold, "cuts": cuts,
            "studio_end": cuts[0] if cuts else None}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("--out", type=Path, default=Path("scenes.json"))
    ap.add_argument("--threshold", type=float, default=0.12)
    a = ap.parse_args()
    d = detect(a.input, a.threshold)
    a.out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(d['cuts'])} mốc cắt, studio_end={d['studio_end']}, thời lượng {d['duration']:.3f}s -> {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
