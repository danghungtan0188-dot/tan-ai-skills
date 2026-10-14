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

## Thấy trong mẫu nhưng chưa làm công thức

- **Intro tranh giấy nhiều lớp** (trăng, sóng, mây cắt giấy chuyển động lớp) cho lễ hội: làm bằng HyperFrames/Remotion, không làm bằng ffmpeg.
- **Chữ ký tên kênh giãn chữ** (chữ in hoa cách đều, mờ ở góc): `drawtext` không có giãn chữ. Chèn khoảng trắng giữa các ký tự trong file chữ.
- **Màu flycam điện ảnh** (trời ngả xanh lục, đất cam): gần với `Cinematic` trong [bo-loc-mau.md](bo-loc-mau.md).
