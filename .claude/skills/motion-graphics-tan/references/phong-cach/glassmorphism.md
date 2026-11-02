# Glassmorphism

**Trông thế nào:** tấm kính mờ trên các đốm màu sáng, viền sáng mỏng, chữ trắng sạch.

**Dùng khi:** giới thiệu app, công nghệ, số liệu dạng giao diện. **Tránh:** nền video sáng nhiều chi tiết (thẻ có nền tối riêng nên vẫn đọc được, nhưng trông nặng).

**Màu:** nền `#12122b`, đốm `#7c3aed`, `#06b6d4`, `#ec4899`, kính `rgba(255,255,255,0.14)`, viền `rgba(255,255,255,0.4)`. **Font:** Inter VN 900 (số), 700 (tên), 400 (dòng phụ).

**Chữ ký chuyển động:** mềm và chậm bằng `power3.out`, kính trượt lên, chữ hiện so le (`stagger`). Đốm màu trôi liên tục phía sau để thấy rõ độ mờ của kính. Thanh tiến độ chạy bằng `scaleX`.

**Thẻ mẫu:** `assets/mau/glassmorphism/index.html`. **Biến:** `ten`, `so`, `phu`. Đổi con số thì đổi cả `width` của `#gl-day` cho khớp.

**Câu lệnh mẫu:**

> Thêm thẻ kính mờ lúc mình nói "[câu nói]": tên "[tên]", số "[84%]", dòng phụ "[dòng phụ]". Đặt trên đầu, không đè mặt.

**Kiểm:** độ mờ `backdrop-filter` thấy rõ ở ảnh 4 khung; chữ trắng vẫn đọc được khi đốm màu sáng trôi qua.
