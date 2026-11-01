"""Ghep lop cho hieu ung "sau nguoi": nen goc -> hieu ung (trong suot) -> nguoi da tach, trong [tu, den].

Ngoai khoang [tu, den] video giu nguyen. Tieng giu nguyen (copy). Hieu ung la video trong suot
(.webm VP9 alpha hoac .mov ProRes 4444) du khung, bat dau tu giay 0 cua no; nguoi la file cua tach_nguoi.py.

    python ghep_lop.py video.mp4 --hieu-ung hu.webm --nguoi edit/nguoi-01.webm --tu 22.4 --den 28.1 -o ra.mp4

.webm PHAI giai ma bang libvpx-vp9: bo giai ma vp9 mac dinh cua ffmpeg bo kenh alpha -> nguoi thanh khoi dac.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def _dau_vao(p: Path) -> list[str]:
    return (["-c:v", "libvpx-vp9"] if p.suffix.lower() == ".webm" else []) + ["-i", str(p)]


def lenh_ghep(nen: Path, hieu_ung: Path, nguoi: Path | None, tu: float, den: float, bd_nguoi: float,
              w: int, h: int, ra: Path) -> list[str]:
    cua_so = f"between(t,{tu:.3f},{den:.3f})"
    loc = (f"[1:v]scale={w}:{h},format=rgba,setpts=PTS-STARTPTS+{tu:.3f}/TB[hu];"
           f"[0:v][hu]overlay=0:0:eof_action=pass:enable='{cua_so}'[a]")
    vao = ["-i", str(nen), *_dau_vao(hieu_ung)]
    if nguoi is not None:
        vao += _dau_vao(nguoi)
        loc += (f";[2:v]scale={w}:{h},format=rgba,setpts=PTS-STARTPTS+{bd_nguoi:.3f}/TB[ng];"
                f"[a][ng]overlay=0:0:eof_action=pass:enable='{cua_so}'[v]")
    else:
        loc = loc.replace("[a]", "[v]")
    return ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *vao, "-filter_complex", loc,
            "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-preset", "faster", "-crf", "18", "-threads", "2",
            "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(ra)]


def kich_thuoc(video: Path) -> tuple[int, int]:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                        "-of", "json", str(video)], capture_output=True, text=True, check=True)
    s = json.loads(r.stdout)["streams"][0]
    return int(s["width"]), int(s["height"])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", type=Path)
    ap.add_argument("--hieu-ung", type=Path, required=True)
    ap.add_argument("--nguoi", type=Path, help="bo trong = hieu ung de len tren nguoi (khong can tach nen)")
    ap.add_argument("--tu", type=float, required=True)
    ap.add_argument("--den", type=float, required=True)
    ap.add_argument("-o", "--out", type=Path, required=True)
    a = ap.parse_args()
    if a.out.resolve() in {a.video.resolve(), a.hieu_ung.resolve()}:
        raise SystemExit("Khong ghi de file dau vao.")
    bd = 0.0
    if a.nguoi:
        mat = a.nguoi.with_suffix(".mat.json")
        bd = json.loads(mat.read_text(encoding="utf-8"))["bat_dau_doan"] if mat.exists() else a.tu
    w, h = kich_thuoc(a.video)
    subprocess.run(lenh_ghep(a.video, a.hieu_ung, a.nguoi, a.tu, a.den, bd, w, h, a.out), check=True)
    print(a.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
