# Tan AI Skills

Kho lưu trữ AI Skills phục vụ công việc, học tập và nghiên cứu, được tổ chức theo từng lĩnh vực để tái sử dụng trên nhiều nền tảng AI như Claude Code, Codex và các công cụ hỗ trợ Agent Skills khác.

## Skill hiện có

| Skill | Trạng thái | Mô tả ngắn |
|---|---|---|
| [marketing](skills/marketing/SKILL.md) | Hoàn thiện | Xây dựng chiến lược, nghiên cứu khách hàng/đối thủ, định vị, thông điệp, nội dung đa kênh, kế hoạch chiến dịch, kế hoạch quảng cáo trả phí ở mức chiến lược, KPI và kiểm tra chất lượng/rủi ro truyền thông. |
| [tan-giong-doc-ban-tin](skills/tan-giong-doc-ban-tin/SKILL.md) | Hoàn thiện | Tổng hợp giọng đọc bản tin tiếng Việt từ kịch bản TXT/DOCX bằng VieNeu-TTS: giọng nam/nữ miền Nam dựng sẵn phong cách tin tức, nhân bản giọng người dùng, tự mở rộng chữ viết tắt, xuất WAV 48kHz + MP3. |
| [heygen-avatar](skills/heygen-avatar/SKILL.md), [heygen-video](skills/heygen-video/SKILL.md), [heygen-translate](skills/heygen-translate/SKILL.md) | Hoàn thiện (gói skill nhập từ HeyGen) | Tạo avatar, tạo video có người dẫn (avatar), và dịch/lồng tiếng video qua HeyGen. |
| [remotion-*](skills) (11 skill: best-practices, captions, create, docs, interactivity, maps, markup, multimedia, render, saas, upgrade) | Hoàn thiện (gói skill nhập từ Remotion) | Kiến thức và quy trình tạo/dựng video lập trình bằng framework Remotion. |
| [video-use](skills/video-use/SKILL.md) | Hoàn thiện (gói skill nhập ngoài) | Chỉnh sửa video qua hội thoại: cắt, ghép, chèn phụ đề, chỉnh màu. |

`marketing` và `tan-giong-doc-ban-tin` là hai skill được xây dựng riêng cho repo này (nguồn chuẩn nằm trong `skills/`, đồng bộ sang `.claude/skills/` và `.agents/skills/`). Các skill còn lại (heygen-*, remotion-*, video-use) là gói skill nhập từ bên ngoài, giữ nguyên theo bản gốc — không tự ý sửa mã nguồn bên trong các thư mục đó.

## Khả năng của skill marketing

- Phân tích sản phẩm, dịch vụ, thương hiệu.
- Nghiên cứu thị trường và đối thủ; phân khúc và xây dựng chân dung khách hàng.
- Xây dựng định vị, đề xuất giá trị, điểm khác biệt và thông điệp chính.
- Viết nội dung Facebook, Zalo, TikTok, website/SEO, email; viết tiêu đề, slogan, CTA, kịch bản video ngắn.
- Lập kế hoạch chiến dịch theo ngày/tuần/tháng (cấu trúc 7/30/90 ngày), phễu marketing và hành trình khách hàng.
- Lập lịch nội dung đa kênh (CSV, UTF-8 BOM để mở đúng tiếng Việt trong Excel).
- Lập kế hoạch quảng cáo trả phí (Facebook, Google) **ở mức chiến lược** — mục tiêu, đối tượng, thông điệp, ngân sách dự kiến, KPI, thiết kế A/B test. **Không** tự truy cập tài khoản quảng cáo, không tự chạy quảng cáo, không tự tuyên bố đã triển khai.
- Đề xuất hệ thống KPI (Reach, CTR, CPL, CPA, CAC, ROAS...) kèm định nghĩa, công thức, hạn chế.
- Kiểm tra bản quyền, quyền riêng tư, quy định quảng cáo và rủi ro gây hiểu nhầm trước khi xuất nội dung.
- Ưu tiên bối cảnh Việt Nam: doanh nghiệp nhỏ, hộ kinh doanh, sản phẩm địa phương và nông sản.

Chi tiết đầy đủ nằm trong [skills/marketing/SKILL.md](skills/marketing/SKILL.md) và các file trong `references/`.

## Cấu trúc thư mục thực tế

