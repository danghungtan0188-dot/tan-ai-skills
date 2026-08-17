# Backend / API

Đọc khi thay đổi endpoint, business logic, xác thực, phân quyền, hoặc xử lý lỗi phía server.

## Thứ tự bắt buộc trong mọi endpoint

```text
1. Validate input      → sai định dạng thì trả 400 ngay, chưa chạm database
2. Xác thực (authn)    → chưa đăng nhập thì 401
3. Phân quyền (authz)  → đăng nhập rồi nhưng không có quyền TRÊN BẢN GHI ĐÓ thì 403
4. Xử lý nghiệp vụ
5. Trả kết quả / mã lỗi đúng ngữ nghĩa
```

Bước 3 là chỗ hay bị bỏ sót nhất. "Đã đăng nhập" **không** đồng nghĩa "được sửa bản ghi này". Endpoint sửa/xóa mà chỉ kiểm đăng nhập là lỗi bảo mật mức chặn.

## Validate input

Dùng đúng thư viện validate mà dự án đã dùng (zod, pydantic, joi...). Không tự viết kiểm tra tay song song với thư viện đó.

Không tin bất cứ gì từ client: id, số lượng, giá, vai trò, cờ quyền. Trường quyết định quyền hạn phải lấy từ session phía server, không lấy từ body.

## Mã lỗi

| Tình huống | Mã |
|---|---|
| Input sai định dạng/thiếu trường | 400 |
| Chưa đăng nhập / token hỏng | 401 |
| Đã đăng nhập nhưng không có quyền | 403 |
| Không tìm thấy bản ghi | 404 |
| Xung đột trạng thái (trùng, đã xử lý rồi) | 409 |
| Lỗi phía server | 500 |

Trả 200 kèm `{error: ...}` là sai. Trả 500 cho input sai cũng sai.

## Xử lý lỗi

- Không `try/except` nuốt lỗi im lặng. Bắt được thì phải log có ngữ cảnh hoặc ném lại.
- **Không trả stack trace ra response.** Log phía server, trả cho client thông điệp chung + mã tra cứu.
- Chỉ bắt lỗi cho tình huống thực sự xảy ra được. Không thêm fallback cho trường hợp không thể xảy ra.

## Secret và cấu hình

Đọc từ biến môi trường (`process.env`, `os.environ`). Không hardcode. Không log. Không đưa vào URL/query string. Thiếu biến môi trường bắt buộc thì **fail sớm lúc khởi động** kèm thông báo rõ tên biến, đừng để chạy tới lúc gọi API mới lỗi.

## Transaction và dữ liệu

Nhiều thao tác ghi phải cùng thành công hoặc cùng thất bại → dùng transaction. Không tự chạy migration/xóa dữ liệu ngoài phạm vi yêu cầu.

## Kiểm trước khi báo xong

```text
[ ] mỗi endpoint mới/sửa: đã kiểm authn + authz trên đúng bản ghi
[ ] input sai → trả đúng 400, không 500
[ ] không có secret trong code, log, hay response
[ ] typecheck + test + build sạch
```
