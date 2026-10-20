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

## 12. Vòng tròn khép về đen (iris) có viền sáng

Kết clip dọc kiểu TikTok: khung co thành vòng tròn quanh người nói rồi khép hẳn. Ví dụ dưới bắt đầu ở giây 1, khép trong 1,6 giây:

```bash
ffmpeg -i in.mp4 -vf "format=yuv420p,geq=lum='st(0,hypot(X-W/2,Y-H/2)/hypot(W/2,H/2));st(1,max(0,1-max(0,T-1)/1.6));if(lt(ld(0),ld(1)-0.03),lum(X,Y),if(lt(ld(0),ld(1)),lum(X,Y)*0.6+60,16))':cb='if(lt(hypot(X-W/2,Y-H/2)/hypot(W/2,H/2),max(0,1-max(0,T-1)/1.6)),cb(X,Y),128)':cr='if(lt(hypot(X-W/2,Y-H/2)/hypot(W/2,H/2),max(0,1-max(0,T-1)/1.6)),cr(X,Y),128)'" out.mp4
```

`geq` chạy chậm, chỉ áp cho 2–3 giây cuối. Đã thử: vòng co đúng, viền sáng rõ.

## Clip dọc nói/hát trước máy (video thứ 10)

Đã có trong repo, không ghi lại: phụ đề nhấn từng từ (`karaoke_word`), mũi tên, vòng tròn và khung chỉ chỗ bấm trên màn hình app (`callouts.py`).

Chưa làm công thức:
- Ảnh vật thật (thẻ, điện thoại) bật ra cạnh tay, có vòng sáng quanh.
- Phóng sát mặt đột ngột theo nhịp nhạc.
- Sticker phản ứng góc khung.
- Nút "Follow" có con trỏ bấm ở cuối clip.
- Vệt bóng khi tay chuyển động nhanh. Đã thử `lagfun`, nhưng trên cảnh ít chuyển động thì chưa thấy rõ, nên chưa ghi thành công thức.

## Video giải đáp chính sách dạng đồ họa (2 video BHXH, 10/2026)

Nhịp chậm: 17–22 giây một cảnh, mỗi cảnh là một ý của văn bản. Hợp với tin giải đáp thủ tục của xã/phường. Cấu trúc chung:

1. **Intro logo:** vệt sáng quét qua, chữ tiêu đề bật vào, có bóng phản chiếu dưới sàn. Dùng mẫu `Intro` trong `do-hoa/`, hoặc `titlecard-lockup` + `light-sweep-pass` của HyperFrames ([hoc-tu-hyperframes.md](hoc-tu-hyperframes.md)).
2. **Thẻ câu hỏi:** câu hỏi đặt giữa nền sáng có đốm bokeh, cụm từ khóa tô **cam**.
3. **MC ảo trong trường quay** (video ghi "có sử dụng AI"), có màn hình bên phải chiếu hình minh họa. MC AI thuộc skill `heygen-video` (trả phí, phải hỏi trước).
4. **Trang minh họa:**
   - Mẫu 1: nền trắng, hình minh họa phẳng bên trái, chữ căn giữa bên phải, cụm quan trọng tô cam hoặc đỏ.
   - Mẫu 2: hộp chữ bo góc, chữ **gõ dần từng ký tự** (preset `typewriter` đã có) trên nền tranh minh họa, tiêu đề chủ đề cố định ở khung trên.
5. **Thanh nhận diện cố định** góc dưới phải suốt video; logo đơn vị góc trên trái.

**Bài học:** nội dung là văn bản pháp lý nên chữ phải ở yên đủ lâu để đọc. Họ giữ mỗi trang chữ 8–15 giây, chữ gõ xong thì đứng yên. Số tiền, số ngày phải viết đúng như văn bản.

## Promo đài truyền hình nhịp nhanh (reel THĐT, 49 giây, 10/2026)

Nhịp rất nhanh: 46 cảnh trong 49 giây, trung bình **1,1 giây một cảnh**. Giọng đọc nam phát thanh viên, âm lượng tổng −14,3 LUFS, LRA 5,2 LU. Mức này hợp với mạng xã hội; bản phát sóng truyền hình vẫn để −23 LUFS. Cấu trúc 4 đoạn:

1. **Montage nghề làm báo (0–12 giây):** cảnh hậu trường cắt 1 cảnh/giây. Giữa các cảnh có:
   - lóe sáng tách màu cầu vồng: preset `light_leak` + `glitch_rgb` đã có
   - chia khung 2–3 ô dọc lệch nhau
   - nhãn chữ thập nhỏ màu cam nhấp nháy
