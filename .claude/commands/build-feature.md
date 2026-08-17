---
description: Xây tính năng mới cho app/website qua chuỗi plan → code → review → test → security
argument-hint: <mô tả tính năng cần xây>
---

Yêu cầu tính năng: **$ARGUMENTS**

Chạy chuỗi APP đầy đủ. Đọc [rules/global.md](rules/global.md) và [rules/coding.md](rules/coding.md) trước.

```text
app-planner → app-builder → code-reviewer → app-tester → security-reviewer
```

1. Gọi agent `app-planner`. Nhận `ImplementationPlan`. Trình bày kế hoạch ngắn gọn cho người dùng (file sẽ đụng, rủi ro, lệnh validation) rồi **làm tiếp luôn** — không dừng chờ xác nhận trừ khi kế hoạch cần quyết định kiến trúc lớn hoặc đụng dữ liệu/secret.

2. Gọi agent `app-builder` với kế hoạch đó. Nhận `ImplementationResult`.

3. Gọi agent `code-reviewer`. `verdict: FAIL` → quay lại `app-builder` kèm danh sách finding. Tối đa 3 vòng.

4. Gọi agent `app-tester`. Có hạng mục `FAIL` → quay lại `app-builder` kèm log lỗi. Tối đa 3 vòng.

5. Gọi agent `security-reviewer`. Có `blocker` → quay lại `app-builder`.

Báo cáo cuối theo đúng khuôn (không gộp thành "ALL PASS"):

```text
LINT:      PASS | FAIL | NOT RUN — <lệnh đã chạy>
TYPECHECK: …
TEST:      …
BUILD:     …
SECURITY:  …
```

Kèm: file đã tạo/sửa, chỗ lệch kế hoạch, việc còn bỏ dở và lý do.

Không commit, không push, không deploy.
