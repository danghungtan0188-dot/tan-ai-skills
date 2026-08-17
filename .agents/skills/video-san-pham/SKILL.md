---
name: video-san-pham
description: Dựng một video sản phẩm ngắn khi được yêu cầu, từ dữ liệu 1 sản phẩm trong Excel/CSV + ảnh sản phẩm — AI viết kịch bản đúng dữ liệu thật, tạo giọng đọc, đồng bộ phụ đề bằng ASR cấp từ (vai trò Whisper), dựng cảnh có chuyển động (vai trò Remotion/HyperFrames), ghép và xuất đúng định dạng TikTok/Facebook (vai trò FFmpeg). Chạy từng video một theo yêu cầu, không tự động quét/xuất cả danh sách Excel. Kích hoạt khi người dùng có ảnh sản phẩm + thông tin sản phẩm (từ Excel hoặc mô tả trực tiếp) muốn ra 1 video TikTok/Facebook, hoặc nói "làm video sản phẩm này", "dựng video quảng cáo cho sản phẩm X từ Excel", "xuất video TikTok/Facebook cho sản phẩm này". Skill này là lớp điều phối (workflow orchestrator) có kèm nguyên tắc cứng + bước tự kiểm tra chất lượng sau khi render — không tự tổng hợp giọng, không tự phiên âm, không tự render; gọi đúng thứ tự các skill/công cụ chuyên trách (tan-giong-doc-ban-tin, video-use, remotion-*/HyperFrames, media-use, marketing) và chịu trách nhiệm phần đọc dữ liệu Excel, đồng bộ kịch bản-giọng đọc-phụ đề-ảnh, và tự kiểm tra đầu ra mà các skill kia không tự làm.
---

# Video sản phẩm (Excel + ảnh → kịch bản → giọng đọc → video phụ đề → xuất TikTok/Facebook)

## Phạm vi

Hỗ trợ: dựng **một video** cho **một sản phẩm cụ thể** khi người dùng yêu cầu — lấy dữ liệu sản phẩm đó (từ 1 dòng Excel/CSV hoặc mô tả trực tiếp) + ảnh sản phẩm, AI viết kịch bản, tạo giọng đọc, đồng bộ phụ đề, dựng cảnh có chuyển động, ghép và xuất đúng định dạng nền tảng.

Không làm:
- Không tự động quét toàn bộ file Excel và xuất hàng loạt — chỉ xử lý sản phẩm được chỉ định trong yêu cầu hiện tại. Muốn video khác thì yêu cầu lần khác.
- Không tự bịa thông tin sản phẩm (giá, công dụng, khuyến mãi, chất liệu...) không có trong dữ liệu — thiếu thì hỏi lại hoặc bỏ qua phần đó trong kịch bản, không tự suy diễn.
- Không tự tổng hợp giọng nói, không tự phiên âm, không tự render — việc này thuộc về các skill/công cụ được gọi bên dưới.
- Không tự thêm nhạc nền/SFX không rõ nguồn gốc bản quyền.

## Ranh giới với skill khác (tránh gọi nhầm)

- **Có dữ liệu Excel/CSV + ảnh sản phẩm, muốn ra video quảng cáo ngắn cho TikTok/Facebook** → đúng skill này.
- **Có sẵn video quay/tải về (không phải dựng từ ảnh tĩnh sản phẩm), muốn edit/chỉnh lại** → dùng `bien-tap-video`, không dùng skill này.
- **Có kịch bản văn bản tự do (không theo khung HOOK→TÍNH NĂNG→GIÁ→CTA của sản phẩm thương mại) muốn ghép giọng đọc vào video** → dùng `video-thuyet-minh`.

## Nguyên tắc cứng (đúng đắn kỹ thuật — không thương lượng)

Đây là các điểm nếu làm sai sẽ hỏng lặng lẽ (silent failure) hoặc phải làm lại toàn bộ. Không phải gu thẩm mỹ, là đúng/sai kỹ thuật.

