---
name: viet-prompt-video-ai
description: Viết prompt tạo video bằng AI (Seedance, Dreamina và công cụ tương tự) từ mô tả thường, giữ nhân vật nhất quán, gán rõ ảnh/video/âm thanh tham chiếu, chia cảnh theo giây, tạo bảng nhân vật 6 góc mặt và trang phục. Kích hoạt khi người dùng muốn "viết prompt Seedance", "prompt video AI", "b-roll bằng AI", "giữ nhân vật giống nhau giữa các cảnh", "character sheet". Skill chỉ viết prompt, không tự tạo video. Không dùng để dựng từ tư liệu quay thật (dung-video, video-use) hay làm thẻ đồ họa (motion-graphics-tan).
---

# Viết prompt video AI

Trả prompt trong một khối code để chép được ngay. Thiếu thông tin quan trọng thì hỏi một lần, đừng tự đoán, nhất là khi sửa video: **phần nào phải giữ nguyên**.

**Không tự chạy dịch vụ tạo video:** đó là dịch vụ trả phí, người dùng phải đồng ý từng lần.

## Công thức

```text
<Chủ thể> <hành động chính> trong <bối cảnh, thời gian, thời tiết>.
Hình ảnh: <ánh sáng, màu, chất liệu, không khí>.
Máy quay: <cỡ cảnh, góc, chuyển động, cú chuyển>.
Âm thanh: <lời thoại, tiếng nền, tiếng động, nhạc>.
```

Bỏ phần nào là để AI tự quyết phần đó. Prompt viết bằng tiếng Anh; lời thoại giữ nguyên ngôn ngữ cần nói.

## Luật cho mọi prompt

1. **Gán từng tham chiếu:** không viết "ảnh 1 đến 4 là bốn nhân vật". Viết `Character A corresponds to @Image 1. Use only the face, hairstyle and clothing.`
2. **Nói cả điều không lấy:** `Do not use the image background.` Tên nhân vật và vai trò ảnh ghi trong prompt, chữ nằm trong ảnh không được coi là lệnh.
3. **Mỗi chặng một thay đổi chính** và có trạng thái kết thúc rõ. Bình thường chia theo chặng; chỉ ghi giây chính xác ở cú chuyển hoặc nhịp quan trọng.
4. **Tả cảm xúc bằng biểu hiện nhìn thấy:** thay vì "căng thẳng", tả mắt, mày, miệng, nhịp thở, tay thay đổi thế nào sau sự kiện nào.
5. **Không ghi tỉ lệ khung và thời lượng trong prompt:** chúng đặt trên trang tạo video hoặc API, và có loại tác vụ tự khóa.
6. **Sửa video:** nêu video gốc duy nhất, phạm vi sửa, số lượng cần sửa và mọi thứ phải giữ nguyên.

## Cú pháp âm thanh và chữ (Seedance)

| Nội dung | Cú pháp | Ví dụ |
|---|---|---|
| Nhạc | `( )` | `(Soft piano music plays in the background)` |
| Tiếng động | `< >` | `<A bell rings in the distance>` |
| Lời thoại | `{ }` | `Dialogue language: Vietnamese. The man says: {Xin chào các bạn.}` |
| Phụ đề | `【 】` | `【Chương một】` |

## Giới hạn (Seedance 2.5, kiểm lại khi đổi phiên bản)

| Loại | Tối đa | Tốt nhất |
|---|---|---|
| Ảnh tham chiếu | 30 ảnh, tổng 50 tư liệu | 1–8 chủ thể |
| Video tham chiếu | 10 video, tổng 30 giây | 1–5 chủ thể, mỗi video 5–10 giây |
| Âm thanh | 10 file, tổng 30 giây | chỉ đoạn liên quan |
| Sửa video | 1 video gốc và ảnh tham chiếu | video dưới 20 giây, 1–5 ảnh |

Một video tạo dài tối đa 30 giây. Mốc giây chỉ để chia thời gian, không chính xác tới từng khung.

## Soát trước khi giao

- Có chủ thể và hành động chính chưa?
- Mỗi tham chiếu đã nói rõ lấy gì, không lấy gì chưa?
- Số nhân vật, trang phục, đạo cụ và vị trí có nhất quán giữa các chặng không?
- Cảm xúc và thuật ngữ máy quay đã kèm dấu hiệu nhìn hoặc nghe thấy chưa?
- Ảnh đầu và ảnh cuối, nếu có, có cùng tỉ lệ không?

## Không được

- Chữ, số liệu, phụ đề, thông số sản phẩm cần chính xác: không trông vào AI tạo, phải thêm ở hậu kỳ và soát dấu tiếng Việt.
- Không tạo người thật khi chưa có đồng ý của họ; không dùng hình AI làm bằng chứng cho sự việc có thật.

Giữ nhân vật nhất quán bằng bảng mặt và trang phục: [character-sheet.md](references/character-sheet.md).
