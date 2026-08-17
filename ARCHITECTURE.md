# Kiến trúc hệ thống

Tài liệu này giải thích **cách các lớp nối vào nhau**. Nguyên tắc làm việc nằm ở [CLAUDE.md](CLAUDE.md); rule chi tiết nằm trong [rules/](rules/).

## Sáu lớp

```text
Agent   = Ai thực hiện?
Command = Tôi gọi công việc bằng cách nào?
Skill   = Công việc được thực hiện như thế nào?
Rule    = Quy tắc bắt buộc phải tuân thủ
Hook    = Kiểm soát tự động trước/sau thao tác
Test    = Làm sao biết kết quả thực sự đúng?
```

## Luồng tổng quát

```text
USER
 ↓
COMMAND            .claude/commands/*.md
 ↓
ORCHESTRATOR       .claude/agents/orchestrator.md
 ↓
SPECIALIST AGENT   .claude/agents/*.md
 ↓
SKILL              skills/*/SKILL.md
 ↓
RULES              rules/*.md
 ↓
IMPLEMENTATION
 ↓
HOOKS / VALIDATION .claude/hooks/*.py, scripts/video_qa.py
 ↓
REVIEWER
 ↓
PASS → OUTPUT
FAIL → Fix → Retest  (tối đa 3 vòng)
```

## Luồng APP

```text
Request
 → app-planner      → ImplementationPlan
 → app-builder      → ImplementationResult
 → code-reviewer    → ReviewReport
 → app-tester       → TestReport
 → security-reviewer→ ReviewReport
 → PASS
```

Cổng chất lượng: `TestReport` không có hạng mục nào `FAIL`, và `ReviewReport.verdict = PASS`. Hạng mục chưa chạy ghi `NOT_RUN` kèm lý do — **không** được suy ra là PASS.

## Luồng VIDEO

```text
Video
 → video-analyzer  → VideoAnalysis   (ffprobe + contact sheet)
 → video-editor    → EditPlan + RenderResult
 → [hook check_render tự chạy sau mỗi lệnh ffmpeg]
 → video-reviewer  → VideoQAReport   (ffprobe --strict + xem khung hình)
 → PASS
```

`ffmpeg exit code 0` **không** phải PASS. Chỉ `VideoQAReport.status` mới quyết định.

## Vị trí file — và vì sao

| Thành phần | Vị trí | Lý do |
|---|---|---|
| Agents | `.claude/agents/` | Claude Code **chỉ** đọc agent ở đây. Đặt ở root sẽ thành Markdown chết. |
| Commands | `.claude/commands/` | Tương tự — đây là nơi slash command được nạp. |
| Hooks | `.claude/hooks/` + `.claude/settings.json` | `settings.json` là nơi duy nhất wiring hook được đọc. |
| Skills | `skills/` (nguồn chuẩn) | Mirror sang `.claude/skills/` (Claude Code) và `.agents/skills/` (Codex) bằng `scripts/sync_skills.py`. |
| Rules | `rules/` | Tài liệu người đọc, được agent/command/skill tham chiếu bằng đường dẫn. |
| Data contracts | `data-contracts/` | JSON Schema, kiểm được bằng test. |
| Script dùng chung | `scripts/` | Dùng bởi cả hook, command và agent. |
| Tests | `tests/` | `python -m unittest discover -s tests` |

**Quy ước đường dẫn:** agent và command được nạp như prompt, khi Claude đọc file thì cwd là gốc repo. Vì vậy mọi liên kết tới file cấp repo phải **tính từ gốc repo** (`rules/global.md`), không dùng `../`. Liên kết trong nội bộ một skill thì tính từ thư mục skill (`references/frontend.md`). Test `tests/test_architecture.py` ép quy ước này.

## Agents

