---
name: video-marketing
description: Hiệu ứng video marketing kiểu người nói 9:16 (TikTok, Reels, Facebook) — đặt hiệu ứng ĐÚNG LÚC người nói một câu, nằm SAU người (tách nền) và KHÔNG đè mặt. Nền móng có sẵn — tim_cau_noi (câu nói → giây), tach_nguoi (tách người đúng đoạn + vùng mặt), ghep_lop (nền → hiệu ứng → người). Kích hoạt khi người dùng muốn thêm hiệu ứng "lúc mình nói …", đặt biểu đồ / carousel ảnh / checklist / sơ đồ nhánh / tường tiêu đề / nét vẽ tay phía sau người, hoặc làm video quảng bá dịch vụ, sản phẩm. Không dùng cho bản tin ATT NEWS hay phim tài liệu (phong cách nghiêm túc — xem bien-tap-video-thong-minh-song-ngu-tan).
---

# Video marketing: hiệu ứng theo câu nói, sau người

## Quy trình một hiệu ứng

```text
1. tim_cau_noi.py  video + "câu nói"         → giây bắt đầu / kết thúc (khớp < 60% thì DỪNG, hỏi lại câu)
2. dựng hiệu ứng    HyperFrames + GSAP        → video TRONG SUỐT (.webm VP9 alpha / .mov ProRes 4444) đủ khung,
                                                 chữ/số chính đặt trên `tren_dau` của bước 3
3. tach_nguoi.py   video --tu --den           → người trong suốt + .mat.json (hop_mat, tren_dau)
4. ghep_lop.py     video --hieu-ung --nguoi   → MP4: nền → hiệu ứng → người, chỉ trong [tu, den]
5. QA              video_qa.py --strict --audio + xem khung giữa cửa sổ: hiệu ứng có, mặt không bị che
6. Cả video xong   /review-video                → thêm phần giám khảo 6 câu: 2–3 giây đầu có giữ người xem không,
                                                 cảnh kết có lời kêu gọi rõ không, tối đa 3 việc nên sửa trước
```

Chạy từ thư mục skill (`scripts/`). Mỗi lần chỉ tách MỘT đoạn ngắn — máy hay sập khi chạy nặng.

```bash
python scripts/tim_cau_noi.py video.mp4 "điện thoại, máy tính bảng hay là máy tính" -o edit/moc.json
python scripts/tach_nguoi.py video.mp4 --tu 22.4 --den 28.1 -o edit/nguoi-01.webm
python scripts/ghep_lop.py video.mp4 --hieu-ung edit/hu-01.webm --nguoi edit/nguoi-01.webm --tu 22.4 --den 28.1 -o edit/ra-01.mp4
```

Hiệu ứng được phép đè lên người (không cần sau người) → bỏ `--nguoi`, khỏi tách nền.

## Viết câu lệnh hiệu ứng (khuôn)

> Thêm hiệu ứng **[tên]** lúc mình nói "**[câu nói]**". Nội dung: [số liệu / danh sách / thư mục ảnh].
> Đặt **[trên đầu / sau người / giữa khung]**, **không đè mặt**. Màu [..], chữ to. [Mục nào sáng lên lúc nói "[từ]".]

Câu nói là **neo thời gian** (không ghi giây tay). Mỗi mốc phụ ("sáng lên lúc nói …") cũng tìm bằng `tim_cau_noi.py -c`.

## Hiệu ứng dự kiến (chưa có mẫu — làm từng cái, mỗi cái có bài thi)

| Hiệu ứng | Dùng khi | Trạng thái |
|---|---|---|
| Bar Chart Race, Minimal Line Graph | số liệu tăng trưởng, so sánh | chưa có mẫu |
| Checklist, Constellation Hub | các bước, các ý chính | chưa có mẫu |
| Orbit / Vision Carousel | khoe bộ ảnh sản phẩm, khách hàng | chưa có mẫu |
| Multi Device Splay, Exploded Stack | giới thiệu web/app, sản phẩm | chưa có mẫu |
| Headline Wall, Doodle Boil | tin xu hướng, vlog kể chuyện | chưa có mẫu |

Trước khi tự viết: tra kho HyperFrames bằng tiếng Anh — `npx hyperframes catalog --query "<mô tả chuyển động>"`
(skill `hyperframes-registry`). Chuyển động dùng `gsap-timeline` / `gsap-plugins`.

## Video quảng cáo mở bằng nỗi đau

Khung 5 nhịp (nỗi đau → kết quả thật → lợi ích → dễ dùng → mời dùng thử), kèm cách làm video vị trí nhà đất: [quang-cao-noi-dau.md](references/quang-cao-noi-dau.md).

## Nhịp dựng

Punch-in, hình chèn, mức âm thanh và cách cắt lời lặp: [nhip-dung-nguoi-noi.md](references/nhip-dung-nguoi-noi.md).

## Không được

- Không lấy hiệu ứng từ gói trả phí của người khác; chỉ dùng khối nguồn mở (HyperFrames, GSAP) hoặc tự viết.
- Không ghi đè video gốc; không tách nền cả video dài.
- Không báo xong khi chưa xem khung giữa cửa sổ hiệu ứng.
