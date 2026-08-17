# Rule bảo mật

Được thực thi tự động bởi `.claude/hooks/guard_secrets.py` và `.claude/hooks/guard_bash.py`.

## 1. Secret

**Không bao giờ** ghi vào bất kỳ file nào trong repo:

| Loại | Ví dụ tiền tố |
|---|---|
| Anthropic API key | `sk-ant-…` |
| OpenAI-style key | `sk-…` |
| Google API key | `AIza…` |
| GitHub token | `ghp_…`, `gho_…`, `github_pat_…` |
| AWS access key | `AKIA…` |
| Slack token | `xoxb-…` |
| Private key | `-----BEGIN … PRIVATE KEY-----` |
| Supabase service_role | JWT có claim `service_role` |

Quy tắc:

- File `.env` thật: **không tạo, không ghi, không commit**. Chỉ được tạo `.env.example` với giá trị placeholder (`<your-key>`, `xxx`, `changeme`).
- Trong code, đọc secret qua `os.environ` / `process.env`, không hardcode.
- Không in secret ra log, không đưa secret vào tên file, URL, query string, hay commit message.
- Không tự tạo Service Role key. Nếu thao tác cần nó → dừng, báo người dùng tự làm.

Hook `guard_secrets.py` chặn thao tác Write/Edit vi phạm và trả lý do cho Claude. Nếu bị chặn: **sửa nội dung**, không tìm cách lách hook.

## 2. Lệnh bị CHẶN HẲN

Hook `guard_bash.py` chặn (exit 2), không có cách nào bỏ qua trong phiên:

- `rm -rf /`, `rm -rf ~`, `rm -rf *` ở thư mục gốc
- `DROP DATABASE` / `DROP SCHEMA` / `TRUNCATE TABLE`
- `DELETE FROM <bảng>` không có `WHERE`
- `DISABLE ROW LEVEL SECURITY`
- `supabase db reset`
- `curl … | sh`, `iwr … | iex` (tải về rồi chạy)
- `git push --force`

Cần thật thì báo người dùng tự chạy tay.

## 3. Lệnh cần NGƯỜI DÙNG XÁC NHẬN

Hook trả `permissionDecision: ask` — Claude Code sẽ hỏi bạn:

- `git push`, `gh pr create`, `gh release create`
- `npm/yarn/pnpm publish`, `docker push`
- `vercel --prod`, `netlify deploy --prod`, `firebase deploy`, `wrangler deploy`
- `supabase db push`, `supabase link`, `supabase functions deploy`
- `git reset --hard`, `git clean -fd`

## 4. Supabase

Không tự ý: reset database, xóa dữ liệu, tắt RLS, tạo Service Role key, bypass policy.

Được làm: viết migration mới (không sửa migration đã apply), viết RLS policy, viết query, đọc schema.

Mọi bảng chứa dữ liệu người dùng **phải** bật RLS. Bảng mới không có policy = lỗi bảo mật, báo trong review.

## 5. Rà soát trước khi giao

Agent `security-reviewer` phải kiểm: secret rò rỉ, `.env` bị tracked, endpoint thiếu auth, thiếu kiểm tra quyền, SQL/command injection, RLS thiếu, dữ liệu nhạy cảm trong log.
