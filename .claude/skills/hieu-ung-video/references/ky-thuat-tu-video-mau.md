# Kỹ thuật rút từ video mẫu (10/2026)

Rút từ 9 video tham khảo tải về (bản tin xã, tổng kết chương trình, lễ hội Trung thu, lễ tri ân, flycam huyện, clip đường xá dạng dọc). Chỉ ghi những gì repo **chưa có**. Mọi công thức dưới đây đã render thử trên clip 1280×720 30fps, giải mã lại không lỗi, xem khung hình đúng như mô tả.

## Nhịp cắt đo được

| Loại video mẫu | Giây/cảnh trung bình | Ghi chú |
|---|---|---|
| Tổng kết chương trình (montage nhạc) | 2,3–3 | cắt theo nhịp, nhiều chuyển cảnh trang trí |
| Bản tin có MC | 6,5 | MC + cảnh minh họa, phụ đề song ngữ |
| Flycam giới thiệu địa phương | 15 | cảnh dài, lia chậm, chuyển qua đen giữa các phần |
| Lễ tri ân, lễ trang trọng | rất dài | nối bằng hòa tan chậm, gần như không cắt cứng |

**Bài học khi phân tích:** `select='gt(scene,0.30)'` **bỏ sót chuyển cảnh hòa tan**. Video lễ 460 giây chỉ đếm được 5 cảnh, dù nhìn khung hình thấy hòa tan liên tục. Video nhiều dissolve phải hạ ngưỡng xuống 0,1–0,15 hoặc nhìn tờ khung hình, đừng tin con số.

## 1. Mây/khói mở cảnh (organic reveal)

Cảnh sau "ăn" dần qua các mảng loang mềm như mây tan. Video mẫu dùng clip mây thật. Bản dưới đây không cần clip mây, mặt nạ loang tạo bằng tổng các sóng sin:

```bash
ffmpeg -i a.mp4 -i b.mp4 -filter_complex "[0][1]xfade=transition=custom:duration=1.5:offset=<GIAY>:expr='st(0, clip((1-P)*1.6-0.3 - (0.5+0.22*sin(X/41)*cos(Y/33)+0.18*sin((X+2*Y)/71)+0.1*cos((3*X-Y)/23)) + 0.5, 0, 1)); A*(1-ld(0)) + B*ld(0)'" out.mp4
```

- Trong `xfade` custom, `P` chạy **từ 1 về 0**: `1-P` mới là tiến độ.
- Bỏ phần `clip(...)` mềm, thay bằng `if(gt(...),B,A)` thì mép thành lốm đốm cứng, trông rẻ tiền. Đã thử, không dùng.
- Đổi các số chia (41, 33, 71, 23) để có hình loang khác.

## 2. Dải nét xoay trên nền mờ

Mở đầu cảnh bằng bản mờ của chính nó. Một dải nét xiên xuất hiện, vừa xoay vừa nở rộng tới khi phủ kín khung:

```bash
ffmpeg -i in.mp4 -filter_complex "[0]split[s][m];[m]boxblur=20:2[bl];[bl][s]blend=all_expr='if(lt(abs((X-W/2)*sin(0.5+T*0.6)-(Y-H/2)*cos(0.5+T*0.6)), W*0.8*min(T/1.5,1)), B, A)'" out.mp4
```

`0.5+T*0.6` là góc xoay, `W*0.8*min(T/1.5,1)` là nửa bề rộng dải (kín khung sau 1,5 giây). Muốn dùng giữa clip thì thay `T` bằng `(T-<GIAY_BAT_DAU>)`.

## 3. Chuyển cảnh `xfade` chưa có trong bảng chuyển cảnh

| Tên gọi | `transition=` | Dùng khi |
|---|---|---|
| Cửa mở ngang/dọc | `horzopen` / `vertopen` | mở màn, vào phần mới. Mẫu lễ hội dùng khung minh họa tách đôi lộ cảnh flycam |
| Cửa khép | `horzclose` / `vertclose` | kết phần |
| Qua xám | `fadegrays` | từ tư liệu trắng đen sang hiện tại, hoặc ngược lại |

Cú pháp giống các kiểu trong [chuyen-canh.md](chuyen-canh.md).

## 4. Gương và kính vạn hoa

Mẫu tổng kết dùng ở cảnh hồ bơi để tạo khung đối xứng. Dùng liều nhỏ, 1–2 giây:

```bash
# gương trên–dưới (nửa trên lật xuống dưới)
ffmpeg -i in.mp4 -vf "crop=iw:ih/2:0:0,split[t][u];[u]vflip[f];[t][f]vstack" out.mp4
# kính vạn hoa 4 góc
ffmpeg -i in.mp4 -vf "crop=iw/2:ih/2:0:0,split[a][b];[b]hflip[c];[a][c]hstack,split[d][e];[e]vflip[g];[d][g]vstack" out.mp4
```

