#!/usr/bin/env python3
"""Dựng bilingual.json: ASR chỉ lấy MỐC THỜI GIAN, lời Việt hiệu đính theo kịch bản gốc.

  1) python build_bilingual.py transcribe INPUT --out asr_words.json
     whisper `small`, 1 tiến trình (máy này nóng nhanh). In bảng từ có đánh chỉ số.
  2) Viết cues.json:  [[tu_dau, tu_cuoi, "lời Việt đã hiệu đính", "English"], ...]
     chỉ số lấy từ bảng ở bước 1; lời Việt lấy theo kịch bản (docx), KHÔNG chép ASR.
  3) python build_bilingual.py build asr_words.json cues.json --out bilingual.json

ASR nghe sai rất nhiều ở bản tin: "chúc thỏ" (chúc thọ), "quý viên" (Ủy viên),
"sang lọc" (sàng lọc), "trà my tế" (Trạm Y tế), "VNAD" (VNeID), "bang đầu" (ban đầu).
"""
from __future__ import annotations
import argparse
import json
import subprocess
import tempfile
from pathlib import Path


def transcribe(src: Path, out: Path) -> list[dict]:
    from faster_whisper import WhisperModel
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "a.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vn", "-ac", "1", "-ar", "16000",
                        str(wav)], check=True)
        model = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
        segs, _ = model.transcribe(str(wav), language="vi", beam_size=5, word_timestamps=True)
        words = [{"s": round(w.start, 2), "e": round(w.end, 2), "w": w.word.strip()}
                 for s in segs for w in (s.words or [])]
    out.write_text(json.dumps(words, ensure_ascii=False), encoding="utf-8")
    for i in range(0, len(words), 10):
        print(f"{i:4d} [{words[i]['s']:7.2f}] " + " ".join(w["w"] for w in words[i:i + 10]))
    return words


def build(words: list[dict], cues: list, max_chars: int = 52) -> dict:
    segs, loi, truoc = [], [], 0.0
    for k, (i, j, vi, en) in enumerate(cues, 1):
        if not (0 <= i <= j < len(words)):
            loi.append(f"cue {k}: chỉ số từ {i}–{j} ngoài phạm vi 0–{len(words) - 1}")
            continue
        st, et = max(words[i]["s"], truoc + 0.02), words[j]["e"]
        if et <= st:
            loi.append(f"cue {k}: mốc {st}–{et}s không hợp lệ")
        for ten, chu in (("VI", vi), ("EN", en)):
            if not chu.strip():
                loi.append(f"cue {k}: thiếu {ten}")
            elif len(chu) > max_chars:
                loi.append(f"cue {k}: {ten} {len(chu)} ký tự (> {max_chars}) — sẽ tràn 2 dòng: {chu}")
        segs.append({"start": round(st, 2), "end": round(et, 2), "vi": vi, "en": en})
        truoc = et
    if loi:
        raise SystemExit("cues.json chưa đạt:\n" + "\n".join(loi))
    return {"meta": {"source_language": "vi", "translation_language": "en",
                     "english_above_vietnamese": True, "needs_review": True}, "segments": segs}


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("transcribe")
    t.add_argument("input", type=Path)
    t.add_argument("--out", type=Path, default=Path("asr_words.json"))
    b = sub.add_parser("build")
    b.add_argument("words", type=Path)
    b.add_argument("cues", type=Path)
    b.add_argument("--out", type=Path, default=Path("bilingual.json"))
    b.add_argument("--max-chars", type=int, default=52)
    a = ap.parse_args()
    if a.cmd == "transcribe":
        transcribe(a.input, a.out)
        return 0
    data = build(json.loads(a.words.read_text(encoding="utf-8")),
                 json.loads(a.cues.read_text(encoding="utf-8")), a.max_chars)
    a.out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    s = data["segments"]
    print(f"{len(s)} cue, {s[0]['start']}s → {s[-1]['end']}s -> {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
