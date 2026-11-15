# Kỹ thuật dựng học từ 86 video marketing

Mỗi kỹ thuật có một thẻ mẫu HyperFrames 1080×1920 trong `assets/ky-thuat/<ten>/index.html`.
Nguồn: 81 reel Facebook (Quizzy Social Media, Hong Phuong) + 5 video YouTube Ngô Bằng AI, xem hết 2 khung/giây và đo nhịp cắt (06/11/2026).
**Học cách làm, không chép thiết kế:** màu, hoa tiết và chữ trong thẻ là của mình (nền kem/nâu đất, nhấn vàng/cam, viền xanh ngọc).

## Bảng chọn

| Kỹ thuật | Thẻ | Dùng khi | Thời lượng mẫu | Biến |
|---|---|---|---|---|
| Phụ đề tô từ khóa | `phu-de-to-tu` | Video người nói: chữ trắng viền đen, từ quan trọng màu vàng | 4 s, mỗi câu ~1,9 s | `dong-1` `tu-1` `dong-2` `tu-2` |
| Tiêu đề mở đầu | `tieu-de-mo-dau` | 3 giây đầu: có ngay khung 0, có con số, không chào hỏi | 3 s | `dong-nho` `dong-lon` `dong-so` |
| Số mục to | `so-muc-to` | Chia video thành bước "01, 02…" | 3 s | `so` `ten-muc` `giai-thich` |
| Khung điện thoại | `khung-dien-thoai` | Đặt clip ví dụ trong khung máy trên nền hoa tiết | 3,5 s | `trong-khung` `nhan` |
| Ô "?" lật dần | `o-hoi-lat` | Danh sách 3 ý, lật ô đúng lúc nói tới, giữ người xem tới cuối | 4,5 s, lật ở 1,2 / 2,2 / 3,2 s | `tieu-de` `muc-1..3` |
| Chia đôi | `chia-doi` | Hướng dẫn thao tác: trên màn hình máy, dưới người nói | 4 s | `buoc` `cho-nguoi` |
| Thẻ kiến thức | `the-kien-thuc` | "GIAI ĐOẠN 1–5", nền trơn, đứng yên để chụp màn hình | 5 s (vào xong trong 1 s rồi đứng) | `giai-doan` `moc` `muc-tieu` `y-1..3` |
| Mốc giờ số to | `moc-gio` | Vlog "một ngày", mỗi cảnh một mốc giờ | 3 s | `gio` `viec` |
| Khoanh đỏ vẽ tay | `khoanh-tay` | Chỉ nút cần bấm trên cảnh quay màn hình | 3 s, vẽ trong 0,45 s | `nut` `ghi-chu` |
| Chữ mờ phía sau | `chu-ma-nen` | Mở chương: chữ viền rất to trôi chậm sau số chương + tiêu đề | 3,5 s | `chu-ma` `so-chuong` `tieu-de` |
| Con trỏ chuột giả | `con-tro-gia` | Dựng lại giao diện bằng thẻ (không lộ thông tin riêng): gõ chữ → di chuột → bấm → kết quả | 4,5 s | `cau-hoi` `go` `nut` `ket-qua` |
| Số đếm chạy | `so-dem-chay` | Một con số ấn tượng: chạy 0 → số cuối, dấu chấm hàng nghìn kiểu Việt | 3,5 s, đếm 1,4 s | `nhan` `so-cuoi` `don-vi` |
| Ô bình luận gõ từ khóa | `o-binh-luan` | Lời mời comment nhận quà: ô bình luận giả hiện dưới mặt, từ khóa gõ từng ký tự nên người xem thấy đúng phải gõ gì (Hong Phuong 2132119387418154: 190 bình luận) | 4 s, gõ từ 1,1 s, 0,12 s/ký tự | `dong-tren` `chu-goi` `tu-khoa` `go` |
| Giải thích 5 cảnh | `giai-thich-5-canh` | Giới thiệu dịch vụ trọn gói: vấn đề → mình làm gì → 3 bước → một bằng chứng → tên. Thanh cam chạy qua mọi cảnh, chữ cũ ra xong chữ mới mới vào | 8 s, cảnh ở 0 / 1,3 / 2,5 / 4,6 / 6 s | `van-de` `minh-lam` `buoc-1..3` `bang-chung` `ten` |
| Công thức từng bước | `cong-thuc-tung-buoc` | Món ăn, mỹ phẩm, quy trình "bỏ vào → ra kết quả": ly đầy dần từng lớp, nhãn định lượng ngang lớp | 5 s, lớp vào ở 0,5 / 1,2 / 1,9 s | `tieu-de` `tp-1..3` `ket-qua` |
| Hình biến giao diện | `hinh-bien-giao-dien` | Một khối duy nhất đổi hình nút → vòng tải → dấu tích → thẻ kết quả, không cắt cảnh. Hợp quảng cáo app, đặt lịch, đặt hàng | 5 s, đổi ở 1,1 / 2 / 2,8 s | `nut` `ket-qua` `chi-tiet` |

