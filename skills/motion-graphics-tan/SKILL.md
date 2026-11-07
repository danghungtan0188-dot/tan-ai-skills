---
name: motion-graphics-tan
description: Thư viện phong cách motion graphics cho thẻ, title, số liệu trong video — mỗi phong cách có bảng màu, font hỗ trợ tiếng Việt, chữ ký chuyển động GSAP và thẻ mẫu HyperFrames đã render thật. Hiện có Swiss, Kinetic Type, Pop Art, Glassmorphism, Editorial, Flat 2D, Bauhaus, Neo-brutalism, Minimal sang trọng, Synthwave, Clay 3D, Pixel 8-bit, Doodle, Paper cut, Neon, Space/Orbit, Globe 3D, Chrome, Gradient UI, Isometric. Kích hoạt khi người dùng muốn thẻ/title/motion graphic theo một phong cách ("kiểu Swiss", "chữ động", "pop art", "kính mờ", "kiểu báo chí", "phẳng", "bauhaus", "brutalism", "sang trọng", "retro", "đất nặn", "pixel", "vẽ tay", "giấy cắt", "neon", "vũ trụ", "địa cầu", "kim loại", "gradient", "isometric"), hỏi nên chọn phong cách nào, hoặc muốn video chuyển động đẹp hơn. Không dùng để cắt ghép hay thêm phụ đề (video-use, bien-tap-video-thong-minh-song-ngu-tan); hiệu ứng theo câu nói đặt sau người thì kết hợp với video-marketing.
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
| Giới thiệu dịch vụ, hướng dẫn thân thiện | Flat 2D | [flat-2d.md](references/phong-cach/flat-2d.md) |
| Thương hiệu, thiết kế, giáo dục | Bauhaus | [bauhaus.md](references/phong-cach/bauhaus.md) |
| Mạng xã hội cho người trẻ, kêu gọi bấm | Neo-brutalism | [neo-brutalism.md](references/phong-cach/neo-brutalism.md) |
| Sản phẩm cao cấp, lễ kỷ niệm, thư mời | Minimal sang trọng | [minimal-sang.md](references/phong-cach/minimal-sang.md) |
| Âm nhạc, sự kiện đêm, giải trí | Synthwave | [synthwave.md](references/phong-cach/synthwave.md) |
| Sản phẩm dễ thương, mỹ phẩm, trẻ em | Clay 3D | [clay-3d.md](references/phong-cach/clay-3d.md) |
| Game, thử thách, cấp độ, điểm số | Pixel 8-bit | [pixel-8bit.md](references/phong-cach/pixel-8bit.md) |
| Hướng dẫn các bước, checklist, vlog | Doodle vẽ tay | [doodle.md](references/phong-cach/doodle.md) |
| Kể chuyện, quê hương, thiên nhiên | Paper cut | [paper-cut.md](references/phong-cach/paper-cut.md) |
| Quán, sự kiện tối, thông báo giờ mở cửa | Neon glow | [neon-glow.md](references/phong-cach/neon-glow.md) |
| Tầm nhìn, khởi đầu mới, ra mắt | Space/Orbit | [space-orbit.md](references/phong-cach/space-orbit.md) |
| Thị trường, mạng lưới, số quốc gia | Globe 3D | [globe-3d.md](references/phong-cach/globe-3d.md) |
| Sản phẩm công nghệ, xe, bản cao cấp | Chrome | [chrome.md](references/phong-cach/chrome.md) |
| Báo cáo số liệu, tăng trưởng, phần mềm | Gradient UI | [gradient-ui.md](references/phong-cach/gradient-ui.md) |
| Giải thích cấu trúc, các lớp, quy trình | Isometric 3D | [isometric.md](references/phong-cach/isometric.md) |

Không rõ thì chọn theo độ nghiêm túc của chủ đề. **Pop Art, Kinetic Type, Neo-brutalism, Synthwave không hợp tin buồn, phim tài liệu.**

Chọn thẻ theo ý của từng câu nói: [canh-theo-muc-dich.md](references/canh-theo-muc-dich.md).

## Kỹ thuật dựng video marketing (15 thẻ)

