# Hồ sơ giọng cá nhân được ủy quyền

Chỉ dùng chế độ này khi chính chủ xác nhận mẫu giọng thuộc về họ và cho phép sử dụng cho nội dung cụ thể.

## Tạo mẫu kỹ thuật

Chạy:

```bash
python scripts/prepare_voice_profile.py input.mp4 \
  --subject "Tên chủ thể" \
  --consent-scope "MC của chính chủ; tiếng Việt và tiếng Anh" \
  --output-dir private/voice-profiles/ten-ho-so
```

Script tạo `reference.wav` mono 48 kHz và `profile.json`. Đây chỉ là mẫu âm thanh đã chuẩn hóa, chưa phải mô hình giọng và chưa đăng ký với nhà cung cấp.

## Đăng ký và sử dụng

- Chỉ đăng ký giọng khi người dùng chủ động yêu cầu và nhà cung cấp hỗ trợ xác minh/đồng ý của chính chủ.
- Lưu `voice_profile_id` trong `private/voice-profiles/.../provider.json`; không ghi token API.
- Tạo bản thử 20–30 giây trước, nghe lại phát âm tiếng Việt, tiếng Anh, tên riêng và số liệu.
- Không tự dùng hồ sơ cho nội dung mới. Trước mỗi lần tổng hợp, nêu kịch bản hoặc mục đích và nhận xác nhận của người dùng.
- Không dùng cho quảng cáo, phát biểu chính trị, tài chính, pháp lý hoặc nội dung có thể gây hiểu nhầm nếu chưa có chấp thuận cụ thể.

## Hợp đồng hồ sơ

`profile.json` gồm: `subject`, `self_attested`, `consent_scope`, `consent_recorded_at`, thông số nguồn và đường dẫn mẫu tương đối. Tệp nằm trong `private/` và bị Git bỏ qua.
