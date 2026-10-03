"""Đồ hoạ động bằng Remotion (thư mục `do-hoa/` ở gốc repo).

Python chỉ gọi `npx remotion render` với props JSON. ffmpeg vẫn dựng video chính (video.py) và
đắp các clip đồ hoạ trong suốt (ProRes 4444) vào đúng giây — thời lượng video không đổi.
Render đồ hoạ nặng (Chrome chạy ngầm): concurrency 2, và clip đã render thì dùng lại theo props.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

from . import REPO_ROOT, write_json

DIR = REPO_ROOT / "do-hoa"
MAU = {"intro": "Intro", "so-lieu": "SoLieu", "lower-third": "LowerThird", "chu-dong": "ChuDong"}
TRONG_SUOT = {"Intro", "SoLieu", "LowerThird"}  # xuất .mov có kênh alpha để đắp lên video
GIAY_MAC_DINH = {"Intro": 4.0, "SoLieu": 5.0, "LowerThird": 5.0}
KHOA_DU_AN = {"intro": "Intro", "so_lieu": "SoLieu", "lower_third": "LowerThird"}  # mục `do_hoa` trong dự án
# Remotion gộp props với defaultProps (dữ liệu mẫu cho Studio) — trường không khai báo phải gửi rỗng, kẻo lọt dữ liệu mẫu.
RONG = {"Intro": {"phuDe": "", "ngay": ""},
        "SoLieu": {"soLe": 0, "tienTo": "", "donVi": "", "moTa": "", "cot": []},
        "LowerThird": {"chucVu": ""},
        "ChuDong": {"amThanh": "", "tieuDe": ""}}


class DoHoaError(RuntimeError):
    pass


def check() -> str | None:
    if not shutil.which("npx"):
        return "chưa có Node.js (npx) — cài Node 18+ từ nodejs.org"
    if not (DIR / "node_modules").exists():
        return "chưa cài gói Remotion — chạy: cd do-hoa && npm i"
    return None


def camel(props: dict) -> dict:
    """tieu_de -> tieuDe: dự án dùng snake_case như phần còn lại của tan_studio, Remotion dùng camelCase."""
    def conv(k: str) -> str:
        head, *rest = k.split("_")
        return head + "".join(p[:1].upper() + p[1:] for p in rest)
    return {conv(k): ([camel(x) if isinstance(x, dict) else x for x in v] if isinstance(v, list) else v)
            for k, v in props.items()}


def comp_id(mau: str) -> str:
    comp = MAU.get(mau, mau)
    if comp not in MAU.values():
        raise DoHoaError(f"không có mẫu '{mau}'. Có: {sorted(MAU)}")
    return comp


def render(mau: str, props: dict, out: Path, anh_tai_giay: float | None = None,
           public_dir: Path | None = None) -> Path:
    """props theo camelCase của mẫu. anh_tai_giay: chỉ xuất một khung PNG ở giây đó (xem nhanh, rất nhẹ)."""
    reason = check()
    if reason:
        raise DoHoaError(reason)
    comp = comp_id(mau)
    out = Path(out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    props_file = write_json(out.with_name(out.stem + ".props.json"), {**RONG[comp], **props})
    cmd = [shutil.which("npx"), "remotion", "render" if anh_tai_giay is None else "still", "src/index.ts", comp,
           str(out), f"--props={props_file}", "--log=error"]
    cmd.append("--concurrency=2" if anh_tai_giay is None else f"--frame={round(anh_tai_giay * 30)}")
    if public_dir:
        cmd.append(f"--public-dir={Path(public_dir).resolve()}")
    r = subprocess.run(cmd, cwd=DIR, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode or not out.exists():
        raise DoHoaError(f"Remotion lỗi (exit {r.returncode}): {(r.stderr or r.stdout).strip()[-800:]}")
    return out


def check_config(do_hoa: dict) -> list[str]:
    errors = [f"do_hoa có khoá lạ '{k}' — dùng {sorted(KHOA_DU_AN)}" for k in do_hoa if k not in KHOA_DU_AN]
    for key, items in do_hoa.items():
        for item in (items if isinstance(items, list) else [items]):
            if key != "intro" and "tai" not in item:
                errors.append(f"do_hoa.{key}: thiếu 'tai' (giây bắt đầu đắp)")
    return errors


def overlays(do_hoa: dict, ti_le: str, out_dir: Path, duration: float) -> list[dict]:
    """Render (hoặc dùng lại) từng clip đồ hoạ trong mục `do_hoa` của dự án; trả danh sách để video.py đắp."""
    out = []
    for key, comp in KHOA_DU_AN.items():
        items = do_hoa.get(key) or []
        for item in (items if isinstance(items, list) else [items]):
            tai = float(item.get("tai", 0.0))
            props = {k: v for k, v in item.items() if k != "tai"}
            props = {"tiLe": ti_le, "thoiLuong": GIAY_MAC_DINH[comp], **camel(props)}
            if tai >= duration:
                raise DoHoaError(f"do_hoa.{key} đắp ở {tai}s nhưng video chỉ dài {duration:.1f}s")
            props["thoiLuong"] = min(props["thoiLuong"], round(duration - tai, 3))
            digest = hashlib.sha1(f"{comp}|{json.dumps(props, sort_keys=True, ensure_ascii=False)}".encode())
            clip = Path(out_dir) / f"{comp}_{digest.hexdigest()[:8]}.mov"
            if not clip.exists():
                render(comp, props, clip)
            out.append({"mau": comp, "tep": str(clip), "tai": tai, "thoi_luong": props["thoiLuong"]})
    return sorted(out, key=lambda o: o["tai"])
