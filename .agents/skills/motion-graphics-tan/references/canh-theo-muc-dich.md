# Chọn thẻ theo ý cần diễn đạt

Bảng "Chọn phong cách" trong `SKILL.md` chọn theo chủ đề video. Bảng này chọn theo **điều người nói đang diễn đạt ở câu đó**. Trong một video, chọn một phong cách chung trước; nếu phong cách đó không có thẻ hợp ý thì dùng thẻ khác cùng tông, đừng trộn nhiều phong cách.

| Câu nói đang diễn đạt | Thẻ hợp | Biến cần điền |
|---|---|---|
| Một con số, kết quả | `gradient-ui` | `tieu-de`, `so`, `phu` |
| Số liệu dạng giao diện app | `glassmorphism` | `ten`, `so`, `phu` |
| Giá, khuyến mãi, tin vui | `pop-art` | `keu`, `so` |
| Điểm số, cấp độ, thử thách | `pixel-8bit` | `diem`, `tieu-de`, `phu` |
| Quy mô, số quốc gia, mạng lưới | `globe-3d` | `tieu-de`, `so` |
| Các bước, checklist | `doodle` | `tieu-de`, `buoc1`, `buoc2`, `buoc3` |
| Các lớp, cấu trúc | `isometric` | `tieu-de`, `lop1`, `lop2`, `lop3` |
| Sang mục mới có số thứ tự | `swiss` | `so`, `tieu-de`, `phu` |
| Câu chốt, khẩu hiệu, mở đầu | `kinetic-type` | `chot` |
| Kêu gọi bấm, đăng ký | `neo-brutalism` | `nhan-dan`, `tieu-de`, `nut` |
| Giới thiệu dịch vụ, app | `flat-2d` | `mo-dau`, `tieu-de`, `phu` |
| Giới thiệu sản phẩm công nghệ, xe | `chrome` | `tieu-de`, `phu` |
| Giới thiệu sản phẩm dễ thương | `clay-3d` | `tieu-de`, `phu` |
| Giới thiệu thương hiệu | `bauhaus` | `tieu-de`, `phu` |
| Tiêu đề tin, phóng sự | `editorial` | `tieu-muc`, `dong1`, `dong2`, `dong3`, `phu` |
| Kỷ niệm, trao giải, thư mời | `minimal-sang` | `nho`, `dong1`, `dong2`, `phu` |
| Thông báo sự kiện, giờ mở cửa | `neon-glow` | `dong1`, `dong2`, `phu` |
| Âm nhạc, đêm diễn | `synthwave` | `tieu-de`, `phu` |
| Kể chuyện, quê hương | `paper-cut` | `tieu-de`, `phu` |
| Tầm nhìn, khởi đầu mới | `space-orbit` | `tieu-de`, `phu` |

**Chưa có thẻ:** so sánh hai bên, trước và sau, câu hỏi rồi trả lời. Gặp các ý này thì báo trong kế hoạch ở cổng duyệt 1, đừng ép vào thẻ không hợp. Có thể chuyển thể từ thư viện tham khảo bên dưới (`comparison`, `before-after`, `question-answer`).

Số liệu, giá và lời chứng thực trên thẻ phải lấy từ lời nói hoặc tư liệu của người dùng, không dùng số mẫu.

## Thư viện tham khảo: editonny

Bản tải về nằm ngoài repo, chỉ có trên máy này: `D:\GitHub\editonny-thu-vien\skills\editonny\visuals\` (commit `49714f2`, 145 cảnh, 79 clip, 482 MB). Tra cảnh theo `whenToUse` trong `catalog.json`, đừng mở cả thư mục.

- **Chưa dùng thẳng được:** cảnh chạy trong khung dự án của editonny, chữ mẫu chưa phải tiếng Việt. Muốn dùng phải chuyển thể sang thẻ của skill này, thay bằng font `… VN` và soát dấu ở độ phân giải cao.
- **Giấy phép:** mã là MIT; tiếng động trong `library/effects/` là CC0 theo `CREDITS.md`, nhạc trong `library/music/` khai CC0 trong `catalog.json`. Clip và ảnh phải kiểm nguồn từng file trước khi đưa vào video đăng công khai hoặc chép vào repo này.
- **Không làm theo `recipes/` có gọi Kling, ElevenLabs:** đó là dịch vụ trả phí, phải được người dùng đồng ý từng lần.
