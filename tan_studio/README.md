# tan_studio — script tiếng Việt → giọng đọc → video có phụ đề → học có kiểm soát

```text
kịch bản .txt/.docx
 → chuan_hoa   số, ngày, giờ, tiền, đơn vị, viết tắt, quy tắc phát âm đã duyệt (ghi vết từng thay đổi)
 → giong_doc   engine TTS (mặc định VieNeu, giọng "nam" = Minh Triết)
 → phu_de      SRT từ chữ GỐC + mốc thời gian từng đoạn audio
 → kiem_truoc  kiểm script / audio / phụ đề — lỗi mức `loi` CHẶN dựng video
 → dung_video  ffmpeg 1 lượt: nền (ảnh/clip/màu) + giọng + phụ đề đốt vào hình
 → kiem_tra    kích thước, thời lượng, khung đen, khoảng lặng + scripts/video_qa.py --strict --audio
 → (bạn)       xem-lai: chấp nhận / từ chối / đánh dấu lỗi  →  quy tắc đề xuất  →  bạn duyệt
```

Không viết lại skill: `tan_studio` nạp thẳng code trong `skills/tan-giong-doc-ban-tin/scripts/`,
`skills/bien-tap-video-thong-minh-song-ngu-tan/scripts/` và `scripts/video_qa.py`.

**Kỹ thuật ≠ nội dung.** Máy chỉ kiểm được kỹ thuật (định dạng, thời lượng, mức âm, phụ đề, văn bản).
Mọi báo cáo ghi `Nội dung: CHƯA ĐÁNH GIÁ` cho tới khi bạn chạy `xem-lai chap-nhan|tu-choi`.
"Kỹ thuật: DONE/PASS" **không** có nghĩa là video nghe/nhìn đã đạt.

## Cài đặt

```bash
python -m tan_studio kiem-tra
```

| Thành phần | Bắt buộc? | Dùng cho |
|---|---|---|
| Python ≥ 3.10, ffmpeg + ffprobe trên PATH | có | mọi bước có audio/video |
| `numpy` | nên có | kiểm audio (im lặng, vỡ tiếng, tốc độ đọc, khoảng lặng) |
| `pip install vieneu soundfile` | để có giọng thật | engine `vieneu` — lần đầu tự tải model (cần mạng) |
| `python-docx`, `faster-whisper`, `jsonschema` | tuỳ chọn | `.docx`, `danh-gia-tts --asr`, test schema |

Không cần API key. `HF_TOKEN` (tuỳ chọn, xem `.env.example`) chỉ để tải model nhanh hơn — đặt làm biến
môi trường, không ghi vào file dự án. tan_studio không gửi script/media đi đâu và không dùng chúng để huấn
luyện mô hình; lần duy nhất ra mạng là thư viện vieneu tải model lần đầu.

## Workflow mẫu và nghiệm thu

```bash
python -m tan_studio nghiem-thu                    # audio giả, ~5 giây, không cần vieneu
python -m tan_studio nghiem-thu --engine vieneu    # giọng thật, ~1 phút
```

Chạy `tan_studio/vi-du/` trên **bản sao sạch** (trong `outputs/nghiem-thu/`) rồi kiểm tiêu chí ở
`tan_studio/vi-du/nghiem-thu.json`: mọi bước xong, văn bản chuẩn hoá đúng, phát hiện được `VNeID` và
"ủy", khung đúng kích thước, QA kỹ thuật PASS, phụ đề hiện chữ gốc, hồ sơ có phiên bản. **Mọi thay đổi
trong tan_studio hoặc các script skill nó gọi phải chạy lại lệnh này** (test `TestNghiemThu` cũng chạy nó).

## Chạy một dự án

```bash
python -m tan_studio chay du-an.json --xem-truoc     # nửa độ phân giải, mã hoá nhanh — xem trước
python -m tan_studio chay du-an.json                 # bản đầy đủ
python -m tan_studio chay du-an.json --lan-chay <ID> --buoc dung_video,kiem_tra   # sau khi sửa tay phu-de.srt
python -m tan_studio chay-lai du-an.json <ID>        # chạy lại đúng cấu hình đã lưu → lần chạy mới
python -m tan_studio so-sanh du-an.json <ID-A> <ID-B> [--video so-sanh.mp4]
python -m tan_studio bao-cao du-an.json [--lan-chay ID]
```