2. **Vòng HUD đếm số:** vòng tròn kiểu ống kính, có vạch chia, số đếm tăng ở giữa, đè lên từng cảnh. Vòng này thu lại thành logo đài. HyperFrames có sẵn: luật `counting-dynamic-scale` + `camcorder-hud`/`sdf-iris`.
3. **Câu hỏi bật theo lời đọc:** "Bạn cần gì?", "Bạn yêu thích điều gì?"… Chữ đỏ in hoa trong ô trắng, trồi lên 0,25 giây đúng lúc phát thanh viên đọc. Viền vàng mờ ở mép trên và dưới khung.
4. **Kêu gọi hành động:** gia đình xem TV, máy đẩy vào màn hình có mã QR khảo sát. Tay cầm điện thoại quét mã, màn hình điện thoại chiếu phiếu khảo sát. Kết bằng 2 mã QR và 2 logo trên nền tia sáng xanh.

Công thức ô câu hỏi (đã thử):

```bash
ffmpeg -i in.mp4 -vf "drawtext=fontfile='C\:/Windows/Fonts/arialbd.ttf':textfile=hoi.txt:fontsize=56:fontcolor=0xD7141A:box=1:boxcolor=white:boxborderw=22:x=(w-tw)/2:y=h*0.42+18*max(0\,1-t/0.25):alpha='min(1,t/0.25)'" out.mp4
```

Muốn hiện ở giây khác thì thay `t` bằng `(t-<GIAY>)` và thêm `enable='between(t,<GIAY>,<HET>)'`.

## Reel "AI dựng cả video": người nói + đồ họa thay nhau (85 giây, dọc, 10/2026)

Video tiếng Anh, một người nói trước máy kể việc giao cho AI dựng video. Nhịp chậm (14 giây một cảnh), nhưng **đồ họa đổi liên tục trong từng cảnh**. Âm lượng −14,2 LUFS, LRA chỉ 1,9 LU: nén rất mạnh cho điện thoại, không dùng cho bản tin.

**Bố cục khung dọc:** nền đen. Dòng tiêu đề cố định phía trên, dòng kêu gọi bình luận cố định phía dưới. Nội dung 16:9 nằm giữa. Gần với mục 7 ở trên, thêm dòng chữ cố định dưới đáy.

**Cách dựng đáng học:**
1. **Người nói ↔ khung tròn góc.** Khi đồ họa chiếm khung, người nói thu thành vòng tròn nhỏ viền trắng ở góc dưới phải, vẫn nói tiếp. Hết đồ họa thì phóng lại toàn khung. Người xem không mất mặt người nói.
2. **Phụ đề từng từ có một từ nhấn đổi kiểu chữ:** chữ đậm không chân trắng, riêng từ khóa đổi sang **chữ nghiêng có chân màu đỏ cam** ("entire", "everything", "copy", "touched"). Kiểu chữ nhấn này lặp lại ở mọi tiêu đề đồ họa ("one *habit*", "five *months*", "saved *instructions*"), thành nhận diện riêng của kênh. Áp cho mình: chữ đậm trắng + từ khóa nghiêng màu vàng ATT.
3. **Thẻ bay ra từ sau lưng người nói:** người nói nhắc tới "thẻ", "chú thích" thì thẻ nhỏ bay ra hai bên. Cần tách người khỏi nền (HyperFrames `media-use` có tách nền) hoặc chỉ đặt thẻ ở vùng trống.
4. **Đồ họa minh họa đúng lời:** nói "5 tháng" thì hiện dòng thời gian có ảnh; nói "hai điều thay đổi" thì hiện 2 thẻ số "1", "2" rồi mỗi thẻ lật thành ảnh; nói "chi phí" thì một máy in nhả **hóa đơn** liệt kê từng việc; nói "skill" thì xấp giấy hướng dẫn rơi vào một chiếc hộp có nhãn.
5. **Cảnh đổi bằng mặt nạ:** vòng tròn hoặc góc trắng lấn vào khung; tiêu đề chữ lớn trên nền đỏ có đường viền bo tròn tự vẽ quanh chữ.

**Bài học về cách làm, không phải hiệu ứng:** tác giả nói AI dựng đẹp lên khi **giao từng việc một** (nghiên cứu → cắt → lên kế hoạch đồ họa → dựng đồ họa → kiểm từng khung → lưu điều đã sửa) và **lưu điều đã sửa vào skill** để lần sau tốt hơn. Repo này đã làm đúng như vậy: chuỗi agent `video-analyzer → video-editor → video-reviewer` và lệnh `/rut-kinh-nghiem` sau mỗi video.

