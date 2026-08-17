# Filters (bộ lọc màu)

Dùng tổ hợp `eq` (sáng/tương phản/bão hòa) + `curves` (đường cong tông màu) + `colorbalance` (cân bằng màu theo shadow/midtone/highlight) + `vignette` (tối 4 góc). Đã kiểm chứng thực tế trong dự án (3 vùng màu: trung tính, đỏ-vàng bão hòa cao, tương phản cao).

## Công thức chung

```bash
ffmpeg -i input.mp4 -vf "<FILTER_CHAIN>" -c:v libx264 -preset fast -crf 19 -pix_fmt yuv420p -c:a copy output.mp4
```

## Bảng filter kiểu CapCut

| Tên CapCut (gần đúng) | Filter chain ffmpeg | Ghi chú |
|---|---|---|
| Natural/Trung tính | `eq=contrast=1.06:saturation=1.0,curves=master='0/0 0.25/0.23 0.75/0.77 1/1'` | Tăng nhẹ tương phản, không đổi tông màu — đã dùng cho nội dung trang trọng |
| Vibrant/Rực rỡ | `eq=contrast=1.10:saturation=1.25,colorbalance=rs=0.05:bs=-0.06:rm=0.06:bm=-0.05:rh=0.10:bh=-0.08` | Đỏ-vàng bão hòa cao — đã dùng cho cảnh sân khấu/lễ hội |
| Cinematic (teal-orange) | `eq=contrast=1.18:saturation=1.05,colorbalance=rs=0.03:bs=-0.02:bm=0.02:rh=0.06:bh=-0.04,curves=master='0/0 0.2/0.15 0.8/0.85 1/1'` | Bóng ngả xanh lục lam, highlight ngả cam — đã dùng cho đoạn cao trào |
| Đen trắng (B&W) | `hue=s=0,eq=contrast=1.15` | Khử màu hoàn toàn + tăng tương phản |
| Vintage/Retro | `curves=r='0/0.05 0.5/0.5 1/0.95':g='0/0 0.5/0.5 1/0.9':b='0/0.1 0.5/0.45 1/0.8',eq=saturation=0.75:contrast=0.95` | Nâng đen (không đen tuyệt đối), ngả vàng nhẹ, giảm bão hòa |
| Ấm (Warm) | `colorbalance=rs=0.08:bs=-0.08:rm=0.06:bm=-0.06` | Đẩy đỏ/vàng lên, giảm xanh lam |
| Lạnh (Cool) | `colorbalance=rs=-0.06:bs=0.08:rm=-0.04:bm=0.06` | Ngược lại Warm — đẩy xanh lam lên |
| Vignette (tối 4 góc) | `vignette=angle=PI/4:mode=backward` | Ghép thêm vào cuối chain bất kỳ filter nào ở trên |
| Phim cũ (film grain nhẹ) | `noise=alls=8:allf=t+u` | Thêm nhiễu hạt — dùng liều nhẹ (alls dưới 15) tránh vỡ hình |

## Nguyên tắc chọn filter theo nội dung

- Nội dung tư liệu/phỏng vấn/tin tức trang trọng: **Natural** hoặc chỉnh nhẹ, không dùng Vintage/B&W (làm mất tính xác thực).
- Nội dung sự kiện/lễ hội/sân khấu: **Vibrant** — nhấn không khí.
- Đoạn cao trào/kết phim: **Cinematic** — tạo điểm nhấn cảm xúc khác biệt phần còn lại.
- Vintage/B&W chỉ dùng khi nội dung chủ đích hoài niệm/nghệ thuật, không dùng mặc định.

## Kiểm tra trước khi áp toàn video

Luôn test 1 filter trên 1 frame trước bằng:
```bash
ffmpeg -y -ss <giay> -i input.mp4 -frames:v 1 -vf "<FILTER_CHAIN>" preview.png
```
Xem ảnh preview, đặc biệt kiểm tra **da mặt người không bị ám màu bất thường** trước khi áp lên cả clip.
