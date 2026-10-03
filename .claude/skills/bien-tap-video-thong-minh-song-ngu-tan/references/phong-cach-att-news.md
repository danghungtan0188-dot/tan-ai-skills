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

**Bản động (Remotion).** Cùng vị trí 65,5% chiều cao, cùng màu ATT NEWS, có hiệu ứng vào/ra:

```bash
python -m tan_studio do-hoa lower-third --dat ten="..." --dat chuc_vu="..." --thoi-luong 4 --anh 2   # xem 1 khung trước
python -m tan_studio do-hoa lower-third --dat ten="..." --dat chuc_vu="..." --thoi-luong 4 --out lt1.mov
python scripts/render_att.py INPUT ... --do-hoa lt1.mov,12.5     # đắp từ giây 12,5 — bỏ --lower-thirds ASS
```

Cùng cách đó cho `intro` (đặt ở giây 0, che cả phần trường quay — chỉ dùng khi nguồn không có MC mở đầu) và
`so-lieu` (thẻ số đếm lên + biểu đồ cột, phủ cả khung trong lúc giọng đọc vẫn chạy). Banner động **chưa tự né cảnh**
như `make_lower_thirds_ass.py --scenes`: tự chọn giây và `--thoi-luong` nằm gọn trong một cảnh (xem `scenes.json`).

## 5. Âm thanh và mã hoá

Loudnorm **2 lượt linear** (đo trước, áp một mức gain cố định) — không bóp dải động.
`render_att.py` tự làm. Mã hoá `-preset faster -crf 20`: bản sk2 ra 64 MB so với 110 MB của
`preset medium`, mắt không thấy khác, máy đỡ nóng.

## 5b. Khi nguồn đã được dựng sẵn

Có lúc người dùng đưa file **đã có phụ đề và banner đốt vào hình**. Kiểm trước bằng cách trích
vài khung ở phần phóng sự. Nếu đã có thì **bỏ trống `--captions`** và không tạo lower-third mới —
dựng đè sẽ thành hai lớp chữ chồng nhau. Chỉ thêm phần còn thiếu: logo, icon, thẻ/clip trong khung
TV, outro.

**Luôn hỏi hoặc tự tìm bản gốc chưa gắn chữ.** Ở bản tin liệt sĩ, bản sạch nằm trong `Downloads`
với đuôi tên `_khong_chu_loi_dan`, dài đúng bằng phần phóng sự. Có bản sạch thì xoá được đồ hoạ cũ
gọn ghẽ bằng `--replace`, thay vì che đè để lại vệt.

```bash
--replace "doan_sach.mp4,26.267"     # thay nguyên khung hình từ giây 26.267
```

Cách tính: `thời lượng đoạn = mốc cắt cảnh kế tiếp − mốc bắt đầu`; lấy từ `scenes.json`.

## 5c. Màn hình TV trong trường quay

Màn hình đo được: **x 889–1920, y 231–646**, tỉ lệ 2,49. Nguồn quay 16:9 (1,78) nên **không thể
vừa phủ kín vừa thấy trọn khung** — phải chọn:

| Cách | Lệnh | Đánh đổi |
|---|---|---|
| Thấy trọn khung, nền hai bên cùng tông phông | nền 1030×414 + `scale=-2:414` đặt giữa | Không mất gì. **Nên dùng.** |
| Phủ kín màn hình | `crop=1656:664:132:0,scale=1030:414` | Mất 29% chiều cao |
| Thu nhỏ, chừa hai bên | `scale=-2:410` | Hai bên lộ hình nền phông |

Nền hai bên: dải dọc RGB (182,208,242) → (120,164,210) — đo từ chính màn hình phông.

Clip trong khung TV:
```bash
ffmpeg -ss <bat_dau> -t <dai> -i NGUON -an -filter_complex \
 "[1:v]scale=-2:414,setpts=<he_so>*PTS,fps=30[fg];[0:v][fg]overlay=(W-w)/2:0:shortest=1,\
  drawbox=x=0:y=0:w=iw:h=ih:color=white@0.95:t=3[v]" ...
python render_att.py ... --card-video tv_clip.mp4 --card-pos 889,231
```
Hệ số `setpts` = thời lượng phần trường quay ÷ độ dài đoạn — giãn cho khớp, **không lặp**. Lặp 5 giây
thì cứ 5 giây lại giật một lần; nối chồng mờ đỡ hơn nhưng vẫn thấy.