Công thức khung tròn góc (đã thử, 200 px, viền trắng 6 px):

```bash
ffmpeg -i nen.mp4 -i nguoi_noi.mp4 -filter_complex "[1]crop=ih:ih,scale=200:200,format=yuva420p,geq=lum='lum(X,Y)':cb='cb(X,Y)':cr='cr(X,Y)':a='if(lt(hypot(X-100,Y-100),97),255,0)'[pip];color=white:s=212x212,format=yuva420p,geq=lum=235:cb=128:cr=128:a='if(lt(hypot(X-106,Y-106),105),255,0)'[vien];[0][vien]overlay=W-w-34:H-h-34:shortest=1[t];[t][pip]overlay=W-w-40:H-h-40:shortest=1" -pix_fmt yuv420p out.mp4
```

`crop=ih:ih` cắt giữa khung; mặt người nói lệch tâm thì thêm `x` vào `crop`. Muốn người nói **thu/phóng mượt** giữa toàn khung và vòng tròn thì dùng mẫu Remotion `NguoiNoiPip` (đã render thử):

```bash
npx remotion render src/index.ts NguoiNoiPip out.mp4 --props=pip.json --public-dir=<thu_muc_file> --concurrency=2
```

```json
{"tiLe":"16:9","thoiLuong":8,"video":"nguoi_noi.mp4","doHoa":[{"tu":1.5,"den":4,"file":"anh2.jpg"},{"tu":4,"den":6.5,"file":"bieu_do.mp4"}],"coTron":220}
```

- Video người nói chạy suốt, giữ nguyên tiếng. Mỗi đoạn `doHoa` phủ ảnh hoặc video toàn khung; người nói thu thành vòng tròn trong 0,45 giây rồi phóng lại.
- Hai đoạn đồ họa cách nhau dưới 0,9 giây được gộp: người nói **ở yên trong vòng tròn** qua chỗ nối. Bản đầu chưa gộp nên người nói bật ra rồi thu lại ngay, trông giật (đã sửa, đã kiểm khung ở chỗ nối).
- `thoiLuong` đặt bằng độ dài video người nói.

## Reel kể chuyện nghề có giọng AI "Adam" (2 phút 44 giây, 10/2026)

Không có người trên hình; giọng AI nam miền Bắc kể chuyện đời thường, câu mở đầu gây tò mò. Cảnh dài (23 giây một cảnh), nhưng chữ và nhãn đổi liên tục theo lời. Bố cục cố định đáng học cho video **giải thích bằng màn hình/tài liệu**:

- **Nền tối có lưới mờ**, đốm sáng vàng nhẹ ở góc trái.
- **Bên trái:** hình minh họa (bản vẽ, ảnh chụp màn hình). **Bên phải:** phụ đề lớn 2–3 dòng, chữ đang đọc tô **vàng**, chữ chưa đọc màu trắng.
- **Nhãn vàng nhỏ cố định góc trên phải** nhắc chủ đề cả video ("Nhận làm website, nhận luôn file CAD"). Góc trên trái có tiêu đề đoạn chữ in hoa, có một từ nền vàng.
- **Danh sách đánh số hiện dần** theo lời ("01 LOGO", "02 WEBSITE"…).
- **Chú thích hỏi chấm trên ảnh:** nói "nét nào là tường?" thì nhãn đen "TƯỜNG?" bật lên đúng chỗ, kèm **vòng tròn vàng** khoanh vùng rối. Cách này khiến người xem nhìn đúng chỗ đang nói.
- **Quay màn hình** có nhãn nhỏ góc dưới trái ghi đang xem gì ("Mở bộ file CAD gốc").

Đã có sẵn: phụ đề tô từng từ (`karaoke_word`), vòng khoanh và nhãn (`callouts.py`), danh sách hiện dần (HyperFrames `kinetic-type-beats`). Giọng đã lưu thành **"Adam - video AutoCAD"** (xem kho giọng của skill `tan-giong-doc-ban-tin`).

## Bản đồ hành trình "Follow the red line" (KOYO 2026, 2 phút 5 giây, 10/2026)

Video bài hát về mùa lá đỏ Nhật: một **đường đỏ** đi từ bắc xuống nam qua 8 điểm ngắm lá. Đo được: không có cú cắt nào (`scdet` ngưỡng 12 bắt 0 lần), toàn bộ là **một máy quay ảo bay liên tục** trên bản đồ. Khoảng 10 giây một điểm, xen 2 đoạn điệp khúc "momiji" và 2 lần lùi ra toàn cảnh. Âm lượng mean −16,8 dB, đỉnh −1 dB.