**Không làm thành thẻ:** nhân vật hoạt hình 3D hóa thân chủ kênh (Ngô Bằng). Việc này cần dịch vụ tạo hình AI trả phí, nên phải hỏi người dùng trước. Dùng skill `viet-prompt-video-ai` để viết prompt, cuối prompt luôn có dòng "không chữ, không phụ đề".

Ba thẻ cuối học từ 703 prompt video Opus 5.5, xem [hoc-tu-prompt-opus.md](hoc-tu-prompt-opus.md).

## Nhịp chuẩn đo từ 86 video (đặt thẻ cho khớp)

- Mỗi cảnh **1,5–2,5 giây**. Khoảng 2/3 số lần cắt là cắt thẳng. Chuyển mềm **dưới 0,4 giây**.
- Thẻ vào trong **0,15–0,35 giây**. Chữ cuối giữ ít nhất 2 giây (cảnh báo `line_unread`).
- 3 giây đầu: tiêu đề có ngay khung 0, không chào hỏi. 2/3 video có con số ngay 3 giây đầu.
- Không đặt tiếng "vút" ở mọi thẻ. Chỉ dùng ở chỗ đổi phần hoặc khi hiện số.
- **Cắt nhanh hơn không làm tăng lượt xem** (10 video nhiều lượt xem nhất: 1,8 s/cảnh, bằng nhóm còn lại). Nội dung quyết định.

## Học thêm khi xem kỹ 50 video (15/11/2026, chưa có thẻ)

Mỗi video được xem trọn từng khung (20 video nhiều lượt xem nhất và 30 video còn lại). Đây là các kỹ thuật chưa có thẻ. Khi cần, làm thẻ mới theo luật ở dưới.

| Kỹ thuật | Dùng khi | Gần với thẻ |
|---|---|---|
| Chữ khổng lồ quét ngang khung rồi thu nhỏ thành một dòng danh sách | Nhấn một con số hoặc từ khóa ("20 TRIỆU/THÁNG", "TUỔI DÊ") | `so-dem-chay` |
| Lóe sáng (light leak) cam/vàng 0,3–0,5 s | **Chỉ ở chỗ đổi phần**, 1–2 lần mỗi video, không đặt giữa câu | — |
| Xé giấy mở sang nền họa tiết có khung điện thoại, ra lại bằng lỗ giấy rách | Vào phần ví dụ hoặc demo | `khung-dien-thoai` |
| Khung ngắm 4 góc vuông bao quanh ảnh mẫu | "Nhìn vào đây" trước khi so sánh trước/sau | `khoanh-tay` |
| Chữ cong theo vòng cung trên đầu người nói | Câu đánh giá ngắn ("khá là phèn") | — |
| Nhãn tên cột bay ra quanh một bảng, cộng dồn tới khi kín | Giải thích bảng tính, lịch đăng bài | `o-hoi-lat` |
| Chữ nhân bản bay kín khung đúng **một** lần | Con số tiền, câu kết | — |
| Lưới storyboard 9–12 ô xen kẽ với cảnh thành phẩm | Khoe quy trình: bản vẽ khớp thành phẩm | `chia-doi` |

- **Kém lượt xem thường do thân video dài và đơn điệu, không do thiếu hiệu ứng.** Ví dụ: 90 s quay màn hình tài liệu, không phóng to, không nhãn bước. Quay màn hình phải phóng vào dòng đang nói, có nhãn bước, mỗi đoạn ≤ 5 s.
- Mỗi kênh có **một chữ ký lặp ở mọi video** (chữ rơi kín khung ở cuối; cua pixel + xé giấy). Chọn một chữ ký cho kênh mình và giữ nguyên.
- Ghi chú đầy đủ ở repo riêng `hoc-marketing` (`docs/xem-ky-20-video.md`, `docs/xem-ky-30-video.md`).

## Bộ đồ họa đài (khung ngang 1920×1080, 15/11/2026)

