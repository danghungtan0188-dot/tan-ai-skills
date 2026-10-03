# CIT Voice Studio — nhà cung cấp TTS cục bộ tùy chọn

Dùng tài liệu này khi người dùng đã cài và đang mở CIT Voice Studio, hoặc yêu cầu dùng các giọng của ứng dụng đó. Đây là lớp kết nối độc lập qua API công khai; repo này không sao chép mã nguồn, model hay bộ cài CIT.

## Khi nên chọn

- Cần chọn trong danh sách giọng có sẵn của CIT hoặc tạo audio bằng ứng dụng đang chạy.
- Cần TTS cục bộ qua HTTP để agent/script khác gọi được.
- Cần dùng ngôn ngữ do model CIT hiện tại hỗ trợ; kiểm tra từ `/health`, không giả định theo phiên bản tài liệu.

Giữ VieNeu-TTS tích hợp trong `synthesize.py` làm mặc định khi CIT chưa chạy, khi cần hồ sơ giọng ATT đã đăng ký từ WAV, hoặc khi cần quy trình tiếp tục từng đoạn sau lỗi. CIT Voice Studio không nhận file WAV có sẵn để nhân bản; chỉ tạo giọng bằng quy trình đồng ý trực tiếp trong chính ứng dụng.

## Quy trình

```powershell
python scripts/cit_voice_api.py health
python scripts/cit_voice_api.py voices
python scripts/cit_voice_api.py generate --input ban-tin.txt --voice "Minh Đức" --output outputs/ban-tin.wav
```

Tên `voice_id` phải lấy từ lệnh `voices`; không suy đoán từ tên hiển thị. Với API phiên bản mới, đọc tài liệu đang chạy tại `http://127.0.0.1:8001/docs` hoặc `openapi.json` trước khi thêm endpoint/tham số mới.

Sau khi tạo, dùng `ffprobe` hoặc công cụ QA của video để xác nhận file đọc được, thời lượng > 0, sample rate/kênh phù hợp và nghe thử tên riêng, số liệu, ngày tháng. Từ điển phát âm được quản lý trong CIT; tự điển của skill này không tự đồng bộ sang CIT.

## An toàn và quyền riêng tư

- Mặc định client chỉ cho phép `localhost`. Không dùng `--allow-remote` nếu người dùng chưa chủ động bật API LAN.
- Khi gọi máy khác, bắt buộc `--api-key`; ưu tiên mạng tin cậy. HTTP trong LAN không mã hóa, vì vậy không gửi kịch bản nhạy cảm qua mạng không tin cậy.
- Không ghi khóa API vào repo, log, lệnh mẫu hay file cấu hình được commit.
- Chỉ dùng giọng cá nhân đã có sự đồng ý phù hợp. Không đổi tên một giọng gần giống thành tên MC/người thật.
- Giữ nhãn AI trong metadata do nhà cung cấp tạo và đề nghị ghi “Giọng đọc được tạo bằng AI” khi xuất bản công khai.

## Phần tốt đã có sẵn trong repo này

Không sao chép lại các tính năng mà pipeline hiện tại đã làm tốt: chuẩn hóa viết tắt/số/ngày, chia script dài, lưu từng phần để chạy tiếp, WAV 48 kHz, MP3 và hồ sơ giọng ATT ngoài Git. CIT chỉ là provider bổ sung, không thay đổi các hợp đồng đó.
