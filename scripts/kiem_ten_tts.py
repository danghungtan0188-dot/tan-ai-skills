#!/usr/bin/env python3
"""Kiểm tên người / cụm bắt buộc trong các bản đọc TTS bằng bỏ phiếu 3 lần nghe.

Whisper nghe mỗi lần một kiểu, nên nghe mỗi file 3 cách (beam 5 / beam 1 / temperature 0,4);
một cụm ĐẠT khi ≥ 2/3 lần nghe ra đủ cụm đó. Bản tin có lãnh đạo Trung ương không được sai tên.

  python scripts/kiem_ten_tts.py cau.json [--ra ket_qua.json]

cau.json (đường dẫn wav tính từ thư mục chứa cau.json):
  [{"id": "c3_01", "file": "ban/c3_01.wav", "can": ["đỗ văn chẩn", "trị giá"]}, ...]

Kết quả nghe được lưu ngay sau từng file; chạy lại bỏ qua file đã nghe (cùng kích thước, cùng giờ sửa).
LƯU Ý: máy nghe sai đều đặn chưa chắc là giọng sai (13/11: "Thị"→"Thiện" 14/14 bản, tai người nghe đúng)
— cụm CẦN XEM thì gửi người dùng nghe 10–20 s trước khi đổi giọng hay đọc lại.
Exit 0 = mọi cụm đạt; 1 = có cụm cần xem; 2 = lỗi đầu vào.
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

REPO = Path(__file__).resolve().parents[1]
CACH_NGHE = [dict(beam_size=5), dict(beam_size=1), dict(beam_size=1, temperature=0.4)]
NGUONG = 2


def chuan(s):
    s = " ".join(re.sub(r"[^\w\s]", " ", unicodedata.normalize("NFC", s.lower())).split())
    return s.replace("uỷ", "ủy")


def cham(nghe, can, nguong=NGUONG):
    """nghe: các chuỗi whisper nghe ra; can: các cụm bắt buộc. Trả [(cụm, số lần nghe ra, đạt?)]."""
    nghe = [f" {chuan(n)} " for n in nghe]
    ra = []
    for c in can:
        so = sum(f" {chuan(c)} " in n for n in nghe)
        ra.append((c, so, so >= nguong))
    return ra


def _dau_van_tay(p):
    st = p.stat()
    return [st.st_size, int(st.st_mtime)]


def _nghe_file(model, p):
    import numpy as np
    import soundfile as sf

    sys.path.insert(0, str(REPO / "skills" / "bien-tap-video-thong-minh-song-ngu-tan" / "scripts"))
    from cat_gon_tts import cat_gon

    a, sr = sf.read(p, dtype="float32")
    x, _ = cat_gon(a if a.ndim == 1 else a.mean(1), sr)
    y16 = np.interp(np.arange(0, len(x), sr / 16000), np.arange(len(x)), x).astype(np.float32)
    return [" ".join(s.text for s in model.transcribe(y16, language="vi", condition_on_previous_text=False,
                                                      vad_filter=True, **k)[0]) for k in CACH_NGHE]


def _ha_uu_tien():
    if sys.platform == "win32":  # máy hay sập khi chạy nặng: ưu tiên thấp
        import ctypes

        ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x40)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Kiểm tên/cụm bắt buộc trong bản đọc TTS (whisper small, bỏ phiếu 2/3).")
    ap.add_argument("cau", help="file JSON danh sách câu")
    ap.add_argument("--ra", help="file kết quả JSON (mặc định: <cau>_ket_qua.json)")
    ap.add_argument("--model", default="small", help="model whisper (mặc định small — medium quá chậm trên máy này)")
    args = ap.parse_args(argv)

    nguon = Path(args.cau)
    try:
        ds = json.loads(nguon.read_text(encoding="utf-8"))
        for c in ds:
            c["id"], c["file"], c["can"]  # noqa: B018 — kiểm khóa bắt buộc
    except (OSError, ValueError, KeyError, TypeError) as e:
        print(f"LOI đọc {nguon}: {e}", file=sys.stderr)
        return 2
    ra = Path(args.ra) if args.ra else nguon.with_name(nguon.stem + "_ket_qua.json")
    nho = json.loads(ra.read_text(encoding="utf-8")) if ra.exists() else {}

    model = None
    can_xem = {}
    for c in ds:
        p = (nguon.parent / c["file"]).resolve()
        if not p.exists():
            print(f"LOI không có file {p}", file=sys.stderr)
            return 2
        cu = nho.get(c["id"])
        if not cu or cu.get("file") != str(p) or cu.get("van_tay") != _dau_van_tay(p):
            if model is None:
                _ha_uu_tien()
                from faster_whisper import WhisperModel

                model = WhisperModel(args.model, device="cpu", compute_type="int8", cpu_threads=1)
            nho[c["id"]] = {"file": str(p), "van_tay": _dau_van_tay(p), "nghe": _nghe_file(model, p)}
            ra.write_text(json.dumps(nho, ensure_ascii=False, indent=1), encoding="utf-8")  # lưu từng file
        nghe = nho[c["id"]]["nghe"]
        for cum, so, dat in cham(nghe, c["can"]):
            print(f"{c['id']:8s} {cum:24s} {so}/{len(nghe)} {'DAT' if dat else 'CAN XEM'} | {' || '.join(map(chuan, nghe))}",
                  flush=True)
            if not dat:
                can_xem.setdefault(c["id"], []).append(cum)
    nho["_can_xem"] = can_xem
    ra.write_text(json.dumps(nho, ensure_ascii=False, indent=1), encoding="utf-8")
    print("XONG, cần xem:", can_xem or "không có", "→", ra)
    return 1 if can_xem else 0


if __name__ == "__main__":
    sys.exit(main())
