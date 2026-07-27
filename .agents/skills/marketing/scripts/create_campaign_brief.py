#!/usr/bin/env python3
"""Tao khung marketing brief (Markdown) tu tham so dong lenh."""

import argparse
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

BRIEF_TEMPLATE = """# Marketing Brief

## 1. Thông tin thương hiệu

- Tên thương hiệu: {brand}
- Ngành hàng: {industry}
- Giọng điệu thương hiệu: {tone}

## 2. Sản phẩm/dịch vụ

- Tên sản phẩm/dịch vụ: {product}
- Mô tả ngắn: {product_desc}

## 3. Mục tiêu marketing

- Mục tiêu chính (SMART): {goal}

## 4. Khách hàng mục tiêu

- Mô tả sơ bộ: {audience}

## 5. Thị trường và bối cảnh

- Khu vực triển khai: {region}

## 6. Kênh truyền thông

- Kênh ưu tiên: {channels}

## 7. Thời gian thực hiện

- Ngày bắt đầu: {start_date}
- Ngày kết thúc: {end_date}

## 8. Ngân sách

- Tổng ngân sách: {budget}

## 9. Ràng buộc khác

- Ràng buộc: {constraints}

## 10. KPI mong muốn

- Chỉ số chính: {kpi}

## Giả định đã sử dụng

{assumptions}
"""

CHUA_XAC_DINH = "Chưa xác định"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="create_campaign_brief.py",
        description=(
            "Tao nhanh khung marketing brief dang Markdown tu thong tin "
            "duoc cung cap qua tham so dong lenh. Muc nao khong duoc "
            "cung cap se duoc ghi la 'Chua xac dinh'."
        ),
    )
    parser.add_argument("--brand", default=CHUA_XAC_DINH, help="Tên thương hiệu")
    parser.add_argument("--product", default=CHUA_XAC_DINH, help="Tên sản phẩm/dịch vụ")
    parser.add_argument("--product-desc", dest="product_desc", default=CHUA_XAC_DINH, help="Mô tả ngắn sản phẩm/dịch vụ")
    parser.add_argument("--industry", default=CHUA_XAC_DINH, help="Ngành hàng")
    parser.add_argument("--tone", default=CHUA_XAC_DINH, help="Giọng điệu thương hiệu")
    parser.add_argument("--goal", default=CHUA_XAC_DINH, help="Mục tiêu marketing chính (nên viết theo SMART)")
    parser.add_argument("--audience", default=CHUA_XAC_DINH, help="Mô tả khách hàng mục tiêu")
    parser.add_argument("--region", default=CHUA_XAC_DINH, help="Khu vực triển khai")
    parser.add_argument("--channels", default=CHUA_XAC_DINH, help="Danh sách kênh, phân tách bằng dấu phẩy")
    parser.add_argument("--start-date", dest="start_date", default=CHUA_XAC_DINH, help="Ngày bắt đầu (YYYY-MM-DD)")
    parser.add_argument("--end-date", dest="end_date", default=CHUA_XAC_DINH, help="Ngày kết thúc (YYYY-MM-DD)")
    parser.add_argument("--budget", default=CHUA_XAC_DINH, help="Tổng ngân sách dự kiến")
    parser.add_argument("--constraints", default=CHUA_XAC_DINH, help="Ràng buộc pháp lý/ngành hoặc nội dung cần tránh")
    parser.add_argument("--kpi", default=CHUA_XAC_DINH, help="Chỉ số KPI chính mong muốn theo dõi")
    parser.add_argument("-o", "--output", default=None, help="Đường dẫn file Markdown để ghi kết quả (mặc định in ra màn hình)")
    parser.add_argument("--force", action="store_true", help="Cho phép ghi đè nếu file --output đã tồn tại")
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    missing = [
        name
        for name, value in (
            ("brand", args.brand),
            ("product", args.product),
            ("goal", args.goal),
            ("audience", args.audience),
        )
        if value == CHUA_XAC_DINH
    ]
    assumptions_lines = []
    if missing:
        assumptions_lines.append(
            "- Chưa cung cấp: " + ", ".join(missing) + ". Cần xác nhận lại trước khi dùng brief này để ra quyết định."
        )
    else:
        assumptions_lines.append("- Không có giả định nào; toàn bộ thông tin cốt lõi đã được cung cấp.")

    content = BRIEF_TEMPLATE.format(
        brand=args.brand,
        product=args.product,
        product_desc=args.product_desc,
        industry=args.industry,
        tone=args.tone,
        goal=args.goal,
        audience=args.audience,
        region=args.region,
        channels=args.channels,
        start_date=args.start_date,
        end_date=args.end_date,
        budget=args.budget,
        constraints=args.constraints,
        kpi=args.kpi,
        assumptions="\n".join(assumptions_lines),
    )

    if args.output:
        output_path = Path(args.output)
        if output_path.exists() and not args.force:
            print(
                f"Lỗi: file '{output_path}' đã tồn tại. Dùng --force để ghi đè.",
                file=sys.stderr,
            )
            return 1
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
        print(f"Đã tạo brief tại: {output_path}")
    else:
        print(content)

    return 0


if __name__ == "__main__":
    sys.exit(main())
