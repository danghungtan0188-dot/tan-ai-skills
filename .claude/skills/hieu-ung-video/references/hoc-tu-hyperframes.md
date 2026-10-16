# Học từ HyperFrames (HeyGen)

Tóm tắt bằng lời của mình từ repo `heygen-com/hyperframes` (giấy phép Apache-2.0), bản 14/10/2026, bản sao nằm ở `Documents\GitHub\hyperframes`. Không chép nguyên văn. Muốn xem chi tiết thì mở đúng file nguồn ghi trong từng mục.

## 1. Tình trạng trên máy

| Thành phần | Có chưa | Ghi chú |
|---|---|---|
| 13 skill `hyperframes*`, `general-video`, `motion-graphics`, `product-launch-video`, `media-use` | có | cài ở `~\.claude\skills` và `~\.agents\skills`, dùng được cho mọi dự án |
| 8 skill mới trong repo gốc | **chưa cài** | xem bảng dưới |
| Phần mềm render (CLI) | **chưa cài** | gọi bằng `npx hyperframes@latest <lệnh>`, lần đầu tự tải |
| Git LFS | chưa cài | 43 file test lớn trong bản sao báo "khác", không ảnh hưởng việc đọc |

8 skill mới đáng cài, có trong `hyperframes/skills/`:

| Skill | Dùng khi |
|---|---|
| `talking-head-recut` | video phỏng vấn/người nói trước máy → thêm thẻ tiêu đề, lower-third, số liệu, trích dẫn, khung trong khung, khớp theo lời |
| `embedded-captions` | phụ đề thiết kế gắn vào cảnh |
| `slideshow` | chuỗi ảnh thành video trình chiếu |
| `music-to-video` | dựng theo nhịp nhạc: video lời bài hát, trình chiếu, quảng cáo nhịp nhanh |
| `faceless-explainer` | biến bài viết, ghi chú thành video giải thích không cần người, không cần cảnh quay |
| `figma` | đưa thiết kế Figma vào làm chuyển động |
| `remotion-to-hyperframes` | chuyển mẫu Remotion sang HyperFrames, chỉ khi được yêu cầu rõ |
| `pr-to-video` | video giải thích thay đổi code, ít dùng |

## 2. Nguyên tắc dựng (áp được cả cho Remotion trong `do-hoa/`)

HyperFrames dựng video bằng một trang HTML: mỗi phần tử khai báo giờ vào `data-start` và độ dài `data-duration`. Chuyển động nằm trên **một** dòng thời gian GSAP dừng sẵn, để máy render tua tới bất kỳ khung nào. Nguồn: `skills/hyperframes-core/SKILL.md`, `skills/hyperframes-animation/rules-index.md`.

1. **Tua tới đâu cũng đúng.** Khung hình ở giây t chỉ được phụ thuộc vào t. Cấm số ngẫu nhiên không cố định, cấm đồng hồ thật, cấm tải mạng lúc render. Cần ngẫu nhiên thì sinh từ số thứ tự. Trong `do-hoa/` mình đã theo đúng: `random("x1")` trong `TranhGiay`.
2. **Chỉ động vào transform và màu.** Không tween `width/height/top/left`. Muốn phóng to thì dùng `scale`, muốn đổi chỗ thì dùng `translate`, muốn lộ dần thì dùng mặt nạ (`clip-path`).
3. **Ghi rõ trạng thái đầu.** Dùng `fromTo` với giá trị tuyệt đối. Không dùng `+=` tương đối, vì tua ngược sẽ sai.
4. **So le cả nhóm không quá khoảng 0,5 giây.** Số phần tử × khoảng so le ≤ 0,5 giây thì mắt mới đọc thành một nhịp.
5. **Không dùng CSS `transition`** trên phần tử có chuyển động. Nó chạy riêng, không theo dòng thời gian, nên gây nháy hình.
6. **Mỗi cảnh ghép 2–4 "luật chuyển động"**, không nhồi hết vào một cảnh.
7. **Âm thanh phải có `id`.** Thiếu `id` thì render ra không có tiếng.
8. **Duyệt trước, render sau.** `check` không lỗi → chụp `snapshot` vài giây giữa cảnh để xem → `preview` cho người dùng sửa → chỉ `render` khi đã duyệt.