| Agent | Trách nhiệm | Không được làm |
|---|---|---|
| `orchestrator` | Phân loại APP/VIDEO/REPO, chọn agent, sắp thứ tự, tổng hợp | Viết code, chạy ffmpeg |
| `app-planner` | Đọc kiến trúc, lập `ImplementationPlan` | Sửa file (chỉ có quyền đọc) |
| `app-builder` | Viết code frontend/backend/database | Sửa ngoài phạm vi, tự kết luận PASS |
| `code-reviewer` | Tìm lỗi logic, chỗ phá vỡ chức năng đang chạy, chỗ rườm rà | Sửa code |
| `security-reviewer` | Secret, auth/phân quyền, RLS, injection, log | Sửa code |
| `app-tester` | Chạy lint/typecheck/test/build thật | Sửa code, bịa lệnh |
| `video-analyzer` | ffprobe + contact sheet → `VideoAnalysis` | Dựng, render |
| `video-editor` | `EditPlan` + thực thi qua skill video | Cắt khi chưa được phép |
| `video-reviewer` | QA file đã render, phán quyết PASS/FAIL | Sửa video |

## Commands

| Command | Chuỗi |
|---|---|
| `/build-feature` | planner → builder → reviewer → tester → security |
| `/fix` | tái hiện → nguyên nhân gốc → test đỏ → sửa → xác nhận |
| `/review` | code-reviewer |
| `/test` | app-tester |
| `/security-check` | security-reviewer |
| `/video-news` | analyzer → template bản tin → editor → reviewer |
| `/edit-video` | analyzer → định tuyến skill → editor → reviewer |
| `/review-video` | video-reviewer |
| `/sync-skills` | sync_skills.py + test kiến trúc |

## Hooks

| Hook | Sự kiện | Hành vi |
|---|---|---|
| `guard_secrets.py` | PreToolUse trên `Write\|Edit\|NotebookEdit` | Chặn (exit 2) khi ghi `.env` thật hoặc secret. Placeholder được cho qua. |
| `guard_bash.py` | PreToolUse trên `Bash\|PowerShell` | **Chặn hẳn** lệnh phá dữ liệu/tắt bảo mật. **Hỏi người dùng** với thao tác ra ngoài (push, deploy, publish). |
| `check_render.py` | PostToolUse trên `Bash\|PowerShell` | Sau mỗi lệnh `ffmpeg`, tự probe file đầu ra. Chặn khi file hỏng nặng; chỉ cảnh báo với vấn đề định dạng. |

Hook là **lớp kiểm tra nhanh**. Kiểm tra đầy đủ nằm ở agent reviewer:

```text
check_render.py (lenient)  →  chặn file hỏng, cảnh báo phần còn lại
video_qa.py --strict       →  coi mọi cảnh báo là lỗi, dùng ở /review-video
```

## Data contracts

Agent truyền dữ liệu cho nhau bằng object có schema, không bằng văn xuôi.

```text
APP:   FeatureRequest → ImplementationPlan → ImplementationResult → TestReport → ReviewReport
VIDEO: VideoInput → VideoAnalysis → EditPlan → RenderResult → VideoQAReport
```

Schema ép luôn rule chống PASS giả: `TestReport` có `status: PASS` **bắt buộc** phải kèm `command` và `exit_code`; `status: NOT_RUN` **bắt buộc** kèm `reason_not_run`; không tồn tại giá trị `ALL_PASS`. Test `tests/test_contracts.py` kiểm đúng những ràng buộc này.

## Tests

```bash
python -m unittest discover -s tests -v
```

| File | Kiểm gì |
|---|---|
| `test_hooks.py` | Nạp JSON vào stdin của hook như Claude Code làm thật, kiểm exit code cho từng tình huống chặn/hỏi/cho qua |
| `test_contracts.py` | Schema hợp lệ, ví dụ khớp schema, ràng buộc chống PASS giả có hiệu lực |
| `test_architecture.py` | Frontmatter agent/command, hook trỏ tới script có thật, liên kết `rules/`+`data-contracts/` không hỏng, skill đã đồng bộ |

## Điều Claude không được tự ý làm

1. Push GitHub, tạo PR, deploy, publish package — hook hỏi người dùng trước.
2. Reset/xóa database, tắt RLS, tạo Service Role key — chặn hẳn.
3. Ghi secret hoặc `.env` thật — chặn hẳn.
4. Ghi đè file video gốc, cắt thời lượng khi chưa được phép.
5. Báo PASS cho hạng mục chưa thực sự chạy.
