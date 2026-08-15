# QC Checklist — Trợ lý Video Bản tin Tấn

## Nội dung
- [ ] Đúng tên người, đơn vị, sự kiện, ngày tháng.
- [ ] Không thêm số liệu/quy định ngoài nguồn.
- [ ] Không lỗi chính tả tiếng Việt trên banner.
- [ ] Banner đúng cảnh và không lặp quá mức.

## Hình ảnh
- [ ] MC không bị che mặt.
- [ ] Banner không che người phát biểu/màn hình/phông sự kiện.
- [ ] Facebook/Zalo nhỏ gọn, không chiếm khung hình.
- [ ] ATT NEWS nhất quán.
- [ ] Không dùng effect gây rối.
- [ ] Kiểm tra đầu, giữa, cuối và các điểm chuyển cảnh.

## Âm thanh
- [ ] Có audio nếu nguồn có tiếng.
- [ ] MC rõ, không clipping.
- [ ] Nếu dùng Hoài - Natural: đúng voice đã resolve, không giả định theo tên.
- [ ] Nhạc nền nếu có phải thấp hơn lời đọc.

## File kỹ thuật
Chạy:
```bash
ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,width,height,pix_fmt -of default=nw=1 OUTPUT.mp4
```
Yêu cầu:
- [ ] codec video H.264.
- [ ] audio AAC nếu có audio.
- [ ] pix_fmt yuv420p.
- [ ] duration đủ, sai lệch không đáng kể so với timeline dự kiến.
- [ ] `+faststart` khi xuất file giao.
- [ ] dung lượng phù hợp để tải/phát trên trình duyệt.

## Kiểm tra lỗi render
- [ ] Không giao file chỉ vì file tồn tại.
- [ ] Nếu render timeout, kiểm duration file dở trước khi làm tiếp.
- [ ] Video >60s + filter graph nặng: ưu tiên chia segment.
- [ ] Sau concat, ffprobe lại file cuối.

## Delivery
Chỉ thông báo hoàn tất sau khi tất cả mục bắt buộc PASS. Nếu bản Full HD quá nặng, tạo thêm bản 720p nhẹ, không tự xóa bản chất lượng cao.