Lệnh (chạy trong thư mục dự án HyperFrames):

```bash
npx hyperframes@latest init <ten-du-an>
npx hyperframes@latest check
npx hyperframes@latest snapshot --at 1.5,4,7
npx hyperframes@latest preview --background
npx hyperframes@latest render
npx hyperframes@latest catalog
npx hyperframes@latest add <ten-mau>
npx hyperframes@latest timeline
```

`check` cần sạch lỗi. Còn lỗi thì phần kiểm bố cục và độ tương phản không chạy, dù nó vẫn báo "0 sample" trông như sạch. `catalog` liệt kê mẫu, `add` cài mẫu vào dự án, `timeline` liệt kê các lớp và clip.

## 3. Kho mẫu (registry): 455 mục

Gồm 210 khối (block, dựng sẵn cả cảnh), 237 thành phần (component, ghép vào cảnh có sẵn) và 8 ví dụ. Nguồn: `registry/blocks/*/registry-item.json`. Những mục hợp với video xã/phường, bản tin, sự kiện:

| Nhu cầu | Tên mẫu |
|---|---|
| Lower-third tên – chức vụ | `lt-clean-bar` `lt-dark-card` `lt-kicker-name` `lt-mask-reveal` `lt-side-rule` `lt-soft-pill` `lt-stack-bars` `lt-bold-block` `lt-accent-underline` `lower-third-bild` |
| Chữ chạy cuối màn hình | `news-ticker` |
| Thẻ tiêu đề | `titlecard-lockup` `titlecard-calm` `hw-write-title` (chữ viết tay) `glass-shard-title` |
| Phụ đề có kiểu | `caption-pill-karaoke` `caption-highlight` `caption-kinetic-slam` `caption-emoji-pop` `caption-editorial-emphasis` `caption-weight-shift` `caption-clip-wipe` |
| Chuyển cảnh | `light-leak` `organic-light-leak-overlay` `flash-through-white` `whip-pan` `sdf-iris` `swirl-vortex` `glitch` `curtain-reveal` `directional-wipe` `fade-through` `beat-freeze-cut` `cinematic-zoom` và các họ `transitions-blur/-push/-radial/-scale/-light/-grid/-destruction/-dissolve` |
| Lộ cảnh (reveal) | `paper-collage-reveal` `ink-bleed-reveal` `iris-reveal` `panel-reveal` `particle-image-reveal` `pull-back-reveal` `soft-blur-in` `scramble-reveal` `svg-stroke-trace` |
| Máy quay ảo | `push-in` `rack-focus` `focus-rack` `camera-shake` `camera-dolly-zoom` `drift-hold` `pan-stations` |
| Số liệu, bản đồ | `animated-bar-chart` `data-chart` `conic-progress-ring` `decline-chart` `mk-progress-stat` `bar-chart-race` `world-map` |
| Mạng xã hội | `tiktok-follow` `instagram-follow` `yt-comment-card` `x-follow-card` |
| Lớp phủ, chú thích | `light-sweep-pass` `vignette` `grain-overlay` `hw-arrow` `hw-callout-circle` `hw-box-label` `yt-circle-pointer` |
| Ảnh băng chuyền | `carousel-circle-*` `carousel-orbit-*` `carousel-path-*` |

Mẫu gắn nhãn `webgpu`/`shader` (khoảng 40 mục) cần card đồ họa. Máy bạn hay sập khi chạy nặng, nên ưu tiên mẫu CSS/GSAP thường.

## 4. Luật chuyển động (49) và kịch bản cảnh (22)

Luật nằm ở `skills/hyperframes-animation/rules/`, mỗi luật là một công thức nhỏ. Mục hay dùng:

