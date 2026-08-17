---
name: bien-tap-video
description: Skill biên tập video thông minh — khi người dùng đưa vào 1 video (hoặc mô tả video muốn dựng), tự phân tích metadata + khung hình để nhận diện chủ đề (sự kiện/hội nghị, quảng cáo sản phẩm, vlog du lịch, phỏng vấn/tutorial, đám cưới/kỷ niệm gia đình, thể thao/hành động, ẩm thực, nội dung mạng xã hội ngắn dạng Reels/TikTok), rồi áp dụng đúng phong cách dựng (cấu trúc, nhịp cắt, hiệu ứng, màu sắc, nhạc nền, phụ đề) cho chủ đề đó — luôn theo bộ nguyên tắc chất lượng chuyên nghiệp dùng chung. Kích hoạt khi người dùng đưa 1 file video muốn edit/dựng lại, muốn phân tích cách dựng của 1 video, hoặc nói chung chung "edit video này cho hay/chuyên nghiệp" mà chưa nói rõ chủ đề. Skill này là lớp điều phối (router + creative direction) — không tự sở hữu công cụ render; khi thực thi thật, phối hợp với skill video-use (cắt/ghép/màu/phụ đề), HyperFrames (đồ họa động, transition), hoặc remotion-* (dựng lập trình). Với chủ đề sự kiện/hội nghị kiểu Việt Nam, dùng lại skill dung-video-su-kien làm module chi tiết.
---

# Biên tập video thông minh

## Phạm vi

Hỗ trợ: phân tích video đầu vào (metadata + khung hình), nhận diện chủ đề, chọn hướng dựng phù hợp chủ đề, lập kịch bản dựng (edit plan) đạt chất lượng chuyên nghiệp, và điều phối công cụ thực thi (video-use / HyperFrames / remotion-*).

Không làm: không tự sở hữu engine render video (không có khả năng tự xuất file video cuối cùng nếu không gọi qua `video-use`/HyperFrames/remotion); không tự tải hoặc tái sử dụng nội dung có bản quyền của người khác khi chưa được phép; không suy diễn nhạc nền/lời thoại nếu chưa thực sự trích xuất/nghe được; không bịa thông tin về nội dung video (tên người, địa điểm, sự kiện) khi không quan sát được.

## Ranh giới với skill khác (tránh gọi nhầm)

- **Có sẵn 1 file video quay/tải về, muốn edit/dựng lại, chỉnh màu, cắt, thêm hiệu ứng** → đúng skill này.
- **Không có video có sẵn, chỉ có dữ liệu Excel/CSV + ảnh sản phẩm, muốn ra video quảng cáo TikTok/Facebook** → dùng `video-san-pham`, không dùng skill này (skill này không tự tạo cảnh từ ảnh tĩnh theo dữ liệu sản phẩm).
- **Có kịch bản/bản tin dạng văn bản cần đọc thành giọng rồi ghép vào video** → dùng `video-thuyet-minh` (skill đó sẽ tự gọi lại skill này cho phần hình ảnh nếu cần).
- **Chủ đề nhận diện được là sự kiện/hội nghị kiểu Việt Nam** → skill này tự động route sang `dung-video-su-kien`, không cần người dùng gọi tay skill đó.

## Quy trình cốt lõi

1. **Phân tích video đầu vào.** Chạy `scripts/phan_tich_video.py <đường_dẫn_video>` để lấy metadata (thời lượng, độ phân giải, orientation, có/không có audio) và ảnh contact sheet (lưới khung hình trích định kỳ). Đọc ảnh contact sheet bằng công cụ đọc file ảnh để xem tổng quan nội dung — không cần xem toàn bộ video theo thời gian thực.
2. **Nhận diện chủ đề.** Dựa vào contact sheet + mô tả người dùng, đối chiếu [assets/bang-nhan-dien-chu-de.md](assets/bang-nhan-dien-chu-de.md). Nếu vẫn không rõ (ví dụ nội dung hỗn hợp hoặc quá đặc thù), hỏi lại người dùng thay vì đoán.
3. **Đọc nguyên tắc chất lượng dùng chung trước tiên.** Luôn đọc [references/nguyen-tac-chat-luong.md](references/nguyen-tac-chat-luong.md) — áp dụng cho mọi chủ đề, đây là phần quyết định video "có chất" hay không, không phụ thuộc chủ đề cụ thể.
4. **Đọc hướng dẫn theo đúng chủ đề đã nhận diện:**
   - Sự kiện/hội nghị/hội thi kiểu Việt Nam → dùng skill **`dung-video-su-kien`** (gọi qua Skill tool), không lặp lại nội dung ở đây.
   - Quảng cáo/giới thiệu sản phẩm → [references/quang-cao-san-pham.md](references/quang-cao-san-pham.md)
   - Vlog du lịch/trải nghiệm → [references/vlog-du-lich.md](references/vlog-du-lich.md)
   - Phỏng vấn/tutorial/hướng dẫn (talking-head) → [references/phong-van-tutorial.md](references/phong-van-tutorial.md)
   - Đám cưới/kỷ niệm gia đình → [references/ky-niem-gia-dinh.md](references/ky-niem-gia-dinh.md)
   - Thể thao/hành động → [references/the-thao-hanh-dong.md](references/the-thao-hanh-dong.md)
   - Ẩm thực/nấu ăn → [references/am-thuc.md](references/am-thuc.md)
   - Nội dung mạng xã hội ngắn (Reels/TikTok/Shorts, không thuộc các nhóm trên) → [references/mang-xa-hoi-ngan.md](references/mang-xa-hoi-ngan.md)
