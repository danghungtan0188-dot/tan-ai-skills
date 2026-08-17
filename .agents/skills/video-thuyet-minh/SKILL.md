---
name: video-thuyet-minh
description: Quy trình sản xuất video có lời thuyết minh/bản tin tiếng Việt từ đầu đến cuối — nối skill tan-giong-doc-ban-tin (kịch bản → giọng đọc chuẩn phát thanh viên) với skill bien-tap-video/dung-video-su-kien (dựng/chỉnh hình ảnh) và video-use (thực thi ghép). Kích hoạt khi người dùng có 1 kịch bản/bản tin tiếng Việt muốn biến thành video hoàn chỉnh có giọng đọc, muốn lồng giọng đọc vào video đã có/đang dựng, hoặc nói chung "làm video bản tin", "đọc kịch bản này rồi ghép vào video", "làm video thuyết minh". Skill này là lớp điều phối toàn quy trình (workflow orchestrator) — không tự tổng hợp giọng nói hay tự render, mà gọi đúng thứ tự 3 skill trên và xử lý phần đồng bộ lời đọc với hình ảnh + trộn âm thanh mà 3 skill kia không tự làm.
---

# Video thuyết minh (kịch bản → giọng đọc → video hoàn chỉnh)

## Phạm vi

Hỗ trợ: toàn bộ quy trình từ kịch bản tiếng Việt đến video hoàn chỉnh có lời đọc — tạo giọng đọc, xác định/dựng hình ảnh nền, đồng bộ thời lượng lời đọc với từng cảnh, trộn âm thanh (giọng đọc + nhạc nền + âm thanh gốc), xuất bản video cuối.

Không làm: không tự viết lại nội dung kịch bản (chỉ đọc nguyên văn như `tan-giong-doc-ban-tin` quy định); không tự tổng hợp giọng nói hay tự render video (việc này thuộc về 3 skill được gọi bên dưới); không bịa hình ảnh/cảnh quay khi người dùng chưa cung cấp — hỏi lại thay vì tự tạo nội dung hình ảnh không có thật.

## Ranh giới với skill khác (tránh gọi nhầm)

- **Có kịch bản/bản tin văn bản + muốn giọng đọc ghép vào hình ảnh (có sẵn hoặc cần dựng)** → đúng skill này.
- **Chỉ cần file giọng đọc, không cần ghép vào video nào cả** → dùng thẳng `tan-giong-doc-ban-tin`, không cần qua skill này.
- **Sản phẩm thương mại cụ thể + dữ liệu Excel/CSV + ảnh sản phẩm, muốn ra video quảng cáo TikTok/Facebook theo khung HOOK→TÍNH NĂNG→GIÁ→CTA** → dùng `video-san-pham` (skill đó đã tự gọi `tan-giong-doc-ban-tin` cho phần giọng đọc, không cần qua skill này).
- **⚠️ Bài học thực tế:** trong phiên làm việc trước, quy trình "kịch bản → giọng đọc → ghép vào video" đã bị làm thủ công bằng lệnh ffmpeg trực tiếp thay vì gọi đúng skill này — kết quả vẫn ra được nhưng đi vòng, tốn thời gian và dễ bỏ sót bước (ví dụ đồng bộ thời lượng, trộn âm thanh). Khi gặp đúng tình huống "kịch bản + video cần lồng giọng đọc", **luôn vào skill này trước**, không tự xử lý tay bằng ffmpeg ngay từ đầu.

## 3 skill được điều phối

1. **`tan-giong-doc-ban-tin`** — kịch bản `.txt`/`.docx` → file audio giọng đọc (WAV/MP3), giọng nam/nữ miền Nam phong cách tin tức hoặc giọng nhân bản riêng.
2. **`bien-tap-video`** (tự route sang `dung-video-su-kien` nếu đúng chủ đề sự kiện) — nhận diện chủ đề, lập kịch bản dựng hình ảnh.
3. **`video-use`** — thực thi: cắt/ghép hình theo kịch bản dựng, ghép audio giọng đọc vào đúng vị trí, trộn âm thanh, xuất file cuối.

## Quy trình cốt lõi

