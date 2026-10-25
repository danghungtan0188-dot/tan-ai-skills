#!/usr/bin/env python3
"""Kiem tra moi trich dan `file:dong` trong tai lieu kien truc co that.

Tai lieu do /quet-kien-truc viet ra ghi nguon dang `src/app.ts:42` hoac
`src/app.ts:42-60` (trong dau backtick). Script nay mo dung file, kiem tra
dong co ton tai va khong rong. Trich dan sai = tai lieu dang bia.

Vi du:
  python scripts/check_citations.py ../du-an/docs/02-ky-thuat/architecture.md --root ../du-an

Exit 0 = moi trich dan dung, 1 = co trich dan sai, 2 = khong co tai lieu
hoac khong co trich dan nao.
"""

import argparse
import re
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

# `duong/dan/file.ext:12` hoac `duong/dan/file.ext:12-30`
CITATION = re.compile(r"`([^`\s:]+\.[A-Za-z0-9]+):(\d+)(?:-(\d+))?`")


def check(doc: Path, root: Path) -> tuple[int, list[str]]:
    """Tra ve (so trich dan, danh sach loi)."""
    errors = []
    found = CITATION.findall(doc.read_text(encoding="utf-8"))
    for path, start, end in found:
        start, end = int(start), int(end or start)
        ref = f"{path}:{start}" + (f"-{end}" if end != start else "")
        target = root / path
        if not target.is_file():
            errors.append(f"{ref} — không có file")
            continue
        lines = target.read_text(encoding="utf-8", errors="replace").splitlines()
        if start < 1 or end < start or end > len(lines):
            errors.append(f"{ref} — file chỉ có {len(lines)} dòng")
        elif not any(lines[i - 1].strip() for i in range(start, end + 1)):
            errors.append(f"{ref} — dòng trống")
    return len(found), errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("doc", type=Path, help="file tai lieu kien truc (.md)")
    parser.add_argument("--root", type=Path,
                        help="goc du an de tinh duong dan (mac dinh: thu muc chua git gan nhat)")
    args = parser.parse_args()

    if not args.doc.is_file():
        print(f"Không thấy tài liệu: {args.doc}")
        return 2
    root = args.root
    if root is None:
        root = next((p for p in args.doc.resolve().parents if (p / ".git").exists()),
                    args.doc.resolve().parent)

    total, errors = check(args.doc, root)
    if total == 0:
        print("Không có trích dẫn `file:dòng` nào — tài liệu chưa dẫn nguồn.")
        return 2
    for e in errors:
        print(f"SAI  {e}")
    print(f"{total - len(errors)}/{total} trích dẫn đúng (gốc: {root})")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
