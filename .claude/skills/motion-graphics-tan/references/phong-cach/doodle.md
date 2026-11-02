# Doodle vẽ tay

**Trông thế nào:** giấy kẻ, chữ viết tay, nét bút tự vẽ, ô tích và ngôi sao không thẳng hàng, tất cả rung nhẹ như hoạt hình vẽ tay.

**Dùng khi:** hướng dẫn các bước, checklist, vlog, nội dung gần gũi. **Tránh:** chủ đề trang trọng.

**Màu:** giấy `#fdfaf1`, kẻ `#cfe0ee`, bút `#24303f`, đỏ `#e4572e`, xanh `#2a9d8f`. **Font:** Patrick Hand VN.

**Chữ ký chuyển động:** nét tự vẽ bằng `strokeDashoffset` (đường SVG đặt `pathLength="1"`, `strokeDasharray: 1`). Rung kiểu "boil": đổi vị trí mỗi 1/8 giây bằng `tl.set`, lệch tối đa 3px theo danh sách cố định, không dùng `Math.random`.

**Thẻ mẫu:** `assets/mau/doodle/index.html`. **Biến:** `tieu-de`, `buoc1`, `buoc2`, `buoc3`.

**Câu lệnh mẫu:**

> Thêm thẻ Doodle lúc mình nói "[câu nói]": tiêu đề "[tiêu đề]", các bước "[bước 1; bước 2; bước 3]". Mỗi dấu tích tự vẽ lúc mình nói tới bước đó. Đặt trên đầu, không đè mặt.

**Kiểm:** tiêu đề một dòng (tối đa khoảng 18 ký tự); chữ bước 3 không chạm ngôi sao góc dưới; dấu tích hiện đúng thứ tự; rung nhẹ, không làm chữ khó đọc (chữ đứng yên, chỉ nét vẽ rung).
