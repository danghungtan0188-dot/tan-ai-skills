---
name: hieu-ung-video
description: Thư viện hiệu ứng dựng video kiểu CapCut/CupCut — chuyển cảnh (transition), hoạt hình chữ, bộ lọc màu (filter), chuyển động camera (Ken Burns/zoom/pan), sticker/icon overlay, và hiệu chỉnh hình ảnh (adjustment) — mỗi hiệu ứng có công thức ffmpeg/HyperFrames thực thi được ngay, không chỉ mô tả suông. Kích hoạt khi người dùng muốn thêm hiệu ứng/effect vào video, hỏi "làm sao có hiệu ứng như CapCut", muốn transition/chuyển cảnh cụ thể, chữ động, filter màu, zoom/pan ảnh, sticker/icon, hoặc muốn tái tạo hiệu ứng thấy trong 1 video tham khảo. Đây là thư viện công thức (cookbook) — được `bien-tap-video`, `dung-video-su-kien`, `video-thuyet-minh`, `video-san-pham` gọi tới khi cần 1 hiệu ứng cụ thể, cũng dùng được trực tiếp khi người dùng chỉ cần 1 hiệu ứng đơn lẻ trên 1 clip.
---

# Thư viện hiệu ứng video (kiểu CapCut)

## Phạm vi

Hỗ trợ: tra và áp dụng công thức ffmpeg/HyperFrames cho các nhóm hiệu ứng phổ biến trong CapCut — Transitions (chuyển cảnh), Text (chữ/hoạt hình chữ), Filters (bộ lọc màu), Effects/Adjustment (chuyển động camera, hiệu chỉnh hình ảnh), Stickers (icon/nhãn overlay). Đây là **thư viện công thức**, không phải quy trình dựng hoàn chỉnh — dùng kết hợp với `bien-tap-video`/`video-thuyet-minh` cho toàn bộ video, hoặc dùng lẻ khi chỉ cần 1 hiệu ứng.

Không làm: không tự bịa hiệu ứng không có thật trong CapCut/công thức ffmpeg đã kiểm chứng; không tự render toàn bộ video (chỉ áp hiệu ứng lên đoạn/clip được chỉ định, người dùng hoặc skill gọi quyết định bố cục tổng thể); không dùng sticker/logo có bản quyền của bên thứ ba khi chưa được phép — sticker/icon tự dựng bằng shape+text (như đã làm trong dự án), không tải ảnh logo ngoài.

## Danh mục hiệu ứng

| Nhóm (kiểu CapCut) | File tham khảo | Ví dụ |
|---|---|---|
| **Transitions** — chuyển cảnh | [references/chuyen-canh.md](references/chuyen-canh.md) | fade, dissolve, wipe, slide, circle open/close, zoom |
| **Text** — chữ & hoạt hình chữ | [references/chu-va-hoat-hinh.md](references/chu-va-hoat-hinh.md) | tiêu đề tĩnh, banner/lower-third, typewriter, pop-in, fade-in chữ |
| **Filters** — bộ lọc màu | [references/bo-loc-mau.md](references/bo-loc-mau.md) | vintage/retro, đen-trắng, ấm/lạnh, teal-orange điện ảnh, vignette |
| **Effects/chuyển động camera** | [references/chuyen-dong-camera.md](references/chuyen-dong-camera.md) | Ken Burns (zoom/pan ảnh tĩnh), speed ramp, freeze frame, slow-motion |
| **Stickers/icon overlay** | [references/nhan-dan-sticker.md](references/nhan-dan-sticker.md) | icon mạng xã hội, nhãn/badge, khung viền |
| **Adjustment** — hiệu chỉnh hình ảnh | [references/hieu-chinh.md](references/hieu-chinh.md) | sáng/tương phản/bão hòa, làm nét, giảm rung (kèm cảnh báo rủi ro) |

Xem nhanh toàn bộ tên hiệu ứng trong [assets/thu-vien-hieu-ung.md](assets/thu-vien-hieu-ung.md).

## Quy trình sử dụng

1. **Xác định hiệu ứng cần** — nếu người dùng chỉ vào 1 video tham khảo ("làm như video này"), trích khung hình/xem đoạn có hiệu ứng để nhận diện đúng nhóm (dùng cách trích contact sheet đã mô tả trong `dung-video-su-kien`), rồi tra bảng danh mục ở trên.
2. **Đọc đúng file reference** tương ứng nhóm hiệu ứng, lấy công thức ffmpeg/HyperFrames.
3. **Áp thử trên 1 đoạn ngắn trước**, xuất preview, kiểm tra bằng cách trích khung hình xem kết quả trước khi áp lên cả video — đặc biệt với các hiệu ứng có rủi ro artifact (giảm rung, stabilize) đã ghi rõ trong [references/hieu-chinh.md](references/hieu-chinh.md).
4. **Xác nhận với người dùng** nếu hiệu ứng làm thay đổi lớn (đổi tông màu mạnh, tăng tốc/giảm tốc nhiều) trước khi áp lên toàn video.
5. Bàn giao lại cho skill đang điều phối (`bien-tap-video`/`video-thuyet-minh`/`video-san-pham`) để ghép vào tổng thể, hoặc xuất trực tiếp nếu chỉ làm 1 clip đơn lẻ.

## Xử lý dữ liệu thiếu và giả định

- Không chắc hiệu ứng người dùng mô tả tương ứng công thức nào: hỏi lại hoặc trích khung hình từ video tham khảo để xác nhận trực quan, không tự đoán rồi áp sai.
- Hiệu ứng có rủi ro kỹ thuật cao (giảm rung/stabilize qua nhiều cú cắt cảnh) — đã có bài học thực tế: chạy 1 lần trên đoạn có nhiều cảnh cắt gây vỡ hình nặng. Luôn tách riêng theo từng cảnh liên tục trước khi áp, không chạy 1 lượt xuyên nhiều cảnh cắt khác nhau (xem chi tiết trong [references/hieu-chinh.md](references/hieu-chinh.md)).
- Không có font hỗ trợ tiếng Việt trên máy: kiểm tra `C:\Windows\Fonts` trước, dùng `segoeuib.ttf`/`arialbd.ttf` (đã xác nhận hỗ trợ dấu tiếng Việt).

## Định dạng đầu ra

- Lệnh ffmpeg/HyperFrames cụ thể đã điền tham số đúng theo yêu cầu (không đưa công thức chung chung).
- 1 khung hình/preview ngắn để người dùng xác nhận trước khi áp toàn video.
- Ghi rõ hiệu ứng nào tương đương tên gọi trong CapCut để người dùng dễ đối chiếu (vd. "Dissolve" trong CapCut ≈ `xfade=transition=dissolve` trong ffmpeg).
