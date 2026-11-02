"""Render mot the mau phong cach (assets/mau/<ten>/index.html) de XEM: check -> render -> anh 4 khung.

Chi render TREN MAY (`hyperframes render`), khong bao gio `cloud render` (dich vu tra phi HeyGen).

    python render_mau.py swiss                 # -> <ra>/swiss.mp4 + <ra>/swiss.soi.png
    python render_mau.py swiss --ra D:/tam
    python render_mau.py swiss --trong-suot    # -> swiss.webm nen trong suot, de dua vao ghep_lop.py cua video-marketing

Exit 0 = check ok + render dung thoi luong; 1 = co loi (in ra).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HYPERFRAMES = "hyperframes@0.8.226"
MAU = Path(__file__).resolve().parents[1] / "assets" / "mau"
CAU_HINH = {"$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
            "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
            "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"}}


def thoi_luong_goc(html: str) -> float:
    m = re.search(r'data-composition-id="main"[^>]*data-duration="([\d.]+)"', html)
    if not m:
        raise SystemExit("index.html thieu root data-composition-id=\"main\" co data-duration")
    return float(m.group(1))


def bo_nen(html: str) -> str:
    """Doi nen xam xem thu (--nen) thanh trong suot."""
    if "--nen: #8a8f96" not in html:
        raise SystemExit("index.html thieu '--nen: #8a8f96' nen khong xuat trong suot duoc")
    return html.replace("--nen: #8a8f96", "--nen: transparent", 1)


def lenh_soi(mp4: Path, ra: Path, fps: int, giay: float) -> list[str]:
    """4 khung o 10%, 30%, 60%, 93% thoi luong, ghep ngang."""
    n = [round(fps * giay * k) for k in (0.1, 0.3, 0.6, 0.93)]
    chon = "+".join(f"eq(n\\,{i})" for i in n)
    return ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(mp4), "-vf",
            f"select='{chon}',scale=270:480,tile=4x1", "-frames:v", "1", "-fps_mode", "vfr", str(ra)]


def _npx(*a: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(["npx", "-y", HYPERFRAMES, *a], cwd=cwd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", shell=sys.platform == "win32")


def main() -> int:
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ten", help="ten thu muc trong assets/mau/")
    ap.add_argument("--ra", type=Path, default=Path(tempfile.gettempdir()) / "motion-graphics-tan")
    ap.add_argument("--trong-suot", action="store_true", help="xuat .webm VP9 alpha thay vi .mp4 nen xam")
    a = ap.parse_args()
    nguon = MAU / a.ten / "index.html"
    html = nguon.read_text(encoding="utf-8")
    giay = thoi_luong_goc(html)
    if a.trong_suot:
        html = bo_nen(html)
    a.ra.mkdir(parents=True, exist_ok=True)
    # Windows: tien trinh render (Chrome) con giu file vai giay -> don thu muc tam khong duoc thi bo qua
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tam:
        du_an = Path(tam).resolve()
        (du_an / "index.html").write_text(html, encoding="utf-8")
        (du_an / "hyperframes.json").write_text(json.dumps(CAU_HINH), encoding="utf-8")
        kiem = _npx("check", "--json", cwd=du_an)
        try:
            ket = json.loads(kiem.stdout)
        except ValueError:
            print(kiem.stdout[-800:], kiem.stderr[-800:])
            return 1
        # Doc MOI muc cua check (lint, layout, contrast, craft...): tung bo sot contrast nen render ra the loi.
        phat_hien = [f for v in ket.values() if isinstance(v, dict) for f in v.get("findings", [])]
        loi = [f for f in phat_hien if f.get("severity") == "error"]
        canh_bao = sorted({f["code"] for f in phat_hien if f.get("severity") == "warning"})
        print(f"check: {'ok' if ket.get('ok') else 'LOI'}; loi {len(loi)}; canh bao {canh_bao or 'khong'}")
        for f in loi:
            print("  LOI", f.get("code"), f.get("message"), "| Fix:", f.get("fixHint"))
        if loi or not ket.get("ok"):
            return 1
        mp4 = a.ra / f"{a.ten}.{'webm' if a.trong_suot else 'mp4'}"
        dinh_dang = ["--format", "webm"] if a.trong_suot else []
        r = _npx("render", "--quality", "draft", *dinh_dang, "-o", str(mp4), cwd=du_an)
        if r.returncode or not mp4.exists():
            print(r.stdout[-1200:], r.stderr[-1200:])
            return 1
    dai = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                str(mp4)], capture_output=True, text=True).stdout.strip() or 0)
    soi = a.ra / f"{a.ten}.soi.png"
    subprocess.run(lenh_soi(mp4, soi, 30, giay), check=True)
    dung = abs(dai - giay) < 0.1
    print(f"render: {mp4} ({dai:.2f}s / mong {giay}s {'DUNG' if dung else 'LECH'}); anh 4 khung: {soi}")
    return 0 if dung else 1


if __name__ == "__main__":
    raise SystemExit(main())