**Cắt khung phải né đồ hoạ đã đốt sẵn trong nguồn:** phụ đề ở y ≥ 880, banner tên người ở y 668–823.
Để lọt banner tên vào khung TV là gắn tên một người vào ô nhỏ giữa lúc đang dẫn chuyện khác.

## 5d. Banner cho khúc MC dẫn

Dựng bằng `broadcast_kit.py` của skill `chuyen-gia-edit-video-tan`, thu còn khoảng **52%** rồi đắp
bằng `--overlay`:

```bash
--overlay "banner_mc.png,46,843,1.5,26.0"
```

Đặt ở (46, 843): dưới MC, **trên** cụm icon (y 972) và không chạm chữ trên bàn dẫn.

## 5e. Giọng đọc to, trong, ấm

```
highpass=f=75,
equalizer=f=160:t=q:w=1.0:g=2,      # trầm ấm
equalizer=f=450:t=q:w=1.2:g=-1.5,   # bỏ tiếng đục
equalizer=f=3200:t=q:w=1.2:g=2.5,   # rõ lời
equalizer=f=9000:t=q:w=1.0:g=1.2,   # thoáng
lowpass=f=15500,
alimiter=limit=0.78:attack=5:release=60:level=disabled
```

`--lufs -13.5 --tp -1.0`. Kết quả đo thật: −13,47 LUFS, đỉnh −0,99 dBTP, **LRA 7,20 so với 6,50 của
nguồn** — to hơn mà dải động còn rộng hơn.

Hai điều phải nhớ:
- `alimiter` mặc định **tự bù mức**; không đặt `level=disabled` thì loudness vọt lên và đỉnh chạm 0 dBTP.
- Nâng dải cao làm đỉnh vọt theo. Muốn to hơn thì **nới trần đỉnh lên −1,0 dBTP**, đừng ép thêm
  limiter — ép limiter là bóp dải động.

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
| Đề xuất thêm nhạc nền | **Bản tin ATT NEWS không dùng nhạc nền.** Outro im lặng là cố ý, không phải thiếu sót |
| Coi nhẹ tiếng hiện trường | Tiếng máy cắt, bước chân, tiếng gió là **bằng chứng của sự kiện** — giữ nguyên, không ducking, không lọc mạnh tay |
| Đắp phụ đề lên video vốn đã có phụ đề đốt sẵn | trích khung kiểm trước; có rồi thì bỏ trống `--captions` |
| Lớp `--replace` đặt sau logo/icon nên che mất chúng | thay hình phải nằm dưới cùng; đã có test chặn |
| `alimiter` tự bù mức, loudness vọt lên và đỉnh chạm 0 dBTP | luôn đặt `level=disabled` |
| Ép limiter để tăng độ to | nới trần đỉnh lên −1,0 dBTP trước; ép limiter là bóp dải động |
| Clip trong khung TV lặp đoạn ngắn nên giật từng vòng | giãn `setpts` cho khớp đúng phần trường quay, không lặp |
| Khung cắt cho TV lọt banner tên người của nguồn | né y 668–823 (banner) và y ≥ 880 (phụ đề) |
| Dùng ảnh chụp màn hình nhỏ làm logo nền tảng | 53 px là quá thấp cho phát sóng — xin file gốc lớn |
| `x264` báo lỗi "width not divisible by 2" | mọi kích thước phải chẵn (1030 chứ không 1031) |
| Tin tang lễ, liệt sĩ mà outro có biểu tượng like | dùng `make_outro.py --no-like` |

Thông số ATT NEWS trong `tro-ly-video-ban-tin-tan/references/att-news.md` ghi icon mạng xã hội
"4–8% chiều rộng", lệch với thực tế 194 px (10%). **File này là nguồn chuẩn.**
