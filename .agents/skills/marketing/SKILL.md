---
name: marketing
description: Hỗ trợ xây dựng chiến lược, nghiên cứu khách hàng/đối thủ, định vị, thông điệp, nội dung đa kênh (Facebook, Zalo, TikTok, website, email, SEO), kế hoạch chiến dịch theo ngày/tuần/tháng, kế hoạch quảng cáo trả phí ở mức chiến lược (không tự chạy quảng cáo), lịch nội dung, KPI và kiểm tra chất lượng/rủi ro truyền thông. Ưu tiên bối cảnh Việt Nam, doanh nghiệp nhỏ, hộ kinh doanh, sản phẩm địa phương và nông sản. Kích hoạt khi người dùng cần nghiên cứu thị trường, xây dựng chân dung khách hàng, viết nội dung quảng bá, lập brief/kế hoạch marketing, lập lịch đăng, viết kịch bản video ngắn, slogan, CTA, hoặc đánh giá/kiểm tra một chiến dịch. Đầu ra gồm brief, chân dung khách hàng, kế hoạch chiến dịch, lịch nội dung, nội dung sẵn sàng đăng, kịch bản video, bảng KPI.
---

# Marketing

## Phạm vi

Hỗ trợ: phân tích sản phẩm/thương hiệu, nghiên cứu thị trường và đối thủ, phân khúc và chân dung khách hàng, định vị và đề xuất giá trị, thông điệp và CTA, lập kế hoạch chiến dịch (7/30/90 ngày), phễu và hành trình khách hàng, lịch nội dung đa kênh, nội dung Facebook/Zalo/TikTok/website/email/SEO, kịch bản video ngắn, kế hoạch quảng cáo trả phí **ở mức chiến lược**, hệ thống KPI, kiểm tra chất lượng và rủi ro truyền thông.

Không làm: không tự truy cập hoặc thay đổi tài khoản quảng cáo; không tự đăng bài hoặc chạy quảng cáo; không tuyên bố đã triển khai khi mới chỉ lập kế hoạch; không bịa số liệu thị trường, nguồn, đối thủ, nhận xét khách hàng hoặc kết quả chiến dịch; không cam kết tuyệt đối về doanh thu, hiệu quả hoặc công dụng sản phẩm.

## Quy trình cốt lõi

1. **Tiếp nhận và chuẩn hóa brief.** Nếu người dùng chưa cung cấp đủ, dùng khung ở [assets/marketing-brief-template.md](assets/marketing-brief-template.md); điền phần đã có, đánh dấu phần còn thiếu. Có thể chạy `scripts/create_campaign_brief.py` khi thông tin đến rời rạc qua tham số dòng lệnh.
2. **Xác định mục tiêu** theo chuẩn SMART.
3. **Phân tích khách hàng và bối cảnh.** Đọc [references/customer-research.md](references/customer-research.md) khi cần nghiên cứu thị trường, đối thủ, phân khúc hoặc chân dung khách hàng. Trình bày chân dung khách hàng theo [assets/customer-persona-template.md](assets/customer-persona-template.md).
4. **Xây dựng định vị và thông điệp.** Đọc [references/positioning-messaging.md](references/positioning-messaging.md) khi cần định vị, USP, slogan, tiêu đề, CTA hoặc áp dụng AIDA/PAS/FAB.
5. **Chọn chiến lược và kênh.** Đọc [references/content-channels.md](references/content-channels.md) khi viết nội dung cho một kênh cụ thể. Đọc [references/paid-advertising.md](references/paid-advertising.md) khi lập kế hoạch quảng cáo trả phí — chỉ ở mức chiến lược, không thao tác tài khoản thật.
6. **Xây dựng nội dung và lịch triển khai.** Dùng [assets/campaign-plan-template.md](assets/campaign-plan-template.md) cho kế hoạch chiến dịch; tham khảo [references/campaign-planning.md](references/campaign-planning.md) cho phễu, hành trình khách hàng, cấu trúc 7/30/90 ngày. Dùng [assets/content-calendar-template.csv](assets/content-calendar-template.csv) hoặc chạy `scripts/create_content_calendar.py` khi cần lịch nhiều ngày/nhiều kênh. Dùng [assets/short-video-script-template.md](assets/short-video-script-template.md) cho kịch bản TikTok/video ngắn.
7. **Xác định KPI.** Đọc [references/marketing-kpis.md](references/marketing-kpis.md) để chọn đúng định nghĩa, công thức, đơn vị. Không tự đưa "mức chuẩn ngành" nếu không có nguồn.
8. **Kiểm tra chất lượng và rủi ro** trước khi xuất. Đọc [references/compliance-quality.md](references/compliance-quality.md) và rà theo [assets/content-review-checklist.md](assets/content-review-checklist.md). Nếu đã có file kế hoạch Markdown, có thể chạy `scripts/validate_campaign.py` để rà soát tự động các mục bắt buộc.
9. **Xuất kết quả có thể sử dụng ngay** theo định dạng bên dưới.

