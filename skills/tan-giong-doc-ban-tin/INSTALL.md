# Cài đặt trên Windows

Skill này **không đóng gói lại mã nguồn** của [VieNeu-TTS](https://github.com/pnnbao97/VieNeu-TTS) (Apache-2.0) — nó chỉ gọi gói Python `vieneu` đã công bố chính thức trên PyPI. Vì vậy không có "mã nguồn lõi" nào nằm trong skill để chỉnh sửa; nếu cần thay đổi hành vi lõi (mô hình, phonemizer...), việc đó thuộc về nâng cấp gói `vieneu`, không phải sửa file trong skill.

## 0. Kiểm tra nhanh

Sau khi làm xong các bước dưới, chạy:
```bash
python scripts/check_env.py
```
Script này tự kiểm tra Python, `vieneu`, `ffmpeg`, `python-docx`, PyTorch/GPU và báo lỗi kèm lệnh khắc phục cụ thể.

## 1. Cài `uv` (khuyến nghị) hoặc dùng `pip` có sẵn

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```
`uv` không bắt buộc — có thể dùng thẳng `pip` ở bước 3 nếu đã có Python cài sẵn.

## 2. (Khuyến nghị) Tạo virtual environment riêng

Máy chạy Python rất mới (ví dụ 3.13/3.14) đôi khi chưa có sẵn bản wheel biên dịch cho một số gói ML (`onnxruntime`, `tokenizers`). Để tránh lỗi cài đặt, ghim về Python 3.12:
```bash
uv venv --python 3.12
.venv\Scripts\activate
```
Nếu `pip install vieneu` ở bước sau chạy trơn tru với Python bạn đang có, có thể bỏ qua bước này.

## 3. Cài gói `vieneu`

Chọn **một** trong hai lựa chọn:

### Lựa chọn A — CPU (khuyến nghị cho hầu hết máy, kể cả không có GPU)
```bash
pip install vieneu
```
Chạy giọng đọc dựng sẵn (kể cả 2 giọng nam/nữ miền Nam phong cách tin tức) hoàn toàn trên CPU qua ONNX Runtime, không cần PyTorch. **Lưu ý:** một số bản `vieneu` giới hạn tính năng nhân bản giọng (voice cloning) trên CPU — nếu gặp lỗi ở bước nhân bản giọng của bạn, chuyển sang Lựa chọn B.

### Lựa chọn B — GPU (NVIDIA CUDA ≥ 12.8) — cần cho nhân bản giọng chắc chắn hoạt động
```bash
pip install torch==2.8.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cu128
pip install "transformers==4.57.6"
pip install vieneu
```
Yêu cầu GPU NVIDIA + [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-downloads). Nếu không có GPU NVIDIA, dùng Lựa chọn A — vẫn nghe được đầy đủ 14 giọng dựng sẵn, chỉ riêng bước tự nhân bản giọng của bạn có thể không khả dụng.

## 4. Cài phụ thuộc riêng của skill (đọc file DOCX)

```bash
pip install python-docx
```
(hoặc: `pip install -r scripts\requirements.txt`)

## 5. Đảm bảo có `ffmpeg` (để xuất MP3)

Kiểm tra:
```bash
ffmpeg -version
```
Nếu chưa có:
```bash
winget install Gyan.FFmpeg
```
Mở lại terminal sau khi cài để PATH cập nhật. Không có `ffmpeg` vẫn dùng được skill — chỉ mất bước xuất MP3 (vẫn có WAV 48kHz).

## 6. Chạy thử với ví dụ có sẵn

```bash
cd skills\tan-giong-doc-ban-tin
python scripts\synthesize.py --input examples\example_ban_tin.txt --voice nam
```
Lần chạy đầu sẽ tự tải mô hình từ Hugging Face (vài trăm MB, cần mạng) — các lần sau dùng lại cache, không cần mạng.

Kết quả nằm ở `outputs\example_ban_tin.wav` và `outputs\example_ban_tin.mp3`.

## 7. (Tuỳ chọn) Nhân bản giọng của bạn

Chuẩn bị 1 file WAV mẫu, 3–8 giây, giọng rõ, ít tạp âm nền:
```bash
python scripts\clone_voice.py enroll --name "Giọng của tôi" --wav "C:\đường\dẫn\giong_toi.wav"
```
Giọng được lưu tại `%USERPROFILE%\.tan-giong-doc-ban-tin\voices\giong_cua_toi.json` — **không** ghi đè vào thư mục cài đặt của `vieneu`, nên an toàn khi nâng cấp gói sau này.

Dùng lại:
```bash
python scripts\synthesize.py --input ban_tin.docx --voice "Giọng của tôi"
```

## Gặp lỗi?

Xem [references/troubleshooting.md](references/troubleshooting.md).
