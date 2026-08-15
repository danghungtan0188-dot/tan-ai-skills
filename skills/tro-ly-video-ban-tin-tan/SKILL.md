---
name: tro-ly-video-ban-tin-tan
version: 1.0.0
description: |
  Trợ lý sản xuất video bản tin từ kịch bản đến file MP4 hoàn chỉnh. Kết hợp HeyGen presenter,
  ưu tiên giọng nữ Hoài - Natural khi có sẵn, hậu kỳ FFmpeg theo phong cách bản tin/CapCut,
  banner theo ngữ cảnh, ATT NEWS, Facebook/Zalo nhỏ gọn, kiểm tra chất lượng và khả năng phát/tải.
argument-hint: "[script_or_video] [--style att-news] [--voice Hoai-Natural]"
allowed-tools: Bash, Read, Write, WebFetch, mcp__heygen__*
---

# Trợ lý Video Bản tin Tấn

## Mục tiêu
Tạo video bản tin chính thống, hiện đại, mượt, có MC HeyGen, giọng đọc tiếng Việt rõ và hậu kỳ chuyên nghiệp. Không lạm dụng hiệu ứng; ưu tiên dễ xem, đúng nội dung, không che nhân vật và có thể phát/tải ổn định.

## Khi nào dùng
Dùng khi người dùng gọi `$tro-ly-video-ban-tin-tan` hoặc yêu cầu:
- tạo video bản tin từ kịch bản;
- tạo MC HeyGen rồi hậu kỳ;
- edit video sự kiện, hội nghị, tuyên truyền;
- thêm banner, lower-third, logo ATT NEWS, Facebook/Zalo;
- thêm hiệu ứng kiểu CapCut bằng FFmpeg;
- xuất video MP4 sẵn đăng Facebook/Zalo/cổng thông tin.

## Pipeline bắt buộc
1. **Input Check**: đọc kịch bản, kiểm video/audio, lấy duration/fps/resolution bằng ffprobe.
2. **Script Check**: sửa lỗi đọc, số, ngày tháng, tên riêng; không tự bịa nội dung.
3. **HeyGen**: nếu cần MC, dùng HeyGen theo skill `heygen-video`. Ưu tiên avatar đã có của người dùng.
4. **Voice**: ưu tiên `Hoài - Natural` nếu HeyGen hiện có đúng voice đó. Yêu cầu: nữ miền Nam, rõ, ấm, truyền cảm, tốc độ hơi nhanh kiểu phát thanh viên. Không giả định voice ID; phải resolve từ danh sách voice hiện tại.
5. **Scene Map**: chia MC / B-roll / người phát biểu / hoạt động / kết. Ghi timecode.
6. **Edit Plan**: chọn banner và effect theo ngữ cảnh, không phủ kín màn hình.
7. **FFmpeg Edit**: dùng công thức trong `references/ffmpeg-recipes.md`.
8. **ATT NEWS Preset**: áp dụng `references/att-news.md` khi video thuộc hệ ATT NEWS.
9. **QC**: chạy checklist trong `references/qc-checklist.md`.
10. **Delivery**: chỉ giao file khi ffprobe xác nhận đủ duration, codec, audio và file phát được.

## Quy tắc dựng hình
- MC mở đầu: tiêu đề chính xuất hiện sau 1-2 giây, tránh che mặt/ngực MC.
- B-roll: banner theo đúng cảnh, mỗi banner thường 5-10 giây.
- Không để 2-3 banner lớn cùng lúc.
- Không che gương mặt, bục phát biểu, màn hình hội nghị, chữ trên phông sân khấu.
- Facebook/Zalo mặc định **nhỏ gọn**, đặt sát mép dưới hoặc góc, khoảng 4-8% chiều rộng khung hình; không dùng cụm social lớn.
- ATT NEWS bug nhỏ ở góc, không chiếm vùng nội dung.
- Tiêu đề và tên người/đơn vị quan trọng ưu tiên rõ, ngắn, tương phản cao.
- Hiệu ứng kiểu CapCut phải tiết chế: bản tin chính thống, không TikTok hóa nội dung hành chính.

## Quy tắc banner theo ngữ cảnh
Từ transcript/kịch bản, tự đề xuất 3-6 banner ngắn. Ví dụ chủ đề chuyển đổi số:
- AN THẠNH THỦY ĐẨY MẠNH “BÌNH DÂN HỌC VỤ SỐ”
- TRANG BỊ KIẾN THỨC, KỸ NĂNG SỐ
- HƯỚNG DẪN SỬ DỤNG CÁC TIỆN ÍCH SỐ
- THỰC HIỆN GIAO DỊCH TRỰC TUYẾN
- NÂNG CAO Ý THỨC AN TOÀN TRÊN KHÔNG GIAN MẠNG
- LAN TỎA PHONG TRÀO “BÌNH DÂN HỌC VỤ SỐ”

Không thêm số liệu, quy định hoặc kết luận chưa có trong nguồn.

## Thư viện hiệu ứng
Skill có 6 nhóm công thức FFmpeg chạy được ngay:
1. Transitions
2. Text
3. Filters
4. Effects
5. Stickers
6. Adjustment

Luôn đọc `references/ffmpeg-recipes.md` trước khi dựng.

## Lỗi thực tế phải tránh
- Render video dài trong một tiến trình có thể timeout. Nếu thời lượng >60 giây hoặc filter graph nặng: chia 3-4 segment, render riêng rồi concat.
- File render dở vẫn có thể tồn tại nhưng duration ngắn. Luôn ffprobe duration sau render.
- File quá lớn có thể không phát được trong trình duyệt/ChatGPT. Tạo bản giao H.264 + AAC, `yuv420p`, `+faststart`, bitrate/CRF hợp lý.
- Không dùng `-c copy` sau khi thêm filter/effect.
- Stabilization có thể crop/warp mạnh; chỉ dùng khi thật sự cần và kiểm tra preview.

## Chuẩn xuất mặc định
```bash
ffmpeg -y -i INPUT.mp4 \
  -c:v libx264 -preset veryfast -crf 23 \
  -pix_fmt yuv420p \
  -c:a aac -b:a 128k \
  -movflags +faststart OUTPUT.mp4
```

Mặc định ưu tiên 1920x1080 nếu nguồn đủ chất lượng; nếu cần file nhẹ/ổn định để tải, xuất thêm 1280x720.

## Quy tắc giao file
Không nói "xong" trước khi kiểm tra:
```bash
ffprobe -v error -show_entries format=duration,size \
  -show_entries stream=codec_name,width,height,pix_fmt \
  -of default=nw=1 OUTPUT.mp4
```
Phải có video H.264, audio AAC nếu nguồn có tiếng, pix_fmt yuv420p, duration xấp xỉ nguồn và dung lượng hợp lý.
