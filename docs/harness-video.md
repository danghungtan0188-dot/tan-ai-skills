# Harness dựng video — kiến trúc đích và bản đồ thành phần

Mục tiêu: người dùng đưa **tư liệu + vài gợi ý bằng lời** → repo tự hiểu, tự dựng, tự kiểm, tự sửa →
chỉ dừng ở **2 cổng duyệt** → giao video → rút kinh nghiệm có duyệt. Bán tự động, khép kín.

Kiến trúc đích lấy theo tài liệu "AI Video Editing Harness" (8 giai đoạn) người dùng gửi ngày 01/11/2026.
Tài liệu đó tự ghi: *không cần ép repo giống hoàn toàn — đây là kiến trúc đích để đối chiếu và nâng cấp từng phần.*

## 1. Vòng bán tự động

```text
 TƯ LIỆU + GỢI Ý
      │
 1. Hiểu yêu cầu ── gợi ý → bản yêu cầu (loại video, độ dài, tỉ lệ, phong cách, phải có / cấm)
 2. Phân tích ───── probe từng file, xem ảnh, nghe lời → VideoAnalysis
 3. Kế hoạch ────── chọn skill + cảnh + chữ + chuyển cảnh + âm thanh → EditPlan
      │
 ■ CỔNG DUYỆT 1 ── người dùng xem bảng kế hoạch: đồng ý / sửa gợi ý
      │
 4. Dựng ────────── cắt ghép → màu → đồ hoạ → âm thanh → phụ đề → render
 5. Kiểm tự động ── video_qa --strict --audio + xem khung hình → PASS / FAIL
      │  FAIL → tự sửa → dựng lại → kiểm lại (tối đa 3 vòng, rồi báo người dùng)
 ■ CỔNG DUYỆT 2 ── người dùng xem video: chấp nhận / góp ý (góp ý → quay lại 3)
      │
 6. Giao + rút kinh nghiệm ── /rut-kinh-nghiem → bài học ĐỀ XUẤT → người dùng duyệt → test/luật
```

Máy tự làm mọi bước **đo và kiểm**. Người giữ 2 việc **quyết**: kế hoạch có đúng ý không, video có đạt không.

## 2. Bản đồ: kiến trúc đích ↔ thành phần thật

| Kiến trúc đích | Thành phần đang có | Tình trạng |
|---|---|---|
| Hướng dẫn repo, luật | `CLAUDE.md`, `rules/video.md`, `rules/global.md` | có |
| Hợp đồng dữ liệu (schemas) | `data-contracts/video.schema.json` (VideoInput, VideoAnalysis, EditPlan, RenderResult, VideoQAReport), `data-contracts/studio.schema.json` | có |
| Editing Manifest | `EditPlan` trong `data-contracts/video.schema.json`; hồ sơ chạy run.json của `tan_studio/workflow.py` | có, chưa thống nhất hai dạng |
| Điều phối (orchestrator) | `.claude/agents/orchestrator.md` → `.claude/agents/video-analyzer.md` → `.claude/agents/video-editor.md` → `.claude/agents/video-reviewer.md` | có |
| Chọn skill (routing) | bảng "Chọn skill thực thi" trong `.claude/agents/video-editor.md`; bảng trong `.claude/commands/edit-video.md` | có, **hai bảng** — xem `docs/kiem-ke-skill.md` đề xuất 4 |
| Workflow theo loại | `.claude/commands/dung-tu-kho.md` (kho clip → bản tin), `.claude/commands/video-news.md` (bản tin), `.claude/commands/edit-video.md` (tự do), `tan_studio/workflow.py` (kịch bản → video) | có, **ba cửa vào** |
| Skills | `skills/` (32 skill) — kiểm kê ở `docs/kiem-ke-skill.md` | có, còn chồng chéo |
| Engines | `tan_studio/` (ffmpeg, TTS, phụ đề), `do-hoa/` (Remotion), `remotion-studio/`, HyperFrames (ngoài repo) | có |
| Thư viện hiệu ứng, mẫu | `skills/hieu-ung-video/`, `do-hoa/src/mau/`; ngoài repo: HyperFrames + 8 skill GSAP (chuyển động), danh sách ở `scripts/skills-ngoai.json`; thư viện tham khảo editonny ở ổ D, xem `skills/motion-graphics-tan/references/canh-theo-muc-dich.md` | có |
| Phong cách motion graphics | `skills/motion-graphics-tan/` — 20 phong cách có thẻ mẫu đã render, font tiếng Việt đi kèm, xuất trong suốt được; chưa ghép lên video thật | có |
| Hiệu ứng marketing (người nói 9:16) | `skills/video-marketing/` — neo theo câu nói, tách người đúng đoạn, ghép nền → hiệu ứng → người; 10 hiệu ứng chưa có mẫu | nền móng có (01/11) |
| Phong cách đã chốt | `skills/bien-tap-video-thong-minh-song-ngu-tan/references/phong-cach-att-news.md` | có (ATT NEWS); loại khác chưa |
| Trạng thái, chạy lại | run.json ghi sau mỗi bước + `python -m tan_studio chay-lai` | có, chỉ trong `tan_studio` |
| Kiểm định kỹ thuật | `scripts/video_qa.py`, `.claude/hooks/check_render.py`, `tan_studio/nghiem_thu.py`, `scripts/kiem_diem_cat.py` (điểm cắt theo sóng âm), `scripts/kiem_phu_de_ocr.py` (đọc lại phụ đề, cần Tesseract tiếng Việt; chưa chạy thật) | có |
| Chốt chặn | `.claude/hooks/` (8 hook), `docs/bai-hoc-va-chot-chan.md` | có |
| Thử hệ thống với AI thật | `scripts/harness_eval.py` | có |
| Bài thi chuẩn, hồi quy chất lượng video | `evaluations/bai_thi.py` (đầu vào tự sinh → `tan_studio` → phiếu điểm 10 tiêu chí), mốc `evaluations/moc-chuan.json` | có (01/11) — mới phủ đường "kịch bản → video" |
| Quan sát: nhật ký hook / skill / agent / lệnh | `observability/nhat_ky.py` (mọi hook ghi khi chặn/hỏi/nhắc), `.claude/hooks/ghi_su_dung.py`, xem bằng `observability/xem.py`; dữ liệu ở ~/.tan-harness/nhat-ky/ (ngoài repo) | có (01/11) — render đã có hồ sơ riêng (run.json, phiếu điểm) |
| Bộ nhớ, bài học | `skills/bien-tap-video-thong-minh-song-ngu-tan/references/nhat-ky-ban-tin.md`, memory của Claude | có |
| Tự cải tiến có duyệt | `.claude/commands/rut-kinh-nghiem.md`, `tan_studio/rules.py` (đề xuất → duyệt → áp dụng, có phiên bản, hoàn tác) | có |
| Một cửa vào bán tự động | `.claude/commands/dung-video.md`: gợi ý → bản yêu cầu `VideoBrief` (kiểm bằng `scripts/kiem_brief.py`) → định tuyến sang 4 cửa vào đang có → 2 cổng duyệt → `/rut-kinh-nghiem` | có (01/11) |