Logo hoặc chữ trong khung cũng bị lật. Áp lên cảnh sạch, chưa chèn đồ họa.

## 5. Bloom: tỏa sáng vùng sáng

Hợp lễ trang trọng và cảnh đèn đêm. Vùng sáng tỏa mềm, vùng tối giữ nguyên:

```bash
ffmpeg -i in.mp4 -vf "format=gbrp,split[a][b];[b]curves=all='0/0 0.6/0 1/1',gblur=sigma=25[g];[a][g]blend=all_mode=screen:all_opacity=0.6,format=yuv420p" out.mp4
```

**Bắt buộc có `format=gbrp`** trước `blend=screen`. Lần thử đầu blend thẳng trên YUV, cả khung ám tím hồng.

## 6. Ảnh khung trắng nghiêng trên nền đen trắng mờ

Kiểu "ảnh rải bàn" của video tổng kết. Nền là chính cảnh đó bị khử màu và làm mờ. Ảnh màu có viền trắng nằm nghiêng ở giữa:

```bash
ffmpeg -i in.mp4 -filter_complex "[0]split[bg][fg];[bg]hue=s=0,boxblur=12:2[bgb];[fg]scale=iw*0.55:-2,pad=iw+24:ih+24:12:12:white,rotate=-5*PI/180:c=none:ow=rotw(-5*PI/180):oh=roth(-5*PI/180)[ph];[bgb][ph]overlay=(W-w)/2:(H-h)/2" -pix_fmt yuv420p out.mp4
```

Mẫu gốc còn có nhiều ảnh bay vào xếp chồng, rồi ảnh giữa phóng to thành toàn khung. Muốn chuyển động đó thì dựng qua HyperFrames (`hyperframes-animation`). ffmpeg thuần chỉ nên làm bản tĩnh như trên.

## 7. Khung dọc 9:16 chứa video ngang + chữ phía trên

Dạng clip giới thiệu đường xá trên TikTok: nền đen, video 16:9 ở giữa, chữ địa danh trắng đặt ngay trên video:

```bash
ffmpeg -i in.mp4 -vf "scale=1080:-2,pad=1080:1920:0:(oh-ih)/2:black,drawtext=fontfile='C\:/Windows/Fonts/segoeuib.ttf':textfile=chu.txt:fontsize=46:fontcolor=white:line_spacing=10:x=(w-tw)/2:y=(h-1080*9/16)/2-th-40" out.mp4
```

`chu.txt` lưu UTF-8. Mỗi dòng là một dòng chữ.

## 8. Hai dải chồng trên–dưới

Mỗi dải là một cảnh, có khe đen ở giữa. Video tổng kết dùng ngay đầu phim để vừa mở màn vừa cho thấy hai hoạt động cùng lúc:

```bash
ffmpeg -i a.mp4 -i b.mp4 -filter_complex "[0]crop=iw:ih*0.46:0:ih*0.27[t];[1]crop=iw:ih*0.46:0:ih*0.27[u];[t][u]vstack,pad=iw:ih/0.92:0:(oh-ih)/2:black,scale=1920:1080" out.mp4
```

## 9. Lưới 3×2 cùng một cảnh

Nhân một cảnh thành 6 ô trên nền đen. Dùng như nhịp nhấn, khoảng 1 giây, rồi cắt về toàn khung:

```bash
ffmpeg -i in.mp4 -filter_complex "[0]scale=iw/3-8:-2,pad=iw+8:ih+8:4:4:black,split=6[a][b][c][d][e][f];[a][b][c][d][e][f]xstack=inputs=6:layout=0_0|w0_0|w0+w1_0|0_h0|w0_h0|w0+w1_h0,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black" out.mp4
```

## 10. Chữ lồng video (video chạy bên trong chữ)

Video tổng kết dùng cho con số năm, video lễ dùng cho tên địa phương. Chữ trắng trên nền đen làm mặt nạ alpha:

```bash
ffmpeg -i in.mp4 -f lavfi -i "color=black:s=1920x1080:d=<GIAY>" -filter_complex "[1]drawtext=fontfile='C\:/Windows/Fonts/arialbd.ttf':text='2026':fontsize=560:fontcolor=white:x=(w-tw)/2:y=(h-th)/2,format=gray[m];[0]format=yuva420p[v];[v][m]alphamerge[k];[1][k]overlay" -pix_fmt yuv420p out.mp4
```

Chữ càng đậm, càng to thì càng thấy rõ hình bên trong. Dùng font đậm (`arialbd.ttf`). Video lễ còn phóng to chữ cho tới khi máy "chui" qua một chữ cái vào cảnh. Hiệu ứng đó dựng bằng Remotion.

