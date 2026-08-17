#!/usr/bin/env python3
"""Doc du lieu san pham tu file CSV/XLSX va doi chieu anh trong thu muc.

Chi dung thu vien chuan Python (khong can cai openpyxl/pandas).
Doc XLSX: chi doc sheet dau tien, khong ho tro o gop hoac cong thuc
(mo Excel va "Paste as values" hoac xuat CSV neu file co cong thuc).

Vi du:
    python doc_du_lieu_san_pham.py san_pham.csv --list
    python doc_du_lieu_san_pham.py san_pham.csv --ma-san-pham SP001 --images-dir anh/
    python doc_du_lieu_san_pham.py san_pham.xlsx --ten-san-pham "Mat ong rung" --images-dir anh/
"""

import argparse
import csv
import json
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

REQUIRED_COLUMNS = ["ma_san_pham", "ten_san_pham", "mo_ta_ngan", "gia", "ten_file_anh"]
OPTIONAL_COLUMNS = ["tinh_nang_chinh", "gia_khuyen_mai", "cta", "giong_doc", "ghi_chu"]
ALL_COLUMNS = REQUIRED_COLUMNS + OPTIONAL_COLUMNS

NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"


def _tag(name: str) -> str:
    return f"{{{NS_MAIN}}}{name}"


def _col_to_index(cell_ref: str) -> int:
    letters = "".join(ch for ch in cell_ref if ch.isalpha())
    idx = 0
    for ch in letters:
        idx = idx * 26 + (ord(ch.upper()) - ord("A") + 1)
    return idx - 1


def read_csv(path: Path) -> list:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]


def read_xlsx(path: Path) -> list:
    with zipfile.ZipFile(path) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall(_tag("si")):
                text = "".join(t.text or "" for t in si.iter(_tag("t")))
                shared.append(text)

        sheet_names = sorted(
            n for n in z.namelist()
            if n.startswith("xl/worksheets/sheet") and n.endswith(".xml")
        )
        if not sheet_names:
            return []
        sheet_path = "xl/worksheets/sheet1.xml" if "xl/worksheets/sheet1.xml" in sheet_names else sheet_names[0]

        root = ET.fromstring(z.read(sheet_path))
        raw_rows = []
        for row in root.iter(_tag("row")):
            cells = {}
            for c in row.findall(_tag("c")):
                ref = c.get("r")
                if not ref:
                    continue
                col_idx = _col_to_index(ref)
                cell_type = c.get("t")
                v_el = c.find(_tag("v"))
                if v_el is None:
                    is_el = c.find(_tag("is"))
                    if is_el is not None:
                        text = "".join(t.text or "" for t in is_el.iter(_tag("t")))
                        cells[col_idx] = text
                    continue
                val = v_el.text or ""
                if cell_type == "s":
                    try:
                        val = shared[int(val)]
                    except (ValueError, IndexError):
                        val = ""
                cells[col_idx] = val
            if cells:
                max_idx = max(cells)
                raw_rows.append([cells.get(i, "") for i in range(max_idx + 1)])

    if not raw_rows:
        return []

    header = [h.strip() for h in raw_rows[0]]
    data_rows = []
    for r in raw_rows[1:]:
        r = list(r) + [""] * (len(header) - len(r))
        row_dict = {header[i]: r[i] for i in range(len(header)) if header[i]}
        if any(v for v in row_dict.values()):
            data_rows.append(row_dict)
    return data_rows


def load_products(path: Path) -> list:
    if path.suffix.lower() == ".xlsx":
        return read_xlsx(path)
    return read_csv(path)


def validate_row(row: dict) -> list:
    missing = [col for col in REQUIRED_COLUMNS if not (row.get(col) or "").strip()]
    return missing


def check_images(row: dict, images_dir: Path) -> list:
    raw = (row.get("ten_file_anh") or "").strip()
    if not raw:
        return []
    missing = []
    for name in [n.strip() for n in raw.split(";") if n.strip()]:
        if not (images_dir / name).exists():
            missing.append(name)
    return missing


