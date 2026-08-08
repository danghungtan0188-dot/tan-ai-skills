#!/usr/bin/env python3
"""Doc kich ban tieng Viet tu file .txt hoac .docx, tach thanh danh sach doan van.

Khong phu thuoc vieneu. Chi dung thu vien chuan + python-docx (cho .docx).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


class ScriptReadError(RuntimeError):
    pass


def _read_txt(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1258", "cp1252"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise ScriptReadError(
        f"Khong doc duoc file TXT (thu utf-8-sig/utf-8/cp1258/cp1252 deu loi): {path}"
    )


def _read_docx(path: Path) -> str:
    try:
        import docx  # python-docx
    except ImportError as exc:
        raise ScriptReadError(
            "Thieu thu vien 'python-docx'. Cai bang: pip install python-docx"
        ) from exc

    try:
        document = docx.Document(str(path))
    except Exception as exc:  # package raises various exceptions for bad files
        raise ScriptReadError(f"File DOCX khong doc duoc hoac bi hong: {path} ({exc})") from exc

    lines: List[str] = []
    for para in document.paragraphs:
        lines.append(para.text)
    return "\n".join(lines)


def split_paragraphs(text: str) -> List[str]:
    """Tach van ban thanh cac doan (ngan cach boi dong trong), bo doan rong."""
    raw_paragraphs = text.replace("\r\n", "\n").replace("\r", "\n").split("\n\n")
    paragraphs: List[str] = []
    for block in raw_paragraphs:
        # Trong mot "doan", vẫn co the co xuong dong don (VD tieu de + body) -> gop lai bang khoang trang.
        joined = " ".join(line.strip() for line in block.split("\n") if line.strip())
        if joined:
            paragraphs.append(joined)
    return paragraphs


def read_script(path: str | Path) -> List[str]:
    """Doc file kich ban va tra ve danh sach doan van khong rong.

    Ho tro .txt va .docx. Nem ScriptReadError voi thong bao ro rang khi that bai.
    """
    p = Path(path)
    if not p.exists():
        raise ScriptReadError(f"Khong tim thay file kich ban: {p}")
    if p.is_dir():
        raise ScriptReadError(f"Duong dan la thu muc, khong phai file: {p}")

    suffix = p.suffix.lower()
    if suffix == ".txt":
        text = _read_txt(p)
    elif suffix == ".docx":
        text = _read_docx(p)
    elif suffix == ".doc":
        raise ScriptReadError(
            "File .doc (Word cu) khong duoc ho tro. Hay luu lai sang .docx hoac .txt roi thu lai."
        )
    else:
        raise ScriptReadError(
            f"Dinh dang '{suffix}' khong duoc ho tro. Chi ho tro .txt va .docx."
        )

    paragraphs = split_paragraphs(text)
    if not paragraphs:
        raise ScriptReadError(f"File khong co noi dung van ban nao co the doc duoc: {p}")
    return paragraphs


def _main() -> int:
    parser = argparse.ArgumentParser(
        description="Doc kich ban TXT/DOCX va in danh sach doan van (dung de kiem tra nhanh)."
    )
    parser.add_argument("input", help="Duong dan file .txt hoac .docx")
    args = parser.parse_args()

    try:
        paragraphs = read_script(args.input)
    except ScriptReadError as exc:
        print(f"LOI: {exc}", file=sys.stderr)
        return 2

    print(f"Doc duoc {len(paragraphs)} doan tu: {args.input}\n")
    for i, para in enumerate(paragraphs, 1):
        preview = para if len(para) <= 120 else para[:117] + "..."
        print(f"[{i:02d}] ({len(para)} ky tu) {preview}")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
