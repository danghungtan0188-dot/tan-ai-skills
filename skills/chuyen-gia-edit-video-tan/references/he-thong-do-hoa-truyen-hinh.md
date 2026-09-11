# Hệ thống banner – chú thích – icon truyền hình Việt Nam

"Chất truyền hình Việt Nam" nhưng **thiết kế nguyên bản**: không lấy màu, logo, kiểu chữ hay bố cục đặc trưng
của VTV, HTV hay bất kỳ đài nào; không trích xuất logo/icon từ ảnh chụp màn hình của đài.

Công cụ: `scripts/broadcast_kit.py` (banner, thẻ, motion), `scripts/callouts.py` (chú thích),
`scripts/icons.py` (icon), `scripts/validate_graphics.py` (kiểm tự động).
Token: `assets/broadcast/styles.json`, preset: `assets/broadcast/programs.json`.

## 1. Năm phong cách hình ảnh

| Phong cách | Dùng cho | Chủ đạo | Motion |
|---|---|---|---|
| `national-modern` | chính luận, thông tin công cộng (hợp bản tin ATT NEWS) | navy + đỏ + vàng | trượt 0,45 s |
| `newsroom-digital` | công nghệ, kinh tế, tin nhanh | nền tối + cyan | lộ dần theo mặt nạ 0,30 s |
| `editorial-premium` | phân tích, phỏng vấn, phóng sự | than chì + vàng đồng | mờ dần 0,60 s |
| `community-live` | sự kiện, tin địa phương | xanh lá + hổ phách | trượt 0,40 s |
| `urgent-alert` | cảnh báo, giao thông, thời tiết, tin khẩn | đỏ đậm + vàng | trượt 0,25 s, **không nhấp nháy** |

Đổi phong cách = đổi một tham số `--style`; màu, bo góc, mật độ, motion đi theo token.
Chữ trên nền nhấn tự chọn trắng/đen theo độ tương phản (≥ 4,5:1).

## 2. Bảy preset chương trình

`tin-nhanh`, `chinh-luan`, `phan-tich`, `cong-nghe`, `cong-dong`, `canh-bao-khan`, `social-doc` — mỗi preset định
phong cách, khung hình, độ dài, bộ component, chế độ phụ đề, nhịp cắt, chuyển cảnh và nhạc (xem `programs.json`).
`canh-bao-khan` bắt buộc `verified=true` + nguồn + thời điểm cập nhật; cấm nhấp nháy, còi hú giả.

## 3. Banner — 15 component

| Component | Dùng khi | Ô mặc định |
|---|---|---|
| `headline_strap` | tiêu đề tin, tự xuống tối đa 2 dòng | dải dưới (thay phiên với lower-third) |
| `topic_slug` | chuyên mục: Y TẾ, GIÁO DỤC… | trên trái, hàng 0 |
| `lower_third` | tên + chức danh (chỉ lấy từ kịch bản/người dùng) | dải dưới |
| `chip` | vị trí / ngày / giờ / LIVE, kèm icon | trên trái, hàng 1 |
| `label_chip` | HÌNH ẢNH AI · TƯ LIỆU · ẢNH MINH HOẠ · MÔ PHỎNG | trên phải, hàng 0 |
| `source_strap` | "Nguồn: …" | trên phải hàng 1 (9:16: trái hàng 2) |
| `breaking_bar` | tin khẩn — từ chối dựng nếu thiếu xác minh | ngang đáy |
| `status_bar` | "Cập nhật 14:30" | ngang đỉnh |
| `ticker_strip` | tin chạy | ngang đáy |
| `quote_card` | trích dẫn nguyên văn + người nói | giữa |
| `fact_card` | con số chính (dùng số thật) | phải, từ hàng 3 |
| `comparison` | so sánh hai giá trị | giữa |
| `timeline` | mốc sự kiện | giữa |
| `map_card` | bản đồ **người dùng cung cấp** + ghim + nhãn | phải |
| `end_card` | CTA / kết | toàn khung |

Dải dưới chỉ một banner một lúc. 20% đáy dành cho phụ đề.

## 4. Chú thích (`callouts.py`)

Mũi tên · vòng tròn · ngoặc góc · spotlight · kính lúp · ghim số · biểu đồ cột · bộ đếm tăng dần ·
quy trình nhiều bước · chú thích bám vật thể (`track` bằng OpenCV MIL + tệp `sendcmd`).
Mọi nét có viền tối bên dưới để nổi trên nền nào cũng đọc được.

Quy tắc tránh: không đè **mặt, tay, micro, màn hình trình chiếu, phụ đề (20% đáy)**; khung dọc chừa UI nền tảng
(trên 12%, dưới 20%, phải 15%). Tối đa 2 chú thích cùng lúc, mỗi cái hiện ≥ 1,5 s.
Tracker chỉ gợi ý vị trí — mất dấu thì dừng, không đoán; xem lại từng giây.

## 5. Icon (`icons.py` → `assets/broadcast/icons/*.svg`)

22 icon một hệ: lưới 24, nét 2, đầu nét tròn — live, time, date, location, map, weather, traffic, document,
data, medical, education, tech, archive, stock, ai, microphone, camera, quote, phone, website, email, warning.
SVG và PNG vẽ từ cùng một định nghĩa. Không trộn emoji với icon này. Logo Facebook/Zalo/YouTube/TikTok chỉ dùng
file chính thức do người dùng cung cấp — không tự vẽ lại logo nền tảng.

## 6. Motion

Vào → giữ → ra, dựng thành chuỗi khung PNG (lặp lại được y hệt, không phụ thuộc biểu thức ffmpeg):
trượt, mờ dần, lộ dần theo mặt nạ, bộ đếm, ticker 140 px/s.
Tin khẩn: không nhấp nháy; cả video không quá 3 lần chớp sáng mỗi giây (ngưỡng an toàn cho người nhạy cảm
ánh sáng); không xen kẽ đỏ–xanh.

## 7. Khung hình 16:9 · 9:16 · 1:1

Dựng lại đồ hoạ theo `--aspect` — vùng an toàn và ô bố cục khác nhau theo khung; **không crop mù** bản 16:9.

## 8. Kiểm tự động

```bash
python scripts/broadcast_kit.py render spec.json --out-dir gfx
python scripts/validate_graphics.py gfx/manifest.json --video INPUT --scenes scenes.json --frames gfx/duyet
```

Lỗi chặn: ra ngoài vùng an toàn · che mặt (tự dò bằng OpenCV) hoặc vùng `--protect` · chữ dưới cỡ tối thiểu ·
tương phản < 4,5:1 · logo méo > 2% · tin khẩn chưa xác minh · trùng id · hai đồ hoạ đè nhau cùng lúc ·
banner tràn cảnh. Cảnh báo: chữ dài, không đọc kịp (> 15 ký tự/giây).
Dò mặt có thể sót mặt nghiêng/nhỏ — vẫn phải xem ảnh trong `gfx/duyet`.

Ghép một đồ hoạ vào video:

```
-framerate 30 -i gfx/<id>/f_%04d.png
[k:v]setpts=PTS-STARTPTS+<start>/TB[g];[base][g]overlay=<x>:<y>:eof_action=pass
```