```text
tan-ai-skills/
├── README.md
└── skills/
    └── marketing/              ← nguồn chuẩn duy nhất, chỉnh sửa tại đây
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml     ← manifest tương thích Codex/Agent Skills
        ├── references/         ← kiến thức chi tiết, đọc khi cần
        ├── assets/              ← mẫu Markdown/CSV có thể sao chép và dùng ngay
        └── scripts/             ← script Python hỗ trợ thao tác thực tế

# Sau khi chạy scripts/sync_skill.py --force, hai bản sao sau được tạo tự động:
.agents/skills/marketing/        ← dành cho Codex và công cụ hỗ trợ Agent Skills
.claude/skills/marketing/        ← dành cho Claude Code
```

`skills/marketing/` là **nguồn chuẩn duy nhất**. Không chỉnh sửa trực tiếp `.agents/skills/marketing` hoặc `.claude/skills/marketing` — hai thư mục này chỉ là bản sao được sinh ra bởi `sync_skill.py` và sẽ bị ghi đè mỗi lần đồng bộ lại.

## Cách sử dụng với Claude Code

1. Chạy đồng bộ ít nhất một lần: `python skills/marketing/scripts/sync_skill.py --force`.
2. Claude Code đọc skill từ `.claude/skills/marketing/`.
3. Trong phiên làm việc, mô tả yêu cầu marketing bằng ngôn ngữ tự nhiên (ví dụ ở phần "Ví dụ câu lệnh" bên dưới) — Claude Code sẽ tự kích hoạt skill khi phù hợp.

## Cách sử dụng với Codex

1. Chạy đồng bộ: `python skills/marketing/scripts/sync_skill.py --force`.
2. Trỏ công cụ Codex/Agent Skills của bạn tới `.agents/skills/marketing/`, dùng `agents/openai.yaml` làm manifest mô tả skill (entrypoint, references, assets, scripts).
3. Với công cụ không tự đọc `.agents/`, có thể trỏ trực tiếp tới `skills/marketing/SKILL.md` làm nguồn chuẩn.

## Cách chạy các script

Yêu cầu Python 3 (không cần cài thư viện ngoài). Mỗi script hỗ trợ `--help`.

```bash
# Tạo brief marketing nhanh từ tham số dòng lệnh
python skills/marketing/scripts/create_campaign_brief.py --brand "Tên thương hiệu" --product "Tên sản phẩm" --goal "Mục tiêu SMART" -o brief.md

# Tạo lịch nội dung CSV cho 30 ngày, 2 kênh
python skills/marketing/scripts/create_content_calendar.py --start-date 2026-08-01 --days 30 --channels "Facebook,TikTok" -o content-calendar.csv

# Rà soát một kế hoạch chiến dịch Markdown đã có
python skills/marketing/scripts/validate_campaign.py duong-dan/ke-hoach.md
```

## Cách kiểm tra và đồng bộ

```bash
# Kiểm tra ba bản (nguồn, .agents, .claude) đã đồng bộ chưa — không ghi gì
python skills/marketing/scripts/sync_skill.py --check

# Thực hiện đồng bộ, ghi đè hai bản sao bằng nội dung nguồn chuẩn
python skills/marketing/scripts/sync_skill.py --force
```

Chạy `sync_skill.py --check` sau mỗi lần chỉnh sửa `skills/marketing/` để biết có cần đồng bộ lại không; chạy `--force` để cập nhật `.agents/` và `.claude/`.

## Ví dụ câu lệnh sử dụng skill

- "Viết 3 bài Facebook giới thiệu mật ong rừng U Minh, giọng điệu gần gũi, có CTA để lại số điện thoại."
- "Lập kế hoạch chiến dịch 30 ngày ra mắt cà phê rang mộc mới cho khách hàng thành thị 25–40 tuổi."
- "Xây dựng chân dung khách hàng cho sản phẩm rau sạch giao tận nhà tại TP.HCM."
- "Lập kế hoạch quảng cáo Facebook ở mức chiến lược cho chương trình khuyến mãi cuối năm, ngân sách 15 triệu VND."
- "Kiểm tra bài viết này có phóng đại công dụng sản phẩm không: [nội dung]."

## Cảnh báo bảo mật

**Không** lưu API key, mật khẩu, token, hoặc file `.env` chứa dữ liệu thật vào bất kỳ đâu trong repo này — kể cả trong brief, kế hoạch chiến dịch, hoặc ví dụ minh họa. Repo này chỉ chứa hướng dẫn, mẫu và script xử lý cục bộ; không có script nào gọi API hoặc tải dữ liệu từ bên ngoài.

## Kế hoạch phát triển tương lai

Các skill sau đang trong kế hoạch, **chưa được tạo**:

- journalism
- agriculture
- office
- AI
- Apps Script
- Python
- prompt engineering
- RAG
- data analysis
- SEO
- social media
- English
- automation
