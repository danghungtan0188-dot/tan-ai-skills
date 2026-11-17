"""Soi video da dung tim CANH LAP: cung mot hinh/anh xuat hien lai o hai cho cach xa nhau.

Bai hoc 17/11/2026 (phong su "80 nam Van hoa soi duong"): anh Bac 3 lan, flycam 3 lan, dong sen AI 3 lan
-> nguoi dung: "moi canh chi xuat hien 1 lan", "quy tac khong co canh bi lap rat quan trong".
Kiem tren VIDEO (khong phai bang phan canh) nen bat ca lap do ghep tay, khac kieu zoom/truot.

    python kiem_lap_canh.py BAN_DUNG.mp4                 # 2 hinh/giay, cach nhau >= 8 s moi tinh la lap
    python kiem_lap_canh.py BAN_DUNG.mp4 --bo 0:10 --bo 300:307   # bo qua intro/ket dai (logo lap lai co chu y)

Cach do: moi khung -> ban do duong net 64x36 (numpy), so khop bang tuong quan; giong >= --nguong lien tuc
>= 1,5 s va hai lan cach nhau >= --cach giay thi la cung canh.
Exit 0 = khong lap; 1 = co lap (in tung cap moc).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

W, H = 64, 36


def khung(f: Path, fps: float):
    """Moi khung -> vector DUONG NET (do lech diem anh ke ben) 64x36, chuan hoa; kem do net trung binh.
    So duong net thay vi mau: cac the do hoa cung nen mau khac nhau o chu nen khong bi tinh la lap."""
    import numpy as np
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(f), "-vf",
                        f"fps={fps},scale={W}:{H}:flags=area,format=gray", "-f", "rawvideo", "-"],
                       capture_output=True, check=True)
    a = np.frombuffer(r.stdout, dtype=np.uint8).astype(np.float32)
    a = a[: len(a) // (W * H) * W * H].reshape(-1, H, W)
    g = np.abs(np.diff(a, axis=2))[:, :-1, :] + np.abs(np.diff(a, axis=1))[:, :, :-1]
    g = g.reshape(len(g), -1)
    net = g.mean(axis=1)
    g = g - net[:, None]
    g /= np.linalg.norm(g, axis=1, keepdims=True) + 1e-6
    return g, net


def tim_lap(ds, fps: float, cach: float, nguong: float, bo: list[tuple[float, float]],
            ben: float = 1.5, net_toi_thieu: float = 2.0) -> list[tuple[float, float, float]]:
    """Cap (giay a, giay b, tuong quan): giong nhau >= nguong LIEN TUC >= ben giay (loai khoanh khac mo dau
    giong nhau cua hai the cung mau), hai lan cach nhau >= cach giay. Bo khung phang (man den, nen tron)."""
    import numpy as np
    g, net = ds
    n = len(g)
    t = np.arange(n) / fps
    dung = (net >= net_toi_thieu) & ~np.array([any(a <= x <= b for a, b in bo) for x in t], dtype=bool)
    c = g @ g.T
    giong = (c >= nguong) & dung[:, None] & dung[None, :]
    k = max(1, int(round(ben * fps)))
    lap = []
    buoc = int(cach * fps)
    for i in range(n):
        for j in range(i + buoc, n - k + 1):
            if i + k <= n and all(giong[i + m, j + m] for m in range(k)):
                lap.append((t[i], t[j], float(c[i, j])))
    gon: list[tuple[float, float, float]] = []
    for a, b2, cc in lap:
        if gon and abs(a - gon[-1][0]) < 3 and abs(b2 - gon[-1][1]) < 3:
            continue
        gon.append((a, b2, cc))
    return gon


def doc_bo(s: str) -> tuple[float, float]:
    a, b = s.split(":")
    return float(a), float(b)


def mmss(t: float) -> str:
    return f"{int(t // 60)}:{int(t % 60):02d}"


def main() -> int:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", type=Path)
    ap.add_argument("--fps", type=float, default=2.0)
    ap.add_argument("--cach", type=float, default=8.0, help="hai lan xuat hien cach nhau toi thieu (giay)")
    ap.add_argument("--nguong", type=float, default=0.95, help="tuong quan >= nguong la cung canh")
    ap.add_argument("--bo", type=doc_bo, action="append", default=[], help="khoang bo qua GIAY_DAU:GIAY_CUOI")
    a = ap.parse_args()
    lap = tim_lap(khung(a.video, a.fps), a.fps, a.cach, a.nguong, a.bo)
    if lap:
        for x, y, c in lap:
            print(f"LAP: {mmss(x)} va {mmss(y)} (tuong quan {c:.3f})")
        return 1
    print("PASS: khong co canh lap")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
