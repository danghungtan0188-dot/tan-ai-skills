# Hợp đồng banner người phát biểu

Dùng khi video có người phát biểu, trả lời phỏng vấn hoặc đại diện đơn vị cung cấp thông tin.

```json
[
  {
    "start": 12.4,
    "end": 18.0,
    "name": "Ông NGUYỄN VĂN A",
    "detail": "Chức vụ – Đơn vị hoặc địa chỉ đã xác minh",
    "position": "bottom_left"
  }
]
```

- `name`, `start`, `end` là bắt buộc; `detail` là chức vụ + đơn vị hoặc địa chỉ đã được xác minh.
- Không suy đoán họ tên, học hàm, chức vụ, đơn vị hay địa chỉ từ khuôn mặt/giọng nói. Nếu thiếu, hỏi người dùng hoặc dùng nhãn trung tính đã được duyệt.
- Mỗi người chỉ hiện ở lần xuất hiện/phát biểu đầu, trừ khi cách nhau lâu hoặc ngữ cảnh đổi.
- Mặc định vào sau lời nói 0,2–0,4 giây; thời lượng 4–6 giây; không dài hơn đoạn phát biểu.
- 16:9: đặt góc trái dưới, chừa 5% biên; chiều cao khoảng 13–17% khung hình. 9:16: thu gọn chiều rộng và kiểm tra mặt/người.
- Khi có phụ đề: lower-third nằm cao hơn vùng phụ đề hoặc phụ đề dịch lên; không chồng hai lớp.
- Viết hoa tên ở mức dễ đọc; không viết hoa toàn bộ chức vụ/địa chỉ. Kiểm tra dấu tiếng Việt trước khi render.

Tạo ASS bằng `scripts/make_lower_thirds_ass.py lower-thirds.json lower-thirds.ass --width 1920 --height 1080`.
