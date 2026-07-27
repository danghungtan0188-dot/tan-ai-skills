#!/usr/bin/env python3
"""Tao lich noi dung (CSV, UTF-8 BOM) cho nhieu ngay va nhieu kenh."""

import argparse
import csv
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

HEADERS = [
    "Ngày đăng",
    "Giờ đăng",
    "Kênh",
    "Mục tiêu",
    "Nhóm khách hàng",
    "Chủ đề",
    "Định dạng",
    "Nội dung chính",
    "CTA",
    "Người phụ trách",
    "Trạng thái",
    "KPI theo dõi",
]

FREQUENCY_DAYS = {
    "daily": 1,
    "alternate": 2,
    "weekly": 7,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="create_content_calendar.py",
        description=(
            "Tao lich noi dung dang CSV (UTF-8 BOM, mo dung tieng Viet trong "
            "Excel) cho mot khoang thoi gian va danh sach kenh cho truoc. "
            "Cac cot noi dung chi tiet duoc de trong de nguoi dung dien tiep."
        ),
    )
    parser.add_argument(
        "--start-date",
        dest="start_date",
        required=True,
        help="Ngày bắt đầu, định dạng YYYY-MM-DD",
    )
    parser.add_argument(
        "--days",
        type=int,
        required=True,
        help="Số ngày của lịch nội dung (số nguyên dương)",
    )
    parser.add_argument(
        "--channels",
        required=True,
        help="Danh sách kênh, phân tách bằng dấu phẩy (ví dụ: Facebook,TikTok)",
    )
    parser.add_argument(
        "--frequency",
        choices=sorted(FREQUENCY_DAYS.keys()),
        default="daily",
        help="Tần suất đăng mỗi kênh: daily (mỗi ngày), alternate (cách ngày), weekly (mỗi tuần). Mặc định: daily",
    )
    parser.add_argument(
        "--time",
        default="08:00",
        help="Giờ đăng mặc định cho mỗi dòng, định dạng HH:MM. Mặc định: 08:00",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="content-calendar.csv",
        help="Đường dẫn file CSV đầu ra. Mặc định: content-calendar.csv",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Cho phép ghi đè nếu file đầu ra đã tồn tại",
    )
    return parser


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        start = parse_date(args.start_date)
    except ValueError:
        print(
            f"Lỗi: --start-date '{args.start_date}' không đúng định dạng YYYY-MM-DD.",
            file=sys.stderr,
        )
        return 1

    if args.days <= 0:
        print("Lỗi: --days phải là số nguyên dương.", file=sys.stderr)
        return 1

    channels = [c.strip() for c in args.channels.split(",") if c.strip()]
    if not channels:
        print("Lỗi: --channels phải có ít nhất một kênh hợp lệ.", file=sys.stderr)
        return 1

    output_path = Path(args.output)
    if output_path.exists() and not args.force:
        print(
            f"Lỗi: file '{output_path}' đã tồn tại. Dùng --force để ghi đè.",
            file=sys.stderr,
        )
        return 1

    step = FREQUENCY_DAYS[args.frequency]

    rows = []
    for offset in range(0, args.days, step):
        current_day = start + timedelta(days=offset)
        for channel in channels:
            rows.append(
                {
                    "Ngày đăng": current_day.isoformat(),
                    "Giờ đăng": args.time,
                    "Kênh": channel,
                    "Mục tiêu": "",
                    "Nhóm khách hàng": "",
                    "Chủ đề": "",
                    "Định dạng": "",
                    "Nội dung chính": "",
                    "CTA": "",
                    "Người phụ trách": "",
                    "Trạng thái": "Chưa thực hiện",
                    "KPI theo dõi": "",
                }
            )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Đã tạo lịch nội dung với {len(rows)} dòng tại: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
