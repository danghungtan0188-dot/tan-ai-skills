#!/usr/bin/env python3
"""Kiem ban yeu cau edit/brief.json cua lenh /dung-video khop VideoBrief (data-contracts/video.schema.json).

  python scripts/kiem_brief.py <thu muc tu lieu>/edit/brief.json

Exit 0 = khop; 1 = sai (in tung loi + danh sach truong dung); 2 = khong doc duoc file.
"""

import json
import sys
from pathlib import Path

import jsonschema

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

SCHEMA = Path(__file__).resolve().parents[1] / "data-contracts" / "video.schema.json"


def loi(brief: object) -> list[str]:
    defs = json.loads(SCHEMA.read_text(encoding="utf-8"))["$defs"]
    v = jsonschema.Draft202012Validator({"$ref": "#/$defs/VideoBrief", "$defs": defs})
    return [f"{'/'.join(map(str, e.absolute_path)) or '(goc)'}: {e.message}"
            for e in sorted(v.iter_errors(brief), key=lambda e: list(map(str, e.absolute_path)))]


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        brief = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"Khong doc duoc {sys.argv[1]}: {exc}", file=sys.stderr)
        return 2
    sai = loi(brief)
    if not sai:
        print("brief OK")
        return 0
    truong = json.loads(SCHEMA.read_text(encoding="utf-8"))["$defs"]["VideoBrief"]["properties"]
    print("brief SAI hop dong VideoBrief:")
    for dong in sai:
        print(f"  - {dong}")
    print("Chi dung dung cac truong: " + ", ".join(truong))
    print("Sua edit/brief.json roi chay lai. Chua OK thi KHONG sang buoc 2.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
