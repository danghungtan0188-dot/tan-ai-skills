# Tiêu đề kiểu "title preset" (12 kiểu chữ nhiều lớp)

Thẻ mẫu: `assets/tieu-de-preset/index.html`. Công cụ: `scripts/render_tieu_de.py`.
Học **thể loại** chữ tiêu đề nhiều lớp đang thịnh trên CapCut, Reels (chữ viết tay đè lên chữ in đậm, chuyển màu, viền dày, phát sáng, nổi khối), **không chép mẫu của gói preset bán có phí**. Màu, chữ, bố cục là của mình.

## Cấu trúc

| Lớp | Biến | Font |
|---|---|---|
| Chữ nhấn viết tay, nghiêng, đè góc trên trái | `nhan` | Dancing Script, Great Vibes, Pacifico, Lobster |
| Chữ chính in đậm, vẽ bằng SVG (chuyển màu, viền, sáng, nổi khối) | `chinh` | Anton, Bungee, Paytone One, Oswald |
| Dòng phụ nhỏ, lệch phải | `phu` | Oswald, Paytone One |

Font trong `assets/tieu-de-preset/fonts/` (Google Fonts, OFL, đủ dấu tiếng Việt, đặt tên đuôi ` VN`). Chữ chính tự co cho vừa 84% chiều ngang khung.

## 12 kiểu

| Kiểu | Dùng khi | Vào |
|---|---|---|
| `vang-kim` | Tên chương trình, tiêu đề bản tin | Bật lên |
| `neon` | Sự kiện đêm, ca nhạc | Chớp neon |
| `bang-do` | Tin nóng, tin khẩn | Băng đỏ quét |
| `noi-khoi` | Mẹo, bí quyết, hướng dẫn | Đập xuống + rung |
| `vien-doi` | Kỹ năng, bài học | Vẽ viền rồi đổ màu |
| `sang-trong` | Lễ kỷ niệm, thư mời | Trôi lên chậm |
| `sale-nong` | Khuyến mãi, giảm giá | Đập + tia bung |
| `xanh-tuoi` | Nông sản, môi trường | Bật lên |
| `bang-mau` | Chuyên đề, chuyên mục | Băng xanh quét |
| `chu-rong` | Mở chương, hành trình | Vẽ viền rồi mực dâng |
| `go-chu` | Mẹo, cảnh báo, kiến thức | Gõ từng chữ |
| `toc-do` | Thể thao, tốc độ | Trượt nghiêng |

Không hợp tin buồn: `neon`, `sale-nong`, `toc-do`, `noi-khoi`.

## Lệnh

```powershell
cd skills\motion-graphics-tan\scripts
python render_tieu_de.py --ds
python render_tieu_de.py --bang
python render_tieu_de.py vang-kim --nhan "Bản tin" --chinh "AN THẠNH THỦY" --phu "Thứ Năm, 27/11/2026"
python render_tieu_de.py sale-nong --chinh "50%" --png
python render_tieu_de.py bang-do --doc --giay 5
```

- `--bang`: 12 ảnh tĩnh ghép 4×3 trên nền xám để chọn kiểu. Dùng lệnh `snapshot` nên không render video.
- Mặc định: `.mov` ProRes nền trong suốt kèm tiếng động (`scripts/sfx`, −20 LUFS), kéo thẳng vào Premiere.
- `--png`: ảnh tĩnh trong suốt để làm thumbnail.

## Luật

- Không tween `filter` (hiệu ứng sáng, nổi khối là `filter` tĩnh trên SVG). Độ nghiêng đặt bằng `gsap.set`, không dùng CSS `transform` trên phần tử GSAP điều khiển.
- Không dùng `background-clip: text`. Chữ chuyển màu là SVG `<text>` với `linearGradient`.
- Dựng thẻ sau `document.fonts.ready`, đăng ký timeline ở cuối hàm async để đo chữ đúng font.
- Thêm kiểu mới: thêm 1 mục vào `KIEU` trong `index.html`, 1 dòng mẫu chữ vào `MAU_CHU` trong `render_tieu_de.py`, 1 dòng vào bảng trên.
