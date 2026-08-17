---
name: bien-tap-video-thong-minh-song-ngu-tan
description: Phân tích nội dung, hình ảnh, lời nói và nhịp của từng video để tự chọn chiến lược biên tập phù hợp, đồng thời tạo phụ đề song ngữ tiếng Anh ở dòng trên và tiếng Việt ở dòng dưới. Dùng cho bản tin, hội nghị, phỏng vấn, tuyên truyền, sự kiện, phóng sự, video giáo dục và mạng xã hội; không tự cắt video nếu chưa được người dùng cho phép.
---

# Biên tập video thông minh song ngữ Tan

Phân tích trước, chọn phong cách sau. Không áp một preset cho mọi video.

## Quy trình

1. Chạy `scripts/analyze_and_plan.py INPUT --transcript transcript.txt --out edit/plan.json` để đo thông số, mật độ chuyển cảnh và phân loại nội dung.
2. Đọc `references/editing-profiles.md`, đối chiếu kết quả tự động với nội dung thật và chọn một profile chính; chỉ pha profile khi có lý do rõ.
3. Mặc định `cut_authorized=false`. Không trim, bỏ cảnh, rút khoảng lặng, freeze hoặc speed-ramp làm đổi thời lượng. Nếu muốn cắt, liệt kê mốc, lý do và hỏi người dùng.
4. Chuẩn bị `bilingual.json` theo `references/bilingual-contract.md`. Dịch theo nghĩa và văn phong tự nhiên; giữ nguyên tên riêng, chức danh, địa danh, số liệu. Không dịch từ nội dung chưa nghe/đọc rõ.
5. Khi có người phát biểu/phỏng vấn, xác minh tên và chức vụ/đơn vị hoặc địa chỉ; tạo `lower-thirds.ass` theo `references/lower-third-contract.md`. Không nhận diện hoặc đoán danh tính từ hình ảnh.
6. Nếu người dùng yêu cầu dùng giọng cá nhân đã được chính họ cho phép, đọc `references/authorized-voice.md`. Chỉ dùng hồ sơ đã có xác nhận; không commit mẫu giọng, token hoặc `voice_profile_id` lên GitHub.
7. Chạy `scripts/make_bilingual_ass.py bilingual.json captions.ass`: tiếng Anh dòng trên, tiếng Việt dòng dưới, cùng mốc thời gian.
8. Chạy `scripts/render.py INPUT plan.json captions.ass OUTPUT --source INPUT --lower-thirds lower-thirds.ass`; bỏ đối số cuối nếu video không có người phát biểu.
9. Chạy `scripts/qa.py OUTPUT --source INPUT --cut-authorized no --captions bilingual.json` và xem thủ công các điểm vào/ra chữ, chuyển cảnh, lower-third, 2 giây đầu/cuối.

## Ra quyết định theo nội dung

- **Bản tin/chính quyền:** News Clean, xanh–đỏ, hard cut/dissolve ngắn, chữ rõ, hiệu ứng tiết chế.
- **Hội nghị/tuyên truyền:** ưu tiên thông tin, toàn–trung–cận, lower-third, ổn định hình và âm lời.
- **Phỏng vấn:** giữ nhịp nói tự nhiên, ít transition, lower-third người nói, ducking nhạc.
- **Phóng sự/sự kiện:** nhịp vừa, montage theo cụm, cut-on-action, sound bridge.
- **Giáo dục/hướng dẫn:** caption rõ, callout, highlight từ khóa, màn hình đủ lâu để đọc.
- **Mạng xã hội/montage:** hook nhanh, chuyển động và hiệu ứng mạnh hơn nhưng không che nội dung.

## Phụ đề song ngữ bắt buộc

- English ở trên; Tiếng Việt ở dưới. Không đảo thứ tự.
- Cùng mốc thời gian và cùng ý nghĩa; tối đa 2 dòng ngôn ngữ trong một cue.
- English dùng màu trắng hoặc vàng nhạt; Tiếng Việt màu trắng, cỡ lớn hơn nhẹ.
- Mỗi dòng nên ≤42 ký tự khi 16:9 và ≤30 ký tự khi 9:16; chia câu theo cụm nghĩa, không tách tên người hoặc số liệu.
- Vùng phụ đề không chồng logo, ticker, lower-third hoặc mặt người.
- Kiểm tra thủ công bản dịch và đồng bộ; máy không được tự tuyên bố bản dịch chính xác khi chưa rà soát.

## Bảy lớp dựng

Luôn cân nhắc Text, Stickers, Effects, Transitions, Captions, Filters và Adjustment, nhưng chỉ dùng lớp phục vụ nội dung. “Dùng hết” nghĩa là đánh giá đủ bảy lớp, không phải nhồi mọi hiệu ứng vào một video.

**1. Text** — tiêu đề, lower-third, banner, chữ 3D giả lập, glow, stroke, shadow, typewriter, karaoke, đếm ngược.
Chữ phải đọc được trên điện thoại: stroke hoặc shadow đủ tách nền, không đặt chữ mảnh trên nền động. Typewriter và karaoke chỉ dùng khi có mốc thời gian thật, không gõ theo cảm tính. Lower-third theo `references/lower-third-contract.md`.

