---
description: Một cửa vào bán tự động — đưa tư liệu + vài gợi ý bằng lời, repo tự hiểu, lập kế hoạch, dừng ở 2 cổng duyệt, tự dựng, tự kiểm, tự sửa, rồi rút kinh nghiệm
argument-hint: <thư mục/file tư liệu> "<gợi ý: loại video, độ dài, phong cách, phải có, không được làm>"
---

Đầu vào: **$ARGUMENTS**

Vòng khép kín ở [docs/harness-video.md](docs/harness-video.md) mục 1. Đọc [rules/video.md](rules/video.md) trước.
Lệnh này **không tự dựng**: nó hiểu yêu cầu, chọn cửa vào đang có, giữ hai cổng duyệt, rồi giao việc dựng
cho cửa vào đó. Thư mục làm việc: `<thư mục tư liệu>/edit/` (cạnh tư liệu, không để trong repo).

## 1. Hiểu yêu cầu → `edit/brief.json`

Viết bản yêu cầu theo `VideoBrief` trong `data-contracts/video.schema.json`. Dùng **đúng khuôn này** —
đúng tên trường, không thêm trường khác (thông tin từng clip để dành cho bước phân tích):

```json
{
  "source": "<đường dẫn thư mục/file tư liệu, dạng chuỗi>",
  "request": "<nguyên văn gợi ý>",
  "video_type": "ban_tin | su_kien | tai_lieu | mang_xa_hoi | san_pham | thuyet_minh | tu_do",
  "route": "dung-tu-kho | video-news | edit-video | tan_studio",
  "target_duration": 60,
  "aspect_ratio": "16:9 | 9:16 | 1:1 | null",
  "platform": "facebook | tiktok | youtube | zalo | reels | shorts | khac | null",
  "style": "att-news | null",
  "must_have": [],
  "must_avoid": [],
  "unknowns": [],
  "cut_authorized": false,
  "gate_plan": "cho",
  "gate_final": "chua_toi"
}
```

- `request` = **nguyên văn** gợi ý, không tóm tắt.
- Chỉ điền thông số người dùng đã nói hoặc suy ra chắc chắn từ tư liệu. Không rõ → để `null` và ghi vào `unknowns`.
  **Độ dài** chưa có → luôn vào `unknowns`.
- `style`: loại `ban_tin` mà người dùng không nói khác → `att-news`
  ([phong-cach-att-news.md](skills/bien-tap-video-thong-minh-song-ngu-tan/references/phong-cach-att-news.md)).
- `cut_authorized` = `true` chỉ khi gợi ý nói rõ được cắt / rút ngắn.
- `gate_plan` = `"cho"`, `gate_final` = `"chua_toi"`.

**Bắt buộc** kiểm bản yêu cầu (script nằm trong repo `tan-ai-skills`). Chưa in `brief OK` thì sửa theo
thông báo rồi chạy lại — **không sang bước 2**:

```bash
python "C:/Users/DANG HUNG TAN/Documents/GitHub/tan-ai-skills/scripts/kiem_brief.py" <thư mục tư liệu>/edit/brief.json
```

## 2. Chọn cửa vào (`route`) — tự chọn, nói đã chọn gì

| Tư liệu | `route` | Làm theo |
|---|---|---|
| Thư mục nhiều clip thô | `dung-tu-kho` | `.claude/commands/dung-tu-kho.md` |
| 1 video + bản tin / sự kiện / hội nghị | `video-news` | `.claude/commands/video-news.md` |
| Kịch bản `.txt` / `.docx` (có hoặc không kèm ảnh/clip) | `tan_studio` | `tan_studio/README.md` → `python -m tan_studio chay <du-an.json>` |
| 1 video, yêu cầu khác | `edit-video` | `.claude/commands/edit-video.md` |

## 3. Phân tích + kế hoạch

Chạy phần **phân tích và lập kế hoạch** của cửa vào đã chọn (tới trước bước ghép/render của nó).
Kế hoạch phải thoả `must_have` / `must_avoid` trong `brief.json`; mục nào không làm được thì nói rõ.

**Mặc định tắt**, chỉ bật khi gợi ý nói rõ hoặc nằm trong `must_have`: nhạc, tiếng động, lọc màu, chuyển cảnh,
chuyển động máy, đổi khung hình. Câu chung như "làm cho hay / sinh động" không tính là đã yêu cầu các thứ này.

Có thẻ đồ hoạ → chọn theo câu nói bằng
[canh-theo-muc-dich.md](skills/motion-graphics-tan/references/canh-theo-muc-dich.md), chỉ đọc đúng một file phong cách đã chọn.

## ■ CỔNG DUYỆT 1 — dừng ở đây

Đưa người dùng **Thẻ cài đặt** đọc trong vài giây, không để trong khối code. Mỗi mục ghi nguồn:
_(yêu cầu)_ = người dùng đã nói, _(từ tư liệu)_ = đo được từ file, _(đề xuất)_ = AI chọn:

