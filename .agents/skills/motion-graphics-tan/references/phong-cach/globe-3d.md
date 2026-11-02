# Globe 3D

**Trông thế nào:** quả địa cầu giả lập bằng CSS. Dải lục địa trượt ngang sau mặt nạ tròn, lớp sáng tối phủ trên tạo khối cầu, quầng xanh quanh viền. Không dùng WebGL.

**Dùng khi:** thị trường, mạng lưới, số quốc gia, kết nối. **Tránh:** cần bản đồ chính xác: lục địa ở đây chỉ mang tính trang trí. Bản đồ thật dùng skill `ban-do-video` hoặc `remotion-maps`.

**Màu:** đêm `#06122b`, biển `#1769c7`, đất `#3fbf7f`, quầng `#58c4ff`, trắng. **Font:** Inter VN 900 (tiêu đề), 700 (con số).

**Chữ ký chuyển động:** quả cầu quay đều: dải lục địa dài gấp đôi trượt ngang (`ease: none`), hai nửa dải giống nhau để có thể lặp. Phóng to êm bằng `power3.out`, chữ hiện sau.

**Thẻ mẫu:** `assets/mau/globe-3d/index.html`. **Biến:** `tieu-de`, `so`.

**Câu lệnh mẫu:**

> Thêm thẻ quả địa cầu lúc mình nói "[câu nói]": tiêu đề "[tiêu đề]", con số "[12 quốc gia]". Đặt trên đầu, không đè mặt.

**Kiểm:** con số là số thật; không dùng thẻ này để chỉ một địa điểm cụ thể (lục địa không đúng hình thật).
