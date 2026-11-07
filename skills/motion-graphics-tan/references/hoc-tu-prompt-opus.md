# Học từ 703 prompt video làm bằng Opus 5.5

Nguồn: [yihui-dev/awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos) (MIT), file `data/videos.json`, bản ngày 12/10/2026. Đọc ngày 07/11/2026.
Prompt và video là **của từng tác giả** trên X. Ở đây chỉ rút cách viết và cách dựng, diễn đạt lại bằng lời của mình. Không chép prompt, không làm lại video của ai.

## Kho có gì (đếm thật)

| Loại | Số prompt | Công nghệ hay gặp |
|---|---|---|
| Motion graphics | 369 | canvas 267, svg 183, three.js 131, shader 92, gsap 86 |
| 3D | 117 | |
| Giải thích (explainer) | 116 | |
| Tương tác, game | 101 | |

207/703 prompt chỉ có một phần (tác giả không công bố hết). Prompt điển hình dài khoảng 220 ký tự, tức một hai câu yêu cầu. Prompt dài thì có cấu trúc rõ.

**Không hợp máy này:** three.js, shader, WebGL (máy hay sập khi chạy nặng). Chỉ học từ nhóm SVG/CSS/GSAP/canvas 2D.

## Khung prompt của nhóm làm đẹp nhất

Nhóm prompt dài, ra video đẹp, thường chia thành khối có tên (`<inputs>` 26 lần, `<direction>` 27 lần, "ask me" 32 lần):

| Khối | Viết gì | Bản tiếng Việt dùng cho mình |
|---|---|---|
| Đầu vào | Liệt kê thứ AI phải **hỏi** người dùng trước khi làm: sản phẩm, màu thương hiệu, số liệu thật, tỉ lệ khung | "Hỏi mình: tên dịch vụ, 3 lợi ích, một con số thật, màu chủ đạo, tỉ lệ 9:16 hay 16:9" |
| Hướng đi | Phong cách bằng tính từ cụ thể, kèm **danh sách cấm** (nhún nảy quá đà, hạt bắn, phát sáng, gradient trên giao diện, khoảng chết) | Chọn một phong cách trong `references/phong-cach/`, chép phần "Không làm" của nó |
| Cấu trúc | Chuỗi cảnh nối bằng mũi tên, khóa theo nhịp nhạc (ví dụ 120 BPM, mỗi phách một thay đổi) | Chuỗi thẻ: `tieu-de-mo-dau → so-muc-to → so-dem-chay → ...` |
| Chuyển động | Luật chuyển động: lò xo hơi vượt một chút, nội dung vào **sau** khi khung bắt đầu đổi và ra **trước** khi khung đổi tiếp, khung cuối bằng khung đầu để lặp | Đã có trong luật thẻ của skill này |
| Xuất | Trước tiên xuất ảnh mỗi phách một khung để soát, sửa chỗ chật, rồi mới render thật | Chính là bước `render_mau.py` → ảnh 4 khung → ảnh chữ |

## Mẫu đáng học (đã làm thành thẻ)

| Mẫu trong kho | Ý chính | Thẻ của mình |
|---|---|---|
| Video giải thích 30 giây cho doanh nghiệp, 5 cảnh (prompt của @alex_prompter) | Vấn đề của khách → mình làm gì → 3 bước → một bằng chứng → tên mình | `giai-thich-5-canh` |
| Công thức pha chế từ ly rỗng tới ly đầy (prompt của @Ror_Fly) | Từng thành phần đi vào theo thứ tự, kèm định lượng, thấy kết quả lớn dần | `cong-thuc-tung-buoc` |
| Một hình biến qua 8–12 trạng thái giao diện (9 prompt, ví dụ @twoclipping, @verbove) | Một khối duy nhất, không cắt; đổi cỡ, bo góc, màu trong khi nội dung bên trong thay | `hinh-bien-giao-dien` |

## Luật rút ra (trùng với HyperFrames, nên giữ)

- **Mọi thứ tính từ thời gian**, không dùng hẹn giờ, không dùng CSS transition, không giữ trạng thái giữa các khung. HyperFrames tua timeline GSAP nên đã đúng sẵn, chỉ cần không dùng `setTimeout` và `repeat: -1`.
- **Nội dung không chồng nhau khi đổi cảnh:** chữ cũ ra xong rồi chữ mới mới vào. Khung đổi trước, chữ theo sau.
- **Một điểm nhấn màu chạy giữa các cảnh** thay vì mờ từ đen sang màu nhấn.
- **Dữ liệu thật, không để chữ giữ chỗ** kiểu "Lorem ipsum" hay "Sản phẩm A". Thiếu số liệu thì hỏi người dùng.
- **Soát trước, render sau:** xem ảnh tĩnh từng cảnh, sửa chỗ chật, rồi mới render cả video.

## Viết prompt cho việc của mình

Khi người dùng nhờ "làm motion giới thiệu dịch vụ", dùng khung trên, điền bằng tiếng Việt, chọn thẻ có sẵn trước khi viết thẻ mới.
Muốn video AI (Seedance, Veo…) thay vì motion bằng code thì dùng skill `viet-prompt-video-ai`.
