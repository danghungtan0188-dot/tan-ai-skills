# Cấu trúc tổng thể

Dựa trên video mẫu (~182 giây / 3:02, 1920x1080, 30fps), video tổng kết sự kiện/hội thi kiểu này chia thành 8 phân đoạn theo trình tự cố định. Tỉ lệ % là thời lượng gợi ý theo tổng thời lượng video — điều chỉnh theo độ dài thực tế, không phải con số bắt buộc.

| # | Phân đoạn | Tỉ lệ gợi ý | Nội dung |
|---|---|---|---|
| 1 | Mở đầu | ~5% | Cảnh hội trường, khán giả vẫy tay/vỗ tay — tạo không khí trước khi vào tiêu đề |
| 2 | Title card | ~3% | Banner tên sự kiện (đơn vị + tên hội thi + lần thứ mấy + năm) — xem [do-hoa-tieu-de.md](do-hoa-tieu-de.md) |
| 3 | Phần thi tình huống/tiểu phẩm | ~20% | Dàn dựng như phim ngắn trên sân khấu, có bối cảnh riêng (ví dụ: phòng họp giả lập, hiện trường giả lập) |
| 4 | Phần thi kiến thức (gameshow) | ~15% | Overlay đồ họa đếm ngược + câu hỏi trắc nghiệm chồng lên video thật — xem [overlay-gameshow.md](overlay-gameshow.md) |
| 5 | Phỏng vấn | ~10% | Máy quay tay, mic phóng viên, không cắt lower-third tên người được phỏng vấn |
| 6 | Khai mạc/sân khấu lớn | ~15% | Ánh sáng sân khấu (spotlight vàng/đỏ, khói), tiết mục văn nghệ — chuyển vào bằng hiệu ứng transition, xem [transition-hieu-ung.md](transition-hieu-ung.md) |
| 7 | Trao giải + ăn mừng | ~15% | Đội nhận cờ/bằng khen, khán giả vỗ tay, ánh sáng nhấp nháy |
| 8 | Hero-intro / outro | ~17% | Từng thành viên đội bước ra giới thiệu kiểu trailer, kết bằng title card tên đội — xem [hero-intro.md](hero-intro.md) |

## Nguyên tắc chuyển đoạn

- Trong cùng 1 phân đoạn: cắt cứng (hard cut) giữa các góc máy, nhịp cắt trung bình 2–4 giây/cảnh.
- Giữa 2 phân đoạn lớn có tính chất khác nhau (ví dụ: từ "hội trường" sang "sân khấu lớn"): dùng hiệu ứng transition có chủ đích (xem [transition-hieu-ung.md](transition-hieu-ung.md)), không cắt cứng.
- Đoạn hero-intro cuối luôn tách biệt hẳn về nhịp điệu và màu sắc so với phần còn lại — báo hiệu đây là đoạn "cao trào/kết".

## Cách phân tích một video mẫu khác (quy trình đã dùng)

Khi người dùng đưa 1 video và muốn phân tích cách dựng, dùng ffmpeg để trích khung hình định kỳ thành 1 ảnh lưới (contact sheet) rồi xem bằng công cụ đọc ảnh — tránh phải xem toàn bộ video theo thời gian thực:

```bash
ffprobe -v error -show_entries format=duration,size,bit_rate \
  -show_entries stream=codec_name,codec_type,width,height,avg_frame_rate \
  -of default=noprint_wrappers=1 input.mp4

ffmpeg -y -i input.mp4 -vf "fps=1/5,scale=320:-1,tile=6x7" -frames:v 1 -update 1 contact_sheet.png
```

- `fps=1/5`: 1 khung hình mỗi 5 giây — điều chỉnh mật độ theo thời lượng video (video càng dài, khoảng cách càng lớn để giữ số ô lưới hợp lý, khoảng 30–42 ô là vừa đọc).
- `tile=6x7`: số cột x số hàng của lưới ảnh, tính sao cho đủ chứa tổng số khung hình trích được.
- Bắt buộc thêm `-update 1` khi dùng `-frames:v 1` để ghi ảnh tĩnh, nếu không ffmpeg sẽ báo lỗi thiếu pattern tên file chuỗi ảnh.

Sau khi có contact sheet, đọc ảnh bằng công cụ đọc file ảnh và mô tả từng phân đoạn theo bảng cấu trúc ở trên.
