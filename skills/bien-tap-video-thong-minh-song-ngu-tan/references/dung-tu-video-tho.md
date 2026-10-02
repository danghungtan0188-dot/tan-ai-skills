# Dựng bản tin từ video thô tự quay

Người dùng đưa cả thư mục clip chưa dựng → xem hết → cắt ghép thành **một** bản tin có logic
chuẩn truyền hình, **độ dài do người dùng đặt**.

Nếu người dùng chỉ nói “clip trong kho”, đọc [kho-clip.md](kho-clip.md) để tìm ở Desktop,
Documents và Google Drive trước khi chạy khảo sát.

Khác với đường chạy thường ở chỗ: ở đây `cut_authorized` buộc phải bật. Có hai cách hợp lệ:

1. Người dùng yêu cầu rõ “tự động tìm/xem/cắt ghép/dựng” trong yêu cầu hiện tại: xem như đã cho phép
   cắt trong đúng kho và đúng đầu ra đó; tạo plan với `--approved` và chạy liền tới QA.
2. Người dùng chỉ nói “xem/lập phương án”: in bảng đoạn và chờ duyệt, không dùng `--approved`.

Không lấy quyền của một yêu cầu cũ để cắt một kho mới hoặc đầu ra mới.

## Cần có gì trên máy

```bash
pip install opencv-python numpy Pillow
```

Thêm `ffmpeg` và `ffprobe` trong PATH. `survey_rushes.py` kiểm các thứ này ngay khi khởi động và
báo thiếu trước khi quét, chứ không chết giữa chừng.

## Phân vai

| Ai | Làm gì |
|---|---|
| `survey_rushes.py` | đo: thời lượng, khung, fps, cờ xoay, LUFS, mốc cắt cảnh, nét/sáng/động từng cảnh |
| **Claude** | **xem contact sheet, nhận ra cảnh nào là gì, chọn cảnh và viết lý do** |
| `build_edit_plan.py` | kiểm luật dựng, co giãn cho khớp độ dài, in bảng duyệt |
| Người dùng | duyệt bảng |
| `assemble.py` | ghép thật |

Máy không đoán nội dung. Số liệu chỉ nói cảnh **nét hay mờ**, không nói cảnh **quay cái gì**.

## Bước 1 — khảo sát

```bash
python scripts/survey_rushes.py "D:/quay/20-09" --recursive --out edit/rushes.json --sheet edit/contact.jpg
```

`--recursive` tìm mọi video trong các thư mục con nhưng bỏ qua `.git`, `node_modules`, `outputs`,
`render`, `edit`, `thumbs` và cache để không lấy nhầm video đã dựng. Chỉ dùng đúng kho người dùng chỉ
định; không quét cả Desktop, Documents hay toàn ổ đĩa nếu họ chưa đặt các vị trí đó vào phạm vi.

Rồi **mở `contact.jpg` ra xem hết**. Mỗi ô là một cảnh, nhãn ghi `clip.cảnh  t=giây  dài  tên file`;
nhãn đỏ là cảnh máy thấy mờ, tối hoặc rung. Đọc cả phần `CẢNH BÁO` in ra màn hình: clip câm, clip
khác tỉ lệ/fps, clip có cờ xoay.

Cảnh dưới 1,2 giây bị bỏ (thường là nháy sáng, lia ngang, lỡ tay). Muốn giữ thì hạ `--min-shot`.

## Bước 2 — chọn cảnh

Viết `chon-canh.json`. Cấu trúc theo **mục nội dung**, không theo thứ tự file:

```json
{"tieu_de": "Xã An Thạnh Thủy khám sức khỏe cho người cao tuổi",
 "muc": [
  {"id": "mo-dau", "ten": "Bối cảnh",
   "canh": [{"shot": "0.1", "co": "toan", "ly_do": "toàn cảnh sân trạm y tế, đặt địa điểm"}]},
  {"id": "dien-bien", "ten": "Diễn biến buổi khám",
   "canh": [{"shot": "2.3", "co": "trung", "in": 12.0, "out": 17.0, "ly_do": "bác sĩ đo huyết áp"},
            {"shot": "1.5", "co": "can", "ly_do": "cận tay lấy mẫu máu"}]},
  {"id": "phat-bieu", "ten": "Người dân nói",
   "canh": [{"shot": "3.2", "co": "trung", "loai": "phat_bieu", "in": 4.0, "out": 21.0,
             "ly_do": "câu trả lời trọn ý, không hụt đầu câu"}]}]}
```

- `co`: `toan` | `trung` | `can` — bắt buộc, và **đoạn đầu phải là `toan`**.
- `loai`: `broll` (mặc định) hoặc `phat_bieu`.
- `in`/`out`: giây trong clip gốc; bỏ trống thì lấy trọn cảnh.
- `ly_do`: bắt buộc. Không nghĩ ra lý do thì đừng đưa cảnh đó vào.
- `hinh` (tuỳ chọn): tên kiểu chuyển động trong khuôn — `zoom_cham`, `day_phai`, `nhanh_12`…
  Có dùng thì phải đưa `--khuon` cho cả `build_edit_plan.py` và `assemble.py`.
  Xem [khuon-tu-video-cu.md](khuon-tu-video-cu.md).

**Cách dựng cho ra chất bản tin:** mỗi mục mở bằng một cảnh rộng rồi siết dần vào cận; không để
hai cảnh cùng cỡ đứng cạnh nhau; xen cận cảnh chi tiết (tay, giấy tờ, thiết bị) giữa hai cảnh
trung cho đỡ đều đều; phát biểu đặt sau khi người xem đã thấy bối cảnh, không mở màn bằng
phát biểu.

