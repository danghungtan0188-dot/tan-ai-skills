# Kỹ thuật và hiệu ứng đã làm được (10/2026)

Tra cứu nhanh những thứ đã dựng thành công và người dùng duyệt, để video sau dùng lại thay vì làm lại từ đầu.
Mã nguồn đầy đủ nằm ở `remotion-studio/src/an-sinh-7-11/` (video An sinh 7/11, lãnh đạo Trung ương)
và `remotion-studio/src/vneid-tien-ich/` (VNeID 5 tiện ích). Lỗi đã gặp khi làm: bảng §7 của
[phong-cach-att-news.md](phong-cach-att-news.md).

## 1. Video tuyên truyền chỉ có đồ họa + ảnh (không footage)

Khi người dùng dặn "không lấy ảnh/khúc video khác": dựng toàn bộ bằng Remotion từ ảnh họ gửi. Render nhẹ hơn
ghép nhiều video chồng lớp, phù hợp máy hay sập khi nóng.

Bố cục đã duyệt:

| Phần | Cách dựng |
|---|---|
| Mở đầu | 3 huy hiệu giá trị (quà · học bổng · khám bệnh) bật lò xo theo từng câu đọc → tiêu đề vàng 2 dòng + hoa văn + chip ngày |
| Giới thiệu lãnh đạo | ảnh khung viền vàng phát sáng bên trái (2 ảnh nối mờ) + chức vụ vàng + **tên to nhất khung, 1 dòng** bên phải |
| Mỗi địa điểm | poster người dùng ghép (ngang 1536×1024) bên trái; phải: tiêu đề 2 dòng, chip giờ, ô số liệu đếm lên |
| Người dân cần lưu ý | 4 ô lưới 2×2, mỗi ô 1 huy hiệu + chữ tô đậm ý chính, hiện đúng câu đọc |
| Kết | dòng thời gian 3 mốc giờ → thông điệp → "TRÂN TRỌNG THÔNG BÁO" + 3 dấu ✓ |

Mọi thứ hiện ra **đúng lúc giọng đọc tới**: `data.ts` sinh từ `moc.json` (`T[id]` = giây bắt đầu từng câu).

## 2. Thành phần Remotion dùng lại được (`AnSinh711.tsx`)

| Tên | Làm gì | Ghi chú |
|---|---|---|
| `HuyHieu` | huy hiệu tròn: viền vàng nét đứt xoay chậm, vành vàng, lõi đỏ thẫm, biểu tượng vàng 2 tông, sao lấp lánh | người dùng: "biểu tượng nên đẹp hơn" — thay icon nét mảnh |
| `IconTron` | 11 biểu tượng SVG 2 tông (nét + mảng mờ): quà, sách, y tế (tim + chữ thập), giờ, ghim, người, giấy tờ, điện thoại, danh sách, mắt, dấu ✓ | đổi màu bằng `mau`/`phu` |
| `Quet` | vệt sáng trắng xiên lướt qua thẻ lúc thẻ hiện | thẻ cần `position: relative; overflow: hidden` |
| `BungSao` | 8 chấm vàng bung ra quanh con số lúc đếm xong | đặt trong ô số `position: relative` |
| `HoaVan` | vạch vàng – hình thoi xoay – vạch vàng chạy ra từ giữa, dưới tiêu đề lớn | thay cho đường kẻ trơn |
| `ChuVang` | chữ vàng **màu đặc** + bóng + quầng sáng nhấp nháy | KHÔNG dùng `background-clip:text` (render ra khối màu) |
| `PhuDe` | phụ đề tiếng Việt chữ viết số (7/11/2026, 200…) — bảng `HIEN` trong `tao_giong.py` đổi chữ đọc → chữ viết | cỡ 42 |
| `Nen` | nền xanh lá + **mạng lưới laser trôi** (30 điểm, nối điểm gần < 400 px) + **tia vàng nan quạt** xoay chậm | người dùng chọn giữ cả hai |

## 3. 4 giây kết kiểu đài (`KetAnhSang.tsx`)

Học nhịp từ 8 s cuối video mẫu của đài, **không chép logo/QR của đài**:
0–1,5 s tia sáng bắn xéo có **đầu sáng chói** (sao băng) + chùm tia lửa → 0,9–1,9 s **viền neon xanh lơ**
chạy quanh khung (`strokeDasharray/strokeDashoffset`) + nét neon gợn sóng dưới → 1,85 s chớp sáng, logo ATT NEWS
hiện + **vệt sáng lướt ngang** → dòng UBND hiện bằng `clipPath inset` từ trái → khẩu hiệu vàng nghiêng chạy ra →
3,4–4 s mờ về đen. Nền xanh lá sáng + mạng lưới laser.

