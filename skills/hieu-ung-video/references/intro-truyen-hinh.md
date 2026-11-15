# Intro, kết và chuyển cảnh zoom học từ truyền hình

Rút từ 4 video Tân đưa ngày 15/11/2026, soi 10 khung/giây:
- 3 video của Truyền hình Đồng Tháp: trailer gameshow 66 s, giới thiệu thí sinh 146 s, phóng sự 10 phút;
- 1 phim tổng kết sự kiện làm từ ảnh tĩnh, 6 phút.

Ghi chú đầy đủ từng giây ở repo riêng `hoc-marketing` (`docs/hoc-4-video-desktop.md`).
**Học cách làm, không chép đồ họa của đài.**

## 1. Công thức intro trailer 18 giây (hình khớp từng câu đọc)

| Nhịp | Dài | Làm gì | Có sẵn trong repo |
|---|---|---|---|
| Con số biểu tượng | 3 s | Một con số (năm thứ, số năm, mốc) nổi khối, xoay từ nghiêng ra chính diện, máy đẩy vào chậm | `so-dem-chay`, `tieu-de-mo-dau` (`motion-graphics-tan`) |
| Lóe sáng chuyển | 0,4 s | Vệt sáng quét chéo + hòa tan | `light_leak`, `flash_white` ([ky-thuat-tu-video-mau.md](ky-thuat-tu-video-mau.md)) |
| Tường ảnh tư liệu | 6 s | Hàng trăm ảnh cũ ghép thành mặt cong, máy bay sát rồi logo trồi lên từ biển ảnh | Mẫu Remotion `AnhBayVao` (gần nhất) |
| Giữ logo | 2 s | Logo + tiêu đề phụ viết tay đứng yên trên nền mờ | — |
| Bộ đếm chạy tới mốc | 3,3 s | Vòng HUD đếm 16 → 100, **cảnh dưới vòng đổi mỗi 0,3–0,5 s**; chớp 1 khung tên chương trình giữa chừng | Mẫu Remotion `HudDemSo` |
| Đỉnh | 0,8 s | Tới mốc: sao/hạt nổ từ tâm, khối lớn bay vào máy lấp kín khung | — |
| Vào nội dung | 1 s | Chữ khổng lồ chạy ngang trước cảnh thật ("TỔNG KẾT NĂM…") | Bảng "Hiệu ứng trend" trong [lam-nhu-capcut.md](lam-nhu-capcut.md) |

**Hình khớp lời đọc (chép lời whisper):**
- 0,8–5,9 s đọc "17 năm, một hành trình bền bỉ…" ↔ huy chương số 17;
- 5,9–11,2 s "…chắp cánh ước mơ cho biết bao thế hệ" ↔ tường ảnh các thế hệ;
- 11,2–17,1 s "năm thứ 17 đã chính thức trở lại" ↔ bộ đếm chạy tới 100, nổ sao đúng lúc câu khép lại.

Mỗi khối đồ họa dài đúng một câu đọc.

**Bộ đếm là sợi chỉ:** chuỗi cảnh cắt rất nhanh (0,3 s) vẫn không rối vì có một thứ đứng yên ở giữa (vòng đếm). Dùng cho "10 năm HTX", "100% xã viên".

## 2. Intro chương trình phóng sự (ẩn dụ bằng hình, 20 s)

Sách 3D mở giữa trời → ảnh trường dựng lên từ trang sách → đom đóm có vệt hạt bay quanh bàn học đêm rồi đậu vào đèn, **đèn sáng** → biểu tượng (Khuê Văn Các) → **máy lao xuyên qua ô cửa tròn** → tựa thư pháp lộ ra qua khung cửa → giữ 2,5 s → **tối về đen 0,6 s → sáng lên cảnh thật**.

- Ẩn dụ một ý duy nhất ("thắp sáng" = đèn bật), không cần chữ giải thích.
- **Dip to black** tách thế giới đồ họa khỏi phóng sự thật.
- Phóng sự mở bằng chuỗi cảnh **xa → gần** (toàn → trung → cận mặt giữ 3,5 s → đặc tả tay), không lời. Hợp phong cách phim tài liệu của Tân.

## 3. Phần kết của đài

- **Logo tài trợ, 10 s:** mỗi logo một cách hiện riêng, 2 s mỗi logo (hạt tụ lại thành logo 3D; nền mưa số vàng + tia sáng; logo + khẩu hiệu thư pháp). Sau đó **cả hàng về đứng chung**, vệt sáng lướt qua từng logo.
- **Ident đài, 8 s, giống hệt nhau ở mọi video:**
  1. nét sáng vẽ viền chữ;
  2. khối chữ 3D trượt chéo sát máy;
  3. lóe thành tấm sáng;
  4. thu lại thành logo, chữ đổ màu kèm lệch màu RGB;
  5. icon mạng xã hội bật lần lượt;
  6. tên kênh gõ dần, đứng yên tới hết.
- Kênh ATT đã có intro/kết tia laser nền xanh lá. Nên **khóa thành một ident cố định** và thêm hàng icon mạng xã hội + tên kênh gõ dần.

## 4. Bố cục vuông 1:1 cho Facebook

Nửa trên: video ngang 16:9 gốc. Nửa dưới: **băng cố định suốt video** gồm câu mời ("Đón xem tập 1…" hoặc "Bạn chọn team nào?") + hàng logo đối tác. Một bản dựng ngang dùng lại cho bài đăng vuông, câu hỏi ở băng dưới mồi bình luận.

## 5. Chuyển cảnh zoom (phim tổng kết từ ảnh tĩnh)

Soi ở 10 khung/giây. Toàn bộ chuyển cảnh dài 0,5–0,8 s. Phần mờ mạnh nhất chỉ 1–2 khung.

