# Kiểm kê 29 skill (01/11/2026)

Chỉ đọc, chưa sửa gì. Mỗi đề xuất ở cuối cần người dùng duyệt từng mục.

**Cách đo:** đọc frontmatter `skills/*/SKILL.md`; đếm commit bằng `git rev-list --count HEAD -- skills/<ten>`;
"được gọi từ" = tên skill xuất hiện trong `.claude/commands`, `.claude/agents`, `rules/`, `CLAUDE.md`.
Số commit chỉ là **dấu hiệu gián tiếp** của việc dùng thật — repo chưa ghi lại lần nào skill được kích hoạt.

## Tổng quan

| Nhóm | Số skill | Ghi chú |
|---|---|---|
| Skill của anh — video | 10 | Chồng chéo nhiều nhất |
| Skill của anh — khác | 3 | `phat-trien-app`, `xay-ai-agent`, `marketing` |
| Bản chép từ nơi khác (upstream) | 16 | 11 `remotion-*`, 3 `heygen-*`, `video-use`, `humanizer` |
| **Cộng** | **29** | |

## 1. Skill video của anh (10)

| Skill | Làm gì | Commit / lần cuối | Ai gọi | Nhận xét |
|---|---|---|---|---|
| `bien-tap-video-thong-minh-song-ngu-tan` | Kho clip → video; phụ đề Anh–Việt; ATT NEWS | 27 / 29-10 | `video-editor`, `/dung-tu-kho`, `/video-news`, `tan_studio` | **Skill chủ lực** (25 file .py). Giữ |
| `hieu-ung-video` | Công thức từng hiệu ứng (transition, chữ động, filter) | 23 / 25-10 | `video-editor`, `orchestrator` | Dùng nhiều. Giữ |
| `tan-giong-doc-ban-tin` | Giọng đọc VieNeu-TTS | 5 / 03-10 | `video-editor`, `tan_studio` | Lõi của STUDIO. Giữ |
| `chuyen-gia-edit-video-tan` | Dựng bằng code "tương đương CapCut" | 6 / 22-10 | `video-editor` | **Chồng với `hieu-ung-video`** (cả hai đều là bộ hiệu ứng kiểu CapCut) |
| `bien-tap-video` | Router: nhận chủ đề → chọn phong cách | 2 / 22-10 | `video-editor`, `orchestrator` | **Chồng vai router** với bảng chọn skill trong `video-editor` |
| `ban-do-video` | Video bản đồ từ OpenStreetMap | 2 / 22-10 | không command/agent nào | Có test riêng. Chưa được định tuyến |
| `video-thuyet-minh` | Kịch bản → giọng → ghép vào video | 2 / 29-09 | `video-editor` | **Chồng với `tro-ly-video-ban-tin-tan`** |
| `tro-ly-video-ban-tin-tan` | Kịch bản → MP4 bản tin, có HeyGen | 7 / 29-09 | **không ai gọi** | Viết theo cú pháp Codex (`$ten-skill`); gắn với HeyGen trả phí |
| `video-san-pham` | Video sản phẩm từ Excel + ảnh | 1 / 18-08 | `video-editor` | Ít dùng, phạm vi rõ |
| `dung-video-su-kien` | Video sự kiện kiểu Việt Nam | 1 / 18-08 | `video-editor` | Đúc kết từ **một** video mẫu |

## 2. Skill khác của anh (3)

| Skill | Commit / lần cuối | Ai gọi | Nhận xét |
|---|---|---|---|
| `phat-trien-app` | 1 / 18-08 | 5 agent APP, `rules/coding.md` | Nền của nhánh APP. Giữ |
| `xay-ai-agent` | 1 / 25-10 | không ai gọi (chỉ kích hoạt theo mô tả) | Phạm vi rõ. Giữ |
| `marketing` | 3 / 04-08 | không ai gọi | Không đụng từ tháng 8 |

