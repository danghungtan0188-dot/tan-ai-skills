# Nhịp dựng video người nói

Mức khởi điểm, chỉnh theo góp ý sau mỗi video. Các mục đều **mặc định tắt**: chỉ làm khi người dùng yêu cầu hoặc đã duyệt ở thẻ cài đặt.

| Mục | Cách làm |
|---|---|
| **Punch-in** | Phóng nhẹ che cú cắt, khoảng 30 giây một lần, đặt ở câu mở đầu, tiêu đề từng ý, câu hỏi cho người xem, câu nhắc lại và câu cuối. Không che mặt, không phóng tới mức vỡ hình. |
| **Hình chèn** | Gắn đúng từ đang nhắc tới hình đó, dùng `tim_cau_noi.py`. Với quay màn hình, chọn đoạn sao cho khoảnh khắc quan trọng rơi đúng lúc nói. |
| **Đồ họa và cú cắt** | Không để lộ người nói dưới 0,5 giây giữa đồ họa và cú cắt; kiểm bằng `scripts/kiem_chop_hinh.py`. |
| **Âm thanh** | Giữ nguyên mức giọng, chỉ tăng khi đỉnh còn dư. Nhạc thấp hơn giọng khoảng 15 dB, tiếng động khoảng 6,5 dB. Quay màn hình và đồ họa tắt tiếng. |
| **Nhạc** | Mỗi phần một bản, đổi ngay trước ý lớn, chồng 0,6 giây mỗi bên. Giữ khoảng 2 giây sau chữ cuối để nhạc ngân hết. |
| **Màu** | Lớp chỉnh màu nằm ngay trên hình người nói, để hình chèn và đồ họa giữ màu thật. |

## Khi được phép cắt

- Chỉ áp dụng khi `cut_authorized` là `true`. Cắt lời lặp nghĩa là giữ lần nói trọn vẹn cuối và bỏ các lần hỏng trước đó; không xóa hết tiếng đệm và khoảng lặng.
- Kiểm điểm cắt bằng `scripts/kiem_diem_cat.py`, rồi nghe lại bản đã cắt bằng `scripts/nghe_lai_sau_cat.py` và đọc cả file lời.
- Câu tự sửa không có chỗ lặng để cắt thì giữ nguyên và ghi vào báo cáo.