def find_row(rows: list, ma_san_pham: str = None, ten_san_pham: str = None) -> list:
    matches = []
    for row in rows:
        if ma_san_pham and (row.get("ma_san_pham") or "").strip().lower() == ma_san_pham.strip().lower():
            matches.append(row)
        elif ten_san_pham and ten_san_pham.strip().lower() in (row.get("ten_san_pham") or "").strip().lower():
            matches.append(row)
    return matches


def print_row_report(row: dict, images_dir: Path = None) -> bool:
    ok = True
    print(f"--- {row.get('ma_san_pham', '(khong co ma)')} — {row.get('ten_san_pham', '')} ---")
    for col in ALL_COLUMNS:
        val = row.get(col, "")
        marker = "" if val else "  [trong]"
        print(f"  {col}: {val}{marker}")

    missing_required = validate_row(row)
    if missing_required:
        ok = False
        print(f"  CANH BAO: thieu truong bat buoc: {', '.join(missing_required)}")

    if images_dir is not None:
        missing_images = check_images(row, images_dir)
        if missing_images:
            ok = False
            print(f"  CANH BAO: khong tim thay anh trong thu muc: {', '.join(missing_images)}")
        elif row.get("ten_file_anh"):
            print("  Anh: da doi chieu, tat ca ton tai.")

    return ok


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Doc du lieu san pham tu CSV/XLSX, tra 1 san pham va doi chieu anh."
    )
    parser.add_argument("file", type=Path, help="Duong dan file CSV hoac XLSX danh sach san pham.")
    lookup = parser.add_mutually_exclusive_group()
    lookup.add_argument("--ma-san-pham", help="Tra theo ma san pham chinh xac (khong phan biet hoa/thuong).")
    lookup.add_argument("--ten-san-pham", help="Tra theo ten san pham (khop mot phan, khong phan biet hoa/thuong).")
    lookup.add_argument("--list", action="store_true", help="Liet ke toan bo san pham, khong doi chieu anh.")
    parser.add_argument("--images-dir", type=Path, help="Thu muc anh de doi chieu ten_file_anh.")
    parser.add_argument("--output", type=Path, help="Ghi ket qua (JSON) ra file, ngoai viec in ra man hinh.")
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.file.exists():
        print(f"Loi: khong tim thay file {args.file}", file=sys.stderr)
        return 2

    try:
        rows = load_products(args.file)
    except Exception as exc:  # noqa: BLE001 - bao loi doc file ro rang cho nguoi dung
        print(f"Loi doc file: {exc}", file=sys.stderr)
        return 2

    if not rows:
        print("Khong doc duoc dong du lieu nao tu file.", file=sys.stderr)
        return 2

    if args.list:
        print(f"Tong {len(rows)} san pham:")
        for row in rows:
            print(f"  {row.get('ma_san_pham', '?')} — {row.get('ten_san_pham', '?')}")
        return 0

    if not args.ma_san_pham and not args.ten_san_pham:
        parser.error("Can --ma-san-pham hoac --ten-san-pham (hoac dung --list de xem toan bo).")

    matches = find_row(rows, ma_san_pham=args.ma_san_pham, ten_san_pham=args.ten_san_pham)

    if not matches:
        print("Khong tim thay san pham nao khop. Kiem tra lai ma/ten hoac dung --list.", file=sys.stderr)
        return 1

    if len(matches) > 1:
        print(f"Tim thay {len(matches)} san pham khop — can chi dinh ro hon:", file=sys.stderr)
        for row in matches:
            print(f"  {row.get('ma_san_pham', '?')} — {row.get('ten_san_pham', '?')}", file=sys.stderr)
        return 1

    row = matches[0]
    ok = print_row_report(row, images_dir=args.images_dir)

    if args.output:
        args.output.write_text(json.dumps(row, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Da ghi JSON: {args.output}")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
