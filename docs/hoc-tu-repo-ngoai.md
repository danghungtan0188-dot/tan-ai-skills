# Học từ repo ngoài

Repo đã xem (10–11/2026) và việc học được. Cập nhật cột "Trạng thái" khi làm xong. Đã đọc README và vài file; repo nào chưa chạy thử thì ghi rõ.

## Đã làm

| Học gì | Từ repo | Thành |
|---|---|---|
| Tìm cảnh minh hoạ theo từ khoá (Pexels/Pixabay) | harry0703/MoneyPrinterTurbo (MIT) | `python -m tan_studio tim-canh` |
| Chuyển cảnh + vệt sáng chính hãng | remotion-dev/remotion | mẫu `GhepCanh` trong `do-hoa/` |
| Vòng HUD đếm số, công thức montage glitch | reel THĐT | mẫu `HudDemSo` + `skills/hieu-ung-video/references/ky-thuat-tu-video-mau.md` |
| Giám khảo chấm độ hay của video (6 câu có mốc giây) | sarpstar/cinecode (MIT) | bước 3 của agent `video-reviewer`, `/review-video` (PR #23) |
| Ghi nguồn nhạc / hiệu ứng âm thanh | Vincentwei1021/video-shotcraft (Apache-2.0) | `rules/video.md` mục 5: `nguon-am-thanh.md` cạnh video giao |
| Nhãn khi thiếu thông tin, tách "cần xác nhận" / "giả định" | coreyhaines31/marketingskills (MIT) | đã có sẵn trong `kich-ban-video-marketing` (`[CẦN XÁC NHẬN: ...]`) |

## Còn lại

| # | Học gì | Từ repo | Áp vào | Ghi chú |
|---|---|---|---|---|
| 1 | Tắt plugin không dùng | aicodeking/leanrea (đo: nạp đủ công cụ REA tốn ~400k token chỉ để trả lời "OK") | ứng dụng Claude: 22 plugin đồng bộ, 298 skill, 177 MCP | người dùng tự tắt trong ứng dụng |
| 2 | Tài liệu thư viện mới nhất + skill Next.js | upstash/context7 (MIT), vercel-labs/agent-skills (không có file giấy phép: chỉ cài, không chép) | dự án English Kids | cần người dùng đồng ý cài |
| 3 | Viết mô tả skill gọn: từ khoá đầu câu, mỗi tình huống một từ kích hoạt, chỉ đường sang skill liên quan | mattpocock/skills `writing-for-agents` (MIT) | ~33 skill của repo | |
| 4 | Trang xem trước các mẫu đồ hoạ | video-shotcraft (gallery 150 cảnh) | 36 mẫu `do-hoa/` | render từng mẫu một, máy hay nóng |
| 5 | Đo có skill / không skill, mỗi bài 3 lần, chấm theo đáp án | leanrea `bench/` | skill tự viết, bằng `scripts/harness_eval.py` | |
| 6 | Prompt "senior lười": viết ít, không bỏ kiểm đầu vào / bảo mật / test | DietrichGebert/ponytail (MIT) | `senior-dev-harness` | số liệu là tác giả tự đo: đo lại bằng `evals/thu_that.py` trước khi dùng |
| 7 | Chỉ dựng lại cảnh bị sửa | MoneyPrinterTurbo | `tan_studio` | |
| 8 | Chạy hàng loạt theo file danh sách (JSONL) | MoneyPrinterTurbo | `tan_studio` | khi làm nhiều video cùng khuôn |

## Để dành

| Học gì | Từ repo | Khi nào |
|---|---|---|
| Skill bảo mật | trailofbits/skills (CC-BY-SA: cài plugin, không chép) | app có thanh toán / dữ liệu cá nhân |
| Skill Supabase, Flutter, Cloudflare | supabase/agent-skills, flutter/agent-plugins, cloudflare/skills | quay lại website / AgriPocket |
| `customer-research`, `pricing`, `launch` | marketingskills | bắt đầu bán dịch vụ dựng video |
| Phần 13–14 (MCP, agent) | rohitg00/ai-engineering-from-scratch (MIT) | muốn hiểu sâu cách xây agent |
| Thẻ cảnh quảng bá sản phẩm, xuất JianYing | video-shotcraft | video giới thiệu website / app (phần dùng `OffthreadVideo` bị Windows chặn trên máy này) |
| Thay REA bằng một file skill | leanrea | chỉ khi phân tích ngược app |

## Không lấy

mattpocock/skills phần lập trình (harness đã có `interview-me`, `handoff`, TDD), affaan-m/ECC (harness cùng loại, cài vào giẫm chân), thedotmack/claude-mem (trùng bộ nhớ + `PROGRESS.md`, mặc định gửi thống kê), OpenSpec / BMAD / get-shit-done (nặng, harness có `spec-driven-development`), cinecode cả bộ (mới một tuần, trùng HyperFrames).

Danh sách 356 repo đã quét: `D:\GitHub\quet-github-vibe-coding-2026-11-08.csv`.