```markdown
### 🎬 <tên video> · cài đặt cần duyệt

<một câu nói sẽ làm gì>

**⚠️ Cần anh quyết** (bỏ mục này nếu `unknowns` rỗng)
- <mọi `unknowns`, gom vào một câu hỏi, có lựa chọn A / B>

- 🎯 **Mục tiêu:** loại video, cửa vào, độ dài _(…)_
- 🎞️ **Tư liệu:** file, thời lượng _(từ tư liệu)_
- ✂️ **Cắt:** giữ nguyên hoặc đoạn được cắt _(…)_
- 💬 **Phụ đề:** có/không, kiểu, vị trí không che mặt _(…)_
- 🔊 **Âm thanh:** chuẩn âm lượng; nhạc, tiếng động tắt _(…)_
- ✨ **Đồ hoạ:** từng thẻ kèm câu nói và giây xuất hiện _(…)_
- 🎨 **Hình:** giữ nguyên màu gốc _(…)_
- 📐 **Khung:** tỉ lệ, kích thước, FPS _(…)_
- 📁 **Giao:** đường dẫn file ra _(…)_
```

Rồi **dừng lượt**: chưa ghép, chưa render.

Chỉ đi thẳng qua cổng 1 khi gợi ý nói rõ "tự động luôn / không cần duyệt" **và** `unknowns` rỗng.
Người dùng đồng ý → `gate_plan: "dong_y"`. Sửa → cập nhật `brief.json`, quay lại bước 3.

## 4. Dựng + kiểm tự động

**Mẫu trước:** render đoạn 8–15 giây khó nhất (có đồ hoạ và phụ đề), tự kiểm, sửa xong mới render cả video.
Chỉ dừng cho người dùng xem mẫu khi gợi ý yêu cầu duyệt mẫu. Video ngắn hơn 20 giây thì bỏ qua bước này.

Có cắt (`cut_authorized: true`) → kiểm điểm cắt trước khi ghép, ghép xong kiểm lại với `--ra`.
Chỉ dời điểm cắt theo gợi ý của script, không tự cắt thêm lời:

```bash
python "C:/Users/DANG HUNG TAN/Documents/GitHub/tan-ai-skills/scripts/kiem_diem_cat.py" <nguồn> <kế hoạch.json> [--ra <video đã cắt>]
```

Làm tiếp các bước còn lại của cửa vào (ghép → màu → đồ hoạ → âm thanh → phụ đề → render) rồi:

```bash
python scripts/video_qa.py <output> --strict --audio
python "C:/Users/DANG HUNG TAN/Documents/GitHub/tan-ai-skills/scripts/kiem_phu_de_ocr.py" <output> <phụ đề.srt>
```

Script OCR thoát mã 3 = `NOT RUN` (máy thiếu Tesseract tiếng Việt), không phải PASS; khi đó soát chữ bằng mắt.

**Xem khung hình** ở các mốc có chữ / đồ hoạ (chữ che mặt, phụ đề ngoài vùng an toàn, hình vỡ): gộp thành một ảnh
nhiều khung, chỉ mở khung to khi nghi có lỗi hoặc script báo FAIL.
FAIL → sửa → render lại → kiểm lại, **tối đa 3 vòng**; vẫn FAIL thì dừng và báo người dùng lỗi gì.

## ■ CỔNG DUYỆT 2

Đưa đường dẫn video + kết quả QA. Hỏi: chấp nhận hay góp ý.
Góp ý → thêm vào `must_have` / `must_avoid`, `gate_final: "gop_y"`, quay lại bước 3 (kế hoạch mới lại qua cổng 1
nếu đổi độ dài, cắt bỏ đoạn dài hoặc đổi cửa vào). Chấp nhận → `gate_final: "chap_nhan"`.

## 5. Rút kinh nghiệm

Ngay sau khi chấp nhận: chạy `/rut-kinh-nghiem` cho video này. Bài học chỉ là **đề xuất**;
thành luật / test khi người dùng duyệt.

## Không được

- Không tự dùng dịch vụ trả phí (HeyGen…) khi gợi ý không nói rõ.
- Không ghi đè tư liệu gốc; không cắt thời lượng khi `cut_authorized` là `false`.
- Không báo xong khi QA chưa PASS hoặc người dùng chưa qua cổng 2.

## Báo cáo cuối

```text
BẢN YÊU CẦU:  edit/brief.json — <loại>, <cửa vào>, <độ dài>s, <tỉ lệ>
CỔNG 1:       đồng ý <lúc> | sửa <n> lần
MẪU:          PASS | FAIL | NOT RUN
ĐIỂM CẮT:     PASS | FAIL | NOT RUN
VIDEO QA:     PASS | FAIL (vòng <n>/3)
OCR PHỤ ĐỀ:   PASS | FAIL | NOT RUN
KIỂM HÌNH:    PASS | FAIL | NOT RUN
CỔNG 2:       chấp nhận | góp ý
OUTPUT:       <đường dẫn>
RÚT KN:       <số bài học đề xuất>
```
