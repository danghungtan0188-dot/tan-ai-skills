---
description: Rút kinh nghiệm sau khi giao một video — trả lời bốn câu hỏi, ghi nhật ký, biến bài học thành test hoặc luật trong script
argument-hint: [tên video vừa làm]
---

Video vừa giao: **$ARGUMENTS**

Chạy **ngay sau khi giao video**, trước khi đóng phiên. Quy trình đầy đủ:
[skills/bien-tap-video-thong-minh-song-ngu-tan/references/rut-kinh-nghiem.md](skills/bien-tap-video-thong-minh-song-ngu-tan/references/rut-kinh-nghiem.md)

**1. Trả lời bốn câu, kèm số đo thật — không viết "vừa phải", "khá hơn".**

1. Chỗ nào phải làm lại từ hai lần trở lên?
2. Tham số nào lần này chốt được? (toạ độ, cỡ chữ, LUFS, ngưỡng, thời lượng)
3. Lỗi nào máy đáng lẽ bắt được mà không bắt? ← loại quý nhất
4. Cái gì hay, nên giữ làm mặc định?

**2. Tạo chỗ neo cho từng bài học.** Chưa neo được thì chưa tính là đã lưu:

| Dạng | Khi nào | Làm gì |
|---|---|---|
| `test:` | máy đáng lẽ bắt được | thêm class test trong `tests/` |
| `script:` | thành mặc định hoặc luật chặn | sửa script trong `skills/.../scripts/` |
| `doc:` | thông số đã chốt, quy ước | thêm dòng vào `references/` |

Sở thích riêng của người dùng (không thuộc kỹ thuật dựng) → lưu vào memory, không nhét vào nhật ký.

**3. Ghi nhật ký.** Thêm dòng ở **cuối bảng**
[references/nhat-ky-ban-tin.md](skills/bien-tap-video-thong-minh-song-ngu-tan/references/nhat-ky-ban-tin.md).
Không sửa dòng cũ; luật cũ sai thì thêm dòng mới ghi "thay cho …".

**4. Kiểm và đồng bộ.**

```bash
python -m unittest discover -s tests
python scripts/sync_skills.py --force
```

`tests/test_kinh_nghiem.py` sẽ đỏ nếu khai chỗ neo không có thật.

**5. Commit riêng** một commit cho phần rút kinh nghiệm, để sau này lần lại được video nào sinh ra luật nào.

Báo cáo:

```text
BÀI HỌC:     <số dòng thêm vào nhật ký>
ĐÃ NEO:      test:<…> script:<…> doc:<…>
TEST:        <số> PASS
ĐỒNG BỘ:     <n>/<n>
```

Không ghi bài học chưa kiểm chứng. Không biến thứ phụ thuộc từng video thành luật cứng.
