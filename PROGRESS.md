# Tiến độ repo tan-ai-skills

Cập nhật: 2026-10-25. Đầu mỗi phiên đọc file này; cuối phiên ("end session") cập nhật lại.

## Tình trạng hiện tại

- 29 skill, 12 command, 9 agent, 3 hook. Test: `python -m unittest discover -s tests` (299 bài, đều đạt).
- Máy và GitHub khớp nhau tới commit `b3daeaa` (repo **công khai**).
- Đang làm: nâng cấp repo theo bảng chấm điểm (PROGRESS.md → test số đếm → gộp test → GitHub tự chạy test).

## Đã làm gần đây

| Ngày | Việc |
|---|---|
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

1. Test tự kiểm số skill/command ghi trong `CLAUDE.md` khớp thực tế.
2. Gộp test `remotion-studio` vào lệnh test chung.
3. GitHub Actions tự chạy test sau mỗi lần push.
4. Soát ảnh VNeID trên repo công khai.
