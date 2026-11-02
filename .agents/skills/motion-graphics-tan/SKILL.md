---
name: motion-graphics-tan
description: Thư viện phong cách motion graphics cho thẻ, title, số liệu trong video — mỗi phong cách có bảng màu, font hỗ trợ tiếng Việt, chữ ký chuyển động GSAP và thẻ mẫu HyperFrames đã render thật. Hiện có Swiss, Kinetic Type, Pop Art, Glassmorphism, Editorial. Kích hoạt khi người dùng muốn thẻ/title/motion graphic theo một phong cách ("kiểu Swiss", "chữ động", "pop art", "kính mờ", "kiểu báo chí"), hỏi nên chọn phong cách nào, hoặc muốn video chuyển động đẹp hơn. Không dùng để cắt ghép hay thêm phụ đề (video-use, bien-tap-video-thong-minh-song-ngu-tan); hiệu ứng theo câu nói đặt sau người thì kết hợp với video-marketing.
---

# Motion graphics theo phong cách

Một skill, nhiều công thức: mỗi phong cách là một file trong `references/phong-cach/` và một thẻ mẫu trong `assets/mau/<ten>/index.html`.

## Chọn phong cách

| Nội dung | Phong cách | Công thức |
|---|---|---|
| Bản tin, phóng sự, chủ đề nghiêm túc | Editorial | [editorial.md](references/phong-cach/editorial.md) |
| Số thứ tự, giới thiệu chương, thông tin rõ ràng | Swiss | [swiss.md](references/phong-cach/swiss.md) |
| Câu khẩu hiệu, mở đầu video ngắn | Kinetic Type | [kinetic-type.md](references/phong-cach/kinetic-type.md) |
| Khuyến mãi, tin vui, video bán hàng | Pop Art | [pop-art.md](references/phong-cach/pop-art.md) |
| App, công nghệ, số liệu trên giao diện | Glassmorphism | [glassmorphism.md](references/phong-cach/glassmorphism.md) |

Không rõ thì chọn theo độ nghiêm túc của chủ đề. **Pop Art và Kinetic Type không hợp tin buồn, phim tài liệu.**

## Quy trình

1. Đọc công thức của phong cách, chép thẻ mẫu sang dự án, đổi nội dung qua biến (`data-var-text`).
2. Kiểm và xem: `python scripts/render_mau.py <ten>` (chạy từ thư mục skill) → `check` phải 0 lỗi, rồi **mở ảnh 4 khung ra xem** — chữ có đủ dấu không, màu có đúng không.
3. Đặt lên video người nói: `python scripts/render_mau.py <ten> --trong-suot` ra `.webm` nền trong suốt, rồi `ghep_lop.py` của skill `video-marketing`.

## Luật khi viết thẻ

- **Tên biến nội dung không được trùng tên biến CSS.** Biến `nhan` đè lên `--nhan` làm mất màu mà render vẫn chạy (lỗi thật ở thẻ Editorial).
- Chỉ dùng font có bộ chữ tiếng Việt và kiểm bằng mắt: Inter, Montserrat, Playfair Display đã kiểm. Archivo Black không có tiếng Việt.
- Thẻ đặt nửa trên khung (`top: 170px`, cao 1000px), là vị trí "trên đầu người nói".
- Thẻ mẫu dài 3 giây để xem nhanh. Dùng thật thì chỉnh thời lượng theo câu nói, dòng chữ cuối giữ ít nhất 2 giây (cảnh báo `line_unread`).
- Cảnh báo `first_frame_empty` và `nested_structure_needs_subcomposition` được chấp nhận ở thẻ phủ lên video.
- **Chỉ render trên máy.** Không dùng `hyperframes cloud render` (dịch vụ trả phí) khi người dùng chưa đồng ý.
- Học phong cách và kỹ thuật, không chép thiết kế, hình, chữ của người khác.

## Lộ trình 20 phong cách

- **Đợt 1 (đã có, đã render):** Swiss, Kinetic Type, Pop Art, Glassmorphism, Editorial.
- **Thấy trong reel, chưa làm:** Flat 2D, Clay 3D, Space/Orbit, Pixel 8-bit, Globe 3D, Chrome, Synthwave, Bauhaus, Gradient UI.
- **Đề xuất thêm, chưa làm:** Neo-brutalism, Doodle vẽ tay, Paper cut/collage, Neon glow, Minimal sang trọng, Isometric 3D.
