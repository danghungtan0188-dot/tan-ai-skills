# Synthwave

**Trông thế nào:** retro thập niên 80. Mặt trời sọc ngang, lưới phối cảnh chạy về phía người xem, chữ neon.

**Dùng khi:** âm nhạc, sự kiện đêm, giải trí, game. **Tránh:** tin tức, chủ đề nghiêm túc.

**Màu:** tím đậm `#1a0b3b`, tím `#4a1a8c`, hồng `#ff2e93`, cam `#ffb347`, neon `#19e6f0`. **Font:** Montserrat VN 900 nghiêng (tiêu đề), 700 (dòng phụ).

**Chữ ký chuyển động:** lưới chạy đều (`ease: none`), quãng đường là bội số của ô lưới (48px) để nếu lặp thì không bị giật. Mặt trời mọc bằng `power2.out`. Tiêu đề bật sáng rồi chớp một lần như đèn neon.

**Thẻ mẫu:** `assets/mau/synthwave/index.html`. **Biến:** `tieu-de`, `phu`.

**Câu lệnh mẫu:**

> Thêm thẻ Synthwave lúc mình nói "[câu nói]": tiêu đề "[ĐÊM NHẠC]", dòng phụ "[thời gian, địa điểm]". Đặt trên đầu, không đè mặt.

**Kiểm:** ô lưới nhỏ (ô to thì phối cảnh vỡ thành vài vạch); dấu dưới của tiêu đề không chạm dòng phụ; chữ neon dùng màu đặc + `text-shadow`, không dùng `background-clip: text`.