## Khi nào chạy script

- `scripts/create_campaign_brief.py` — sinh nhanh brief Markdown từ tham số dòng lệnh (sản phẩm, mục tiêu, khách hàng, kênh, thời gian, ngân sách).
- `scripts/create_content_calendar.py` — sinh lịch nội dung CSV nhiều ngày/nhiều kênh thay vì soạn tay.
- `scripts/validate_campaign.py` — rà soát một kế hoạch chiến dịch Markdown đã có, phát hiện mục còn thiếu trước khi giao cho người dùng.
- `scripts/sync_skill.py` — chỉ dùng khi bảo trì skill (đồng bộ `skills/marketing` sang `.agents/skills/marketing` và `.claude/skills/marketing`). Không dùng trong công việc marketing thông thường.

Mỗi script hỗ trợ `--help`. Chạy bằng Python 3, không cần thư viện ngoài.

## Xử lý dữ liệu thiếu và giả định

- Thiếu thông tin **không** làm thay đổi đáng kể chiến lược (ví dụ giọng điệu cụ thể, khung giờ đăng): tự đưa giả định hợp lý, ghi rõ trong mục "Giả định" của đầu ra.
- Thiếu thông tin **có thể** thay đổi đáng kể kết quả (ví dụ ngân sách, khách hàng mục tiêu, mục tiêu chiến dịch): hỏi lại người dùng trước khi tiếp tục.
- Luôn phân biệt trong đầu ra: dữ kiện người dùng cung cấp / dữ kiện đã xác minh từ nguồn / giả định / đề xuất AI.
- Khi yêu cầu phụ thuộc thông tin hiện tại (giá, xu hướng, đối thủ, quy định quảng cáo) và có công cụ tra cứu, hãy tra cứu nguồn đáng tin cậy và trích dẫn; nếu không có công cụ, nói rõ đây là giả định hoặc nhận định định tính, không trình bày như sự thật.

## Kiểm tra chất lượng trước khi xuất

Dùng đầy đủ [assets/content-review-checklist.md](assets/content-review-checklist.md); tối thiểu xác nhận: đúng mục tiêu, đúng khách hàng mục tiêu, thông điệp rõ ràng, phù hợp kênh đăng, CTA rõ ràng, không có thông tin chưa kiểm chứng trình bày như sự thật, không phóng đại hoặc gây hiểu nhầm, tôn trọng bản quyền và quyền riêng tư.

## Định dạng đầu ra

- **Nội dung đơn lẻ** (bài đăng, email, kịch bản): bản hoàn chỉnh sẵn sàng dùng trước, kèm 2–3 phương án tiêu đề/CTA khi phù hợp.
- **Kế hoạch chiến dịch**: theo [assets/campaign-plan-template.md](assets/campaign-plan-template.md), trình bày bảng khi có nhiều kênh/mốc thời gian.
- **Lịch nội dung**: file CSV UTF-8 BOM (Excel mở đúng tiếng Việt), theo [assets/content-calendar-template.csv](assets/content-calendar-template.csv) hoặc output của script.
- **Kế hoạch quảng cáo trả phí**: ghi rõ đây là kế hoạch chiến lược, không phải chiến dịch đã chạy; không kèm số liệu hiệu suất thực tế.
- Luôn kèm mục "Giả định" nếu có giả định được sử dụng trong đầu ra.
