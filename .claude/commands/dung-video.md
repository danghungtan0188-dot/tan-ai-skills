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

## ■ CỔNG DUYỆT 1 — dừng ở đây

Đưa người dùng: bảng bản yêu cầu (loại, cửa vào, độ dài, tỉ lệ, phong cách, phải có, không được),
bảng kế hoạch (đoạn / cảnh / chữ / âm thanh), và **một câu hỏi duy nhất** gom mọi `unknowns`. Rồi **dừng lượt**:
chưa ghép, chưa render.

Chỉ đi thẳng qua cổng 1 khi gợi ý nói rõ "tự động luôn / không cần duyệt" **và** `unknowns` rỗng.
Người dùng đồng ý → `gate_plan: "dong_y"`. Sửa → cập nhật `brief.json`, quay lại bước 3.

## 4. Dựng + kiểm tự động

Làm tiếp các bước còn lại của cửa vào (ghép → màu → đồ hoạ → âm thanh → phụ đề → render) rồi:

```bash
python scripts/video_qa.py <output> --strict --audio
```

và **xem khung hình** ở các mốc có chữ / đồ hoạ (chữ che mặt, phụ đề ngoài vùng an toàn, hình vỡ).
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
VIDEO QA:     PASS | FAIL (vòng <n>/3)
KIỂM HÌNH:    PASS | FAIL | NOT RUN
CỔNG 2:       chấp nhận | góp ý
OUTPUT:       <đường dẫn>
RÚT KN:       <số bài học đề xuất>
```