## 3. Bản chép từ nơi khác (16) — vấn đề lớn nhất

| Bộ | Có ở đâu | Vấn đề |
|---|---|---|
| 11 `remotion-*` | `skills/` của repo **và** `~/.claude/skills/` (thư mục thật, không phải liên kết) **và** plugin `remotion:` | 3 bản. `remotion-best-practices` và `remotion-markup` trong repo đã **khác** bản ở `~/.claude/skills` (9 skill còn lại giống hệt) → AI có thể đọc bản cũ |
| 3 `heygen-*` | repo **và** `~/.claude/skills/` | 2 bản |
| `video-use`, `humanizer` | repo | Bản chép, không tự cập nhật khi tác giả sửa |

Ngoài repo, máy còn cài các skill video khác có phạm vi gần giống (chưa đọc nội dung, chỉ thấy tên trong danh sách skill):
`video-editing`, `embedded-captions`, `general-video`, `anthropic-skills:video-editing-toolkit`,
`anthropic-skills:video-narration-workflow`, `anthropic-skills:vietnamese-tts-voice`, `anthropic-skills:voicestudio-dubbing`.
Càng nhiều skill mô tả gần nhau, AI càng dễ chọn nhầm.

## 4. Đề xuất (chờ duyệt từng mục)

| # | Đề xuất | Lợi | Rủi ro |
|---|---|---|---|
| 1 | ✓ **Đã làm 01/11**: 15 skill (11 `remotion-*`, 3 `heygen-*`, `tan-giong-doc-ban-tin`) ở `~/.claude/skills` thành junction về `.claude/skills/` của repo (bản cũ ở `~/.claude/skills_cu_ban_chep_20261101/`); `video-use` giữ bản cài riêng vì có `.venv` 369 MB; `sync_skills.py --check` báo khi bản chép riêng lệch repo. Còn lại: plugin `remotion:` vẫn là bản thứ hai — tắt hay giữ do người dùng quyết. Đề xuất gốc: **Một nguồn cho skill upstream**: xoá bản chép trùng ở `~/.claude/skills/` (giữ bản repo, có sync), hoặc ngược lại bỏ khỏi repo và dùng plugin | Hết lệch phiên bản | Phải soát skill nào đang trỏ tới đường dẫn cũ |
| 2 | **Gộp `tro-ly-video-ban-tin-tan` vào `video-thuyet-minh`**, phần HeyGen thành tuỳ chọn (vẫn qua `guard_tra_phi`) | Bớt một đường "kịch bản → bản tin" | Mất cú pháp gọi `$tro-ly…` nếu Codex còn dùng |
| 3 | **Vạch ranh giới `chuyen-gia-edit-video-tan` ↔ `hieu-ung-video`**: `hieu-ung-video` giữ công thức từng hiệu ứng; `chuyen-gia` chỉ giữ quy trình dựng và gọi sang `hieu-ung-video` | Một công thức chỉ ở một chỗ | Cần soát sâu nội dung hai skill trước khi sửa |
| 4 | **Một router duy nhất**: bảng chọn skill trong `video-editor` là nơi định tuyến; `bien-tap-video` chỉ còn phần "phong cách theo chủ đề" | Hết hai bảng định tuyến lệch nhau | Nhỏ |
| 5 | **Định tuyến `ban-do-video`**: thêm một dòng vào bảng của `video-editor` | Skill có test nhưng chưa ai gọi | Không |
| 6 | **Test kích hoạt**: mỗi skill một câu mẫu "phải chọn skill này" đưa vào `scripts/harness_eval.py` | Đo được AI có chọn đúng skill không | Tốn lượt Claude khi chạy |
| 7 | **Ghi lại lần dùng skill** (cùng GĐ5 nhật ký hook) | Biết skill nào thật sự được dùng, thay cho đếm commit | Không |

Không đề xuất xoá skill nào của anh khi chưa có số liệu dùng thật (mục 7).
