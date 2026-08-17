---
name: phat-trien-app
description: Quy trình phát triển app và website trong repo này — dò kiến trúc dự án hiện có trước khi sửa, quy ước viết frontend (UI, component, state, responsive, accessibility), backend (API, business logic, xác thực, phân quyền, validation), database/Supabase (schema, migration, RLS, query), và chuỗi validation thật (lint → typecheck → test → build → security). Kích hoạt khi người dùng muốn xây tính năng mới, sửa lỗi, refactor, review code, hoặc kiểm thử cho một dự án phần mềm; hoặc khi chạy các command /build-feature, /fix, /review, /test, /security-check. Skill này là bộ quy ước dùng chung cho các agent app-planner, app-builder, code-reviewer, app-tester, security-reviewer — không tự chọn framework thay người dùng và không tự deploy.
---

# Phát triển app / website

## Phạm vi

Hỗ trợ: dò kiến trúc một dự án phần mềm bất kỳ, lập kế hoạch thay đổi, viết code frontend/backend/database theo đúng quy ước sẵn có của dự án đó, và chạy chuỗi validation thật.

Không làm: không chọn framework thay người dùng khi dự án chưa có; không deploy; không đụng production; không tự thêm công cụ/thư viện mới khi chưa được yêu cầu.

## Khi nào dùng

Dùng khi yêu cầu liên quan tới code: tính năng mới, sửa lỗi, review, kiểm thử, rà bảo mật. Không dùng cho việc dựng video (xem `bien-tap-video`) hay nội dung marketing (xem `marketing`).

## Đầu vào

Yêu cầu bằng lời của người dùng, cộng với chính source code của dự án đang mở. Skill này **không giả định** dự án dùng framework nào — luôn dò trước.

## Quy trình

### 1. Dò kiến trúc (bắt buộc, không được bỏ)

Đọc theo thứ tự, dừng khi đã đủ hiểu:

| File | Cho biết |
|---|---|
| `package.json` | framework, script lint/test/build thật, dependency |
| `pyproject.toml` / `requirements.txt` | dự án Python, công cụ test |
| `go.mod`, `Cargo.toml`, `composer.json` | ngôn ngữ khác |
| `Makefile`, `justfile` | lệnh chuẩn của dự án |
| `.github/workflows/*.yml` | **chuỗi kiểm tra mà dự án thực sự tin dùng** — nguồn chính xác nhất cho lệnh validation |
| `tsconfig.json`, `.eslintrc*`, `ruff.toml` | quy ước code |
| `supabase/`, `prisma/`, `migrations/` | tầng dữ liệu |
| `README.md`, `CONTRIBUTING.md` | quy ước riêng của nhóm |

Thư mục trống hoặc chưa có file nào ở trên → đây là dự án mới. **Dừng lại hỏi người dùng** về framework và tầng dữ liệu; đó là quyết định kiến trúc lớn, không tự chọn.

### 2. Xác định lệnh validation thật

Ghi ra danh sách lệnh lấy được từ bước 1. Không suy đoán. Bước nào dự án không có thì ghi rõ là không có — sau này báo cáo `NOT RUN`, không báo PASS.

### 3. Đọc trước khi sửa

Đọc file sắp sửa, chỗ gọi tới nó (`Grep`), và test liên quan. Không đoán API thư viện — mở source hoặc tài liệu ra xem.

### 4. Viết code theo lớp

- Frontend → [references/frontend.md](references/frontend.md)
- Backend / API → [references/backend.md](references/backend.md)
- Database / Supabase → [references/supabase.md](references/supabase.md)

### 5. Kiểm thử

Theo [references/kiem-thu.md](references/kiem-thu.md). Chuỗi bắt buộc:

```text
lint → typecheck → unit → integration → build → security
```

Dừng ngay khi có FAIL, sửa, chạy lại chính lệnh đó.

## Rule bắt buộc

Đọc và tuân thủ:

- [rules/global.md](rules/global.md) — không bịa, NO TEST = NO PASS, vòng lặp FAIL → sửa → chạy lại
- [rules/coding.md](rules/coding.md) — đọc trước khi sửa, thay đổi nhỏ nhất, không phá thứ đang PASS
- [rules/security.md](rules/security.md) — secret, RLS, lệnh bị chặn

Hai hook đang hoạt động sẽ chặn nếu vi phạm: `guard_secrets.py` (ghi secret) và `guard_bash.py` (lệnh phá dữ liệu / thao tác ra ngoài).

## Phụ thuộc

Chính công cụ của dự án đang mở (npm/pnpm/pip/go...). Skill này không tự cài thêm gì.

## Đầu ra

Object theo [data-contracts/app.schema.json](data-contracts/app.schema.json): `ImplementationPlan`, `ImplementationResult`, `TestReport`, `ReviewReport` — tùy agent nào đang chạy.

Kèm bản tóm tắt tiếng Việt: đã sửa file nào, chạy lệnh gì, kết quả từng hạng mục.

## Xử lý thất bại

| Tình huống | Xử lý |
|---|---|
| Validation FAIL | Sửa nguyên nhân gốc → chạy lại đúng lệnh đó. Tối đa 3 vòng, sau đó dừng và báo người dùng những gì đã thử. |
| Test đang đỏ sẵn từ trước | Ghi nhận là trạng thái nền, không nhận là do mình, không tự sửa nếu ngoài phạm vi. |
| Dự án không có lint/test/build | Ghi `NOT RUN (dự án không có)`. Không tự thêm công cụ mới. |
| Cần secret, cần deploy, cần đụng production | Dừng, báo người dùng tự làm. |
| Thư viện dùng khác với hiểu biết của mình | Đọc source trong `node_modules`/site-packages hoặc tài liệu. Không đoán. |
