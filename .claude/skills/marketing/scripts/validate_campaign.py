#!/usr/bin/env python3
"""Ra soat mot ke hoach chien dich (Markdown) de kiem tra cac muc bat buoc."""

import argparse
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

REQUIRED_SECTIONS = [
    ("Mục tiêu", ["mục tiêu"]),
    ("Khách hàng", ["khách hàng"]),
    ("Định vị", ["định vị"]),
    ("Thông điệp", ["thông điệp"]),
    ("Kênh", ["kênh"]),
    ("Thời gian/Lịch triển khai", ["thời gian", "lịch triển khai", "lịch trình", "ngày bắt đầu"]),
    ("Ngân sách", ["ngân sách"]),
    ("KPI", ["kpi"]),
    ("Rủi ro", ["rủi ro"]),
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="validate_campaign.py",
        description=(
            "Kiem tra mot file ke hoach chien dich dang Markdown xem co du "
            "cac muc bat buoc hay khong: muc tieu, khach hang, dinh vi, "
            "thong diep, kenh, thoi gian, ngan sach, KPI, rui ro."
        ),
    )
    parser.add_argument("file", help="Đường dẫn file kế hoạch chiến dịch (Markdown)")
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    path = Path(args.file)
    if not path.exists():
        print(f"Lỗi: không tìm thấy file '{path}'.", file=sys.stderr)
        return 2
    if not path.is_file():
        print(f"Lỗi: '{path}' không phải là file.", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8-sig", errors="ignore").lower()

    missing = []
    for label, keywords in REQUIRED_SECTIONS:
        if not any(keyword in text for keyword in keywords):
            missing.append(label)

    print(f"Kiểm tra file: {path}")
    if not missing:
        print("Kết quả: ĐẠT — kế hoạch có đủ các mục bắt buộc.")
        return 0

    print("Kết quả: CHƯA ĐẠT — thiếu các mục sau:")
    for label in missing:
        print(f"  - {label}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
