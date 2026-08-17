# Overlay gameshow (phần thi kiến thức)

Quan sát từ video mẫu: trong đoạn thi kiến thức, video thật (người dự thi đứng trên sân khấu) được giữ nguyên làm nền, và 2 lớp đồ họa chồng lên trên:

## Lớp 1 — Đồng hồ đếm ngược

- Vị trí: góc trên bên phải khung hình.
- Hình thức: khung số dạng đồng hồ điện tử (digital), nền tối, chữ số sáng, đơn vị hiển thị `MM:SS` (ví dụ `03:48`).
- Có thể kèm nhãn nhỏ phía trên như "Thời gian trả lời câu hỏi".
- Không che mặt người thi — luôn đặt ở góc trống của khung hình.

## Lớp 2 — Khung câu hỏi trắc nghiệm

- Vị trí: dải ngang phía trên hoặc giữa khung hình, nền bán trong suốt (đen ~60–70% opacity) để chữ trắng nổi bật mà vẫn thấy được video nền phía sau.
- Nội dung: câu hỏi đầy đủ + các phương án trả lời (dạng liệt kê ngắn, có thể đánh số hoặc icon lựa chọn như nút "Trả lời").
- Font: rõ ràng, dễ đọc ở kích thước nhỏ trên di động (ưu tiên chữ không chân, cỡ đủ lớn).
- Câu hỏi giữ nguyên trên màn hình trong suốt thời gian đếm ngược, không đổi giữa chừng.

## Nguyên tắc phối hợp 2 lớp

- Đồng hồ đếm ngược và khung câu hỏi xuất hiện/biến mất cùng lúc, đồng bộ với hành động thật trên sân khấu (người dẫn chương trình đọc câu hỏi → overlay xuất hiện → hết giờ → overlay biến mất, cắt sang cảnh khác).
- Đây là lớp đồ họa động (motion graphic), không phải phụ đề tĩnh — cần dựng riêng rồi compose lên video gốc, không chèn text tĩnh đơn giản.

## Gợi ý dựng bằng công cụ

- Dựng bằng HyperFrames: tạo 1 sub-composition riêng cho "quiz overlay" gồm 2 track (đồng hồ đếm ngược dùng biến đếm thời gian thật, khung câu hỏi dùng `class="clip"` xuất hiện/biến mất theo `data-*` timing) — tham khảo `hyperframes-core` cho cấu trúc composition và `hyperframes-animation` cho cách hiện/ẩn overlay mượt.
- Dựng bằng Remotion: dùng `remotion-interactivity` nếu cần logic đếm ngược có thể tái sử dụng nhiều lần trong video, `remotion-markup` cho bố cục khung câu hỏi.
- Ghép overlay đã dựng lên clip quay thật: dùng skill `video-use` để compose lớp đồ họa lên đúng khoảng thời gian trên timeline gốc.
