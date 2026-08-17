# Title card mở đầu (banner giới thiệu)

Quan sát từ video mẫu: title card xuất hiện ngay sau cảnh mở đầu (khán giả vỗ tay), đứng yên hoặc có chuyển động nhẹ (chữ trượt vào/hoa văn lấp lánh), giữ hình khoảng 2–3 giây trước khi cắt sang nội dung.

## Cấu trúc thị giác

- **Banner nền**: dải màu đỏ đô (#8B1A1A – #B22222 tùy sắc thái) trải ngang hoặc dọc, có thể có gradient nhẹ sang vàng ở viền.
- **Khung chữ chính**: tên hội thi/sự kiện, chữ vàng (#F5C518 – #FFD700) hoặc trắng viền vàng, font đậm, chữ hoa toàn bộ hoặc viết hoa đầu câu tùy độ dài.
- **Dòng phụ**: tên đơn vị + "(Lần thứ N) – Năm YYYY" hoặc địa điểm + ngày tháng, cỡ chữ nhỏ hơn dòng chính, đặt ngay dưới.
- **Hoa văn trang trí**: hoa sen cách điệu ở góc hoặc hai bên (biểu tượng phổ biến trong video sự kiện nhà nước Việt Nam), có thể thêm ngôi sao vàng nhỏ hoặc dải lụa đỏ.
- **Nền phía sau chữ**: thường là ảnh mờ (blur) của chính cảnh sự kiện, không dùng nền trơn — tạo cảm giác gắn với nội dung thật.

## Thời lượng và chuyển động

- Hiện: fade-in hoặc trượt từ dưới lên, 0.3–0.5s.
- Giữ hình tĩnh: 2–3 giây, đủ để đọc hết chữ.
- Ẩn: fade-out hoặc cắt cứng sang cảnh tiếp theo.
- Nếu tên sự kiện dài, có thể lặp lại title card ở đầu mỗi phân đoạn lớn (video mẫu dùng lại gần như cùng 1 mẫu title card ở 2–3 thời điểm khác nhau trong video — tại phần thi và tại lễ khai mạc).

## Gợi ý dựng bằng công cụ

- Dựng bằng HyperFrames: dùng `hyperframes-creative` để chọn palette đỏ-vàng và typography, `hyperframes-animation` cho hiệu ứng fade/trượt chữ (2–3 rule motion, không cần nhiều hơn).
- Dựng bằng Remotion: dùng `remotion-markup` cho bố cục banner + chữ, `remotion-create` để khởi tạo composition riêng cho title card rồi ghép vào timeline chính.
- Nếu chỉ cần overlay nhanh lên clip có sẵn (không dựng lại từ đầu): dùng skill `video-use` để chèn lớp text/graphic lên đúng đoạn video.
