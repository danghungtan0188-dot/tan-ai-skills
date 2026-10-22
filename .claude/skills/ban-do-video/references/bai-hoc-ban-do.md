# Bài học video bản đồ (10/2026)

Gom từ 3 video mẫu đã xem kỹ + 1 bản thử tự làm. Phân tích đầy đủ từng video (khung hình, nhịp, công thức) nằm trong
`skills/hieu-ung-video/references/ky-thuat-tu-video-mau.md`; file này chỉ giữ phần dùng cho bản đồ.

## 1. "Góc nhìn quy hoạch — Sông Đáy" (reel dọc 3 phút 10)

- **Cách làm:** có file giọng đọc trước → kéo vào Claude desktop (tab Code) → gọi skill bản đồ riêng của tác giả → ~20 phút ra `SongDay_BanDo_v4.mp4` (117 giây, 1080×1920). Là **bản thứ 4** — có duyệt nội dung và sửa 3 lượt, không phải một Enter.
- **Bố cục:** nền đen lưới ô + ánh vàng từ dưới; thẻ bản đồ bo góc viền xanh ngọc; trong thẻ cố định: dòng nhỏ giãn chữ + tên lớn + dòng phụ, mũi tên Bắc + bản đồ nhỏ định vị, thước tỷ lệ, tiêu đề lớn phát sáng, phụ đề từ khóa vàng, 2 dòng nguồn, thanh tiến độ.
- **Đồ họa:** sông phát sáng, mũi tên trắng chạy theo dòng, nét đứt = phương án nắn dòng, số đo bên bờ; nhãn trạng thái viên thuốc ("PHƯƠNG ÁN ĐANG NGHIÊN CỨU"); ô cảnh báo "Chưa phải quy hoạch cuối cùng"; thước bề rộng đường + mặt cắt làn xe; số đếm "6.000+ HỘ"; biểu tượng người + dấu hỏi trên khu dân cư; bảng bật/tắt lớp có ô tích; vùng quỹ đất viền vàng; so diện tích bằng 2 ô vuông đúng tỷ lệ; sơ đồ hai bên (bản đồ tối đi); ô "CHỈ CẦN NHỚ 3 THỨ".
- **Tự kiểm 5 mục** (đã thành bảng trong SKILL.md) và **lỗi v3 → v4**: nhãn đè nhãn, tên xã lộ qua thẻ, 2 nhãn trùng, nhãn thò dưới ghim, nhãn bị mép cắt.
- **Ghi nguồn rõ "chưa phải quy hoạch duyệt"** — rất nên học cho tin chính quyền.

## 2. "KOYO — Follow the Red Line" (125 giây, 8 điểm)

- **Mỗi điểm 6 nhịp:** bay theo đường đỏ → ô phẳng nở thành địa hình → đường đỏ chạy trên địa hình → **biểu tượng riêng của nơi đó dựng từ cùng bộ nét + hạt cam** (cây chấm xoắn, thác nét dọc, đèo zíc zắc + số 08→48, vòm cây + thước 300 M, cổng torii khung dây, cầu + đường kích thước 390 M / 173 M) → hạt tụ thành **ảnh thật** viền cam có đường kẻ nối về điểm → ảnh thu thành dải mỏng trượt đi. Không có cú cắt nào.
- **Mở = kết** (tiêu đề + toàn cảnh); 2 lần lùi ra toàn cảnh, bảng danh sách tích dần.
- **Hậu trường (4 ngày, 12 bản nháp, 9 lần đổi hướng):** mặt đất đứng yên, chỉ đường + đốm sáng nhấn nhạc; đo rung từng khung trước khi đưa xem; in vị trí camera từng khung để bắt camera nhấp nhô; bản đồ phẳng, 3D chỉ ở điểm dừng; mỗi điểm ≥ 10 giây; camera hạ thấp, đến gần, sương, ảnh thật 2,7 giây có ghi nguồn; mẫu 1 điểm cận cảnh duyệt xong mới làm lại cả bài.
- **Bản nhẹ cho miền Tây (phẳng):** bỏ khối địa hình; "trồi lên" = ảnh vệ tinh mở ra từ ô chữ nhật; ẩn dụ bằng SVG: ruộng → lưới chấm vàng mọc dần, kênh → nét chảy song song, cầu → đường kích thước, chợ nổi → chấm ghe tụ lại, trường/trạm → khung dây nhà.

## 3. Phóng sự xã "Lương Hòa đồng hành cùng doanh nghiệp"

- **Bản đồ xã nổi khối** → đã thành mẫu `BanDoNoi`: nền xanh đêm + ranh xã lân cận mờ; nét trắng chạy viền; phủ ngọc; khối nổi mép sáng; tên xã gõ từng chữ góc dưới trái; **lóe trắng nối sang flycam**.
- Ngay sau bản đồ là flycam + **số đè thẳng lên flycam** theo lời bình → mẫu `SoDeFlycam`.

## 4. GeoReel (repo `Vibetool/GeoReel`, MIT — đã tải về `D:\GitHub\GeoReel` để đọc)

- Agent skill dựng flyover 3D bằng Cesium (nặng, cần token miễn phí; thiếu token thì về ảnh phẳng Esri).
- **Học được luật đặt nhãn** (`render/flyover.html`, hàm `resolveLabelCollisions`): khung chữ tính trên màn hình; nhãn gần mép (x > 70 % hoặc < 30 %) canh vào trong; thử đẩy lên 0…6 dòng, dòng đầu tiên không đụng thì dùng, có đường kẻ nối về điểm; nhớ độ đẩy cũ ("sticky") để nhãn không nhảy giữa các khung. `BanDoVeTinh` đã áp (chưa có "sticky" — máy quay chậm nên chưa thấy nhảy; nếu thấy thì thêm).

## 5. Bản thử tự làm: kênh Chợ Gạo – xã An Thạnh Thủy (24 giây, 9:16)

Thư mục `Desktop/video/_bando_chogao/` — đủ chuỗi script đời đầu + props + giọng "Hùng Tân chân thật - script".

- **Kênh là ranh giới, không phải "chảy trong xã"** — chỉ phát hiện khi vẽ chồng lên ảnh. Đã thành `scripts/do_ranh.py` + test.
- Bản đầu dính đúng 3 lỗi nhóm Sông Đáy (đè nhãn, chữ lộ qua ô số, mép cắt) + phụ đề không xuống dòng, phụ đề đè thước tỷ lệ → đã sửa trong mẫu (vùng cấm nhãn: tiêu đề + bản đồ nhỏ, ô số, thước + phụ đề).
- Way cầu trên OSM hay mang tên đường ("Đường huyện 25B") → `chuyen_toa_do.py` chỉ lấy way tên bắt đầu "Cầu".
- Nominatim bị chặn DNS trên máy; Overpass dùng được. Truy vấn relation phải `out geom;` (thiếu `members` nếu dùng `out geom tags;`).
- Render 723 khung mất 751 giây ở 2 luồng — **chậm vì ảnh nền lớn + bộ lọc**; từ nay 1 luồng và báo trước thời gian. Nhãn "ĐT.877" bị ẩn do hết chỗ — nếu cần thì dời điểm đặt nhãn dọc tuyến.