**Nhận diện hình ảnh (đáng học nhất):**
- **Ba màu:** nền xanh rêu đậm, nét trắng ngà mảnh, nhấn **cam đỏ** (đường đi, khung ảnh, chữ "NEXT"). Không có màu thứ tư. Ảnh thật là chỗ duy nhất có màu tự nhiên.
- **Khung HUD cố định:** dòng trên gồm tên dự án · "FOLLOW THE RED LINE — vùng · điểm" bên trái và tọa độ `40.591°N 140.978°E` bên phải, gạch mảnh ngăn dưới. Dòng dưới ghi thông số khối địa hình và **nguồn dữ liệu** ("Boundaries: Natural Earth (public domain) · Elevation: AWS Terrain Tiles"). Toàn bộ bằng chữ đơn cách in hoa, giãn chữ.
- **Ô chặng (trên trái):** "NEXT · STOP 02 / 08 · vùng", tên điểm, rồi **ngày cực to** (10/13) cạnh tên tỉnh, dòng nguồn dự báo nhỏ. Ở cảnh toàn thì ô này đổi thành **bảng 8 điểm + ngày**: điểm đã qua tô cam, điểm kế ghi nhãn "NEXT".
- **Phụ đề hai thứ tiếng** giữa dưới: tiếng Anh trên, chữ đang hát sáng trắng, phần chưa hát xám; tiếng Nhật nhỏ hơn bên dưới. Điệp khúc thì chữ to lệch phải.

**Chuyển động:**
1. **Đường đỏ tự vẽ** theo lộ trình, **đầu bút là đốm sáng lóe** có tia lửa nhỏ. Đoạn sắp đi tới vẽ **nét đứt trắng**, đi qua rồi mới thành nét đỏ liền.
2. **Máy quay nghiêng 3D** (pitch khoảng 45–60°) bám theo đầu bút, ranh giới tỉnh nổi khối mỏng có bóng.
3. Tới điểm: hoặc **ảnh thật trong khung viền cam** có **đường kẻ gãy khúc nối về đúng điểm** trên bản đồ (kèm dòng ghi nguồn ảnh Wikimedia), hoặc **khối địa hình cắt vuông** vẽ bằng đường đồng mức, có nhãn "TÊN · RELIEF 100–1442 M · tọa độ" nối bằng đường kẻ.
4. **Điệp khúc:** chữ viết tay "momiji" **tự vẽ nét** màu cam, kèm cây lá vẽ bằng nét đồng mức xếp tầng.
5. **Lùi ra toàn cảnh** hai lần (giữa bài và cuối): cả nước, đủ 8 điểm và đường đỏ nối liền, câu kết "One line, all the way down".

**Xem dày 1,5 giây/khung cả video — cấu trúc thật (học kỹ):**

*Khung chuyện:* mở bằng toàn cảnh nước Nhật có 8 điểm, **tiêu đề chữ Nhật lớn "紅葉前線" (hai chữ trắng, hai chữ cam) + dòng phụ "KOYO ZENSEN · FOLLOW THE RED LINE"**; kết lại đúng khung đó ("See you in the red") — **mở và kết là một khung** (bookend). Giữa bài và cuối bài có 2 lần lùi ra toàn cảnh, bảng danh sách tích dần từng điểm, các điểm đã qua sáng lên.

*Mỗi điểm (khoảng 10 giây) lặp cùng 6 nhịp:*
1. **Bay theo đường đỏ** tới điểm: máy nghiêng, nét đứt trắng phía trước, đầu bút lóe.
2. **Mặt phẳng hóa địa hình:** một ô chữ nhật phẳng nhỏ ở điểm đến **nở ra và trồi lên** thành khối/vùng địa hình vẽ bằng đường đồng mức trắng mảnh.
3. **Đường đỏ chạy trên địa hình** theo đúng lộ trình (đèo, thung lũng), có vệt sáng và tia lửa.
4. **Biểu tượng riêng của nơi đó, dựng bằng cùng bộ nét + hạt cam** — đây là chỗ hay nhất:
   - núi lá vàng → **cây hình nón xoắn bằng chấm cam**;
   - hẻm suối → **thác bằng hàng trăm nét dọc cam**;
   - đèo 48 khúc cua → **dải đường zíc zắc leo dốc + số đếm "08 → 48"**;
   - hàng cây ngân hạnh 300 m → **vòm chấm vàng + thước đo "300 M"**;
   - núi soi bóng sông → **cây chấm cam và bóng ngược của nó**;
   - cổng torii → **khung dây cổng torii** vẽ nét;
   - cầu treo → **đường kích thước kiểu bản vẽ "390 M" (dài) rồi "173 M" (cao)**.