```json
{
  "ten": "ban-tin-0210",
  "kich_ban": "kich-ban.docx",
  "audio": null,
  "phu_de": null,
  "media": ["anh1.jpg", "clip1.mp4"],
  "ti_le": "16:9",
  "thu_muc_ket_qua": "ket-qua",
  "tts": {"engine": "vieneu", "giong": "nam", "phong_cach": "tin_tuc", "toc_do": 1.0, "khoang_lang_ms": 450, "mp3": false},
  "chuan_hoa": {"tat_quy_tac": []},
  "kiem_tra": {"toc_do_doc": {"min": 3.0, "max": 6.5}, "chan_khi_loi": true},
  "ho_so": {"luu_van_ban": true}
}
```

- Đường dẫn tính từ thư mục file dự án. Tư liệu gốc chỉ được đọc, không bao giờ bị ghi đè hay sao chép.
- `audio`: có sẵn giọng thì bỏ qua `giong_doc`; phụ đề chia theo số ký tự (ước lượng — nên xem lại).
- `media`: ảnh/clip chia đều thời lượng, giữ tỉ lệ (viền đen, không cắt mặt). Rỗng → nền màu. Không tự tải media.
- `toc_do` khác 1.0 bị từ chối (kéo tempo làm giọng máy móc); muốn dài hơn thì tăng `khoang_lang_ms`.
- `kiem_tra`: ghi đè ngưỡng trong `tan_studio/data/nguong.json`.
- `ho_so.luu_van_ban: false`: sau khi chạy xong, xoá văn bản script khỏi hồ sơ (chỉ giữ sha256 + độ dài);
  `phu-de.srt` và video vẫn còn vì là sản phẩm. Lần chạy đó không chạy tiếp được, chỉ `chay-lai`.
- Thẻ nghỉ trong kịch bản: `Phần một. [nghỉ 2s] Phần hai.` hoặc `[nghỉ 500ms]` — im lặng đúng khoảng đó thay cho
  `khoang_lang_ms` (tối đa 10 giây mỗi thẻ). Thẻ tách đoạn đọc và không hiện trên phụ đề.
- `giong`: 25 giọng VieNeu + giọng đã nhân bản. 11 giọng mới (Mỹ Duyên, Kim Thanh, Minh Quân Pro…) phải nạp một lần:
  `python skills/tan-giong-doc-ban-tin/scripts/import_hf_voices.py` — danh sách ở `references/voices.md` của skill.

## Lồng tiếng theo phụ đề

Có sẵn `.srt`/`.vtt` của video (tự gõ, xuất từ CapCut, hoặc dịch): đọc từng câu đúng mốc, ra một file audio dài bằng video.

```bash
python -m tan_studio long-tieng video.srt --giong "Thùy Dung"            # kết quả: video-long-tieng/ cạnh file .srt
python -m tan_studio long-tieng video.srt --giong nam --toc-do-toi-da 1.3
```

Câu dài hơn chỗ của nó: (1) lấn sang khoảng lặng trước câu sau → (2) đọc nhanh hơn, mặc định tối đa 1.15 lần
(tối đa cho phép 1.5 — nhanh hơn nghe máy móc) → (3) đẩy câu sau lùi lại và xuất `phu-de-da-chinh.srt` để chữ khớp giọng.
Không bao giờ cắt chữ. Tự bỏ thẻ định dạng (`<i>`, `{\an8}`) và áp dụng quy tắc phát âm đã duyệt (phạm vi cá nhân/hệ thống).
Đầu ra: `long-tieng.wav`, `long-tieng.json` (mốc gốc/mốc đặt, tốc độ, số giây bị lùi từng câu), `cau/*.wav` (chạy lại
thì bỏ qua câu đã đọc). File phụ đề gốc chỉ được đọc.

## Đồ hoạ động (Remotion)

Mẫu nằm ở `do-hoa/` (Remotion + React, màu/logo ATT NEWS). Cài một lần: `cd do-hoa && npm i` (cần Node 18+).
ffmpeg vẫn dựng video chính; Remotion chỉ xuất clip đồ hoạ **trong suốt** (ProRes 4444) để đắp vào đúng giây,
nằm dưới phụ đề — thời lượng video không đổi nên QA giữ nguyên. Clip đã render dùng lại theo props.

