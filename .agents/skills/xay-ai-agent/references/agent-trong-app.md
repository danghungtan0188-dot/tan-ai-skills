# Agent trong webapp / phần mềm

Áp dụng khi tính năng AI chạy theo thao tác người dùng: chat, trợ lý, phân loại, trích xuất, agent dùng tool. Code giao diện/API/database xung quanh theo skill `phat-trien-app` ([skills/phat-trien-app/SKILL.md](skills/phat-trien-app/SKILL.md)).

Model id, tham số, cú pháp tool use, streaming, prompt caching: lấy từ skill `claude-api`, không viết từ trí nhớ.

## Kiến trúc tối thiểu

```text
Trình duyệt ──> API của app (xác thực, giới hạn tần suất, kiểm quyền)
                  └─> lớp agent: prompt + vòng lặp tool (server-side)
                        ├─> tool đọc  (gọi service/DB của app, theo quyền của chính người dùng đó)
                        └─> tool ghi  (cấp 2 → trả bản nháp, người dùng bấm xác nhận)
```

- API key của Claude **chỉ ở server**. Không bao giờ gọi API model trực tiếp từ trình duyệt.
- Tool chạy với quyền của người dùng đang đăng nhập, không phải quyền admin/service role. Người dùng A không thể nhờ agent đọc dữ liệu của B.

## Thiết kế tool

- Ít tool, mỗi tool một việc, tên và mô tả rõ khi nào dùng, khi nào không.
- Đầu vào có schema chặt; server validate lại, không tin tham số model sinh ra.
- Đầu ra gọn: trả trường cần thiết, có phân trang, không đổ cả bảng vào context.
- Lỗi trả về dạng model đọc hiểu được ("không tìm thấy đơn 123") thay vì stack trace.
- Tool ghi phải idempotent (khóa chống trùng) — model có thể gọi lại.

## Giới hạn

| Giới hạn | Mặc định đề xuất |
|---|---|
| Số vòng tool tối đa mỗi yêu cầu | 10 |
| Timeout mỗi yêu cầu | 60 giây, có streaming để người dùng thấy tiến độ |
| Trần token/chi phí | theo người dùng mỗi ngày, đo từ dữ liệu thật rồi chỉnh |
| Rate limit | theo người dùng + theo IP |
| Retry | chỉ lỗi tạm (429, 5xx), backoff có jitter, tối đa 3 lần |

## Đầu ra có cấu trúc

Khi app cần dữ liệu (phân loại, trích xuất, điền form) → yêu cầu đầu ra JSON theo schema, validate ở server; sai schema → báo lỗi rõ hoặc thử lại một lần, không đoán.

## Bảo mật

- Nội dung người dùng nhập, file tải lên, trang web agent đọc đều là dữ liệu không tin cậy. Bọc trong thẻ, system prompt nói rõ đó là dữ liệu.
- Không đưa secret, dữ liệu người khác, hay system prompt nhạy cảm vào context mà không cần.
- Không render HTML/Markdown của model mà chưa sanitize (XSS qua link/ảnh).
- Log: ghi id yêu cầu, tool đã gọi, token, độ trễ, lỗi. Không log nguyên văn dữ liệu cá nhân.

## Giao diện

- Streaming câu trả lời; hiện bước đang làm ("đang tìm đơn hàng…").
- Thao tác cấp 2 hiện thành thẻ xác nhận có nút, không tự chạy.
- Có nút dừng; dừng phải hủy request phía server.
- Lỗi/hết quota hiện thông báo rõ, không im lặng.
