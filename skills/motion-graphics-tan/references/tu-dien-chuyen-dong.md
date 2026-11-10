# Từ điển chuyển động: gọi đúng tên, ra lệnh đúng ý

Chuyển thể tiếng Việt từ [showheyohtaki/motion-prompt](https://github.com/showheyohtaki/motion-prompt) (MIT, © 2026 Shohei Ohtaki, commit `7819d38`). Giấy phép gốc: `scripts/giay-phep/motion-prompt-LICENSE.txt`.
Lấy 2 bộ: **motion** (#001–024) và **camera** (#025–048). Câu ra lệnh mẫu viết lại cho việc của Tân.
**Xem mẫu chạy** của từng tên: https://showheyohtaki.github.io/motion-prompt/#001 (đổi số ở cuối link).

**Cách ra lệnh:** tên kỹ thuật + **bao lâu** + **mạnh cỡ nào** + **cái gì chuyển động**. Thiếu 3 thứ sau thì AI tự đoán và hay đoán sai.
Cột "Thẻ sẵn" là thẻ có trong `assets/ky-thuat/` hoặc `assets/mau/` của skill này.

## Chuyển động đồ họa (motion)

| # | Tên gọi | Tiếng Việt | Là gì | Câu ra lệnh mẫu | Thẻ sẵn |
|---|---|---|---|---|---|
| 001 | Pop-in | Bật vào | Hiện ra kèm một cú nảy nhẹ | "Cho logo bật vào, 0,4 s, vượt nhẹ rồi về chỗ." | `so-muc-to` |
| 002 | Stagger | Lần lượt | Các món hiện nối nhau, lệch nhau chút thời gian | "3 ô hiện lần lượt từ trên xuống, cách nhau 0,1 s." | `o-hoi-lat` |
| 003 | Burst | Bung tia | Tia và chấm bung ra quanh vật vừa hiện | "Lúc trái xoài hiện, bung 8 tia ngắn quanh nó, mờ đi trong 0,3 s." | |
| 004 | Line draw | Vẽ nét | Đường kẻ dài ra như đang được vẽ | "Vẽ đường biểu đồ từ trái sang trong 1,2 s." | `khoanh-tay` |
| 005 | Mask reveal | Trồi từ mép | Chữ trồi lên từ sau một mép vô hình | "Tiêu đề trồi từ dưới lên, 0,6 s, dòng sau trễ dòng trước một chút." | |
| 006 | Typewriter | Gõ chữ | Chữ hiện từng ký tự, có con trỏ | "Gõ từ khóa 0,12 s mỗi ký tự, con trỏ nháy ở cuối." | `o-binh-luan`, `con-tro-gia` |
| 007 | Count-up | Số đếm chạy | Con số chạy nhanh tới số cuối | "Đếm từ 0 lên 1.400.000 trong 1,4 s, chậm dần ở cuối." | `so-dem-chay` |
| 008 | Kinetic typography | Chữ động theo lời | Chữ to nhỏ, xoay, nhảy theo nhịp lời nói | "Từ được nhấn trong lời thì phóng to và rơi đúng nhịp." | `kinetic-type`, `phu-de-to-tu` |
| 009 | Easing | Nhanh chậm tự nhiên | Tăng tốc và giảm tốc thay vì đều đều | "Vào thì chậm dần lúc dừng (ease-out)." | |
| 010 | Overshoot | Vượt rồi về | Đi lố mục tiêu một chút rồi về chỗ | "Kim đồng hồ vượt khoảng 10% rồi lùi về." | |
| 011 | Squash & stretch | Nén giãn | Bẹp và giãn cho có cảm giác đàn hồi | "Trái bóng chạm đất thì bẹp nhẹ, giữ tinh tế." | |
| 012 | Shape morph | Biến hình | Hình này đổi mượt thành hình khác | "Biến nút bấm thành dấu tích trong 0,8 s." | `hinh-bien-giao-dien` |
| 013 | Liquid motion | Chảy như nước | Hình chảy và nhập vào nhau như chất lỏng | "Logo hiện bằng các giọt nước gom lại thành hình." | |
| 014 | Motion trail | Vệt đuôi | Vệt mờ dần chạy theo vật đang bay | "Vòng tròn bay có 5 bóng mờ dần phía sau." | |
| 015 | Particles | Hạt bay | Nhiều mảnh nhỏ bay ra, rơi tản mát | "Lúc chốt đơn, bắn hạt 4 màu từ dưới lên, rơi hết trong 1,5 s." | |
| 016 | Parallax | Lớp xa gần | Lớp gần chạy nhanh, lớp xa chạy chậm, tạo chiều sâu | "Tách cảnh vườn thành 3 lớp, lớp gần trượt nhanh hơn." | `chu-ma-nen` |
| 017 | Mask transition | Chuyển qua khung | Cảnh sau hiện trong một hình đang lớn dần | "Cảnh sau mở ra trong vòng tròn lớn dần từ giữa, 0,5 s." | |
| 018 | Shape transition | Chuyển bằng mảng | Mảng màu phủ kín rồi lộ cảnh sau | "3 dải màu quét ngang phủ màn hình rồi rút đi, lộ cảnh mới." | |
| 019 | Liquid transition | Chuyển chảy | Chất lỏng tràn vào thay cảnh | "Cà phê tràn từ trên xuống thay cảnh." | |
| 020 | Zoom through | Phóng xuyên | Phóng vào một vật rồi xuyên qua sang cảnh sau | "Phóng vào màn hình điện thoại rồi xuyên sang cảnh sản phẩm." | |
| 021 | Flip | Lật thẻ | Lật như lá bài để thấy mặt sau | "Lật ô từ dấu ? sang nội dung, 0,4 s." | `o-hoi-lat` |
| 022 | Light sweep | Vệt sáng lướt | Một dải sáng lướt qua bề mặt | "Cho vệt sáng lướt qua chữ tên sản phẩm một lần." | `chrome` |
| 023 | Glitch | Nhiễu hình | Hình vỡ như bị lỗi | "Nhiễu hình 0,2 s ở chữ 'Sai rồi'." | |
| 024 | Impact shake | Rung khi chạm | Cả khung rung khi vật đập xuống | "Số 01 đập xuống thì rung khung nhẹ 0,15 s." | |

## Máy quay và cắt cảnh (camera)

| # | Tên gọi | Tiếng Việt | Là gì | Câu ra lệnh mẫu |
|---|---|---|---|---|
| 025 | Pan | Lia ngang | Máy xoay trái hoặc phải | "Lia chậm từ trái sang qua cả vườn xoài, 4 s." |
| 026 | Tilt | Lia dọc | Máy ngửa lên hoặc cúi xuống | "Lia từ gốc cây lên tới chùm trái." |
| 027 | Dolly in | Đẩy máy vào | Máy tiến lại gần | "Đẩy máy từ từ vào tay người đang gói hàng." |
| 028 | Zoom in | Phóng ống kính | Ống kính phóng to, máy đứng yên | "Phóng nhẹ 110% vào mặt người nói ở câu đắt." |
| 029 | Tracking shot | Đi theo | Máy đi cùng nhân vật | "Đi theo cô chú từ cổng vào vườn." |
| 030 | Orbit (Arc shot) | Quay vòng | Máy vòng quanh chủ thể | "Quay vòng nửa vòng quanh giỏ quà Tết." |
| 031 | Crane up | Nâng máy | Máy được nâng lên cao | "Nâng máy từ mặt bàn lên thấy cả xưởng." |
| 032 | Dolly zoom (Vertigo) | Kéo đẩy chóng mặt | Người đứng yên, nền phía sau co giãn | "Dùng một lần ở lúc 'bất ngờ', 1,5 s." |
| 033 | Rack focus | Chuyển nét | Đổi nét giữa gần và xa | "Nét từ trái xoài phía trước sang người phía sau." |
| 034 | Handheld | Cầm tay | Rung nhẹ như cầm máy bằng tay | "Thêm rung cầm tay nhẹ cho cảnh vlog." |
| 035 | FPV drone shot | Bay xuyên | Bay nhanh, xuyên qua không gian | "Bay xuyên qua luống rau, nhanh." |
| 036 | Dutch angle | Nghiêng khung | Khung nghiêng chéo | "Nghiêng khung 10° ở cảnh 'rối quá'." |
| 037 | Slow motion | Quay chậm | Chiếu chậm hành động | "Chiếu chậm cảnh rót nước mắm, 50%." |
| 038 | Speed ramp | Đổi tốc | Đang nhanh chuyển chậm (hoặc ngược lại) giữa cảnh | "Nhanh tới lúc dao chạm trái, rồi chậm lại 0,5 s." |
| 039 | Time-lapse | Tua nhanh thời gian | Nén nhiều giờ thành vài giây | "Tua nhanh cảnh phơi bánh tráng từ sáng tới trưa, 3 s." |
| 040 | Freeze frame | Dừng hình | Dừng hành động một nhịp | "Dừng hình lúc trái xoài vừa bổ đôi, 0,8 s, kèm chữ." |
| 041 | Jump cut | Cắt nhảy | Cùng khung hình, nhảy tới thời điểm sau | "Cắt bỏ chỗ ngập ngừng, phóng nhẹ ở mỗi cú cắt để che." |
| 042 | Match cut | Cắt khớp | Cắt sang cảnh có hình hoặc chuyển động giống | "Cắt từ trái xoài tròn sang mặt trời tròn." |
| 043 | Whip pan | Lia vụt | Lia rất nhanh, nhòe sang cảnh sau | "Lia vụt từ người nói sang sản phẩm." |
| 044 | Cross dissolve | Hòa tan | Cảnh này mờ dần vào cảnh sau | "Hòa tan 0,3 s giữa hai đoạn" (dùng ít, xem `kiem-re-tien.md`) |
| 045 | Wipe | Gạt cảnh | Một mép di chuyển thay cảnh | "Gạt từ trái sang bằng cạnh khay hàng." |
| 046 | Smash cut | Cắt đột ngột | Cắt phắt sang cảnh trái ngược | "Đang yên tĩnh cắt phắt sang cảnh chợ đông." |
| 047 | J-cut | Tiếng trước hình | Tiếng cảnh sau vang lên trước khi thấy hình | "Cho tiếng xèo xèo vào trước hình chảo 0,5 s." |
| 048 | L-cut | Tiếng kéo dài | Tiếng cảnh trước còn kéo sang cảnh sau | "Giữ lời cô chú khi đã cắt sang cảnh vườn." |

## Nhịp chuẩn đi kèm (đo từ 86 video, xem `ky-thuat.md`)

- Phần lớn cắt thẳng (khoảng 2/3). Chuyển cảnh (#017–021, #043–045) chỉ dùng ở chỗ đổi phần, dưới 0,4 s.
- Tránh để mọi thứ đều **hòa tan, mờ dần** (#044). Dân chuyên dùng chuyển động nhiều hơn mờ dần khoảng 6 lần.
- Mỗi video chỉ một cú "lớn" (#032 kéo đẩy chóng mặt, #024 rung mạnh, #015 hạt bay).

Còn 6 bộ khác trong repo gốc (motion2, camera2, ui, lp, lp2, photo). Cần thì xem gallery ở trên.