5. **Hạt lá bay tụ vào khung → thành ảnh thật** viền cam, đường kẻ nối về điểm; phụ đề đổi câu.
6. **Ảnh thu lại thành một dải mỏng rồi trượt đi**, đường đỏ đi tiếp sang điểm sau. **Không có cú cắt nào** — mọi thứ mọc ra từ đường và quay về đường.

*Điệp khúc:* chữ viết tay "momiji" tự vẽ nét cam + cây lá dựng bằng đường đồng mức xếp tầng; chữ lớn lệch phải.

*Nhịp với nhạc:* mỗi điểm đổi đúng đầu câu hát; số đếm, thước đo bật đúng chữ được hát ("three hundred ninety metres").

*Nhiều khả năng dựng bằng:* trình duyệt + WebGL (three.js hoặc deck.gl) với địa hình AWS Terrain Tiles và ranh giới Natural Earth, render từng khung rồi mã hóa bằng ffmpeg (metadata `Lavf62 / libx264` — không phải phần mềm dựng tay). HyperFrames có sẵn bộ chuyển Three.js nên dựng được kiểu này; nhưng WebGL 3D **rất nặng** cho máy hay sập nguồn.

**Bài học lớn rút ra (áp cho mọi video bản đồ/giải thích):**
- **Một bộ từ vựng hình ảnh** (nét mảnh + hạt một màu nhấn) dùng xuyên suốt, nhưng **mỗi điểm có một ẩn dụ riêng** dựng từ chính bộ từ vựng đó → vừa đồng bộ vừa không nhàm.
- **Số liệu thành hình:** thay vì chỉ ghi "390 m", vẽ đường kích thước kiểu bản vẽ kỹ thuật ngay trên vật thể.
- **Ảnh thật là phần thưởng**, xuất hiện sau phần đồ họa và mọc ra từ hạt/đường — không chèn ảnh trơ.
- **Mở = kết**, và có 1–2 lần lùi ra toàn cảnh để người xem nắm tiến độ.

**Phiên bản nhẹ máy cho mình (chưa dựng):** địa hình miền Tây phẳng nên bỏ khối 3D; "trồi lên" thay bằng **ảnh vệ tinh mở ra từ ô chữ nhật** (mẫu `BanDoVeTinh` đã có ảnh nền + phóng). Ẩn dụ từng điểm làm bằng SVG trong Remotion, ví dụ: ruộng lúa → lưới ô vuông chấm vàng mọc dần; kênh → các nét chảy song song; cầu → đường kích thước "dài … m"; chợ nổi → chấm ghe tụ lại; trường/trạm y tế → khung dây nhà. Hạt bay tụ thành ảnh: lấy mẫu màu ảnh thành lưới chấm, chấm bay từ đường vào đúng ô rồi hòa sang ảnh.

**Áp vào video của mình:**
- Bản đồ một tỉnh/xã: ranh giới lấy từ OpenStreetMap hoặc GADM, **kiểm lại sau sáp nhập 2025**; có bản đồ chính thức của xã thì dò theo bản đó (như mẫu `BanDoXa`). Bay máy quay bằng MapLibre (skill `remotion-maps`, miễn phí) hoặc vẽ vector trong Remotion rồi nghiêng bằng CSS `perspective`.
- **Bỏ khối địa hình 3D** với vùng đồng bằng: miền Tây phẳng nên khối trơ, lại phải dựng three.js nặng máy (máy hay sập nguồn khi chạy nặng). Thay bằng ảnh/clip quay thật trong khung viền + đường kẻ nối.
- Màu cho ATT NEWS: nền navy + nét trắng + nhấn vàng ATT, giữ đúng luật ba màu.
- Ghép sẵn với thứ đã có: khung ảnh 3D (`PhuNu96`), viền chạy quanh ranh giới (`BanDoXa`), đầu bút lóe tia lửa (`KetLaser`), phụ đề song ngữ (skill `bien-tap-video-thong-minh-song-ngu-tan`).
- Dữ liệu điểm nên để trong một file JSON (tên, tọa độ, ngày, ảnh, câu thuyết minh) để mẫu tự dựng; ghi nguồn bản đồ và ảnh ở dòng dưới như video mẫu.

## Reel dọc "Góc nhìn quy hoạch — Sông Đáy" (3 phút 10 giây, 9:16, 10/2026)