## 11. Mẫu chuyển động trong `do-hoa/` (Remotion)

Hai mẫu dựng từ cách làm của video lễ hội và video tổng kết. Hình vẽ là SVG tự dựng, không lấy ảnh của video mẫu.

| Mẫu | Làm gì | Xuất |
|---|---|---|
| `TranhGiay` | Intro tranh giấy nhiều lớp: trời hoàng hôn, trăng lên, núi – mây – 3 lớp sóng đổ bóng như giấy cắt, máy đẩy tới. Chữ vàng viền tối hiện từ mờ sang nét, đốm sáng lấp lánh. Cuối clip tranh tách đôi như cửa mở để lộ video bên dưới | `.mov` ProRes 4444 nền trong suốt |
| `AnhBayVao` | Nền là ảnh chính khử màu và làm mờ. Từng ảnh viền trắng bay vào từ một hướng, nghiêng nhẹ, xếp chồng. Ảnh cuối danh sách đáp giữa rồi phóng to phủ kín, nền trở lại màu, tiêu đề hiện ở dưới | `.mp4` toàn khung |

Lệnh render, chạy trong `do-hoa/`:

```bash
npx remotion render src/index.ts TranhGiay out.mov --props=tranh.json --concurrency=2
npx remotion render src/index.ts AnhBayVao out.mp4 --props=anh.json --public-dir=<thu_muc_anh> --concurrency=2
```

```json
{"tiLe":"16:9","thoiLuong":6,"dongTren":"Ủy ban nhân dân","dongChinh":"Xã An Thạnh Thủy","dongDuoi":"Đêm hội trăng rằm 2026","moCua":true}
{"tiLe":"16:9","thoiLuong":7,"anh":["anh1.jpg","anh2.jpg","anh3.jpg","anh4.jpg","anh5.jpg"],"cachNhau":0.45,"tieuDe":"Chương trình phòng, chống đuối nước 2026"}
```

- `anh` nhận từ 2 đến 8 ảnh. **Ảnh cuối là ảnh chính**, được phóng to toàn khung.
- Ảnh chính nên là ảnh không có viền đen. Ảnh cắt từ video bị viền đen hai bên thì viền đó cũng phóng to theo.
- `moCua: false` thì tranh giữ tới hết clip, không tách đôi.
- Muốn xem nhanh một khung trước khi render cả clip: `npx remotion still src/index.ts TranhGiay hinh.png --props=tranh.json --frame=105`.

## Thấy trong mẫu, ghi lại để dựng sau

Xem dày 3 khung/giây ở đầu, giữa, cuối cả 4 video. Những kỹ thuật này chưa có công thức. Phần lớn nên dựng bằng Remotion:

- **Số năm lăn như đồng hồ đo:** "2025" thành "2026", chữ số cuối trượt lên, số mới từ trên rơi xuống.
- **Tiêu đề kết có bóng phản chiếu:** các chữ cái hiện ngẫu nhiên từng chữ, bóng ngược mờ bên dưới, nền tia sáng hội tụ.
- **Nhãn góc gõ ngẫu nhiên:** tên đơn vị ở góc hiện ra từng chữ cái theo thứ tự lộn xộn.
- **Trái tim vẽ bằng vệt hạt vàng** làm cảnh kết.
- **Ảnh bay tràn khung nhiều ảnh nhỏ** như một bức tường ảnh chuyển động trên nền đen.
- **Cửa sổ nhỏ nở ra toàn khung**, có bo góc tròn.
- **Mặt nạ cong như đồng hồ cát** đóng vào khung.
- **Vỡ khối pixel** khi chuyển cảnh.
- **Xoáy (swirl)** ở cảnh flycam kết.
- **Khung tranh minh họa tách thành 3 dải dọc** để lộ cảnh flycam.
- **Tên địa điểm 2 dòng:** dòng trên vàng, dòng dưới đỏ, cả hai có viền.
- **Chữ ký tên kênh giãn chữ** (chữ in hoa cách đều, mờ ở góc): `drawtext` không có giãn chữ. Chèn khoảng trắng giữa các ký tự trong file chữ.
- **Màu flycam điện ảnh** (trời ngả xanh lục, đất cam): gần với `Cinematic` trong [bo-loc-mau.md](bo-loc-mau.md).
- **Hiệu ứng đã có trong repo:** vệt sáng (`light_leak`), làm mờ khi phóng (`zoom_blur`), lóe trắng (`flash_white`), tách màu RGB (`glitch_rgb`). Xem `references/effect-catalog.md` của skill `chuyen-gia-edit-video-tan`.
