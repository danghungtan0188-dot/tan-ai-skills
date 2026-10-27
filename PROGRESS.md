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
   a. Cho người dùng xem rồi mới thêm `guard_video.py` (nhóm `Bash|PowerShell`) và `guard_tra_phi.py`
      (matcher `Bash|PowerShell|Skill|mcp__heygen__.*`) vào `~/.claude/settings.json`, đúng dạng lệnh chịu
      lỗi khi thiếu file như 5 hook đang có; sao lưu settings trước.
   b. Thử thật bằng `claude -p` (Haiku) ở thư mục tạm: `bash -c "rm -rf ."` bị chặn; ffmpeg `libx264` thiếu
      preset bị chặn; gọi skill `heygen-video` thì bị hỏi.
   c. Push nhánh, tạo PR vào `main`; người dùng tự merge (Claude bị chặn merge).
1. Soát ảnh VNeID trên repo công khai.
2. Thêm `/khoi-tao-du-an` vào danh sách "Command gọi được" trong `CLAUDE.md`.
3. Harness engineering GĐ5 (nhật ký mỗi lần hook chặn/hỏi/nhắc).
