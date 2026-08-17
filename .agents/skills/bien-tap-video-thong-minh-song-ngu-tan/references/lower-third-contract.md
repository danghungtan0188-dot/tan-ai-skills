# Banner người phát biểu

Dùng cùng chuẩn với video bản tin: `name`, `detail`, `start`, `end`, `position`. `detail` là chức vụ–đơn vị hoặc địa chỉ đã được xác minh.

```json
[{"start":12.4,"end":18.0,"name":"Ông NGUYỄN VĂN A","detail":"Chức vụ – Đơn vị hoặc địa chỉ đã xác minh","position":"bottom_left"}]
```

- Không suy đoán danh tính/chức vụ từ khuôn mặt hoặc giọng nói; thiếu dữ liệu thì hỏi người dùng.
- Hiện sau khi bắt đầu phát biểu 0,2–0,4 giây, thường 4–6 giây và chỉ ở lần giới thiệu đầu.
- Tên ở dòng trên, chức vụ/đơn vị hoặc địa chỉ ở dòng dưới; chữ trắng trên nền xanh chính thống.
- Không che mặt và không chồng phụ đề song ngữ. Ưu tiên lower-third ở khoảng 70–82% chiều cao; chuyển phụ đề xuống vùng an toàn hoặc đẩy lower-third lên khi cần.

Tạo file bằng `scripts/make_lower_thirds_ass.py lower-thirds.json lower-thirds.ass`.