- **Chữ:** `kinetic-beat-slam` (chữ đập vào theo nhịp), `gradient-text-sweep` (dải màu chạy qua chữ), `3d-text-depth-layers` (chữ nổi khối), `hacker-flip-3d` (chữ lật giải mã), `asr-keyword-glow` (từ khóa sáng lên đúng lúc nói), `discrete-text-sequence` (gõ chữ có xóa, có dừng).
- **Số:** `counting-dynamic-scale` (số đếm, càng lớn càng phình), `vertical-spring-ticker` (cột số lăn như đồng hồ đo), `stat-bars-and-fills` (cột, vòng tiến độ, sao).
- **Máy quay:** `viewport-change` (zoom/pan cả cảnh), `coordinate-target-zoom` (zoom vào điểm lệch tâm), `multi-phase-camera` (lùi – nhìn – đẩy), `depth-of-field-blur` (đổi tiêu điểm), `3d-camera-flight` (bay qua không gian 3D).
- **Hiệu ứng:** `ambient-glow-bloom`, `particle-burst`, `motion-blur-streak`, `chromatic-glitch`, `spring-pop-entrance`, `waterfall-entry`, `center-outward-expansion`, `depth-scatter-assemble`, `split-tilt-cards`, `svg-path-draw`.
- **Con trỏ, giao diện:** `cursor-click-ripple`, `cursor-drag`, `ai-tracking-box`.

Kịch bản cảnh (`blueprints/`) là cách ghép nhiều luật thành một cảnh trọn vẹn. Hợp với mình: `titlecard-reveal`, `logo-assemble-lockup`, `dataviz-countup`, `kinetic-type-beats`, `grid-card-assemble`, `camera-journey`, `spatial-pan-stations`, `comparison-split`, `ticker-takeover`, `typewriter-reveal`, `video-text-pivot`.

Thao tác dựng cơ bản (cắt, tỉa, đảo thứ tự, đóng băng, đổi tốc độ, zoom, Ken Burns, crop, mặt nạ, hòa tan, giảm nhạc khi có lời, căn tiếng theo hình) có công thức sẵn trong `skills/hyperframes-core/references/creator-editing-recipes.md`.

## 5. Hiệu ứng thấy trong video mẫu → mẫu HyperFrames có sẵn

Nối với danh sách "ghi lại để dựng sau" trong [ky-thuat-tu-video-mau.md](ky-thuat-tu-video-mau.md):

| Thấy trong video mẫu | Dùng mẫu HyperFrames |
|---|---|
| số năm lăn 2025 → 2026 | luật `vertical-spring-ticker` |
| chữ hiện ngẫu nhiên từng chữ cái, nhãn góc gõ lộn xộn | `scramble-reveal`, luật `hacker-flip-3d` |
| vỡ khối pixel, glitch | `glitch`, họ `transitions-destruction`, luật `chromatic-glitch` |
| xoáy ở cảnh flycam | `swirl-vortex` |
| vòng tròn/đồng hồ cát khép | `sdf-iris`, `iris-reveal` |
| tường ảnh nhỏ bay khắp khung | `mk-clone-wall-transition`, kịch bản `grid-card-assemble` |
| trái tim hạt vàng | gần nhất: luật `particle-burst` (phải tự vẽ đường trái tim) |
| cửa sổ nhỏ nở ra toàn khung | `card-resize`, luật `anchored-layout-expand` |
| nút Follow có con trỏ bấm | `tiktok-follow`, luật `cursor-click-ripple` |
| vệt sáng, lóe trắng | `light-leak`, `light-sweep-pass`, `flash-through-white` |
| phóng sát theo nhịp | `push-in`, mục "Zoom / punch" trong `creator-editing-recipes.md` |
| tranh giấy, ảnh rải chồng | `paper-collage-reveal` (mình đã có `TranhGiay`, `AnhBayVao` bằng Remotion) |
| khung tách dải lộ cảnh | `curtain-reveal`, `panel-reveal` |

## 6. Chọn công cụ nào

| Việc | Dùng |
|---|---|
| cắt ghép, màu, chuyển cảnh `xfade`, phụ đề, nén | ffmpeg (các file khác trong `references/`) |
| đồ họa ATT NEWS đã có mẫu, gọi từ `tan_studio` | Remotion trong `do-hoa/` |
| cần một hiệu ứng có sẵn trong registry, hoặc dựng cả video chuyển động từ ý tưởng/bài viết | HyperFrames: `npx hyperframes@latest add <mẫu>` |
| quảng cáo HeyGen có người dẫn (trả phí) | skill `heygen-video`, phải hỏi bạn từng lần |

**Chưa kiểm:** mình mới đọc repo, chưa cài CLI nên chưa render thử mẫu HyperFrames nào trên máy này. Lần đầu dùng, chạy `npx hyperframes@latest doctor` trước để xem máy đủ điều kiện chưa.
