# Rút kinh nghiệm sau mỗi video

Mục tiêu: **video sau khá hơn video trước**, và cái khá hơn đó phải nằm lại trong repo, không nằm
trong trí nhớ của một phiên làm việc. Nhưng skill không được phình ra vì nhận xét nhất thời.

Chạy phần này **ngay sau khi giao video**, trước khi đóng phiên. Không để dồn.
Gọi nhanh bằng `/rut-kinh-nghiem`.

## Luật gốc: kinh nghiệm chỉ tính khi có chỗ neo

Một bài học chỉ được coi là "đã lưu" khi nó biến thành **một trong ba thứ** sau:

| Dạng | Khi nào dùng | Neo vào |
|---|---|---|
| `test:` | máy đáng lẽ bắt được lỗi này | một class trong `tests/` |
| `script:` | thành tham số mặc định hoặc một luật chặn trong code | file `.py` trong `scripts/` |
| `doc:` | thông số đã chốt, quy ước trình bày, thứ tự thao tác | file trong `references/` |

Ghi chú suông không tính — lần sau vẫn quên. Nếu một bài học không neo được vào đâu trong ba chỗ
trên thì nó chưa đủ rõ để thành kinh nghiệm; viết lại cho cụ thể hơn.

Sở thích riêng của người dùng (không thuộc kỹ thuật dựng) thì lưu vào memory, không nhét vào đây.

## Bốn câu hỏi cố định

Sau mỗi video, trả lời đúng bốn câu, ngắn gọn, **kèm số đo thật**:

1. **Chỗ nào phải làm lại từ hai lần trở lên?** — làm lại nhiều lần nghĩa là quy trình còn thiếu
   một bước hoặc một tham số chưa chốt.
2. **Tham số nào lần này chốt được?** — toạ độ, cỡ chữ, mức LUFS, thời lượng, ngưỡng. Ghi con số,
   không ghi "vừa phải".
3. **Lỗi nào máy đáng lẽ bắt được mà không bắt?** — đây là loại quý nhất: biến thẳng thành test.
4. **Cái gì hay, nên giữ làm mặc định?**

## Bài học nào được đưa vào skill

Không phải cái gì cũng thành luật. Phân loại trước:

| Loại | Xử lý |
|---|---|
| Sở thích cho riêng một video/chiến dịch | giữ trong hồ sơ dự án, **không** thành mặc định toàn cục |
| Mẫu dựng đã được người dùng xác nhận và dùng lại được | đưa vào `references/`, ghi rõ **phạm vi áp dụng** |
| Lỗi kỹ thuật đo được | sửa script **và** thêm test hồi quy |
| Sai sự thật, mất dữ liệu, vi phạm quyền, mất an toàn | thành ràng buộc cứng ngay, kèm kiểm tự động nếu làm được |
| Ý tưởng chưa được xem, chưa ai xác nhận | để nguyên dạng đề xuất, đừng viết như quy trình chuẩn |

Một bài học chỉ đủ điều kiện đưa vào khi trả lời được: **điều gì tốt hơn · bằng chứng nào · áp dụng
ở đâu · trường hợp nào KHÔNG nên áp dụng.** Thiếu vế cuối là dấu hiệu bài học còn mơ hồ.

## Sau đó làm gì

1. Ghi một dòng vào [nhat-ky-ban-tin.md](nhat-ky-ban-tin.md).
2. Với mỗi bài học, tạo chỗ neo tương ứng: thêm test, sửa mặc định trong script, hoặc thêm dòng
   vào bảng "Sai sót đã gặp" của [phong-cach-att-news.md](phong-cach-att-news.md).
3. Chạy `python -m unittest discover -s tests` và `python scripts/sync_skills.py --force`.
4. Commit riêng một commit cho phần rút kinh nghiệm, để sau này lần lại được video nào sinh ra luật nào.
5. **Trước video kế tiếp**, đọc lại các dòng nhật ký cùng thể loại và cùng định dạng đầu ra.

`tests/test_kinh_nghiem.py` kiểm nhật ký: mọi chỗ neo khai trong cột **Chốt bằng** phải có thật.
Khai `test:TenClass` mà class đó không tồn tại thì test đỏ — chặn thói quen ghi cho có.

Chỉ sửa nguồn chuẩn `skills/`; không sửa `.claude/skills/` hay `.agents/skills/` vì lần đồng bộ sau
sẽ ghi đè. Đồng bộ xong **không** đồng nghĩa đã commit; chỉ commit/push khi người dùng yêu cầu.

## Đo "video sau tốt hơn" bằng gì

Không đánh giá bằng cảm giác chung. So theo tiêu chí liên quan tới chính yêu cầu đó: đúng nội dung
và số liệu · bố cục logic · đúng thời lượng · chất lượng chọn cảnh · độ mượt điểm nối · độ rõ lời ·
đồng bộ giọng–phụ đề · chữ đọc được trên điện thoại · đúng nhận diện ATT NEWS · số lỗi kỹ thuật ·
**số vòng phải sửa lại**. Không hy sinh tính chính xác hay an toàn để đổi lấy nhịp nhanh và hiệu ứng.

## Đừng làm

- Đừng ghi bài học khi chưa kiểm chứng. "Hình như để 0,3 s thì đẹp hơn" không phải kinh nghiệm.
- Đừng biến mọi thứ thành luật cứng. Thứ phụ thuộc từng video (chọn cảnh nào, nói gì) thì không
  chốt được; chỉ chốt thứ lặp lại ở mọi video.
- Đừng sửa lại bài học cũ cho gọn. Nếu một luật hoá ra sai, **thêm dòng mới ghi rõ đã thay** và
  nói vì sao, giữ lại dấu vết.
- Đừng commit clip nguồn, file render, mẫu giọng, voice embedding, token, ID hồ sơ nhà cung cấp
  hay đường dẫn chứa dữ liệu riêng. Cần ví dụ thì dùng dữ liệu giả.
