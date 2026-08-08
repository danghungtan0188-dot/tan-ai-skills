#!/usr/bin/env python3
"""Quan ly noi luu giong da nhan ban va danh muc giong dung san cua VieNeu-TTS.

QUAN TRONG: script nay KHONG dung ham vieneu.save_voices() theo duong dan mac
dinh cua no, vi mac dinh no se GHI DE vao file JSON nam BEN TRONG goi vieneu da
cai (site-packages/vieneu/assets/voices_v3_turbo.json). Ghi vao do vua kho quan
ly vua se MAT du lieu moi khi `pip install --upgrade vieneu`. Thay vao do, giong
nhan ban cua nguoi dung duoc luu o thu muc rieng cua skill nay va duoc NAP LAI
vao doi tuong Vieneu() luc chay bang cach hop nhat vao thuoc tinh
`_preset_voices` (thuoc tinh du lieu cong khai cua doi tuong, khong phai sua
ma nguon thu vien).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

# Thu muc du lieu rieng cua skill — KHONG nam trong site-packages / thu muc cai vieneu.
SKILL_DATA_DIR = Path.home() / ".tan-giong-doc-ban-tin"
VOICES_DIR = SKILL_DATA_DIR / "voices"
CUSTOM_VOICES_FILE = VOICES_DIR / "giong_cua_toi.json"
DEFAULT_OUTPUT_DIR = Path("outputs")

# Hai giong "nam mien Nam" / "nu mien Nam" phong cach tin tuc, dung san trong
# VieNeu-TTS-v3-Turbo (xem references/voices.md) — dung cho --voice nam / --voice nu.
VOICE_SHORTCUTS: Dict[str, str] = {
    "nam": "Minh Triết",
    "nu": "Thùy Dung",
    "nam-mien-nam": "Minh Triết",
    "nu-mien-nam": "Thùy Dung",
    "nam-tin-tuc": "Minh Triết",
    "nu-tin-tuc": "Thùy Dung",
}

# Danh muc 14 giong dung san cua VieNeu-TTS-v3-Turbo (chi de tra cuu/hien thi —
# khong dung de tong hop, du lieu am thanh that nam trong goi vieneu da cai).
BUILTIN_VOICE_CATALOG: List[Dict[str, str]] = [
    {"name": "Minh Đức", "gender": "nam", "region": "Bắc", "style": "tin_tuc"},
    {"name": "Phạm Tuyên", "gender": "nam", "region": "Bắc", "style": "tu_nhien"},
    {"name": "Thanh Bình", "gender": "nam", "region": "Bắc", "style": "doc_truyen"},
    {"name": "Trúc Ly", "gender": "nữ", "region": "Bắc", "style": "tu_nhien"},
    {"name": "Ngọc Linh", "gender": "nữ", "region": "Bắc", "style": "doc_truyen"},
    {"name": "Đoan Trang", "gender": "nữ", "region": "Bắc", "style": "tu_nhien"},
    {"name": "Mai Anh", "gender": "nữ", "region": "Bắc", "style": "tin_tuc"},
    {"name": "Quang Sơn", "gender": "nam", "region": "Trung", "style": "tu_nhien"},
    {"name": "Ngọc Trân", "gender": "nữ", "region": "Trung", "style": "tu_nhien"},
    {"name": "Thái Sơn", "gender": "nam", "region": "Nam", "style": "doc_truyen"},
    {"name": "Xuân Vĩnh", "gender": "nam", "region": "Nam", "style": "tu_nhien"},
    {"name": "Thục Đoan", "gender": "nữ", "region": "Nam", "style": "doc_truyen"},
    {"name": "Minh Triết", "gender": "nam", "region": "Nam", "style": "tin_tuc"},
    {"name": "Thùy Dung", "gender": "nữ", "region": "Nam", "style": "tin_tuc"},
]


def resolve_voice_name(requested: str) -> str:
    """Doi shortcut ('nam'/'nu'...) sang ten giong that; giu nguyen neu khong phai shortcut."""
    key = requested.strip().lower()
    return VOICE_SHORTCUTS.get(key, requested)


def ensure_data_dirs() -> None:
    VOICES_DIR.mkdir(parents=True, exist_ok=True)


def load_custom_voices(vieneu_instance: Any, path: Path | None = None) -> int:
    """Nap cac giong da nhan ban (luu boi clone_voice.py) vao doi tuong Vieneu().

    Tra ve so giong da nap. Khong lam gi neu file chua ton tai (chua nhan ban
    giong nao) — day KHONG phai loi.
    """
    import numpy as np

    voices_file = path or CUSTOM_VOICES_FILE
    if not voices_file.exists():
        return 0

    data = json.loads(voices_file.read_text(encoding="utf-8"))
    presets = data.get("presets", {})
    preset_dict = getattr(vieneu_instance, "_preset_voices", None)
    if preset_dict is None:
        print(
            "CANH BAO: doi tuong Vieneu() hien tai khong co thuoc tinh "
            "_preset_voices (co the dang chay o mode khac v3turbo) — "
            "khong nap duoc giong da nhan ban.",
            file=sys.stderr,
        )
        return 0

    count = 0
    for name, v in presets.items():
        emb = v.get("speaker_emb")
        codes = v.get("codes")
        preset_dict[name] = {
            "description": v.get("description", ""),
            "gender": v.get("gender", ""),
            "style": v.get("style", "tu_nhien"),
            "speaker_emb": np.asarray(emb, dtype=np.float32) if emb is not None else None,
            "codes": np.asarray(codes, dtype=np.int64) if codes is not None else None,
        }
        count += 1
    return count


def save_enrolled_voice(vieneu_instance: Any, path: Path | None = None) -> str:
    """Ghi TOAN BO giong hien co trong bo nho (dung san + moi nhan ban) ra file
    rieng cua skill (KHONG dung duong dan mac dinh cua thu vien).
    """
    ensure_data_dirs()
    voices_file = path or CUSTOM_VOICES_FILE
    saved_path = vieneu_instance.save_voices(path=str(voices_file))
    return saved_path


def list_all_voice_names(vieneu_instance: Any) -> List[Tuple[str, str]]:
    """Tra ve [(nhan hien thi, ten_giong)] gop ca giong dung san va giong da nhan ban."""
    return list(vieneu_instance.list_preset_voices())
