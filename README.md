# Tan AI Skills

Kho lưu trữ AI Skills phục vụ công việc, học tập và nghiên cứu, được tổ chức theo từng lĩnh vực để tái sử dụng trên nhiều nền tảng AI như Claude Code, Codex và các công cụ hỗ trợ Agent Skills khác.

## Skill hiện có

| Skill | Trạng thái | Mô tả ngắn |
|---|---|---|
| [marketing](skills/marketing/SKILL.md) | Hoàn thiện | Xây dựng chiến lược, nghiên cứu khách hàng/đối thủ, định vị, thông điệp, nội dung đa kênh, kế hoạch chiến dịch, kế hoạch quảng cáo trả phí ở mức chiến lược, KPI và kiểm tra chất lượng/rủi ro truyền thông. |
| [tan-giong-doc-ban-tin](skills/tan-giong-doc-ban-tin/SKILL.md) | Hoàn thiện | Tổng hợp giọng đọc bản tin tiếng Việt từ kịch bản TXT/DOCX bằng VieNeu-TTS: giọng nam/nữ miền Nam dựng sẵn phong cách tin tức, nhân bản giọng người dùng, tự mở rộng chữ viết tắt, xuất WAV 48kHz + MP3. |
| [dung-video-su-kien](skills/dung-video-su-kien/SKILL.md) | Hoàn thiện | Công thức dựng video tổng kết sự kiện/hội thi kiểu Việt Nam: title card banner đỏ-vàng, overlay gameshow (đếm ngược + trắc nghiệm), transition hiệu ứng lửa/xé, đoạn hero-intro nhân vật cuối video, tông màu ánh sáng theo phân đoạn. Đúc kết từ phân tích thực tế 1 video mẫu (Đồng Tháp 24h). Là bản đặc tả phong cách, không tự render — phối hợp với video-use/HyperFrames/remotion-* để dựng thật. |
| [bien-tap-video](skills/bien-tap-video/SKILL.md) | Hoàn thiện | Skill biên tập video thông minh: đưa vào 1 video, tự phân tích metadata + khung hình (script `phan_tich_video.py`), nhận diện chủ đề (sự kiện, quảng cáo, vlog du lịch, phỏng vấn/tutorial, đám cưới/kỷ niệm, thể thao, ẩm thực, mạng xã hội ngắn), rồi áp dụng đúng phong cách dựng theo bộ nguyên tắc chất lượng chuyên nghiệp dùng chung. Là lớp điều phối — phối hợp với `dung-video-su-kien`, video-use, HyperFrames, remotion-* để dựng thật. |
| [video-thuyet-minh](skills/video-thuyet-minh/SKILL.md) | Hoàn thiện | Quy trình sản xuất video có lời thuyết minh/bản tin tiếng Việt từ đầu đến cuối: nối `tan-giong-doc-ban-tin` (giọng đọc) với `bien-tap-video`/`dung-video-su-kien` (hình ảnh) và `video-use` (thực thi ghép), xử lý phần đồng bộ lời đọc với hình ảnh và trộn âm thanh (ducking nhạc nền dưới giọng đọc) mà 3 skill kia không tự làm. Là lớp điều phối toàn quy trình, không tự tổng hợp giọng hay tự render. |
| [hieu-ung-video](skills/hieu-ung-video/SKILL.md) | Hoàn thiện | Thư viện công thức hiệu ứng kiểu CapCut: chuyển cảnh (xfade), chữ/hoạt hình chữ, bộ lọc màu, chuyển động camera (Ken Burns/speed ramp/freeze), sticker/icon, hiệu chỉnh hình ảnh — mỗi mục có lệnh ffmpeg thực thi được ngay, kèm cảnh báo rủi ro đã gặp thật (stabilize xuyên cắt cảnh gây vỡ hình, seek-artifact khi kiểm tra khung hình). Được các skill dựng video khác gọi tới khi cần 1 hiệu ứng cụ thể. |
| [video-san-pham](skills/video-san-pham/SKILL.md) | Hoàn thiện | Dựng **từng video sản phẩm** khi được yêu cầu, từ 1 dòng Excel/CSV sản phẩm + ảnh: AI viết kịch bản đúng dữ liệu thật → `tan-giong-doc-ban-tin` tạo giọng đọc → ASR cấp từ đồng bộ phụ đề (vai trò Whisper) → dựng cảnh có chuyển động qua Remotion/HyperFrames → ghép và xuất đúng định dạng TikTok/Facebook qua `video-use` (vai trò FFmpeg). Có "nguyên tắc cứng" (không bịa dữ liệu, phụ đề burn cuối cùng, kiểm rủi ro nội dung trước khi xuất) và bước tự kiểm tra đầu ra bằng `ffprobe` (script `kiem_tra_dau_ra.py`), tối đa 3 lần tự sửa trước khi báo người dùng. Không tự động quét/xuất hàng loạt cả file Excel — chỉ xử lý sản phẩm được chỉ định trong từng yêu cầu. |
| [chuyen-gia-edit-video-tan](skills/chuyen-gia-edit-video-tan/SKILL.md) | Hoàn thiện | Phân tích video mẫu và dựng video chuyên nghiệp bằng code với bộ chức năng tương đương CapCut: Text, Stickers, Effects, Transitions, Captions, Filters, Adjustment. Dùng cho bản tin, sự kiện, MC, phóng sự, Facebook, Zalo, Reels, Shorts. Có `references/effect-catalog.md` liệt kê preset và cách tái tạo bằng ffmpeg. |
| [bien-tap-video-thong-minh-song-ngu-tan](skills/bien-tap-video-thong-minh-song-ngu-tan/SKILL.md) | Hoàn thiện | Phân tích nội dung/hình ảnh/lời nói/nhịp để tự chọn chiến lược biên tập, kèm phụ đề song ngữ tiếng Anh dòng trên và tiếng Việt dòng dưới. Có mục "Bảy lớp dựng" mô tả đầy đủ Text, Stickers, Effects, Transitions, Captions, Filters, Adjustment kèm ràng buộc an toàn từng lớp. Mặc định `cut_authorized=false` — không tự cắt khi chưa được phép. |
| [phat-trien-app](skills/phat-trien-app/SKILL.md) | Hoàn thiện | Quy trình phát triển app/website: dò kiến trúc dự án trước khi sửa, quy ước frontend/backend/Supabase, và chuỗi validation thật (lint → typecheck → test → build → security). Là bộ quy ước dùng chung cho các agent app-planner, app-builder, code-reviewer, app-tester, security-reviewer. |
| [heygen-avatar](skills/heygen-avatar/SKILL.md), [heygen-video](skills/heygen-video/SKILL.md), [heygen-translate](skills/heygen-translate/SKILL.md) | Hoàn thiện (gói skill nhập từ HeyGen) | Tạo avatar, tạo video có người dẫn (avatar), và dịch/lồng tiếng video qua HeyGen. |
| [remotion-*](skills) (11 skill: best-practices, captions, create, docs, interactivity, maps, markup, multimedia, render, saas, upgrade) | Hoàn thiện (gói skill nhập từ Remotion) | Kiến thức và quy trình tạo/dựng video lập trình bằng framework Remotion. |
| [video-use](skills/video-use/SKILL.md) | Hoàn thiện (gói skill nhập ngoài) | Chỉnh sửa video qua hội thoại: cắt, ghép, chèn phụ đề, chỉnh màu. |

