# Neon glow

**Trông thế nào:** bảng đèn ống trên tường tối. Lõi chữ gần trắng, quầng sáng màu quanh chữ, khung đèn phát sáng cả trong lẫn ngoài.

**Dùng khi:** quán, sự kiện tối, giải trí, thông báo giờ mở cửa. **Tránh:** tin tức, nền video sáng.

**Màu:** tường `#0d0a1a`, hồng `#ff3fa4`, xanh neon `#22e6ff`, vàng `#ffe66d`, lõi `#fff5fb`. **Font:** Tilt Neon VN.

**Chữ ký chuyển động:** bật đèn ống. Từng phần chớp vài lần tại các mốc cố định bằng `tl.set` rồi sáng hẳn, sau đó thở nhẹ (`sine.inOut`, số lần lặp cố định). Quầng sáng là nhiều lớp `text-shadow`.

**Thẻ mẫu:** `assets/mau/neon-glow/index.html`. **Biến:** `dong1`, `dong2`, `phu`.

**Câu lệnh mẫu:**

> Thêm thẻ neon lúc mình nói "[câu nói]": dòng lớn "[dòng 1]", dòng vừa "[dòng 2]", dòng nhỏ "[dòng phụ]". Đặt trên đầu, không đè mặt.

**Kiểm:** lõi chữ gần trắng (chữ màu đậm không ra chất đèn); dòng lớn tối đa khoảng 9 ký tự để nằm gọn trong khung; chớp không quá 0,4 giây mỗi phần.
