# Danh sách giọng dựng sẵn (VieNeu-TTS-v3-Turbo)

Nguồn: `src/vieneu/assets/voices_v3_turbo.json` trong repo [pnnbao97/VieNeu-TTS](https://github.com/pnnbao97/VieNeu-TTS) (Apache-2.0). 14 giọng, 3 vùng miền, 3 phong cách đọc (`tu_nhien`, `tin_tuc`, `doc_truyen`).

## Giọng dùng cho `--voice nam` / `--voice nu` (mặc định của skill này)

| Shortcut | Tên giọng thật | Giới tính | Vùng | Phong cách |
|---|---|---|---|---|
| `nam` | Minh Triết | Nam | **Nam** | tin_tuc |
| `nu` | Thùy Dung | Nữ | **Nam** | tin_tuc |

Đây là 2 giọng nam/nữ miền Nam, phong cách đọc tin tức duy nhất có sẵn trong bộ 14 giọng — dùng đúng theo yêu cầu "giọng nam, nữ miền Nam, phong cách đọc tin tức".

## Toàn bộ 14 giọng

| Tên giọng | Giới tính | Vùng | Phong cách |
|---|---|---|---|
| Minh Đức | Nam | Bắc | tin_tuc |
| Phạm Tuyên | Nam | Bắc | tu_nhien |
| Thanh Bình | Nam | Bắc | doc_truyen |
| Trúc Ly | Nữ | Bắc | tu_nhien |
| Ngọc Linh | Nữ | Bắc | doc_truyen |
| Đoan Trang | Nữ | Bắc | tu_nhien |
| Mai Anh | Nữ | Bắc | tin_tuc |
| Quang Sơn | Nam | Trung | tu_nhien |
| Ngọc Trân | Nữ | Trung | tu_nhien |
| Thái Sơn | Nam | Nam | doc_truyen |
| Xuân Vĩnh | Nam | Nam | tu_nhien |
| Thục Đoan | Nữ | Nam | doc_truyen |
| **Minh Triết** | **Nam** | **Nam** | **tin_tuc** |
| **Thùy Dung** | **Nữ** | **Nam** | **tin_tuc** |

Dùng tên giọng trực tiếp qua `--voice "Tên giọng"`, ví dụ `--voice "Xuân Vĩnh"` để có giọng nam miền Nam phong cách tự nhiên (không phải tin tức), hoặc `--voice "Thục Đoan"` cho giọng nữ miền Nam phong cách kể chuyện.

Style (`--style`) áp dụng độc lập với tên giọng — có thể ép `--style tu_nhien` lên giọng `Minh Triết` nếu muốn giọng đọc tin nghe tự nhiên hơn, dù giọng này vốn được huấn luyện cho phong cách tin_tuc là chính.

## Giọng đã nhân bản (voice cloning)

Sau khi chạy `clone_voice.py enroll --name "..."`, tên giọng đó xuất hiện thêm trong danh sách trên khi chạy `synthesize.py` (không cần chỉnh sửa bảng này). Xem [../INSTALL.md](../INSTALL.md) mục nhân bản giọng.
