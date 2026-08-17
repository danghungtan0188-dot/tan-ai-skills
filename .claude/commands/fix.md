---
description: Sửa một lỗi cụ thể theo quy trình tái hiện → sửa → tái hiện lại
argument-hint: <mô tả lỗi, thông báo lỗi, hoặc đường dẫn file>
---

Lỗi cần sửa: **$ARGUMENTS**

Đọc [rules/coding.md](rules/coding.md) trước. Quy trình bắt buộc:

1. **Tái hiện.** Chạy được lệnh/thao tác làm lỗi xuất hiện. Ghi lại thông báo lỗi thật.
   Không tái hiện được → nói rõ, hỏi người dùng cách tái hiện, **không đoán rồi sửa bừa**.

2. **Tìm nguyên nhân gốc.** Đọc code, lần theo stack trace. Không vá triệu chứng (bọc try/catch, thêm `if` chặn) khi chưa hiểu vì sao lỗi.

3. **Viết test tái hiện lỗi** (nếu dự án có test). Xác nhận test đỏ **trước khi** sửa.

4. **Sửa nhỏ nhất.** Chỉ động vào chỗ gây lỗi. Không tiện tay dọn dẹp xung quanh.

5. **Xác nhận.** Chạy lại chính lệnh ở bước 1 → hết lỗi. Chạy test ở bước 3 → xanh. Chạy toàn bộ test hiện có → **không có test nào từ xanh chuyển đỏ**.

Với lỗi phức tạp đụng nhiều file, gọi agent `app-planner` trước bước 4.

Báo cáo:

```text
TÁI HIỆN:   được / không được — <lệnh>
NGUYÊN NHÂN: <gốc rễ, không phải triệu chứng>
SỬA:        <file:dòng>
XÁC NHẬN:   PASS | FAIL — <lệnh đã chạy lại>
HỒI QUY:    PASS | NOT RUN — <bộ test đã chạy>
```
