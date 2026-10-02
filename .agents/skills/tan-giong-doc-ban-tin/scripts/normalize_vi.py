#!/usr/bin/env python3
"""Chuan hoa van ban tieng Viet truoc khi dua vao VieNeu-TTS.

Hai buoc, theo thu tu:
1. Mo rong chu viet tat theo tu dien (references/abbreviations.json).
2. Doi so, ngay thang, phan tram thanh chu. Bo chuan hoa so cua vieneu doc sai
   that ("22-5-2003" -> "22 tháng 5203", "1402 ngày 26" dinh thanh mot so), nen
   tu doi o day; sau buoc nay van ban khong con chu so de thu vien doc lai.
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


_DIGITS = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
_GROUPS = ["", " nghìn", " triệu"]


def _read_triple(n: int, full: bool) -> str:
    """Doc so 0-999. full=True: doc ca 'không trăm', 'lẻ' (nhom dung sau nhom khac)."""
    h, t, u = n // 100, n // 10 % 10, n % 10
    words = []
    if full or h:
        words.append(f"{_DIGITS[h]} trăm")
    if t == 0:
        if u:
            words.append(f"lẻ {_DIGITS[u]}" if words else _DIGITS[u])
    elif t == 1:
        words.append("mười" + {0: "", 5: " lăm"}.get(u, f" {_DIGITS[u]}"))
    else:
        words.append(f"{_DIGITS[t]} mươi" + {0: "", 1: " mốt", 4: " tư", 5: " lăm"}.get(u, f" {_DIGITS[u]}"))
    return " ".join(words)


def number_to_words(n: int, full: bool = False) -> str:
    if n == 0:
        return "không"
    if n >= 1_000_000_000:
        head, rest = divmod(n, 1_000_000_000)
        return f"{number_to_words(head)} tỷ" + (f" {number_to_words(rest, True)}" if rest else "")
    parts = []
    for idx, g in zip((2, 1, 0), (n // 1_000_000, n // 1000 % 1000, n % 1000)):
        if g:
            parts.append(_read_triple(g, full or bool(parts)) + _GROUPS[idx])
    return " ".join(parts)


def _digits_or_number(s: str) -> str:
    """'0909' doc tung chu so; con lai doc nhu so."""
    if len(s) > 1 and s.startswith("0"):
        return " ".join(_DIGITS[int(c)] for c in s)
    return number_to_words(int(s))


def _month(m: int) -> str:
    return "tư" if m == 4 else number_to_words(m)


_FULL_DATE = re.compile(r"\b(\d{1,2})([/.-])(\d{1,2})\2(\d{4})\b")
_DAY_MONTH = re.compile(r"(?<=ngày )(\d{1,2})[/-](\d{1,2})\b(?![/.-]\d)")
_MONTH_YEAR = re.compile(r"(?<=tháng )(\d{1,2})/(\d{4})\b")
_NUMBER = re.compile(r"(\d{1,3}(?:\.\d{3})+(?![\d.])|\d+(?:,\d+)?)(\s?%)?")


def normalize_numbers(text: str) -> str:
    """Doi ngay thang, so, so thap phan, phan tram thanh chu."""

    def full_date(m: re.Match) -> str:
        d, mo, y = int(m.group(1)), int(m.group(3)), int(m.group(4))
        if not (1 <= d <= 31 and 1 <= mo <= 12):
            return m.group(0)
        prefix = "" if text[: m.start()].endswith("ngày ") else "ngày "
        return f"{prefix}{number_to_words(d)} tháng {_month(mo)} năm {number_to_words(y)}"

    out = _FULL_DATE.sub(full_date, text)
    out = _DAY_MONTH.sub(lambda m: f"{number_to_words(int(m.group(1)))} tháng {_month(int(m.group(2)))}", out)
    out = _MONTH_YEAR.sub(lambda m: f"{_month(int(m.group(1)))} năm {number_to_words(int(m.group(2)))}", out)

    def number(m: re.Match) -> str:
        raw = m.group(1)
        if "," in raw:
            whole, frac = raw.split(",")
            words = f"{_digits_or_number(whole)} phẩy {_digits_or_number(frac)}"
        else:
            words = _digits_or_number(raw.replace(".", ""))
        return words + (" phần trăm" if m.group(2) else "")

    return _NUMBER.sub(number, out)


def normalize_text(text: str, rules: Optional[List[dict]] = None) -> str:
    """Viet tat truoc (vi co quy tac nhu 'Q.5'), roi toi so."""
    return normalize_numbers(expand_abbreviations(text, rules))


def _main() -> int:
    parser = argparse.ArgumentParser(
        description="Mo rong chu viet tat (references/abbreviations.json) roi doi so/ngay thanh chu."
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
        result = normalize_text(text, rules)
    except NormalizeError as exc:
        print(f"LOI: {exc}", file=sys.stderr)
        return 2

    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(_main())
