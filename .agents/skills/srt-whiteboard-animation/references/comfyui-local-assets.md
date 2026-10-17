# Dùng ComfyUI cục bộ để chuẩn bị hình whiteboard

Đây là bước tạo **ảnh nguồn/line art** cho `srt-whiteboard-animation`; ComfyUI không tự xử lý SRT, không thay thế bước annotation và không render video whiteboard cuối.

## Quy trình

1. Mở ComfyUI Desktop hoặc bản local đã cài. Dùng workflow tạo ảnh cục bộ và model đã có hoặc được phép tải.
2. Tạo một ảnh 16:9 cho mỗi cảnh, theo brief đã duyệt và đúng visual spec trong `../SKILL.md`: nền giấy ấm `#F5EBD7`, nét phác màu xám đậm, điểm nhấn đỏ/cam/xanh tiết chế, ít chi tiết, nhiều khoảng trống, không chữ/nhãn/logo.
3. Giữ thiết kế nhân vật và vật thể nhất quán giữa các cảnh bằng prompt/reference/workflow giống nhau. Xem ảnh kết quả ở kích thước đầy đủ; sửa chữ giả, nét dính, chủ thể chồng lấn hoặc chi tiết không thuộc kịch bản trước khi đưa vào annotation.
4. Lưu PNG vào thư mục dự án whiteboard; ghi nhận kích thước pixel thật và dùng đúng kích thước đó cho `canvas.width`/`canvas.height`.
5. Tiếp tục các bước annotation, preview, render và QA trong `../SKILL.md`.

## Chi phí và quyền sử dụng

- Chạy model trên máy cá nhân không gọi API và không tự phát sinh phí API. Vẫn cần tải model, dung lượng lưu trữ, phần cứng phù hợp và điện năng.
- Nếu workflow có cloud/API nodes, hãy tắt chúng hoặc dùng `--disable-api-nodes` theo hướng dẫn ComfyUI khi muốn giữ xử lý offline. Không bật dịch vụ tính phí hoặc dùng credential nếu người dùng chưa yêu cầu.
- Kiểm tra giấy phép của model, workflow và custom nodes riêng; giấy phép GPL-3.0 của ComfyUI không tự cấp quyền sử dụng mọi model/asset đi kèm.
- Không tải ảnh riêng tư lên dịch vụ đám mây. Dùng dữ liệu demo hoặc đã được cho phép.

ComfyUI chính thức: [Comfy-Org/ComfyUI](https://github.com/Comfy-Org/ComfyUI). Repo không được vendor vào `tan-ai-skills`; đây chỉ là hướng dẫn tùy chọn.
