#!/usr/bin/env python3
"""Tìm clip thô trong kho của người dùng rồi in bảng ứng viên để xác nhận.

    python find_clips.py [--kho D:/quay ...] [--tu 2026-09-20] [--den 2026-09-30]
                         [--ten "suc khoe"] [--min-mb 2] [--out ung-vien.json]

Không có `--kho` thì tìm mặc định ở Desktop, Documents và thư mục Google Drive đã đồng bộ
(xem references/kho-clip.md). Chỉ quét trong kho được chỉ định, không mở rộng sang chỗ khác.

`--ten` so khớp **bỏ dấu, không phân biệt hoa thường**, khớp cả tên file lẫn tên thư mục cha —
gõ "suc khoe" tìm được "Khám sức khỏe 20-09".

Bỏ qua thư mục đầu ra và cache; bỏ file nhỏ hơn `--min-mb` (thường là clip lỡ tay).
Máy chỉ LỌC theo tên và ngày. Có danh sách rồi vẫn phải chạy survey_rushes.py để xem thật.
"""
from __future__ import annotations
import argparse
import json
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from survey_rushes import DUOI  # noqa: E402

BO_QUA = {".git", "node_modules", "outputs", "output", "render", "renders", "edit",
          "thumbs", "cache", "__pycache__", "$RECYCLE.BIN", "System Volume Information"}


def khong_dau(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if not unicodedata.combining(c))


def kho_mac_dinh() -> list[Path]:
    nha = Path.home()
    ung = [nha / "Desktop", nha / "Documents", nha / "Google Drive", nha / "My Drive"]
    ung += [Path(f"{c}:/My Drive") for c in "GH"]
    return [p for p in ung if p.is_dir()]


def quet(goc: Path) -> list[Path]:
    ra = []
    for p in goc.rglob("*"):
        if p.is_dir():
            continue
        if BO_QUA & {x for x in p.parts}:
            continue
        if p.suffix.lower() in DUOI:
            ra.append(p)
    return ra


def loc(files: list[Path], ten: str | None, tu: float | None, den: float | None,
        min_mb: float) -> list[dict]:
    khoa = khong_dau(ten) if ten else None
    ra = []
    for p in files:
        try:
            st = p.stat()
        except OSError:                 # file trên Drive chưa tải về, hoặc mất quyền đọc
            continue
        if st.st_size < min_mb * 1024 * 1024:
            continue
        if tu and st.st_mtime < tu:
            continue
        if den and st.st_mtime > den:
            continue
        if khoa and khoa not in khong_dau(f"{p.parent.name} {p.name}"):
            continue
        ra.append({"file": str(p), "name": p.name, "thu_muc": str(p.parent),
                   "mb": round(st.st_size / 1024 / 1024, 1),
                   "sua": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M")})
    return sorted(ra, key=lambda x: x["sua"], reverse=True)


def ngay(s: str | None, cuoi: bool = False) -> float | None:
    if not s:
        return None
    d = datetime.strptime(s, "%Y-%m-%d")
    return (d.replace(hour=23, minute=59, second=59) if cuoi else d).timestamp()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kho", nargs="*", type=Path, default=[])
    ap.add_argument("--tu", help="ngày sửa từ, dạng 2026-09-20")
    ap.add_argument("--den")
    ap.add_argument("--ten", help="từ khoá trong tên file hoặc tên thư mục cha")
    ap.add_argument("--min-mb", type=float, default=2.0)
    ap.add_argument("--out", type=Path, help="ghi danh sách ra JSON")
    a = ap.parse_args()
    kho = a.kho or kho_mac_dinh()
    if not kho:
        raise SystemExit("Không thấy kho nào để tìm — đưa đường dẫn bằng --kho")
    files = [f for g in kho for f in quet(Path(g))]
    ra = loc(files, a.ten, ngay(a.tu), ngay(a.den, True), a.min_mb)
    print("Kho tìm: " + ", ".join(str(k) for k in kho))
    for x in ra[:60]:
        print(f"  {x['sua']}  {x['mb']:>7.1f}MB  {x['name'][:42]:<42}  {x['thu_muc']}")
    if len(ra) > 60:
        print(f"  … còn {len(ra) - 60} file nữa")
    print(f"{len(ra)}/{len(files)} clip khớp điều kiện")
    if a.out:
        a.out.write_text(json.dumps(ra, ensure_ascii=False, indent=1), encoding="utf-8")
        print("->", a.out)
    print("Xác nhận danh sách với người dùng, rồi chạy survey_rushes.py trên thư mục chứa chúng.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
