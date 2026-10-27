# Bài học và chốt chặn

Mỗi bài học rút ra khi làm việc (ghi trong memory của Claude) được xếp vào một trong hai loại:

- **máy**: máy kiểm được, nên phải có chốt chặn thật (hook, test hoặc code). Cột "Chỗ neo" trỏ tới
  nó theo dạng `test:TenClass`, `hook:ten.py`, `code:duong/dan`. `tests/test_bai_hoc_chot_chan.py`
  bắt buộc mọi chỗ neo phải có thật.
- **người**: cần phán đoán theo ngữ cảnh, ép bằng máy sẽ chặn nhầm. Giữ ở memory và skill.

Có bài học mới: thêm một dòng vào đây. Nếu là loại "máy" thì viết chốt chặn trước, rồi mới ghi dòng.

| Bài học | Loại | Chốt chặn | Chỗ neo |
|---|---|---|---|
| Không ghi đè video gốc; nén bản Zalo ra file mới | máy | `guard_bash` chặn ffmpeg xuất ra chính file đầu vào | `hook:guard_bash.py` `test:TestGuardBash` |
| Commit chỉ file mình sửa | máy | `guard_bash` hỏi trước `git add -A`, `git add .`, `git commit -a` | `hook:guard_bash.py` `test:TestGuardBash` |
| Không báo đã xong khi chưa kiểm đúng | máy | `nhac_test` nhắc khi sửa code mà chưa chạy test sau lần sửa cuối | `hook:nhac_test.py` `test:TestNhacTest` |
| Đầu phiên phải đọc tiến độ | máy | `session_start` nạp `PROGRESS.md` vào ngữ cảnh | `hook:session_start.py` `test:TestSessionStart` |
| Xử lý âm thanh không bóp dải động | máy | `guard_video` chặn `loudnorm` một lượt thiếu `linear=true` | `hook:guard_video.py` `test:TestGuardVideo` |
| Chạy nhẹ, đừng làm nóng máy | máy | `guard_video` chặn x264/x265 thiếu `-preset faster` hoặc nhanh hơn; `tan_studio` mặc định `faster` | `hook:guard_video.py` `test:TestGuardVideo` `code:tan_studio/video.py` |
| Máy hay sập khi chạy nặng: một việc nặng một lúc | máy | `guard_video` chặn ffmpeg mới khi đang có `ffmpeg.exe` chạy | `hook:guard_video.py` `test:TestGuardVideo` |
| Không tự ý dùng dịch vụ trả phí (HeyGen) | máy | `guard_tra_phi` hỏi người dùng mỗi lần gọi HeyGen | `hook:guard_tra_phi.py` `test:TestGuardTraPhi` |
| remotion.exe bị Windows chặn | máy | Mẫu Remotion mới không dùng `OffthreadVideo` (trừ `NguoiNoiPip`, `PhuNu96`) | `test:TestRemotionKhongDungOffthreadVideo` |
| VieNeu-TTS: số phải viết thành chữ | máy | Chuẩn hóa số trước khi đọc | `code:tan_studio/normalize.py` `test:TestSoThanhChu` `test:TestNormalizeNumbers` |
| Đo bằng ASR phải nghe nhiều lần | máy | Chấm TTS nghe ở nhiều temperature | `code:tan_studio/evaluation.py` `test:TestDanhGiaTTS` |
| Rút kinh nghiệm sau mỗi video | máy | Mỗi dòng nhật ký bản tin phải trỏ tới test/script/tài liệu có thật | `test:TestNhatKyBanTin` |
| Script chạy nền phải lưu từng bước | người | Cách viết script, không dò được bằng lệnh | memory |
| Chọn bản TTS bằng điểm số | người | Quy trình chấm, đã có ở `tan_studio/evaluation.py` nhưng chọn công thức là phán đoán | memory |
| Chấm TTS bằng whisper small trên máy này | người | Cấu hình theo máy | memory |
| Bản tin ATT NEWS không dùng nhạc nền | người | Tùy thể loại; video quảng bá vẫn cần nhạc | memory, skill song ngữ |
| Phong cách phim tài liệu | người | Thẩm mỹ | memory |
| Phong cách edit ATT NEWS | người | Đã chốt trong `references/phong-cach-att-news.md` | skill song ngữ |
| Video quảng bá dịch vụ | người | Câu chữ trên thẻ | memory |
| Không tự ý cắt lời người nói | người | Phải nghe nội dung mới biết chỗ nào hỏng | memory |
| Người dùng chỉ file nào thì dùng file đó | người | Cách giao tiếp | memory |
| Xuất file vào thư mục người dùng mở (Desktop) | người | Đích xuất tùy việc; `outputs/` vẫn dùng cho nghiệm thu | memory |
| Tải video đúng thư mục | người | Câu dặn áp cho cả lô link | memory |
| Tự động định tuyến pipeline video | người | Cách làm việc | memory |
