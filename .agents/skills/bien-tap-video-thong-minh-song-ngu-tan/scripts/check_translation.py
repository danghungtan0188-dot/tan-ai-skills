#!/usr/bin/env python3
"""Kiểm máy bản dịch trong bilingual.json: thuật ngữ, số liệu, câu chưa dịch.

    python check_translation.py bilingual.json [--glossary references/glossary-vi-en.csv] [--strict]

- Thuật ngữ: câu Việt có từ trong glossary thì câu Anh phải có một bản dịch được chấp nhận.
  Từ dài khớp trước ("Phó Chủ tịch UBND xã" trước "Chủ tịch UBND xã").
- Số liệu: mọi con số trong câu Việt phải có mặt trong câu Anh (2.500 = 2,500; tháng 9 = September).
- Chưa dịch: câu Anh rỗng hoặc trùng câu Việt.

Đây chỉ là lưới lọc lỗi máy bắt được. Cờ needs_review chỉ được tắt sau khi người rà xong.
"""
from __future__ import annotations
import argparse
import csv
import json
import re
import unicodedata
from pathlib import Path

MAC_DINH = Path(__file__).resolve().parents[1] / "references" / "glossary-vi-en.csv"
THANG = {m: i for i, m in enumerate(
    "january february march april may june july august september october november december".split(), 1)}
THANG |= {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6, "jul": 7, "aug": 8,
          "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12}
SO_CHU = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve".split())}


def chuan(s: str) -> str:
    return unicodedata.normalize("NFC", s).lower()


def doc_glossary(path: Path) -> list[tuple[list[str], list[str]]]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append(([chuan(x) for x in r["vi"].split("|")], [chuan(x) for x in r["en"].split("|")]))
    return sorted(rows, key=lambda r: -max(map(len, r[0])))


def so_viet(s: str) -> set[str]:
    return set(re.findall(r"\d+", re.sub(r"(?<=\d)\.(?=\d{3}\b)", "", s)))


def so_anh(s: str) -> set[str]:
    kq = set(re.findall(r"\d+", re.sub(r"(?<=\d),(?=\d{3}\b)", "", s)))
    for tu in re.findall(r"[a-z]+", s):
        if tu in THANG:
            kq.add(str(THANG[tu]))
        if tu in SO_CHU:
            kq.add(str(SO_CHU[tu]))
    return kq


def check(segs: list[dict], glossary: list) -> list[str]:
    canh_bao = []
    for n, s in enumerate(segs, 1):
        vi, en = chuan(s.get("vi", "")), chuan(s.get("en", ""))
        if not en.strip() or en == vi:
            canh_bao.append(f"cue {n}: chưa dịch — {s.get('vi', '')[:40]}")
            continue
        con = vi
        for vi_alt, en_alt in glossary:
            khop = next((x for x in vi_alt if x in con), None)
            if not khop:
                continue
            if not any(e in en for e in en_alt):
                canh_bao.append(f"cue {n}: thuật ngữ '{khop}' → cần '{en_alt[0]}' | EN: {s['en'][:50]}")
            con = con.replace(khop, " " * len(khop))
        thieu = so_viet(vi) - so_anh(en)
        if thieu:
            canh_bao.append(f"cue {n}: số liệu {sorted(thieu)} không có trong câu Anh | {s['en'][:50]}")
    return canh_bao


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("--glossary", type=Path, default=MAC_DINH)
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    data = json.loads(a.input.read_text(encoding="utf-8"))
    canh_bao = check(data.get("segments", []), doc_glossary(a.glossary))
    for x in canh_bao:
        print("CẢNH BÁO ", x)
    if data.get("meta", {}).get("needs_review", True):
        print("GHI CHÚ   needs_review=true — bản dịch chưa được người rà, không báo là đã chính xác.")
    print(f"{len(data.get('segments', []))} cue, {len(canh_bao)} cảnh báo")
    return 1 if (a.strict and canh_bao) else 0


if __name__ == "__main__":
    raise SystemExit(main())
