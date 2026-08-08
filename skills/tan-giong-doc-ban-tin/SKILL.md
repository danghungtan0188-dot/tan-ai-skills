---
name: tan-giong-doc-ban-tin
description: Tổng hợp giọng đọc bản tin tiếng Việt từ kịch bản TXT/DOCX bằng VieNeu-TTS (Apache-2.0, https://github.com/pnnbao97/VieNeu-TTS). Hỗ trợ giọng nam/nữ miền Nam dựng sẵn phong cách đọc tin tức, nhân bản và lưu giọng nói của người dùng từ file WAV mẫu, tự động mở rộng chữ viết tắt tiếng Việt (số và ngày tháng đã được thư viện tự chuẩn hoá), tự chia đoạn dài, xuất WAV 48kHz và MP3. Kích hoạt khi người dùng cần đọc bản tin/kịch bản tiếng Việt thành giọng nói, tạo audio bản tin, lồng tiếng bằng giọng nam/nữ miền Nam, hoặc nhân bản giọng đọc của chính họ để dùng lại.
---

# Tân — Giọng đọc bản tin

## Phạm vi

Hỗ trợ: đọc kịch bản/bản tin tiếng Việt (`.txt`, `.docx`) thành file âm thanh; chọn giọng nam hoặc nữ miền Nam dựng sẵn, phong cách đọc tin tức (mặc định), hoặc bất kỳ giọng nào trong 14 giọng dựng sẵn của VieNeu-TTS-v3-Turbo; nhân bản và lưu lại giọng nói của người dùng từ một file WAV mẫu để tái sử dụng; mở rộng chữ viết tắt tiếng Việt thường gặp trong bản tin (hành chính, chức danh, giao thông...) trước khi tổng hợp; xuất WAV 48kHz và MP3.

Không làm: không tự động thêm hoặc sửa nội dung bản tin (chỉ đọc nguyên văn, có chuẩn hoá chữ viết tắt/số/ngày để phát âm đúng); không chỉnh sửa mã nguồn của thư viện `vieneu` — skill chỉ gọi API công khai của gói đã cài qua `pip`/`uv`, không vendor lại source code; không tự lưu giọng nhân bản vào thư mục cài đặt của `vieneu` (tránh mất dữ liệu khi nâng cấp gói); không đảm bảo nhân bản giọng hoạt động trên mọi máy — máy không có GPU NVIDIA có thể cần cài thêm bộ PyTorch (xem [INSTALL.md](INSTALL.md)).

## Nguồn & giấy phép

Dựa trên thư viện [VieNeu-TTS](https://github.com/pnnbao97/VieNeu-TTS) của Phạm Nguyễn Ngọc Bảo, phát hành theo **giấy phép Apache License 2.0** (tự do sử dụng, kể cả thương mại, chỉ cần giữ thông báo bản quyền/giấy phép gốc). Skill này gọi gói PyPI `vieneu` chính thức — không sao chép mã nguồn của repo vào đây. Khi trích dẫn nguồn gốc mô hình, tham khảo phần Citation trong README của repo gốc.

## Cài đặt

Xem [INSTALL.md](INSTALL.md) — hướng dẫn từng bước cho Windows (uv/pip, CPU hoặc GPU, ffmpeg, kiểm tra môi trường bằng `scripts/check_env.py`). **Chạy `python scripts/check_env.py` trước khi dùng lần đầu.**

Không có API key hay dịch vụ trả phí nào liên quan — VieNeu-TTS chạy hoàn toàn offline trên máy sau khi tải mô hình lần đầu.

## Quy trình cốt lõi

1. **Kiểm tra môi trường.** Chạy `python scripts/check_env.py` nếu chưa chắc máy đã sẵn sàng (Python, `vieneu`, `ffmpeg`, `python-docx`, GPU tuỳ chọn).
2. **Xác nhận kịch bản đầu vào** với người dùng: đường dẫn file `.txt`/`.docx`, có cần nhân bản giọng riêng không, giọng nam hay nữ (hoặc tên giọng cụ thể), phong cách đọc.
3. **(Tuỳ chọn) Nhân bản giọng của người dùng** nếu họ cung cấp file WAV mẫu (3–8 giây, giọng sạch):
   ```bash
   python scripts/clone_voice.py enroll --name "Giọng của tôi" --wav duong_dan/mau.wav
   ```
   Giọng được lưu tại `~/.tan-giong-doc-ban-tin/voices/giong_cua_toi.json`, dùng lại được ở bước 4 qua `--voice "Giọng của tôi"`. Nếu lỗi liên quan `torch`/`cuda`, xem [references/troubleshooting.md](references/troubleshooting.md).
4. **Tổng hợp giọng đọc:**
   ```bash
   python scripts/synthesize.py --input duong_dan/ban_tin.docx --voice nam
   python scripts/synthesize.py --input duong_dan/ban_tin.txt --voice nu --style tin_tuc
   python scripts/synthesize.py --input duong_dan/ban_tin.txt --voice "Giọng của tôi"
   ```
   `--voice nam` / `--voice nu` là hai giọng miền Nam, phong cách tin tức, dựng sẵn (Minh Triết / Thùy Dung — xem [references/voices.md](references/voices.md) cho toàn bộ 14 giọng). Script tự: đọc TXT/DOCX → tách đoạn → mở rộng chữ viết tắt (`scripts/normalize_vi.py`, tự điển ở [references/abbreviations.json](references/abbreviations.json)) → gọi VieNeu-TTS tổng hợp từng đoạn (thư viện tự chuẩn hoá số/ngày tháng và tự chia nhỏ đoạn dài ở tầng phoneme) → ghép các đoạn bằng khoảng lặng → lưu WAV 48kHz → chuyển MP3 bằng `ffmpeg`.
5. **Kiểm tra kết quả** với người dùng: nghe thử file WAV/MP3 xuất ra (mặc định ở `outputs/`), báo lại số đoạn lỗi nếu có (script tiếp tục chạy các đoạn còn lại thay vì dừng hẳn, và tổng kết ở cuối).
6. **Nếu có lỗi**, tra [references/troubleshooting.md](references/troubleshooting.md) trước khi tự đoán nguyên nhân.

## Khi nào chạy script

- `scripts/check_env.py` — kiểm tra môi trường trước khi dùng lần đầu, hoặc khi có lỗi không rõ nguyên nhân.
- `scripts/clone_voice.py enroll|list|remove` — nhân bản/quản lý giọng nói riêng của người dùng.
- `scripts/synthesize.py` — lệnh chính: kịch bản → WAV 48kHz + MP3. Chạy `--help` để xem đầy đủ tuỳ chọn (`--style`, `--gap-ms`, `--mp3-bitrate`, `--out-dir`, `--no-mp3`, `--abbrev-dict`, `--no-abbrev`...).
- `scripts/normalize_vi.py "<văn bản>"` — chỉ để xem trước kết quả mở rộng viết tắt mà không tổng hợp giọng (hữu ích khi debug tự điển).
- `scripts/read_script.py <file>` — chỉ để xem trước file được tách đoạn thế nào, không tổng hợp giọng.

Mỗi script hỗ trợ `--help`.

## Ví dụ sử dụng

```bash
# Kiểm tra môi trường lần đầu
python scripts/check_env.py

# Đọc thử ví dụ có sẵn bằng giọng nam miền Nam, phong cách tin tức
python scripts/synthesize.py --input examples/example_ban_tin.txt --voice nam

# Đọc bằng giọng nữ, xuất vào thư mục riêng với tên file riêng
python scripts/synthesize.py --input ban_tin.docx --voice nu --out-dir outputs/2026-08-04 --out-name sang

# Nhân bản giọng của người dùng rồi dùng lại
python scripts/clone_voice.py enroll --name "Giọng của tôi" --wav mau_giong.wav
python scripts/synthesize.py --input ban_tin.txt --voice "Giọng của tôi" --style tin_tuc

# Chỉ xuất WAV, không cần MP3, khoảng lặng giữa đoạn dài hơn
python scripts/synthesize.py --input ban_tin.txt --voice nam --no-mp3 --gap-ms 700

# Xem trước chữ viết tắt được mở rộng thế nào (không tổng hợp giọng)
python scripts/normalize_vi.py "UBND TP.HCM họp cùng CSGT về ATGT."
```

## Xử lý dữ liệu thiếu và giả định

- Người dùng chưa nói rõ giọng nam hay nữ: hỏi lại trước khi chạy `synthesize.py` (mặc định của script là `nam` nếu không truyền `--voice`, nhưng nên xác nhận với người dùng thay vì tự chọn).
- File kịch bản chứa cả tiêu đề lẫn nhiều mục tin riêng biệt: mỗi đoạn (ngăn bởi dòng trống) được tổng hợp và ghép nối bằng khoảng lặng — không tự chia lại thành nhiều file trừ khi người dùng yêu cầu.
- Chữ viết tắt không có trong tự điển mặc định ([references/abbreviations.json](references/abbreviations.json)): có thể thêm quy tắc mới vào file JSON đó (có `_ghi_chu` giải thích định dạng) hoặc dùng `--abbrev-dict` trỏ tới tự điển riêng — không tự bịa cách đọc nếu không chắc.