Học từ trailer, phóng sự và ident của Truyền hình Đồng Tháp (`hieu-ung-video/references/intro-truyen-hinh.md`). Dùng màu ATT có sẵn trong `do-hoa/src/chung.tsx`: navy, vàng, chữ ATT đỏ – xanh lá – xanh dương. Thẻ có `data-resolution="landscape"`; `render_mau.py` tự đổi ảnh soi sang khung ngang.

| Thẻ | Dùng khi | Thời lượng | Biến |
|---|---|---|---|
| `dai-lower-third` | Tên + chức vụ người phát biểu, đặt ở 65,5% chiều cao như luật ATT | 5 s, vào xong 0,8 s | `ten` `chuc-vu` |
| `dai-chu-chay` | Băng chữ chạy dưới màn hình, nhãn đỏ cố định, chữ chạy đều 300 px/giây | 6 s | `nhan` `noi-dung` |
| `dai-logo-goc` | Logo ATT NEWS góc trên phải + tên bản tin + giờ, vệt sáng lướt qua ở 1,6 s | 4 s | `ten-ban-tin` `gio` |
| `dai-gio-phat-song` | Thẻ lịch phát sóng: tên chương trình, tập, giờ rất to, ngày; đứng yên 4,5 s cho kịp đọc | 6 s | `ten-chuong-trinh` `tap` `gio-phat` `ngay` |
| `dai-ident` | Ident kênh gắn cuối mọi video: nét sáng vẽ chữ → khối chữ trượt chéo → lóe → logo 3 màu → icon mạng xã hội → tên kênh gõ dần | 8 s | `ten-kenh` `mxh-1..4` |
| `dai-tai-tro` | Hàng nhà tài trợ: mỗi ô vào một kiểu (lật, phóng, trượt), vệt sáng lướt qua từng ô | 6 s | `tieu-de` `tai-tro-1..3` |
| `dai-diem-tin` | Đầu bản tin: tiêu đề + 4 tít nổi bật có số thứ tự, vào cách nhau 0,6 s | 8 s | `tieu-de` `tin-1..4` |
| `dai-chuyen-muc` | Bumper 3 s giữa các mục ("NÔNG NGHIỆP"…); khối màu quét chéo, tên mục đập vào | 3 s | `ten-muc` `phu` |
| `dai-dinh-vi` | Góc trên trái lúc vào phóng sự: ghim + địa điểm + ngày | 4 s | `dia-diem` `thoi-gian` |
| `dai-trich-dan` | Trích lời phát biểu toàn khung: ô ảnh người nói, ngoặc kép vàng, lời hiện dần, tên + chức danh | 6 s | `loi` `nguoi` `chuc-danh` |
| `dai-e-kip` | Cuối phóng sự: "THỰC HIỆN" + 3 dòng ê-kíp | 6 s | `tieu-de` `dong-1..3` |
| `dai-tiep-theo` | Trước giờ nghỉ / cuối chương trình: "TIẾP THEO" + nội dung + lời hẹn gõ dần | 5 s | `nhan` `noi-dung` `hen` |
| `dai-gia-nong-san` | Bảng giá 4 mặt hàng, mũi tên tăng (xanh) / giảm (đỏ) vẽ bằng CSS; đổi class `tang`/`giam` theo giá thật | 8 s | `tieu-de` `ngay` `mat-hang-1..4` `gia-1..4` |
| `dai-dem-nguoc` | Màn chờ: vòng tròn rút dần, số đếm lùi 7 → 0 theo thời gian timeline (tua được) | 8 s | `nhan` `ten-ct` |
| `dai-tin-nong` | Tin khẩn: nền đỏ, nhãn nhấp nháy 2 lần, tít lớn, băng vàng | 5 s | `nhan` `tit` `bang` |
| `dai-hai-khung` | Kết nối trường quay + hiện trường. Lòng khung để trống: xuất `--trong-suot`, đặt 2 video vào ô x 100/970, y 200, 850×480 | 6 s | `nhan-1` `ten-1` `nhan-2` `ten-2` |
| `dai-dien-thoai` | Phỏng vấn qua điện thoại: ô ảnh tròn, biểu tượng máy rung, sóng âm 7 cột | 6 s | `nhan` `ten` `chuc-danh` |
| `dai-thoi-tiet` | Thời tiết 4 vùng: biểu tượng nắng / mưa vẽ bằng CSS, nhiệt độ | 7 s | `tieu-de` `vung-1..4` `nhiet-1..4` |

