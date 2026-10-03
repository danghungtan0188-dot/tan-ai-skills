"""Phụ đề từ script gốc + mốc thời gian từng đoạn audio.

Phụ đề hiển thị chữ GỐC (người xem đọc "22/5/2003"), còn giọng đọc dùng bản đã chuẩn hoá.
Phương pháp căn thời gian ghi vào kết quả để biết độ chính xác:
- `moc_doan_tts`: biết chính xác đầu/cuối từng đoạn (mỗi đoạn một file WAV); trong một đoạn,
  các cue chia thời gian theo tỉ lệ số ký tự — ước lượng, có thể lệch vài trăm mili-giây.
- `ti_le_so_chu`: audio có sẵn, không có mốc đoạn — chia cả bài theo số ký tự.
File SRT xuất ra sửa tay được; bước dựng video đọc lại đúng file SRT đó.
"""

from __future__ import annotations

import re
from pathlib import Path

import check_subtitles  # noqa: E402  (skills/bien-tap-video-thong-minh-song-ngu-tan/scripts)
import export_subtitles  # noqa: E402

LINE = {"16:9": 42, "9:16": 30}  # ký tự mỗi dòng, khớp ngưỡng check_subtitles; mỗi cue tối đa 2 dòng


def split_cues(text: str, max_len: int = 2 * LINE["16:9"] - 4) -> list[str]:
    """Cắt theo câu; câu dài cắt ở dấu phẩy rồi gộp lại cho vừa; vẫn dài thì chia đều theo từ."""
    out = []
    for sent in re.split(r"(?<=[.!?…])\s+", text.strip()):
        buf = ""
        for piece in ([sent] if len(sent) <= max_len else re.split(r"(?<=[,;:])\s+", sent)):
            cand = f"{buf} {piece}".strip()
            if len(cand) <= max_len:
                buf = cand
                continue
            if buf:
                out.append(buf)
            buf = ""
            if len(piece) <= max_len:
                buf = piece
            else:
                out += _even_split(piece, max_len)
        if buf:
            out.append(buf)
    return [c for c in out if c]


def _even_split(text: str, max_len: int) -> list[str]:
    """Chia thành k khúc gần bằng nhau, cắt ở khoảng trắng gần điểm chia nhất."""
    words = text.split()
    k = -(-len(text) // max_len)
    chunks, cur = [], []
    target = len(text) / k
    for w in words:
        if cur and len(" ".join(cur + [w])) > target * 1.15 and len(chunks) < k - 1:
            chunks.append(" ".join(cur))
            cur = []
        cur.append(w)
    chunks.append(" ".join(cur))
    return chunks


def _spread(chunks: list[str], start: float, end: float) -> list[dict]:
    total = sum(len(c) for c in chunks) or 1
    cues, t = [], start
    for c in chunks:
        dur = (end - start) * len(c) / total
        cues.append({"start": round(t, 3), "end": round(t + dur, 3), "vi": c})
        t += dur
    return cues


def cues_from_tts(segments: list[dict], tts_segments: list[dict], aspect: str = "16:9") -> list[dict]:
    originals = {s["index"]: s["original"] for s in segments}
    cues = []
    for t in tts_segments:
        cues += _spread(split_cues(originals[t["index"]], 2 * LINE[aspect] - 4), t["start"], t["end"])
    return cues


def cues_from_duration(segments: list[dict], duration: float, aspect: str = "16:9") -> list[dict]:
    chunks = [c for s in segments for c in split_cues(s["original"], 2 * LINE[aspect] - 4)]
    return _spread(chunks, 0.0, duration)


def write_srt(cues: list[dict], path: Path, aspect: str = "16:9") -> Path:
    Path(path).write_text(export_subtitles.srt(cues, "vi", LINE[aspect]), encoding="utf-8")
    return Path(path)


def read_srt(path: Path) -> list[dict]:
    cues = check_subtitles.parse(Path(path).read_text(encoding="utf-8"), "srt")
    return [{"start": c["start"], "end": c["end"], "vi": "\n".join(c["lines"])} for c in cues]


def validate(path: Path, aspect: str = "16:9") -> tuple[list[str], list[str]]:
    """(lỗi, cảnh báo) theo check_subtitles của skill."""
    cues = check_subtitles.parse(Path(path).read_text(encoding="utf-8"), "srt")
    return check_subtitles.check(cues, max_chars=LINE[aspect])
