# Kinetic Type

**Trông thế nào:** chữ là hình ảnh chính. Các hàng chữ lặp lại, đặc xen rỗng ruột, trôi ngược chiều nhau, rồi một chữ chốt màu đỏ đập vào giữa.

**Dùng khi:** khẩu hiệu, mở đầu video ngắn, nhấn một ý. **Tránh:** câu dài, tin buồn.

**Màu:** nền `#0a0a0a`, chữ `#f5f5f0`, chốt `#ff3b30`. **Font:** Montserrat VN 900.

**Chữ ký chuyển động:** hàng chữ trôi đều (`ease: none`) suốt thời lượng. Chữ chốt thu từ `scale: 2.6` về 1 bằng `expo.out`, đồng thời các hàng tối xuống còn 28% để chốt nổi lên.

**Thẻ mẫu:** `assets/mau/kinetic-type/index.html`. **Biến:** `chot`. Chữ lặp sửa trực tiếp ở 6 thẻ `.kt-hang`.

**Câu lệnh mẫu:**

> Thêm thẻ Kinetic Type lúc mình nói "[câu nói]": chữ lặp "[2 từ]", chữ chốt "[2 từ]". Đặt trên đầu, không đè mặt.

**Kiểm:** chữ chốt nằm gọn trong thẻ ở khung cuối (tối đa khoảng 10 ký tự ở cỡ 118px); dấu tiếng Việt không dính vào hàng bên cạnh.