## Bước 3 — lên kế hoạch và xin duyệt

```bash
python scripts/build_edit_plan.py edit/rushes.json edit/chon-canh.json --target 180 --approved --out edit/edit-plan.json
```

Luật máy kiểm (FAIL thì sửa `chon-canh.json` rồi chạy lại):

| Luật | Vì sao |
|---|---|
| b-roll 2,5–8 giây | dưới 2,5 s người xem chưa kịp hiểu; trên 8 s là lê thê |
| phát biểu ≥ 4 giây | ngắn hơn là câu nói bị cụt |
| b-roll không trùm qua mốc cắt cảnh | giữa đoạn sẽ có cú nhảy hình |
| không hai đoạn liền nhau cùng clip cùng cỡ cảnh | nhảy hình (jump cut) |
| đoạn đầu phải là cảnh toàn | mất bối cảnh thì khán giả không biết đang ở đâu |
| mỗi đoạn phải có lý do | chặn thói quen nhét cảnh cho đủ giờ |
| tổng khớp yêu cầu ±2 giây | đúng thời lượng người dùng đặt |

Co giãn **chỉ đụng b-roll** và không kéo quá ranh giới cảnh; phát biểu giữ nguyên vào/ra. Nếu
thiếu quá nhiều giây, máy báo cần thêm bao nhiêu cảnh — chọn thêm, đừng kéo dài cảnh cũ.

Bảng in ra có cột mục, cảnh, cỡ, loại, vào→ra, dài, vị trí và lý do. Nếu yêu cầu hiện tại đã nói rõ
**tự động dựng/cắt ghép**, `--approved` ghi quyền đó vào plan và có thể sang bước 4 ngay. Nếu chưa có
quyền, bỏ `--approved`, đưa nguyên bảng cho người dùng duyệt rồi tạo lại plan có `--approved`.

## Bước 4 — ghép và hoàn thiện

```bash
python scripts/assemble.py edit/edit-plan.json --out edit/rough.mp4 --rushes edit/rushes.json
```

**Chạy được hay không phụ thuộc kế hoạch:** `assemble.py` từ chối khi `cut_authorized` chưa true
(chưa duyệt), khi `valid: false` (kế hoạch còn lỗi), khi kế hoạch rỗng, hoặc khi thiếu clip /
thiếu file `--voice` / `--rushes`. Ghép xong nó **tự `ffprobe` lại file thật** và báo lỗi nếu
thời lượng, khung hình, fps hoặc luồng tiếng không khớp — render xong chưa phải là xong.

- Nối hard cut, chuẩn hoá mọi clip về 1920×1080 / 30 fps / 48 kHz.
- `--rushes` cân mức tiếng từng clip bằng **một mức gain cố định** đo sẵn — clip này không to hơn
  clip kia, mà dải động vẫn giữ nguyên.
- Có lời đọc thì `--voice vo.wav`; tiếng hiện trường hạ còn `--nat-db` (mặc định −12 dB) bằng gain
  cố định, **không ducking động**. Tiếng hiện trường là bằng chứng sự việc, phải nghe rõ.
  Lời đọc ngắn hơn phim thì được bù im lặng, dài hơn thì bị cắt — tiếng luôn dài đúng bằng kế hoạch.
- Không chuẩn hoá LUFS ở đây — để `render_att.py` làm một lần ở cuối, tránh chồng hai lớp.

Xong `rough.mp4` thì quay lại đường chạy quen: `detect_scenes.py` → phụ đề song ngữ →
`make_lower_thirds_ass.py` → `render_att.py` → `qa.py`.

## Bước 5 — kiểm theo kế hoạch, không kiểm theo nguồn

Bản dựng từ nhiều clip **cố tình** khác thời lượng nguồn, nên `--cut-authorized yes` sẽ bỏ luôn
phép kiểm thời lượng. Thay vào đó kiểm theo chính kế hoạch đã duyệt:

```bash
python scripts/qa.py edit/final.mp4 --plan edit/edit-plan.json --cut-authorized yes \
  --tail 4 --captions edit/bilingual.json
```

- **LỖI** nếu thời lượng lệch kế hoạch quá 0,5 giây, hoặc kế hoạch lệch yêu cầu quá 2 giây.
- **CẢNH BÁO** nếu không dò thấy mốc cắt ở đúng vị trí đã duyệt — nghĩa là một đoạn có thể bị
  rơi hoặc lặp. Hai cảnh quá giống nhau thì `scdet` có thể sót, nên đây là cảnh báo để xem tay,
  không phải lỗi chặn.

Muốn biết có cắt vào giữa câu nói không thì chạy lại bước 3 với `--kiem-tieng`: máy đo mức âm
quanh từng mốc vào/ra và cảnh báo chỗ đang có tiếng to (mặc định trên −30 dBFS). Máy không phân
biệt được tiếng nói với tiếng máy nổ — cảnh báo là để **nghe lại**, không phải để tin ngay.

## Sai sót phải tránh

- Đoán nội dung cảnh từ tên file hoặc từ số liệu nét/sáng. Phải nhìn ảnh.
- Cắt trước rồi mới đưa bảng. Duyệt trước, cắt sau.
- Kéo dài cảnh cho đủ giờ thay vì chọn thêm cảnh — hình sẽ ì.
- Để clip dọc (có cờ xoay) lọt vào mà không kiểm chiều hình: `assemble.py` sẽ thêm hai dải đen.
- Quên clip câm: `assemble.py` tự chèn im lặng đúng độ dài, nhưng đoạn đó **mất tiếng hiện trường**,
  phải tính trước có lời đọc hay không.
