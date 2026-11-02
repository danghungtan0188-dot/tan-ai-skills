# Space/Orbit

**Trông thế nào:** trời sao, hành tinh có vành, vệ tinh bay quanh trên quỹ đạo dẹt. Rộng lớn và chậm.

**Dùng khi:** tầm nhìn, khởi đầu mới, ra mắt, công nghệ, giáo dục khoa học. **Tránh:** nội dung nhiều chữ, tin ngắn.

**Màu:** đêm `#0a0f2c`, cam `#ff9d4d`, cam đậm `#d9602a`, vành `#ffd9a8`, xanh `#6fd3ff`, trắng. **Font:** Montserrat VN 900 (tiêu đề), 500 (dòng phụ).

**Chữ ký chuyển động:** chậm và rộng bằng `power2.out`. Hệ hành tinh phóng to từ xa. Vệ tinh chạy theo góc bằng `cos`/`sin` trong `onUpdate` của tween, nên tính theo thời gian và render lại vẫn giống hệt. Nửa trên của hành tinh (`#sp-che`) vẽ đè lên vành để vành có vẻ vòng ra phía sau.

**Thẻ mẫu:** `assets/mau/space-orbit/index.html`. **Biến:** `tieu-de`, `phu`.

**Câu lệnh mẫu:**

> Thêm thẻ Space lúc mình nói "[câu nói]": tiêu đề "[tiêu đề]", dòng phụ "[dòng phụ]". Đặt trên đầu, không đè mặt.

**Kiểm:** vệ tinh có di chuyển giữa các khung; vành bị hành tinh che ở nửa sau; tiêu đề nằm gọn một dòng (khoảng 15 ký tự).
