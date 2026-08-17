# Rule lập trình (App / Website)

Áp dụng cho `app-planner`, `app-builder`, `code-reviewer`, `app-tester` và skill `phat-trien-app`.

## 1. Đọc trước khi sửa

Không viết dòng nào trước khi đã đọc: file sắp sửa, chỗ gọi tới nó, và test hiện có (nếu có). Không đoán API của thư viện — mở file/`node_modules` hoặc tài liệu ra xem.

## 2. Thay đổi nhỏ nhất

- Không "cải thiện" đoạn bên cạnh, không đổi format, không đổi tên biến ngoài phạm vi.
- Không viết lại thứ đang chạy tốt.
- Theo đúng văn phong, cách đặt tên, mật độ comment của code xung quanh.
- Ưu tiên tái sử dụng hàm/component đã có hơn viết mới.
- Không thêm lớp cấu hình/trừu tượng cho thứ chỉ dùng một lần.

## 3. Không phá thứ đang PASS

Trước khi sửa: chạy test/build hiện có, ghi lại trạng thái nền. Sau khi sửa: chạy lại đúng bộ đó. Có test đang xanh mà chuyển đỏ = phải sửa, không được bỏ qua hay đánh dấu skip.

## 4. Test

- Sửa bug → viết test tái hiện bug **trước**, xác nhận nó đỏ, sửa, xác nhận nó xanh (regression test).
- Thêm tính năng → có test cho happy path và ít nhất 1 input sai.
- Không viết test hình thức chỉ để tăng số lượng.

## 5. Thứ tự validation

Chạy theo thứ tự này, dừng ngay khi có FAIL và sửa trước khi đi tiếp:

```text
1. lint        → sửa lỗi cú pháp/style trước, rẻ nhất
2. typecheck   → sửa lỗi kiểu
3. unit test
4. integration test (nếu có)
5. build
6. security-check
```

Lệnh cụ thể lấy từ `package.json` scripts / `Makefile` / `pyproject.toml` của chính dự án — **không tự bịa lệnh**. Dự án không có script nào cho bước nào thì ghi `NOT RUN (dự án không có)`, không ghi PASS.

## 6. Xử lý lỗi

Chỉ bắt lỗi cho tình huống thực sự xảy ra được. Không `try/except` nuốt lỗi im lặng. Không thêm fallback cho trường hợp không thể xảy ra.

## 7. Frontend

Responsive là bắt buộc (mobile trước). Ảnh có `alt`, form control có `label`, tương phản đủ đọc. Không gọi API trực tiếp trong component nếu dự án đã có lớp service/hook.

## 8. Backend

Mọi endpoint: xác thực đầu vào, kiểm tra quyền, trả mã lỗi đúng ngữ nghĩa. Không tin dữ liệu từ client. Không trả stack trace ra response.
