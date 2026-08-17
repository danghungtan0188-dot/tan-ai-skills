# Định dạng xuất: TikTok / Facebook

## Thông số theo nền tảng

| Nền tảng | Tỉ lệ | Độ phân giải khuyến nghị | Thời lượng gợi ý | Ghi chú vùng an toàn |
|---|---|---|---|---|
| TikTok | 9:16 dọc | 1080×1920 | 15–34s cho video sản phẩm | Chừa ~250px đáy và ~120px đỉnh cho UI (nút tương tác, caption app, tên tài khoản) — không đặt CTA/chữ quan trọng trong vùng này. |
| Facebook Reels | 9:16 dọc | 1080×1920 | 15–34s | Tương tự TikTok, chừa đáy cho thanh tương tác. |
| Facebook Feed (vuông) | 1:1 | 1080×1080 | 15–60s | An toàn hơn cho chữ, nhưng ảnh preview có thể bị crop trên một số vị trí hiển thị — kiểm tra chủ thể sản phẩm luôn nằm giữa khung. |
| Facebook Feed (dọc 4:5) | 4:5 | 1080×1350 | 15–60s | Chiếm diện tích feed lớn hơn 1:1, dùng khi muốn nổi bật hơn. |

## Codec/nén xuất (qua `video-use` render.py)

- Video: H.264, `yuv420p` (tương thích rộng nhất khi upload lên TikTok/Facebook).
- Khung hình: 30fps trừ khi nguồn khác yêu cầu.
- Audio: AAC, loudness giọng đọc mục tiêu −16 đến −19 LUFS (cùng chuẩn với `video-thuyet-minh`).

## Quy tắc bố cục theo Nguyên tắc cứng #4 (không kéo giãn méo ảnh)

1. Xác định tỉ lệ khung hình đích trước khi dựng cảnh (Bước E), không dựng xong mới crop.
2. Ảnh nguồn khác tỉ lệ đích: crop thông minh giữ chủ thể sản phẩm ở giữa/1/3 khung; nếu crop sẽ mất chi tiết quan trọng (nhãn, logo, toàn bộ sản phẩm), dùng nền phụ (blur từ chính ảnh hoặc màu nền thương hiệu) lấp phần thừa thay vì crop mất hoặc kéo giãn.
3. Text overlay (tên/giá/CTA) và phụ đề không được đặt trùng vùng an toàn của nền tảng đích — kiểm tra ở Bước H (`references/kiem-tra-chat-luong-tu-dong.md`).

## Đặt tên file xuất

`<ma_san_pham>_<nen_tang>.mp4`, ví dụ:

- `SP001_tiktok.mp4`
- `SP001_facebook_feed.mp4`
- `SP001_facebook_reels.mp4`

Nếu người dùng chỉ yêu cầu 1 nền tảng, chỉ xuất đúng 1 file đó — không tự xuất thêm định dạng chưa được yêu cầu.
