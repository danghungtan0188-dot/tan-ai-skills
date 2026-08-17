# Kiểm thử và validation

Đọc khi chạy kiểm tra hoặc viết test.

## Tìm lệnh thật — không bịa

Nguồn đáng tin, theo thứ tự ưu tiên:

1. `.github/workflows/*.yml` — chuỗi mà dự án thực sự tin dùng, chính xác nhất
2. `package.json` → `scripts`
3. `Makefile` / `justfile`
4. `pyproject.toml` → `[tool.pytest]`, `[tool.ruff]`
5. `README.md` mục hướng dẫn chạy

Không tìm thấy lệnh cho một bước → bước đó là `NOT RUN (dự án không có)`. **Không tự thêm công cụ test mới vào dự án** để có cái mà chạy.

## Thứ tự chạy

```text
lint → typecheck → unit → integration → build → security
```

Rẻ trước, đắt sau. **Dừng ngay khi có FAIL**, sửa nguyên nhân, chạy lại đúng lệnh vừa FAIL. Không chạy tiếp các bước sau khi bước trước đang đỏ.

## Ghi nhận kết quả

Với mỗi bước ghi đủ: lệnh đã chạy, exit code, phần output có ý nghĩa.

Ba trạng thái, không có trạng thái thứ tư:

| Trạng thái | Điều kiện |
|---|---|
| `PASS` | đã chạy thật, exit code 0 |
| `FAIL` | đã chạy thật, exit code khác 0 |
| `NOT_RUN` | chưa chạy — bắt buộc kèm lý do |

Không bao giờ viết "ALL PASS". Không suy ra kết quả của bước chưa chạy.

## Viết test

**Sửa bug** → test tái hiện bug trước, xác nhận **đỏ**, rồi mới sửa, rồi xác nhận **xanh**. Test viết sau khi đã sửa mà không thấy nó đỏ bao giờ thì không chứng minh được gì.

**Tính năng mới** → tối thiểu: happy path, một input sai, một edge case thật (rỗng, null, 0, chuỗi tiếng Việt có dấu, số lớn).

Không viết test hình thức để tăng số lượng. Test khẳng định lại hằng số (`expect(1).toBe(1)`) hoặc chỉ gọi hàm mà không kiểm kết quả là test rác.

## Hồi quy

Trước khi sửa: chạy bộ test hiện có, **ghi lại trạng thái nền**. Sau khi sửa: chạy lại đúng bộ đó.

Test đang xanh mà chuyển đỏ = phải sửa. Không được `skip`, không được sửa assertion cho khớp với hành vi mới trừ khi hành vi mới đúng là điều người dùng yêu cầu — và khi đó phải nói rõ đã đổi test nào, vì sao.

Test đã đỏ sẵn từ trước khi mình động vào: ghi nhận, không nhận là do mình, không tự sửa nếu ngoài phạm vi.

## Test flaky

Chạy lại tối đa 2 lần. Vẫn lúc xanh lúc đỏ → ghi rõ là **flaky**, không ghi PASS. Flaky là lỗi thật, chỉ là chưa tìm ra.

## Các nhóm cần phủ

```text
happy path
input sai định dạng
input thiếu
edge case (rỗng, 0, null, chuỗi dài, tiếng Việt có dấu)
hồi quy (bug đã từng xảy ra)
bảo mật (truy cập không có quyền phải bị chặn)
```