| Kiểu | Diễn biến | Thời lượng |
|---|---|---|
| **Zoom xuyên mờ tâm** | Cảnh cũ phóng vào tăng tốc 0,2 s → 1–2 khung mờ tâm (radial blur) → cảnh mới bắt đầu phóng to ~130%, nghiêng 10–30°, còn mờ → chậm dần về 100%, thẳng | 0,6–0,8 s |
| **Đập zoom tại chỗ** | 1 khung mờ tâm chớp trên chính ảnh đang chiếu, kèm lóe sáng, đúng phách nhạc | 0,1 s |
| **Zoom lùi + gương** | Ảnh mới thu nhỏ dần, viền ngoài lặp ảnh soi gương thay vì nền đen | 0,5 s |
| **Lật dọc + phình ống kính** | Ảnh ép mỏng thành sọc dọc (lật 3D) rồi bung ra ảnh mới bị phình như mắt cá | 0,4 s |
| **Xoay mờ** | Ảnh cũ xoay nhanh có mờ xoay → cắt vào ảnh mới đang lùi về | 0,3 s |
| **Hộp kính 3D** | Màn đen → ảnh nhỏ trong khối kính trong suốt xoay lao về máy | 0,6 s |

Nguồn mở làm sẵn (MIT, đã tải ở `D:\GitHub\ngoai\gl-transitions`, chưa chạy trên máy): `CrossZoom` (zoom xuyên mờ), `RotateScaleFade`, `ZoomInCircles`, `Cube` / `InsideCube`, `WhipSpin`, `Swirl`.

### Công thức ffmpeg zoom xuyên (đã chạy thử 15/11 trên clip 540×960)

Cảnh `a` lao vào 0,3 s cuối. Cảnh `b` vào 0,5 s đầu từ phóng 1,5 và nghiêng 8°, chậm dần về thẳng. Mờ tâm giả bằng cách trộn 3 bản phóng to lệch nhau.

```bash
ffmpeg -threads 2 -i a.mp4 -i b.mp4 -filter_complex "\
[0:v]trim=0:1.7,setpts=PTS-STARTPTS[a1];\
[0:v]trim=1.7:2,setpts=PTS-STARTPTS,zoompan=z='1+0.8*pow(in/8,2)':d=1:x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':s=540x960:fps=30,split=3[p][q][r];[q]scale=576:-2,crop=540:960[q2];[r]scale=612:-2,crop=540:960[r2];[p][q2][r2]mix=inputs=3[a2];\
[1:v]trim=0:0.5,setpts=PTS-STARTPTS,rotate='0.14*pow(1-t/0.5,2)':c=black,zoompan=z='1+0.5*pow(1-in/14,2)':d=1:x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':s=540x960:fps=30,split=3[u][v][w];[v]scale=568:-2,crop=540:960[v2];[w]scale=596:-2,crop=540:960[w2];[u][v2][w2]mix=inputs=3[b1];\
[1:v]trim=0.5,setpts=PTS-STARTPTS[b2];\
[a1][a2][b1][b2]concat=n=4:v=1:a=0,format=yuv420p" -c:v libx264 -preset faster -crf 20 ra.mp4
```

- Đổi `1.7:2` theo độ dài cảnh `a` (0,3 s cuối). Đổi `540x960` cho đúng khung. `in/8` và `in/14` là số khung của đoạn lao vào/đi ra trừ 1 (ở 30 khung/giây).
- **Xoay TRƯỚC, phóng to SAU.** Làm ngược lại (phóng to rồi xoay) thì khung đầu của cảnh mới lộ góc đen. Đã thấy lỗi này khi thử, đã sửa.
- Chỉ ghép hình. Tiếng ghép riêng, rồi đặt một tiếng "vút" đúng khung mờ nhất (bộ `sfx` của `motion-graphics-tan`).
- Mỗi video chỉ dùng **1–3 lần** ở chỗ đổi phần. Phim tổng kết 6 phút dùng chuyển cảnh liên tục thì xem rất mỏi mắt.

## 6. Mở phim tổng kết từ ảnh tĩnh

Học được 5 kiểu mở, đều làm được chỉ bằng ảnh:
1. **Ảnh bo góc trượt lên xếp chồng**, 0,4 s một ảnh, như chia thẻ bài.
2. **Số năm lăn dọc 2025 → 2026**: chữ số cuối lăn chậm 1,4 s, có nhiễu lệch màu.
3. **Chữ lồng ảnh**: lòng chữ số năm là ảnh, đổi mỗi 0,2 s.
4. **Lời chào** hiện từ xám, lóe viền cam rồi thành trắng.
5. **Hàng chục ảnh nhỏ bay rải** trên nền đen, dày dần rồi thưa.

**Kết:** nền tia sáng lao về tâm, chữ "cảm ơn" hiện ngẫu nhiên từng chữ cái có bóng phản chiếu, rồi vệt hạt vàng vẽ hình trái tim.

## Số đo nhịp (`tham_do_sau.py`)

| Video | Cảnh trung vị | Cắt mềm | Nhạc nền |
|---|---|---|---|
| Trailer 66 s | **0,27 s** | 35/66 | có, 117 BPM |
| Giới thiệu thí sinh 146 s | 6,9 s | 6/19 | có, 117 BPM |
| Phim ảnh tĩnh 6 phút | 0,73 s | 219/316 (chuyển mềm trung bình 0,5 s) | có, 144 BPM |
| Phóng sự 10 phút | 2,5 s | 23/190 | có, nhỏ hơn giọng 15,7 dB |

Trailer cắt cực nhanh vì đồ họa và bộ đếm chiếm gần hết thời lượng. Phóng sự giữ 2,5 s/cảnh, nhạc rất nhỏ dưới giọng.
