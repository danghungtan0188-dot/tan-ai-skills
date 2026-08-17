---
description: Rà soát bảo mật — secret rò rỉ, .env bị commit, thiếu auth/phân quyền, RLS, injection
argument-hint: [thư mục hoặc file cần rà, để trống là toàn repo]
---

Phạm vi: **$ARGUMENTS** (để trống = toàn bộ file được git tracked).

Gọi agent `security-reviewer`. Đọc [rules/security.md](rules/security.md).

Báo cáo theo từng mục, ghi rõ mục nào **đã chạy** và mục nào **chưa chạy được**:

```text
SECRET RÒ RỈ:      PASS | FAIL | NOT RUN
.env BỊ TRACKED:   PASS | FAIL | NOT RUN
AUTH / PHÂN QUYỀN: PASS | FAIL | NOT RUN
RLS (Supabase):    PASS | FAIL | NOT RUN
INJECTION:         PASS | FAIL | NOT RUN
LOG / RESPONSE:    PASS | FAIL | NOT RUN
PHỤ THUỘC:         PASS | FAIL | NOT RUN
```

Mỗi finding `blocker`/`major` phải có kịch bản tấn công cụ thể: kẻ tấn công gửi gì, lấy được gì.

**Chỉ báo cáo, không tự sửa** — trừ khi lỗi là secret đang nằm trong file chưa commit và cách sửa hiển nhiên (thay bằng biến môi trường); khi đó sửa rồi nói rõ đã sửa gì.

Phát hiện secret **đã bị commit vào lịch sử git** → dừng lại, báo người dùng ngay: key đó phải coi như đã lộ và cần thu hồi ở nhà cung cấp. Không tự chạy lệnh viết lại lịch sử git.
