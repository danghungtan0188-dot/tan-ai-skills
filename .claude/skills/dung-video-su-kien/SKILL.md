---
name: dung-video-su-kien
description: Công thức dựng video tổng kết sự kiện/hội thi/tin tức phong trào kiểu Việt Nam (hội nghị, lễ khai mạc, hội thi lực lượng, sự kiện đoàn thể, cơ quan nhà nước, địa phương): title card banner đỏ-vàng, overlay gameshow (đếm ngược + trắc nghiệm), transition hiệu ứng lửa/xé, đoạn hero-intro nhân vật cuối video, tông màu ánh sáng sân khấu. Đúc kết từ phân tích thực tế 1 video mẫu (kênh Đồng Tháp 24h, hội thi lực lượng bảo vệ an ninh trật tự ở cơ sở). Kích hoạt khi người dùng muốn dựng/edit video tổng kết sự kiện, hội nghị, lễ khai mạc, hội thi, phong trào thi đua theo phong cách bán-điện ảnh kiểu này, hoặc muốn phân tích/học theo cách một video sự kiện cụ thể đã được dựng. Skill này là bản đặc tả phong cách (playbook), không tự render video — khi thực thi cần phối hợp với công cụ dựng video khác (video-use, remotion-*, hoặc HyperFrames).
---

# Dựng video sự kiện kiểu Việt Nam

## Phạm vi

Hỗ trợ: lập kịch bản dựng (edit plan), xác định cấu trúc phân đoạn, thiết kế title card, overlay đồ họa, hiệu ứng chuyển cảnh, đoạn giới thiệu nhân vật cuối video, và tông màu/ánh sáng — cho thể loại video tổng kết sự kiện/hội thi/phong trào thi đua kiểu cơ quan nhà nước, đoàn thể, địa phương tại Việt Nam (ví dụ: hội thi lực lượng bảo vệ an ninh trật tự, đại hội, lễ khai mạc, chương trình văn nghệ tổng kết).

Không làm: không tự tải video có bản quyền của người khác để tái sử dụng nội dung; không tự thực thi render (cần dùng `video-use`, `remotion-*`, hoặc HyperFrames để dựng thật); không bịa số liệu/tên đơn vị/giải thưởng khi tường thuật lại một sự kiện có thật — chỉ mô tả kỹ thuật dựng, không suy diễn nội dung không quan sát được.

## Ranh giới với skill khác (tránh gọi nhầm)

Skill này là **module con**, thường được `bien-tap-video` tự động gọi khi nhận diện đúng chủ đề — người dùng thường **không cần gọi trực tiếp** skill này. Chỉ gọi thẳng khi đã chắc chắn 100% đây đúng là video sự kiện/hội thi kiểu Việt Nam và muốn xem riêng công thức phong cách, không cần bước phân tích/nhận diện chủ đề của `bien-tap-video`.

## Nguồn gốc

Playbook này được rút ra từ việc phân tích trực tiếp 1 video thật (Facebook Reel, kênh "Đồng Tháp 24h", ~3 phút, 1920x1080, 30fps) bằng cách trích khung hình định kỳ (ffmpeg) và xem xét từng phân đoạn. Đây là quan sát trực quan (visual-only) — **chưa phân tích nhạc nền/nhịp cắt theo beat** vì chưa nghe âm thanh gốc; áp dụng phần nhạc theo kinh nghiệm dựng phim chung, không phải trích xuất từ file mẫu.

## Quy trình cốt lõi

1. **Xác định cấu trúc tổng thể.** Đọc [references/cau-truc-video.md](references/cau-truc-video.md) — 8 phân đoạn chuẩn và tỉ lệ thời lượng gợi ý theo tổng thời lượng video.
2. **Thiết kế title card mở đầu.** Đọc [references/do-hoa-tieu-de.md](references/do-hoa-tieu-de.md) cho banner đỏ-vàng, hoa văn, kiểu chữ, thời lượng hiển thị.
3. **Dựng overlay gameshow (nếu có phần thi kiến thức/trắc nghiệm).** Đọc [references/overlay-gameshow.md](references/overlay-gameshow.md) — đồng hồ đếm ngược, khung câu hỏi, cách dựng bằng Remotion/HyperFrames.
4. **Chọn hiệu ứng chuyển cảnh.** Đọc [references/transition-hieu-ung.md](references/transition-hieu-ung.md) — hiệu ứng "xé/cháy" giữa hai phân đoạn lớn, khi nào dùng.
5. **Dựng đoạn hero-intro (nếu kết thúc bằng giới thiệu đội/nhân vật).** Đọc [references/hero-intro.md](references/hero-intro.md).
6. **Áp tông màu & ánh sáng.** Đọc [references/mau-sac-anh-sang.md](references/mau-sac-anh-sang.md) cho từng loại cảnh (hội trường, sân khấu, phỏng vấn, hero-intro).
7. **Lập kịch bản dựng (edit plan) hoàn chỉnh** theo [assets/shot-list-template.md](assets/shot-list-template.md) — liệt kê từng cảnh, thời lượng, hiệu ứng, ghi chú kỹ thuật.
8. **Bàn giao cho công cụ thực thi.** Playbook này không render video. Khi người dùng muốn dựng thật:
   - Cắt/ghép/phụ đề/chỉnh màu clip có sẵn → dùng skill **video-use**.
   - Dựng đồ họa động (title card, overlay gameshow, transition) theo lập trình → dùng **HyperFrames** (skill `hyperframes`, `hyperframes-animation`, `hyperframes-creative`) hoặc **remotion-*** nếu dự án đã dùng Remotion.
   - Nếu người dùng chỉ muốn học/tham khảo cách dựng, dừng ở bước lập kịch bản dựng, không cần gọi công cụ render.

## Xử lý dữ liệu thiếu và giả định

- Nếu người dùng chỉ đưa 1 video mẫu và muốn "học theo": phân tích trực quan bằng cách trích khung hình (xem [references/cau-truc-video.md](references/cau-truc-video.md) mục "Cách phân tích video mẫu"), không suy đoán nội dung ngoài những gì quan sát được trên khung hình.
- Nếu thiếu thông tin cụ thể của sự kiện thật (tên đơn vị, giải thưởng, số liệu) khi viết title card hoặc lời dẫn: để chỗ trống dạng `[Tên đơn vị]`, không tự bịa.
- Nhạc nền: vì chưa có công cụ nghe/phân tích âm thanh trong phiên làm việc, luôn ghi rõ đây là **đề xuất chung** theo kinh nghiệm dựng phim (nhạc hào hùng/trang trọng cho phần lễ, nhạc dồn dập cho gameshow, nhạc cảm xúc cho hero-intro), không phải trích xuất từ file mẫu.

## Định dạng đầu ra

- **Kịch bản dựng (edit plan)**: theo [assets/shot-list-template.md](assets/shot-list-template.md), dạng bảng: thứ tự cảnh — thời lượng — nội dung — hiệu ứng/overlay — ghi chú màu sắc.
- **Phân tích video mẫu**: mô tả theo từng phân đoạn trong [references/cau-truc-video.md](references/cau-truc-video.md), nêu rõ đây là quan sát từ khung hình trích xuất, không phải đọc mã nguồn edit gốc.
- Luôn nêu rõ bước tiếp theo cần công cụ nào (video-use / HyperFrames / remotion-*) nếu người dùng muốn dựng thật, thay vì tự nhận đã dựng xong.
