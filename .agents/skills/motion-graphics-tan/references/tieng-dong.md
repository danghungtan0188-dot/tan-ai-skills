# Tiếng động tự tổng hợp cho thẻ chuyển động

Nguồn: bộ `sfx` của [whaleyxbt/claude-motion](https://github.com/whaleyxbt/claude-motion) (giấy phép MIT, commit `6f80380`).
Chép nguyên vào `scripts/sfx/`, kèm `scripts/sfx/LICENSE`. **Không sửa code gốc.** Mẫu riêng của repo nằm trong `scripts/sfx/cues/`.

Bộ này chỉ dùng Python có sẵn:
- không cần file âm thanh mẫu, không lo bản quyền, không phải cài thêm gì;
- mỗi lần chạy cho ra đúng một kết quả;
- máy nhẹ: 9 âm thanh cho 4,5 giây làm xong trong khoảng 1 giây.

## Chạy

```bash
cd skills/motion-graphics-tan/scripts
python -m sfx --list                                            # các loại tiếng có sẵn
python -m sfx sfx/cues/o_hoi_lat.py --out D:/tam/o-hoi-lat.wav  # mẫu cho thẻ ky-thuat/o-hoi-lat
```

Kết quả đã đo (08/11/2026): −14,0 LUFS, đỉnh −2,0 dBFS, LRA 2,3. Tiếng pop rơi đúng lúc ô lật (1,37 / 2,37 / 3,37 s).

## Viết tiếng cho thẻ mới

1. Ghi mốc thời gian của thẻ vào một file JSON cạnh bản tiếng (`<ten>.json`). Lấy mốc từ timeline GSAP của thẻ, **không gõ số tay trong hàm `score`**. Đổi nhịp thẻ thì chỉ sửa JSON.
2. Chép `sfx/cues/o_hoi_lat.py`, đổi các lệnh `mix.put(thời_điểm, tiếng, độ_to, pan)`.
3. Ghép vào video: `ffmpeg -threads 2 -i the.mp4 -i tieng.wav -c:v copy -c:a aac -shortest ra.mp4`, rồi kiểm bằng `look.py` (xem [kiem-re-tien.md](kiem-re-tien.md)).

## Hình nào đi với tiếng nào

| Trên màn hình | Tiếng | Ghi chú |
|---|---|---|
| Chữ gõ | `mix.typing()` | mỗi ký tự một tiếng phím, lệch nhịp nhẹ cho thật |
| Chữ, dòng hiện ra | `whoosh()` + `blip()` lúc chữ chạm | ngắn, nhẹ |
| Nhãn, viên thuốc, ô bật ra | `pop()` | cao dần theo thứ tự |
| Bấm nút, bước | `click()` + `blip()` | cùng giọng nhạc |
| Nét vẽ tay | `scratch()` | |
| Dồn lên cao trào | `riser()` | kết đúng lúc chạm, mỗi video một lần |
| Xong, thành công | `chime()` | hợp âm cùng giọng |
| Chuyển cảnh chính | `whoosh()` vào, `impact()` lúc chạm | mỗi video một lần |
| Nền suốt video | `pad()` + `envelope()` | hạ xuống dưới cú chuyển chính |

**Nhấn, không kể lể:** không phải chuyển động nào cũng cần tiếng. Chuyển động liên tục (trôi, xoay chậm) để im.
Số đo 86 reel cũng cho thấy hai kênh Facebook gần như không đặt tiếng ở mọi cú cắt.

## Độ to và vị trí

- Tiếng chính: 0,25–0,35. Tiếng phụ: 0,08–0,2. Nền `pad`: khoảng 0,03.
- Pan theo vị trí trên màn hình (−1 trái … +1 phải). Một chuỗi tiếng thì quét từ trái sang phải.
- Chọn **một giọng nhạc** cho mọi tiếng có cao độ. Cao độ tăng theo tiến trình.
- Bộ tự master về `TARGET_LUFS` (mặc định −14, trùng chuẩn đã đo ở Facebook) và giữ đỉnh ≤ −2 dBFS.
- Video có **giọng người nói**: tiếng hiệu ứng thấp hơn giọng khoảng 6,5 dB, nhạc nền thấp hơn khoảng 15 dB (xem `video-marketing/references/nhip-dung-nguoi-noi.md`). Trộn sau cùng, loudnorm 2 lượt `linear=true`.

## Không dùng

Phần ElevenLabs của repo gốc là dịch vụ trả phí, nên không chép. Giọng đọc dùng skill `tan-giong-doc-ban-tin` (VieNeu, chạy trên máy).
