"""Tìm và tải cảnh minh hoạ (b-roll) từ Pexels/Pixabay theo từ khoá.

Lệnh riêng, chạy tay: `chay` vẫn không ra mạng. Chỉ gửi đi TỪ KHOÁ người dùng gõ, không gửi script/media.
Cách lọc phỏng theo MoneyPrinterTurbo (MIT, app/services/material.py): đúng chiều khung, đủ dài,
chọn bản nhỏ nhất mà vẫn phủ kín khung để file nhẹ. Key đọc từ biến môi trường, không ghi ra file.
"""

from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path
from urllib.parse import urlencode

from . import write_json
from .video import SIZES

KEYS = {"pexels": "PEXELS_API_KEY", "pixabay": "PIXABAY_API_KEY"}
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) tan-studio"
MAX_BYTES = 512 * 1024 * 1024


def _get(url: str, headers: dict | None = None, timeout: int = 60):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})}),
                                  timeout=timeout)


def _get_json(url: str, headers: dict | None = None) -> dict:
    with _get(url, headers) as r:
        return json.loads(r.read().decode("utf-8"))


def _key(nguon: str) -> str:
    key = os.environ.get(KEYS[nguon], "").strip()
    if not key:
        raise RuntimeError(f"chưa đặt biến môi trường {KEYS[nguon]} (lấy key miễn phí trên trang {nguon})")
    return key


def dung_chieu(w: int, h: int, ti_le: str) -> bool:
    return w > h if ti_le == "16:9" else h > w


def chon_ban(ban: list[tuple[int, int, str]], ti_le: str) -> tuple[int, int, str] | None:
    """Bản (rộng, cao, url) nhỏ nhất mà đúng chiều và không nhỏ hơn khung đích."""
    tw, th = SIZES[ti_le]
    hop = [b for b in ban if dung_chieu(b[0], b[1], ti_le) and b[0] >= tw and b[1] >= th]
    return min(hop, key=lambda b: b[0] * b[1]) if hop else None


def tim_pexels(tu_khoa: str, ti_le: str, toi_thieu_s: float, so_luong: int, get_json=_get_json) -> list[dict]:
    q = urlencode({"query": tu_khoa, "per_page": 40, "orientation": "landscape" if ti_le == "16:9" else "portrait"})
    data = get_json(f"https://api.pexels.com/v1/videos/search?{q}", {"Authorization": _key("pexels")})
    out = []
    for v in data.get("videos", []):
        if (v.get("duration") or 0) < toi_thieu_s:
            continue
        ban = chon_ban([(f.get("width") or 0, f.get("height") or 0, f.get("link"))
                        for f in v.get("video_files", []) if f.get("link")], ti_le)
        if ban:
            out.append({"nguon": "pexels", "id": str(v["id"]), "url": ban[2], "rong": ban[0], "cao": ban[1],
                        "thoi_luong": v["duration"], "trang": v.get("url"), "tac_gia": (v.get("user") or {}).get("name")})
    return out[:so_luong]


def tim_pixabay(tu_khoa: str, ti_le: str, toi_thieu_s: float, so_luong: int, get_json=_get_json) -> list[dict]:
    q = urlencode({"q": tu_khoa, "video_type": "film", "per_page": 50, "key": _key("pixabay")})
    data = get_json(f"https://pixabay.com/api/videos/?{q}")
    out = []
    for v in data.get("hits", []):
        if (v.get("duration") or 0) < toi_thieu_s:
            continue
        ban = chon_ban([(f.get("width") or 0, f.get("height") or 0, f.get("url"))
                        for f in (v.get("videos") or {}).values() if f.get("url")], ti_le)
        if ban:
            out.append({"nguon": "pixabay", "id": str(v["id"]), "url": ban[2], "rong": ban[0], "cao": ban[1],
                        "thoi_luong": v["duration"], "trang": v.get("pageURL"), "tac_gia": v.get("user")})
    return out[:so_luong]


TIM = {"pexels": tim_pexels, "pixabay": tim_pixabay}


def tai(canh: list[dict], out_dir: Path, tu_khoa: str, get=_get, log=print) -> list[Path]:
    """Tải vào out_dir/<nguon>-<id>.mp4 (đã có thì bỏ qua), ghi nguon.json để ghi công tác giả."""
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for c in canh:
        dst = out_dir / f"{c['nguon']}-{c['id']}.mp4"
        if dst.exists() and dst.stat().st_size > 0:
            log(f"đã có: {dst.name}")
        else:
            part = dst.with_suffix(".part")
            n = 0
            with get(c["url"], timeout=240) as r, open(part, "wb") as f:
                while chunk := r.read(1024 * 1024):
                    n += len(chunk)
                    if n > MAX_BYTES:
                        f.close()
                        part.unlink()
                        raise RuntimeError(f"{dst.name} lớn hơn 512 MB, bỏ")
                    f.write(chunk)
            part.replace(dst)
            log(f"đã tải: {dst.name} ({n / 1e6:.1f} MB)")
        paths.append(dst)
    ghi = out_dir / "nguon.json"
    cu = json.loads(ghi.read_text(encoding="utf-8")) if ghi.exists() else []
    co = {(x["nguon"], x["id"]) for x in cu}
    cu += [{**{k: v for k, v in c.items() if k != "url"}, "tu_khoa": tu_khoa, "file": f"{c['nguon']}-{c['id']}.mp4"}
           for c in canh if (c["nguon"], c["id"]) not in co]
    write_json(ghi, cu)
    return paths
