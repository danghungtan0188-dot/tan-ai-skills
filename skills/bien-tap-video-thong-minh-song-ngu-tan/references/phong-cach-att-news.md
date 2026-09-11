# Phong cách ATT NEWS — bản tin xã An Thạnh Thủy

Bộ thông số chốt ngày 2026-08-20, cập nhật 2026-09-12 sau hai bản tin `06` (mừng thọ) và `sk2`
(khám sức khỏe). **Áp dụng y nguyên**, không tự đổi vị trí, màu, cỡ chữ.

Nguồn chuẩn: 1920×1080, 30 fps, có MC dẫn trong trường quay rồi chuyển sang phóng sự.

---

## 1. Bố cục cố định

| Vị trí | Thành phần | Thời gian |
|---|---|---|
| Trên phải | logo **ATT NEWS** | từ `studio_end` |
| Sát trái logo | logo phụ (vd logo y tế) | xuyên suốt |
| Trong màn hình TV | thẻ ảnh tin | trước `studio_end` |
| Dưới trái, sát mép | icon **Facebook · Zalo** | xuyên suốt |
| Dưới trái, trên icon | banner hoạt động / người phát biểu | từng đoạn |
| Giữa dưới | phụ đề song ngữ | ~99% thời lượng |

Toạ độ ở 1920×1080:

```
ATT NEWS       x=1612       y=130     (268×78)
logo phụ       x=1598-w     y=130     (cao 78, cách logo 14px)
thẻ ảnh TV     x=900        y=240     (1000×394)
Facebook/Zalo  x=46         y=H-h-46  (194×62, alpha 0.94)
```

Màn hình TV trong phông đo được: x 889–1920, y 231–646 (mép dưới bị bàn dẫn che). Phông dùng
chung mọi bản tin nên số đo này dùng lại được.

## 2. Quy trình một lượt

```bash
python scripts/detect_scenes.py INPUT --out scenes.json          # studio_end = mốc cắt đầu tiên
python scripts/build_bilingual.py transcribe INPUT --out asr_words.json
# viết cues.json rồi:
python scripts/build_bilingual.py build asr_words.json cues.json --out bilingual.json
python scripts/export_subtitles.py bilingual.json --mode ass --out-dir . --stem cap
python scripts/make_lower_thirds_ass.py lower-thirds.json lt.ass --scenes scenes.json
python scripts/make_tv_card.py ANH.jpg --label "..." --title "..." "..." --out card.png --preview studio.png
python scripts/make_att_bugs.py --out-dir .
python scripts/make_outro.py --title "..." "..." --sub "..." --logo att_news.png --out-dir outro
python scripts/render_att.py INPUT --captions cap.song-ngu.ass --lower-thirds lt.ass \
    --scenes scenes.json --card card.png --extra-logo logo.png --outro-dir outro --out OUT.mp4
python scripts/qa.py OUT.mp4 --source INPUT --tail 4 --captions bilingual.json
```

**Không ghi cứng mốc đắp logo.** Mỗi video một khác: video 06 là 30,4 s, sk2 là 26,3 s.
Đắp logo từ giây 0 sẽ chồng lên logo có sẵn trong phông trường quay.

## 3. Phụ đề song ngữ

Font mặc định đã là Arial (máy Windows không có DejaVu Sans — font thiếu thì dấu tiếng Việt lỗi).
Tiếng Anh 42 vàng nhạt MarginV 158; tiếng Việt 46 trắng MarginV 100.
**Mỗi cue ≤ 52 ký tự mỗi ngôn ngữ.** Chi tiết: [quy-trinh-song-ngu.md](quy-trinh-song-ngu.md).

## 4. Banner

`make_lower_thirds_ass.py --scenes scenes.json` tự chặn banner tràn sang cảnh khác — lỗi này
ffprobe không bắt được và từng suýt gắn tên người vào cảnh không có người đó.
Hộp banner đặt ở 65,5% chiều cao, kết thúc trên đỉnh dòng phụ đề tiếng Anh.
Cảnh ngắn hơn 4 giây thì rút banner cho vừa cảnh; cảnh 3 giây thì bỏ dòng phụ cho kịp đọc.

Tên và chức vụ **chỉ lấy từ kịch bản hoặc người dùng xác nhận**, không đoán từ khuôn mặt.

## 5. Âm thanh và mã hoá

Loudnorm **2 lượt linear** (đo trước, áp một mức gain cố định) — không bóp dải động.
`render_att.py` tự làm. Mã hoá `-preset faster -crf 20`: bản sk2 ra 64 MB so với 110 MB của
`preset medium`, mắt không thấy khác, máy đỡ nóng.

## 6. Kiểm trước khi giao

1. `qa.py OUT --source INPUT --tail <giây outro> --captions bilingual.json`
2. `check_translation.py bilingual.json` — bắt thiếu thuật ngữ, thiếu số liệu.
3. **Xem mắt tối thiểu 5 khung:** một cảnh trường quay, một cảnh ngay sau `studio_end`, một cảnh
   có banner hoạt động, một cảnh có banner người phát biểu, một khung outro.
4. Kiểm riêng: có chồng hai logo ở phần trường quay không; banner có đúng cảnh không.

## 7. Sai sót đã gặp — đừng lặp lại

| Sai sót | Cách tránh |
|---|---|
| Lời Việt chép từ ASR | ASR chỉ lấy mốc; lời Việt theo kịch bản gốc |
| Bản dịch rơi mất "People's Committee" khi gặp "UBND xã" | chạy `check_translation.py` |
| Banner tràn sang cảnh sau | `make_lower_thirds_ass.py --scenes` |
| Hộp banner đè dòng phụ đề tiếng Anh | vị trí mặc định đã sửa, có test giữ |
| Huy hiệu góc trên trái che mặt ở cảnh cuối | dựng ảnh ghép thử bằng PIL trên các cảnh trước khi render |
| Đắp logo ATT chồng logo có sẵn trong phông | chỉ đắp từ `studio_end` |
| Cắt nền trắng bằng floodfill làm thủng đĩa trắng bên trong logo | đặt logo lên thẻ trắng bo góc |
| Ảnh người dùng dán trong khung chat không phải file trên đĩa | tìm file mới nhất trên Desktop; đọc lại vì có thể bị ghi đè cùng tên |
| Render lại nhiều lần làm nóng máy | ghép thử bằng PIL trước; dừng lượt render cũ trước khi chạy lượt mới |
| Outro ngắn hơn 3 giây thì không kịp hiện logo và dòng kêu gọi | `make_outro.py` chặn dưới 3 giây |
| Outro chưa có nhạc | chỉ thêm khi người dùng đưa bản nhạc có quyền dùng |

Thông số ATT NEWS trong `tro-ly-video-ban-tin-tan/references/att-news.md` ghi icon mạng xã hội
"4–8% chiều rộng", lệch với thực tế 194 px (10%). **File này là nguồn chuẩn.**
