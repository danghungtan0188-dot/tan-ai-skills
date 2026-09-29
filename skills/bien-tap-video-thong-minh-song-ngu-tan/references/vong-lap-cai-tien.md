# Vòng lặp cải tiến sau mỗi video

Mục tiêu: video sau kế thừa những gì đã được chứng minh là tốt ở video trước, nhưng skill không phình ra bởi nhận xét nhất thời, dữ liệu riêng tư hoặc quy tắc mâu thuẫn.

## Chu trình bắt buộc

1. **Ghi nhận:** sau khi giao bản xem thử hoặc bản cuối, ghi lại phản hồi cụ thể của người dùng và kết quả QA.
2. **Phân loại:** đánh dấu mỗi bài học là `candidate`, `confirmed`, `promoted` hoặc `rejected`.
3. **Kiểm chứng:** đối chiếu với video, log, thông số đo hoặc phản hồi xác nhận; nêu rõ bài học áp dụng cho loại video nào và khi nào không áp dụng.
4. **Nâng cấp:** chỉ đưa bài học đủ điều kiện vào nguồn chuẩn `skills/bien-tap-video-thong-minh-song-ngu-tan/`; sau đó đồng bộ các bản sao bằng `python scripts/sync_skills.py --force`.
5. **Xác minh:** chạy test liên quan, kiểm liên kết tài liệu và `python scripts/sync_skills.py --check` trước khi coi nâng cấp là hoàn tất.
6. **Kế thừa:** trước khi dựng video tiếp theo, đọc các bài học `confirmed`/`promoted` cùng thể loại, thương hiệu và định dạng đầu ra.

## Khi nào được đưa vào repo hoặc skill

- **Sở thích chỉ dành cho một video/chiến dịch:** giữ trong hồ sơ dự án, không biến thành mặc định toàn cục.
- **Mẫu dựng được người dùng xác nhận và có khả năng dùng lại:** đưa vào tài liệu tham chiếu, ghi rõ phạm vi áp dụng.
- **Lỗi kỹ thuật hoặc điều kiện có thể đo:** sửa script và thêm test hồi quy khi có thể.
- **Lỗi an toàn, sai sự thật, mất dữ liệu hoặc vi phạm quyền:** nâng thành ràng buộc cứng ngay, kèm kiểm tra tự động nếu khả thi.
- **Ý tưởng chưa được xem hoặc chưa được người dùng xác nhận:** giữ ở trạng thái `candidate`; không quảng bá thành quy trình chuẩn.

Một bài học chỉ được `promoted` khi trả lời được bốn câu hỏi: điều gì tốt hơn, bằng chứng nào chứng minh, áp dụng ở đâu, và trường hợp nào không nên áp dụng.

## Mẫu ghi rút kinh nghiệm

Lưu nhật ký làm việc ngoài thư mục skill nếu nội dung có tên người, dữ liệu dự án hoặc đường dẫn riêng tư. Có thể dùng mẫu ngắn sau:

```markdown
## Video / ngày
- Loại video, tỷ lệ khung hình, thời lượng đích:
- Điều người dùng thích:
- Điều cần sửa:
- Nguyên nhân đã xác minh:
- Bài học đề xuất:
- Bằng chứng / mốc thời gian / kết quả QA:
- Phạm vi áp dụng và ngoại lệ:
- Trạng thái: candidate | confirmed | promoted | rejected
- Thay đổi repo/test liên quan:
```

## Ranh giới lưu trữ

Không commit clip nguồn, file render, mẫu giọng, voice embedding, token, ID hồ sơ nhà cung cấp, dữ liệu cá nhân hoặc đường dẫn chứa bí mật. Repo chỉ lưu quy trình tổng quát, preset không nhạy cảm, mã nguồn và test. Nếu bài học cần ví dụ, dùng dữ liệu giả hoặc mô tả đã loại thông tin riêng tư.

Chỉ sửa nguồn chuẩn; không sửa trực tiếp `.claude/skills/` hoặc `.agents/skills/` vì lần đồng bộ sau sẽ ghi đè. Cập nhật cục bộ và đồng bộ không đồng nghĩa với commit hoặc push; chỉ commit/push khi người dùng yêu cầu.

## Tiêu chuẩn “video sau tốt hơn”

Không đánh giá bằng cảm giác chung. So sánh theo các tiêu chí phù hợp với yêu cầu: đúng nội dung và số liệu, bố cục logic, đúng thời lượng, chất lượng chọn cảnh, độ mượt chuyển cảnh, độ rõ lời, đồng bộ giọng/phụ đề, khả năng đọc chữ, nhận diện ATT NEWS, lỗi kỹ thuật và số vòng sửa. Chỉ tối ưu tiêu chí có liên quan; không hy sinh tính chính xác hoặc an toàn để tăng nhịp hay hiệu ứng.
