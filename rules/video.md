# Rule video

Áp dụng cho `video-analyzer`, `video-editor`, `video-reviewer` và toàn bộ skill video trong `skills/`.

## 0. QUY TẮC TỐI QUAN TRỌNG: KHÔNG LẶP CẢNH

- Trong một video, **mỗi cảnh (ảnh, đoạn clip, thẻ đồ họa) chỉ xuất hiện một lần**. Cùng một ảnh với kiểu zoom/trượt khác vẫn là lặp.
- Không đủ input → **tìm ảnh thích hợp trên mạng** (giấy phép mở, ghi nguồn) **hoặc làm đồ họa 2D/3D**. Không lặp cảnh cũ, không nhét ảnh không đúng nội dung để lấp chỗ.
- Trước khi dựng: bảng phân cảnh phải qua bước kiểm lặp. Dựng xong: **bắt buộc** chạy
  `python skills/bien-tap-video-thong-minh-song-ngu-tan/scripts/kiem_lap_canh.py <video> --bo 0:<hết intro đài>`.
  Còn dòng `LAP` → **chưa được giao**, kể cả khi mọi kiểm khác đã PASS.

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

## 2b. Tự chấm từng cảnh ≥ 9/10 rồi mới render bản cuối

Người dùng đặt (23/11/2026): dựng xong phải **tự soát kỹ từng cảnh**, cảnh nào trượt bất kỳ tiêu chí nào thì làm lại;
**chỉ render bản cuối khi tự chấm ≥ 9/10**. Lý do: bản tin 13/11 phải sửa v6 → v10 vì lỗi người dùng tự phát hiện
(đọc sai "Tham dự", số 40/80, nhạc nghe như không đổi, chữ tràn khung) — người dùng không phải người soát lỗi.

1. Soát trên **bản nháp nhẹ**, chưa render bản cuối: ảnh lưới khung hình từng cảnh, khung 1080p cắt sát chỗ có chữ,
   nghe từng câu giọng đọc.
2. Chấm **từng cảnh** theo 5 nhóm, ghi điểm và lý do:

   | Nhóm | Đạt khi |
   |---|---|
   | Nội dung | tên, chức danh, con số, ngày đúng nguyên văn tư liệu; không bịa — **sai tên/số = cảnh đó 0 điểm** |
   | Hình | không lặp cảnh (mục 0); không rung/tối/mờ; không che mặt; chữ Việt đủ dấu, không tràn khung, không chữ lẻ dòng |
   | Giọng | đọc đúng tên, "tr", "Ủy" (`scripts/kiem_ten_tts.py`, nghe 3 lần); đầu câu không mất âm; khớp hình |
   | Âm thanh | nhạc nghe ra được nhưng dưới giọng (≈ −29 LUFS dưới giọng −16); không rè; không bóp dải động (mục 5) |
   | Nhịp, phong cách | đúng `skills/bien-tap-video-thong-minh-song-ngu-tan/references/phong-cach-att-news.md` (với bản tin); chuyển cảnh mượt; đúng thời lượng |

3. Cảnh dưới chuẩn → sửa → soát lại **chính cảnh đó**. Lặp tới khi tổng ≥ 9/10 và **không cảnh nào trượt nhóm Nội dung**.
4. Render bản cuối, chạy `video_qa.py --strict --audio` (mục 2), giao kèm **bảng điểm từng cảnh** cho người dùng.

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
- Nhạc nền, hiệu ứng âm thanh không phải tự làm: ghi vào `nguon-am-thanh.md` cạnh video giao — mỗi file một dòng: tên file, nguồn (link), tác giả, giấy phép, có phải ghi tên tác giả không. Không rõ giấy phép thì không dùng. Bị khiếu nại bản quyền trên Facebook/TikTok thì file này là bằng chứng.

## 6. Nội dung

- Không bịa tên người, chức vụ, địa điểm, số liệu xuất hiện trong video. Chưa xác nhận thì để trống và hỏi.
- Không dùng nhạc/hình có bản quyền của người khác khi chưa có quyền.
- Không xóa watermark của người khác, không sao chép tài nguyên độc quyền.

## 7. Giữ file gốc

Không ghi đè file nguồn. Xuất ra tên/thư mục mới. Ghi đè file gốc là thao tác không đảo ngược → phải hỏi người dùng.
