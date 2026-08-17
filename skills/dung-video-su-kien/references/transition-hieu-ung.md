# Hiệu ứng chuyển cảnh (transition)

Quan sát từ video mẫu: giữa 2 phân đoạn có tính chất khác nhau rõ rệt (ví dụ từ cảnh hội trường sang cảnh khai mạc sân khấu lớn), video dùng 1 hiệu ứng chuyển cảnh có chủ đích thay vì cắt cứng — quan sát được 2 biến thể trong cùng video mẫu:

## Biến thể A — "Xé/nứt" dọc khung hình

- Một vệt đen dạng vết nứt/xé giấy chạy dọc theo chiều cao khung hình, lan rộng dần từ giữa ra hai bên.
- Trong lúc vệt xé lan rộng, lộ ra cảnh tiếp theo ở phía sau (giống hiệu ứng "xé màn hình" lộ cảnh mới).
- Thời lượng ngắn, khoảng 0.5–1 giây.

## Biến thể B — "Lửa/ánh sáng bùng cháy"

- Hiệu ứng ánh sáng/lửa (glow vàng cam, có khói/hạt sáng bay) chiếm trọn khung hình trong khoảnh khắc chuyển cảnh, tạo cảm giác bùng nổ trước khi hiện cảnh mới.
- Thường dùng ở điểm chuyển cao trào (ví dụ trước đoạn trao giải hoặc trước đoạn hero-intro cuối).

## Nguyên tắc sử dụng

- Chỉ dùng transition có hiệu ứng ở các điểm chuyển **phân đoạn lớn** (tối đa 2–3 lần trong cả video) — không lạm dụng giữa các cảnh nhỏ trong cùng phân đoạn, vì sẽ làm video rối mắt.
- Hiệu ứng luôn đi kèm/đồng bộ với nhịp nhạc nền tại điểm chuyển (nhạc thường có 1 tiếng "hit"/nhấn mạnh đúng lúc transition xảy ra) — đây là quy ước dựng phim phổ biến, không phải trích xuất trực tiếp từ nhạc gốc của video mẫu (xem ghi chú giới hạn trong SKILL.md).

## Gợi ý dựng bằng công cụ

- Đây là hiệu ứng cần asset overlay có sẵn (video lửa/ánh sáng dạng luma matte hoặc additive blend, video vết nứt/xé dạng alpha mask) — tìm/giải quyết qua skill `media-use` (resolve overlay/SFX từ kho có sẵn) thay vì tự vẽ from scratch.
- Ghép luma/alpha mask lên điểm cắt: dùng `hyperframes-animation` (mask reveal, seek-safe) nếu dựng trong HyperFrames, hoặc filter blend/luma của `video-use`/ffmpeg nếu compose trực tiếp lên clip đã quay.
- Nếu không có asset overlay phù hợp, phương án đơn giản hơn: dùng crossfade nhanh (0.3–0.5s) kèm 1 flash trắng ngắn tại điểm cắt — tạo cảm giác chuyển cảnh có chủ đích mà không cần asset phức tạp.
