# Banner tên kiểu phóng sự truyền hình

Học từ phóng sự "Vĩnh Hựu – vùng đất an toàn khu" (VHTV), đo trên khung 1920×1080.
Mẫu dựng sẵn: `do-hoa/src/mau/BannerPhongSu.tsx` (composition `BannerPhongSu`, nền trong suốt).

## Thông số đo được

| Phần | Vị trí (px, khung 1080p) | Màu | Chữ |
|---|---|---|---|
| Cả banner | y 830–945 (77–87,5% chiều cao) | — | — |
| Huy hiệu "PHÓNG SỰ" | x 194–410, hình bình hành nghiêng 14°, bo 12, viền trắng 3 | `#0BA44D` | trắng, đậm, 34; vòng tròn trắng mảnh xoay sau chữ |
| Thanh tầng trên (tên) | x 405–1731, y 836–887 (51 px) | `#169A4D` | trắng, đậm, 44, bắt đầu x ≈ 535 |
| Thanh tầng dưới (địa danh) | y 889–942 (53 px), mép trái có nêm xanh đậm | `#CBDBBE` | xanh `#169A4D`, đậm, 40 |

Tên người viết: chức danh thường ("Bà", "Ông") + HỌ TÊN IN HOA. Dòng dưới: "Xã …, tỉnh …".

## Chuyển động (đo từng 0,1 s)

1. 0,0–0,3 s: huy hiệu trượt vào từ phải, thanh trượt theo trễ 0,05 s, dừng êm (ease-out).
2. 0,3–0,6 s: chữ quét hiện từ trái sang; vòng tròn huy hiệu bung ra (hơi nảy) rồi xoay liên tục.
3. Khi đứng yên: cứ ~2,5 s có vệt sáng lướt qua huy hiệu.
4. Ra: 0,4 s cuối mờ + dịch sang trái.

## Dùng

```bash
cd do-hoa
npx remotion still src/index.ts BannerPhongSu out.png --props=props.json --frame=60     # xem trước
npx remotion render src/index.ts BannerPhongSu out_png --props=props.json --sequence --image-format=png
```

`props.json`: `{"tiLe":"16:9","thoiLuong":5,"ten":"Bà NGUYỄN THỊ A","diaChi":"Xã An Thạnh Thủy, tỉnh Đồng Tháp","nhan":"PHÓNG SỰ"}`.
Đổi màu theo kênh qua `mauDam`, `mauHuyHieu`, `mauNhat`.

Lưu ý:
- ffmpeg kèm Remotion trên máy này hỏng khi ghép `.mov` hoặc `.mp4`. Phải xuất `--sequence` rồi đắp bằng ffmpeg hệ thống.
- Banner nằm ở 77–87,5% chiều cao, nên đè lên dòng phụ đề nếu phụ đề đặt cao. Khi có banner, hạ phụ đề xuống hoặc tắt phụ đề trong lúc banner hiện.
- Tên và chức danh chỉ lấy từ kịch bản hoặc người dùng xác nhận.

## Tránh đè phụ đề (video5, 2026-10-09)

Phụ đề lời bình hội nghị cỡ 58, có câu xuống 2 dòng. Banner đặt ở vị trí gốc (77–87,5 % cao) đè lên
dòng trên của phụ đề. Đã chốt: `BannerPhongSu` `dichLen: 90`, `AnhTuLieu` `dichLen: 80`
(px trên khung 1080p). Ảnh tư liệu có chú thích mà phụ đề đã nói đủ ý thì bỏ chú thích (video6).
