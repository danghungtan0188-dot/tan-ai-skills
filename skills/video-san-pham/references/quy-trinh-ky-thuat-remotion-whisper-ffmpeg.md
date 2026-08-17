# Quy trình kỹ thuật: Remotion + Whisper + FFmpeg trong skill này

Yêu cầu gốc dùng bộ ba "Remotion + Whisper + FFmpeg". Tài liệu này giải thích từng vai trò được thực hiện cụ thể bằng công cụ/skill nào đã có sẵn trong repo, để không tạo ra một pipeline mới trùng lặp.

## 1. Remotion / HyperFrames — dựng cảnh có chuyển động từ ảnh tĩnh

Ảnh sản phẩm là ảnh tĩnh; video cần chuyển động để không nhàm chán. Hai lựa chọn engine, chọn 1 theo tình huống:

- **HyperFrames** (skill `hyperframes` → route `general-video` hoặc `product-launch-video`) — ưu tiên khi cần dựng nhanh, composition HTML/CSS/GSAP, kiểm tra bằng `hyperframes lint`/`check`/`preview` trước khi render. Phù hợp phần lớn video sản phẩm ngắn kiểu này.
- **Remotion thuần** (`remotion-create` để khởi tạo project, `remotion-captions` để hiển thị phụ đề đúng type `Caption`, `remotion-render` để xuất) — chọn khi người dùng yêu cầu cụ thể Remotion/React hoặc đã có hệ thống component Remotion sẵn.

Trong cả hai trường hợp, kỹ thuật "biến ảnh tĩnh thành cảnh có chuyển động":

- Ken Burns cơ bản: `scale` từ 1.0 → 1.06–1.1 và `translate` nhẹ trong suốt thời lượng cảnh, easing `ease-out cubic` (không dùng `linear`, xem `hyperframes-animation`).
- Ảnh không đúng tỉ lệ khung hình đích (vd. ảnh vuông cho khung dọc 9:16): **crop thông minh giữ chủ thể sản phẩm ở giữa khung** là lựa chọn mặc định; dùng nền blur từ chính ảnh gốc hoặc màu nền thương hiệu làm khung phụ khi crop sẽ cắt mất phần sản phẩm quan trọng. Không bao giờ kéo giãn (stretch) ảnh làm méo tỉ lệ — vi phạm Nguyên tắc cứng #4 trong SKILL.md.
- Overlay tên/giá/CTA: đặt ở vùng an toàn theo nền tảng đích (xem [dinh-dang-xuat-tiktok-facebook.md](dinh-dang-xuat-tiktok-facebook.md)), áp **trước** phụ đề trong thứ tự layer.
- Số ảnh tối thiểu cho một video 15–30s: ít nhất 2–3 ảnh khác góc/khác chi tiết sản phẩm để có nhịp chuyển cảnh; nếu Excel chỉ có 1 ảnh, hỏi người dùng có ảnh khác không thay vì kéo dài 1 cảnh quá lâu (>8–10s một ảnh tĩnh dễ nhàm).

## 2. Whisper / ASR cấp từ — đồng bộ phụ đề chính xác

Vai trò "Whisper" trong yêu cầu gốc là: chuyển giọng đọc thành timestamp cấp từ để phụ đề khớp chính xác, không cần đếm nhịp thủ công. Trong repo này thực hiện qua:

- **`video-use` `helpers/transcribe.py`** — gọi ASR cấp từ (hosted, có confidence + timestamp per word), kết quả cache theo nguồn để không phiên âm lại nếu file audio không đổi.
- **`hyperframes-cli transcribe`** — lựa chọn thay thế nếu đang làm việc trong composition HyperFrames.

Quy tắc bắt buộc: transcribe **chính file giọng đọc vừa tổng hợp ở Bước C** (không phải transcribe kịch bản gốc dạng text) — vì thời lượng thực tế của từng từ phụ thuộc vào tốc độ đọc thật của giọng TTS, không phải ước lượng từ độ dài chữ. Output là danh sách `{text, startMs, endMs}` theo type `Caption` của `remotion-captions`, dùng trực tiếp cho Bước E.

Nếu ASR trả về confidence thấp cho một cụm từ (ví dụ tên thương hiệu, số liệu kỹ thuật khó phát âm): đối chiếu lại bằng tai (nghe lại đoạn audio đó) trước khi tin timestamp, không tự động chấp nhận nếu nghi ngờ sai.

## 3. FFmpeg — ghép, nén, xuất đúng thông số nền tảng

Vai trò "FFmpeg" thực hiện qua `video-use` (`render.py` và các helper liên quan), vốn đã đóng gói đúng các quy tắc đúng đắn kỹ thuật (Hard Rules) của `video-use`:

- Phụ đề áp **sau cùng** trong chuỗi filter (nếu áp trước, overlay che mất phụ đề — lỗi âm thầm, không báo lỗi rõ ràng).
- Fade audio 30ms tại mọi điểm nối để tránh tiếng "pop".
- Trích đoạn từng phần rồi ghép `-c copy` khi có nhiều cảnh, tránh encode lại nhiều lần.

Sau khi xuất, `scripts/kiem_tra_dau_ra.py` của skill này gọi `ffprobe` (đi kèm ffmpeg) để tự động đối chiếu độ phân giải, tỉ lệ khung hình và thời lượng file xuất với kế hoạch đã duyệt — đây là bước tự kiểm tra khoa học thay vì chỉ tin bằng mắt.

## Vì sao ánh xạ thế này thay vì cài đặt riêng "Whisper" và "Remotion" từ đầu

Repo đã có `video-use` (ASR cấp từ + FFmpeg pipeline đã kiểm chứng qua Hard Rules) và `remotion-*`/`hyperframes` (dựng cảnh lập trình đã kiểm chứng). Dựng lại một pipeline Whisper/Remotion/FFmpeg độc lập sẽ trùng lặp và mất đi các quy tắc đúng đắn (đồng bộ phụ đề, chống pop âm thanh, chống double-encode) mà các skill kia đã đúc kết. Skill `video-san-pham` chỉ thêm phần các skill kia chưa tự làm: đọc dữ liệu Excel/ảnh theo sản phẩm, viết kịch bản đúng dữ liệu thật, và tự kiểm tra đầu ra theo kế hoạch đã duyệt.
