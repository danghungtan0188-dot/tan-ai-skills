# Viết đề bài cho video "wow" dựng bằng code

Rút từ kho `yihui-dev/awesome-opus5-5-videos` (MIT; 703 prompt của các video viral làm bằng Claude Opus 5.5, xem kèm bản làm lại trên skillry.dev) + hậu trường video KOYO (10/2026). Dùng khi người dùng đưa một ý tưởng ngắn và muốn video "xịn", hoặc khi mình tự lập đề bài trước khi dựng.

## Kho làm bằng gì (đếm trên 703 mục)

`canvas` 267 · `svg` 183 · `threejs` 131 · `shader` 92 · `gsap` 86 · `css` 57 · `audio` 39 · hạt 17 · ảnh AI chỉ 6. Nhóm: motion graphics 369, 3D 117, giải thích 116, tương tác 101.
→ Video gây sốt gần như **toàn bộ vẽ bằng code, không dùng AI tạo video**; ảnh AI chỉ làm nhân vật/phông khi cần.

## Khung đề bài (học từ các prompt mạnh nhất)

Viết thành các mục rõ ràng (prompt "explainer sản phẩm" hay nhất kho dùng đúng các thẻ này):

1. **Đầu vào** — thứ cần có trước khi dựng: nội dung/số liệu thật, ảnh/clip, màu + font + màu nhấn của kênh, tỉ lệ khung (16:9 / 9:16 / 1:1), giọng đọc hoặc bài hát.
2. **Luật** — ràng buộc kỹ thuật và thẩm mỹ, ví dụ:
   - mọi chuyển động tính từ khung hình (`useCurrentFrame`), không hẹn giờ, không ngẫu nhiên không hạt giống;
   - **"một hình, không bao giờ cắt"** — mọi trạng thái là cùng một khối đổi kích thước/bo góc/màu, nội dung đổi bên trong (cách KOYO: mọi thứ mọc ra từ đường đỏ);
   - dữ liệu thật, không chữ giữ chỗ.
3. **Cấu trúc** — chuỗi cảnh viết bằng mũi tên (`logo → nút → … → logo`), **lưới nhịp** (ví dụ 120 BPM, "mỗi phách có một việc xảy ra").
4. **Chuyển động** — lò xo có vượt nhẹ; nội dung **vào sau khi khung bắt đầu biến hình, ra trước lần biến hình kế tiếp** để chữ không bao giờ đè nhau; nhòe ngắn khi chuyển; **không mờ thẳng từ đen sang màu nhấn**.
5. **Âm thanh** — nhạc/tiếng động tự tổng hợp bằng code được; **mọi cú cắt rơi đúng phách**.
6. **Tiêu chuẩn và phản mẫu** — nêu thước đo ("như studio motion design làm, không phải 'video AI'", "kiểu The Pudding / 3Blue1Brown: sắc nét, một ý hình thức mạnh mỗi cảnh, hệ thiết kế nhất quán") và **cái không muốn** ("không slop", "không Pixar", "không phải powerpoint tô màu").
7. **Quyền tự quyết** — "làm trọn từ đầu tới cuối, tự quyết, cuối cùng báo lại đã quyết gì" khi người dùng vắng; ngược lại thì **làm mẫu 10–20 giây trước** (quy trình KOYO).

## Nguyên tắc rút ra

- **Có tham chiếu**: dán link/clip mẫu, nói rõ học cái gì (màu, nhịp, kiểu chữ) — AI giỏi bắt chước.
- **Gọi đúng tên phong cách**: motion graphic, kinetic typography, vẽ tay, mực tàu, cắt giấy, origami/doodle, địa hình 3D, infinite zoom… Không biết tên thì chụp khung hình hỏi.
- **Một ý hình thức mạnh mỗi cảnh** + một hệ thiết kế xuyên suốt (KOYO: nét mảnh + hạt cam; mỗi điểm một ẩn dụ riêng).
- **Mô phỏng thật khi giải thích** ("bước ngẫu nhiên phải là bước ngẫu nhiên thật, không phải hình vẽ") và dùng số thật.
- **Xin bảng phong cách/nhân vật trước** khi có nhân vật (style sheet → nhân vật phụ → cảnh).
- **Tốn thời gian nhất là vòng duyệt**: hỏi bằng 4 câu (hình / âm thanh / chuyển cảnh / đủ wow chưa), sửa từng chặng.

## Mẫu đề bài ngắn cho video của kênh (điền vào)

```text
Làm video <thời lượng> <tỉ lệ> về <chủ đề>, cho <kênh/người xem>.
Tham chiếu: <link/clip> — học <màu/nhịp/kiểu chữ/chuyển cảnh>.
Phong cách: <tên phong cách>; một hệ hình xuyên suốt: <nét/khối/màu nhấn>; mỗi phần một ẩn dụ riêng.
Nội dung thật: <số liệu, tên, địa danh — nguồn>.
Âm thanh: <giọng đọc nào / nhạc / tiếng động>, cắt theo phách.
Không muốn: <slop, chữ đè, kết vội, ...>.
Làm mẫu 15 giây trước, tôi duyệt theo 4 câu rồi mới làm cả bài.
```