1. **Kịch bản chỉ dùng dữ liệu thật** đã xác nhận từ Excel/người dùng. Trường nào trống thì bỏ qua trong kịch bản, không tự đoán giá/công dụng/khuyến mãi.
2. **Phụ đề lấy timestamp từ bước ASR cấp từ** (transcribe chính file giọng đọc vừa tổng hợp) — không tự đếm nhịp hay ước lượng thời điểm bằng tay.
3. **Phụ đề luôn burn SAU CÙNG** trong chuỗi ghép (kế thừa Hard Rule của `video-use`): overlay tên/giá/CTA áp trước, phụ đề áp cuối cùng — ngược lại phụ đề bị overlay che mất.
4. **Ảnh không đúng tỉ lệ khung hình đích thì crop thông minh giữ chủ thể sản phẩm hoặc thêm nền (blur/màu nền thương hiệu), không bao giờ kéo giãn méo ảnh.**
5. **Bắt buộc qua bước kiểm tra rủi ro nội dung** (phóng đại công dụng, sai lệch giá, bản quyền hình ảnh/nhạc) trước khi ghép xuất bản cuối — không xuất file khi chưa qua bước này.
6. **Tự kiểm tra (self-eval) video đã render trước khi giao cho người dùng** — không trình bày bản chưa tự kiểm tra. Nếu phát hiện lỗi: sửa và render lại. **Tối đa 3 lần tự sửa** — quá đó thì dừng và báo cụ thể lỗi còn tồn đọng cho người dùng thay vì lặp vô hạn.
7. **Một yêu cầu = một video.** Không tự ý mở rộng sang sản phẩm khác trong Excel khi chưa được yêu cầu.

## Bộ ba kỹ thuật nền và cách ánh xạ vào skill có sẵn trong repo này

Yêu cầu gốc là "Remotion + Whisper + FFmpeg". Trong bộ skill của repo này, ba vai trò đó thực hiện như sau (chi tiết trong [references/quy-trinh-ky-thuat-remotion-whisper-ffmpeg.md](references/quy-trinh-ky-thuat-remotion-whisper-ffmpeg.md)):

1. **Remotion (dựng cảnh lập trình)** — `remotion-create`/`remotion-captions`/`remotion-render`, hoặc HyperFrames (skill `hyperframes`) nếu phù hợp hơn: dựng cảnh từ ảnh sản phẩm (chuyển động Ken Burns/pan/zoom nhẹ), overlay tên/giá/CTA, hiển thị phụ đề đã đồng bộ.
2. **Whisper / ASR cấp từ (đồng bộ phụ đề)** — `video-use` (`helpers/transcribe.py`) hoặc `hyperframes-cli transcribe`: phiên âm file giọng đọc vừa tổng hợp, lấy timestamp cấp từ chính xác.
3. **FFmpeg (ghép/nén/xuất)** — `video-use` (`render.py`): ghép cảnh + audio + phụ đề (LAST) thành video cuối, đúng thông số nền tảng đích. `scripts/kiem_tra_dau_ra.py` của skill này gọi `ffprobe` để tự kiểm tra file xuất.

## Skill được điều phối

