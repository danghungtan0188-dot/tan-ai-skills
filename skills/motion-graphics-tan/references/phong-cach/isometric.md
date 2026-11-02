# Isometric 3D

**Trông thế nào:** góc nhìn nghiêng cố định, các tấm xếp chồng rồi tách lớp, có đường kẻ và nhãn cho từng lớp. Dùng phép biến đổi CSS, không WebGL.

**Dùng khi:** giải thích cấu trúc, các lớp của sản phẩm, hệ thống, quy trình. **Tránh:** hơn 4 lớp (nhãn sẽ chật).

**Màu:** nền `#f1f3fb`, lam `#3454d1`, hồng `#e83f6f`, vàng `#ffbf00`, mực `#171a2b`. Mỗi tấm có bóng cứng tối hơn cùng tông để tạo độ dày. **Font:** Montserrat VN 900 (tiêu đề), 800 (nhãn).

**Chữ ký chuyển động:** các tấm bung theo trục `z` bằng `power3.inOut`, sau đó kẻ và nhãn hiện lần lượt từ trên xuống. Góc nhìn đặt bằng CSS ở phần tử cha `#is-san` (`rotateX(58deg) rotateZ(45deg)`), GSAP chỉ động vào các tấm con.

**Thẻ mẫu:** `assets/mau/isometric/index.html`. **Biến:** `tieu-de`, `lop1`, `lop2`, `lop3`.

**Câu lệnh mẫu:**

> Thêm thẻ isometric lúc mình nói "[câu nói]": tiêu đề "[tiêu đề]", ba lớp "[lớp 1; lớp 2; lớp 3]". Các lớp tách ra lúc mình nói "[từ]". Đặt trên đầu, không đè mặt.

**Kiểm:** đường kẻ chỉ đúng tấm của nó; nhãn tối đa khoảng 10 ký tự để không tràn thẻ; các tấm không dính vào nhau khi đã tách.
