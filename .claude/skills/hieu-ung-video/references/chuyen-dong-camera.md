# Chuyển động camera (Ken Burns, speed ramp, freeze, slow-motion)

## Ken Burns (zoom/pan trên ảnh tĩnh)

CapCut gọi đây là hiệu ứng mặc định khi thêm ảnh vào timeline. Dùng filter `zoompan`:

```bash
ffmpeg -loop 1 -i anh.jpg -t 5 \
  -vf "scale=3840:2160,zoompan=z='min(zoom+0.0015,1.3)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=25" \
  -c:v libx264 -preset fast -crf 19 -pix_fmt yuv420p output.mp4
```

- `d=125` = số khung hình hiệu ứng chạy (125 khung ở 25fps = 5 giây).
- `z='min(zoom+0.0015,1.3)'` = tốc độ zoom, tăng dần tới tối đa 1.3x — chỉnh hệ số 0.0015 để nhanh/chậm.
- Đổi `x=`/`y=` để pan (lia) thay vì chỉ zoom tĩnh giữa khung — ví dụ pan từ trái sang phải: `x='if(eq(on,1),0,x+2)'`.
- **Luôn scale ảnh gốc lên độ phân giải cao hơn đích trước khi zoompan** (ví dụ đích 1080p thì scale ảnh lên ít nhất 4K) để tránh vỡ nét khi zoom.

## Speed ramp (tăng/giảm tốc mượt trong 1 clip)

Đơn giản hóa (tốc độ đổi đột ngột tại 1 mốc, đã dùng thật trong dự án — MC đọc nhanh hơn 1.18x, đồng bộ setpts+atempo giữ khớp khẩu hình):

```bash
ffmpeg -i input.mp4 -vf "setpts=PTS/<HE_SO>" -af "atempo=<HE_SO>" output.mp4
```
`<HE_SO>` > 1 = nhanh hơn, < 1 = chậm hơn. `atempo` chỉ nhận 0.5–2.0 mỗi lần — cần tốc độ ngoài khoảng đó thì chain nhiều `atempo` liên tiếp (vd `atempo=2.0,atempo=1.5` cho 3x).

Speed ramp mượt (tốc độ đổi dần theo thời gian, không đột ngột) cần biểu thức `setpts` theo hàm thời gian phức tạp hơn — hoặc đơn giản hơn là chia clip thành nhiều đoạn tốc độ khác nhau rồi nối bằng crossfade ngắn (xem [chuyen-canh.md](chuyen-canh.md)).

## Freeze frame (đóng băng 1 khung hình)

```bash
ffmpeg -i input.mp4 -vf "tpad=stop_mode=clone:stop_duration=2" output.mp4
```
Giữ khung hình cuối thêm 2 giây. Muốn freeze ở giữa clip (không phải cuối): cắt clip tại điểm đó thành 2 đoạn, chèn đoạn freeze ở giữa, nối lại bằng concat.

## Slow-motion mượt (không giật, khác atempo/setpts thô)

Nếu chỉ giảm tốc bằng `setpts=2*PTS` mà nguồn quay ở fps thấp (30fps), chuyển động sẽ giật. Dùng nội suy khung hình:
```bash
ffmpeg -i input.mp4 -vf "minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:vsbmc=1,setpts=2*PTS" output.mp4
```
Chậm hơn nhiều khi render (nội suy khung hình tốn CPU) — chỉ dùng khi thật sự cần mượt, còn lại `setpts` thô là đủ cho hầu hết nhu cầu.
