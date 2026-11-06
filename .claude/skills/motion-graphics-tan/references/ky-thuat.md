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

**Không làm thành thẻ:** nhân vật hoạt hình 3D hóa thân chủ kênh (Ngô Bằng). Việc này cần dịch vụ tạo hình AI trả phí, nên phải hỏi người dùng trước. Dùng skill `viet-prompt-video-ai` để viết prompt, cuối prompt luôn có dòng "không chữ, không phụ đề".

## Nhịp chuẩn đo từ 86 video (đặt thẻ cho khớp)

- Mỗi cảnh **1,5–2,5 giây**. Khoảng 2/3 số lần cắt là cắt thẳng. Chuyển mềm **dưới 0,4 giây**.
- Thẻ vào trong **0,15–0,35 giây**. Chữ cuối giữ ít nhất 2 giây (cảnh báo `line_unread`).
- 3 giây đầu: tiêu đề có ngay khung 0, không chào hỏi. 2/3 video có con số ngay 3 giây đầu.
- Không đặt tiếng "vút" ở mọi thẻ. Chỉ dùng ở chỗ đổi phần hoặc khi hiện số.
- **Cắt nhanh hơn không làm tăng lượt xem** (10 video nhiều lượt xem nhất: 1,8 s/cảnh, bằng nhóm còn lại). Nội dung quyết định.

## Luật riêng của nhóm thẻ này (học từ lúc làm)

- **Chữ vàng không đặt trực tiếp trên nền xám hoặc video sáng.** Bộ kiểm báo tương phản 2,3:1. Đặt chữ vàng trên băng hoặc khối đen (`tieu-de-mo-dau`, `so-muc-to`).
- **Chữ mờ phía sau làm bằng nét viền** (`color: transparent; -webkit-text-stroke`) kèm `data-layout-allow-overlap`. Chữ tô đặc màu tối sẽ bị báo lỗi tương phản 1,37:1. Chữ mờ phải nằm ngoài vùng tiêu đề.
- **Nét SVG vẽ dần dùng đầu tròn thì còn để lại một chấm** trước khi vẽ. Ẩn nét (`opacity: 0`) tới đúng lúc bắt đầu vẽ (`khoanh-tay`).
- **Số đếm:** con số nằm trong biến ẩn `so-cuoi`, chữ số hiển thị cập nhật bằng `onUpdate`. Số dài phải vừa thẻ, nếu không bộ kiểm báo `text_box_overflow`.
- Chữ gõ dần và con trỏ nháy: dùng `clipPath: inset(...)` với `ease: "steps(n)"`. Nháy một số lần cố định, không `repeat: -1`.
- Thẻ toàn khung (`khung-dien-thoai`, `chia-doi`, `the-kien-thuc`, `chu-ma-nen`) tự có nền. Xuất `--trong-suot` vẫn chạy được nhưng nền thẻ vẫn còn.

## Kiểm

`python scripts/render_mau.py <ten>` (chạy từ thư mục skill): `check` phải 0 lỗi, xem ảnh 4 khung và `<ten>.chu.png`.
Render **từng thẻ một** để máy không nóng.
