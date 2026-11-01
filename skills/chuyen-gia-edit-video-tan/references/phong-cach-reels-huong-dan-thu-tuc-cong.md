# Cách dựng Reel người dẫn + màn hình minh họa

Ghi chép về **hình ảnh và kỹ thuật edit** quan sát được trong một nhóm Reel công khai. Mục tiêu là rút ra ngôn ngữ dựng có thể áp dụng lại cho video của người dùng; không sao chép gương mặt, giọng nói, tên, phù hiệu, logo, watermark, lời thoại hay bộ nhận diện của người đăng.

## Nguồn và giới hạn quan sát

Ngày xem: 2026-10-14. Đã xem các Reel công khai sau trong trình phát Facebook:

- https://www.facebook.com/reel/4783217628577680/
- https://www.facebook.com/reel/1433144461508773/
- https://www.facebook.com/reel/2163296207592291/

Facebook chỉ hiện tùy chọn lưu Reel vào tài khoản, không có nút tải tệp video. Do đó ghi chép dựa trên việc xem playback và các khung hình ở nhiều thời điểm, không phải phân tích toàn bộ tệp ngoại tuyến. Mẫu Reel còn nhiều hơn ba video; danh sách dưới đây là toàn bộ kỹ thuật thấy được trong mẫu đã xem, không khẳng định bao quát toàn bộ trang. Không đủ bằng chứng để xác định phần mềm/preset cụ thể, font chính xác, toàn bộ keyframe, nhạc/SFX hoặc mọi điểm cắt.

## Bảng kỹ thuật đã quan sát

| Nhóm | Điều nhìn thấy | Cách tái tạo trung tính |
|---|---|---|
| Khung hình | Video dọc 9:16; người dẫn thường ở giữa, nền sáng và gọn. Cỡ trung và cận mặt/cận thân cùng xuất hiện. | Dựng khung dọc; giữ chủ thể ở vùng trung tâm. Chuyển giữa cỡ trung và cận bằng cut hoặc crop theo shot; không khẳng định có zoom camera nếu chỉ thấy đổi cỡ khung. |
| Người dẫn | Nhìn thẳng máy quay, biểu cảm và dùng tay chỉ/diễn đạt. Một số shot có động tác đưa vật/điện thoại lên. | Ưu tiên shot nói trực diện; cắt theo ý/lời nhấn. Giữ tay và vật minh họa trong khung an toàn. |
| Xen màn hình | Có đoạn chuyển sang giao diện smartphone/trang web chiếm gần hoặc toàn khung; có đoạn trở lại người dẫn. | Tách track screen-recording và presenter; cắt luân phiên theo bước. Phóng/crop vào vùng cần nhìn, giữ đủ lâu để người xem đọc được. |
| Callout tiêu đề | Banner chữ lớn, tương phản; thumbnail và một số đoạn có khối vàng bo góc, chữ đậm; có thẻ đỏ làm màu nhấn. | Dùng title card ngắn, chữ sans-serif đậm, tối đa một ý; animate nhẹ bằng pop/slide nếu cần. Màu cụ thể là ghi nhận của mẫu, có thể thay bằng palette thương hiệu riêng. |
| Chỉ điểm UI | Có mũi tên xanh phủ lên ảnh giao diện để chỉ trường nhập liệu. | Thêm mũi tên/viền highlight trên lớp overlay; đặt đúng tọa độ UI, chỉ một điểm mỗi nhịp. Dùng keyframe để di chuyển khi khung màn hình cuộn hoặc đổi trang. |
| Phụ đề | Chữ lớn nằm ở vùng thấp; khung hình đã thấy phụ đề vàng/đen có tương phản và nhấn một số từ. | Tạo caption ASS/SRT tối đa hai dòng, stroke/shadow để đọc trên nền sáng tối; tô màu từ khóa có chọn lọc. Canh vùng an toàn để không chồng giao diện nền tảng. |
| Lớp ảnh | Có khung lồng tài liệu/logo giao diện bên cạnh người dẫn; có đoạn hiển thị ảnh chụp bình luận/câu hỏi phía trên người dẫn. | Dùng split-screen hoặc overlay card; thêm shadow/viền mảnh nếu nền nhập với nhau. Giữ kích thước chữ trong ảnh đọc được; che dữ liệu riêng tư. |
| Chuyển động/nhòe | Một khung chuyển động quan sát được có vệt/ảnh bóng ngang quanh người dẫn, trông giống motion-smear/trailing. Chưa xác định chính xác hiệu ứng hay thời điểm áp dụng. | Nếu muốn thử, chỉ dùng rất ngắn ở một điểm nhấn/chuyển shot; so sánh preview với hard cut. Không gắn cho mọi cảnh và không ghi là preset cụ thể. |
| Nhịp | Cảm giác nhịp đến từ đổi giữa người dẫn, giao diện và card minh họa; không có timeline để xác định chính xác độ dài từng shot. | Chia shot theo ý hoàn chỉnh; thay hình ở chỗ bắt đầu thao tác hoặc cần bằng chứng trực quan. Tránh cắt liên tục khiến screen recording không đọc kịp. |
| Màu/ánh sáng | Người dẫn trên nền trung tính, ánh sáng khá đều; đồ họa vàng/đỏ/xanh nổi trên nền. | Giữ màu da tự nhiên, cân bằng sáng; dùng màu mạnh cho chữ/callout thay vì phủ filter nặng toàn khung. |
| Âm thanh | Không xác minh được cấu trúc nhạc, SFX, ducking hay hiệu ứng giọng qua mẫu xem này. | Không tự gán nhạc/SFX vào hồ sơ quan sát. Khi dựng mới, kiểm tra lời rõ trước; chỉ thêm nhạc có quyền và hạ dưới lời. |