1. **`tan-giong-doc-ban-tin`** — kịch bản đã duyệt → file audio giọng đọc.
2. **`marketing`** — viết sâu hơn kịch bản nếu cần, và **bắt buộc dùng cho bước kiểm tra rủi ro nội dung** (Nguyên tắc cứng #5) trước khi xuất.
3. **`remotion-create`/`remotion-captions`/`remotion-render`** hoặc **HyperFrames** (`hyperframes`) — dựng cảnh từ ảnh + hiển thị phụ đề.
4. **`video-use`** — ASR cấp từ, ghép/nén/xuất video cuối, burn phụ đề.
5. **`media-use`** — nhạc nền/SFX hợp lệ bản quyền nếu người dùng muốn thêm.
6. **`bien-tap-video`** — bộ nguyên tắc chất lượng dựng chung khi cần tham chiếu thêm.

## Quy trình cốt lõi

1. **Tiếp nhận yêu cầu.** Xác định: sản phẩm nào (mã SP/tên — tra trong Excel nếu có, hoặc người dùng mô tả trực tiếp không cần Excel), ảnh dùng, giọng đọc, nền tảng xuất (TikTok dọc 1080×1920 / Facebook Feed vuông hoặc Reels dọc). Chỉ hỏi những gì thực sự chưa xác định được từ yêu cầu — không hỏi lại thông tin đã có sẵn trong Excel/ảnh.
2. **Bước A — Lấy & xác thực dữ liệu.** Chạy `scripts/doc_du_lieu_san_pham.py --ma-san-pham <mã>` (hoặc `--ten-san-pham`) trên file Excel/CSV, đối chiếu ảnh với thư mục đã cho theo [references/du-lieu-dau-vao-excel-anh.md](references/du-lieu-dau-vao-excel-anh.md). Thiếu trường bắt buộc hoặc ảnh không khớp: hỏi ngay tại đây — đây là điểm chặn hợp lệ duy nhất trước khi bắt đầu, không phải hỏi tuỳ hứng.
3. **Bước B — AI viết kịch bản.** Khung gợi ý: HOOK (3–5s) → GIỚI THIỆU/TÍNH NĂNG → GIÁ/KHUYẾN MÃI (nếu có) → CTA. Chỉ dùng dữ liệu thật (Nguyên tắc cứng #1). Trình bày kịch bản để người dùng duyệt — **đây là điểm duyệt duy nhất cần chờ xác nhận**, vì lời thoại khó sửa sau khi đã tổng hợp giọng và dựng video. Sau khi duyệt, chạy liền các bước C→H không dừng lại hỏi thêm, trừ khi gặp lỗi kỹ thuật thật sự chặn được.
4. **Bước C — Tạo giọng đọc.** Gọi `tan-giong-doc-ban-tin` với kịch bản đã duyệt.
5. **Bước D — ASR cấp từ (vai trò Whisper).** Transcribe file giọng đọc vừa tạo (video-use `helpers/transcribe.py` hoặc `hyperframes-cli transcribe`) lấy timestamp cấp từ — nguồn duy nhất cho phụ đề (Nguyên tắc cứng #2).
6. **Bước E — Dựng cảnh + phụ đề (vai trò Remotion).** Ảnh sản phẩm → cảnh có chuyển động nhẹ, overlay tên/giá/CTA đúng dữ liệu thật, phụ đề theo timestamp bước D, xử lý tỉ lệ khung hình theo Nguyên tắc cứng #4.
7. **Bước F — Kiểm tra rủi ro nội dung.** Gọi bước kiểm tra của skill `marketing` (phóng đại công dụng, sai lệch giá, bản quyền) trên kịch bản + overlay trước khi ghép cuối (Nguyên tắc cứng #5). Có vấn đề: sửa kịch bản/overlay, quay lại bước cần thiết, không xuất bản khi chưa qua.
8. **Bước G — Ghép & xuất (vai trò FFmpeg).** Gọi `video-use` ghép cảnh + audio + phụ đề (LAST — Nguyên tắc cứng #3), xuất theo đúng thông số nền tảng theo [references/dinh-dang-xuat-tiktok-facebook.md](references/dinh-dang-xuat-tiktok-facebook.md), đặt tên file theo mã sản phẩm + nền tảng.
9. **Bước H — Tự kiểm tra đầu ra.** Chạy `scripts/kiem_tra_dau_ra.py` (gọi `ffprobe`) đối chiếu độ phân giải/tỉ lệ/thời lượng với kế hoạch; đối chiếu thủ công theo checklist trong [references/kiem-tra-chat-luong-tu-dong.md](references/kiem-tra-chat-luong-tu-dong.md) (đồng bộ audio-phụ đề, chữ không bị cắt/che, âm lượng giọng đọc rõ hơn nhạc nền). Lỗi: sửa và lặp lại bước liên quan, tối đa 3 lần (Nguyên tắc cứng #6). Đạt: giao video.

## Xử lý dữ liệu thiếu và giả định

- Thiếu trường bắt buộc (mã SP, tên, mô tả ngắn, giá, tên file ảnh) cho sản phẩm được yêu cầu: dừng ở Bước A, hỏi lại — không tự bịa để chạy tiếp.
- Ảnh trong Excel không khớp file thực tế: báo thiếu, hỏi lại tên/đường dẫn đúng, không tự chọn ảnh gần giống.
- Chưa rõ giọng đọc hoặc nền tảng xuất: hỏi 1 lần ở Bước 1 (Tiếp nhận yêu cầu), không hỏi lại giữa chừng.
- Không có nhạc nền được cung cấp: hỏi có muốn thêm không (qua `media-use`) hay giữ video chỉ có giọng đọc.
- Bước F phát hiện rủi ro không tự sửa được rõ ràng (vd. giá trong Excel có vẻ sai): báo cho người dùng, không tự đoán giá đúng.

## Định dạng đầu ra

- **Kịch bản chờ duyệt** (Bước B, trước khi tổng hợp giọng): theo [assets/ke-hoach-video-san-pham-template.md](assets/ke-hoach-video-san-pham-template.md).
- **Video hoàn chỉnh**: 1 file/nền tảng được yêu cầu, đặt tên `<mã sản phẩm>_<nền tảng>.mp4` (vd. `SP001_tiktok.mp4`), kèm caption ngắn + hashtag gợi ý để đăng, và tóm tắt ngắn: nguồn dữ liệu đã dùng, giọng đọc, engine dựng cảnh, kết quả tự kiểm tra ở Bước H (đạt/số lần sửa lại).