| Mẫu | Dùng cho | Mặc định |
|---|---|---|
| `intro` | logo ATT NEWS bật vào, tiêu đề trượt lên (`\n` để xuống dòng), mờ dần lộ video | 4 giây |
| `so-lieu` | số lớn đếm lên + (tuỳ chọn) biểu đồ cột ngang | 5 giây |
| `lower-third` | tên + chức vụ, dưới trái, ở 65,5% chiều cao như phong cách ATT NEWS | 5 giây |
| `chu-dong` | video "chữ là nội dung" 9:16: chữ bật theo giọng, từ đang đọc tô vàng | dài bằng giọng |

Trong file dự án (khoá viết snake_case, `tai` = giây bắt đầu đắp):

```json
"do_hoa": {
  "intro": {"tieu_de": "An Thạnh Thủy\ntập huấn nông nghiệp", "phu_de": "Bản tin xã An Thạnh Thủy", "ngay": "03/10/2026"},
  "lower_third": [{"tai": 4.5, "ten": "Ông Nguyễn Văn A", "chuc_vu": "Chủ tịch UBND xã"}],
  "so_lieu": [{"tai": 10, "tieu_de": "Hộ dân tham gia", "gia_tri": 120, "don_vi": "hộ",
               "tien_to": "+", "so_le": 0, "mo_ta": "tăng gấp đôi năm trước",
               "cot": [{"nhan": "2025", "gia_tri": 60}, {"nhan": "2026", "gia_tri": 120}]}]
}
```

Dùng riêng:

```bash
python -m tan_studio do-hoa lower-third --dat ten="Bà Trần Thị B" --dat chuc_vu="Trưởng ấp" --anh 2   # xem 1 khung PNG
python -m tan_studio do-hoa intro --props intro.json --out intro.mov                                # .mov trong suốt, kéo vào CapCut được
python -m tan_studio do-hoa chu-dong --tu-lan-chay du-an/ket-qua/<run_id> --dat tieu_de="Tin nhanh"   # Reels từ giọng + phụ đề
cd do-hoa && npx remotion studio                                                                     # sửa mẫu, xem trực tiếp
```

Tên, chức vụ, số liệu **chỉ lấy từ kịch bản hoặc người dùng xác nhận**. Render đồ hoạ nặng hơn ffmpeg
(~20 giây cho clip 3 giây trên máy này): dùng `--anh` xem trước, render đủ khi đã ưng.

## Hồ sơ một lần chạy (`<dự án>/ket-qua/<run_id>/`)

| File | Nội dung |
|---|---|
| `run.json` (schema `RunReport`) | thời điểm, `app_version`, `config_hash`, cấu hình đầy đủ, phiên bản (git, mã nguồn, hash từng script skill, quy tắc học được đang bật + phiên bản), dấu vân tay đầu vào (kích thước, sha256 — không sao chép media), từng bước: trạng thái, thời gian xử lý, cảnh báo, lỗi, đầu ra; timeline dựng; `noi_dung` |
| `bao-cao.md` | bản đọc được của run.json |
| `chuan-hoa.json/.txt` | gốc, chuẩn hoá, từng thay đổi + lý do + id/phiên bản quy tắc |
| `giong-doc/` | `tts.json` (engine, phiên bản, giọng, tham số, mốc đoạn), `giong-doc.wav`, `doan/*.wav` |
| `phu-de.srt` | phụ đề — sửa tay được |
| `phat-hien.json` | phát hiện tự động (schema `Finding`) |
| `<ten>.mp4`, `<ten>.ass`, `qa.json` | video, phụ đề đã định dạng, QA kỹ thuật |

## Kiểm tra tự động

Mỗi phát hiện có `id`, `ma`, `muc_do` (`loi` chặn / `canh_bao` / `thong_tin`), `vi_tri` (đoạn, từ, giây, cue),
`ly_do`, `goi_y`, `dau_van_tay` (ổn định giữa các lần chạy). Chỉ báo, không tự sửa nội dung.

| Nhóm | Kiểm |
|---|---|
| script | đoạn rỗng, chỗ đánh dấu `[...]`/`TODO`/`???`, chỗ không chắc cách đọc, từ khó, dấu câu lặp, câu quá dài |
| audio | im lặng, vỡ tiếng (clipping), khoảng lặng giữa đoạn, tốc độ đọc bất thường (dấu hiệu nuốt/lặp chữ), tổng thời lượng lệch số chữ |
| phụ đề | lỗi timecode/chồng lấn, dòng quá dài theo tỉ lệ khung, đọc quá nhanh, phụ đề hết sớm/dài hơn giọng |
| video | mở được, có hình/tiếng, đúng kích thước, thời lượng khớp giọng, khung đen, khoảng lặng, codec/faststart |

