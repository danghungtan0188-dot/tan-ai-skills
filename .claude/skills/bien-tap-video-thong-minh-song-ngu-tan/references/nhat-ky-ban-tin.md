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
