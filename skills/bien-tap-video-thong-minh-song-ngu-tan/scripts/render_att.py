#!/usr/bin/env python3
"""Render bản tin ATT NEWS một lượt — thay cho lệnh ffmpeg viết tay.

    python render_att.py INPUT --captions captions.ass --scenes scenes.json --out OUT.mp4
        [--lower-thirds lower-thirds.ass] [--card screen_card.png] [--extra-logo logo.png]
        [--outro-dir outro_frames] [--bugs-dir .] [--studio-end GIAY] [--preview]

Lớp và vị trí ở 1920×1080:
  thẻ TV          (900,240)          chỉ khi t < studio_end
  Facebook/Zalo   (46,H-h-46) α 0.94  suốt video
  ATT NEWS        (1612,130)         chỉ khi t ≥ studio_end — phần trường quay đã in sẵn logo
  logo phụ        cao 78, cách ATT NEWS 14 px về trái, suốt video (vd logo y tế)
  banner, phụ đề  lớp trên cùng
Âm thanh: loudnorm 2 lượt linear. Outro: nối khung PNG 30 fps + đoạn im lặng cùng độ dài.
Mã hoá: preset faster, crf 20 (máy nóng nhanh); --preview: veryfast, crf 27.
Sau khi render: qa.py OUT --source INPUT --tail <giây outro> --captions bilingual.json
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from make_att_bugs import icon_mxh, logo_att  # noqa: E402
from render import FILTERS, duration, loudnorm_linear, q  # noqa: E402


def build_cmd(a, studio_end: float, dur: float, af: str) -> list[str]:
    bugs = Path(a.bugs_dir)
    att, icons = bugs / "att_news.png", bugs / "icons.png"
    if not att.exists():
        logo_att().save(att)
    if not icons.exists():
        icon_mxh().save(icons)

    inputs, fc = ["-i", str(a.input)], [f"[0:v]{FILTERS['news_clean']}[v0]"]
    cur = "v0"

    def them(args: list[str]) -> int:
        inputs.extend(args)
        return sum(1 for x in inputs if x == "-i") - 1

    def lop(expr: str) -> None:
        nonlocal cur
        nxt = f"v{len(fc)}"
        fc.append(expr.format(cur=cur, nxt=nxt))
        cur = nxt

    if a.card:
        i = them(["-i", str(a.card)])
        lop(f"[{{cur}}][{i}:v]overlay=900:240:enable='lt(t,{studio_end})'[{{nxt}}]")
    i = them(["-i", str(icons)])
    lop(f"[{i}:v]format=rgba,colorchannelmixer=aa=0.94[ic];[{{cur}}][ic]overlay=46:H-h-46[{{nxt}}]")
    i = them(["-i", str(att)])
    lop(f"[{i}:v]format=rgba[att];[{{cur}}][att]overlay=1612:130:enable='gte(t,{studio_end})'[{{nxt}}]")
    if a.extra_logo:
        i = them(["-i", str(a.extra_logo)])
        lop(f"[{i}:v]format=rgba,scale=-1:78[xl];[{{cur}}][xl]overlay=x=1598-w:y=130[{{nxt}}]")
    subs = ",".join(f"subtitles='{q(Path(p).resolve())}'" for p in (a.lower_thirds, a.captions) if p)
    outro = sorted(Path(a.outro_dir).glob("f_*.png")) if a.outro_dir else []
    fade = f",fade=t=out:st={dur - 0.4:.3f}:d=0.4" if outro else ""
    lop(f"[{{cur}}]{subs},trim=0:{dur},setpts=PTS-STARTPTS{fade},fps=30,format=yuv420p,setsar=1[{{nxt}}]")
    amain = f"[0:a]{af},aresample=44100,atrim=0:{dur},asetpts=PTS-STARTPTS"
    if outro:
        do_dai = len(outro) / 30
        i = them(["-framerate", "30", "-i", str(Path(a.outro_dir) / "f_%04d.png")])
        j = them(["-f", "lavfi", "-t", f"{do_dai:.3f}", "-i", "anullsrc=r=44100:cl=stereo"])
        fc.append(f"[{i}:v]fps=30,format=yuv420p,setsar=1,setpts=PTS-STARTPTS[ov];[{cur}][ov]concat=n=2:v=1:a=0[vo]")
        fc.append(f"{amain},afade=t=out:st={dur - 0.5:.3f}:d=0.5[am];[{j}:a]aresample=44100[oa];"
                  "[am][oa]concat=n=2:v=0:a=1[ao]")
    else:
        fc.append(f"[{cur}]null[vo];{amain}[ao]")
    enc = ["veryfast", "27"] if a.preview else ["faster", "20"]
    return ["ffmpeg", "-y", "-hide_banner", "-v", "error", "-stats", *inputs,
            "-filter_complex", ";".join(fc), "-map", "[vo]", "-map", "[ao]",
            "-c:v", "libx264", "-preset", enc[0], "-crf", enc[1],
            "-c:a", "aac", "-ar", "44100", "-b:a", "192k", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(a.out)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("--captions", required=True)
    ap.add_argument("--scenes", type=Path)
    ap.add_argument("--studio-end", type=float)
    ap.add_argument("--lower-thirds")
    ap.add_argument("--card", type=Path)
    ap.add_argument("--extra-logo", type=Path)
    ap.add_argument("--outro-dir", type=Path)
    ap.add_argument("--bugs-dir", default=".")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--preview", action="store_true")
    a = ap.parse_args()
    se = a.studio_end if a.studio_end is not None else (
        json.loads(a.scenes.read_text(encoding="utf-8"))["studio_end"] if a.scenes else None)
    if se is None:
        raise SystemExit("Cần --scenes (từ detect_scenes.py) hoặc --studio-end")
    dur = float(duration(str(a.input)))
    subprocess.run(build_cmd(a, se, dur, loudnorm_linear(str(a.input))), check=True)
    print(a.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
