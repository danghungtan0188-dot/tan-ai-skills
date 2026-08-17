# Dữ liệu đầu vào: Excel/CSV sản phẩm + thư mục ảnh

## Cột dữ liệu

| Cột | Bắt buộc | Ý nghĩa |
|---|---|---|
| `ma_san_pham` | Có | Mã định danh duy nhất, dùng để tra cứu và đặt tên file xuất (vd. `SP001`). |
| `ten_san_pham` | Có | Tên sản phẩm hiển thị trong kịch bản/overlay. |
| `mo_ta_ngan` | Có | Mô tả ngắn 1–2 câu, dùng làm chất liệu chính viết kịch bản. |
| `gia` | Có | Giá bán, giữ nguyên định dạng người dùng nhập (vd. `199.000đ`) — không tự quy đổi/làm tròn. |
| `ten_file_anh` | Có | Tên file ảnh trong thư mục ảnh, nhiều ảnh cách nhau bằng `;` (vd. `sp001_1.jpg;sp001_2.jpg`). |
| `tinh_nang_chinh` | Không | Tính năng/điểm bán nổi bật, cách nhau bằng `;`. |
| `gia_khuyen_mai` | Không | Giá sau khuyến mãi, nếu có. Không có thì kịch bản không nhắc khuyến mãi. |
| `cta` | Không | Lời kêu gọi hành động mong muốn (vd. "Nhắn tin đặt hàng", "Mua ngay tại shop"). Trống thì dùng CTA mặc định trung tính, nêu rõ với người dùng đây là CTA tự đề xuất. |
| `giong_doc` | Không | Ghi đè giọng đọc riêng cho sản phẩm này (nam/nữ/tên giọng nhân bản), nếu khác giọng mặc định đã chọn ở đầu phiên. |
| `ghi_chu` | Không | Ghi chú tự do, không đưa vào kịch bản trừ khi người dùng yêu cầu. |

## Định dạng file

- **CSV**: mã hoá UTF-8 có BOM để Excel mở đúng tiếng Việt (cùng quy ước với skill `marketing`). Đọc bằng `scripts/doc_du_lieu_san_pham.py`.
- **XLSX**: script đọc trực tiếp bằng thư viện chuẩn Python (`zipfile` + `xml.etree`), không cần cài `openpyxl`. Giới hạn: chỉ đọc **sheet đầu tiên**, không hỗ trợ ô gộp (merged cells) hoặc công thức — nếu file có công thức, mở Excel và "Paste as values" trước, hoặc xuất CSV.

## Thư mục ảnh

- Truyền đường dẫn thư mục ảnh riêng, tên file trong cột `ten_file_anh` phải khớp chính xác (phân biệt hoa/thường tuỳ hệ điều hành).
- Script `doc_du_lieu_san_pham.py` đối chiếu và báo rõ ảnh nào không tìm thấy — không tự thay bằng ảnh khác trong thư mục.
- Ảnh nên có độ phân giải đủ lớn để crop/zoom (Ken Burns) mà không vỡ nét — tối thiểu chiều dài cạnh ngắn ≥ 1080px cho khung dọc TikTok.

## Cách dùng script cho một sản phẩm cụ thể

```bash
# Tra 1 sản phẩm theo mã, đối chiếu ảnh trong thư mục
python skills/video-san-pham/scripts/doc_du_lieu_san_pham.py duong-dan/san-pham.csv \
  --ma-san-pham SP001 --images-dir duong-dan/anh-san-pham

# Không nhớ mã, tra theo tên gần đúng
python skills/video-san-pham/scripts/doc_du_lieu_san_pham.py duong-dan/san-pham.xlsx \
  --ten-san-pham "Mật ong rừng" --images-dir duong-dan/anh-san-pham

# Xem toàn bộ danh sách để chọn (không xử lý gì thêm)
python skills/video-san-pham/scripts/doc_du_lieu_san_pham.py duong-dan/san-pham.csv --list
```
