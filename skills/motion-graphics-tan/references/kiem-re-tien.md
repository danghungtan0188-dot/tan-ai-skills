# Kiểm "video nhìn rẻ tiền" sau khi render

Nguồn: [Tejashmakwana/motionmaxxing](https://github.com/Tejashmakwana/motionmaxxing) (Apache 2.0, commit `8c8ec0f`).
- `scripts/look.py` chép từ repo gốc. Chỗ sửa duy nhất là thêm `-threads 2` cho mọi lệnh ffmpeg, để máy nhẹ. Đầu file có ghi rõ chỗ sửa này.
- Giấy phép và NOTICE gốc nằm ở `scripts/giay-phep/`.
- Phần dưới đây là **tóm tắt tiếng Việt**, không chép nguyên văn.
- Không lấy `lint.mjs`, vì nó phải mở Chrome để soi trang, nặng máy.

## Chạy

```bash
python skills/motion-graphics-tan/scripts/look.py ra.mp4 --out D:/tam/look --expect 4.5 --expect-audio
```

`--strict` làm script trả mã 3 khi có cổng không đạt, để chặn tự động.

Kết quả ghi vào thư mục `--out`:

| File | Chứa gì |
|---|---|
| `sheet.jpg` | Bảng khung hình |
| `cuts.txt` | Các cú cắt |
| `still.txt` | Các đoạn hình đứng im |
| `mid.jpg` | Khung 2 khung **trước** mỗi cú cắt, nơi hay giấu lỗi chuyển cảnh |
| `strips.jpg` | Khung trước, đúng và sau mỗi cú cắt |
| `gates.json` | Kết quả các cổng |

Trên Windows, ảnh không có mốc giờ in lên. Script chỉ tìm font ở đường dẫn Mac và Linux. Việc này không ảnh hưởng kết quả các cổng.

## Các cổng

| Cổng | Đạt khi | Ai chấm |
|---|---|---|
| G0 có video thật | Giải mã được, không đen trắng, hình có chuyển động, đúng thời lượng (`--expect`), có tiếng và không câm (`--expect-audio`) | `look.py` |
| G1 chữ chứng minh đọc được | Chữ giao diện cao ít nhất 4% khung, được phóng to | Mắt, trên `sheet.jpg` |
| G2 không khung trống | Không quá 3 khung liền là một mảng màu phẳng | `look.py` |
| G3 kết ngắn | Hình đứng im ở cuối ≤ 1,4 giây (0,6–1,4 là đẹp). Cảnh cuối ≤ 25% thời lượng | `look.py` |
| G4 một nhân vật chính mỗi khung | Hai khối chỉ được đặt cạnh nhau khi một khối lớn gấp đôi khối kia | Mắt |

Kèm theo là các số đo:
- **AUDIO:** LUFS, LRA, đỉnh, khoảng câm, và tỉ lệ cú cắt trùng tiếng. Dân chuyên cho khoảng 1/3 cú cắt rơi đúng tiếng.
- **MOTION:** độ đổi hình trung bình giữa các khung. Phim người làm có trung vị 6,8/255, khoảng giữa 4,4–9,8.

MOTION là câu hỏi để tự xem lại, không phải cổng.

Đã thử (08/11/2026) trên thẻ `o-hoi-lat` ghép tiếng `sfx`: G0, G2, G3 đạt; −14,0 LUFS; MOTION 0,3/255, nghĩa là thẻ đứng yên phần lớn thời gian. Với thẻ phủ lên video người nói thì như vậy là bình thường, vì video phía sau mới là phần chuyển động.

## Dấu hiệu "rẻ tiền" (tóm tắt các luật gốc)

- **Đồ trang trí kiểu trang web:** tên thương hiệu ở góc, bộ đếm "02 / 05", mốc giờ kỹ thuật, thanh tiến trình, ngoặc góc.
- **Bố cục kiểu slide:** khối tiêu đề trái đứng yên, thiết bị bên phải; dòng nhỏ trên tiêu đề.
- **Thẻ giao diện chung chung:** thẻ bo góc có chấm trạng thái, số liệu bịa.
- **Phông màu phẳng đổi mỗi cảnh**, thẻ nhỏ lơ lửng giữa nền trống.
- **Mờ dần ở mọi chỗ:** dân chuyên dùng chuyển động (di chuyển, phóng) nhiều gấp khoảng 6 lần mờ dần.
- **Kết kiểu chân trang web:** logo, khẩu hiệu, nút, link; giữ thẻ kết quá 1,4 giây.
- **Tự nhận "đã kiểm"** mà không có số liệu, hoặc không xem video.

## Luật nghề có số (của dân chuyên)

- **Vào thì giảm tốc, ra thì tăng tốc.** Phần lớn quãng đường đi trong 4–8 khung đầu. Một chuyển động trung bình khoảng 10 khung (0,33 s). Mỗi phim nhiều nhất một cú nảy.
- **Cắt khi đang chuyển động**, không cắt lúc đứng yên. Cảnh mới bắt đầu khi đã đang chuyển động.
- **Đi vào từ to xuống**, không mọc từ số 0. Ví dụ: logo đập vào từ khoảng 3,5 lần, con trỏ vào từ 2–5 lần.
- **Chữ đi theo nhịp lời:** các từ cách nhau 2–12 khung. Chỉ gõ từng ký tự trong ô nhập của chính sản phẩm.
- **Bấm nút cho thật:** con trỏ dừng trước rồi mới bấm, nút lún 2–3 khung, đích phản hồi sau 1 khung.
- **Không khung chết:** khung đứng yên vẫn giữ một thứ còn sống (trôi nhẹ, con trỏ nháy, ánh sáng).

## Khi nào KHÔNG theo

Ba thẻ kỹ thuật trong repo (`moc-gio`, `con-tro-gia`, `so-muc-to`) dùng đúng những kiểu mà motionmaxxing coi là "rẻ tiền". Đó là các kiểu học từ số đo 86 reel marketing nhiều lượt xem.
- **Clip TikTok/Facebook cho hộ kinh doanh:** theo số đo 86 video ([ky-thuat.md](ky-thuat.md)).
- **Showreel, quảng cáo cao cấp, video ra mắt:** theo các luật trên và chạy `look.py --strict`.
