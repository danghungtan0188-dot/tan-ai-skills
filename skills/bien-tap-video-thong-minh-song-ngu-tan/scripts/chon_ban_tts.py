"""Chọn bản đọc TTS tốt nhất của một cụm theo SÀN CỨNG — phát âm trước, ngữ điệu sau.

Mỗi bản là dict: {"ten", "cer", "thieu" (list chữ khó sai), "f0r" (biên độ cao độ, semitone), "dur" (giây)}.

1. Loại bản dài bất thường (> 1,3 × trung vị của cụm): bản lặp chữ / có tiếng lạ luôn dài hơn hẳn.
   (Video 96 năm Hội LHPN, 2026-10-18: bản lặp "vun đắp hạnh phúc" dài 4,9 s so với 3,1 s lại sai ÍT
   chữ khó nhất nên bị chọn trúng.)
2. Giữ các bản sai ít chữ khó nhất.
3. Sàn = CER thấp nhất + 0,03; bỏ bản trên sàn.
4. Trong số đạt sàn mới xét ngữ điệu: min(f0r, 11), rồi CER thấp hơn.
"""
from __future__ import annotations

import statistics

NGUONG_DAI = 1.3
SAN_CER = 0.03


def chon_ban(ban: list[dict]) -> str:
    if not ban:
        raise ValueError("không có bản nào để chọn")
    tv = statistics.median(b["dur"] for b in ban)
    con = [b for b in ban if b["dur"] <= NGUONG_DAI * tv] or ban
    it_sai = min(len(b["thieu"]) for b in con)
    con = [b for b in con if len(b["thieu"]) == it_sai]
    san = min(b["cer"] for b in con) + SAN_CER
    con = [b for b in con if b["cer"] <= san]
    return max(con, key=lambda b: (min(b["f0r"], 11), -b["cer"], b["f0r"]))["ten"]
