# Phiếu chấm thẩm mỹ (cổng duyệt 2)

Dùng sau khi `video_qa.py` và các script kiểm kỹ thuật đã PASS. Phiếu này giúp người dùng duyệt nhanh, **không thay mắt người dùng** và **không có điểm tổng**: AI tự chấm bài của mình thường cho điểm cao.

## Cách chấm

- Mỗi tiêu chí ghi **Đạt** hoặc **Chưa đạt**, kèm mốc giây và điều nhìn hoặc nghe thấy ở đó.
- **Chưa đạt** phải có cách sửa cụ thể. Không có bằng chứng thì không được ghi Đạt.
- Chỉ chấm tiêu chí đã xem khung hình hoặc nghe đoạn đó; chưa xem thì ghi `NOT RUN`.
- Mức số trong bảng là mức khởi điểm, chỉnh theo góp ý sau mỗi video.

| # | Tiêu chí | Đạt khi |
|---|---|---|
| 1 | **3 giây đầu** | Có câu nói, chữ hoặc hình khiến người xem muốn xem tiếp; không mở bằng màn hình trống hay logo dài |
| 2 | **Chữ đọc kịp** | Mỗi dòng chữ hiện ít nhất 1 giây cho mỗi 3 chữ; chữ không chạy khi người xem còn đang đọc |
| 3 | **Nhịp** | Video mạng xã hội không có đoạn quá 8 giây mà hình không đổi gì; bản tin, phim tài liệu không xét mục này |
| 4 | **Đồ họa đúng lúc** | Thẻ hiện đúng câu đang nói tới nó, không che mặt, không lộ chớp hình giữa đồ họa và cú cắt |
| 5 | **Thống nhất** | Một phong cách, một bộ màu, một bộ font cho cả video |
| 6 | **Âm thanh** | Giọng rõ từ đầu đến cuối; nhạc và tiếng động, nếu có, không lấn giọng; không có tiếng bụp ở cú cắt |
| 7 | **Kết** | Có câu chốt hoặc lời kêu gọi rõ; không cắt cụt chữ cuối |

## Mẫu đưa người dùng

```text
PHIẾU THẨM MỸ (AI tự xem, chỉ để tham khảo)
1 3 giây đầu      Đạt       0.0s  câu hỏi "…" kèm chữ to
2 Chữ đọc kịp     Chưa đạt  12.4s dòng 9 chữ chỉ hiện 1,5 giây → kéo dài tới 3 giây
…
```
