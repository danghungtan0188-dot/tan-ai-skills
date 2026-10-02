# Làm video mới theo khuôn video cũ

Video sau không phải chỉnh lại kiểu chữ, màu, vị trí logo từ đầu. Lấy khuôn từ project cũ rồi áp.

## Cái gì chép được, cái gì phải làm lại

| Việc | Chép từ video cũ được không | Bằng gì |
|---|---|---|
| Font, màu, cỡ, viền, vị trí chữ/phụ đề | **được**, nguyên khối style | `khuon_mau.py trich/ap` |
| Logo, intro/outro, thẻ TV, mức LUFS | **được**, nếu còn file trên máy | `khuon_mau.py` (đọc lệnh render cũ) |
| Bộ lọc màu, chuỗi lọc âm | **được** | cùng chỗ trên |
| Cắt khoảng lặng, cắt từ đệm (ờ, à) | **đề xuất được**, không tự cắt | `cut_silence.py` |
| Phụ đề từ giọng nói | **được**, nhưng là bản nháp | `build_bilingual.py tu-asr` |
| Tốc độ, zoom, scale, vị trí khung hình | **không** — tuỳ từng đoạn | chỉnh tay cho từng đoạn |
| Chọn cảnh, nội dung, lời bình | **không** | người làm quyết định |

Khuôn chỉ giữ thứ **lặp lại ở mọi video**. Thứ phụ thuộc nội dung từng video thì chép sang là hỏng.

## 1. Lấy khuôn từ project cũ

```bash
python scripts/khuon_mau.py trich \
  --ass cu/cap.song-ngu.ass --ass cu/lt.ass \
  --lenh cu/lenh-render.txt --ghi-chu "ATT NEWS 16:9" \
  --out khuon-att.json
```

- `--ass`: đọc **style thật** trong file ASS cũ — font, cỡ, màu chữ, màu viền, độ dày viền, canh
  lề, MarginV, PlayRes. Không đoán từ ảnh, chỉ đọc cái đã ghi ra file.
- `--lenh`: file text chứa đúng dòng lệnh `render_att.py` đã chạy lần trước. Nhặt lại
  `--card-pos`, `--extra-logo`, `--outro-dir`, `--audio-pre`, `--lufs`, `--tp`.
  **Nhớ lưu dòng lệnh mỗi lần render** — không có nó thì phần này trống.

## 2. Áp khuôn cho video mới

```bash
python scripts/khuon_mau.py ap khuon-att.json --cues moi/bilingual.json --out-ass moi/cap.ass
python scripts/khuon_mau.py lenh khuon-att.json moi/rough.mp4 moi/final.mp4 --them --scenes moi/scenes.json
```

`ap` giữ nguyên khối style cũ, chỉ thay lời → chữ giống hệt video trước.
`lenh` in lại lệnh render với đúng tham số cũ, chỉ đổi file vào/ra.

Khuôn thiếu style `EN` hoặc `VI` thì `ap` báo lỗi — khuôn đó không dùng cho phụ đề song ngữ được.

## 3. Bỏ khoảng lặng và từ đệm

```bash
python scripts/cut_silence.py VIDEO --words asr_words.json --out edit/de-xuat-cat.json
```

In bảng: mốc vào, mốc ra, lý do, tổng số giây bỏ đi, thời lượng còn lại. **Đây là đề xuất.**

- Chỉ xét khoảng lặng dài hơn `--toi-thieu` (mặc định 1 giây) và **vẫn chừa `--giu` giây**
  (mặc định 0,35) ở mỗi chỗ. Người nói cần nhịp thở; bản tin cần khoảng ngắt giữa hai ý.
  Cắt sạch khoảng lặng làm lời dồn cục, nghe mệt.
- Từ đệm: chỉ cắt từ đệm đứng riêng và ngắn hơn 1,2 giây. Máy không hiểu nghĩa — đọc bảng, bỏ
  bớt dòng nào không nên cắt, rồi mới cắt.

Duyệt xong mới cắt:

```bash
python scripts/cut_silence.py VIDEO --de-xuat edit/de-xuat-cat.json --ap edit/gon.mp4 --approved
```

Không có `--approved` thì script từ chối ngay. Cắt xong nó ghi `anh-xa.json` (mốc cũ → mốc mới).

**Cắt xong phụ đề cũ lệch hết** — phải dời mốc:

```bash
python scripts/cut_silence.py --doi-moc edit/bilingual.json edit/anh-xa.json --out edit/bilingual2.json
```

Mốc rơi đúng vào đoạn bị cắt sẽ bị dồn về mép gần nhất, nên vẫn phải xem lại đồng bộ bằng mắt.

## 4. Phụ đề từ giọng nói khi không có kịch bản

Có kịch bản gốc thì **đừng dùng** phần này — ASR nghe sai tên riêng, chức danh, số liệu
(xem đầu `build_bilingual.py`). Chỉ dùng cho phỏng vấn, tiếng hiện trường, khi không có bản chữ.

```bash
python scripts/build_bilingual.py transcribe VIDEO --out edit/asr_words.json
python scripts/build_bilingual.py tu-asr edit/asr_words.json --out edit/cues-nhap.json
```

File ra là **nháp**: lời Việt là bản máy nghe, tiếng Anh để trống. Nghe lại sửa lời Việt, dịch
tiếng Anh, rồi mới `build_bilingual.py build`. Cue ngắt khi người nói nghỉ hơn 0,6 giây,
khi hết câu, hoặc khi chạm giới hạn ký tự.
