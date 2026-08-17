---
description: Rà soát code đã thay đổi — tìm lỗi logic, chỗ phá vỡ chức năng đang chạy, và chỗ rườm rà
argument-hint: [nhánh, file, hoặc để trống để review diff hiện tại]
---

Phạm vi review: **$ARGUMENTS** (để trống = `git diff` chưa commit + đã stage).

Gọi agent `code-reviewer` với phạm vi trên. Nhận `ReviewReport`.

Trình bày kết quả theo mức nghiêm trọng, mỗi finding gồm:

```text
[blocker|major|minor|nit] <file>:<dòng>
  Vấn đề:    <một câu>
  Kịch bản:  <input/state cụ thể → kết quả sai cụ thể>
  Đề xuất:   <cách sửa>
```

Finding không dựng được kịch bản hỏng cụ thể thì bỏ, đừng báo cho đủ số lượng. Không có finding nào là kết quả hợp lệ — nói thẳng "không tìm thấy vấn đề" và liệt kê những gì đã thực sự đọc.

Cuối cùng ghi rõ đã **đọc** những file nào và **không** đọc những gì.

Chỉ báo cáo, **không tự sửa**. Người dùng muốn sửa thì họ sẽ nói.