1. **Tiếp nhận đầu vào.** Xác nhận với người dùng: file kịch bản (đường dẫn `.txt`/`.docx`), có sẵn video/footage nền chưa hay cần dựng mới, giọng đọc muốn dùng (nam/nữ/giọng nhân bản), mục đích (video bản tin có hình nền tĩnh/động, hay lồng giọng đọc vào video sự kiện đã dựng).
2. **Bước A — Tạo giọng đọc.** Gọi skill **`tan-giong-doc-ban-tin`** với kịch bản đã xác nhận. Lấy file audio + biết thời lượng chính xác của từng đoạn (script `read_script.py`/log của `synthesize.py` cho biết cách chia đoạn).
3. **Bước B — Chuẩn bị hình ảnh.**
   - Nếu người dùng đã có video/footage: gọi skill **`bien-tap-video`** để phân tích + nhận diện chủ đề, lập kịch bản dựng hình (route sang `dung-video-su-kien` nếu là sự kiện).
   - Nếu chưa có, hoặc cần thêm hình minh hoạ/đồ họa: dùng HyperFrames/`media-use` để dựng cảnh tĩnh/động phù hợp nội dung kịch bản — không tự bịa cảnh cụ thể (địa điểm, người, sự kiện) nếu người dùng chưa mô tả.
4. **Bước C — Đồng bộ lời đọc với hình ảnh.** Đọc [references/dong-bo-loi-doc-hinh-anh.md](references/dong-bo-loi-doc-hinh-anh.md) — thời lượng audio của từng đoạn kịch bản quyết định thời lượng cảnh hình tương ứng, không phải ngược lại.
5. **Bước D — Trộn âm thanh.** Đọc [references/can-bang-am-thanh.md](references/can-bang-am-thanh.md) — giọng đọc là lớp ưu tiên cao nhất, nhạc nền/âm thanh gốc phải hạ xuống rõ rệt khi giọng đọc đang phát.
6. **Bước E — Lập kế hoạch ghép cuối** theo [assets/ke-hoach-video-thuyet-minh-template.md](assets/ke-hoach-video-thuyet-minh-template.md), xác nhận với người dùng trước khi thực thi.
7. **Bước F — Thực thi.** Gọi skill **`video-use`** để ghép hình theo kịch bản dựng + audio giọng đọc theo timeline đã lập ở bước C, áp mixing ở bước D, xuất video cuối.
8. **Rà chất lượng** theo checklist trong `bien-tap-video/references/nguyen-tac-chat-luong.md` (nhịp cắt, hiệu ứng, màu sắc) **và** thêm kiểm tra riêng: lời đọc có bị cắt cụt giữa câu không, có đoạn nào hình và lời lệch nhau không, âm lượng giọng đọc có nghe rõ hơn nhạc nền/âm thanh gốc không.

## Xử lý dữ liệu thiếu và giả định

- Chưa rõ giọng đọc nam/nữ hay video nền: hỏi lại, không tự chọn (kế thừa nguyên tắc của `tan-giong-doc-ban-tin`).
- Kịch bản dài hơn nhiều so với hình ảnh có sẵn, hoặc ngược lại: nêu rõ chênh lệch với người dùng và đề xuất phương án (rút gọn kịch bản, hoặc bổ sung/kéo dài hình ảnh) — không tự ý cắt bớt nội dung kịch bản hoặc lặp hình ảnh mà không xác nhận.
- Không có nhạc nền được cung cấp: hỏi người dùng có muốn thêm nhạc nền không (qua `media-use`) hay giữ video chỉ có giọng đọc, không tự thêm nhạc không rõ nguồn gốc bản quyền.

## Định dạng đầu ra

- **Kế hoạch ghép** (trước khi thực thi): theo [assets/ke-hoach-video-thuyet-minh-template.md](assets/ke-hoach-video-thuyet-minh-template.md), liệt kê từng đoạn kịch bản — thời lượng audio — cảnh hình tương ứng — ghi chú mixing.
- **Video hoàn chỉnh**: file xuất từ `video-use`, kèm tóm tắt các bước đã qua (giọng đọc dùng, nguồn hình ảnh, cách mixing) để người dùng biết rõ phần nào là thật, phần nào là dựng thêm.