Ngoài phong cách, có 12 thẻ kỹ thuật học từ 86 video marketing, nằm trong `assets/ky-thuat/`:

- phụ đề tô từ khóa, tiêu đề mở đầu, số mục to;
- khung điện thoại, ô "?" lật dần, chia đôi màn hình;
- thẻ kiến thức "Giai đoạn", mốc giờ, khoanh đỏ vẽ tay;
- chữ mờ phía sau, con trỏ chuột giả, số đếm chạy;
- thêm 3 thẻ học từ 703 prompt video Opus 5.5: giải thích 5 cảnh, công thức từng bước, hình biến giao diện. Khung viết prompt motion: [hoc-tu-prompt-opus.md](references/hoc-tu-prompt-opus.md).

Kèm theo là nhịp chuẩn đo được (mỗi cảnh 1,5–2,5 s, chuyển mềm dưới 0,4 s). Xem [ky-thuat.md](references/ky-thuat.md). Render giống thẻ phong cách: `python scripts/render_mau.py <ten-ky-thuat>`.

## Quy trình

1. Đọc công thức của phong cách, chép thẻ mẫu sang dự án, đổi nội dung qua biến (`data-var-text`).
2. Kiểm và xem: `python scripts/render_mau.py <ten>` (chạy từ thư mục skill) → `check` phải 0 lỗi, rồi xem ảnh 4 khung (chuyển động) và **ảnh `<ten>.chu.png`** cắt sát ở độ phân giải gốc (đúng font, đúng màu, không chồng chữ).
3. Đặt lên video người nói: `python scripts/render_mau.py <ten> --trong-suot` ra `.webm` nền trong suốt, rồi `ghep_lop.py` của skill `video-marketing`.

## Luật khi viết thẻ

- **Tên biến nội dung không được trùng tên biến CSS.** Biến `nhan` đè lên `--nhan` làm mất màu mà render vẫn chạy (lỗi thật ở thẻ Editorial).
- **Chỉ dùng font có đuôi ` VN`** (`Montserrat`, `Inter`, `Playfair`, `Nunito`, `VT323`, `Patrick Hand`, `Tilt Neon`) trong `assets/fonts/` (chép khối `@font-face` từ `font-face.json`). Tên gốc `Montserrat`, `Inter`… bị thay bằng bộ font đi kèm chỉ có chữ Latin: **ư, ơ, ự hiện bằng font khác**. Font khác phải có bộ chữ `vietnamese` (Archivo Black, Press Start 2P, Pixelify Sans không có).
- **Soi chữ ở độ phân giải cao**, cắt sát thẻ. Ảnh 4 khung thu nhỏ không đủ để thấy sai font (đợt 1 từng lọt lỗi này).
- Không tween `letterSpacing`, `left`, `top`, `width`; không dùng `background-clip: text`.
- Phần tử còn nằm ngoài khung phải `opacity: 0`, nếu không bộ kiểm đo tương phản sai và báo lỗi.
- Thẻ đặt nửa trên khung (`top: 170px`, cao 1000px), là vị trí "trên đầu người nói".
- Thẻ mẫu dài 3 giây để xem nhanh. Dùng thật thì chỉnh thời lượng theo câu nói, dòng chữ cuối giữ ít nhất 2 giây (cảnh báo `line_unread`).
- Cảnh báo `first_frame_empty` và `nested_structure_needs_subcomposition` được chấp nhận ở thẻ phủ lên video.
- **Chỉ render trên máy.** Không dùng `hyperframes cloud render` (dịch vụ trả phí) khi người dùng chưa đồng ý.
- Học phong cách và kỹ thuật, không chép thiết kế, hình, chữ của người khác.

## Đủ 20 phong cách

Tất cả có thẻ mẫu đã render và dựng bằng CSS/SVG, không WebGL (máy hay sập khi chạy nặng). Thêm phong cách mới: thẻ trong `assets/mau/`, công thức trong `references/phong-cach/`, một dòng ở bảng trên.

**Chưa kiểm:** chưa có thẻ nào được ghép lên video người nói thật.
