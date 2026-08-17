# Adjustment (hiệu chỉnh hình ảnh)

## Sáng / Tương phản / Bão hòa / Làm nét cơ bản

```
eq=brightness=<−1..1>:contrast=<0..2, mặc định 1>:saturation=<0..3, mặc định 1>
unsharp=5:5:0.8:3:3:0.4
```
`unsharp` làm nét nhẹ — tăng số `0.8` để nét hơn, giảm nếu thấy viền bị "gắt"/nhiễu.

## ⚠️ Giảm rung / Stabilize — bài học thực tế, đọc trước khi dùng

Đã xảy ra lỗi thật trong dự án: chạy `vidstabdetect`+`vidstabtransform` (2-pass) xuyên qua 1 đoạn có **nhiều cú cắt cảnh khác nhau** (không phải 1 cảnh quay liên tục) → gây **vỡ hình/nhiễu nặng** tại điểm cắt, vì bộ ổn định hiểu nhầm cú cắt là 1 chuyển động camera cực lớn cần bù trừ mạnh.

**Quy tắc bắt buộc trước khi dùng:**
1. Xác nhận đoạn định ổn định hóa là **1 cảnh quay liên tục thật sự** (không có cắt dựng bên trong) — kiểm tra bằng cách xem contact sheet/timeline_view trước.
2. Nếu đoạn dài có nhiều cú cắt: **tách riêng từng cảnh liên tục thành clip riêng**, chạy vidstab cho từng clip độc lập, rồi mới nối lại.
3. Sau khi stabilize, **luôn kiểm tra bằng giải mã tuần tự** (không phải seek từng khung — xem phần seek artifact bên dưới) trên toàn bộ đoạn trước khi giao, đặc biệt quanh các điểm nghi ngờ có cắt cảnh.
4. Nếu không chắc đoạn có bị cắt cảnh bên trong hay không: **hỏi người dùng hoặc bỏ qua bước này**, không tự chạy liều — hậu quả (vỡ hình) tệ hơn nhiều so với rung nhẹ ban đầu.

Công thức 2-pass (chỉ dùng khi đã xác nhận điều kiện trên):
```bash
ffmpeg -i input.mp4 -vf vidstabdetect=shakiness=8:accuracy=15:result=transforms.trf -f null -
ffmpeg -i input.mp4 -vf "vidstabtransform=input=transforms.trf:zoom=0:smoothing=15,unsharp=5:5:0.8:3:3:0.4" output.mp4
```

## ⚠️ Kiểm tra khung hình bằng SEEK có thể cho kết quả sai (bài học thực tế)

Đã gặp: dùng `ffmpeg -ss <giây> -frames:v 1` để trích từng khung hình riêng lẻ (kiểu `timeline_view.py`) trên 1 file cụ thể (bản HeyGen render) **cho ra khung hình trắng/chớp giả** không có thật trong video — trong khi giải mã tuần tự (đọc liên tục từ đầu, không seek nhảy) lại hoàn toàn sạch. Đây là lỗi của **cách trích khung hình**, không phải lỗi video thật.

**Khi nghi ngờ 1 lỗi hình ảnh phát hiện qua công cụ xem (timeline_view/screenshot theo giây):** xác minh lại bằng giải mã tuần tự trước khi kết luận video có lỗi:
```bash
ffmpeg -i input.mp4 -ss <bat_dau> -t <do_dai> -vf "select='not(mod(n\,<N>))',tile=<COT>x1" -frames:v 1 kiemtra.png
```
Lệnh này giải mã tuần tự rồi mới chọn khung hiển thị (không seek nhảy từng khung), cho kết quả đáng tin hơn khi cần xác minh lỗi nghi ngờ.

## Kiểm tra tính toàn vẹn file sau mọi lần xử lý

```bash
ffmpeg -v error -i output.mp4 -f null - 2>&1 | head -20
```
Không có output = file sạch. Có `Invalid NAL unit`/`moov atom not found`/lỗi khác = file hỏng, cần render lại bước vừa rồi (đã gặp thật: 1 lần file bị hỏng ngay sau bước loudnorm, render lại là hết).
