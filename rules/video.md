# Rule video

Áp dụng cho `video-analyzer`, `video-editor`, `video-reviewer` và toàn bộ skill video trong `skills/`.

## 1. Chuẩn đầu ra mặc định

Trừ khi người dùng yêu cầu khác:

```text
Container:      MP4
Video codec:    H.264 (libx264)
Audio codec:    AAC
Pixel format:   yuv420p
Faststart:      bật (-movflags +faststart)
Kích thước:     chiều rộng và cao đều là số chẵn
```

Lệnh nền tham khảo:

```bash
ffmpeg -i input.mp4 -c:v libx264 -pix_fmt yuv420p -c:a aac -movflags +faststart output.mp4
```

## 2. Render xong ≠ xong

FFmpeg exit code 0 **không** phải bằng chứng video đúng. Bắt buộc chạy:

```bash
python scripts/video_qa.py output.mp4 --strict --audio
```

Kiểm: file tồn tại, dung lượng hợp lý, thời lượng > 0, có luồng hình, có luồng tiếng, codec/pix_fmt đúng, faststart, track tiếng không im lặng.

Hook `.claude/hooks/check_render.py` tự chạy bản nhanh sau mỗi lệnh `ffmpeg` và chặn nếu file hỏng nặng. Bản `--strict` vẫn phải chạy thủ công ở bước review cuối.

## 3. Không cắt khi chưa được phép

Không tự cắt bỏ đoạn, không tự đổi thời lượng tổng nếu người dùng chưa đồng ý. Đối chiếu:

```bash
python scripts/video_qa.py output.mp4 --source input.mp4
```

Lệch quá 0.1 giây mà chưa được phép cắt = FAIL. Khi đã được phép, thêm `--cut-authorized`.

## 4. Chữ và đồ họa

- **Không che mặt người**, không che nhân vật chính, không che chữ/logo quan trọng của khung hình gốc.
- Lower-third: đặt ở 1/4 dưới, cách mép an toàn, hiện 3–5 giây, có fade vào/ra.

  ```text
  HỌ VÀ TÊN          ← đậm, lớn
  Chức vụ / đơn vị   ← nhỏ hơn, nhạt hơn
  ```

- Phụ đề: nằm trong safe area (cách mép dưới ≥ 8% chiều cao), tối đa 2 dòng, mỗi dòng ≤ 42 ký tự, ngắt dòng theo cụm nghĩa. Đủ tương phản để đọc trên điện thoại (có viền/nền mờ).
- Phụ đề phải khớp giọng đọc. Không tự viết phụ đề từ suy đoán nội dung — phải có transcript thật.

## 5. Âm thanh

- Không được mất tiếng. Nếu video gốc có tiếng, video ra phải có tiếng.
- Nhạc nền phải ducking xuống dưới giọng đọc, không đè lời.
- Chuẩn hóa mức âm trước khi giao.

## 6. Nội dung

- Không bịa tên người, chức vụ, địa điểm, số liệu xuất hiện trong video. Chưa xác nhận thì để trống và hỏi.
- Không dùng nhạc/hình có bản quyền của người khác khi chưa có quyền.
- Không xóa watermark của người khác, không sao chép tài nguyên độc quyền.

## 7. Giữ file gốc

Không ghi đè file nguồn. Xuất ra tên/thư mục mới. Ghi đè file gốc là thao tác không đảo ngược → phải hỏi người dùng.
