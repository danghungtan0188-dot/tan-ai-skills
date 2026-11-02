# Editorial

**Trông thế nào:** trang báo. Giấy ngà, chữ có chân lớn, nhãn đỏ, đường kẻ kép, dòng cuối nghiêng màu đỏ.

**Dùng khi:** bản tin, phóng sự, chủ đề nghiêm túc. **Tránh:** video khuyến mãi ồn ào. Khi làm bản tin ATT NEWS, bộ thông số đã chốt trong `phong-cach-att-news.md` được ưu tiên hơn thẻ này.

**Màu:** giấy `#f6f1e7`, mực `#1a1714`, nhấn `#b3261e`. **Font:** Playfair VN 700 (tiêu đề), Inter VN 700 và 400 (nhãn, dòng phụ).

**Chữ ký chuyển động:** trang trọng, không nảy. Đường kẻ chạy ngang trước (`power3.inOut`), từng dòng trôi lên từ sau mặt nạ (`yPercent`, `power3.out`, `stagger`).

**Thẻ mẫu:** `assets/mau/editorial/index.html`. **Biến:** `tieu-muc`, `dong1`, `dong2`, `dong3`, `phu`. Không đặt tên biến `nhan`: nó đè lên màu `--nhan`.

**Câu lệnh mẫu:**

> Thêm thẻ kiểu báo chí lúc mình nói "[câu nói]": nhãn "[TIN NỔI BẬT]", tiêu đề 3 dòng "[dòng 1 / dòng 2 / dòng 3]", dòng phụ "[nguồn, ngày]". Đặt trên đầu, không đè mặt.

**Kiểm:** mỗi dòng tiêu đề tối đa khoảng 14 ký tự; dấu hỏi, dấu ngã trên chữ hoa không bị mặt nạ cắt; nhãn có nền đỏ.
