---
description: Chạy validation thật của dự án (lint, typecheck, test, build) và báo cáo trung thực
argument-hint: [bước cụ thể: lint | typecheck | unit | build — để trống là chạy hết]
---

Phạm vi: **$ARGUMENTS** (để trống = chạy toàn bộ chuỗi).

Gọi agent `app-tester`. Nhận `TestReport`.

Nhắc lại rule cứng ([rules/global.md](rules/global.md)): **NO TEST = NO PASS**. Bước chưa chạy phải ghi `NOT RUN` kèm lý do, không được suy ra kết quả.

Báo cáo:

```text
LINT:       PASS | FAIL | NOT RUN — <lệnh> (exit <mã>)
TYPECHECK:  …
UNIT:       …
INTEGRATION:…
BUILD:      …
```

Có `FAIL` → in dòng lỗi thật (không tóm tắt mất thông tin), rồi hỏi người dùng có muốn sửa luôn không. Người dùng đồng ý → chạy `/fix` cho từng lỗi.

Dự án không có lệnh cho bước nào → ghi `NOT RUN (dự án không có <lệnh>)`. Không bịa lệnh, không tự thêm công cụ test mới vào dự án.