**Chuẩn quốc tế đã áp (EBU R95, ITU-R BT.1848):** ở khung 1920×1080, mọi chữ và logo nằm trong **vùng an toàn đồ họa 90%**, tức cách mép trái/phải ≥ 96 px, trên/dưới ≥ 54 px. Nền và băng màu được tràn ra mép (vùng an toàn hành động 93%: 67/38 px). Ngày 15/11 đã kéo 4 thẻ vào trong vùng này: logo góc, định vị, băng chữ chạy, hai khung. Âm thanh phát sóng: châu Âu EBU R128 −23 LUFS, đỉnh −1 dBTP; Mỹ ATSC A/85 −24 LKFS. Chuẩn ở Việt Nam chưa xác minh: hỏi đài nhận bài.

- **Không thay bản ATT đang dùng.** Bản tin ATT NEWS vẫn dùng lower-third Remotion và kết tia laser (`tan_studio do-hoa`). Theo luật phong cách ATT phải "áp dụng y nguyên". Bộ thẻ này dùng cho khách khác, chương trình mới, hoặc khi Tân muốn đổi.
- `dai-tai-tro` đang dùng chữ thay logo. Có logo thật thì đặt ảnh vào ô, giữ hiệu ứng.
- Xuất `--trong-suot` để đắp lên video bằng ffmpeg (lower-third, chữ chạy, logo góc). Thẻ toàn khung (giờ phát sóng, ident, tài trợ) tự có nền.
- **Ô chữ phải rộng hơn chữ ở cỡ lớn nhất.** `dai-ident` lần đầu bị lỗi `text_occluded`: chữ "NEWS" 104 px rộng 345 px trong ô 290 px, lấn sang ô ATT. Đã hạ cỡ chữ xuống 86 px, nới ô lên 340 px. Lớp lóe trắng và khối trượt che chữ là cố ý: đánh dấu `data-layout-allow-occlusion` ngay trên lớp che.
  Cùng lỗi với số đếm: "00:03" cỡ 200 px rộng ~560 px trong vòng tròn chỉ có lòng 440 px, nên đè lên vòng. Bộ kiểm không bắt được lỗi này, phải soi ảnh mới thấy. Đã hạ xuống 130 px.
- **Chữ trên ô trong suốt đặt trên nền sáng dễ trượt chuẩn tương phản.** `dai-thoi-tiet` lần đầu chỉ đạt 2,91:1 (chuẩn tối thiểu 3:1). Đã làm ô đậm hơn (độ đục 0,82) và nền tối hơn.

## Luật riêng của nhóm thẻ này (học từ lúc làm)

- **Chữ vàng không đặt trực tiếp trên nền xám hoặc video sáng.** Bộ kiểm báo tương phản 2,3:1. Đặt chữ vàng trên băng hoặc khối đen (`tieu-de-mo-dau`, `so-muc-to`).
- **Chữ mờ phía sau làm bằng nét viền** (`color: transparent; -webkit-text-stroke`) kèm `data-layout-allow-overlap`. Chữ tô đặc màu tối sẽ bị báo lỗi tương phản 1,37:1. Chữ mờ phải nằm ngoài vùng tiêu đề.
- **Nét SVG vẽ dần dùng đầu tròn thì còn để lại một chấm** trước khi vẽ. Ẩn nét (`opacity: 0`) tới đúng lúc bắt đầu vẽ (`khoanh-tay`).
- **Số đếm:** con số nằm trong biến ẩn `so-cuoi`, chữ số hiển thị cập nhật bằng `onUpdate`. Số dài phải vừa thẻ, nếu không bộ kiểm báo `text_box_overflow`.
- Chữ gõ dần và con trỏ nháy: dùng `clipPath: inset(...)` với `ease: "steps(n)"`. Nháy một số lần cố định, không `repeat: -1`.
- **Đổi hình một khối bằng `clipPath: inset(... round R)`**, không tween `width`/`height` (`hinh-bien-giao-dien`). Dấu tích vẽ bằng hai cạnh viền xoay 45°, không dùng ký tự ✓ (dễ rơi sang font khác).
- **Chữ cam sáng trên nền kem chỉ đạt 2,3:1**, dùng cam đậm `#b94a10` (`giai-thich-5-canh`).
- Thẻ toàn khung (`khung-dien-thoai`, `chia-doi`, `the-kien-thuc`, `chu-ma-nen`, `giai-thich-5-canh`) tự có nền. Xuất `--trong-suot` vẫn chạy được nhưng nền thẻ vẫn còn.

## Kiểm

`python scripts/render_mau.py <ten>` (chạy từ thư mục skill): `check` phải 0 lỗi, xem ảnh 4 khung và `<ten>.chu.png`.
Render **từng thẻ một** để máy không nóng.
