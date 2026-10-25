# Học từ OpenMontage và Diagram Design

Tóm tắt bằng lời của mình, đọc ngày 25/10/2026. Không chép code. Bản fork nằm trên GitHub
`danghungtan0188-dot/OpenMontage` và `danghungtan0188-dot/diagram-design`, chưa tải về máy.

## 1. OpenMontage — chỉ lấy ý tưởng, không dùng code

Repo `calesthio/OpenMontage`, giấy phép **AGPL-3.0**: chép code vào đây thì phải công khai cả repo,
nên **không chép**. Nó còn gọi dịch vụ trả phí (Veo, Kling, fal) và Blender — nặng máy, tốn tiền.

Điều đáng học, từ `pipeline_defs/documentary-montage.yaml`:

| Ý tưởng | Áp vào repo này |
|---|---|
| Tìm tư liệu miễn phí ở Pexels, Archive.org (kho Prelinger), NASA, Wikimedia Commons, Unsplash | Nguồn B-roll khi kho clip của người dùng thiếu cảnh. Kiểm giấy phép **từng** file trước khi dùng, ghi nguồn vào edit-plan |
| Mỗi "ô cảnh" trong kế hoạch được tả bằng danh từ + tính từ cụ thể, kèm 2–3 câu tìm kiếm ngắn | Khi `build_edit_plan` thiếu cảnh, ghi rõ ô cảnh cần gì để tìm cho trúng |
| Ít nhất 2 cảnh "đinh" (hero) được đánh dấu riêng | Chọn trước 2 cảnh mạnh nhất, đặt ở mở đầu và cao trào |
| Câu hỏi chủ đề gói trong **một** câu | Viết một câu này trước khi dựng phim tài liệu |
| Mỗi chặng (ý tưởng → kế hoạch cảnh → …) đều dừng chờ người duyệt, tối đa 3 lần sửa mỗi chặng | Giống bước DUYỆT edit-plan đang có |

**Không theo:** OpenMontage bắt buộc có nhạc nền cho phim tài liệu, ngược với phong cách
phim tài liệu đã chốt (không nhạc).

## 2. Diagram Design — nguyên tắc vẽ sơ đồ

Repo `cathrynlavery/diagram-design`, giấy phép MIT, 287 file (5 MB), 45 loại sơ đồ HTML/SVG.
Không chép cả bộ vì trùng với `do-hoa/`. Lấy nguyên tắc từ `skills/diagram-design/SKILL.md`,
dùng khi làm sơ đồ, quy trình, biểu đồ trong video:

- **Bớt là cách làm đẹp nhất.** Sơ đồ xong khi không bỏ được gì nữa, không phải khi đã thêm đủ.
- Mỗi khối là một ý riêng. Hai khối luôn đi cùng nhau thì gộp làm một.
- Mỗi đường nối phải mang thông tin. Bố cục đã cho thấy quan hệ thì bỏ đường nối.
- **Màu nổi chỉ cho 1–2 khối chính.** Tô 5 khối là mất điểm nhấn.
- **Quá 9 khối thì tách làm hai sơ đồ.** Độ dày vừa phải, người xem không cần chú thích mới hiểu.
- Trước khi vẽ, hỏi: người xem có hiểu nhanh hơn so với một câu nói hoặc một bảng không? Không thì đừng vẽ.
- Bảng màu mặc định của họ: nền `#f5f5f5`, chữ `#2d3142`, nhấn `#bf4520` (cam đất) — gần với tông
  nâu đồng của phim tài liệu, dùng thử được khi chưa có bảng màu riêng.