**2. Stickers** — PNG/WebP/GIF/video alpha, logo, icon mạng xã hội, emoji, callout.
Chỉ dùng tài nguyên có quyền. Không xóa hoặc che watermark của người khác. Sticker không che mặt, micro, tay, chữ trên sân khấu hoặc màn hình trình chiếu. Logo cố định một góc, giữ nguyên vị trí suốt video.

**3. Effects** — flash, light leak, zoom/motion blur, shake, glitch, RGB split, vignette, grain, freeze, slow motion, speed ramp, Ken Burns.
Bản tin và hội nghị: tiết chế, gần như chỉ vignette/grain nhẹ. Mạng xã hội/montage: mạnh hơn nhưng vẫn không che nội dung. **Freeze, slow motion và speed ramp làm đổi thời lượng** — chỉ dùng khi `cut_authorized=true`, nếu không thì bỏ.

**4. Transitions** — cut, fade, dissolve, dip-white, dip-black, wipe, slide, push, zoom, blur, radial/circle, whip-pan, flash.
Mặc định hard cut. Dissolve ngắn giữa cụm cảnh. Whip-pan, zoom, glitch chỉ cho montage. Không đặt transition vào giữa một câu nói đang dở. Transition dài quá 0,5 giây trong bản tin là quá đà.

**5. Captions** — SRT/ASS, caption theo câu hoặc theo từ, karaoke highlight, hộp nền, vùng an toàn, tái tính timestamp sau cắt.
Ở skill này caption luôn là song ngữ theo mục "Phụ đề song ngữ bắt buộc" ở trên. Hộp nền mờ khi nền sáng hoặc nhiều chi tiết. **Cắt/ghép xong phải tính lại toàn bộ timestamp** rồi kiểm lại đồng bộ, không giữ nguyên file cũ.

**6. Filters** — Natural, Vibrant, Cinematic, Warm, Cool, B&W, Vintage, News Clean.
Ưu tiên **màu da thật**: giảm strength ngay khi da ngả đỏ hoặc cháy vùng sáng. Bản tin/chính quyền dùng News Clean hoặc Natural. Không đổi tông giữa chừng trong cùng một cụm cảnh.

**7. Adjustment** — brightness/exposure, contrast, saturation, temperature/tint, sharpen, denoise, stabilization, crop, rotate, opacity, speed, audio gain/ducking.
Sửa lỗi kỹ thuật trước, làm đẹp sau. Denoise trước sharpen. **Không stabilize xuyên qua điểm cắt cảnh** — sẽ vỡ hình. Crop/rotate làm đổi khung: kiểm lại chữ và lower-third có bị cắt cụt không. Ducking nhạc nền xuống dưới lời nói, chuẩn hóa mức âm cuối cùng.
**Speed làm đổi thời lượng** — áp cùng ràng buộc `cut_authorized` như mục Effects.

Công thức ffmpeg và tên preset cụ thể cho từng lớp: xem `chuyen-gia-edit-video-tan/references/effect-catalog.md` và skill `hieu-ung-video`. Không tự nghĩ filter chain từ đầu.

## Banner người phát biểu

- Khi người phát biểu xuất hiện, dùng banner hai dòng: tên nổi bật phía trên; chức vụ–đơn vị hoặc địa chỉ phía dưới.
- Màu xanh đậm–xanh dương, chữ trắng, điểm nhấn cyan/đỏ nhỏ; chuyển động trượt vào nhẹ, phù hợp ATT NEWS.
- Hiện 4–6 giây ở lần giới thiệu đầu; không che mặt, micro, tay hoặc nội dung quan trọng.
- Lower-third và phụ đề song ngữ phải nằm ở hai vùng riêng. Đọc `references/lower-third-contract.md` trước khi tạo.

## Ranh giới an toàn

- Không xóa watermark hoặc dùng tài nguyên không có quyền.
- Không tự thêm sự kiện, con số, chức danh hay phát biểu.
- Không che nhân vật và thông tin trên sân khấu/màn hình.
- Không suy đoán quyền dùng giọng. Mỗi hồ sơ giọng phải ghi chủ thể, phạm vi cho phép và ngày xác nhận; hỏi lại trước nội dung nhạy cảm hoặc phát biểu có thể bị hiểu là lời nói thật của chủ thể.
- Mẫu giọng cá nhân và mã hồ sơ nhà cung cấp là dữ liệu riêng tư: lưu ngoài Git, không nhúng vào gói skill công khai, không chia sẻ hoặc tái sử dụng cho người khác.
- Khi xuất bản nội dung dùng giọng tổng hợp cá nhân, đề nghị gắn nhãn phù hợp như “Giọng đọc được hỗ trợ bởi AI”.
- H.264 + AAC, `yuv420p`, `+faststart`; mặc định giữ fps và tỷ lệ nguồn.
