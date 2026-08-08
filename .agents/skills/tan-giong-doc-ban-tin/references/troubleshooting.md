# Xử lý lỗi thường gặp

Luôn chạy `python scripts/check_env.py` trước để khoanh vùng lỗi.

## "Chưa cài được thư viện 'vieneu'"
Chạy `pip install vieneu` (CPU) hoặc làm theo mục GPU trong [INSTALL.md](../INSTALL.md). Nếu dùng `uv`, nhớ kích hoạt đúng virtualenv trước (`.venv\Scripts\activate`).

## `pip install vieneu` báo lỗi không tìm được wheel (onnxruntime, tokenizers...)
Thường do Python quá mới (3.13/3.14) mà các gói ML biên dịch sẵn (wheel) chưa kịp phát hành cho phiên bản đó. Khắc phục: tạo virtualenv với Python 3.11 hoặc 3.12:
```bash
uv venv --python 3.12
.venv\Scripts\activate
pip install vieneu
```

## Nhân bản giọng (`clone_voice.py enroll`) báo lỗi liên quan `torch`/`cuda`
Bản CPU/ONNX tối giản có thể chưa hỗ trợ đủ để nhân bản giọng trên máy đó. Cài thêm nhóm GPU/PyTorch rồi thử lại:
```bash
pip install torch==2.8.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cu128
pip install "transformers==4.57.6"
pip install vieneu
```
Cần GPU NVIDIA hỗ trợ CUDA ≥ 12.8. Không có GPU NVIDIA vẫn dùng được **giọng dựng sẵn** (`--voice nam` / `--voice nu`...) bình thường trên CPU — chỉ riêng bước **nhân bản giọng của bạn** mới cần GPU.

## "Không tìm thấy giọng '...'"
Gõ sai tên hoặc dấu tiếng Việt (tên giọng có dấu, ví dụ `"Xuân Vĩnh"` chứ không phải `"Xuan Vinh"`). Xem đúng chính tả trong [voices.md](voices.md), hoặc chạy:
```bash
python -c "from vieneu import Vieneu; v=Vieneu(); print(v.list_preset_voices())"
```

## Không có file MP3 sau khi chạy `synthesize.py`
Script chỉ cảnh báo và bỏ qua bước MP3 nếu không thấy `ffmpeg` trong PATH — file WAV vẫn được tạo bình thường. Cài ffmpeg:
```bash
winget install Gyan.FFmpeg
```
Mở lại terminal (PATH chỉ cập nhật cho phiên mới) rồi chạy lại.

## File DOCX đọc ra rỗng hoặc lỗi
- Kiểm tra file không phải `.doc` (Word 97-2003 cũ) — chỉ hỗ trợ `.docx`. Mở lại bằng Word/LibreOffice và "Save As" sang `.docx`.
- Nếu văn bản nằm trong bảng (table) thay vì đoạn văn thường, `read_script.py` hiện chỉ đọc `document.paragraphs` — chuyển nội dung ra đoạn văn thường trước khi đọc.

## Giọng đọc sai số/ngày tháng
Số và ngày tháng được VieNeu-TTS (qua `sea-g2p`) tự động chuẩn hoá — **không** phải do `normalize_vi.py` xử lý. Nếu đọc sai, khả năng cao là định dạng số/ngày không theo chuẩn phổ biến (ví dụ ngày viết `2026-08-04` thay vì `04/08/2026`) — thử viết lại theo định dạng Việt Nam quen thuộc (`ngày/tháng/năm`).

## Một đoạn cụ thể bị bỏ qua (script vẫn chạy tiếp, in "LOI ở đoạn N")
`synthesize.py` cố ý KHÔNG dừng toàn bộ khi một đoạn lỗi — nó ghi lại và tiếp tục các đoạn còn lại, rồi tổng kết ở cuối. Xem log lỗi cụ thể của đoạn đó (thường do đoạn quá dài bất thường, hoặc chứa ký tự lạ) và sửa lại đoạn đó trong file kịch bản gốc.

## Giọng nhân bản biến mất sau khi cập nhật `vieneu`
Không thể xảy ra với skill này — giọng nhân bản được lưu ở `~\.tan-giong-doc-ban-tin\voices\giong_cua_toi.json` (ngoài thư mục cài đặt `vieneu`), không bị `pip install --upgrade vieneu` ghi đè. Nếu vẫn mất, kiểm tra file đó còn tồn tại hay không.
