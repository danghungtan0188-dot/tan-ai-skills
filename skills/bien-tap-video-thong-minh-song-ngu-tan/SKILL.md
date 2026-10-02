---
name: bien-tap-video-thong-minh-song-ngu-tan
description: Tự tìm và xem toàn bộ clip trong kho/thư mục người dùng chỉ định, phân tích nội dung, hình ảnh, lời nói và nhịp để cắt ghép thành một video hoàn chỉnh có bố cục logic, đúng độ dài được yêu cầu; đồng thời hỗ trợ phụ đề song ngữ Anh trên–Việt dưới và phong cách ATT NEWS. Kích hoạt khi người dùng đưa kho clip, footage hoặc nhiều video và yêu cầu tự động dựng/cắt ghép. Chỉ quét trong kho được chỉ định; chỉ cắt khi yêu cầu hiện tại nói rõ tự động dựng/cắt ghép hoặc người dùng duyệt edit-plan.
---

# Biên tập video thông minh song ngữ Tan

Phân tích trước, chọn phong cách sau. Không áp một preset cho mọi video.

> **Bản tin ATT NEWS (xã An Thạnh Thủy):** đã có bộ thông số chốt sẵn — logo góc, vị trí
> icon mạng xã hội, cỡ/màu phụ đề, lệnh render. Đọc [references/phong-cach-att-news.md](references/phong-cach-att-news.md)
> và áp dụng y nguyên, không dựng lại từ đầu. Tài nguyên góc sinh bằng
> `scripts/make_att_bugs.py`.

> **Người dùng đưa cả thư mục clip thô tự quay?** Đọc [references/dung-tu-video-tho.md](references/dung-tu-video-tho.md)
> trước: khảo sát → xem contact sheet chọn cảnh → kiểm luật dựng và co cho khớp độ dài người dùng
> đặt → **đưa bảng đoạn cho người dùng duyệt** → ghép, rồi mới quay lại quy trình bên dưới từ bước 4.

> **Chế độ tự dựng từ kho:** khi người dùng nói rõ “tự động tìm/xem/cắt ghép/dựng” và chỉ kho
> clip cùng thời lượng đích, đó là quyền cắt cho yêu cầu hiện tại. Quét đệ quy đúng kho đó, xem hết
> contact sheet, tự lập bố cục mở đầu → diễn biến → điểm chính/phát biểu → kết, tạo plan bằng
> `--approved`, ghép và QA mà không cần dừng xin duyệt lại. Nếu chưa có thời lượng đích thì hỏi một
> lần; không tự quét toàn ổ đĩa hay thư mục ngoài phạm vi người dùng đặt.

> **Ba kho mặc định của người dùng:** Desktop, Documents và Google Drive. Khi người dùng nói “trong
> kho” mà không nêu đường dẫn, đọc [references/kho-clip.md](references/kho-clip.md), tìm lần lượt ở ba
> nơi này theo tên/chủ đề/ngày của yêu cầu. Với Google Drive, dùng tìm kiếm Drive hoặc thư mục Drive
> đã đồng bộ; chỉ tải các video đã chọn về thư mục làm việc, không tải toàn bộ Drive.

## Nâng cấp chi tiết

- **Sau mỗi video phải rút kinh nghiệm:** [references/rut-kinh-nghiem.md](references/rut-kinh-nghiem.md) — bốn câu hỏi cố định, ghi một dòng vào [references/nhat-ky-ban-tin.md](references/nhat-ky-ban-tin.md), và **mỗi bài học phải neo vào một test / một luật trong script / một dòng tài liệu** thì mới tính là đã lưu.

- **Làm theo khuôn video cũ:** [references/khuon-tu-video-cu.md](references/khuon-tu-video-cu.md) — `khuon_mau.py` chép nguyên kiểu chữ/màu/viền/vị trí và tham số logo, outro, LUFS từ project cũ; `cut_silence.py` đề xuất bỏ khoảng lặng và từ đệm (không tự cắt); `build_bilingual.py tu-asr` tạo phụ đề nháp từ giọng nói khi không có kịch bản.
- **Dựng từ video thô:** [references/dung-tu-video-tho.md](references/dung-tu-video-tho.md) — `survey_rushes.py` → `build_edit_plan.py` → `assemble.py`; luật cỡ cảnh, độ dài cảnh, chống nhảy hình, khớp đúng thời lượng yêu cầu.
- **Tìm kho clip:** [references/kho-clip.md](references/kho-clip.md) — thứ tự Desktop → Documents → Google Drive, quy tắc lọc video liên quan và cách đưa file Drive về vùng làm việc trước khi khảo sát.
- **Song ngữ Việt–Anh:** [references/quy-trinh-song-ngu.md](references/quy-trinh-song-ngu.md) — lời Việt theo kịch bản (ASR chỉ lấy mốc), glossary, `check_translation.py`, 4 chế độ xuất (`export_subtitles.py`), kiểm SRT/VTT (`check_subtitles.py`).
- **ATT NEWS một lượt:** `detect_scenes.py` → `make_tv_card.py` → `make_outro.py` → `render_att.py` → `qa.py --tail`; banner kiểm tràn cảnh bằng `make_lower_thirds_ass.py --scenes`.
- **MC AI / lip-sync:** [skills/chuyen-gia-edit-video-tan/references/mc-ai-lip-sync.md](skills/chuyen-gia-edit-video-tan/references/mc-ai-lip-sync.md)
- **Chức năng kiểu CapCut:** [skills/chuyen-gia-edit-video-tan/references/capcut-catalog.md](skills/chuyen-gia-edit-video-tan/references/capcut-catalog.md)
- **Banner – icon truyền hình VN:** [skills/chuyen-gia-edit-video-tan/references/he-thong-do-hoa-truyen-hinh.md](skills/chuyen-gia-edit-video-tan/references/he-thong-do-hoa-truyen-hinh.md)

