# Transitions (chuyển cảnh)

Dùng filter `xfade` (video) + `acrossfade` (audio) của ffmpeg — đã kiểm chứng thực tế trong dự án (dissolve 1.0s giữa 2 clip, chạy sạch không lỗi).

## Công thức chung

```bash
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=<KIEU>:duration=<THOI_LUONG>:offset=<DIEM_BAT_DAU>[v];[0:a][1:a]acrossfade=d=<THOI_LUONG>[a]" \
  -map "[v]" -map "[a]" \
  -c:v libx264 -preset fast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 192k output.mp4
```

- `offset` = thời điểm (giây, tính từ đầu clip1) bắt đầu hiệu ứng chuyển — thường đặt = `thời lượng clip1 - duration`.
- `duration` = độ dài hiệu ứng chuyển, 0.5–1.2s cho nội dung trang trọng, 0.2–0.4s cho nhịp nhanh mạng xã hội.
- Bắt buộc 2 input cùng codec/resolution/fps trước khi xfade — chuẩn hoá bằng `scale`/`fps` filter trước nếu khác nhau.

## Bảng ánh xạ tên CapCut ↔ `xfade transition=`

| Tên CapCut (gần đúng) | Giá trị `transition=` | Cảm giác |
|---|---|---|
| Dissolve/Cross Dissolve | `dissolve` | Mượt, 2 cảnh chồng lẫn nhau — dùng cho nội dung trang trọng |
| Fade (qua đen) | `fade` | Dip to black, cổ điển |
| Fade trắng | `fadewhite` | Dip to white — dùng cho nội dung sáng/tích cực |
| Wipe trái→phải | `wipeleft` / `wiperight` | Quét ngang, dứt khoát |
| Wipe lên/xuống | `wipeup` / `wipedown` | Quét dọc |
| Slide trái/phải/lên/xuống | `slideleft` / `slideright` / `slideup` / `slidedown` | Cảnh 2 đẩy cảnh 1 ra, năng động, hợp mạng xã hội |
| Circle Open/Close | `circleopen` / `circleclose` | Vòng tròn mở/đóng, hợp reveal |
| Zoom (phóng to) | `zoomin` | Phóng to vào cảnh 2 |
| Pixelize | `pixelize` | Vỡ pixel — hợp nội dung công nghệ/gaming |
| Radial | `radial` | Quét theo bán kính, giống kim đồng hồ |
| Diagonal | `diagtl` / `diagtr` / `diagbl` / `diagbr` | Quét chéo từ 1 góc |

Danh sách đầy đủ (~50 kiểu): `ffmpeg -h filter=xfade` để xem tất cả giá trị `transition` hỗ trợ trên máy hiện tại.

## Lưu ý khi dùng nhiều transition liên tiếp

- Chỉ dùng transition có hiệu ứng mạnh (wipe, slide, circle) tại điểm chuyển **phân đoạn lớn**; giữa các cảnh nhỏ cùng phân đoạn nên dùng `dissolve` nhẹ hoặc cắt cứng — theo đúng nguyên tắc "hiệu ứng dùng đúng chỗ" đã đúc kết trong `bien-tap-video/references/nguyen-tac-chat-luong.md`.
- Nối nhiều hơn 2 clip: chain nhiều `xfade` liên tiếp trong cùng 1 filter_complex (mỗi cặp 1 xfade, output của xfade trước làm input cho xfade sau), không tách thành nhiều lần render riêng — tránh double-encode.
