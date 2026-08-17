---
name: chuyen-gia-edit-video-tan
description: Phân tích video mẫu và dựng video chuyên nghiệp bằng code với bộ chức năng tương đương CapCut gồm Text, Stickers, Effects, Transitions, Captions, Filters và Adjustment. Dùng cho bản tin, sự kiện, MC, phóng sự, video tuyên truyền, Facebook, Zalo, Reels và Shorts; không dùng để sao chép tài nguyên độc quyền hoặc xóa watermark.
---

# Chuyên gia Edit Video Tan

Biến yêu cầu, tư liệu gốc và video tham chiếu thành phương án dựng có thể kiểm tra, sửa và tái tạo bằng FFmpeg/Python. Giữ nguyên nguồn; sản phẩm nằm trong `edit/` cạnh tư liệu.

## Workflow

1. Chạy `scripts/analyze_video.py INPUT --out edit/analysis` để lấy metadata, loudness, điểm chuyển cảnh và contact sheet.
2. Xem video mẫu ở tốc độ thường; kiểm tra 2 giây đầu/cuối và từng điểm chuyển cảnh. Chỉ ghi nhận kỹ thuật quan sát được, không khẳng định tên preset CapCut khi không có project gốc.
3. Phiên âm mức từ khi có lời; xác minh tên người, chức danh, địa danh, ngày tháng và số liệu. Khi phát hiện người phát biểu/phỏng vấn, lập lower-third theo `references/lower-third-contract.md`; không nhận diện hoặc đoán danh tính từ hình ảnh.
4. Lập `edit/project.json` theo `references/project-schema.md`: timeline, crop, nhịp cắt, text, caption, sticker, transition, effect, filter, adjustment, music và SFX.
5. Đề xuất phương án dựng và chờ duyệt trước khi render toàn bộ. Khi yêu cầu là tạo skill/code, được xây và test engine trước nhưng chưa tự dựng lại tư liệu người dùng.
6. Chạy `scripts/render_project.py edit/project.json --preview`; tự kiểm tra và sửa tối đa ba vòng.
7. Sau duyệt, render H.264/AAC, `yuv420p`, `+faststart`; mặc định 1920×1080, 30 fps. Chỉ tạo 9:16 khi được yêu cầu.

## Bảy nhóm chức năng tương đương CapCut

- **Text:** tiêu đề, lower-third, banner, chữ 3D giả lập, glow, stroke, shadow, typewriter, karaoke, đếm ngược.
- **Stickers:** PNG/WebP/GIF/video alpha, logo, icon mạng xã hội, emoji, callout; chỉ dùng tài nguyên có quyền.
- **Effects:** flash, light leak, zoom/motion blur, shake, glitch, RGB split, vignette, grain, freeze, slow motion, speed ramp, Ken Burns.
- **Transitions:** cut, fade, dissolve, dip-white/black, wipe, slide, push, zoom, blur, radial/circle, whip-pan, flash.
- **Captions:** SRT/ASS, caption theo câu/từ, karaoke highlight, hộp nền, vùng an toàn, tái tính timestamp sau cắt.
- **Filters:** Natural, Vibrant, Cinematic, Warm, Cool, B&W, Vintage, News Clean; ưu tiên màu da thật.
- **Adjustment:** brightness/exposure, contrast, saturation, temperature/tint, sharpen, denoise, stabilization, crop, rotate, opacity, speed, audio gain/ducking.

Đọc `references/effect-catalog.md` khi chọn preset; `references/project-schema.md` trước khi viết JSON.

## Banner người phát biểu

- Khi có người phát biểu, ưu tiên banner hai dòng: tên ở trên; chức vụ–đơn vị hoặc địa chỉ ở dưới.
- Phong cách ATT NEWS: xanh đậm–xanh dương, điểm nhấn cyan/đỏ nhỏ, chữ trắng, chuyển động trượt vào tiết chế.
- Chỉ dùng thông tin do người dùng/tài liệu cung cấp hoặc đã xác minh. Thiếu tên/chức vụ thì hỏi trước khi render.
- Không che mặt, micro, tay diễn đạt hoặc nội dung sân khấu; không chồng phụ đề. Đọc `references/lower-third-contract.md` và tạo ASS bằng `scripts/make_lower_thirds_ass.py`.

## Quy tắc

- **Mặc định không cắt:** giữ nguyên toàn bộ thời lượng, thứ tự cảnh và lời nói của nguồn. Không tự xóa cảnh, rút khoảng lặng, trim đầu/cuối hoặc thay đổi timeline.
- Nếu nhận thấy đoạn nên cắt, chỉ lập danh sách đề xuất gồm mốc `in–out`, lý do và ảnh hưởng. Phải hỏi người dùng và chỉ cắt sau khi nhận được xác nhận rõ ràng.
- Yêu cầu “edit”, “dựng đẹp”, “làm chuyên nghiệp” hoặc “tự làm” không đồng nghĩa với cho phép cắt. Chỉ các chỉ dẫn rõ như “được cắt”, “rút gọn”, “loại đoạn…” mới cấp quyền cắt.
- Ghi `editing.cut_authorized: false` trong project theo mặc định. Khi giá trị này là false, `clips` phải bao phủ liên tục toàn bộ nguồn, không có khoảng mất và không đổi thứ tự.
- Hiệu ứng phục vụ nội dung và nhịp; bản tin nhà nước tiết chế hơn montage giải trí.
- Không cắt giữa từ; chừa 30–200 ms và fade audio khoảng 30 ms tại điểm cắt.
- Transition thường 0,12–0,55 giây; logo/chữ/caption nằm trong vùng an toàn, không che nhân vật hay thông tin.
- Thứ tự: adjustment/filter theo clip → ghép/transition → effect → text/sticker → caption.
- Nhạc phải có quyền sử dụng, thấp hơn lời; ưu tiên ducking.
- Không xóa watermark hay sao chép tài nguyên độc quyền CapCut; chỉ tái tạo hành vi thị giác hợp pháp.

## QA

Chạy `scripts/qa_video.py OUTPUT --source SOURCE --cut-authorized no`; xem 2 giây đầu/cuối, mọi điểm cắt và điểm vào/ra đồ họa; kiểm tra hình–tiếng, caption, chính tả, safe area, màu da, loudness và thời lượng. Khi chưa được phép cắt, QA phải FAIL nếu thời lượng đầu ra lệch nguồn quá 0,08 giây. Sau ba vòng sửa vẫn còn lỗi thì báo rõ.
