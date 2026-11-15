"""Sửa âm "tr" cho VieNeu-TTS (dùng qua `synthesize.py --sua-tr`).

Gốc lỗi: bộ phiên âm sea-g2p của VieNeu đổi cả "tr" và "ch" thành cùng một âm `tʃ`,
nên đọc bao nhiêu lần "trợ" vẫn ra "chợ". Truyền phoneme_dict thì bị bỏ qua, nên sửa
chuỗi phiên âm SAU khi tạo: từ bắt đầu bằng "tr" → đổi `tʃ` đầu tiên thành `tɹ`
(t + r kiểu "tree"), gần âm "tr" uốn lưỡi hơn. Số từ và số cụm phiên âm khớp 1-1;
lệch thì giữ nguyên câu (an toàn hơn đoán).

Bản tin 13/11/2026: V3 Turbo gọi `phonemize_text_with_emotions`, không gọi
`phonemize_batch` — phải vá đúng hàm engine dùng, rồi `kiem_engine` xác nhận.
"""

from __future__ import annotations

import re
import sys
import unicodedata

_TEN_HAM = ("phonemize_batch", "phonemize_with_dict", "phonemize_text_with_emotions")
_DAU = ",.;:!?"


def _khoa(tu: str) -> str:
    return re.sub(r"[^\w]", "", unicodedata.normalize("NFC", tu.lower()))


def la_tr(tu: str) -> bool:
    return _khoa(tu).startswith("tr")


def sua(text: str, ph: str, pho_thay: dict | None = None) -> str:
    """Sửa chuỗi phiên âm `ph` của câu `text`.

    pho_thay: ép phiên âm riêng cho từ giọng này đọc sai, vd {"văn": "vˈan"}.
    """
    a, b = text.split(), ph.split()
    if len(a) != len(b):
        print("CANH BAO lệch số từ, giữ nguyên phiên âm:", text, file=sys.stderr, flush=True)
        return ph
    ra = []
    for tu, am in zip(a, b):
        k = _khoa(tu)
        if pho_thay and k in pho_thay:
            am = pho_thay[k] + "".join(c for c in am if c in _DAU)
        elif la_tr(tu):
            am = am.replace("tʃ", "tɹ", 1)
        ra.append(am)
    return " ".join(ra)


_goc: dict = {}
_moi: dict = {}


def va_phien_am(pho_thay: dict | None = None) -> None:
    """Vá 3 hàm phiên âm ở vieneu_utils.phonemize_text và mọi module vieneu đã `from ... import`.

    Gọi lại sau khi khởi tạo Vieneu(): engine nạp module của nó lúc khởi tạo.
    """
    import vieneu_utils.phonemize_text as pt

    if not _goc:
        _goc.update({ten: getattr(pt, ten) for ten in _TEN_HAM})
        g = _goc
        _moi["phonemize_batch"] = lambda texts, *a, **k: [
            sua(t, p, pho_thay) for t, p in zip(texts, g["phonemize_batch"](texts, *a, **k))]
        _moi["phonemize_with_dict"] = lambda text, *a, **k: sua(text, g["phonemize_with_dict"](text, *a, **k), pho_thay)
        _moi["phonemize_text_with_emotions"] = lambda text, *a, **k: sua(
            text, g["phonemize_text_with_emotions"](text, *a, **k), pho_thay)
    for ten, m in list(sys.modules.items()):
        if m is None or not (ten.startswith("vieneu") or m is pt):
            continue
        for ham in _TEN_HAM:
            if getattr(m, ham, None) is _goc[ham]:
                setattr(m, ham, _moi[ham])


def kiem_engine(tts) -> str:
    """Khẳng định module của engine đang gọi hàm đã vá; trả phiên âm mẫu để in ra log."""
    m = sys.modules[type(tts).__module__]
    for ham in ("phonemize_text_with_emotions", "phonemize_batch"):
        if hasattr(m, ham):
            assert getattr(m, ham) is _moi[ham], f"engine {type(tts).__name__} chưa dùng {ham} đã vá"
    return _moi["phonemize_text_with_emotions"]("nguồn hỗ trợ")
