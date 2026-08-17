# Tông màu & ánh sáng theo từng loại cảnh

Quan sát từ video mẫu, mỗi phân đoạn có "chữ ký" màu sắc riêng — giữ nhất quán trong cùng 1 phân đoạn, thay đổi rõ rệt khi chuyển phân đoạn để khán giả cảm nhận được sự chuyển nhịp.

| Phân đoạn | Tông màu chủ đạo | Đặc điểm ánh sáng |
|---|---|---|
| Hội trường / phần thi tình huống | Trắng-vàng trung tính, hơi ấm | Ánh sáng đèn huỳnh quang/LED trần, đều, ít bóng đổ |
| Overlay gameshow | Giữ nguyên màu nền cảnh quay + lớp đồ họa tối (đen bán trong suốt) đè lên | Không chỉnh màu thêm ở lớp video nền |
| Phỏng vấn | Tự nhiên ngoài trời hoặc ánh sáng trong nhà không qua xử lý nhiều | Ưu tiên rõ mặt hơn là thẩm mỹ, chấp nhận ánh sáng chưa hoàn hảo |
| Khai mạc / sân khấu lớn | Đỏ-vàng rực, bão hòa cao | Spotlight màu, khói sân khấu, nền tối để đèn nổi bật |
| Trao giải + ăn mừng | Đỏ-vàng ấm, có điểm sáng lấp lánh (đèn nháy/kim tuyến ánh sáng) | Ánh sáng động, không tĩnh — tạo không khí phấn khích |
| Hero-intro cuối | Tương phản cao, có thể ngả teal-orange hoặc vàng nắng chiều | Ánh sáng tự nhiên ngoài trời, bóng đổ rõ, hậu kỳ grade rõ rệt hơn các đoạn khác |

## Nguyên tắc chỉnh màu

- **Không grade lại** cảnh tư liệu/phóng sự (hội trường, phỏng vấn) quá tay — giữ tính chân thực, chỉ cân bằng trắng cơ bản.
- **Grade mạnh tay hơn** ở 2 đoạn mang tính trình diễn/cảm xúc: sân khấu lớn (đẩy bão hòa đỏ-vàng) và hero-intro (đẩy tương phản, có thể thêm ngả màu điện ảnh).
- Giữ **da người tự nhiên** xuyên suốt kể cả khi grade mạnh — không để ám màu lên mặt người.
- Chuyển màu giữa các phân đoạn nên trùng với điểm có transition hiệu ứng (xem [transition-hieu-ung.md](transition-hieu-ung.md)) để sự thay đổi tông màu không bị đột ngột khó chịu.

## Gợi ý dựng bằng công cụ

- Chỉnh màu clip đã quay: dùng skill `video-use` (color grade theo mô tả bảng trên, chỉ định rõ phân đoạn nào cần grade mạnh/nhẹ).
- Chọn palette chuẩn hoá khi dựng đồ họa (title card, overlay): tham khảo `hyperframes-creative` để lấy mã màu nhất quán giữa các lớp đồ họa và footage thật.
