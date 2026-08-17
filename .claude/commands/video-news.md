---
description: Dựng video bản tin/sự kiện hoàn chỉnh từ file thô — phân tích, chọn template, title + lower-third + phụ đề, render, QA
argument-hint: <đường dẫn video> [mô tả nội dung, đơn vị, người phát biểu]
---

Đầu vào: **$ARGUMENTS**

Chuỗi VIDEO đầy đủ theo hướng bản tin. Đọc [rules/video.md](rules/video.md) trước.

```text
Input → video-analyzer → chọn template → video-editor → render → video-reviewer → PASS/FAIL
```

**1. Phân tích.** Gọi agent `video-analyzer`. Nhận `VideoAnalysis` — metadata thật + tỉ lệ khung hình + chủ đề + danh sách `unknowns`.

**2. Chọn template theo tỉ lệ và chủ đề.**

| Tỉ lệ | Hướng | Nền tảng đích |
|---|---|---|
| 16:9 | bản tin truyền hình, lower-third rộng | YouTube, màn hình hội trường |
| 9:16 | bản tin dọc, chữ lớn, lower-third gọn | TikTok, Reels, Zalo |
| 1:1 | dạng feed | Facebook |

Chủ đề là sự kiện/hội nghị/hội thi kiểu Việt Nam → dùng skill `dung-video-su-kien`.
Cần lower-third/title dựng bằng code → dùng skill `chuyen-gia-edit-video-tan`.
Cần phụ đề song ngữ Anh trên / Việt dưới → dùng skill `bien-tap-video-thong-minh-song-ngu-tan`.

**3. Xử lý phần chưa biết.** Với mỗi mục trong `unknowns` cần cho bản tin (tên người phát biểu, chức vụ, đơn vị, nội dung lời nói): hỏi người dùng **một lần, gộp thành một câu hỏi**. Không bịa. Chưa có thì để trống lower-third, không điền đại.

**4. Dựng.** Gọi agent `video-editor` với `VideoAnalysis` + template + thông tin người dùng cung cấp. Thứ tự: cắt/ghép → màu → title → lower-third → logo/icon → chuyển cảnh → xử lý âm thanh → **burn phụ đề sau cùng** → render.

**5. QA.** Gọi agent `video-reviewer`. FAIL → xác định lỗi, quay lại bước 4, render lại, QA lại. Tối đa 3 vòng.

Báo cáo cuối:

```text
FFMPEG:        exit <mã>
FFPROBE:       <duration / resolution / fps>
VIDEO STREAM:  <codec, pix_fmt>
AUDIO STREAM:  <codec, sample rate, channels>
VIDEO QA:      PASS | WARN | FAIL | NOT RUN
KIỂM HÌNH:     PASS | FAIL | NOT RUN
OUTPUT:        <đường dẫn>
```

Không ghi đè file gốc. Không cắt thời lượng nếu người dùng chưa cho phép.
