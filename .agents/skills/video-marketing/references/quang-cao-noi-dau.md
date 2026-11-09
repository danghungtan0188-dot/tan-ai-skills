# Video quảng cáo mở bằng nỗi đau

Học từ một reel quảng cáo dịch vụ làm video vị trí nhà đất cho môi giới (khoảng 260 nghìn lượt xem, xem ngày 09/11/2026). Dùng cho video quảng bá dịch vụ, sản phẩm, 9:16, 20–40 giây.

## Khung 5 nhịp

| Nhịp | Thời điểm | Nội dung | Cách dựng trong repo |
|---|---|---|---|
| **1. Nỗi đau** | 0–3 giây | Một câu hỏi đúng nỗi đau của **một nhóm khách cụ thể**, có con số: "Môi giới vẫn mất 2 tiếng dựng 1 video căn nhà?" | Chữ to giữa khung, `motion-graphics-tan` kiểu Kinetic Type hoặc Neo-brutalism |
| **2. Kết quả thật** | 3–15 giây | Cho xem chính sản phẩm đang chạy, không kể tính năng | Video mẫu thật làm bằng repo; với nhà đất dùng mẫu `ViTriNha` của `ban-do-video` |
| **3. Lợi ích** | 15–25 giây | 3–4 lợi ích ngắn, mỗi cái gắn một hình đang chạy | Thẻ checklist kiểu `doodle`, hiện đúng lúc nói bằng `tim_cau_noi.py` |
| **4. Dễ dùng** | 25–30 giây | Bỏ rào cản: "làm trên điện thoại", "không cần biết dựng" | Một câu, một hình thao tác thật |
| **5. Mời dùng thử** | 30–35 giây | Lời mời ít rủi ro: "làm thử 1 video miễn phí" và một hành động duy nhất | Thẻ kêu gọi kiểu `neo-brutalism`, giữ 2 giây cuối |

Kịch bản viết bằng skill `kich-ban-video-marketing` (có luật không bịa); prompt cảnh AI, nếu cần, viết bằng `viet-prompt-video-ai`.

## Luật

- **Một nhóm khách, một nỗi đau.** Nói chung chung ("ai cũng cần video") sẽ không ai thấy mình trong đó.
- **Con số phải thật:** thời gian tiết kiệm, giá, số video phải lấy từ người dùng, thiếu thì bỏ con số.
- **Hình ở nhịp 2 phải là sản phẩm thật** đã làm, không dùng hình minh họa giả làm kết quả.
- **Bán kết quả, không bán công cụ:** nhấn vào thứ khách được (đăng được ngay, khách để lại số), không kể tên phần mềm.
- **Ưu đãi và lời mời** chỉ ghi điều người dùng thật sự cung cấp.
- Video quảng bá dịch vụ của chính người dùng: theo các quy ước đã chốt (nhận làm, không dạy; không phụ đề đoạn tự nói).

## Video vị trí nhà đất

Phần bản đồ đã có ở `ban-do-video`: quét trường, chợ, bệnh viện, đường lớn quanh căn nhà, vẽ đường đi thật kèm số km, thẻ giá và số liên hệ, video 9:16.

Còn thiếu so với reel mẫu: **giọng đọc và phụ đề** (mẫu `ViTriNha` chưa có giọng), và **trang web riêng cho từng căn để khách để lại số** (đó là việc thuộc nhánh APP, chưa làm).
