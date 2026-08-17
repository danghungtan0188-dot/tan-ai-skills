# Kế hoạch video sản phẩm

> Điền các mục trong ngoặc `[...]`. Đánh dấu `[Chưa xác nhận]` cho phần chưa được người dùng xác nhận, không tự bịa.

## Thông tin sản phẩm (từ Bước A)

- **Mã sản phẩm**: [ma_san_pham]
- **Tên sản phẩm**: [ten_san_pham]
- **Mô tả ngắn**: [mo_ta_ngan]
- **Tính năng chính**: [tinh_nang_chinh, hoặc "Không có"]
- **Giá**: [gia]
- **Giá khuyến mãi**: [gia_khuyen_mai, hoặc "Không có — kịch bản không nhắc khuyến mãi"]
- **CTA**: [cta, hoặc "Chưa có trong Excel — đề xuất: ..., chờ xác nhận"]
- **Ảnh dùng**: [danh sách file ảnh đã đối chiếu tồn tại]
- **Giọng đọc**: [nam miền Nam / nữ miền Nam / giọng nhân bản: tên]
- **Nền tảng xuất**: [TikTok 1080x1920 / Facebook Feed 1080x1080 / Facebook Reels 1080x1920 — có thể nhiều]

## Kịch bản chờ duyệt (Bước B)

| Đoạn | Nội dung | Thời lượng ước tính |
|---|---|---|
| HOOK | [câu mở đầu 3–5s] | [Xs] |
| GIỚI THIỆU/TÍNH NĂNG | [nội dung] | [Xs] |
| GIÁ/KHUYẾN MÃI | [nội dung, hoặc "Bỏ qua — không có dữ liệu khuyến mãi"] | [Xs] |
| CTA | [nội dung] | [Xs] |

**[ ] Người dùng đã duyệt kịch bản này trước khi sang Bước C.**

## Kế hoạch dựng cảnh (Bước E)

| # | Ảnh dùng | Chuyển động | Overlay | Ghi chú tỉ lệ khung hình |
|---|---|---|---|---|
| 1 | [tên file] | [Ken Burns zoom in nhẹ / pan trái-phải] | [tên/giá/CTA nếu có ở cảnh này] | [crop giữ chủ thể / nền blur nếu ảnh khác tỉ lệ đích] |

## Công cụ dự kiến dùng để thực thi

- [ ] `tan-giong-doc-ban-tin` — tạo giọng đọc
- [ ] `video-use` — ASR cấp từ (Bước D), ghép/nén/xuất (Bước G)
- [ ] `remotion-create`/`remotion-captions`/`remotion-render` hoặc HyperFrames — dựng cảnh (Bước E)
- [ ] `marketing` — kiểm tra rủi ro nội dung (Bước F)
- [ ] `media-use` — nếu cần thêm nhạc nền/SFX hợp lệ bản quyền

## Bước H — Tự kiểm tra đầu ra

- [ ] `scripts/kiem_tra_dau_ra.py` — độ phân giải/thời lượng/có audio track đạt.
- [ ] Đồng bộ audio–phụ đề đạt (kiểm tra 2–3 điểm).
- [ ] Chữ (tên/giá/CTA/phụ đề) không bị cắt/che, không nằm trong vùng an toàn nền tảng.
- [ ] Âm lượng giọng đọc rõ hơn nhạc nền, không có tiếng "pop" tại điểm nối.
- [ ] Giá/tên/CTA hiển thị trên video khớp đúng dữ liệu đã xác nhận ở Bước A.
- [ ] Ảnh không bị kéo giãn méo.
- **Số lần tự sửa đã dùng**: [0/1/2/3] — nếu 3 mà vẫn lỗi, đã báo cụ thể cho người dùng: [mô tả lỗi còn tồn đọng]

## Bàn giao

- **File xuất**: [đường dẫn từng file theo nền tảng]
- **Caption + hashtag gợi ý**: [nội dung ngắn kèm hashtag]
