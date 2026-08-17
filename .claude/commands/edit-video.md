---
description: Dựng/chỉnh sửa video theo yêu cầu tự do — tự nhận diện chủ đề rồi định tuyến sang đúng skill
argument-hint: <đường dẫn video> <muốn làm gì>
---

Đầu vào: **$ARGUMENTS**

Đọc [rules/video.md](rules/video.md) trước.

**1. Phân tích.** Gọi agent `video-analyzer` → `VideoAnalysis`.

**2. Định tuyến theo thứ có trong tay** (không hỏi người dùng chọn skill, tự chọn rồi nói đã chọn gì):

| Trong tay | Skill |
|---|---|
| 1 file video quay/tải về, chưa rõ chủ đề | `bien-tap-video` |
| Video sự kiện/hội nghị/hội thi kiểu Việt Nam | `dung-video-su-kien` |
| Cần bản tin/MC/lower-third dựng bằng code | `chuyen-gia-edit-video-tan` |
| Cần phụ đề song ngữ Anh/Việt | `bien-tap-video-thong-minh-song-ngu-tan` |
| Excel/CSV + ảnh sản phẩm | `video-san-pham` |
| Kịch bản văn bản cần đọc thành giọng rồi ghép | `video-thuyet-minh` |
| Chỉ cần 1 hiệu ứng đơn lẻ | `hieu-ung-video` |
| Chỉ cần cắt/ghép/màu/phụ đề trên clip thật | `video-use` |

**3. Dựng.** Gọi agent `video-editor`. Nó lập `EditPlan` rồi thực thi.

Xác nhận với người dùng **trước khi chạy** nếu kế hoạch có: cắt bỏ đoạn dài, đổi thời lượng tổng, đổi nhạc, hoặc ghi đè file gốc. Ngoài mấy trường hợp đó thì làm luôn.

**4. QA.** Gọi agent `video-reviewer`. FAIL → sửa → render lại → QA lại, tối đa 3 vòng.

Báo cáo: `EditPlan` đã dùng, lệnh ffmpeg thật đã chạy, kết quả `VideoQAReport`, đường dẫn output. Không nhận đã xong khi QA chưa PASS.
