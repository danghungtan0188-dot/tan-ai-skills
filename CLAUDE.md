# Nguyên tắc làm việc trong repo này

Bộ nguyên tắc giảm các lỗi thường gặp khi AI hỗ trợ làm việc.
Phỏng theo `andrej-karpathy-skills`, đã điều chỉnh cho quy trình của repo này.

**Đánh đổi:** các nguyên tắc này thiên về cẩn trọng hơn là tốc độ. Với việc vặt, dùng phán đoán.

---

## 1. Nêu giả định, đừng dừng lại hỏi vặt

- Nêu rõ giả định đang dùng, rồi **làm tiếp** — đừng dừng chờ xác nhận.
- Nếu có nhiều cách hiểu, chọn cách hợp lý nhất, **nói rõ đã chọn cách nào**, rồi làm.
- Chỉ dừng lại hỏi khi: giả định sai sẽ phải **làm lại toàn bộ**, hoặc thao tác **không thể hoàn tác** (xóa file, đẩy lên mạng, gửi đi cho người khác).
- Với pipeline video: tự động định tuyến vào chuỗi skill, lặp tới khi được duyệt. **Không hỏi lại mỗi vòng.**

## 2. Đơn giản trước

**Lượng công việc tối thiểu giải quyết đúng vấn đề. Không làm dư.**

- Không thêm tính năng ngoài yêu cầu.
- Không tạo lớp trừu tượng cho thứ chỉ dùng một lần.
- Không thêm "linh hoạt", "cấu hình được" nếu không được yêu cầu.
- Không xử lý lỗi cho tình huống không thể xảy ra.
- Nếu viết 200 dòng mà 50 dòng là đủ, viết lại.

Tự hỏi: "người có nghề nhìn vào có thấy chỗ này rườm rà không?" Nếu có, làm gọn lại.

## 3. Sửa đúng chỗ cần sửa

**Chỉ động vào thứ buộc phải động. Chỉ dọn phần mình bày ra.**

- Không "cải thiện" đoạn bên cạnh, không sửa lại cách trình bày, không đổi định dạng.
- Không viết lại thứ đang chạy tốt.
- Theo đúng văn phong sẵn có, kể cả khi mình muốn viết khác.
- Thấy chỗ thừa không liên quan thì **nói ra, đừng tự xóa**.
- Chỉ xóa những thứ mà chính thay đổi của mình làm cho thành thừa.

**Phép thử:** mọi dòng bị thay đổi đều phải truy ngược được về yêu cầu của người dùng.

## 4. Làm việc theo tiêu chí kiểm chứng được

**Định nghĩa thế nào là xong. Lặp tới khi kiểm chứng được là đã xong.**

Biến yêu cầu mơ hồ thành tiêu chí kiểm được:

- "làm video hay hơn" → "đúng tỉ lệ khung hình, phụ đề khớp giọng đọc, thời lượng dưới 60 giây"
- "sửa lỗi này" → "tái hiện được lỗi, sửa, rồi tái hiện lại thấy hết lỗi"
- "viết skill mới" → "skill kích hoạt đúng khi gõ câu mẫu X, không kích hoạt khi gõ câu Y"

Với việc nhiều bước, nêu kế hoạch ngắn trước khi làm:

```
1. [Bước] → kiểm: [cách xác nhận]
2. [Bước] → kiểm: [cách xác nhận]
```

**Không báo "đã xong" khi chưa thật sự kiểm chứng.** Nếu có phần bị bỏ dở hoặc không kiểm được, nói thẳng phần nào và vì sao.

---

**Các nguyên tắc này đang phát huy tác dụng nếu:** ít thay đổi thừa trong mỗi lần sửa, ít phải làm lại vì rườm rà, và mọi báo cáo "đã xong" đều đúng sự thật.

---

# Bản đồ hệ thống (riêng repo này)

Phần trên là nguyên tắc dùng chung. Phần dưới chỉ áp dụng cho repo `tan-ai-skills`.
Giải thích đầy đủ: [ARCHITECTURE.md](ARCHITECTURE.md).

## Có gì ở đâu

```text
.claude/agents/     9 agent   — Claude Code chỉ đọc agent ở đây
.claude/commands/   9 command — slash command
.claude/hooks/      3 hook    — wiring trong .claude/settings.json
skills/             25 skill  — NGUỒN CHUẨN, mirror sang .claude/skills/ + .agents/skills/
rules/              4 rule bắt buộc
data-contracts/     JSON Schema truyền dữ liệu giữa agent
scripts/            script dùng chung (sync_skills.py, video_qa.py)
tests/              python -m unittest discover -s tests
```

## Chọn nhánh nào

| Yêu cầu về | Nhánh | Chuỗi |
|---|---|---|
| code, API, database, UI, bug, test | **APP** | `app-planner → app-builder → code-reviewer → app-tester → security-reviewer` |
| video, dựng, phụ đề, hiệu ứng, bản tin | **VIDEO** | `video-analyzer → video-editor → video-reviewer` |
| skill, agent, command, hook, tài liệu | **REPO** | tự làm + `python scripts/sync_skills.py --check` |

Chưa rõ thuộc nhánh nào → gọi agent `orchestrator`.

## Command gọi được

`/build-feature` `/fix` `/review` `/test` `/security-check`
`/video-news` `/edit-video` `/review-video` `/sync-skills`

## Rule bắt buộc đọc

- [rules/global.md](rules/global.md) — không bịa; **NO TEST = NO PASS**; FAIL → sửa → chạy lại (tối đa 3 vòng)
- [rules/coding.md](rules/coding.md) — đọc trước khi sửa, thay đổi nhỏ nhất, không phá thứ đang PASS
- [rules/security.md](rules/security.md) — secret, RLS, lệnh bị chặn
- [rules/video.md](rules/video.md) — chuẩn output, render xong ≠ xong, không che mặt

## Hook đang hoạt động

| Hook | Khi nào | Làm gì |
|---|---|---|
| `guard_secrets.py` | trước Write/Edit | chặn ghi `.env` thật và secret |
| `guard_bash.py` | trước Bash | chặn hẳn lệnh phá dữ liệu; **hỏi người dùng** với push/deploy/publish |
| `check_render.py` | sau Bash có `ffmpeg` | tự probe file đầu ra, chặn nếu render hỏng |

## Validation

```bash
python -m unittest discover -s tests   # test kiến trúc + hook + contract
python scripts/sync_skills.py --check  # 3 bản skill đã khớp chưa
python scripts/video_qa.py <file> --strict --audio   # QA video đầy đủ
```

## Claude KHÔNG được tự ý

1. Push GitHub, tạo PR, deploy, publish package.
2. Reset/xóa database, tắt RLS, tạo Service Role key.
3. Ghi secret hoặc file `.env` thật.
4. Ghi đè file video gốc; cắt thời lượng khi chưa được phép.
5. Báo PASS cho hạng mục chưa thực sự chạy.

## Quy ước đường dẫn trong file .md

Agent và command được nạp như prompt, cwd là gốc repo → liên kết tới file cấp repo phải tính **từ gốc repo** (`rules/global.md`), không dùng `../`. Liên kết trong nội bộ skill thì tính từ thư mục skill (`references/frontend.md`). `tests/test_architecture.py` ép quy ước này.

## Sửa skill

`skills/` là nguồn chuẩn duy nhất. Sửa xong chạy `python scripts/sync_skills.py --force`. Không sửa trực tiếp `.claude/skills/` hay `.agents/skills/` — sẽ bị ghi đè.
