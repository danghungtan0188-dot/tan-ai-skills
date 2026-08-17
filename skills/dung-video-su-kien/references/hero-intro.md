# Đoạn hero-intro cuối video

Quan sát từ video mẫu: đoạn kết không phải cảnh tư liệu thông thường mà là 1 đoạn dàn dựng riêng, tách biệt hẳn về phong cách — giống trailer giới thiệu nhân vật trong phim/MV hơn là phóng sự.

## Cấu trúc cảnh

- Từng thành viên đội xuất hiện riêng lẻ (1 người/cảnh), bước đi về phía máy quay hoặc đứng tại chỗ thực hiện 1 động tác đặc trưng (chào, khoanh tay trước ngực, quay người...).
- Bối cảnh: kiến trúc đẹp/có tính biểu tượng của địa phương (ví dụ công trình màu vàng kiểu Pháp cổ, có cờ Tổ quốc) — không quay trong hội trường, tạo cảm giác "đời thường/tự hào" khác hẳn phần thi đấu.
- Góc máy: trung cảnh đến toàn thân, máy tĩnh hoặc lia nhẹ theo chuyển động của nhân vật.
- Nhịp cắt: chậm hơn phần thi đấu, mỗi nhân vật giữ khoảng 2–3 giây để khán giả nhìn rõ.

## Màu sắc & kết thúc

- Grade màu điện ảnh: tương phản cao hơn, có thể ngả nhẹ về tông teal-orange (da người ấm, nền/bóng đổ ngả lạnh) hoặc giữ tông ấm vàng nắng chiều tùy thời điểm quay.
- Kết thúc bằng title card riêng: nền tối (đen/nâu sẫm), chữ tên đội/đơn vị màu vàng kiểu chữ khắc nổi (có hiệu ứng đổ bóng/ánh kim), căn giữa khung hình — khác hẳn title card mở đầu (đơn giản hơn, ít hoa văn hơn, mang tính "đóng dấu kết thúc").

## Vai trò trong tổng thể video

- Đây là đoạn "đóng đinh cảm xúc" cuối video — không nhằm cung cấp thêm thông tin sự kiện mà để lại ấn tượng về tập thể/đội thi.
- Luôn đặt ở vị trí cuối cùng, sau đoạn trao giải/ăn mừng, không chen giữa các phân đoạn tường thuật.

## Gợi ý dựng bằng công cụ

- Nếu có footage quay sẵn riêng cho đoạn này: dùng skill `video-use` để cắt, chỉnh màu (color grade) theo mô tả trên, và chèn title card kết.
- Nếu cần dựng title card kết dạng chữ khắc/hiệu ứng ánh kim: dùng `hyperframes-animation` (text effect) hoặc `remotion-markup`.
- Đoạn này **cần footage thật đã quay riêng** (không thể tạo hoàn toàn bằng đồ họa) — nếu người dùng chưa có, cần lên kế hoạch quay (shot list riêng, xem [assets/shot-list-template.md](../assets/shot-list-template.md)) trước khi dựng.
