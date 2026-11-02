# Gradient UI

**Trông thế nào:** nền chuyển màu tím hồng cam, thẻ giao diện trắng bo góc, con số lớn, biểu đồ cột với cột cuối nổi bật.

**Dùng khi:** báo cáo số liệu, phần mềm, tăng trưởng, kết quả chiến dịch. **Tránh:** chủ đề truyền thống, tin buồn.

**Màu:** tím `#5b21d6`, hồng `#e0359b`, cam `#ff8a4c`, trắng, mực `#1d1433`, xám `#6a6280`, cột thường `#dcd3f5`. **Font:** Inter VN 900 (số), 700 (tiêu đề), 400 (dòng phụ).

**Chữ ký chuyển động:** sạch và chắc bằng `power3.out`. Thẻ trượt lên, chữ hiện so le, các cột mọc lần lượt bằng `scaleY`, cột nổi bật vào sau cùng.

**Thẻ mẫu:** `assets/mau/gradient-ui/index.html`. **Biến:** `tieu-de`, `so`, `phu`. Chiều cao cột sửa trong CSS (`#gu-c1` … `#gu-c5`).

**Câu lệnh mẫu:**

> Thêm thẻ số liệu lúc mình nói "[câu nói]": tiêu đề "[tiêu đề]", con số "[+38%]", dòng phụ "[so với kỳ nào]". Số liệu các cột: [5 số]. Đặt trên đầu, không đè mặt.

**Kiểm:** con số và chiều cao cột khớp số liệu thật, không để cột mẫu khi đã có số thật; cột nổi bật là cột cần nhấn.
