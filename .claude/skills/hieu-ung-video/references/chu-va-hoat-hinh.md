# Text & hoạt hình chữ

Dùng filter `drawtext` của ffmpeg. Font tiếng Việt đã xác nhận hoạt động tốt: `C:/Windows/Fonts/segoeuib.ttf` (Segoe UI Bold) — đủ dấu, không lỗi encode khi dùng `textfile=` đọc từ file UTF-8.

## Nguyên tắc bắt buộc (đã kiểm chứng thực tế)

1. **Dùng `textfile=` thay vì `text=` cho tiếng Việt** — tránh lỗi escape shell với dấu và ký tự đặc biệt. Ghi từng dòng chữ ra 1 file `.txt` UTF-8 riêng trước.
2. **Font phải là `.ttf` hỗ trợ Unicode tiếng Việt** — `segoeuib.ttf` hoặc `arialbd.ttf` trên Windows đã test OK. Font không hỗ trợ sẽ ra ký tự lỗi/ô vuông.
3. Trên Windows, đường dẫn font trong filter cần escape dấu `:` — viết `C\:/Windows/Fonts/segoeuib.ttf`.

## Banner/lower-third tiêu đề (đã dùng thật trong dự án)

```bash
F='drawbox=x=460:y=760:w=1000:h=56:color=0xC0272D@1.0:t=fill:enable=between(t\,0\,4),'
F+='drawbox=x=460:y=822:w=1000:h=120:color=0x0A1830@0.85:t=fill:enable=between(t\,0\,4),'
F+='drawbox=x=460:y=822:w=6:h=120:color=0xF5A623@1.0:t=fill:enable=between(t\,0\,4),'
F+="drawtext=fontfile='C\:/Windows/Fonts/segoeuib.ttf':textfile='dong1.txt':fontsize=30:fontcolor=white:x=(w-tw)/2:y=778-th/2:enable=between(t\\,0\\,4),"
F+="drawtext=fontfile='C\:/Windows/Fonts/segoeuib.ttf':textfile='dong2.txt':fontsize=26:fontcolor=white:x=490:y=850:enable=between(t\\,0\\,4)"
ffmpeg -i input.mp4 -vf "$F" -c:v libx264 -preset fast -crf 19 -pix_fmt yuv420p -c:a copy output.mp4
```

Cấu trúc: dải màu đỏ phía trên (tên kênh/thương hiệu) + khung tối bán trong suốt phía dưới (tiêu đề nội dung) + vạch màu nhấn bên trái — đúng kiểu banner tin tức CapCut hay dùng.

## Hoạt hình chữ

### Fade-in / fade-out chữ

```
drawtext=...:alpha='if(lt(t,0.5),t/0.5,if(lt(t,3.5),1,if(lt(t,4),(4-t)/0.5,0)))'
```
Chữ mờ dần vào trong 0.5s, giữ rõ đến t=3.5s, mờ dần ra trong 0.5s cuối.

### Typewriter (chữ gõ dần từng ký tự)

Không có filter dựng sẵn 1-bước; cách làm: nhiều lớp `drawtext` cùng vị trí, mỗi lớp hiện dần thêm 1-2 ký tự theo `enable`, HOẶC dùng `text` với biểu thức cắt chuỗi theo thời gian nếu bản ffmpeg hỗ trợ. Thực tế đơn giản hơn: dựng qua HyperFrames/CSS (typewriter là hiệu ứng CSS/JS chuẩn, xem `hyperframes-animation`) rồi render ra clip overlay, ghép vào bằng `overlay` filter — mượt hơn nhiều so với ép ffmpeg thuần làm typewriter.

### Pop-in (chữ phóng to rồi về đúng cỡ)

Cách đáng tin cậy nhất: dựng qua HyperFrames (`hyperframes-animation`, easing `ease_out_cubic`) rồi render clip overlay có nền trong suốt (WebM alpha), ghép bằng `overlay` — ffmpeg thuần không có scale-theo-thời-gian tiện dụng cho drawtext.

### Đếm ngược động (dùng lại được cho hiệu ứng đồng hồ)

```
drawtext=text='%{eif\:trunc(<TONG_GIAY>-t)\:d}':fontsize=48:fontcolor=white:x=(w-tw)/2:y=40
```
Hiện số giây đếm ngược từ `<TONG_GIAY>` về 0, dùng `%{eif\:...\:d}` để ép kiểu số nguyên.

## Phụ đề (caption) burn-in

Ưu tiên dùng `helpers/render.py` của `video-use` (đã có sẵn force_style chuẩn `bold-overlay` cho short-form, và style `natural-sentence` cho nội dung dài) thay vì tự viết filter `subtitles=` thủ công — video-use đã xử lý đúng thứ tự (phụ đề luôn burn SAU CÙNG, sau mọi overlay khác).
