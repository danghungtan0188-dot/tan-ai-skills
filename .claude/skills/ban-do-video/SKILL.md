---
name: ban-do-video
description: Làm video bản đồ giải thích theo lời đọc cho xã/tỉnh — lấy ranh giới, sông/kênh, đường, cầu từ OpenStreetMap, ghép ảnh vệ tinh Esri làm nền, đổi toạ độ sang pixel rồi dựng bằng mẫu Remotion `BanDoVeTinh` (bản đồ vệ tinh, máy quay trượt/phóng, nhãn tự tránh đè) hoặc `BanDoNoi` (bản đồ xã nổi khối, nét chạy viền). Kích hoạt khi người dùng muốn video bản đồ, "map", ranh giới xã, tuyến kênh/đường/sông, quy hoạch, hành trình qua nhiều điểm, hoặc đưa video mẫu kiểu "Góc nhìn quy hoạch — Sông Đáy", "KOYO Follow the Red Line", phóng sự xã có bản đồ nổi khối.
---

# Video bản đồ theo lời đọc

## Phạm vi

Làm: dữ liệu bản đồ mở (OSM qua Overpass), ảnh vệ tinh Esri, đo số liệu từ dữ liệu, dựng bằng mẫu Remotion có sẵn trong `do-hoa/src/mau/` (`BanDoVeTinh`, `BanDoNoi`, `BanDoXa`), kiểm nhãn và rung máy quay. Học từ 3 video mẫu — ghi đủ trong [references/bai-hoc-ban-do.md](references/bai-hoc-ban-do.md).

Không làm: không bịa số liệu (mọi con số phải đo từ dữ liệu hoặc người dùng đưa, và ghi nguồn trên khung); không dựng 3D WebGL (three.js/Cesium) — quá nặng cho máy hay sập nguồn, trừ khi người dùng yêu cầu rõ; không dùng dịch vụ trả phí (Mapbox key, giọng minimax…) khi chưa hỏi.

## Quy trình

Thư mục dựng đặt cạnh video của người dùng (ví dụ `Desktop/video/_bando_<ten>/`), không trong repo.

1. **Dữ liệu:** `python scripts/lay_osm.py "<tên xã>" --ra osm.json` → in các relation khớp tên; chọn đúng bằng `--id`. Ranh giới sau sáp nhập 2025 có thể chưa đúng — nói với người dùng.
2. **Ảnh nền:** `python scripts/tai_ve_tinh.py 15 <lon0> <lat0> <lon1> <lat1> nen15.jpg` (nới bbox xã ~0,03°); cận cảnh điểm quan trọng: z17, khung đủ cao cho khung dọc 9:16 (~2,9 × 4,4 km).
3. **Đổi toạ độ:** `python scripts/chuyen_toa_do.py osm.json nen15.jpg.json --song "<tên>" --duong "QL.50,ĐT.877" --can cau17.jpg.json --ra ban_do.json`.
4. **Vẽ chồng và nhìn trước khi viết lời** (PIL vẽ ranh giới, sông, đường, cầu lên ảnh nền thu nhỏ). Đo tuyến so với ranh giới bằng `python scripts/do_ranh.py osm.json --xa-id <id> --way <id>`: tách **km trong xã** và **km dọc ranh giới**. Kênh Chợ Gạo: đếm kiểu điểm-trong-đa-giác ra "8,3 km trong xã" nhưng thật ra kênh là **ranh giới** (8,5 km dọc ranh, 0 km trong xã).
5. **Lời đọc** viết từ số đã đo, số viết bằng chữ cho VieNeu; chọn bản đọc bằng `chon_ban_tts.py` (skill `bien-tap-video-thong-minh-song-ngu-tan`). Ghép giọng xong chạy `moc_tung_chu.py giong.wav moc.json` (cùng skill) để có **mốc từng chữ thật** cho phụ đề (`cau_doc[].tu`) — không chia đều câu; câu nào báo "ÍT KHỚP" thì nghe lại.
6. **Props + xem khung tĩnh** (`npx remotion still`) ở mọi mốc đổi cảnh, sửa nhãn/khung tới khi sạch, **rồi** mới render.
7. **Mẫu 10–20 giây trước** khi video cần "wow" (quy trình hậu trường KOYO): người dùng góp ý theo 4 câu — hình? âm thanh? chuyển cảnh? đủ wow chưa? — duyệt xong mới làm dài theo từng chặng.
8. **Render nhẹ:** Remotion `--concurrency=1`, ưu tiên thấp; báo trước thời gian (ảnh vệ tinh nặng: 24 giây video ~ 12–25 phút).
9. **Kiểm:** `python scripts/video_qa.py <file> --strict --audio` (cấp repo) + tự kiểm của video bản đồ dưới đây.

## Tự kiểm riêng của video bản đồ (học từ nhóm Sông Đáy)

| Mục | Ngưỡng |
|---|---|
| Nhãn không đè nhau, không bị mép thẻ cắt, không trùng tên, không lộ qua ô số | xem khung tĩnh mọi mốc; mẫu `BanDoVeTinh` có luật đặt nhãn: ưu tiên → đẩy lên + đường kẻ → hết chỗ thì ẩn |
| Toạ độ khớp ảnh vệ tinh | vẽ chồng, lệch < 1 px ở z15; nét OSM vẽ từ vết GPS (`source=osm-gpx`) lệch khi phóng sát → làm nhạt nét |
| Máy quay êm | lia ≤ 12,8 px/khung, zoom ≤ 6,6 %/khung (in vị trí camera từng khung khi nghi rung) |
| Đủ khung, không khung nhảy | `video_qa` + giải mã hết file |
| Dòng nguồn trên khung | "Ảnh vệ tinh: Esri, Maxar · … © OpenStreetMap" + "chưa phải số liệu chính thức" khi số đo từ OSM |

## Mẫu Remotion

- `BanDoVeTinh` — thẻ bản đồ dọc viền xanh ngọc trên nền lưới; tiêu đề, mũi tên Bắc, bản đồ nhỏ định vị, thước tỷ lệ tự đổi, phụ đề sáng theo lời, dòng nguồn, thanh tiến độ; kênh phát sáng vẽ dần có đầu bút, ranh giới xã vẽ dần, tuyến đường, ghim cầu, ô số đếm lên; máy quay theo `canh`, lớp theo `moc`. Ví dụ props: `Desktop/video/_bando_chogao/props.py`.
- `BanDoNoi` — bản đồ xã nổi khối 16:9 (nét trắng chạy viền → màu ngọc → khối nổi → tên gõ chữ → lóe trắng).
- `BanDoXa` — ranh giới xã phẳng kiểu clip TikTok (dò theo ảnh bản đồ chính thức).
- `SoDeFlycam` — số liệu đè flycam theo lời bình (dùng chung với cảnh flycam sau bản đồ).