**Không kiểm (chưa có cách đáng tin):** chính tả, chuyển cảnh bất thường, cảnh lặp, phát âm đúng/sai,
chất lượng hình. Phát âm chỉ đo được gián tiếp qua `danh-gia-tts --asr` (tham khảo) và tai người nghe.

## Review — một dòng là đủ

```bash
python -m tan_studio xem-lai du-an.json xem                       # phát hiện + quan sát của lần mới nhất
python -m tan_studio xem-lai du-an.json chap-nhan                 # hoặc tu-choi [--ghi-chu]
python -m tan_studio xem-lai du-an.json loi "phụ đề che logo" --loai phu_de --tai 12.5
python -m tan_studio xem-lai du-an.json loi "đánh vần VNeID" --loai phat_am --tu VNeID --doc-dung "vi en i ai đi"
python -m tan_studio xem-lai du-an.json canh-bao --id ph-7e233468 --dung-sai sai   # cảnh báo nhầm
```

Loại: `script, phat_am, giong_doc, hinh_anh, chon_canh, nhip_dung, phu_de, am_thanh, thuong_hieu, ky_thuat`.
Tuỳ chọn: `--doan`, `--tu`, `--tai` (giây), `--canh`, `--de-xuat`, `--uu-tien cao|trung_binh|thap`,
`--pham-vi du_an|chung` (chỉ dự án này / đề xuất thành quy tắc dùng chung), `--lan-chay` (mặc định mới nhất).
Từ chối nội dung giống email, số điện thoại, số CCCD.

## Học có kiểm soát: quan sát → đề xuất → đã duyệt

| Tầng | Ở đâu | Áp dụng tự động? |
|---|---|---|
| Quan sát (`Observation`) | `<dự án>/hoc/quan-sat.jsonl` | không |
| Quy tắc đề xuất (`Rule`, `de_xuat`/`mau_thuan`) | `<dự án>/hoc/quy-tac.json` | **không** |
| Quy tắc đã duyệt (`Rule`, `da_duyet` + `bat`) | `du_an`: `<dự án>/hoc/quy-tac.json` · `ca_nhan`: `~/.tan-studio/quy-tac.json` · `he_thong`: `tan_studio/data/quy_tac_he_thong.json` | có — phạm vi hẹp thắng |

- Quan sát `phat_am` có `--tu` + `--doc-dung` tự sinh **đề xuất** (ví dụ trước/sau lấy từ câu gốc). Trùng thì liên kết
  (`trung_voi`), không tạo bản ghi mới; lỗi đã gặp ở lần chạy trước được ghi `lap_lai_tu_lan_chay`.
- Hai cách đọc khác nhau cho cùng một từ → `mau_thuan`: không tự chọn; chỉ duyệt được ở phạm vi dự án khi dự án chưa
  có quy tắc đã duyệt khác cho từ đó.

```bash
python -m tan_studio quy-tac danh-sach du-an.json
python -m tan_studio quy-tac thu du-an.json qt-xxxx           # so với cấu hình hiện tại: tốt lên / xấu đi / đổi khác
python -m tan_studio quy-tac duyet du-an.json qt-xxxx [--pham-vi du_an|ca_nhan|he_thong]
python -m tan_studio quy-tac tu-choi|tat|bat|hoan-tac|lich-su du-an.json qt-xxxx
python -m tan_studio quy-tac kiem du-an.json                 # kiểm thử hồi quy mọi quy tắc đã duyệt
```

`duyet` sinh ca kiểm thử từ ví dụ và chạy ngay — không qua thì không duyệt. Mỗi thao tác tăng `phien_ban` và ghi
`lich_su` kèm trạng thái trước đó; `hoan-tac` quay về trạng thái trước (kể cả chuyển phạm vi). Quy tắc `he_thong`
nằm trong repo nên đi qua review/commit như code, và `tests/test_tan_studio.py` chạy lại toàn bộ.

## Đo xem có tốt lên không

```bash
python -m tan_studio chi-so du-an.json [du-an-2.json ...] [--theo config_hash|app_version]
python -m tan_studio lich-su-loi du-an.json --loc VNeID
```

`chi-so`: tỉ lệ chấp nhận ngay lần đầu, số lần sửa trước khi duyệt, phút từ lần chạy đầu tới khi duyệt, lỗi theo
loại/bước, tỉ lệ lỗi cũ tái xuất hiện, tỉ lệ cảnh báo được xác nhận đúng, tỉ lệ đề xuất được duyệt. Mỗi tỉ lệ kèm
tử số, mẫu số, cách tính; mẫu số < 3 ghi **"chưa đủ dữ liệu"**. "Lượt sản phẩm" = chuỗi lần chạy kết thúc ở một
lần được chấp nhận (lần chạy xem trước không tính).

