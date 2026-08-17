# Bước H: Tự kiểm tra chất lượng trước khi giao

Áp dụng Nguyên tắc cứng #6 trong SKILL.md: không trình video chưa qua bước này. Tối đa 3 lần tự sửa, quá đó báo cụ thể cho người dùng.

## 1. Kiểm tra tự động bằng `scripts/kiem_tra_dau_ra.py`

```bash
python skills/video-san-pham/scripts/kiem_tra_dau_ra.py duong-dan/SP001_tiktok.mp4 \
  --do-phan-giai 1080x1920 --thoi-luong-toi-thieu 12 --thoi-luong-toi-da 40
```

Script gọi `ffprobe` (bắt buộc có sẵn trên PATH — đi kèm cài đặt `video-use`) để đối chiếu:

- Độ phân giải thực tế của file xuất khớp với độ phân giải đích của nền tảng.
- Thời lượng nằm trong khoảng hợp lý đã đặt kế hoạch.
- File có cả video track và audio track (phát hiện lỗi xuất thiếu tiếng — lỗi âm thầm hay gặp nhất).

Không có `ffprobe` trên máy: báo cho người dùng thay vì bỏ qua bước kiểm tra.

## 2. Kiểm tra bằng mắt/tai (không tự động hoá được, vẫn bắt buộc)

- **Đồng bộ audio–phụ đề**: xem 2–3 điểm trong video (đầu, giữa, cuối), phụ đề xuất hiện đúng lúc lời đọc phát ra từ đó, không sớm/muộn quá ~150ms.
- **Chữ không bị cắt/che**: tên/giá/CTA và phụ đề không bị chồng lên nhau, không nằm trong vùng an toàn nền tảng (xem `dinh-dang-xuat-tiktok-facebook.md`), không bị cắt ở mép khung sau khi crop ảnh.
- **Âm lượng**: giọng đọc luôn nghe rõ hơn nhạc nền (nếu có); không có tiếng "pop" tại điểm nối cảnh.
- **Đúng dữ liệu thật**: giá, tên, CTA hiển thị trên video khớp chính xác với dữ liệu đã xác nhận ở Bước A — đối chiếu lại 1 lần cuối, đây là điểm dễ sai nhất khi overlay được gõ tay.
- **Ảnh không méo**: chủ thể sản phẩm còn nguyên tỉ lệ, không bị kéo giãn dẹt/cao bất thường.

## 3. Khi phát hiện lỗi

1. Xác định lỗi thuộc bước nào (D: ASR sai timestamp, E: dựng cảnh/overlay sai, F: nội dung có rủi ro, G: xuất sai thông số).
2. Sửa đúng bước đó, không làm lại từ đầu toàn bộ pipeline nếu không cần thiết (vd. lỗi overlay chỉ cần dựng lại Bước E + xuất lại Bước G, không cần tổng hợp giọng lại).
3. Render lại, chạy lại Bước H.
4. Đếm số lần lặp. Tới lần thứ 3 vẫn còn lỗi: dừng, báo rõ cho người dùng lỗi gì, đã thử sửa gì, tại sao chưa hết — không lặp vô hạn.

## 4. Báo cáo kèm khi giao video

Một đoạn ngắn: nguồn dữ liệu đã dùng (mã sản phẩm, dòng Excel), giọng đọc, engine dựng cảnh (Remotion/HyperFrames), kết quả Bước H (đạt ngay / số lần sửa lại và lý do), và caption + hashtag gợi ý để đăng.