## Công thức dựng để thử lại phong cách

Đây là công thức tái tạo **cách kể bằng hình ảnh**, không phải chép nguyên timeline từng video:

1. Mở bằng người dẫn ở cỡ trung hoặc một callout lớn.
2. Đổi sang cận cảnh hoặc crop nhấn ở câu quan trọng; chỉ gọi đó là zoom nếu thực sự có chuyển động phóng trong clip.
3. Cắt sang màn hình app/site khi bắt đầu minh họa; thêm mũi tên hoặc khung highlight đúng điểm đang nói.
4. Khi cần giải thích câu hỏi, đặt card/bình luận ở nửa trên và người dẫn ở nửa dưới, hoặc dùng full-screen card rồi quay về presenter.
5. Dùng caption ổn định ở phần thấp; highlight một từ khóa tại một thời điểm.
6. Kết bằng người dẫn hoặc khung kết quả; không thêm logo/watermark của nguồn tham khảo.

## Preset dựng tái sử dụng

- **Canvas:** 9:16; xuất 1080×1920, 30 fps nếu footage và nền tảng hỗ trợ.
- **Cut:** hard cut làm mặc định giữa presenter và screen-recording. Thử motion-smear rất ngắn như một biến thể riêng; không coi đó là hiệu ứng đã được xác định chắc chắn.
- **Punch-in:** ưu tiên crop cắt sang shot gần hơn tại điểm nhấn; chỉ dùng keyframed zoom khi footage hỗ trợ và chuyển động không gây chóng mặt.
- **Title card:** nền vàng bo góc hoặc màu thương hiệu, chữ đậm có tương phản cao; thẻ đỏ chỉ làm điểm nhấn.
- **UI pointer:** mũi tên/outline có màu tương phản, xuất hiện đúng lúc lời dẫn nhắc đến điểm cần bấm; biến mất sau khi hoàn tất bước.
- **Subtitles:** ASS/SRT, tối đa hai dòng, chữ lớn có stroke/shadow; đặt trong safe area, không che tay/mặt hoặc phần UI trọng yếu.
- **Layered composition:** presenter + ảnh chụp câu hỏi / screen-recording. Có thể dùng mask/crop để chia lớp; không làm ảnh minh họa nhỏ đến mức không đọc được.
- **Color:** correction nhẹ, nền sạch, màu da thật; tránh LUT nặng.
- **Effects not confirmed:** không mặc định thêm glitch, shake, flash, whip-pan, film grain, light leak, speed ramp, karaoke từng âm tiết hoặc nhạc/SFX. Chỉ dùng nếu footage/brief mới yêu cầu và preview cho thấy có lợi.

## Checklist edit

- [ ] Đã ghi shot size, cut, overlay, caption và callout riêng trong edit plan.
- [ ] Không nhầm đổi cỡ cảnh với zoom động.
- [ ] Mũi tên/highlight bám đúng vị trí trên screen recording qua mọi frame.
- [ ] Chữ tiếng Việt rõ dấu; caption không đè nhau hay che UI.
- [ ] Card/split-screen đủ lớn để đọc trên điện thoại.
- [ ] Các chuyển động graphic có điểm vào/ra ngắn, không gây rối.
- [ ] Màu da tự nhiên; nền và chữ đủ tương phản.
- [ ] Không sao chép mặt, giọng, phù hiệu, logo, watermark hoặc câu chữ đặc trưng của nguồn.
- [ ] Đã xem toàn bộ preview; không tuyên bố đã xác nhận effect/âm thanh khi chỉ có frame tĩnh.

## Dùng với skill dựng hiện có

Đọc file này cùng `references/project-schema.md` và `references/effect-catalog.md`. Chỉ áp dụng các lớp edit cần thiết cho brief; đây là bộ tham khảo kỹ thuật, không phải yêu cầu bắt buộc dùng tất cả hiệu ứng cùng lúc.
