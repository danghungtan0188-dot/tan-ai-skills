"""Mốc thời gian TỪNG CHỮ cho phụ đề Remotion, lấy từ giọng đã ghép — thay cho chia đều câu theo thời lượng.

Luật học từ `iart-ai/tiktok-video-skills` (10/2026): phụ đề hiện từng chữ chỉ "ăn" khi mỗi chữ rơi đúng âm tiết;
chia đều câu theo thời lượng thì lệch nhìn ra ngay. Văn bản đúng đã biết trước (kịch bản TTS) nên whisper chỉ dùng
để lấy MỐC; chữ whisper nghe sai/thiếu thì nội suy từ hai chữ khớp gần nhất.

    python moc_tung_chu.py giong.wav moc.json        # ghi thêm "tu": [giây bắt đầu từng chữ] vào mỗi câu
"""
from __future__ import annotations

import difflib
import json
import re
import sys
import unicodedata


def chuan(w: str) -> str:
    return re.sub(r"[^\w]", "", unicodedata.normalize("NFC", w.lower()))


def canh_chu(chu: list[str], nghe: list[tuple[str, float]], bat_dau: float, ket_thuc: float) -> list[float]:
    """Gán giây bắt đầu cho từng chữ trong `chu` theo các chữ whisper nghe được `nghe` [(chữ, giây)].

    Chữ khớp được lấy mốc của whisper; chữ không khớp nội suy tuyến tính giữa hai mốc khớp gần nhất
    (hai đầu neo vào bat_dau/ket_thuc). Kết quả luôn tăng dần, nằm trong [bat_dau, ket_thuc]."""
    n = len(chu)
    moc: list[float | None] = [None] * n
    a, b = [chuan(w) for w in chu], [chuan(w) for w, _ in nghe]
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            moc[blk.a + k] = nghe[blk.b + k][1]
    # neo hai đầu rồi nội suy chỗ trống
    diem = [(-1, bat_dau)] + [(i, t) for i, t in enumerate(moc) if t is not None] + [(n, ket_thuc)]
    ra = []
    for i in range(n):
        if moc[i] is not None:
            ra.append(moc[i]); continue
        trai = max((d for d in diem if d[0] < i), key=lambda d: d[0])
        phai = min((d for d in diem if d[0] > i), key=lambda d: d[0])
        ra.append(trai[1] + (phai[1] - trai[1]) * (i - trai[0]) / (phai[0] - trai[0]))
    # đơn điệu + kẹp biên (whisper đôi khi trả mốc lùi)
    for i in range(n):
        ra[i] = min(max(ra[i], bat_dau, ra[i - 1] if i else bat_dau), ket_thuc)
    return [round(t, 3) for t in ra]


def ti_le_khop(chu: list[str], nghe: list[str]) -> float:
    a, b = [chuan(w) for w in chu], [chuan(w) for w in nghe]
    return sum(k.size for k in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks()) / max(1, len(a))


def main(wav: str, moc_json: str) -> None:
    import librosa
    import soundfile as sf
    from faster_whisper import WhisperModel

    moc = json.load(open(moc_json, encoding="utf-8"))
    am, sr = sf.read(wav, dtype="float32")
    am = am if am.ndim == 1 else am.mean(1)
    if sr != 16000:  # faster-whisper nhận mảng số là hiểu 16 kHz; đưa 48 kHz vào sẽ ra chữ vô nghĩa
        am, sr = librosa.resample(am, orig_sr=sr, target_sr=16000), 16000
    m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=1)  # máy hay sập: 1 luồng
    for c in moc["cau"]:
        t0, t1 = c["batDau"], c["ketThuc"]
        doan = am[int(max(0, t0 - 0.1) * sr): int((t1 + 0.1) * sr)]
        seg, _ = m.transcribe(doan, language="vi", beam_size=3, word_timestamps=True, condition_on_previous_text=False)
        nghe = [(w.word.strip(), max(0.0, t0 - 0.1) + w.start) for s in seg for w in (s.words or [])]
        c["tu"] = canh_chu(c["chu"].split(), nghe, t0, t1)
        khop = ti_le_khop(c["chu"].split(), [w for w, _ in nghe])
        print(c.get("id", ""), f"khớp {khop:.0%} chữ", "" if khop >= 0.5 else "<-- ÍT KHỚP: mốc gần như nội suy, nghe lại câu này", flush=True)
    json.dump(moc, open(moc_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