`marketing`, `tan-giong-doc-ban-tin`, `dung-video-su-kien`, `bien-tap-video`, `video-thuyet-minh`, `video-san-pham`, `hieu-ung-video`, `chuyen-gia-edit-video-tan`, `bien-tap-video-thong-minh-song-ngu-tan` và `phat-trien-app` là mười skill được xây dựng riêng cho repo này (nguồn chuẩn nằm trong `skills/`, đồng bộ sang `.claude/skills/` và `.agents/skills/`). Các skill còn lại (heygen-*, remotion-*, video-use) là gói skill nhập từ bên ngoài, giữ nguyên theo bản gốc — không tự ý sửa mã nguồn bên trong các thư mục đó.

## Kiến trúc hệ thống

Repo này không chỉ là thư viện skill — nó là một hệ thống Claude Code có workflow chạy thật:

```text
COMMAND → AGENT → SKILL → RULES → IMPLEMENTATION → HOOK → TEST/REVIEW → OUTPUT
```

| Thành phần | Vị trí | Số lượng |
|---|---|---|
| Agents | `.claude/agents/` | 9 |
| Commands | `.claude/commands/` | 9 |
| Hooks | `.claude/hooks/` + `.claude/settings.json` | 3 |
| Skills | `skills/` (nguồn chuẩn) | 25 |
| Rules | `rules/` | 4 |
| Data contracts | `data-contracts/` | 2 schema |
| Tests | `tests/` | 66 test |