4b. **Cần 1 hiệu ứng cụ thể** (chuyển cảnh, chữ động, filter màu, zoom/pan, sticker, giảm rung...) → dùng skill **`hieu-ung-video`** để lấy công thức ffmpeg/HyperFrames thực thi được, thay vì tự nghĩ ra filter chain từ đầu.
5. **Lập kịch bản dựng (edit plan).** Theo [assets/edit-plan-template.md](assets/edit-plan-template.md), kết hợp cấu trúc/nhịp/màu/nhạc từ bước 3–4 với nội dung thật đã quan sát ở bước 1–2.
6. **Xác nhận với người dùng** trước khi thực thi nếu edit plan có thay đổi lớn so với video gốc (cắt bỏ đoạn dài, đổi nhạc, đổi màu mạnh) — đây là thay đổi khó đảo ngược đối với file gốc nếu ghi đè.
7. **Thực thi.**
   - Cắt/ghép/chỉnh màu/phụ đề trên clip thật → gọi skill **video-use**.
   - Dựng đồ họa động (title card, overlay, transition, text effect) → gọi **HyperFrames** (`hyperframes`, `hyperframes-animation`, `hyperframes-creative`) hoặc **remotion-*** nếu dự án đã dùng Remotion.
   - Tìm nhạc nền/SFX/overlay hợp lệ bản quyền → gọi **media-use**.
8. **Rà chất lượng lần cuối** theo mục "Kiểm tra trước khi giao" trong [references/nguyen-tac-chat-luong.md](references/nguyen-tac-chat-luong.md) trước khi báo hoàn tất.

## Khi nào chạy script

- `scripts/phan_tich_video.py` — luôn chạy đầu tiên khi có 1 file video đầu vào cụ thể. Yêu cầu `ffmpeg`/`ffprobe` có sẵn trên PATH (cài qua `winget install Gyan.FFmpeg` trên Windows nếu chưa có).
- `scripts/sync_skill.py` — chỉ dùng khi bảo trì skill này (đồng bộ `skills/bien-tap-video` sang `.agents/skills/` và `.claude/skills/`).

## Xử lý dữ liệu thiếu và giả định

- Nếu người dùng đã nói rõ chủ đề, dùng luôn, không cần chạy lại bước nhận diện qua contact sheet trừ khi cần xem nội dung thật để lập edit plan chi tiết.
- Nếu video không có audio hoặc chưa nghe được nội dung âm thanh (skill này chỉ phân tích hình ảnh qua ffmpeg, không tự nghe/hiểu giọng nói): mọi đề xuất về nhạc nền, lời bình, đồng bộ theo beat đều là **đề xuất chung**, ghi rõ trong kết quả, không trình bày như đã xác nhận từ audio gốc.
- Không tự đoán tên người/địa điểm/thương hiệu xuất hiện trong video nếu không có chữ hiển thị rõ hoặc người dùng chưa xác nhận.

## Định dạng đầu ra

- **Báo cáo phân tích video**: chủ đề nhận diện được, metadata chính, mô tả ngắn theo từng đoạn quan sát được trên contact sheet.
- **Kịch bản dựng (edit plan)**: theo [assets/edit-plan-template.md](assets/edit-plan-template.md).
- Luôn nêu rõ bước tiếp theo cần skill/công cụ nào để thực thi thật, không tự nhận đã xuất file video hoàn chỉnh nếu chưa thực sự gọi công cụ render.