## 3. Lộ trình (mỗi bước người dùng duyệt rồi mới làm bước sau)

| Bước | Việc | Kiểm bằng |
|---|---|---|
| 1 ✓ | Tài liệu này + test đường dẫn | `tests/test_harness_video_doc.py` |
| 2 ✓ | Bài thi chuẩn `evaluations/bai_thi.py`: đầu vào tự sinh → phiếu điểm → so mốc chuẩn | `--hong khung` / `thieu-media` / `chuan-hoa` đều báo HỒI QUY; `tests/test_bai_thi.py` |
| 3 ✓ | Nhật ký `observability/`: hook chặn/hỏi/nhắc + skill/agent/lệnh được dùng; không ghi nội dung lệnh | `tests/test_nhat_ky.py`; phiên Haiku thật để lại dòng nhật ký đúng |
| 4 ✓ | Lệnh `/dung-video`: gợi ý → `VideoBrief` → định tuyến → 2 cổng duyệt → `/rut-kinh-nghiem` | ca `dung-video-cong-1` trong `scripts/harness_eval.py` (Haiku thật dừng ở cổng 1, chưa render); `tests/test_kiem_brief.py` |
| 5 | Gọn skill (`docs/kiem-ke-skill.md` đề xuất 2–6) + test chọn skill | test kích hoạt đạt |
| 6 | Phong cách theo loại video (bản tin, tài liệu, mạng xã hội, sự kiện) | bài thi đổi loại → phiếu điểm đúng loại |
| 7 | Thống nhất EditPlan và run.json thành một Editing Manifest | ngắt giữa chừng, chạy lại tiếp được |

## 4. Quyết định kiến trúc

| # | Quyết định | Lý do |
|---|---|---|
| Q1 | **Không dời thư mục** theo sơ đồ đích; thành phần mới đặt đúng tên trong sơ đồ (evaluations/, observability/) | Dời thư mục làm gãy hook, test, `tan_studio`, `~/.claude/settings.json`, junction skill mà video không tốt hơn |
| Q2 | **Hai cổng duyệt là bắt buộc**, không có chế độ tự động 100% | Máy đo được kỹ thuật, không đo được "đúng ý"; `tan_studio` đã tách `status` (kỹ thuật) khỏi `noi_dung` (người đánh giá) |
| Q3 | **AI chỉ đề xuất bài học**, người duyệt mới thành luật | Tránh lỗi tự nhân lên; giống `tan_studio/rules.py` |
| Q4 | Cửa vào mới **gọi lại** 3 lệnh đang có, không viết lại | Giữ thứ đang chạy; mỗi lệnh đã có QA 3 vòng |
| Q7 | Skill do công cụ khác quản (HyperFrames, GSAP, Playwright CLI) **không chép vào repo**; repo giữ danh sách + script kiểm/cài lại (`scripts/cai_skill_ngoai.py`) | Chép vào = hai bản lệch nhau; danh sách giúp máy mới dựng lại đủ bộ bằng một lệnh |
| Q6 | Nhật ký **ngoài repo** và **chỉ ghi nhãn**, không ghi nội dung lệnh | Repo công khai; lệnh có thể chứa secret hoặc đường dẫn riêng tư (luật "không ghi dữ liệu nhạy cảm vào log") |
| Q5 | Đầu vào bài thi **tự sinh bằng code** | Repo công khai: không bản quyền, không ảnh cá nhân, file nhỏ, máy không nóng |
