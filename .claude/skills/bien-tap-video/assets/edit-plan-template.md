# Kịch bản dựng video (edit plan)

> Điền các mục trong ngoặc `[...]`. Đánh dấu `[Chưa xác nhận]` cho phần chưa được người dùng xác nhận, không tự bịa.

## Thông tin chung

- **File video gốc**: [đường dẫn]
- **Chủ đề nhận diện**: [từ assets/bang-nhan-dien-chu-de.md]
- **Thời lượng gốc / mục tiêu**: [ss gốc] → [ss mục tiêu]
- **Định dạng xuất**: [ngang 1920x1080 / dọc 1080x1920 / vuông 1080x1080], [fps]
- **Nền tảng đăng dự kiến**: [Facebook Reels / TikTok / YouTube / nội bộ / khác]

## Kết quả phân tích (từ scripts/phan_tich_video.py + contact sheet)

- Metadata: [dán JSON kết quả script]
- Mô tả theo từng đoạn quan sát trên contact sheet: [liệt kê]

## Bảng dựng

| # | Thời điểm gốc | Nội dung | Giữ/Cắt/Rút gọn | Hiệu ứng/overlay | Ghi chú màu sắc |
|---|---|---|---|---|---|
| 1 | [mm:ss–mm:ss] | [Mô tả] | [Giữ nguyên/Cắt bỏ/Rút ngắn còn Xs] | [Không/Transition/Text overlay...] | [Theo nguyên tắc chủ đề] |

## Âm thanh

- Giữ âm thanh gốc: [Có/Không, đoạn nào]
- Nhạc nền đề xuất: [mô tả tâm trạng/tempo — ghi rõ đây là gợi ý, chưa xác nhận từ audio gốc nếu chưa nghe]
- Phụ đề: [Có/Không, ngôn ngữ]

## Kiểm tra chất lượng trước khi giao

Dùng đầy đủ checklist trong [../references/nguyen-tac-chat-luong.md](../references/nguyen-tac-chat-luong.md).

## Công cụ dự kiến dùng để thực thi

- [ ] `video-use` — cắt/ghép/màu/phụ đề trên clip thật
- [ ] HyperFrames (`hyperframes`, `hyperframes-animation`, `hyperframes-creative`) — đồ họa động/transition
- [ ] `remotion-*` — nếu dự án đã dùng Remotion
- [ ] `media-use` — nhạc nền/SFX hợp lệ bản quyền
- [ ] Skill `dung-video-su-kien` — nếu chủ đề là sự kiện/hội nghị kiểu Việt Nam
