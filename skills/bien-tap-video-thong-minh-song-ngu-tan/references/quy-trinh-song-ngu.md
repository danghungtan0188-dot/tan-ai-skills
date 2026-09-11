# Quy trình song ngữ Việt–Anh

## 1. Lời Việt lấy từ kịch bản, không lấy từ ASR

ASR chỉ để lấy **mốc thời gian**. Lời Việt chép theo kịch bản gốc (docx) và sửa chính tả.
Lỗi ASR gặp ở 2 bản tin ATT NEWS: "chúc thỏ" (chúc thọ), "quý viên" (Ủy viên), "quý ban nhân dân"
(Ủy ban nhân dân), "kính láo" (kính lão), "sang lọc" (sàng lọc), "trà my tế" (Trạm Y tế), "VNAD" (VNeID),
"bang đầu" (ban đầu), "phát quyền gai trọc" (phát huy vai trò), "xá" (xã/sáng).

```bash
python scripts/build_bilingual.py transcribe INPUT --out asr_words.json   # in bảng từ có chỉ số
# viết cues.json: [[tu_dau, tu_cuoi, "lời Việt theo kịch bản", "English"], ...]
python scripts/build_bilingual.py build asr_words.json cues.json --out bilingual.json
```

Mỗi cue ≤ 52 ký tự mỗi thứ tiếng khi đốt vào hình 16:9 (dài hơn sẽ thành 4 dòng chữ).
Ngắt câu theo cụm nghĩa; không tách tên người hay số liệu.

## 2. Dịch

- Dịch theo nghĩa, văn phong tin tức; không dịch từng chữ.
- Tên riêng bỏ dấu: An Thạnh Thủy → An Thanh Thuy; Nguyễn Công Thành → Nguyen Cong Thanh.
- Chức danh, cơ quan theo `references/glossary-vi-en.csv`.
- Số liệu giữ nguyên giá trị: 2.500 → 2,500; 7–8/9/2026 → September 7 and 8, 2026.

## 3. Kiểm bản dịch bằng máy

```bash
python scripts/check_translation.py bilingual.json
```

Bắt: thiếu thuật ngữ bắt buộc, số liệu có ở câu Việt nhưng mất ở câu Anh, câu chưa dịch.
Lỗi thật đã bắt được ở video sk2: *"UBND xã An Thạnh Thủy"* dịch thành *"An Thanh Thuy commune"* — mất
"People's Committee". Máy chỉ là lưới lọc; `needs_review` chỉ được tắt sau khi **người** rà xong.

Thêm từ vào glossary: cột `vi` và `en` nhận nhiều cách viết, ngăn bằng `|`. Cụm dài được khớp trước
("Phó Chủ tịch UBND xã" trước "Chủ tịch UBND xã").

## 4. Bốn chế độ xuất phụ đề

```bash
python scripts/export_subtitles.py bilingual.json --mode all --out-dir phu-de --stem ten-video
```

| Chế độ | File | Dùng khi |
|---|---|---|
| `ass` | `ten.song-ngu.ass` | đốt vào hình, EN trên VI dưới — mặc định bản tin ATT NEWS |
| `srt-vi` | `ten.vi_VN.srt` | phụ đề Việt rời, người xem bật/tắt (Facebook đòi đúng dạng `ten.ma_QUOCGIA.srt`) |
| `srt-en` | `ten.en_US.srt` | phụ đề Anh rời |
| `vtt` | `ten.song-ngu.vtt` | web/YouTube, hai dòng EN–VI |

SRT một thứ tiếng tự ngắt dòng quá 42 ký tự thành 2 dòng ở khoảng trắng gần giữa nhất.

## 5. Kiểm file SRT/VTT

```bash
python scripts/check_subtitles.py phu-de/ten.vi_VN.srt
python scripts/check_subtitles.py phu-de/ten.song-ngu.vtt --song-ngu --max-chars 52
```

| Kiểm | Mức |
|---|---|
| timecode sai định dạng/giá trị, bắt đầu ≥ kết thúc, cue rỗng, cue chồng lấn | LỖI |
| cue ngắn hơn 0,8 s, dòng dài hơn 42 (16:9) / 30 (9:16) ký tự, quá 2 dòng | CẢNH BÁO |
| tốc độ đọc quá 17 ký tự/giây (song ngữ tính theo dòng dài nhất) | CẢNH BÁO |

`--strict` biến cảnh báo thành lỗi.
