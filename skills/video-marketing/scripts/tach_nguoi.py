"""Tach nguoi khoi nen DUNG DOAN co hieu ung + do vung mat, de dat hieu ung "sau nguoi, khong de mat".

Chi cat doan [tu - du, den + du] roi tach (may hay sap: khong tach ca video). Tach bang
`npx hyperframes remove-background` (u2net_human_seg, Apache-2.0) -> video trong suot (.webm VP9 alpha).
Vung mat do bang YuNet (quet_mat cua phu_de_tranh_mat.py).

    python tach_nguoi.py video.mp4 --tu 22.4 --den 28.1 -o edit/nguoi-01.webm
    -> edit/nguoi-01.webm (nguoi tren nen trong suot) + edit/nguoi-01.mat.json (vung mat, vung tren dau)
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HYPERFRAMES = "hyperframes@0.8.226"
DU = 0.5  # giay cat du moi dau: hieu ung vao/ra mem van co nguoi da tach
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "bien-tap-video-thong-minh-song-ngu-tan" / "scripts"))


def vung(mat: list[tuple[float, list[tuple[float, float, float, float]]]]) -> dict:
    """Gop moi hop mat trong doan -> hop bao (x0, y0, x1, y1) chuan hoa + 'tren_dau' = y0 nho nhat.

    Hieu ung dat 'tren dau, sau nguoi' thi day phan quan trong (chu, so) nam tren y = tren_dau."""
    hop = [h for _, hs in mat for h in hs]
    if not hop:
        return {"co_mat": False, "hop_mat": None, "tren_dau": None, "so_khung_co_mat": 0, "so_khung": len(mat)}
    x0, y0 = min(h[0] for h in hop), min(h[1] for h in hop)
    x1, y1 = max(h[2] for h in hop), max(h[3] for h in hop)
    return {"co_mat": True, "hop_mat": [round(v, 3) for v in (max(0, x0), max(0, y0), min(1, x1), min(1, y1))],
            "tren_dau": round(max(0.0, y0), 3), "so_khung_co_mat": sum(1 for _, hs in mat if hs),
            "so_khung": len(mat)}


def lenh_cat(video: Path, tu: float, den: float, ra: Path) -> list[str]:
    bd = max(0.0, tu - DU)
    return ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{bd:.3f}", "-to", f"{den + DU:.3f}",
            "-i", str(video), "-an", "-c:v", "libx264", "-preset", "faster", "-crf", "16", "-threads", "2",
            "-pix_fmt", "yuv420p", str(ra)]


def main() -> int:
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", type=Path)
    ap.add_argument("--tu", type=float, required=True)
    ap.add_argument("--den", type=float, required=True)
    ap.add_argument("-o", "--out", type=Path, required=True, help=".webm (trong suot)")
    a = ap.parse_args()
    if a.out.resolve() == a.video.resolve():
        raise SystemExit("Khong ghi de video goc.")
    a.out.parent.mkdir(parents=True, exist_ok=True)
    doan = a.out.with_suffix(".doan.mp4")
    subprocess.run(lenh_cat(a.video, a.tu, a.den, doan), check=True)
    subprocess.run(["npx", "-y", HYPERFRAMES, "remove-background", str(doan), "-o", str(a.out),
                    "--device", "cpu", "--quality", "balanced"], check=True, shell=sys.platform == "win32")
    from phu_de_tranh_mat import quet_mat

    bd = max(0.0, a.tu - DU)
    mat = [(t + bd, hs) for t, hs in quet_mat(str(doan))]
    thong_tin = {"video": str(a.video), "nguoi": str(a.out), "bat_dau_doan": round(bd, 3),
                 "ket_thuc_doan": round(a.den + DU, 3), **vung(mat)}
    a.out.with_suffix(".mat.json").write_text(json.dumps(thong_tin, ensure_ascii=False, indent=1), encoding="utf-8")
    doan.unlink(missing_ok=True)
    print(json.dumps(thong_tin, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
