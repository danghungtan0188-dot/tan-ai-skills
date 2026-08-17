# Frontend

Đọc khi thay đổi UI, component, state, hoặc phần gọi API phía client.

## Trước khi viết

1. Tìm component/hook **đã có** làm việc tương tự (`Grep` theo tên chức năng, không theo tên file). Có rồi thì dùng lại hoặc mở rộng, không viết bản thứ hai.
2. Xem 2–3 component cùng loại để nắm quy ước: cách đặt tên, cách chia props, cách xử lý loading/error, cách import.
3. Xem dự án dùng gì cho style (CSS module, Tailwind, styled-components) và **dùng đúng cái đó**. Không trộn thêm cách thứ hai.

## Quy ước

**Component** — một component một trách nhiệm. Props có kiểu rõ ràng. Không đặt logic nghiệp vụ trong component nếu dự án đã có lớp service/hook riêng.

**State** — state cục bộ trước; chỉ đưa lên store toàn cục khi thực sự có nhiều nơi cần. Không thêm thư viện state mới.

**Gọi API** — qua lớp client/service sẵn có của dự án. Không `fetch` thẳng trong component khi đã có `apiClient`. Mọi lời gọi phải xử lý đủ ba trạng thái: đang tải, lỗi, rỗng.

**Responsive** — mobile trước. Kiểm ở 375px, 768px, 1280px. Không để tràn ngang: bảng/code/ảnh rộng phải cuộn trong khung riêng.

**Accessibility** — ảnh có `alt` (ảnh trang trí thì `alt=""`), input có `label` gắn đúng `id`, nút bấm là `<button>` chứ không phải `<div onClick>`, thứ tự tab hợp lý, tương phản chữ/nền đủ đọc.

**Tiếng Việt** — chuỗi hiển thị có dấu, không viết tắt tùy tiện. Kiểm chữ dài có bị vỡ layout không (tiếng Việt dài hơn tiếng Anh ~20%). File chứa tiếng Việt lưu UTF-8.

## Không làm

- Không đổi design system, palette, font, spacing scale khi chưa được yêu cầu.
- Không format lại file ngoài phần mình sửa.
- Không thêm animation/hiệu ứng không ai yêu cầu.
- Không hardcode URL API — đọc từ cấu hình/biến môi trường của dự án.

## Kiểm trước khi báo xong

```text
[ ] typecheck sạch
[ ] build sạch
[ ] mở thật ở 375px và 1280px, không tràn ngang
[ ] trạng thái loading / lỗi / rỗng đều hiển thị đúng
[ ] console không có error mới
```

Không mở được app để xem thật → ghi mục đó là `NOT RUN`, không ghi PASS.
