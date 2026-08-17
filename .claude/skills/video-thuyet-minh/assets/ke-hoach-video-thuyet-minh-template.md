# Kế hoạch video thuyết minh

> Điền các mục trong ngoặc `[...]`. Đánh dấu `[Chưa xác nhận]` cho phần chưa được người dùng xác nhận, không tự bịa.

## Thông tin chung

- **File kịch bản gốc**: [đường dẫn .txt/.docx]
- **Giọng đọc**: [nam miền Nam (Minh Triết) / nữ miền Nam (Thùy Dung) / giọng nhân bản: tên]
- **Nguồn hình ảnh**: [video/footage có sẵn tại: ... / cần dựng đồ họa / kết hợp cả hai]
- **Chủ đề hình ảnh (theo bien-tap-video)**: [từ assets/bang-nhan-dien-chu-de.md của bien-tap-video]
- **Có nhạc nền không**: [Có, nguồn: ... / Không]
- **Định dạng xuất**: [ngang 1920x1080 / dọc 1080x1920], nền tảng đăng: [...]

## Bảng đồng bộ lời đọc – hình ảnh

| # | Đoạn kịch bản (tóm tắt) | Thời lượng audio | Cảnh hình tương ứng | Điểm cắt hình | Ghi chú |
|---|---|---|---|---|---|
| 1 | [tóm tắt câu/đoạn] | [Xs] | [mô tả cảnh / nguồn file + timestamp] | [cuối câu tại Ys] | [freeze/tăng tốc nếu cần] |

## Kế hoạch trộn âm thanh

- Mức loudness giọng đọc mục tiêu: [-16 đến -19 LUFS]
- Nhạc nền: [có/không, mức ducking khi giọng đọc phát: ...]
- Âm thanh gốc video (nếu có): [giữ/hạ/tắt tại từng đoạn]

## Công cụ dự kiến dùng để thực thi

- [ ] `tan-giong-doc-ban-tin` — tạo file giọng đọc
- [ ] `bien-tap-video` / `dung-video-su-kien` — xử lý/lập kịch bản hình ảnh
- [ ] `video-use` — ghép hình + audio, trộn âm thanh, xuất video cuối
- [ ] `media-use` — nếu cần thêm nhạc nền/SFX hợp lệ bản quyền
- [ ] HyperFrames — nếu cần dựng thêm đồ họa/hình ảnh minh hoạ không có sẵn footage

## Kiểm tra trước khi giao

- [ ] Lời đọc không bị cắt cụt giữa câu ở bất kỳ điểm chuyển cảnh nào.
- [ ] Hình và lời không lệch nhau ở đoạn nào.
- [ ] Giọng đọc luôn nghe rõ hơn nhạc nền/âm thanh gốc khi đang phát.
- [ ] Đã xác nhận với người dùng về nguồn hình ảnh, không tự bịa cảnh quay không có thật.
