# Nhật ký bản tin — mỗi video một dòng

Cách ghi: [rut-kinh-nghiem.md](rut-kinh-nghiem.md). Mỗi bài học phải có **chỗ neo** ở cột
"Chốt bằng", dạng `test:TenClass`, `script:ten_file.py` hoặc `doc:ten-file.md`.
`tests/test_kinh_nghiem.py` kiểm các chỗ neo đó có thật.

Ghi thêm dòng ở **cuối bảng**, không sửa dòng cũ. Luật cũ hoá ra sai thì thêm dòng mới ghi "thay cho …".

| Ngày | Video | Dài | Bài học | Chốt bằng |
|---|---|---|---|---|
| 2026-09 | 06 — mừng thọ | 1:30 + 4s | Lời Việt chép từ ASR sẽ sai tên riêng và số liệu; ASR chỉ dùng để lấy mốc | `doc:phong-cach-att-news.md` |
| 2026-09 | 06 — mừng thọ | 1:30 + 4s | Hộp banner đặt ở 0,72 chiều cao đè lên dòng phụ đề tiếng Anh; hạ xuống 0,655 | `script:make_lower_thirds_ass.py` |
| 2026-09 | 06 — mừng thọ | 1:30 + 4s | Outro dưới 3 giây không kịp hiện logo và dòng kêu gọi | `test:TestMakeOutroGuard` |
| 2026-09 | sk2 — khám sức khỏe | 1:40 + 4s | Banner tràn sang cảnh sau làm gắn tên vào người khác | `test:TestLowerThirdScenes` |
| 2026-09 | sk2 — khám sức khỏe | 1:40 + 4s | `alimiter` mặc định có make-up gain, đẩy loudness lên −12,76 LUFS và TP 0,00; phải đặt `level=disabled` | `doc:phong-cach-att-news.md` |
| 2026-09 | Hungtanngu1 — lấy mẫu hài cốt | 1:56 + 4s | Lớp `--replace` đặt trên lớp logo sẽ che mất logo và icon; phải đặt dưới | `test:TestRenderAttLopHinh` |
| 2026-09 | Hungtanngu1 — lấy mẫu hài cốt | 1:56 + 4s | Nguồn 16:9 đặt vừa khung TV 2.49 thì hoặc đen hai bên hoặc mất nội dung; chọn lọt khung trên nền chuyển sắc | `doc:phong-cach-att-news.md` |
| 2026-09 | Hungtanngu1 — lấy mẫu hài cốt | 1:56 + 4s | Bản tin tang lễ, liệt sĩ không dùng nhạc nền; tiếng hiện trường là bằng chứng sự việc | `script:make_outro.py` |
| 2026-09-29 | — (nâng cấp quy trình) | — | Ghép từ nhiều clip thì `qa.py` phải chạy `--cut-authorized yes`, tức bỏ luôn phép kiểm thời lượng — cần kiểm theo kế hoạch thay vì theo nguồn | `test:TestBuildEditPlan` |
| 2026-09-30 | — (rà soát code) | — | `amix=inputs=2:duration=first` lấy độ dài theo lời đọc: lời ngắn hơn phim thì đuôi phim mất tiếng, lời dài hơn thì tiếng tràn ra ngoài kế hoạch | `test:TestAssembleLoiDoc` |
| 2026-09-30 | — (rà soát code) | — | Luật "duyệt trước, cắt sau" nằm trong tài liệu thì vẫn chạy được; phải chặn bằng code: `cut_authorized`, `valid`, kế hoạch rỗng, thiếu file | `test:TestAssembleTuChoi` |
| 2026-09-30 | — (rà soát code) | — | Render xong không probe lại thì không biết file thật có đúng thời lượng/khung/fps không | `script:assemble.py` |
| 2026-10-02 | — (kiểu chuyển động) | — | `zoompan` sinh mốc thời gian sai hẳn: một đoạn 4 giây ra 4096 giây; phải thêm `setpts=N/fps/TB` ngay sau nó, và đổi tốc độ chỉ được làm SAU khi mốc đã đúng | `test:TestKhuonHinhChayThat` |
| 2026-10-07 | An Thạnh Thủy — vùng căn cứ | 53,3s (3s intro) | Chấm TTS bằng whisper `small` loại oan bản đúng ("vùng"→"phùng", "khốc"→"khúc"); bản chọn phải nghe lại bằng `medium` — bắt được lỗi thật "cách mạng"→"các bạn" | `doc:phong-cach-att-news.md` |
| 2026-10-07 | An Thạnh Thủy — vùng căn cứ | 53,3s (3s intro) | ffmpeg kèm Remotion crash khi ghép ProRes 4444 (`do-hoa --out .mov` hỏng); xuất chuỗi PNG rồi đắp bằng ffmpeg hệ thống | `doc:phong-cach-att-news.md` |
| 2026-10-07 | An Thạnh Thủy — vùng căn cứ | 53,3s (3s intro) | Intro Remotion nền đặc phải đặt trước lời bình (lệch giọng 3,0 s), không trùng chữ với phụ đề câu đầu; footage 50p dựng theo mốc thì tự ghép 25p, không qua `tan_studio dung_video` (ép 30 fps, chia đều) | `doc:phong-cach-att-news.md` |
| 2026-10-07 | An Thạnh Thủy — vùng căn cứ | 53,3s (3s intro) | Ảnh `-loop 1` vào `zoompan` thành video 1166 s; ảnh 4:3 phải crop 16:9 trước zoom; TikTok tải lại có viền đen/chuyển cảnh bên trong — dò từng giây | `doc:phong-cach-att-news.md` |
| 2026-10-07 | An Thạnh Thủy — bản hội nghị | 58,6s | `adelay`+`apad` qua AAC để lại lỗ hổng 1,56 s trong luồng tiếng; QA không bắt, phát hiện khi đo mức từng giây — giờ dựng WAV đủ dài rồi map thẳng | `doc:phong-cach-att-news.md` |
| 2026-10-07 | An Thạnh Thủy — học phóng sự VHTV | — | Đo banner tên kiểu phóng sự (vị trí 77–87,5% cao, nghiêng 14°, 2 tầng xanh `#169A4D`/`#CBDBBE`, trượt vào 0,35 s) và dựng thành mẫu Remotion `BannerPhongSu` | `doc:banner-phong-su.md` |
| 2026-10-08 | Truyền thống cách mạng (tư liệu + nhân chứng) | 1:54 | Hook `check_render` báo FAIL giả ('moov atom not found', 0 byte) với lệnh render chạy nền vì kiểm lúc file đang ghi; giờ bỏ qua lệnh nền, QA chạy sau khi lệnh xong | `test:TestCheckRenderChayNen` |
| 2026-10-08 | Truyền thống cách mạng (tư liệu + nhân chứng) | 1:54 | Sửa nhỏ phải render lại toàn bộ 10–15 phút (6 lần); máy nóng phải giới hạn 2 nhân + ưu tiên thấp; render đè làm hỏng bản đã giao | `doc:phong-cach-att-news.md` |
| 2026-10-08 | Truyền thống cách mạng (tư liệu + nhân chứng) | 1:54 | `xfade` lỗi timebase với mp4 dựng sẵn (thêm `fps=25,settb=1/25`); Georgia thiếu dấu tiếng Việt; numba bị chặn nên đo F0 bằng numpy; loudnorm bóp LRA lời phỏng vấn | `doc:phong-cach-att-news.md` |
| 2026-10-08 | Truyền thống cách mạng (tư liệu + nhân chứng) | 1:54 | Không phủ b-roll lên khúc nhân chứng chỉ tay; dò cử chỉ bằng chuyển động vùng tay | `doc:phong-cach-att-news.md` |
| 2026-10-10 | Hai cuộc kháng chiến – Anh hùng LLVT (tư liệu + nhân chứng + nghĩa trang) | 3:26 | VieNeu phát tiếng lạ sau quãng lặng cuối câu (3/33 câu, người xem nghe "đọc lạ"); cắt lặng theo biên độ không bỏ được — giờ cắt bằng `cat_gon_tts.py` | `test:TestCatGonTTS` `script:cat_gon_tts.py` |
| 2026-10-10 | Hai cuộc kháng chiến – Anh hùng LLVT (tư liệu + nhân chứng + nghĩa trang) | 3:26 | Hình ngắn hơn tiếng 26 s (xfade lặng lẽ bỏ cảnh sau một cảnh hụt) mà `video_qa` vẫn PASS — giờ kiểm `av_length` | `test:TestVideoQaHinhLechTieng` |
| 2026-10-10 | Hai cuộc kháng chiến – Anh hùng LLVT (tư liệu + nhân chứng + nghĩa trang) | 3:26 | 5 vòng render hỏng vì tpad+trim rớt khung PNG, blend+settb lệch mốc, cache thiếu độ dài, bộ chấm ghi đè bộ đã duyệt; ASR hội thoại phòng vọng phải nghe khúc 20 s độc lập | `doc:phong-cach-att-news.md` |
| 2026-10-09 | Địa bàn đứng chân (lời kể ông Tiến + hội thoại Oai–Thành) | — | Lệnh ffmpeg gộp ~26 đầu vào treo cứng 2 lần (CPU 0) — dựng từng cảnh + xfade cụm 5; whisper chép `initial_prompt` thành lời; file jobs Remotion dính `` | `doc:phong-cach-att-news.md` |
| 2026-10-09 | Địa bàn đứng chân (lời kể ông Tiến + hội thoại Oai–Thành) | — | Banner tên và ảnh tư liệu đè phụ đề 2 dòng: chốt `BannerPhongSu dichLen 90`, `AnhTuLieu dichLen 80` | `doc:banner-phong-su.md` |