Máy chưa có font viết tay đủ dấu tiếng Việt (Segoe Script/Print, Gabriola thiếu ơ ư ẻ Ủ…) → khẩu hiệu dùng
chữ nghiêng đậm; muốn chữ viết tay thật phải cài font (hỏi người dùng trước).

## 4. Âm thanh

**Nhạc nền phấn khởi tự soạn** (`_dung/nhac_phan_khoi.py`, không mẫu bản quyền): Rê trưởng 96 BPM, vòng
I–V–vi–IV, pad dây + piano rải nốt móc đôi + bass gốc + trống nhẹ mỗi phách + tiếng lắc lệch phách; đoạn tri ân
người có công dịu xuống (bỏ trống, piano thưa), đoạn kết to dần. Trộn: lúc nghỉ thấp hơn giọng ≤ 6 dB, dưới lời
chỉ hạ 7 dB (−10 dB là "nhạc nền đâu"). Luôn gửi 20 s nghe thử.

**Tiếng hiệu ứng tổng hợp**: "vút" (nhiễu lọc thông cao quét 400→4400 Hz) lúc chuyển cảnh; "ting" (1568 + 2349 Hz
tắt dần) lúc số liệu/ô hiện; 4 s kết thêm "vút" + 14 tiếng lấp lánh + "boong" (196/392/587/784 Hz) lúc logo hiện.

**Thay nhạc/tiếng không phải render lại hình**: Remotion render `--muted`, tiếng ghép riêng
(`ffmpeg -map 0:v -c:v copy` + file tiếng mới).

## 5. Giọng đọc (VieNeu, giọng "Nữ VNeID Sổ sức khỏe")

- Mỗi câu ≥ 4 bản; chấm CER (đổi số → chữ trước khi so) + biến thiên F0; **loại bản dài > 1,5 lần trung vị**.
- Cắt đuôi theo mốc chữ cuối + 0,25 s, nhỏ dần cosin 80 ms; không cắt đầu câu.
- Chữ khó ở đầu câu ("Ủy ban"): đọc kèm từ dẫn ("Đồng thời, …") rồi cắt bỏ từ dẫn theo mốc chữ.
- Chữ giọng này không đọc được ("tri ân" → "chi ân"): **ghép 2 chữ từ bản đúng** (`_dung/ghep_tri_an.py`:
  mốc chữ whisper medium, cắt từ hết chữ đứng trước, nối mềm 25 ms, cân RMS).
- Vá câu đọc sai mà **không đổi hình**: đặt bản mới vào đúng mốc bắt đầu cũ (`_dung/va_tieng.py`), bản mới phải vừa chỗ.
- Nghe kiểm cuối: whisper medium trên file cuối + dò "khúc có tiếng mà không có chữ ≥ 0,3 s" (tiếng lạ).

## 6. Khung tin trên màn hình TV trường quay (ffmpeg)

Màn hình phông ATT: x 889–1920, y 231–646 (1031×415). Tấm nền PNG (PIL) xanh navy viền trắng: trái là chữ
(dòng nhỏ xã · ngày vàng → tiêu đề trắng → vạch vàng → chức vụ vàng → **tên lãnh đạo to nhất, tự co cho vừa 1 dòng**
→ dòng phụ), phải là ô đen 612×348 cho video 604×340 đặt ở (1299, 269).

```bash
ffmpeg -i GOC.mp4 -loop 1 -t <dai_MC> -i khung_tv.png -ss <bat_dau_clip> -t <dai_MC> -i NGUON.mp4 -filter_complex \
 "[1:v]format=rgba[k];[2:v]scale=604:340,setsar=1,setpts=PTS-STARTPTS[c];\
  [0:v][k]overlay=889:231:enable='lt(t,<dai_MC>)'[a];[a][c]overlay=1299:269:enable='lt(t,<dai_MC>)':eof_action=repeat,format=yuv420p[v]" ...
```

Khung có ngay từ khung hình đầu (không fade — fade video không alpha là hiện từ đen); clip bắt đầu ở chỗ đã thấy rõ chủ thể.

## 7. Logo ATT NEWS + Facebook · Zalo toàn video

`scripts/make_att_bugs.py --logo-height 55 --icon-height 44`. Phim đã có logo ở đầu trang thì **dò toạ độ logo có sẵn**
(so mẫu tương quan trên một khung) rồi đè đúng chỗ đó — đặt theo toạ độ chuẩn sẽ thành 2 logo lệch nhau.
Bỏ logo góc ở đoạn MC (phông đã có) và ở 4 s kết (logo lớn giữa khung). Facebook · Zalo góc trái dưới, alpha 0,94.
