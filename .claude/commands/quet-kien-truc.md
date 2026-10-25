---
description: Quét code một dự án app và viết tài liệu kiến trúc gọn, mỗi ý dẫn nguồn file:dòng, có script kiểm tra trích dẫn
argument-hint: <đường dẫn thư mục dự án>
---

Dự án cần quét: **$ARGUMENTS** (để trống = thư mục hiện tại).

Mục đích: lần sau mở dự án, đọc tài liệu này là hiểu hệ thống mà không phải đoán. Đọc [rules/global.md](rules/global.md) trước — **không bịa**.

## Nguyên tắc

- **Mỗi ý kỹ thuật phải có nguồn** dạng `đường/dẫn/file.ext:dòng` hoặc `đường/dẫn/file.ext:đầu-cuối`, viết trong dấu backtick, đường dẫn tính từ gốc dự án.
- Không tìm thấy trong code → ghi **"Không tìm thấy trong code"**. Không suy đoán, không điền theo "thường thì".
- **Không chép giá trị secret.** Biến môi trường chỉ ghi tên (`SUPABASE_URL`), không ghi giá trị; không mở `.env` thật.
- Gọn: dự án nhỏ thì mỗi phần vài dòng. Phần không áp dụng thì ghi một dòng lý do, không bỏ trống tiêu đề.

## Các phần (giữ đúng thứ tự)

1. **Tổng quan** — app làm gì, cho ai dùng.
2. **Công nghệ** — framework, ngôn ngữ, thư viện chính (lấy từ `package.json` / `requirements.txt` / `pyproject.toml`).
3. **Cấu trúc thư mục** — cây thư mục cấp 1–2, mỗi thư mục một dòng vai trò.
4. **Luồng chính** — 1–3 luồng nghiệp vụ quan trọng nhất, đi từ màn hình → xử lý → dữ liệu.
5. **Dữ liệu** — bảng/collection, quan hệ chính, migration nằm đâu.
6. **Xác thực & phân quyền** — đăng nhập thế nào, ai được làm gì, RLS (nếu Supabase).
7. **API / endpoint** — danh sách route và việc mỗi route làm.
8. **Dịch vụ ngoài & cấu hình** — dịch vụ gọi ra ngoài, tên biến môi trường cần có.
9. **Chạy, test, build** — lệnh thật lấy từ scripts của dự án; không có thì ghi "Không có".
10. **Rủi ro & chỗ chưa rõ** — thứ thấy đáng lo khi đọc code (thiếu kiểm tra quyền, thiếu test…), và câu hỏi cần người dùng trả lời.

## Ghi vào đâu

- Dự án đã có tài liệu kiến trúc (`ARCHITECTURE.md`, `docs/**/architecture.md`) → **cập nhật file đó**, giữ phần người dùng viết tay.
- Chưa có → tạo `docs/02-ky-thuat/architecture.md` trong dự án.
- Đầu file ghi ngày quét và commit hiện tại (`git rev-parse --short HEAD`).

## Kiểm chứng — bắt buộc

```bash
python scripts/check_citations.py <file tài liệu> --root <thư mục dự án>
```

Exit khác 0 → sửa trích dẫn sai rồi chạy lại (tối đa 3 vòng, theo [rules/global.md](rules/global.md)). **Không báo xong khi script chưa ra exit 0.**

Báo cáo:

```text
TÀI LIỆU:   <đường dẫn file>
TRÍCH DẪN:  <đúng>/<tổng> — exit <mã>
KHÔNG THẤY: <các phần ghi "Không tìm thấy trong code">
RỦI RO:     <các mục ở phần 10>
```