Người nói giải thích dự án cải tạo sông bằng **bản đồ vệ tinh động** do AI dựng (Claude + một skill bản đồ, giọng đọc từ minimax.audio). Đo được: cả video chỉ **1 cú cắt** (giây 33, từ đoạn khoe "cách làm" sang bản đồ), còn lại một khung bản đồ chạy liên tục, đồ họa đổi theo lời. Âm lượng −14,1 LUFS, LRA 2,3 LU: nén mạnh kiểu mạng xã hội.

**Bố cục khung dọc (đáng học):**
- Nền đen có **lưới ô vuông trắng mờ**, nửa dưới hắt **ánh vàng** từ dưới lên.
- **Thẻ bản đồ dọc bo góc, viền xanh ngọc dày** chiếm giữa khung. Người nói đứng nhỏ, tách nền, ở **góc dưới trái**, đè lên mép thẻ.
- Trong thẻ, giữ cố định:
  - **trên trái:** dòng nhỏ giãn chữ "GÓC NHÌN QUY HOẠCH", tên lớn "SÔNG ĐÁY", dòng phụ "Dự án cải tạo · Hà Nội";
  - **trên phải:** mũi tên chỉ Bắc và **bản đồ nhỏ định vị** (ô vàng khoanh đoạn đang xem);
  - **trái dưới:** thước tỷ lệ "2 km";
  - **dưới:** dòng nhỏ giãn chữ "THỨ HAI" rồi **tiêu đề lớn phát sáng** ("CẢI TẠO SÔNG ĐÁY", "BẰNG QUỸ ĐẤT"); **phụ đề từng cụm từ**, chữ trắng, từ khóa vàng;
  - **đáy:** 2 dòng nguồn ("Ảnh vệ tinh: Esri, Maxar · Sông, cầu, ranh giới xã/phường: © OpenStreetMap · Số liệu: hồ sơ đề xuất… chưa phải quy hoạch duyệt") và **thanh tiến độ mảnh** chạy theo thời lượng.

**Đồ họa trên bản đồ:**
1. **Dòng sông phát sáng xanh ngọc** (nét dày có quầng), **mũi tên trắng nhỏ chạy dọc theo dòng** chỉ hướng nước chảy.
2. **Nhãn địa danh** chữ in hoa nhỏ (xã, cầu); cầu có chấm vàng. Đường giao thông là nét vàng mảnh.
3. **Ô thông tin đáy kính tối viền xanh**: danh sách gạch đầu dòng số liệu ("Nạo vét…", "Đào mới tổng ~13,9 km"); **bảng bật/tắt lớp** có ô tích (Tuyến sông · Tuyến đường · Quy hoạch liên quan) và lớp tương ứng hiện lên theo ô được tích.
4. **Sơ đồ hai bên** (Nhà đầu tư ⇄ Nhà nước) với mũi tên phát sáng hai màu ngược chiều; lúc này **bản đồ tối đi** để sơ đồ nổi lên.
5. **So sánh diện tích bằng hai ô vuông** đúng tỷ lệ (200 ha so với 25 ha) và **vùng quy hoạch viền vàng** khoanh trên ảnh vệ tinh.
6. Máy quay **trượt/phóng dần** theo dòng sông tới đoạn đang nói.

**Phần "cách làm" (0–33 giây) và kêu gọi:** ô đỏ cam "CÁCH LÀM" cùng danh sách tích xanh hiện dần ("Chuẩn bị file audio", "Kéo vào Claude", "Gọi skill bản đồ", "Nhấn Enter"), đè trên quay màn hình. Sau đó là ô "AI TỰ LÀM HẾT / 100% DO AI" và cuối cùng ô "BÌNH LUẬN: SKILL" để xin tương tác. Danh sách ô tích hiện dần **chưa có mẫu sẵn**; gần nhất là `TieuChi` (thẻ sáng lần lượt theo lời đọc, không có dấu tích).

**Họ làm thế nào (nghe lời người nói + đọc màn hình Claude trong video):**
1. **Có file giọng đọc trước** (`Audio.mp3`): tự đọc hoặc tạo bằng minimax.audio. Giọng đọc là kịch bản; mọi thứ khác bám theo giọng.
2. **Kéo file vào Claude desktop (tab Code)**, dự án tên `SON_AI_VIDEO`, rồi **gọi skill bản đồ riêng của họ** ("skill bản đồ hạ tầng") và nhấn Enter. Skill này không công khai (cuối video xin "BÌNH LUẬN: SKILL").
3. Khoảng **20 phút** máy trả về `SongDay_BanDo_v4.mp4` (117 giây, 1080×1920, 3.521 khung, có tiếng động SFX, chưa có nhạc). Skill **tự tìm ranh giới/sông/cầu từ OpenStreetMap và tự lấy ảnh vệ tinh Esri/Maxar** theo địa danh trong lời đọc.
4. Tên file là **v4** và Claude ghi "nội dung, cảnh và số liệu giữ nguyên như anh đã duyệt": thực tế là **có duyệt nội dung và sửa qua 3 lượt**, không phải một Enter là xong như lời quảng cáo.

