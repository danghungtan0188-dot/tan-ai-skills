"""Neo hieu ung theo CAU NOI: dua vao cau nguoi dung noi trong video, tra ve giay bat dau / ket thuc.

Cau lenh hieu ung kieu "them X luc minh noi '...'" can giay that. Whisper (faster-whisper small, 1 luong
nhu moc_tung_chu.py -- may hay sap) lay moc TUNG CHU cua ca video, roi tim doan chu giong cau nhat.
Khop duoi NGUONG thi bao ro, khong doan.

    python tim_cau_noi.py video.mp4 "tu dien thoai may tinh bang hay la may tinh" [-c "cau 2"] -o moc.json
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

NGUONG = 0.6  # ty le chu khop toi thieu de tin moc


def chuan(w: str) -> str:
    return re.sub(r"[^\w]", "", unicodedata.normalize("NFC", w.lower()))


def tim(cau: str, chu: list[tuple[str, float, float]]) -> dict:
    """chu = [(chu, bat_dau, ket_thuc)] theo thu tu. Tra {bat_dau, ket_thuc, do_khop, nghe_duoc}.

    Truot cua so dai bang so chu cua cau (+-2), lay cua so co ty le khop cao nhat; trung thi lay cua so som hon."""
    dich = [chuan(w) for w in cau.split() if chuan(w)]
    nghe = [chuan(w) for w, _, _ in chu]
    if not dich or not nghe:
        return {"bat_dau": None, "ket_thuc": None, "do_khop": 0.0, "nghe_duoc": ""}
    tot = (0.0, 0, 0)
    for dai in range(max(1, len(dich) - 2), len(dich) + 3):
        for i in range(0, max(1, len(nghe) - dai + 1)):
            cs = nghe[i:i + dai]
            sm = difflib.SequenceMatcher(None, dich, cs, autojunk=False)
            ty_le = sum(b.size for b in sm.get_matching_blocks()) / len(dich)
            if ty_le > tot[0] + 1e-9:
                tot = (ty_le, i, i + len(cs))
    ty_le, i, j = tot
    # cat bo chu thua o hai dau cua so (khong khop chu nao cua cau)
    while i < j - 1 and nghe[i] not in dich:
        i += 1
    while j - 1 > i and nghe[j - 1] not in dich:
        j -= 1
    return {"bat_dau": round(chu[i][1], 2), "ket_thuc": round(chu[j - 1][2], 2), "do_khop": round(ty_le, 2),
            "nghe_duoc": " ".join(w for w, _, _ in chu[i:j])}


def nghe_ca_video(video: Path) -> list[tuple[str, float, float]]:
    from faster_whisper import WhisperModel

    with tempfile.TemporaryDirectory() as tam:
        wav = Path(tam) / "a.wav"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-threads", "2", "-i", str(video),
                        "-vn", "-ac", "1", "-ar", "16000", str(wav)], check=True)
        m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=1)
        seg, _ = m.transcribe(str(wav), language="vi", beam_size=3, word_timestamps=True,
                              condition_on_previous_text=False)
        return [(w.word.strip(), w.start, w.end) for s in seg for w in (s.words or []) if w.word.strip()]


def main() -> int:
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", type=Path)
    ap.add_argument("cau", help="cau noi dau tien")
    ap.add_argument("-c", "--cau-them", action="append", default=[], help="them cau khac")
    ap.add_argument("-o", "--out", type=Path, required=True)
    a = ap.parse_args()
    chu = nghe_ca_video(a.video)
    ket_qua, yeu = [], 0
    for cau in [a.cau, *a.cau_them]:
        r = {"cau": cau, **tim(cau, chu)}
        ket_qua.append(r)
        yeu += r["do_khop"] < NGUONG
        canh_bao = "" if r["do_khop"] >= NGUONG else "  <-- KHOP YEU: nghe lai / sua cau, khong dung moc nay"
        print(f"{r['bat_dau']}s -> {r['ket_thuc']}s  khop {r['do_khop']:.0%}  \"{r['nghe_duoc']}\"{canh_bao}")
    a.out.write_text(json.dumps({"video": str(a.video), "moc": ket_qua}, ensure_ascii=False, indent=1), encoding="utf-8")
    return 1 if yeu else 0


if __name__ == "__main__":
    raise SystemExit(main())
