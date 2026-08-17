# Đồng bộ lời đọc với hình ảnh

Nguyên tắc gốc: **audio giọng đọc là trục thời gian chính**, hình ảnh phải khớp theo, không phải cắt hình ảnh tự do rồi ép giọng đọc vào cho vừa.

## Quy trình đo thời lượng

1. Sau khi `tan-giong-doc-ban-tin` xuất audio, mỗi đoạn kịch bản (ngăn bởi dòng trống) tương ứng với 1 đoạn audio có thời lượng xác định — lấy thời lượng chính xác bằng `ffprobe` trên từng file đoạn (nếu script xuất riêng từng đoạn) hoặc note lại timestamp ghép nối nếu xuất 1 file duy nhất.
2. Với mỗi đoạn kịch bản, xác định đoạn hình ảnh tương ứng về mặt nội dung (cảnh nào minh hoạ đúng ý đang đọc).

## Khi hình ảnh ngắn hơn lời đọc

Ưu tiên theo thứ tự (không tự chọn phương án nếu có thể hỏi người dùng khi ảnh hưởng lớn đến nội dung):
1. Kéo dài cảnh bằng cách giữ khung hình cuối (freeze frame) 1–2 giây nếu chênh lệch nhỏ (<2s).
2. Chèn thêm cảnh liên quan khác (nếu có) để lấp khoảng trống.
3. Nếu chênh lệch lớn, báo người dùng: cảnh hiện có không đủ để minh hoạ toàn bộ đoạn lời đọc, hỏi có cảnh khác không hoặc có nên rút gọn đoạn kịch bản đó không.

## Khi hình ảnh dài hơn lời đọc

1. Cắt bớt phần hình ảnh ít thông tin nhất trong cảnh (ví dụ giữ đầu/cuối, cắt đoạn giữa lặp lại).
2. Nếu cảnh có nhịp độ nhanh (ví dụ b-roll), có thể tăng tốc nhẹ (dưới 1.2x) để vừa khít — không tăng tốc cảnh có người nói/hành động rõ ràng vì sẽ trông kỳ quặc.
3. Không kéo dài lời đọc bằng cách chèn khoảng lặng giả tạo giữa câu — nghe không tự nhiên; khoảng lặng chỉ nên xảy ra tại ranh giới câu/đoạn tự nhiên.

## Điểm cắt hình ảnh nên khớp với điểm ngắt câu của lời đọc

- Cắt cảnh tại **cuối câu hoặc cuối mệnh đề** của lời đọc — giống nguyên tắc "audio-first" trong `video-use` (cắt tại ranh giới từ/câu, không cắt giữa từ).
- Nếu 1 đoạn kịch bản dài minh hoạ bằng nhiều cảnh khác nhau, đổi cảnh tại các dấu phẩy/dấu chấm tự nhiên trong câu, không đổi cảnh tuỳ tiện giữa chừng.

## Bàn giao cho video-use

Khi gọi `video-use` để thực thi, cung cấp: audio giọng đọc đã có sẵn thời lượng cố định (không co giãn), danh sách cảnh đã ánh xạ theo từng đoạn kèm thời lượng mục tiêu, và điểm cắt đã xác định ở trên — để `video-use` build EDL đúng theo timeline lời đọc thay vì tự chọn cắt theo nhịp hình ảnh độc lập.
