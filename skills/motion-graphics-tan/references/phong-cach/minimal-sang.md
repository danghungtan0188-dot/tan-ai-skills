# Minimal sang trọng

**Trông thế nào:** nền tối, vàng đồng màu đặc, chữ có chân thanh mảnh, viền mảnh, rất nhiều khoảng trống.

**Dùng khi:** sản phẩm cao cấp, lễ kỷ niệm, trao giải, thư mời. **Tránh:** khuyến mãi ồn ào, nội dung nhiều chữ.

**Màu:** đêm `#0e0d0b`, vàng `#e0b93b`, ngà `#f2ead8`. **Font:** Playfair VN 400 và nghiêng (tiêu đề), Inter VN 400 (dòng nhỏ, dòng phụ).

**Chữ ký chuyển động:** chậm và êm bằng `power2.out`, không nảy. Khung hiện mờ dần, chữ lớn trôi lên từ sau mặt nạ. **Không tween `letterSpacing`:** chữ giật theo từng pixel, bộ kiểm báo lỗi `gsap_non_transform_motion`.

**Thẻ mẫu:** `assets/mau/minimal-sang/index.html`. **Biến:** `nho`, `dong1`, `dong2`, `phu`.

**Câu lệnh mẫu:**

> Thêm thẻ tối giản sang trọng lúc mình nói "[câu nói]": dòng nhỏ "[BỘ SƯU TẬP MỚI]", tiêu đề hai dòng "[dòng 1 / dòng 2]", dòng phụ "[dòng phụ]". Đặt trên đầu, không đè mặt.

**Kiểm:** chữ nhỏ không dưới 34px (nhỏ hơn thì khó đọc trên điện thoại, cảnh báo `text_below_floor`); không dùng chữ vàng gradient: chỉ dùng màu đặc.