**Skill của họ tự kiểm 5 mục trên file cuối (nên học nguyên):**

| Mục | Ngưỡng họ dùng |
|---|---|
| Đủ khung | 3.521 khung = thời lượng × 30 |
| Độ to | −14,0 LUFS, đỉnh −1,7 dBFS |
| Tọa độ khớp ảnh vệ tinh | so 12 khung, lệch nhiều nhất 0,22 px |
| Không khung nhảy | 0 khung giật |
| Máy quay êm | lia tối đa 12,8 px/khung, zoom tối đa 6,6 %/khung |

**Lỗi họ sửa từ v3 sang v4 (lỗi điển hình của video bản đồ, phải có bước kiểm riêng):** nhãn đè nhãn ("BỜ HỮU" đè "SÔNG BÙI"); tên xã mờ lộ xuyên qua ô thông tin; hai nhãn "SÔNG ĐÁY" cùng lúc; nhãn thò ra dưới ghim ("CẦU 72 II"); nhãn bị mép thẻ cắt ("CẦU MAI LĨNH").

**Toàn bộ đồ họa đã thấy (xem 3 giây/khung từ giây 46 tới hết):**
- Mở: ảnh vệ tinh toàn vùng, sông vẽ dần từ **ghim "ĐẬP ĐÁY"** xuôi xuống, nhãn cầu chấm vàng hiện lần lượt dọc sông.
- Sông đoạn đang nói phát sáng xanh ngọc đậm, đoạn khác mờ; **nét đứt trắng** chạy giữa lòng sông = phương án nắn dòng; nhãn số đo bên bờ ("BỜ HỮU ~17,6 KM", "BỜ TẢ ~16,2 KM").
- Nhãn trạng thái dạng viên thuốc ("● PHƯƠNG ÁN ĐANG NGHIÊN CỨU", "HỒ SƠ ĐỀ XUẤT ĐANG LẤY Ý KIẾN"); ô cảnh báo tam giác vàng "Chưa phải quy hoạch cuối cùng".
- Phóng sát tới cầu (ảnh vệ tinh rõ nhà cửa), **thước đo bề rộng đường** "~40 M TRÊN BẢN ĐỒ", ô "QUY MÔ: mặt đường ~20 m · 4 làn xe · nền đường ~33–35 m" có hình mặt cắt làn xe.
- **Số lớn đếm lên** "6.000+ HỘ DỰ KIẾN" (dòng phụ "~24.000 người · toàn tuyến · theo hồ sơ").
- **Biểu tượng người + dấu hỏi** mọc lên trên khu dân cư; ô đỏ có hình sổ đỏ "Có sổ đỏ chưa chắc là ĐẤT AN TOÀN".
- Bảng **đối chiếu lớp** có ô tích (Tuyến sông, Tuyến đường, Quy hoạch liên quan) — tích tới đâu lớp đó hiện tới đó.
- **Vùng quỹ đất viền vàng nhấp nháy** quanh phường, ô so sánh 200 ha / 25 ha bằng hai ô vuông đúng tỷ lệ.
- Sơ đồ "Nhà đầu tư ⇄ Nhà nước" (bản đồ tối đi), ô tổng hợp số liệu dự án có dấu chấm đầu dòng.
- Tuyến đường mới **vẽ dần nét vàng phát sáng** cắt qua ảnh vệ tinh; mũi tên trắng nhỏ chạy theo dòng nước.
- Ô "CHỈ CẦN NHỚ 3 THỨ" có 3 ô tích; cuối là 3 câu hỏi dạng viên thuốc và câu kết chữ lớn hai dòng; nút "+ FOLLOW" đỏ.
- Mỗi ô thông tin đều **nối nghĩa với lời đang nói**, xuất hiện 0,3–0,5 giây sau từ khóa và tắt khi chuyển ý.