`lich-su-loi` in bảng `X`/`.` theo từng lần chạy, ví dụ `X X .  tu:VNeID (đã hết ở lần mới nhất)`.

## Dữ liệu: xem, xuất, xoá, dọn

```bash
python -m tan_studio du-lieu xem du-an.json
python -m tan_studio du-lieu xuat du-an.json --tep du-lieu.zip [--lan-chay ID] [--kem-media]
python -m tan_studio du-lieu don-dep du-an.json --giu 5 [--chac-chan]      # xoá wav/mp4 cũ, giữ JSON
python -m tan_studio du-lieu xoa-lan-chay du-an.json --lan-chay ID [--chac-chan]
python -m tan_studio du-lieu xoa-du-an du-an.json [--chac-chan]           # xoá ket-qua/ và hoc/
```

Không có `--chac-chan` thì chỉ in kế hoạch. Chỉ xoá trong `ket-qua/` và `hoc/` — không bao giờ đụng kịch bản,
audio, media gốc. `don-dep` giữ media của các lần đã được chấp nhận. Xoá một lần chạy xoá luôn quan sát/đánh giá
gắn với nó; quy tắc đã duyệt giữ lại (còn tham chiếu nguồn).

## Đánh giá TTS

```bash
python -m tan_studio danh-gia-tts [--asr] [--luot 3]
python -m tan_studio cham outputs/tts-eval/<lần> <câu> dat|loi --ghi-chu "..."
```

Bộ câu `tan_studio/data/tts_cases.json`. Mỗi lần chạy một thư mục mới, không ghi đè; xuất `ket-qua.json`, `.csv`,
`bao-cao.md`. ASR (whisper small, CPU 4 luồng) **chỉ là tín hiệu tham khảo** — nghe sai tên riêng tiếng Việt nhiều.

## Giới hạn thực tế

| Phần | Trạng thái |
|---|---|
| Chuẩn hoá, phụ đề, kiểm tra, review, quy tắc, chỉ số, dữ liệu | Python thuần, có test |
| Dựng video, kiểm video | cần ffmpeg/ffprobe |
| Giọng thật | cần `vieneu` + model; thiếu thì báo lỗi rõ, không giả vờ tạo audio |
| Engine `thu-nghiem` | audio GIẢ để thử luồng; báo cáo luôn gắn cảnh báo |
| Quy tắc học được | hiện chỉ loại **phát âm** (thay một từ bằng cách đọc). Lỗi hình ảnh/nhịp dựng/âm thanh được ghi nhận và đo, nhưng chưa thành quy tắc tự động |
| Mốc phụ đề trong một đoạn | chia theo số ký tự — ước lượng |
| Chưa có | nhạc nền, chuyển cảnh, nhiều engine, giao diện. Dữ liệu là JSON/JSONL có schema (`data-contracts/studio.schema.json`) để thêm giao diện sau không phải đổi dữ liệu |

Thêm engine: viết lớp có `check()`, `info()`, `open(voice, style)`, `synth(text, path)` trong `tan_studio/tts.py`, thêm vào `ENGINES`.

## Lỗi thường gặp

| Thông báo | Cách xử lý |
|---|---|
| `chưa cài 'vieneu'` | `pip install vieneu soundfile`, hoặc `"engine": "thu-nghiem"` để thử luồng |
| `kiem_truoc FAILED — lỗi chặn xuất video` | đọc từng dòng (có vị trí + gợi ý), sửa kịch bản rồi chạy lại; tạm bỏ chặn: `"kiem_tra": {"chan_khi_loi": false}` |
| `ffmpeg lỗi (exit ...)` | 800 ký tự cuối stderr nằm trong `run.json`; hay gặp: media hỏng, ổ đầy |
| `QA kỹ thuật FAIL` | xem `qa.json` và `phat-hien.json` |
| `mâu thuẫn với [...]` | `quy-tac danh-sach`, tắt/hoàn tác một bên, hoặc duyệt ở phạm vi `du_an` |
| Máy nóng | mỗi lần một việc nặng; ffmpeg/whisper giới hạn 4 luồng; dùng `--xem-truoc` trước khi render đủ |
