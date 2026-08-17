# Database / Supabase

Đọc khi thay đổi schema, migration, RLS, Auth, Storage, hoặc query.

## Tuyệt đối không tự làm

Những việc sau **luôn** phải để người dùng tự làm, kể cả khi họ nói "cứ làm đi":

- reset database (`supabase db reset`)
- xóa dữ liệu thật (`DELETE`, `TRUNCATE`, `DROP`)
- tắt Row Level Security
- tạo hoặc lộ Service Role key
- thao tác trên project production

Hook `guard_bash.py` chặn phần lớn các lệnh này. Bị chặn thì báo người dùng, không tìm cách lách.

## Migration

- Mỗi thay đổi schema = **một file migration mới**, đặt tên có timestamp theo quy ước sẵn có của dự án.
- **Không sửa migration đã apply.** Sai thì viết migration mới để sửa lại.
- Migration phải chạy được trên database rỗng từ đầu tới cuối.
- Thêm cột `NOT NULL` vào bảng đã có dữ liệu → phải có `DEFAULT`, hoặc chia làm 3 bước (thêm nullable → backfill → siết ràng buộc).

## Row Level Security

Mọi bảng chứa dữ liệu người dùng **bắt buộc** bật RLS ngay trong migration tạo bảng:

```sql
alter table public.<ten_bang> enable row level security;
```

Bật RLS mà không có policy = không ai đọc được. Bật rồi thì phải viết policy cho từng thao tác thực sự cần: `select`, `insert`, `update`, `delete`.

Nguyên tắc viết policy:

- So khớp với `auth.uid()`, không so khớp với giá trị client gửi lên.
- Policy `using` (đọc/lọc) và `with check` (ghi) là hai chuyện khác nhau — thiếu `with check` thì người dùng ghi được bản ghi mang `user_id` của người khác.
- Không viết policy `using (true)` cho bảng có dữ liệu riêng tư.

Bảng mới không có RLS hoặc không có policy → `security-reviewer` phải báo mức `blocker`.

## Khóa và index

- Khóa ngoại phải có ràng buộc thật (`references`), không chỉ quy ước đặt tên.
- Cột dùng để lọc/join thường xuyên thì có index. Không tạo index cho mọi cột.
- Nêu rõ hành vi `on delete` (cascade / set null / restrict) — mặc định im lặng dễ gây rác dữ liệu.

## Query

- Không nối chuỗi SQL từ input người dùng. Dùng tham số hóa hoặc query builder của dự án.
- Không `select *` ở đường dẫn nóng; lấy đúng cột cần.
- Truy vấn danh sách phải có phân trang và giới hạn.

## Storage

Bucket mặc định để **private**. Public chỉ khi nội dung thực sự công khai. File người dùng tải lên: kiểm kiểu file và dung lượng phía server, không chỉ phía client.

## Kiểm trước khi báo xong

```text
[ ] migration mới chạy sạch trên database rỗng
[ ] bảng mới đã bật RLS và có policy cho từng thao tác cần
[ ] policy dùng auth.uid(), có cả using và with check
[ ] không có query nối chuỗi từ input người dùng
[ ] không có Service Role key ở phía client
```

Không chạy thử được migration → ghi `NOT RUN` kèm lý do, không ghi PASS.
