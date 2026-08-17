# Trộn âm thanh (giọng đọc + nhạc nền + âm thanh gốc)

Nguyên tắc gốc: **giọng đọc luôn là lớp âm thanh ưu tiên cao nhất** — người xem phải nghe rõ lời đọc ở mọi thời điểm nó đang phát.

## Mức âm lượng tham khảo

- **Giọng đọc (thuyết minh)**: chuẩn phát thanh/lồng tiếng thường quanh **-16 đến -19 LUFS** integrated — to hơn nhạc nền rõ rệt, đủ rõ trên loa điện thoại.
- **Nhạc nền khi KHÔNG có giọng đọc** (đoạn mở đầu/kết, khoảng nghỉ): có thể để tự nhiên, quanh -18 đến -20 LUFS.
- **Nhạc nền khi CÓ giọng đọc đè lên** (ducking): hạ xuống còn khoảng **-28 đến -32 LUFS**, hoặc giảm ~12–15dB so với mức gốc — đủ nghe thấy không khí/nhịp điệu nhưng không cạnh tranh với giọng đọc.
- **Âm thanh gốc của video** (tiếng động trường quay, tiếng ồn hiện trường) khi có giọng đọc đè lên: hạ tương tự nhạc nền, trừ khi âm thanh gốc chính là nội dung cần nghe (ví dụ tiếng người phát biểu quan trọng) — trường hợp đó nên tránh đọc đè lên, hoặc hỏi người dùng muốn ưu tiên bên nào.

## Cách thực hiện bằng ffmpeg (qua video-use)

- **Ducking tĩnh theo từng đoạn** (đơn giản, đủ dùng khi biết chính xác khoảng thời gian giọng đọc phát): dùng filter `volume` áp theo từng khoảng thời gian cụ thể của nhạc nền/âm thanh gốc — hạ khi trùng đoạn giọng đọc, giữ nguyên khi không trùng.
- **Sidechain compression** (`sidechaincompress`, nhạc nền làm input bị nén, giọng đọc làm sidechain kích hoạt): tự động hạ nhạc nền mỗi khi giọng đọc có tín hiệu — mượt hơn ducking tĩnh, phù hợp khi giọng đọc và nhạc nền xen kẽ nhiều lần trong video dài.
- Luôn **fade nhẹ 30–50ms** tại các điểm chuyển mức âm lượng để tránh tiếng "cắt" đột ngột (áp dụng nguyên tắc fade của `video-use`).

## Thứ tự xử lý

1. Chuẩn hoá loudness giọng đọc trước (đưa về mức mục tiêu cố định).
2. Đặt giọng đọc vào đúng vị trí trên timeline theo [dong-bo-loi-doc-hinh-anh.md](dong-bo-loi-doc-hinh-anh.md).
3. Áp ducking cho nhạc nền/âm thanh gốc dựa trên các khoảng thời gian giọng đọc đã đặt.
4. Trộn tất cả các lớp, đo loudness tổng thể đầu ra, chỉnh lại nếu giọng đọc bị át ở bất kỳ đoạn nào.

## Kiểm tra trước khi giao

- [ ] Nghe/kiểm tra từng đoạn có giọng đọc: lời đọc luôn rõ hơn nhạc nền/âm thanh gốc.
- [ ] Không có tiếng "bụp/cắt" tại điểm chuyển âm lượng.
- [ ] Đoạn không có giọng đọc: nhạc nền/âm thanh gốc trở lại mức tự nhiên, không bị nhỏ bất thường.
- [ ] Loudness tổng thể phù hợp nền tảng đăng (tham khảo chuẩn -14 LUFS integrated cho mạng xã hội, nhưng ưu tiên nghe thử thực tế hơn là chỉ theo số đo).
