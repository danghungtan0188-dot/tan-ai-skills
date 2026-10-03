"""Chuẩn hoá script tiếng Việt cho TTS, có ghi vết từng thay đổi.

Mỗi quy tắc có id + lý do; bật/tắt bằng `tat_quy_tac`. Văn bản gốc luôn được giữ.
Chỗ không chắc cách đọc thì KHÔNG đoán: để nguyên và gắn cờ `can_xem_lai`.
Logic số/ngày/viết tắt nằm ở skill tan-giong-doc-ban-tin (normalize_vi.py) — ở đây chỉ gọi lại.
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

from . import DATA, now, read_json

import normalize_vi  # noqa: E402  (skills/tan-giong-doc-ban-tin/scripts)
import read_script  # noqa: E402

CONFIG = read_json(DATA / "chuan_hoa.json", {})

_UNICODE_MAP = {" ": " ", "​": "", "‌": "", "‍": "", "﻿": "",
                "“": '"', "”": '"', "‘": "'", "’": "'", "…": "..."}


def _unicode(text: str, log: list) -> str:
    out = unicodedata.normalize("NFC", text)
    if out != text:
        log.append({"quy_tac": "unicode", "tu": "(dấu tổ hợp)", "thanh": "NFC",
                    "ly_do": "gộp dấu tiếng Việt về một dạng chuẩn"})
    for src, dst in _UNICODE_MAP.items():
        if src in out:
            log.append({"quy_tac": "unicode", "tu": repr(src), "thanh": repr(dst),
                        "ly_do": "ký tự đặc biệt dễ làm TTS đọc lạ"})
            out = out.replace(src, dst)
    return out


def _regex(rule_id: str, reason: str, regex: re.Pattern, repl):
    def apply(text: str, log: list) -> str:
        def cb(m: re.Match) -> str:
            out = repl(m) if callable(repl) else m.expand(repl)
            if out != m.group(0):
                log.append({"quy_tac": rule_id, "tu": m.group(0), "thanh": out, "ly_do": reason})
            return out
        return regex.sub(cb, text)
    return apply


def _chain(*steps):
    def apply(text: str, log: list) -> str:
        for step in steps:
            text = step(text, log)
        return text
    return apply


def _pronunciations(entries: list[dict]):
    steps = [_regex("phat_am", f"quy tắc đã duyệt {e.get('id', '?')} v{e.get('phien_ban', '?')} ({e.get('pham_vi', '?')})",
                    re.compile(rf"(?<!\w){re.escape(e['tu'])}(?!\w)"), lambda m, d=e["doc_thanh"]: d)
             for e in entries]
    return _chain(*steps)


def _abbreviations():
    steps = []
    for rule in normalize_vi.load_rules():
        regex, repl = normalize_vi._compile_rule(rule)
        steps.append(_regex("viet_tat", f"từ điển viết tắt: {rule['pattern']}", regex, repl))
    return _chain(*steps)


def build_rules(phat_am: list[dict]) -> list[dict]:
    """Danh sách quy tắc theo thứ tự chạy. Phát âm người dùng chạy trước để ghi đè."""
    rules = [
        {"id": "unicode", "mo_ta": "NFC, bỏ ký tự vô hình, đổi ngoặc kép cong/dấu ba chấm", "apply": _unicode},
        {"id": "khoang_trang", "mo_ta": "gộp khoảng trắng, bỏ khoảng trắng trước dấu câu, thêm sau dấu phẩy",
         "apply": _chain(
             _regex("khoang_trang", "khoảng trắng thừa", re.compile(r"[ \t]{2,}"), " "),
             _regex("khoang_trang", "khoảng trắng trước dấu câu", re.compile(r"[ \t]+([,.;:!?])"), r"\1"),
             _regex("khoang_trang", "thiếu khoảng trắng sau dấu câu",
                    re.compile(r"([,;!?])(?=[^\s\d\"')\]])"), r"\1 "))},
        {"id": "phat_am", "mo_ta": "từ điển phát âm đã được người dùng duyệt (tên riêng, từ mượn)",
         "apply": _pronunciations(phat_am)},
        {"id": "viet_tat", "mo_ta": "từ điển viết tắt của skill (references/abbreviations.json)",
         "apply": _abbreviations()},
    ]
    for rule_id, reason, regex, fn in normalize_vi.NUMBER_RULES:
        rules.append({"id": rule_id, "mo_ta": reason, "apply": _regex(rule_id, reason, regex, fn)})
    return rules


def _flags(normalized: str) -> list[dict]:
    flags, seen = [], set()

    def add(kind, token, reason):
        if (kind, token) not in seen:
            seen.add((kind, token))
            flags.append({"loai": kind, "doan": token, "ly_do": reason})

    for tok in re.findall(r"\S*\d\S*", normalized):
        add("can_xem_lai", tok.strip(".,;:!?()\""),
            "còn chữ số: dạng mơ hồ nên không tự đoán cách đọc — viết lại bằng chữ hoặc thêm từ điển phát âm")
    for tok in re.findall(r"\w+", normalized):
        if sum(c.isupper() for c in tok) >= 2:
            add("can_xem_lai", tok, "chữ viết tắt chưa có trong từ điển — TTS sẽ tự đánh vần")
    for word, reason in CONFIG.get("tu_kho_tts", {}).items():
        if re.search(rf"(?<!\w){re.escape(word)}(?!\w)", normalized, re.IGNORECASE):
            add("tu_kho_tts", word, reason)
    return flags


def normalize_text(text: str, tat_quy_tac=(), phat_am: list[dict] | None = None) -> dict:
    """phat_am: quy tắc phát âm đang bật (rules.active_pronunciations), hẹp trước rộng sau."""
    rules = build_rules(list(phat_am or []))
    unknown = set(tat_quy_tac) - {r["id"] for r in rules}
    if unknown:
        raise ValueError(f"Không có quy tắc: {sorted(unknown)}. Xem: python -m tan_studio quy-tac")
    log: list = []
    out = text
    for rule in rules:
        if rule["id"] not in tat_quy_tac:
            out = rule["apply"](out, log)
    out = re.sub(r"[ \t]{2,}", " ", out).strip()
    return {"original": text, "normalized": out, "changes": log, "flags": _flags(out)}


PAUSE = re.compile(r"\[\s*nghỉ\s+(\d+(?:[.,]\d+)?)\s*(ms|s)\s*\]", re.IGNORECASE)
PAUSE_MAX_MS = 10_000


def split_pauses(paragraph: str) -> list[tuple[int | None, str]]:
    """'A [nghỉ 2s] B' -> [(None, 'A'), (2000, 'B')]: số mili-giây lặng TRƯỚC mỗi khúc.

    Khúc rỗng (thẻ ở đầu/cuối, hai thẻ liền nhau) bị bỏ, khoảng lặng cộng dồn sang khúc sau;
    thẻ ở cuối đoạn văn trả (ms, '') để đoạn văn sau nhận. Tối đa 10 giây mỗi thẻ.
    """
    parts = PAUSE.split(unicodedata.normalize("NFC", paragraph))
    out, pending = [], None
    for i in range(0, len(parts), 3):
        text = parts[i].strip()
        if text:
            out.append((pending, text))
            pending = None
        if i + 2 < len(parts):
            ms = float(parts[i + 1].replace(",", ".")) * (1 if parts[i + 2].lower() == "ms" else 1000)
            pending = (pending or 0) + min(int(ms), PAUSE_MAX_MS)
    if pending is not None:
        out.append((pending, ""))
    return out


def normalize_script(source, tat_quy_tac=(), phat_am: list[dict] | None = None) -> dict:
    """source: đường dẫn .txt/.docx hoặc chuỗi văn bản. Trả NormalizedScript.

    Thẻ `[nghỉ 2s]` / `[nghỉ 500ms]` tách đoạn; đoạn sau thẻ có `nghi_truoc_ms` (thay khoảng lặng mặc định).
    """
    if isinstance(source, Path) or (isinstance(source, str) and Path(source).suffix.lower() in {".txt", ".docx"}):
        path = Path(source)
        paragraphs = read_script.read_script(path)
        src = str(path)
    else:
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", str(source)) if p.strip()]
        src = None
    segments, pending = [], None
    for para in paragraphs:
        for ms, text in split_pauses(para):
            if ms is not None:
                pending = (pending or 0) + ms
            if not text:
                continue
            seg = {"index": len(segments) + 1, **normalize_text(text, tat_quy_tac, phat_am)}
            if pending is not None:
                seg["nghi_truoc_ms"] = pending
                pending = None
            segments.append(seg)
    return {
        "kind": "NormalizedScript",
        "source": src,
        "created_at": now(),
        "disabled_rules": sorted(tat_quy_tac),
        "segments": segments,
        "original_text": "\n\n".join(s["original"] for s in segments),
        "normalized_text": "\n\n".join(s["normalized"] for s in segments),
    }


def list_rules() -> list[tuple[str, str]]:
    return [(r["id"], r["mo_ta"]) for r in build_rules([])]
