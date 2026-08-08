#!/usr/bin/env python3
"""Chuan hoa van ban tieng Viet truoc khi dua vao VieNeu-TTS.

Pham vi CHI trong file nay: mo rong chu viet tat theo tu dien co the chinh sua
(references/abbreviations.json). Con so va ngay thang KHONG duoc xu ly o day —
thu vien vieneu (qua sea-g2p) da tu dong doc so/ngay thanh chu khi goi
vieneu.infer(...), lam lai o day se gay xung dot / doc sai hai lan.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Optional

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

DEFAULT_DICT_PATH = Path(__file__).resolve().parent.parent / "references" / "abbreviations.json"


class NormalizeError(RuntimeError):
    pass


def load_rules(dict_path: Optional[Path] = None) -> List[dict]:
    path = dict_path or DEFAULT_DICT_PATH
    if not path.exists():
        raise NormalizeError(f"Khong tim thay tu dien viet tat: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise NormalizeError(f"Tu dien viet tat bi loi cu phap JSON ({path}): {exc}") from exc

    rules = data.get("rules", [])
    if not isinstance(rules, list):
        raise NormalizeError(f"Truong 'rules' trong {path} phai la mot danh sach.")
    return rules


def _compile_rule(rule: dict) -> tuple[re.Pattern, str]:
    pattern = rule.get("pattern")
    replacement = rule.get("replacement", "")
    if not pattern:
        raise NormalizeError(f"Muc quy tac thieu 'pattern': {rule}")
    whole_word = rule.get("whole_word", False)
    regex_src = rf"\b(?:{pattern})\b" if whole_word else pattern
    try:
        return re.compile(regex_src), replacement
    except re.error as exc:
        raise NormalizeError(f"Regex khong hop le trong quy tac {rule}: {exc}") from exc


def expand_abbreviations(text: str, rules: Optional[List[dict]] = None) -> str:
    """Ap dung tung quy tac viet tat theo thu tu; tra ve van ban da mo rong."""
    compiled_rules = [_compile_rule(r) for r in (rules if rules is not None else load_rules())]
    out = text
    for regex, replacement in compiled_rules:
        out = regex.sub(replacement, out)
    # Don khoang trang thua do thay the sinh ra (VD "TP. " -> "Thành phố  ")
    out = re.sub(r"[ \t]{2,}", " ", out)
    return out.strip()


def _main() -> int:
    parser = argparse.ArgumentParser(
        description="Mo rong chu viet tat tieng Viet theo tu dien references/abbreviations.json."
    )
    parser.add_argument("text", nargs="?", help="Van ban can chuan hoa (bo qua de doc tu stdin)")
    parser.add_argument("--dict", dest="dict_path", default=None, help="Duong dan tu dien JSON tuy chinh")
    args = parser.parse_args()

    text = args.text if args.text is not None else sys.stdin.read()
    if not text.strip():
        print("LOI: khong co van ban dau vao.", file=sys.stderr)
        return 2

    try:
        rules = load_rules(Path(args.dict_path) if args.dict_path else None)
        result = expand_abbreviations(text, rules)
    except NormalizeError as exc:
        print(f"LOI: {exc}", file=sys.stderr)
        return 2

    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(_main())