**Để sau này mình tự làm (kế hoạch, chưa dựng):** một skill "bản đồ từ giọng đọc" theo chuỗi sẵn có của repo:
1. Giọng đọc (VieNeu) → `faster-whisper` lấy mốc từng chữ → tách địa danh, số liệu.
2. Lấy dữ liệu: ranh giới/sông/đường/cầu từ OpenStreetMap (Overpass), ảnh vệ tinh tải về một lần thành ảnh lớn (kỹ thuật static map của `remotion-maps`), ghi nguồn ở đáy.
3. **Duyệt kịch bản cảnh trước khi render** (danh sách cảnh: vùng nhìn, lớp hiện, ô số liệu, mốc giây) — đúng luật DUYỆT của repo.
4. Dựng bằng Remotion (đã có đầu bút lóe `KetLaser`, viền chạy ranh giới `BanDoXa`, phụ đề từng chữ); render nhẹ 2 luồng.
5. Tự kiểm 5 mục như trên **cộng kiểm nhãn**: không đè nhau, không bị mép cắt, không trùng tên — làm bằng cách tính hộp chữ trong code rồi so từng cặp, không chỉ nhìn bằng mắt.

**Đã dựng thử (10/2026): mẫu Remotion `BanDoVeTinh`** (`do-hoa/src/mau/BanDoVeTinh.tsx`), bản 24 giây kênh Chợ Gạo – xã An Thạnh Thủy. Thư mục dựng `Desktop/video/_bando_chogao/` có đủ chuỗi script: `lay_chi_tiet.py` (Overpass: ranh giới, sông, đường, cầu) → `tai_ve_tinh.py` (ghép ô Esri z15 cho nền, z17 cho cận cảnh, lưu từng ô) → `du_lieu_ban_do.py` (đổi toạ độ sang pixel ảnh nền) → `props.py` → render 2 luồng (723 khung mất 751 s — chậm hơn mẫu thường vì ảnh vệ tinh lớn + bộ lọc).
- **Bài học dữ liệu:** đếm "đoạn kênh trong xã" bằng điểm-trong-đa-giác cho 8,3 km nhưng thực ra **kênh là ranh giới** giữa An Thạnh Thủy và Tân Thuận Bình — chỉ phát hiện khi **vẽ chồng lên ảnh rồi nhìn**. Luôn vẽ chồng dữ liệu lên ảnh nền trước khi viết lời đọc có số liệu; đo "dọc ranh giới" bằng khoảng cách tới đường ranh (< 150 m).
- **Bài học nhãn (học từ GeoReel `render/flyover.html`):** đặt nhãn theo thứ tự ưu tiên, tính khung chữ trên màn hình; đụng thì đẩy lên từng dòng + đường kẻ nối về điểm; gần mép thì canh vào trong; có **vùng cấm** (tiêu đề, bản đồ nhỏ, ô số liệu, phụ đề); hết chỗ thì **ẩn** chứ không để đè/cắt. Bản đầu chưa có luật này dính đúng 3 lỗi nhóm Sông Đáy từng sửa (đè nhãn, lộ chữ qua ô, mép cắt).
- Nét kênh OSM vẽ từ vết GPS (`source=osm-gpx`) lệch lòng kênh khi phóng sát: phóng > 1,8× thì làm nhạt nét để lộ mặt nước thật.

**Áp vào video của mình:**
- Hợp cho **video giải thích quy hoạch, công trình, tuyến đường, kênh thủy lợi** của xã: sông/kênh phát sáng, có mũi tên dòng chảy, ô số liệu và dòng nguồn ghi rõ "chưa phải quy hoạch duyệt". Dòng nguồn như vậy rất nên học cho tin chính quyền.
- **Ảnh vệ tinh:** Esri World Imagery dùng được nếu ghi nguồn đúng điều khoản Esri (kiểm điều khoản trước khi dùng cho bản phát sóng); ranh giới, sông, đường lấy từ OpenStreetMap (ghi "© OpenStreetMap"). Ranh giới xã phường **sau sáp nhập 2025** phải đối chiếu bản đồ chính thức.
- Dựng bằng Remotion: ảnh vệ tinh nền (kỹ thuật static map của `remotion-maps`) + đường SVG cho sông/đường + các ô kính tối. Giữ ba màu: nền tối, xanh ngọc (nước), vàng (đường, vùng quy hoạch); với ATT NEWS đổi viền thẻ sang navy/vàng.
- Bản ngang 16:9 cho Facebook: đặt thẻ bản đồ bên trái, phụ đề và ô số liệu bên phải, giống bố cục cảnh `PhuNu96`.
- Giọng: dùng giọng VieNeu sẵn có của mình, không cần minimax (dịch vụ ngoài, có thể tính phí; phải hỏi trước).

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
