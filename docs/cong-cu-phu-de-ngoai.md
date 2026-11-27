# Công cụ phụ đề bên ngoài: VideoCaptioner, WhisperX, Subtitle Edit

Cài ngày 27/11/2026. Ba repo đã fork về `danghungtan0188-dot/`. **Chỉ ghi cách cài và cách dùng, không chép mã vào repo này** (VideoCaptioner là GPL-3.0).

| Công cụ | Bản | Giấy phép | Fork | Trên máy | Chạy được? |
|---|---|---|---|---|---|
| Subtitle Edit | 5.4.0 | MIT | [subtitleedit](https://github.com/danghungtan0188-dot/subtitleedit) | `D:\GitHub\SubtitleEdit-app\SubtitleEdit.exe` (bản portable, sha256 khớp bản phát hành) | ✅ Mở được, chưa ký số nhưng không bị chặn |
| VideoCaptioner | 1.4.2 | GPL-3.0 | [VideoCaptioner](https://github.com/danghungtan0188-dot/VideoCaptioner) | `D:\GitHub\VideoCaptioner\.venv` (Python 3.11), lệnh `videocaptioner` qua `~\.local\bin\videocaptioner.cmd` | ✅ Lệnh chạy, `doctor` đạt phần cơ bản |
| WhisperX | 3.8.6 | BSD-2 | [whisperX](https://github.com/danghungtan0188-dot/whisperX) | `D:\GitHub\whisperX\.venv` (Python 3.11, torch 2.8 CPU, 1,9 GB) | ❌ Smart App Control chặn `ctranslate2.dll` (chưa ký số) |

## Subtitle Edit: sửa phụ đề bằng tay

Dùng sau khi máy tạo phụ đề (`.srt` của `att-news-graphics`, `video-use`, VideoCaptioner): căn lại thời gian theo sóng âm, sửa chữ, kiểm câu quá dài/quá nhanh, đổi định dạng (SRT, ASS, VTT…). Không cần cài, bấm đúp `SubtitleEdit.exe`.

## VideoCaptioner: chép lời, dịch, in phụ đề có kiểu

- Skill Claude Code gốc đã chép nguyên vào `~/.claude/skills/videocaptioner/SKILL.md` (gọi `/videocaptioner`). Không sửa skill gốc.
- Cài lại trên máy mới:
  ```powershell
  cd D:\GitHub; git clone https://github.com/danghungtan0188-dot/VideoCaptioner.git; cd VideoCaptioner
  uv venv --python 3.11 .venv
  uv pip install --python .venv\Scripts\python.exe "videocaptioner==1.4.2" httpx
  ```
  Bản 1.4.2 **quên khai báo `httpx`**, thiếu là lệnh lỗi ngay; phải cài thêm. Sau đó tạo `~\.local\bin\videocaptioner.cmd` một dòng: `@"D:\GitHub\VideoCaptioner\.venv\Scripts\videocaptioner.exe" %*`, rồi chép `skills\SKILL.md` vào `~/.claude/skills/videocaptioner/`.
- **Giới hạn với tiếng Việt:** nhận diện miễn phí `bijian`/`jianying` **chỉ có tiếng Trung và tiếng Anh**. Tiếng Việt phải dùng `whisper-api` (đám mây OpenAI, trả phí) hoặc `whisper-cpp` (trên máy, chưa cài).
- **Quyền riêng tư:** `bijian`/`jianying` gửi âm thanh lên máy chủ ở Trung Quốc; dịch Bing/Google cũng đi qua mạng. Không dùng cho tư liệu chưa phát sóng hay có thông tin cá nhân.
- Làm mượt câu, ngắt câu bằng AI, lồng tiếng cần khóa API trả phí: **chưa cài khóa**. Hỏi người dùng trước khi dùng (`guard_tra_phi`).
- Dùng được ngay (không cần mạng, không trả phí): in phụ đề `.srt` có sẵn lên video với kiểu chữ đẹp: `videocaptioner synthesize video.mp4 -s phu-de.srt --subtitle-mode hard -o ra.mp4` (xem `videocaptioner synthesize --help`).

## WhisperX: căn thời gian từng từ

Cài đủ (`import whisperx` được) nhưng **chạy bị chặn**: Smart App Control chặn DLL chưa ký số của `ctranslate2` 4.9.0. Cùng lúc `faster_whisper` ở Python 3.14 hệ thống cũng bị chặn ở thư viện khác. Không tự tắt Smart App Control (cài đặt bảo mật, tắt rồi không bật lại được).

Cách chạy được (người dùng quyết):
1. Chạy trong WSL (Linux trong Windows; Smart App Control không xét file Linux). Cần cài WSL (quyền quản trị).
2. Chạy trên máy khác hoặc máy chủ đám mây có GPU.
3. Dùng `whisper-api` của OpenAI qua VideoCaptioner (trả phí, gửi âm thanh lên mạng).

Khi chạy được: mô hình `small`/`medium` + căn chỉnh `--align_model` tiếng Việt cho mốc thời gian từng từ: nền cho phụ đề nhảy chữ và cắt video dài thành short.
