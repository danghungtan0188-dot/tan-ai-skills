---
description: Đồng bộ skills/ (nguồn chuẩn) sang .claude/skills/ và .agents/skills/, rồi chạy test kiến trúc
allowed-tools: Bash(python scripts/sync_skills.py:*), Bash(python -m unittest:*), Read, Glob
---

Kiểm tra trạng thái đồng bộ trước:

```bash
python scripts/sync_skills.py --check
```

Có skill lệch → đồng bộ:

```bash
python scripts/sync_skills.py --force
```

Rồi chạy test kiến trúc để chắc chắn agent/command/skill/contract vẫn hợp lệ:

```bash
python -m unittest discover -s tests -v
```

Báo cáo: skill nào đã được đồng bộ, skill nào đã sẵn khớp, và kết quả test (số test chạy, số fail). Có fail → in lỗi thật, không tóm tắt.

Nhắc: `skills/` là nguồn chuẩn duy nhất. Không sửa trực tiếp `.claude/skills/` hay `.agents/skills/` — sẽ bị ghi đè.