**Command gọi được:**

```text
APP:   /build-feature   /fix   /review   /test   /security-check
VIDEO: /video-news      /edit-video      /review-video
REPO:  /sync-skills
```

Chi tiết đầy đủ: [ARCHITECTURE.md](ARCHITECTURE.md). Bản đồ ngắn cho phiên Claude Code: [CLAUDE.md](CLAUDE.md).

**Kiểm tra hệ thống:**

```bash
python -m unittest discover -s tests    # test kiến trúc + hook + data contract
python scripts/sync_skills.py --check   # 3 bản skill đã khớp chưa
```

## Gọi đúng skill video (bảng định tuyến)

5 skill video trong repo này chia lớp rõ ràng: **skill điều phối** (người dùng gọi trực tiếp) → tự động gọi **skill module/thực thi** bên dưới. Dùng bảng sau để không gọi nhầm:

| Tình huống của bạn | Gọi skill này | KHÔNG gọi skill này |
|---|---|---|
| Có sẵn 1 file video (quay/tải về), muốn edit/dựng lại, chưa rõ chủ đề | `bien-tap-video` | `video-san-pham` (không có Excel/ảnh sản phẩm) |
| Đã biết chắc là video sự kiện/hội nghị/hội thi kiểu Việt Nam, muốn xem riêng công thức phong cách | `dung-video-su-kien` | Bình thường không cần gọi tay — `bien-tap-video` tự route sang khi nhận diện đúng chủ đề |
| Có dữ liệu Excel/CSV + ảnh sản phẩm, muốn ra video quảng cáo TikTok/Facebook | `video-san-pham` | `video-thuyet-minh` (không có kịch bản tự do), `bien-tap-video` (không có video quay sẵn) |
| Có kịch bản/bản tin văn bản tự do, muốn đọc thành giọng rồi ghép vào video (có sẵn hoặc cần dựng) | `video-thuyet-minh` | `video-san-pham` (không phải sản phẩm thương mại theo khung HOOK→GIÁ→CTA) |
| Chỉ cần file giọng đọc, không ghép vào video nào | `tan-giong-doc-ban-tin` | `video-thuyet-minh` (thừa bước, không cần) |
| Cần 1 hiệu ứng cụ thể (chuyển cảnh, chữ động, filter, zoom/pan, sticker...) trên 1 clip, hoặc muốn tái tạo hiệu ứng thấy trong video tham khảo | `hieu-ung-video` | Không cần gọi tay nếu đang dùng `bien-tap-video`/`video-thuyet-minh`/`video-san-pham` — các skill đó tự gọi khi cần |
| Cần avatar/người dẫn AI xuất hiện nói chuyện trong video | `heygen-avatar` rồi `heygen-video` | — |
| Cần dịch/lồng tiếng 1 video đã có sang ngôn ngữ khác | `heygen-translate` | — |

**Quy tắc chung:** nếu không chắc, ưu tiên mô tả tình huống thật (có gì trong tay: video thô? Excel? kịch bản?) thay vì tự chọn tên skill — mô tả đúng sẽ tự kích hoạt đúng skill.

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
