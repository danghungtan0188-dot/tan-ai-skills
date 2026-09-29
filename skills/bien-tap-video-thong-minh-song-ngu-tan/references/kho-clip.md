# Tìm clip trong kho của người dùng

Khi người dùng nói “tìm trong kho”, “các clip tôi vừa đưa vào kho” hoặc không cung cấp đường dẫn,
ba vị trí được phép tìm mặc định là **Desktop**, **Documents** và **Google Drive**. Quyền này chỉ
áp dụng cho việc tìm video phục vụ yêu cầu dựng hiện tại; không mở rộng sang dữ liệu khác.

## Thứ tự tìm

1. **Desktop** — thư mục Desktop của tài khoản hiện tại và các thư mục con.
2. **Documents** — thư mục Documents của tài khoản hiện tại và các thư mục con.
3. **Google Drive**:
   - ưu tiên thư mục Google Drive/My Drive đã đồng bộ trên máy nếu có;
   - nếu không có bản đồng bộ, dùng kết nối Google Drive để tìm theo tên, loại video, thư mục,
     chủ đề và ngày sửa gần yêu cầu;
   - chỉ tải các video đã xác định là đầu vào về thư mục `work/ingest/<ten-cong-viec>/` rồi mới
     chạy `survey_rushes.py`; không tải cả Drive và không thay đổi file gốc trên Drive.

## Cách thu hẹp đúng video

- Dùng tên sự kiện/chủ đề, ngày quay, tên thư mục và khoảng thời gian người dùng vừa tải lên.
- Ưu tiên video mới sửa gần nhất khi người dùng nói “vừa đưa vào”.
- Chấp nhận: MP4, MOV, MTS, M4V, AVI, MKV, MPG, MPEG, WMV.
- Bỏ qua thư mục đầu ra/cache và video đã dựng: `.git`, `node_modules`, `outputs`, `output`,
  `render`, `renders`, `edit`, `thumbs`, `cache`, `__pycache__`.
- Không suy đoán chỉ từ tên file. Sau khi tập hợp ứng viên, vẫn phải chạy khảo sát và xem hết
  contact sheet để biết nội dung thật.

## Khi có trùng hoặc nhiều nhóm không liên quan

- Nếu chỉ một nhóm khớp rõ chủ đề/ngày: dùng nhóm đó và tiếp tục tự động.
- Nếu nhiều nhóm đều hợp lý nhưng dẫn đến video khác nhau: nêu ngắn gọn các thư mục/nhóm ứng viên
  và hỏi người dùng chọn; không trộn sự kiện khác nhau vào một video.
- Không quét ngoài Desktop, Documents và Google Drive nếu người dùng chưa chỉ định vị trí khác.

## Công cụ tìm

Đừng gõ lệnh tìm bằng tay mỗi lần — dùng `find_clips.py` để việc tìm lặp lại được và không sót:

```bash
python scripts/find_clips.py --tu 2026-09-20 --ten "suc khoe" --out edit/ung-vien.json
```

- Không có `--kho` thì tự tìm ở Desktop, Documents và thư mục Google Drive đã đồng bộ.
- `--ten` so khớp **bỏ dấu**, khớp cả tên file lẫn tên thư mục cha.
- Tự bỏ `outputs`, `render`, `edit`, `thumbs`, `cache`, `.git`, `node_modules` và file nhỏ hơn
  `--min-mb` (mặc định 2 MB — thường là clip lỡ tay).

Máy chỉ lọc theo **tên và ngày**. Có danh sách rồi vẫn phải khảo sát và xem contact sheet;
không bao giờ kết luận nội dung từ tên file.

## Sau khi tìm xong

Đưa tất cả clip đã chọn vào cùng một phạm vi khảo sát (thư mục gốc hoặc `work/ingest/...`), rồi chạy:

```bash
python scripts/survey_rushes.py "KHO_DA_CHON" --recursive \
  --out edit/rushes.json --sheet edit/contact.jpg
```

Tiếp tục theo [dung-tu-video-tho.md](dung-tu-video-tho.md): xem contact sheet → chọn cảnh có lý do →
lập plan đúng thời lượng → ghép → hoàn thiện ATT NEWS → QA.
