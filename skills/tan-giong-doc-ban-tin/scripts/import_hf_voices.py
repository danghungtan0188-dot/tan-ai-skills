#!/usr/bin/env python3
"""Nap them giong dung san moi cua VieNeu-TTS-v3-Turbo tu Hugging Face vao kho giong cua skill.

Goi `vieneu` 3.2.x chi kem 14 giong; repo model chinh thuc
(huggingface.co/pnnbao-ump/VieNeu-TTS-v3-Turbo, Apache-2.0, thu muc gguf/voices/) co 25.
Dinh dang giong o do (ref_codes 16 cot + speaker_emb 192 so) giong het giong trong goi,
nen chi can tai ve va them vao CUSTOM_VOICES_FILE — load_custom_voices() se nap luc chay.

Giong da co (trung ten) thi bo qua. Sao luu file kho giong truoc khi ghi.

    python import_hf_voices.py            # tai + them giong con thieu
    python import_hf_voices.py --xem      # chi liet ke, khong ghi
"""

from __future__ import annotations

import argparse
import json
import shutil
import urllib.request
from datetime import datetime
from pathlib import Path

from voices_store import CUSTOM_VOICES_FILE, ensure_data_dirs

BASE = "https://huggingface.co/pnnbao-ump/VieNeu-TTS-v3-Turbo/resolve/main/gguf/voices"
STYLES = {"tin tức": "tin_tuc", "kể chuyện": "doc_truyen", "đọc truyện": "doc_truyen", "tự nhiên": "tu_nhien"}


def _get(path: str) -> str:
    with urllib.request.urlopen(f"{BASE}/{path}", timeout=60) as r:
        return r.read().decode("utf-8")


def to_preset(entry: dict, codes_txt: str, emb_txt: str) -> dict:
    """entry['label'] dang '⭐ Thùy Dung — Nữ · Nam · Phong cách tin tức'."""
    desc = entry["label"].split("—", 1)[1].strip()
    gender, region, style = [p.strip() for p in desc.split("·")]
    codes = [int(x) for x in codes_txt.split()]
    if len(codes) % 16:
        raise ValueError(f"{entry['id']}: ref_codes {len(codes)} so, khong chia het cho 16")
    emb = [float(x) for x in emb_txt.strip().split(",")]
    if len(emb) != 192:
        raise ValueError(f"{entry['id']}: speaker_emb {len(emb)} so, can 192")
    return {
        "description": desc,
        "gender": "female" if gender == "Nữ" else "male",
        "style": next((v for k, v in STYLES.items() if k in style.lower()), "tu_nhien"),
        "region": region,
        "speaker_emb": emb,
        "codes": [codes[i:i + 16] for i in range(0, len(codes), 16)],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--xem", action="store_true", help="chỉ liệt kê giọng sẽ thêm, không ghi")
    a = ap.parse_args()

    manifest = json.loads(_get("manifest.json"))
    store = (json.loads(CUSTOM_VOICES_FILE.read_text(encoding="utf-8"))
             if CUSTOM_VOICES_FILE.exists() else {"presets": {}})
    import vieneu  # chi de biet giong nao goi da kem san
    bundled = json.loads((Path(vieneu.__file__).parent / "assets" / "voices_v3_turbo.json")
                         .read_text(encoding="utf-8"))["presets"]
    have = set(store["presets"]) | set(bundled)
    missing = [v for v in manifest["voices"] if v["name"] not in have]
    for v in missing:
        print(f"+ {v['label']}")
    if not missing:
        print("Đã có đủ giọng trong manifest — không thêm gì.")
        return 0
    if a.xem:
        return 0

    for v in missing:
        store["presets"][v["name"]] = to_preset(v, _get(f"{v['id']}/ref_codes.txt"),
                                                _get(f"{v['id']}/speaker.emb.txt"))
    ensure_data_dirs()
    if CUSTOM_VOICES_FILE.exists():
        backup = CUSTOM_VOICES_FILE.with_name(
            f"{CUSTOM_VOICES_FILE.stem}.backup-{datetime.now():%Y%m%d-%H%M%S}.json")
        shutil.copy2(CUSTOM_VOICES_FILE, backup)
        print(f"Sao lưu: {backup}")
    CUSTOM_VOICES_FILE.write_text(json.dumps(store, ensure_ascii=False), encoding="utf-8")
    print(f"Đã thêm {len(missing)} giọng vào {CUSTOM_VOICES_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
