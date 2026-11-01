# Tiến độ repo tan-ai-skills

Cập nhật: 2026-10-27. Đầu mỗi phiên đọc file này; cuối phiên ("end session") cập nhật lại.

## Tình trạng hiện tại

- 29 skill, 13 command, 9 agent, 7 hook (khai báo cả ở `~/.claude/settings.json` nên chạy ở mọi dự án). Test: `python -m unittest discover -s tests` (345 bài, đều đạt trên máy; đã gồm test `remotion-studio` và test số đếm trong CLAUDE.md).
- Bài học → chốt chặn: `docs/bai-hoc-va-chot-chan.md` (bài học mới loại "máy" phải có hook/test trước khi ghi dòng).
- Repo GitHub **công khai**.
- Nâng cấp theo bảng chấm điểm: bước 1–4 xong (PROGRESS.md, test số đếm, gộp test, GitHub Actions).
  `.github/workflows/test.yml` chạy test trên Windows với `PYTHONUTF8=1`; lần 3 (commit `4c6d79b`,
  25/10) **xanh**. Xem lại bằng `gh run list --workflow test.yml`.

## Đã làm gần đây

| Ngày | Việc |
|---|---|
| 27/10 | Harness engineering GĐ4, nhánh `feat/bai-hoc-thanh-chot-chan`: `guard_bash` dò lệnh trong `bash -c`/`powershell -Command`/`cmd /c`/heredoc; hook mới `guard_video` (loudnorm, preset, một ffmpeg một lúc) và `guard_tra_phi` (hỏi trước HeyGen); test Remotion không dùng `OffthreadVideo`; bản đồ `docs/bai-hoc-va-chot-chan.md` |
| 27/10 | Harness engineering GĐ1–3 (PR #2 đã merge): GĐ1 vá `guard_bash` (lệnh xoá PowerShell/cmd, ffmpeg ghi đè gốc, `git add -A`); GĐ2 hook ra `~/.claude/settings.json`, lệnh dạng chịu lỗi khi thiếu file (bản lưu `settings.json.bak-20261027*`); GĐ3 hook `session_start` + `nhac_test` |
| 25/10 | Thêm skill `humanizer` (MIT); ghi chú học từ OpenMontage + Diagram Design; fork 4 repo về GitHub |
| 25/10 | `.gitignore` chặn `.env`; commit `xay-ai-agent`, `/quet-kien-truc`, `remotion-studio`; push 11 commit |
| 24/10 | Lệnh `/khoi-tao-du-an` |
| 22/10 | Skill `ban-do-video`; mẫu đồ họa SoDeFlycam, BanDoNoi, GhepCanh, HudDemSo; `tim-canh` tìm cảnh Pexels/Pixabay |
| 21/10 | `video_qa --strict --audio`; phụ đề tự tránh mặt (YuNet); render dùng Intel QuickSync |

## Lỗi và việc còn tồn

- **Máy hay sập khi chạy nặng** — luôn chạy một việc nặng một lúc, ffmpeg 2 luồng, Remotion 1 luồng. RAM chưa được kiểm tra lần nào.
- `remotion.exe` bị Windows chặn → `OffthreadVideo` lỗi; mẫu mới dùng `Video` của `@remotion/media`.
- VieNeu-TTS đọc sai vài từ ("ủy", "Hữu"); số phải viết thành chữ.
- Media nặng của `remotion-studio` (`giong.wav`, `nguon.mp4`) chỉ có trên máy, không có trên GitHub.
- Ảnh VNeID trong `remotion-studio/public/vneid-tien-ich/` đã lên repo công khai — cần soát không lộ thông tin cá nhân.
- MCP `n8n` báo không kết nối được (n8n ở localhost:5678 chưa bật).

## Việc tiếp theo (theo thứ tự ưu tiên)

0. **GĐ4 đang dở** (nhánh `feat/bai-hoc-thanh-chot-chan`, đã commit, chưa push; 345 test đạt):
   a. ✓ (28/10) `guard_video.py` và `guard_tra_phi.py` đã có trong `~/.claude/settings.json`, dạng chịu lỗi;
      bản lưu `settings.json.bak-20261028`.
   b. ✓ (30/10) Thử thật bằng `claude -p --model haiku` ở thư mục tạm ngoài repo (chỉ hook toàn cục chạy):
      `bash -c "rm -rf ."` → guard_bash chặn, file mồi còn nguyên; ffmpeg `libx264` thiếu preset → guard_video
      chặn, không tạo `out.mp4`; Skill `heygen-video` → guard_tra_phi hỏi (chế độ `-p` coi như từ chối).
   c. Push nhánh, tạo PR vào `main`; người dùng tự merge (Claude bị chặn merge).
0b. **Harness phần mềm GĐ1** (30/10, nhánh `feat/guard-app` tách từ nhánh GĐ4, đã commit, chưa push): hook `guard_app`
    hỏi trước khi cài thư viện mới / chạy migration / `DROP TABLE`; chặn secret mang tiền tố công khai và
    Stripe `sk_live_`. Đã gắn cả `~/.claude/settings.json` (bản lưu `settings.json.bak-20261030-guard-app`).
    Thử `claude -p`: `npm install left-pad` bị hỏi.
    **GĐ2** (30/10, cùng nhánh, đã commit, chưa push): `nhac_test` thành cổng "xong" — đọc mục `## Lệnh kiểm tra`
    trong CLAUDE.md dự án (không có thì script `package.json`), đòi chạy thành công đủ từng lệnh sau lần sửa
    cuối; `/khoi-tao-du-an` ghi mục này. Thử `claude -p` ở dự án mẫu: Haiku sửa code → bị chặn → chạy test → PASS.
    **GĐ4** (01/11, cùng nhánh, đã commit, chưa push): `scripts/harness_eval.py` — 7 ca chạy `claude -p --model haiku`
    ở thư mục tạm ngoài repo (chỉ hook toàn cục), chấm theo kết quả thật (file còn/mất, hook trả lời, test có
    chạy); có ca đối chứng "lệnh lành không bị chặn nhầm". Chạy thật: **7/7 PASS**. Test offline phần chấm:
    `tests/test_harness_eval.py`. Lưu ý: thư mục tạm phải `resolve()` bỏ tên ngắn 8.3, nếu không Claude Code đòi duyệt tay.
    PR #4 (gồm #3) đã merge vào `main` 01/11 (`3f3498f`). Máy vẫn ở nhánh `feat/guard-app`.
    **Kiểm kê skill** (01/11, nhánh `chore/skill-mot-nguon`, đã commit, chưa push): `docs/kiem-ke-skill.md`, 7 đề xuất. Đã làm đề xuất 1: 15 skill ở
    `~/.claude/skills` thành junction về repo (bản cũ ở `~/.claude/skills_cu_ban_chep_20261101/`), `video-use`
    giữ bản cài riêng (.venv); `sync_skills.py --check` bắt bản chép riêng lệch repo.
    **Harness video** (01/11, nhánh `feat/harness-video`, đã commit, chưa push): `docs/harness-video.md` — vòng bán tự động 2 cổng duyệt, bản đồ
    kiến trúc đích ↔ thành phần thật, lộ trình 7 bước. Bước 1 ✓ (bản đồ + test), bước 2 ✓ `evaluations/bai_thi.py`:
    10 tiêu chí, ~10 giây, 10/10 DAT, LUFS -16,0; ba kiểu `--hong` đều báo HỒI QUY. PR #5 đã merge.
    Bước 3 ✓ (đã commit, chưa push): `observability/` — mọi hook ghi khi chặn/hỏi/nhắc, hook mới `ghi_su_dung` (skill/agent/lệnh),
    xem `python observability/xem.py`; dữ liệu `~/.tan-harness/nhat-ky/` (ngoài repo, chỉ nhãn). Gắn cả
    `~/.claude/settings.json` (bản lưu `settings.json.bak-20261101-nhat-ky`). Phiên Haiku thật để lại 3 dòng đúng.
    Bước 4 ✓ (đã commit, chưa push): lệnh `/dung-video` — gợi ý → `edit/brief.json` (hợp đồng `VideoBrief`, kiểm bằng
    `scripts/kiem_brief.py`) → định tuyến sang `dung-tu-kho` / `video-news` / `edit-video` / `tan_studio` → 2 cổng duyệt →
    `/rut-kinh-nghiem`. Ca thật `harness_eval --ca dung-video-cong-1`: lần đầu Haiku tự đặt tên trường → thêm khuôn JSON
    trong lệnh + script kiểm bắt buộc. Kế tiếp bước 5–7 `docs/harness-video.md`. Sau ~2 tuần nhật ký: đề xuất 2–7 `docs/kiem-ke-skill.md`.
    **Cập nhật skill gốc** (01/11, nhánh `chore/cap-nhat-skill-goc`, đã commit, chưa push): fork `remotion`/`hyperframes`/`humanizer`
    đã `gh repo sync` (REA: script `D:\GitHub\dong-bo-rea.ps1` chạy 8h sáng, đã mới nhất). Remotion 4.0.505 → 4.0.539 (+`remotion-studio`,
    giữ sửa link `../remotion-x/`); `video-use` lên `43cfc56` (bản repo = gốc `92c2b34`, pyproject không đổi); HeyGen, humanizer
    đã giống gốc. Ngoài repo: HyperFrames `npx skills@1.7.4 update -g` (4 skill) + thay `figma`/`slideshow`/`remotion-to-hyperframes`;
    sao lưu `~/.claude/skills_cu_truoc_update_20261101/`. Đã gỡ 14 skill HyperFrames gốc đã bỏ (`RETIRED_SKILLS` trong CLI
    HyperFrames) và cài `reverse-any-video` → bộ trên máy = đúng 8 skill của gốc; Haiku thật chọn đúng `hyperframes`.
    Test riêng của video-use NOT RUN (bị chặn). PR #7 (skill Remotion + video-use) chờ merge.
    Cài thêm (ngoài repo): 8 skill `gsap-*` (greensock/gsap-skills, qua `npx skills`) và Playwright CLI 0.1.23
    (`@playwright/cli`, skill `~/.claude/skills/playwright-cli`). Thử thật: Haiku chọn đúng `gsap-timeline`; playwright-cli
    mở demo todomvc, gõ, chụp màn hình được. Dự án web nên thêm `.playwright-cli/` vào .gitignore.
    **Skill ngoài repo** (01/11, nhánh `feat/skill-ngoai` tách từ nhánh PR #7, đã commit, chưa push): `scripts/skills-ngoai.json` (35 mục:
    HyperFrames 8, GSAP 8, Playwright CLI, 16 junction, video-use) + `scripts/cai_skill_ngoai.py --kiem|--cai|--cap-nhat`;
    máy này 35/35 đạt. `video-editor` định tuyến GSAP (`gsap-timeline`…) và `reverse-any-video`. PR #7, #8 đã merge.
    **Video marketing GĐ A** (01/11, nhánh `feat/video-marketing`, đã commit, chưa push): skill `video-marketing` — `tim_cau_noi.py` (whisper small, câu → giây,
    khớp < 60% thì dừng), `tach_nguoi.py` (cắt đúng đoạn + `npx hyperframes@0.8.226 remove-background` + YuNet → tren_dau),
    `ghep_lop.py` (nền → hiệu ứng → người; .webm phải giải mã libvpx-vp9 để giữ alpha). Test thật ghép lớp đạt.
    CHƯA chạy whisper/tách nền trên video người nói thật — cần người dùng chỉ một clip 9:16. Kế tiếp: GĐ B tra catalog, GĐ C mẫu Bar Chart Race + Checklist.
    Khác: GĐ3 `/thiet-ke` (Playwright chụp màn nhỏ/lớn + axe, cần một dự án web thật).
1. Soát ảnh VNeID trên repo công khai.
2. Thêm `/khoi-tao-du-an` vào danh sách "Command gọi được" trong `CLAUDE.md`.
3. Harness engineering GĐ5 (nhật ký mỗi lần hook chặn/hỏi/nhắc).
