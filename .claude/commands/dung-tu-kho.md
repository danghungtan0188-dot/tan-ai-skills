---
description: Dựng một bản tin hoàn chỉnh từ nhiều clip thô — tìm clip, khảo sát, chọn cảnh, duyệt kế hoạch, ghép, QA theo kế hoạch
argument-hint: <thư mục clip hoặc từ khoá> --dai <giây> [chủ đề, ngày quay]
---

Đầu vào: **$ARGUMENTS**

Đường chạy video thô. Đọc [rules/video.md](rules/video.md) và
[skills/bien-tap-video-thong-minh-song-ngu-tan/references/dung-tu-video-tho.md](skills/bien-tap-video-thong-minh-song-ngu-tan/references/dung-tu-video-tho.md)
trước khi chạy lệnh nào.

```text
find_clips → survey_rushes → XEM ẢNH chọn cảnh → build_edit_plan → DUYỆT → assemble → render_att → qa --plan
```

**Bắt buộc: chốt độ dài trước.** Chưa có số giây thì hỏi một câu duy nhất rồi làm tiếp.

**1. Tìm clip.** Có đường dẫn thì dùng thẳng. Không có thì `scripts/find_clips.py` theo
[references/kho-clip.md](skills/bien-tap-video-thong-minh-song-ngu-tan/references/kho-clip.md).
Nhiều nhóm sự kiện khác nhau cùng khớp → nêu các nhóm, hỏi chọn; **không trộn hai sự kiện vào một video**.

**2. Khảo sát.** `scripts/survey_rushes.py <kho> --recursive --out edit/rushes.json --sheet edit/contact.jpg`

**3. Xem ảnh rồi mới chọn cảnh.** Mở `contact.jpg`. **Không đoán nội dung từ tên file hay từ số liệu
nét/sáng.** Viết `edit/chon-canh.json`: mỗi cảnh có cỡ (`toan`/`trung`/`can`), loại
(`broll`/`phat_bieu`) và **lý do**. Mở mỗi mục bằng cảnh rộng rồi siết dần; không để hai cảnh cùng
cỡ đứng cạnh nhau; phát biểu đặt sau khi đã có bối cảnh.

**4. Lập kế hoạch.** `scripts/build_edit_plan.py edit/rushes.json edit/chon-canh.json --target <giây>
--out edit/edit-plan.json --kiem-tieng`. FAIL → sửa `chon-canh.json`, chạy lại. Thiếu giây thì
**chọn thêm cảnh**, không kéo dài cảnh cũ.

**5. Duyệt.** Đưa nguyên bảng đoạn cho người dùng. Chỉ bỏ qua bước này khi chính yêu cầu hiện tại
đã nói rõ cho tự động cắt ghép (`--approved`).

**6. Ghép.** `scripts/assemble.py edit/edit-plan.json --out edit/rough.mp4 --rushes edit/rushes.json`
(có lời đọc thì thêm `--voice`).

**7. Hoàn thiện + QA.** Phụ đề song ngữ, banner, logo, outro theo
[references/phong-cach-att-news.md](skills/bien-tap-video-thong-minh-song-ngu-tan/references/phong-cach-att-news.md),
rồi `scripts/qa.py OUT --plan edit/edit-plan.json --cut-authorized yes --tail <giây outro>`.
FAIL → sửa → chạy lại, tối đa 3 vòng.

**8. Rút kinh nghiệm.** Chạy `/rut-kinh-nghiem` trước khi đóng việc.

Báo cáo cuối:

```text
CLIP VÀO:      <số clip> / <số cảnh>
KẾ HOẠCH:      <số đoạn> — <tổng>s / yêu cầu <target>s
QA:            PASS | FAIL  (LỖI: … / CẢNH BÁO: …)
OUTPUT:        <đường dẫn>
CHƯA KIỂM:     <ghi rõ, hoặc "không">
```

Không ghi đè clip gốc. Không cắt khi chưa duyệt.
