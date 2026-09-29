# Dựng bản tin từ video thô

**Yêu cầu:** người dùng đưa cả thư mục clip tự quay → xem hết → cắt ghép thành **một** bản tin
có nội dung và logic chuẩn truyền hình, **độ dài do người dùng đặt**.

## Phân vai

- **Máy đo, máy tính toán, máy kiểm luật.** Script không tự chọn cảnh nào nói về cái gì.
- **Claude xem ảnh rồi chọn cảnh.** Nội dung là việc của mắt, không của ffprobe.
- **Người dùng duyệt bảng cảnh trước khi cắt.** `cut_authorized=false` vẫn là mặc định.

## Ba bước

1. `survey_rushes.py FOLDER --out rushes.json --sheet contact.jpg`
   Đo từng clip (thời lượng, khung, fps, xoay, LUFS), tách cảnh, chấm nét/sáng/động cho từng cảnh,
   xuất contact sheet có nhãn `clip.canh t=…` để Claude nhìn mà chọn.
2. Claude viết `chon-canh.json` — mỗi dòng: clip, in/out, thuộc mục nào, **lý do chọn**.
   `build_edit_plan.py rushes.json chon-canh.json --target GIAY --out edit-plan.json`
   Kiểm luật dựng + co giãn b-roll cho khớp đúng độ dài yêu cầu. In bảng để người dùng duyệt.
3. `assemble.py edit-plan.json --out rough.mp4` → `render_att.py` gắn đồ hoạ → `qa.py` kiểm.

## Luật dựng máy kiểm được

- Cảnh b-roll 2,5–8 giây; phát biểu không bị ràng buộc trên.
- Không hai cảnh liền nhau cùng clip mà cùng cỡ cảnh.
- Mở đầu phải có cảnh toàn (establishing).
- Không cắt vào giữa câu nói (mốc cắt cách ranh giới cảnh ≥ 0,4 s).
- Tổng khớp độ dài yêu cầu ±2 s — co giãn ở b-roll, không đụng phát biểu.
