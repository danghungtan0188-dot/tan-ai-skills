"""Nhat ky harness: moi lan hook chan / hoi / nhac, moi lan skill / agent / lenh duoc goi.

Du lieu nam NGOAI repo (repo cong khai): $TAN_NHAT_KY_DIR, mac dinh ~/.tan-harness/nhat-ky/,
moi thang mot file YYYY-MM.jsonl. KHONG ghi noi dung lenh, duong dan day du hay van ban nguoi
dung -- chi ten hook, quyet dinh, nhan ly do ngan, ten cong cu, ten thu muc du an.

Moi ham o day KHONG BAO GIO nem loi: nhat ky hong thi hook van phai chay dung.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

QUYET_DINH = ("chan", "hoi", "nhac", "dung")
DO_DAI_LY_DO = 120


def thu_muc() -> Path:
    return Path(os.environ.get("TAN_NHAT_KY_DIR") or Path.home() / ".tan-harness" / "nhat-ky")


def _du_an(payload: dict | None) -> str:
    cwd = (payload or {}).get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or ""
    return Path(cwd).name if cwd else ""


TRUNG_TRONG_S = 3  # trong chinh repo nay moi hook chay 2 lan (settings repo + toan cuc)


def _trung_dong_cuoi(tep: Path, su_kien: dict) -> bool:
    """Dong cuoi file giong het su_kien (tru 'luc') va cach chua toi TRUNG_TRONG_S giay."""
    if not tep.exists():
        return False
    with open(tep, "rb") as f:
        f.seek(max(0, tep.stat().st_size - 4096))
        cuoi = f.read().decode("utf-8", errors="replace").strip().splitlines()
    if not cuoi:
        return False
    try:
        truoc = json.loads(cuoi[-1])
        luc = time.mktime(time.strptime(truoc.pop("luc"), "%Y-%m-%dT%H:%M:%S"))
    except (ValueError, KeyError, TypeError, AttributeError):
        return False
    return truoc == su_kien and time.time() - luc < TRUNG_TRONG_S


def ghi(su_kien: dict) -> None:
    try:
        tm = thu_muc()
        tm.mkdir(parents=True, exist_ok=True)
        tep = tm / f"{time.strftime('%Y-%m')}.jsonl"
        if _trung_dong_cuoi(tep, su_kien):
            return
        dong = {"luc": time.strftime("%Y-%m-%dT%H:%M:%S"), **su_kien}
        with open(tep, "a", encoding="utf-8") as f:
            f.write(json.dumps(dong, ensure_ascii=False) + "\n")
    except Exception:
        pass


def ghi_hook(hook: str, quyet_dinh: str, ly_do: str, payload: dict | None = None) -> None:
    """Mot quyet dinh cua hook. ly_do la NHAN ngan (vd. 'DROP DATABASE'), khong phai lenh."""
    try:
        p = payload or {}
        ghi({"loai": "hook", "hook": hook, "quyet_dinh": quyet_dinh,
             "ly_do": str(ly_do)[:DO_DAI_LY_DO], "cong_cu": p.get("tool_name") or "",
             "du_an": _du_an(p), "phien": str(p.get("session_id") or "")[:8]})
    except Exception:
        pass


def ghi_su_dung(loai: str, ten: str, payload: dict | None = None) -> None:
    """loai: 'skill' | 'agent' | 'lenh' (slash command nguoi dung go)."""
    try:
        p = payload or {}
        ghi({"loai": loai, "ten": str(ten)[:80], "du_an": _du_an(p),
             "phien": str(p.get("session_id") or "")[:8]})
    except Exception:
        pass


def doc(so_ngay: int = 30) -> list[dict]:
    """Cac dong nhat ky trong so_ngay gan nhat (bo dong hong)."""
    moc = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time() - so_ngay * 86400))
    ra = []
    for tep in sorted(thu_muc().glob("*.jsonl")):
        for dong in tep.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                d = json.loads(dong)
            except ValueError:
                continue
            if isinstance(d, dict) and str(d.get("luc", "")) >= moc:
                ra.append(d)
    return ra
