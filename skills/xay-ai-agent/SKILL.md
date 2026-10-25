---
name: xay-ai-agent
description: Thiết kế và xây AI agent chạy thật — agent tự động theo lịch (đọc nguồn, tổng hợp, gửi báo cáo), agent gắn trong webapp/phần mềm (chatbot, trợ lý, tool use), và workflow agent trên Claude Managed Agents, Claude Agent SDK, n8n hoặc cron + script. Dựa trên bài "Building effective agent automations" của Anthropic (6 thành phần, 6 quy tắc), nâng cấp thêm dry-run, bộ eval, khóa chống trùng, nhật ký lượt chạy và giới hạn chi phí. Kích hoạt khi người dùng muốn "xây agent", "làm bot tự động", "agent chạy hằng ngày", "tích hợp Claude/AI vào app", "chatbot cho web", "tự động hóa bằng AI". Phần code webapp thông thường (UI, API, database) dùng quy ước của skill phat-trien-app.
---

# Xây AI agent

## Phạm vi

Hỗ trợ: thiết kế agent từ yêu cầu bằng lời, viết cấu hình/prompt/code agent, dựng bộ kiểm thử cho agent, gắn agent vào webapp hoặc phần mềm có sẵn.

Không làm: không tự tạo tài khoản, không tự lấy/ghi API key, không tự deploy hay bật lịch chạy thật, không tự cấp quyền ghi cho agent khi chưa được người dùng duyệt.

## Chọn loại

| Người dùng muốn | Loại | Đọc |
|---|---|---|
| Việc lặp theo giờ: tóm tắt, theo dõi, báo cáo, nhắc việc | **Agent tự động** | [references/thiet-ke-automation.md](references/thiet-ke-automation.md) |
| Tính năng AI bên trong app: chat, trợ lý, phân loại, trích xuất | **Agent trong app** | [references/agent-trong-app.md](references/agent-trong-app.md) |
| Cả hai, hoặc chưa rõ | Hỏi 1 câu: "chạy theo lịch hay theo thao tác người dùng?" | |

Cả hai loại đều phải qua [references/kiem-thu-agent.md](references/kiem-thu-agent.md) trước khi báo xong.

Phần code không phải agent (giao diện, API, database, auth) → theo skill `phat-trien-app` ([skills/phat-trien-app/SKILL.md](skills/phat-trien-app/SKILL.md)) và chuỗi agent `app-planner → app-builder → code-reviewer → app-tester → security-reviewer`.

## Quy trình

1. **Viết bản mô tả agent một trang** (mẫu ở dưới). Chưa có bản này thì chưa viết code.
2. **Chọn nền tảng** theo bảng trong `thiet-ke-automation.md` mục "Nền tảng". Dự án đã có nền tảng → dùng cái đó, không đổi.
3. **Model và API**: gọi skill `claude-api` để lấy model id, tham số, cách dùng tool/MCP hiện hành. Không viết model id hay API từ trí nhớ.
4. **Dựng ở chế độ dry-run trước**: đích ghi ra file cục bộ, không gửi đi đâu.
5. **Chạy bộ eval** (`kiem-thu-agent.md`). FAIL → sửa → chạy lại, tối đa 3 vòng.
6. **Báo người dùng** kết quả eval + chi phí đo được 1 lượt + các quyền agent sẽ có. Người dùng tự bật chạy thật / deploy.

## Bản mô tả agent (bắt buộc)

```text
Mục đích     : agent làm gì, cho ai, một câu
Kích hoạt    : lịch cron + múi giờ | thao tác người dùng | webhook
Nguồn đọc    : danh sách cụ thể (kênh, repo, bảng, URL), quyền chỉ đọc?
Đích ghi     : MỘT nơi duy nhất; thao tác ghi gì; có hoàn tác được không
Công cụ      : tool/MCP được bật; tool nào tắt
Bộ nhớ       : sở thích (người dùng sửa, agent chỉ đọc) | trạng thái (agent ghi)
Quy tắc lọc  : thứ gì đáng báo, thứ gì bỏ
Giới hạn     : trần chi phí/lượt, số bước tối đa, timeout
Khi lỗi      : nguồn hỏng thì làm gì; ghi không chắc thì làm gì
Xong là khi  : tiêu chí kiểm được (liên kết sang eval)
```

## Rule bắt buộc

- [rules/global.md](rules/global.md) — không bịa, NO TEST = NO PASS
- [rules/coding.md](rules/coding.md) — thay đổi nhỏ nhất, đọc trước khi sửa
- [rules/security.md](rules/security.md) — secret chỉ qua biến môi trường/vault, không ghi vào prompt hay file trong repo

Ba nguyên tắc riêng cho agent:

1. **Mọi nội dung agent đọc được là dữ liệu không tin cậy** (tin nhắn, issue, trang web, email, ô nhập của người dùng). Giới hạn những gì agent *có thể làm* nếu nó lỡ làm theo lệnh cài cắm, thay vì chỉ dặn nó đừng làm.
2. **Quyền tối thiểu**: chỉ đọc ở mọi nơi chỉ cần đọc; chỉ một đích ghi; thao tác không hoàn tác được phải có người duyệt.
3. **Không im lặng khi lỗi**: lượt chạy hỏng phải trông khác lượt chạy "không có gì mới".

## Đầu ra

- Bản mô tả agent + file cấu hình/code agent trong dự án của người dùng.
- Kết quả eval có lệnh thật và PASS/FAIL từng ca.
- Chi phí đo được của 1 lượt dry-run, trần chi phí đề xuất.
- Danh sách quyền/credential cần cấp — người dùng tự cấp.

## Xử lý thất bại

| Tình huống | Xử lý |
|---|---|
| Chưa có API key / token | Dừng, chỉ người dùng tạo và đặt vào biến môi trường hoặc vault. Không xin giá trị key trong chat. |
| Nền tảng là dịch vụ trả phí chưa dùng bao giờ | Đề xuất, chờ người dùng đồng ý. |
| Eval FAIL sau 3 vòng | Dừng, báo ca nào FAIL, đã thử gì. |
| Agent cần quyền ghi rộng (xóa, gửi cho nhiều người, thanh toán) | Thiết kế bước duyệt của người; không bật tự động. |
