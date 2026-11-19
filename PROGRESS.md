# Tiến độ repo tan-ai-skills

Cập nhật: 2026-11-20. Đầu mỗi phiên đọc file này; cuối phiên ("end session") cập nhật lại.

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
| 20/11 | **Skill/công cụ ngoài (không đổi code repo):** quét đủ 1.008 repo kho phandonggiang → `D:\GitHub\ngoai\kho-repo-phandonggiang.csv`; fork + clone 9 repo vào `D:\GitHub` (rtk, context7, claude-hud, VideoLingo, video-shotcraft, lossless-cut, claude-video, chrome-devtools-mcp, design.md). Cài: 11 skill (video-shotcraft, watch, context7-cli, chrome-devtools-cli + 7 skill chrome-devtools), MCP user `context7` + `chrome-devtools` (ghim phiên bản, `--isolated`), plugin claude-hud (statusLine), LosslessCut portable. lemo-opuscar (99 phong cách phim bằng code) cài + render thử được news-package; craft-anything 0.6.1 soi được trang English Kids. Chi tiết cách cập nhật: memory `project_cap_nhat_skill_goc` |
| 18–19/11 | unslop (sửa giao diện "trông như AI") cài toàn cục + thử trên English Kids (commit `7fef94e` ở nhánh `feature/m1-lesson-player`); blender-skills (28 skill, chờ máy có Blender), rea-video (Python 3.14, tách video 19 s mất ~9,5 phút). PR #46 (`skills-ngoai.json` thêm unslop) và senior-dev-harness PR #15 (README thêm unslop) đã merge |
| 16/11 | **tan-ai-skills:** PR #31 lưu việc bản tin an sinh; #32 chốt chặn font tiếng Việt (`kiem_font_viet.py`, sửa 22 chỗ Arial ≥800); #33 danh mục 37 mẫu `do-hoa/danh-muc.json` + trang xem trước `lam_gallery.mjs`; #34 mẫu `ChuChay` (băng chữ chạy); #35 CI cài fonttools+brotli; **bật bảo vệ nhánh `main` (chỉ merge khi CI `test` xanh)**; trỏ 13 junction Remotion về repo chính. Mở chờ merge: #36 (`BanDoNoi` `nhip12`, xuất WebM cho OBS, 13 skill Three.js trong `skills-ngoai.json`), #37 (`REMOTION_FPS=25` cho bản phát sóng). Đóng 5 PR nháp nhập skill hàng loạt (#30; att-news #7, #9, #10, #12) |
| 16/11 | **att-news:** merge #8 (Motion FX), #11 (gộp 10 skill đồ hoạ thành 1 tài liệu); đồng bộ 13 commit. Mở chờ merge **theo thứ tự** #13 logo bản trắng → #14 kiểm nhấp nháy + luật nhãn AI/trẻ em → #15 sổ nguồn `kiem_nguon.py` → #16 master ProRes/XDCAM + slate |
| 16/11 | Ngoài repo: bộ đóng logo `D:\DongLogo` (logo 25,9% ảnh, góc dưới phải), gói `Desktop\DongLogo_ATTnews.zip` gửi máy khác |
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
- **Smart App Control chặn file chưa ký số** (rtk.exe, DLL torch) → rtk không cài được, VideoLingo/whisperX không chạy. Không tự tắt (cài đặt bảo mật, tắt rồi không bật lại được).
- English Kids: Next.js 16.4.3 có lỗ hổng bảo mật đã biết (build cảnh báo); 1 bài e2e "increased text keeps flashcard navigation readable" trượt (có từ trước, khu vực Codex đang sửa).
- Script phim mẫu của lemo-opuscar viết cho Mac/Linux: trên Windows cần `-X utf8` và shim `python3` đổi `/d/` → `D:/` (đã ghi memory).

## Việc tiếp theo (theo thứ tự ưu tiên)

**Tiếp từ 20/11 (làm trước):**
- Thử thật các công cụ mới trên việc thật: `chrome-devtools` đo tốc độ/LCP trang English Kids; `video-shotcraft` hoặc `lemo-opuscar` (news-package, font đủ dấu tiếng Việt) làm 1 video quảng bá ngắn; `watch` xem nhanh video mẫu.
- English Kids: nâng Next.js lên bản vá bảo mật (việc riêng, có test); xem lại bài e2e đang trượt khi Codex xong phần flashcard.
- Mở phiên Claude Code mới để kiểm thanh trạng thái claude-hud hiện đúng.

**Tiếp từ 16/11:**
- ✓ (17/11) Đã merge tan-ai-skills #36, #37, #40; att-news #13–#17, #20.
- Đánh giá att-news theo chuẩn truyền hình (16/11): đã làm việc 1–5 (25 hình/giây, nhấp nháy, luật AI/trẻ em, sổ nguồn, master+slate). **Còn:** việc 6 `PROGRESS.md` riêng cho att-news (đang là bản chép của tan-ai-skills); việc 7 harness có agent điều phối cho kênh.
- Chờ người dùng: thư mục tư liệu thật để chạy `/dai` lần đầu (nhật ký sản xuất còn trống); danh bạ người đã xác minh (`kenh/danh-ba.json` 0 người); nhạc hiệu có bản quyền; chuẩn âm lượng/định dạng của đài nhận bài; lịch sao lưu 21:00 (`kenh/van-hanh/sao_luu.ps1`) người dùng tự tạo.

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
    **Motion graphics** (đợt 1–3 PR #10, #11, #12 đã merge; đợt 4 02/11, nhánh `feat/motion-graphics-dot-4`, đã commit, chưa push): skill `motion-graphics-tan`
    đủ 20 phong cách, đều CSS/SVG, không WebGL. Font tiếng Việt riêng ở `assets/fonts/`. `render_mau.py`: check → render trên máy → ảnh 4 khung + ảnh cắt sát
    `.chu.png`; `--trong-suot` ra .webm alpha. **Việc kế tiếp quan trọng nhất:** thử thật trên clip người nói 9:16 (người dùng hẹn gửi sau):
    `tim_cau_noi` → `tach_nguoi` → `render_mau --trong-suot` → `ghep_lop`, cùng GĐ B, C của `video-marketing`.
    Khác: GĐ3 `/thiet-ke` (Playwright chụp màn nhỏ/lớn + axe, cần một dự án web thật).
1. Soát ảnh VNeID trên repo công khai.
2. Thêm `/khoi-tao-du-an` vào danh sách "Command gọi được" trong `CLAUDE.md`.
3. Harness engineering GĐ5 (nhật ký mỗi lần hook chặn/hỏi/nhắc).
