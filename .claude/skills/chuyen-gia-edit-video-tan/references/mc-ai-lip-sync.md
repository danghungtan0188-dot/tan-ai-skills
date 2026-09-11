# MC AI, thay lời thoại và lip-sync

Phạm vi: (a) thay lời MC trong video có sẵn và khớp lại khẩu hình; (b) dựng MC ảo mới;
(c) lồng giọng tổng hợp vào hình người thật.

## 1. Quyền dùng khuôn mặt và giọng nói — kiểm trước, thiếu thì dừng

Mỗi khuôn mặt, mỗi giọng phải có **hồ sơ đồng ý**, lưu ngoài Git:

| Trường | Ví dụ |
|---|---|
| Chủ thể | người có khuôn mặt / giọng |
| Loại quyền | khuôn mặt · giọng · cả hai |
| Phạm vi | kênh ATT NEWS; chủ đề được phép; chủ đề cấm |
| Thời hạn, ngày xác nhận, người xác nhận | |
| Bằng chứng | văn bản, tin nhắn đồng ý |

Giọng: theo thêm `skills/bien-tap-video-thong-minh-song-ngu-tan/references/authorized-voice.md`.

**Cấm, kể cả khi được yêu cầu:**
- Dùng mặt/giọng của lãnh đạo, cán bộ, người nổi tiếng hay bất kỳ ai chưa có hồ sơ.
- Để MC AI nói điều có thể bị hiểu là lời thật của một người có thật (phát biểu, chỉ đạo, số liệu y tế, pháp lý).
- Đọc tin khẩn/cảnh báo bằng MC AI khi thông tin chưa xác minh.

## 2. Gắn nhãn nội dung AI

- **Trên hình:** `label_chip(kind="ai")` của `scripts/broadcast_kit.py` ở góc trên phải, ít nhất 3 giây đầu
  mỗi đoạn có MC AI; end card thêm dòng *"MC ảo và giọng đọc được tạo bằng AI"*.
- **Mô tả bài đăng:** *"Video có sử dụng MC ảo/giọng đọc AI."*
- **Nền tảng:** bật nhãn AI khi đăng (Facebook "AI info", YouTube "Altered or synthetic content",
  TikTok "AI-generated"). Người dùng tự đăng; skill không tự đăng.

## 3. Quy trình

1. **Kịch bản đã duyệt** (docx của người dùng). AI không tự viết lại nội dung tin.
2. **Giọng:** skill `tan-giong-doc-ban-tin` (VieNeu-TTS, chạy trên máy, miễn phí) hoặc giọng đã có hồ sơ.
   Chọn bản đọc bằng điểm CER + cao độ F0, không chọn bằng tai.
3. **Lip-sync:** skill `mc-lip-sync` — nằm ở `~/.codex/skills/mc-lip-sync` (bộ skill Codex, **ngoài repo
   này**). Dùng MuseTalk, không phụ thuộc HeyGen. Đầu vào: video MC gốc + audio mới; đầu ra MP4 đã khớp miệng.
   Cài skill chưa có nghĩa là đã có trọng số mô hình — chạy thử 5 giây trước khi chạy cả bài.
   Đường thay thế: `heygen-video` / `heygen-translate` — **dịch vụ trả phí, phải hỏi và được đồng ý từng lần**.
4. **Ghép vào bản tin:** `render_att.py` (skill song ngữ) hoặc `scripts/render_project.py`.
5. **QA chi tiết** — mục 4, bắt buộc trước khi giao.
6. **Nhãn AI** — mục 2.

## 4. QA chi tiết

```bash
python scripts/mc_qa_frames.py VIDEO asr_words.json --face x,y,w,h --out qa_mc.jpg
```

Bảng khung phóng to mặt tại các từ mở bằng **b / m / p** (môi phải khép hẳn — lệch lip-sync lộ rõ nhất ở
đây) cộng mẫu đều mỗi 3 giây. Xem một lượt tốc độ thường và một lượt 0,5×.

| Bộ phận | Đạt khi | Lỗi hay gặp |
|---|---|---|
| Miệng | môi khép hẳn ở b/m/p, mở rộng ở a/o; lệch ≤ 2 khung (~66 ms ở 30 fps) | môi rung khi im lặng; miệng mở lúc đang ngậm |
| Răng | số răng ổn định, rõ từng chiếc | răng nhoè thành một khối trắng, đổi hình giữa các khung |
| Mắt | chớp tự nhiên ~10–20 lần/phút, ánh nhìn ổn định | 30 giây không chớp; mắt lệch; đồng tử méo |
| Tóc | viền tóc sắc, không nháy | quầng mờ quanh đầu, tóc "sôi" |
| Bàn tay | đủ 5 ngón, không dính micro/máy tính bảng | ngón thừa/thiếu, tay tan chảy khi cử động |
| Viền ghép | không halo, không lem xanh | viền trắng/xanh quanh vai, viền rung |
| Ánh sáng | hướng sáng và nhiệt màu khớp phông | mặt sáng hơn phông, bóng ngược hướng |
| Liên tục | áo, kính, phụ kiện, vị trí giữ nguyên suốt đoạn | kính biến mất, áo đổi màu giữa cảnh |

Lỗi ở miệng/răng → chạy lại lip-sync đúng đoạn đó. Lỗi viền/sáng → sửa bước ghép, không phải lip-sync.
Âm thanh: loudnorm 2 lượt linear, không bóp dải động.