## Quy trình

1. Chạy `scripts/analyze_and_plan.py INPUT --transcript transcript.txt --out edit/plan.json` để đo thông số, mật độ chuyển cảnh và phân loại nội dung.
2. Đọc `references/editing-profiles.md`, đối chiếu kết quả tự động với nội dung thật và chọn một profile chính; chỉ pha profile khi có lý do rõ.
3. Mặc định `cut_authorized=false`. Không trim, bỏ cảnh, rút khoảng lặng, freeze hoặc speed-ramp làm đổi thời lượng. Nếu muốn cắt, liệt kê mốc, lý do và hỏi người dùng.
4. Dựng `bilingual.json` theo `references/bilingual-contract.md` và [references/quy-trinh-song-ngu.md](references/quy-trinh-song-ngu.md): `scripts/build_bilingual.py transcribe INPUT` lấy **mốc thời gian**, viết `cues.json` với lời Việt **theo kịch bản gốc** (không chép ASR), rồi `scripts/build_bilingual.py build`. Giữ nguyên tên riêng, chức danh, địa danh, số liệu.
5. Chạy `scripts/detect_scenes.py INPUT --out scenes.json`. Khi có người phát biểu, xác minh tên và chức vụ từ kịch bản, rồi `scripts/make_lower_thirds_ass.py lower-thirds.json lt.ass --scenes scenes.json` — tham số `--scenes` chặn banner tràn sang cảnh khác. Không đoán danh tính từ hình ảnh.
6. Nếu người dùng yêu cầu dùng giọng cá nhân đã được chính họ cho phép, đọc `references/authorized-voice.md`. Chỉ dùng hồ sơ đã có xác nhận; không commit mẫu giọng, token hoặc `voice_profile_id` lên GitHub.
   Với ATT NEWS trên máy của người dùng, ưu tiên lựa chọn rõ ràng: `mc-an-thanh-thuy` cho MC Đài An Thạnh Thủy hoặc `hung-tan-chan-that` cho Giọng Hùng Tân chân thật; tổng hợp qua skill `tan-giong-doc-ban-tin`. Không tự chọn giữa hai giọng khi người dùng chưa chỉ định.
7. Kiểm bản dịch `scripts/check_translation.py bilingual.json`, xuất phụ đề `scripts/export_subtitles.py bilingual.json --mode all`, kiểm file rời `scripts/check_subtitles.py`.
8. Render một lượt. Bản tin ATT NEWS: `scripts/render_att.py INPUT --captions cap.song-ngu.ass --lower-thirds lt.ass --scenes scenes.json --card card.png --outro-dir outro --out OUT.mp4` (xem [references/phong-cach-att-news.md](references/phong-cach-att-news.md)). Video thường: `scripts/render.py INPUT plan.json captions.ass OUTPUT --lower-thirds lt.ass`.
9. Chạy `scripts/qa.py OUTPUT --source INPUT --cut-authorized no --tail <giây outro> --captions bilingual.json` và xem thủ công các điểm vào/ra chữ, chuyển cảnh, lower-third, 2 giây đầu/cuối.
10. Sau khi người dùng xem và phản hồi, chạy `/rut-kinh-nghiem` theo [references/rut-kinh-nghiem.md](references/rut-kinh-nghiem.md): trả lời bốn câu hỏi, ghi một dòng vào [references/nhat-ky-ban-tin.md](references/nhat-ky-ban-tin.md), và neo bài học vào một test / một luật trong script / một dòng tài liệu. Trước video kế tiếp, đọc lại các dòng nhật ký cùng thể loại. Không biến một sở thích nhất thời hay một lỗi cá biệt thành luật chung.

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
