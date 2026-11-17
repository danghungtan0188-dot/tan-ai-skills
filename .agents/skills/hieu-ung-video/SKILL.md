---
name: hieu-ung-video
description: Công thức hiệu ứng kiểu CapCut chạy được ngay bằng ffmpeg/HyperFrames — chuyển cảnh, chữ động, filter màu, Ken Burns/zoom/pan, sticker/icon, chỉnh hình. Dùng khi muốn thêm một hiệu ứng cụ thể vào clip hoặc tái tạo hiệu ứng thấy trong video tham khảo. Không dùng cho phong cách thẻ/title (motion-graphics-tan), hiệu ứng đặt sau người nói (video-marketing) hay cả timeline nhiều hiệu ứng (chuyen-gia-edit-video-tan).
---

# Thư viện hiệu ứng video (kiểu CapCut)

## Phạm vi

Hỗ trợ: tra và áp dụng công thức ffmpeg/HyperFrames cho các nhóm hiệu ứng phổ biến trong CapCut — Transitions (chuyển cảnh), Text (chữ/hoạt hình chữ), Filters (bộ lọc màu), Effects/Adjustment (chuyển động camera, hiệu chỉnh hình ảnh), Stickers (icon/nhãn overlay). Đây là **thư viện công thức**, không phải quy trình dựng hoàn chỉnh — dùng kết hợp với `bien-tap-video`/`video-thuyet-minh` cho toàn bộ video, hoặc dùng lẻ khi chỉ cần 1 hiệu ứng.

Không làm: không tự bịa hiệu ứng không có thật trong CapCut/công thức ffmpeg đã kiểm chứng; không tự render toàn bộ video (chỉ áp hiệu ứng lên đoạn/clip được chỉ định, người dùng hoặc skill gọi quyết định bố cục tổng thể); không dùng sticker/logo có bản quyền của bên thứ ba khi chưa được phép — sticker/icon tự dựng bằng shape+text (như đã làm trong dự án), không tải ảnh logo ngoài.

## Danh mục hiệu ứng

| Nhóm (kiểu CapCut) | File tham khảo | Ví dụ |
|---|---|---|
| **Intro, kết, chuyển cảnh zoom kiểu truyền hình** | [references/intro-truyen-hinh.md](references/intro-truyen-hinh.md) | công thức intro trailer 18 s (con số → tường ảnh → bộ đếm → đỉnh), intro ẩn dụ phóng sự, logo tài trợ + ident đài 8 s, bố cục vuông 1:1, 6 kiểu chuyển cảnh zoom + công thức ffmpeg zoom xuyên đã chạy thử |
| **Bảng 8 mục CapCut** — tra nhanh đã có gì, lấy thêm ở đâu | [references/lam-nhu-capcut.md](references/lam-nhu-capcut.md) | Text, Stickers, Effects, Transitions, Captions, Filters, Adjustment, Templates; 248 chuyển cảnh gl-transitions; khi nào phải dựng trong CapCut |
| **Transitions** — chuyển cảnh | [references/chuyen-canh.md](references/chuyen-canh.md) | fade, dissolve, wipe, slide, circle open/close, zoom |
| **Transitions GPU kiểu CapCut** (chưa chạy trên máy này) | [references/chuyen-canh-gpufx.md](references/chuyen-canh-gpufx.md) | 154 chuyển cảnh cùng tên CapCut: Film Wipe, TV Glitch, Snap Zoom, Heart Wipe… cần bản FFmpeg có `gpufx` |
| **Text** — chữ & hoạt hình chữ | [references/chu-va-hoat-hinh.md](references/chu-va-hoat-hinh.md) | tiêu đề tĩnh, banner/lower-third, typewriter, pop-in, fade-in chữ |
| **Filters** — bộ lọc màu | [references/bo-loc-mau.md](references/bo-loc-mau.md) | vintage/retro, đen-trắng, ấm/lạnh, teal-orange điện ảnh, vignette |
| **Effects/chuyển động camera** | [references/chuyen-dong-camera.md](references/chuyen-dong-camera.md) | Ken Burns (zoom/pan ảnh tĩnh), speed ramp, freeze frame, slow-motion |
| **Stickers/icon overlay** | [references/nhan-dan-sticker.md](references/nhan-dan-sticker.md) | icon mạng xã hội, nhãn/badge, khung viền |
| **Adjustment** — hiệu chỉnh hình ảnh | [references/hieu-chinh.md](references/hieu-chinh.md) | sáng/tương phản/bão hòa, làm nét, giảm rung (kèm cảnh báo rủi ro) |
| **Rút từ video mẫu** | [references/ky-thuat-tu-video-mau.md](references/ky-thuat-tu-video-mau.md) | mây mở cảnh, dải nét xoay, cửa mở, gương/vạn hoa, bloom, ảnh khung nghiêng, khung dọc 9:16, hai dải, lưới 3×2, chữ lồng video, nhịp cắt theo loại video, bản đồ hành trình đường đỏ, bản đồ vệ tinh giải thích quy hoạch (dọc); mẫu Remotion `TranhGiay` (intro tranh giấy), `AnhBayVao` (ảnh bay vào rồi phóng to), `HudDemSo` (vòng HUD đếm số, vỡ ô lộ logo) và `GhepCanh` (nối ảnh/clip bằng chuyển cảnh chính thức của Remotion + vệt sáng); montage glitch nhịp "dồn – nghỉ – dồn" kiểu promo đài |
| **Học từ HyperFrames** | [references/hoc-tu-hyperframes.md](references/hoc-tu-hyperframes.md) | nguyên tắc dựng tua-được, lệnh CLI, 455 mẫu registry chọn theo nhu cầu, 49 luật chuyển động, bảng ánh xạ hiệu ứng video mẫu → mẫu HyperFrames, khi nào dùng ffmpeg/Remotion/HyperFrames |
| **Học từ OpenMontage + Diagram Design** | [references/hoc-tu-openmontage-va-diagram-design.md](references/hoc-tu-openmontage-va-diagram-design.md) | nguồn tư liệu miễn phí, cách tả ô cảnh để tìm B-roll, nguyên tắc vẽ sơ đồ gọn (tối đa 9 khối, 1–2 điểm nhấn) |

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
