# Hồ sơ dựng theo nội dung

| Profile | Nhịp | Transition | Màu | Chữ/hiệu ứng |
|---|---|---|---|---|
| `official_news` | 2,5–6 s/cảnh | cut, dissolve 0,2–0,4 s | News Clean | headline, lower-third, flash rất nhẹ |
| `conference` | 3–8 s/cảnh | cut, fade | Natural/News Clean | diễn giả, đại biểu, thông điệp chính |
| `interview` | theo câu nói | J/L cut, dissolve nhẹ | Natural | tên/chức danh, caption, hầu như không effect |
| `documentary_event` | 1,8–5 s/cảnh | cut-on-action, sound bridge | Natural/Cinematic nhẹ | montage theo cụm, light leak tiết chế |
| `education` | đủ thời gian đọc | cut, slide nhẹ | Clean/Warm | callout, step label, highlight từ khóa |
| `social_montage` | 0,5–2,5 s/cảnh | whip, flash, zoom | Vibrant có kiểm soát | kinetic text, beat cut, effect mạnh hơn |

## Tín hiệu phân loại

- Từ khóa “UBND, hội nghị, đồng chí, tuyên truyền, quyết định” ưu tiên `official_news`/`conference`.
- Một người nói chiếm phần lớn và có hỏi–đáp ưu tiên `interview`.
- “Bước 1, hướng dẫn, cách làm, bài học” ưu tiên `education`.
- Shot rate cao, ít lời, nhạc chủ đạo ưu tiên `social_montage`.
- Không đủ bằng chứng: chọn `official_news` cho nội dung cơ quan hoặc `documentary_event` cho sự kiện chung, rồi báo độ tin cậy thấp.

## Video quảng bá dịch vụ của người dùng (tiếng Anh, đăng Facebook/TikTok)

Chốt sau video "Every day, one small step" (18/10/2026, 2:40, bản ngang 16:9):

- Một bản ngang 16:9 là đủ; không làm thêm bản dọc khi chưa được yêu cầu.
- Đoạn người dùng tự nói tiếng Anh: giữ tiếng gốc, **không phụ đề**; thay bằng ô chữ câu chốt đặt ở vùng nền mờ hai bên (không che mặt) và thanh tên đầu đoạn.
- Lời dẫn chen giữa: tiếng Anh, giọng "Hùng Tân chân thật - English" (đọc đúng 100% cả 15 bản thử).
- Phụ đề lời dẫn: chữ đậm trắng + cụm nhấn Georgia nghiêng vàng `&H002DCDFF`, **có nền tối** ASS `BorderStyle=3`, `BackColour=&H66000000`, viền 14. Không có nền thì chữ mất trên cảnh nền vàng/sáng (gặp thật ở cảnh minh họa nền vàng).
- Thẻ kêu gọi: dịch vụ là **"nhận"** (NHẬN EDIT VIDEO · DỰNG VIDEO AI · LÀM WEB APP & TOOLS · INBOX NGAY), tiêu đề "Your video, *edit with Tan*". Chữ trên thẻ kêu gọi phải đưa người dùng xem trước khi render.
- Âm lượng tổng −16 LUFS, đỉnh −1,4 dBFS, 2 lượt linear.

