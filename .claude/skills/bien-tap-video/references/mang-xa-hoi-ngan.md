# Chủ đề: Nội dung mạng xã hội ngắn (Reels/TikTok/Shorts)

Dùng khi nội dung không khớp rõ với các chủ đề chuyên biệt khác (không phải sự kiện, quảng cáo, vlog, tutorial, đám cưới, thể thao, ẩm thực) — ví dụ: clip hài, trend, đời sống thường ngày, meme, thử thách.

## Dấu hiệu nhận diện

Thời lượng rất ngắn (dưới 60–90s), khung hình dọc (9:16), nhịp cực nhanh, thường có nhạc/trend đang thịnh hành, mục tiêu giữ chân người xem trong vài giây đầu.

## Cấu trúc gợi ý

1. **Hook 1–2 giây đầu** — bắt buộc, quyết định người xem có lướt qua hay không. Có thể là câu hỏi, hình ảnh gây tò mò, hoặc mâu thuẫn thị giác.
2. **Nội dung chính cực ngắn gọn** — đi thẳng vào trọng tâm, không có phần dạo đầu dài dòng.
3. **Twist/cao trào/điểm bất ngờ** — nếu nội dung có yếu tố giải trí, đặt điểm bất ngờ ở khoảng 60–80% thời lượng.
4. **Kết nhanh** — không cần outro dài; có thể kết bằng câu chốt/CTA ngắn (theo dõi, để lại bình luận).

## Nhịp cắt

Cực nhanh, hầu như không có khoảng lặng; cắt bỏ mọi phần thừa không phục vụ hook hoặc cao trào.

## Màu sắc

Bắt mắt, tương phản/bão hòa cao để nổi bật khi lướt feed nhanh; đồng nhất với phong cách kênh nếu người dùng có kênh riêng.

## Đồ họa/overlay

Phụ đề động (animated captions) gần như bắt buộc — chữ lớn, có thể đổi màu/nhấn theo từ khóa; hạn chế logo/watermark che nội dung.

## Nhạc nền (đề xuất chung)

Ưu tiên nhạc/âm thanh đang thịnh hành trên nền tảng dự định đăng (nếu người dùng có chỉ định); nhịp nhạc phải khớp với hook và điểm cao trào.

## Lưu ý

Định dạng dọc 1080x1920 (9:16); nếu nguồn là video ngang, cần lên kế hoạch reframe/crop hợp lý thay vì để viền đen — phối hợp với `media-use` hoặc `video-use` cho bước reframe.

## Luật giữ người xem — bổ sung (học từ `iart-ai/tiktok-video-skills`, MIT, 10/2026)

Đơn vị làm việc là **đường giữ chân từng giây**, không phải từng cú cắt: một bản dựng "xấu" mà giữ được người xem thắng bản đẹp mà tụt ở giây thứ 4.

- **Một ý mỗi video.** Không nói được điều người xem mang về trong một câu thì chưa có video; ý thứ hai làm video khác.
- **Mở "vòng tò mò" trong ~3 giây đầu, đóng ở cuối** — không trả lời sớm, không chôn phần đáp dưới phần dẫn.
- **Khung đầu tiên là khung mạnh nhất, câu móc câu hiện bằng chữ ngay khung 1** (đa số xem tắt tiếng). **Không mờ dần từ đen.**
- Kiểu móc câu: vòng mở ("Lý do thật khiến…"), hứa thẳng ("3 cách … trong 30 giây"), phủ định ("Đừng … nữa"), cái giá ("Việc này tốn … — đừng lặp lại"), danh sách ("3 … (cái thứ 3 …)"), ngắt nhịp hình (phóng giật / lia nhanh ở khung 1).
- **Ngắt nhịp mỗi 2–4 giây và để KHÔNG đều** (đều như máy đếm nhịp đọc ra là chán): cắt cứng, phóng giật 112 %, chèn b-roll, tiếng động, phụ đề bật, đổi góc. Phóng giật là ngắt nhịp rẻ nhất, không cần cảnh mới.
- **Vòng lặp:** khung cuối khớp khung đầu (cùng bố cục, vị trí, màu) hoặc câu cuối nối vào câu đầu; video lặp tốt nhất dài ~7–15 giây.
- **Vùng an toàn 9:16 (1080×1920):** nội dung chính trong hộp giữa **900×1400**; chừa trên ~120 px, **dưới ~320 px** (phụ đề/nút của nền tảng), phải ~120 px (cột like/bình luận).
- **Phụ đề:** lấy **mốc từng chữ thật từ phiên âm** (whisper), không chia đều câu theo thời lượng — lệch nhìn ra ngay; 1–4 chữ mỗi trang; chữ đậm không chân 56–80 px, viền 2–6 px + bóng; nằm ở ~62–70 % chiều cao.
- **Đọc đường giữ chân:** tụt ở 0–2 giây → đổi câu móc câu, bỏ đoạn mở chậm; phẳng rồi tụt giữa bài → thêm ngắt nhịp, cắt dày 2–4 giây; nhích lên gần cuối → người xem đang xem lại, rút ngắn và làm vòng lặp kín hơn.
- **Kiểm bằng 3 khung tĩnh** trước khi render: khung móc câu (đọc được ngay), khung giữa, khung cuối (so với khung đầu nếu làm vòng lặp).
