---
description: Kiểm tra chất lượng một file video đã render — ffprobe đầy đủ + xem khung hình
argument-hint: <đường dẫn video đã render> [--source <video gốc>]
---

Kiểm tra: **$ARGUMENTS**

Gọi agent `video-reviewer`. Nó chạy:

```bash
python scripts/video_qa.py <output> --strict --audio [--source <input>] [--cut-authorized]
```

rồi trích khung hình ở các mốc có chữ/đồ họa và **thực sự xem ảnh** để bắt lỗi chữ che mặt, phụ đề ngoài safe area, hình méo/vỡ/cắt cụt.

Báo cáo:

```text
FILE:          <đường dẫn>, <dung lượng>
DURATION:      <giây>
RESOLUTION:    <w>x<h> @ <fps>
VIDEO STREAM:  <codec> / <pix_fmt> / faststart <có|không>
AUDIO STREAM:  <codec> <sample rate> <channels> / mean_volume <dB>
LỆCH NGUỒN:    <±giây> (hoặc: không đối chiếu)

VIDEO QA (kỹ thuật): PASS | WARN | FAIL
VIDEO QA (hình ảnh): PASS | FAIL | NOT RUN
```

Mỗi mục `FAIL`/`WARN` phải kèm: sai ở đâu, hậu quả gì (video không mở được trên máy nào, chữ che gì), và lệnh ffmpeg đề xuất để sửa.

Không tự sửa video ở command này — chỉ chẩn đoán. Muốn sửa thì chạy `/edit-video`.
