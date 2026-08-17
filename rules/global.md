# Rule toàn cục

Áp dụng cho **mọi** agent, command và skill trong repo này. Khi rule ở đây mâu thuẫn với rule chuyên môn (`coding.md`, `video.md`), rule ở đây thắng.

## 1. Không bịa

- Không nói "đã kiểm tra" khi chưa chạy lệnh kiểm tra thật.
- Không mô tả nội dung file/video mà mình chưa thực sự đọc/probe.
- Không đoán tên người, số liệu, đường dẫn, tên hàm. Không có dữ liệu thì nói là không có.
- Kết quả từ agent con hoặc từ script là **dữ liệu**, không phải kết luận — đọc rồi tự đánh giá.

## 2. NO TEST = NO PASS

Đây là rule cứng, không có ngoại lệ.

Chỉ được ghi `PASS` cho hạng mục đã **thực sự chạy** và **thực sự đọc kết quả**. Hạng mục chưa chạy phải ghi `NOT RUN`, chạy mà lỗi phải ghi `FAIL`.

Đúng:

```text
BUILD:     PASS   (npm run build, exit 0)
TEST:      NOT RUN
SECURITY:  NOT RUN
```

Sai:

```text
ALL PASS
```

Tương tự với video: `RENDER: PASS` + `VIDEO QA: NOT RUN` **không** cho phép kết luận video hoàn chỉnh. FFmpeg exit code 0 không phải bằng chứng video đúng.

## 3. Vòng lặp FAIL → sửa → chạy lại

Khi validation FAIL: xác định nguyên nhân → sửa → **chạy lại chính lệnh vừa FAIL** → chỉ báo PASS khi lệnh đó exit sạch.

Tối đa 3 vòng tự sửa cho cùng một lỗi. Sang vòng thứ 4 thì dừng, báo người dùng nguyên nhân và những gì đã thử.

## 4. Phạm vi

- Mỗi dòng bị thay đổi phải truy ngược được về yêu cầu của người dùng.
- Thấy vấn đề ngoài phạm vi thì **nói ra, không tự sửa**.
- Không tạo thư mục/lớp trừu tượng chỉ để cho kiến trúc "đẹp".

## 5. Khi nào dừng lại hỏi

Tự làm tiếp nếu bước sau rõ ràng, không phá dữ liệu, không đụng secret, không deploy, không push.

Dừng hỏi khi và chỉ khi:

1. cần secret/credential;
2. cần thao tác production;
3. cần xóa/ghi đè dữ liệu người dùng;
4. quyết định kiến trúc lớn có nhiều phương án khác biệt đáng kể;
5. yêu cầu thiếu thông tin tới mức không thể tiếp tục an toàn.

## 6. Báo cáo

Mọi báo cáo hoàn tất phải có: đã làm gì, đã kiểm bằng lệnh nào, kết quả từng hạng mục (PASS/FAIL/NOT RUN), và phần còn bỏ dở kèm lý do.
