---
description: Dựng khung Claude Code cho dự án hiện tại từ khuôn chuẩn (CLAUDE.md, .claude/rules, docs/) rồi điền tài liệu từ code thật
argument-hint: [mô tả ngắn dự án — bỏ trống thì tự đọc code]
---

Dự án: **$ARGUMENTS**

Khuôn chuẩn của người dùng nằm ở `C:\Users\DANG HUNG TAN\Documents\Claude-Code-Project-Template\`. Mục tiêu: sau lệnh này người dùng chỉ cần gõ `/build-feature`, `/fix`, `/review`, `/test` mà không phải viết prompt dài.

1. **Kiểm trạng thái.** `git status` — có thay đổi chưa commit thì báo và **không ghi đè** file nào của người dùng. Thư mục chưa phải Git repo thì hỏi có `git init` không.
2. **Chép khuôn, bỏ qua file đã có** (không bao giờ ghi đè):
   - `CLAUDE.md`, `.claude/rules/*`, `.claude/references/*`, `.claude/skills/*`, `.claude/plans/{active,completed}/README.md`, `.claude/hooks/*`, `.claude/settings.json`
   - `docs/**` (khung tài liệu), `.mcp.example.json` — **không** chép `.mcp.json`; không tạo `.env` thật.
   Dự án đã có `CLAUDE.md` riêng → giữ nguyên, chỉ đề xuất mục còn thiếu.
3. **Điền tài liệu từ code thật, không bịa:**
   - đọc `package.json` / `pyproject.toml` / `requirements.txt` / cấu trúc thư mục → điền ngôn ngữ, framework, lệnh **cài / chạy / lint / typecheck / test / build thật** vào `CLAUDE.md` và `docs/02-ky-thuat/architecture.md`;
   - dự án có sẵn nhiều code → gọi lệnh `/quet-kien-truc` cho tài liệu kiến trúc có dẫn nguồn `file:dòng`;
   - chưa có code → ghi mô tả trong `$ARGUMENTS` vào `docs/03-san-pham/requirements.md`, phần chưa biết để **"(cần người dùng bổ sung)"**.
4. **Thêm mục "Khi người dùng gõ ngắn"** vào cuối `CLAUDE.md` của dự án (nếu chưa có):
   ```markdown
   ## Khi người dùng gõ ngắn
   - "làm tiếp" → đọc .claude/plans/active/, làm bước kế tiếp chưa xong, cập nhật kế hoạch
   - "sửa lỗi này" + ảnh/log → chạy /fix với nội dung đó
   - "xong chưa" / "kiểm tra" → chạy lint + typecheck + test + build thật, báo kết quả thật
   - "thêm <tính năng>" → chạy /build-feature <tính năng>
   ```
5. **Kiểm.** Chạy thử đúng các lệnh đã ghi (ít nhất lệnh test hoặc build) để chắc chúng chạy được trên máy; lệnh nào lỗi thì ghi rõ trong báo cáo, không ghi lệnh chưa chạy được vào `CLAUDE.md` như thể đã đúng.

Không commit, không push — để người dùng tự xem rồi commit.

Báo cáo:

```text
ĐÃ TẠO:     <danh sách file mới>
BỎ QUA:     <file đã có, giữ nguyên>
LỆNH THẬT:  cài | chạy | test | build — <lệnh> → chạy được / lỗi
CẦN BỔ SUNG: <mục tài liệu người dùng phải điền>
DÙNG NGAY:  /build-feature <tính năng> · /fix <lỗi> · /review · /test · "làm tiếp"
```
