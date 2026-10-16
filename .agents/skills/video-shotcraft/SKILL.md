---
name: video-shotcraft
description: Dùng thư viện shot cinematic Remotion để dựng video giới thiệu sản phẩm, SaaS, website hoặc giao diện app; chọn và triển khai các mẫu chuyển động từ video-shotcraft, kết hợp với nhận diện thương hiệu và dữ liệu thật. Kích hoạt khi người dùng muốn video product launch/promo có motion design, muốn dùng shot recipe, hoặc nhắc video-shotcraft.
---

# Video Shotcraft — shot cinematic cho video sản phẩm

Skill này bổ sung ngôn ngữ chuyển động và shot recipe cho video quảng bá sản phẩm. Nguồn tham khảo là repo công khai [Vincentwei1021/video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft), được cấp phép Apache-2.0. Repo mô tả thư viện **124 recipe cards / khoảng 150 shot**; số lượng có thể thay đổi theo phiên bản. Đây là shot/motion recipe dựng bằng Remotion, không phải 150 transition độc lập kiểu CapCut.

## Dùng đúng phạm vi

- Sản phẩm, SaaS, website, dashboard, app, tính năng mới → dùng skill này để chọn ngôn ngữ shot; phối hợp `video-san-pham` nếu làm video quảng cáo từ dữ liệu sản phẩm, hoặc `remotion-create`/`remotion-markup` để dựng bằng Remotion.
- Video quay sẵn cần cắt, chỉnh màu, phụ đề → định tuyến sang `bien-tap-video`/`video-use`; chỉ lấy shotcraft làm tham khảo cho đoạn đồ họa nếu phù hợp.
- Chỉ cần một hiệu ứng FFmpeg/CapCut đơn lẻ → định tuyến sang `hieu-ung-video`.
- Bản tin, sự kiện, vlog, phỏng vấn → không ép phong cách product-film; dùng skill đúng thể loại.

## Quy trình

1. Hiểu sản phẩm, người xem, thông điệp và CTA. Nếu đầu vào là website/app, chỉ chụp trang công khai hoặc dữ liệu demo đã được phép; không đưa dữ liệu khách hàng, nội bộ hay bí mật vào khung hình.
2. Chọn hướng dựng: video hoàn chỉnh hay một shot; template định sẵn hay sáng tác mới. Tôn trọng lựa chọn đã nêu, không hỏi lại điều người dùng đã chốt.
3. Duyệt danh mục mẫu hiện hành tại [Shotcraft Gallery](https://vincentwei1021.github.io/video-shotcraft/) hoặc các recipe trong repo nguồn. Tìm tên và đọc đầy đủ recipe được chọn; nếu triển khai bằng code, xem demo Remotion đi kèm để giữ đúng thời điểm, easing, thứ tự lớp và thông số quan trọng. Không bịa rằng đã kiểm tra một recipe khi chưa mở nó.
4. Chọn ít shot nhưng có vai trò rõ: mở đầu, giới thiệu sản phẩm, giải thích thao tác/tính năng, nhấn kết quả, kết thúc/CTA. Mỗi shot chỉ có một hành động thị giác chính; dùng hold để người xem đọc được nội dung.
5. Dùng screenshot thật của sản phẩm khi mục tiêu là giới thiệu UI. Giữ đúng typography, màu, khoảng cách và hình dạng của sản phẩm; thay dữ liệu thật bằng dữ liệu giả lập khi cần. Không dựng giao diện giả làm người xem hiểu nhầm đó là tính năng có thật.
6. Dựng bằng Remotion với thời lượng, fps, easing và hạt giống ngẫu nhiên xác định; không thêm hiệu ứng chỉ để phô diễn. Căn nhịp cắt với nhạc khi có beat rõ, đồng thời giữ lời thoại và khả năng đọc.
7. Render preview, xem các khung hình ở đầu/giữa/cuối từng shot và kiểm tra lỗi chữ, crop, tràn khung, nhấp nháy, chuyển động giật, âm lượng; sửa rồi mới xuất bản.
8. Ghi lại tên recipe nguồn và những thay đổi đã làm. Nếu không thể truy cập Gallery/repo nguồn, nói rõ giới hạn và chỉ dùng các nguyên tắc chung bên dưới.

## Bản đồ ngôn ngữ shot

Các ví dụ dưới đây là nhóm ý tưởng, không phải hướng dẫn tái tạo nguyên xi. Tìm recipe tương ứng trong Gallery trước khi dùng tên chính xác.

| Nhóm | Cách dùng trong câu chuyện sản phẩm | Ví dụ trong thư viện |
|---|---|---|
| Mở đầu / thương hiệu | Tạo tò mò rồi khóa tên sản phẩm | `text-as-mask`, `logo-shrink-wordmark-lockup` |
| Camera / chiều sâu | Tạo cảm giác khám phá giao diện hoặc cấu trúc | `exploded-view`, `space-camera-moves` |
| Chuyển cảnh bằng vật thể | Dùng thành phần giao diện làm cầu nối giữa cảnh | `card-flock-tumble` |
| Typography động | Nhấn một lợi ích hoặc câu tagline ngắn | `flying-words` |
| UI entrance | Đưa thẻ, panel hoặc màn hình vào bố cục | `card-stack`, `row-embed` |
| Tương tác | Cho thấy thay đổi trạng thái có ý nghĩa | `palette-theme-ripple` |
| Dữ liệu | Làm nổi biến động/chỉ số bằng chuyển động có chủ đích | `axis-rescale-shock` |
| Ánh sáng / nhấn mạnh | Dẫn mắt đến một vùng hoặc thông tin quan trọng | `spotlight-sweep`, `spotlight-hero-card` |
| Nhịp điệu | Cắt theo nhạc hoặc chuỗi thông tin ngắn | `paparazzi-flash` |
| Kết / CTA | Thu chuyển động về một điểm kết thúc dễ nhớ | `input-morph-assemble` |

Không dùng dồn nhiều shot mạnh liên tiếp. Ưu tiên một chuyển động chủ đạo cho mỗi nhịp nội dung, sau đó để hình ổn định đủ lâu để đọc.

## Quyền sử dụng và ghi nguồn

- Không chép toàn bộ mã, recipe, demo, template hoặc media của repo vào dự án này. Khi cần mã nguồn một shot, lấy đúng tệp từ nguồn, giữ thông báo bản quyền/giấy phép áp dụng và tuân thủ Apache-2.0.
- Âm thanh và media trong repo nguồn có thể có giấy phép riêng; kiểm tra file attribution/giấy phép của chính asset trước khi dùng. Không mặc định mọi audio đều theo Apache-2.0.
- Remotion có điều khoản cấp phép riêng; kiểm tra [Remotion license](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md) theo loại hình sử dụng.
- Không tự đăng video, gửi tác phẩm cho bên thứ ba hoặc dùng thông tin đăng nhập/API publishing nếu người dùng chưa yêu cầu.

## Câu lệnh gợi ý

- “Dùng shot recipe cinematic để làm video giới thiệu sản phẩm này.”
- “Tìm một shot trong Video Shotcraft để nhấn tính năng dashboard; giữ đúng màu và font sản phẩm.”
- “Thêm một shot spotlight vào video Remotion hiện tại, xem recipe nguồn rồi mới triển khai.”
