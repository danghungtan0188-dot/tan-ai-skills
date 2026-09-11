# Catalog chức năng kiểu CapCut — trạng thái thật trên máy này

Tên là preset nội bộ; **không** tương thích project, template hay hiệu ứng độc quyền của CapCut.
Trạng thái kiểm ngày 2026-09-11 bằng `ffmpeg -filters` và import Python:

✅ chạy ngay · 🔧 có công cụ, cần ghép lệnh/viết bước · 📦 cần cài thêm · 🤖 cần mô hình AI chưa có · ⛔ không làm
Có sẵn: vidstab, deshake, lut3d, chromakey/colorkey, afftdn, arnndn (thiếu file mô hình), dialoguenhance,
reverse, minterpolate, tmix, rubberband, sidechaincompress, scdet, perspective, zoompan, xfade, rgbashift ·
Python: OpenCV 5 (tracker MIL, dò mặt Haar), librosa, faster-whisper.
**Chưa cài:** mediapipe, rembg, demucs, scenedetect, OpenCV contrib (CSRT/KCF).

Mọi chức năng **đổi thời lượng** (cắt, tốc độ, freeze, reverse) chỉ dùng khi `cut_authorized=true`.

| Nhóm | Chức năng | Cách làm | Trạng thái |
|---|---|---|---|
| Cắt ghép | split / trim | `-ss/-to` từng clip + concat; `render_project.py` | ✅ |
| | ripple delete | bỏ đoạn + concat; **phải tính lại mốc phụ đề** | 🔧 |
| | multicam | đồng bộ theo âm thanh (librosa), chọn góc từng đoạn | 🔧 |
| | transcript editing | mốc từ `build_bilingual.py transcribe` → danh sách cắt theo từ; chừa 30–200 ms, không cắt giữa từ | 🔧 |
| Tốc độ | speed ramp | `setpts` + `atempo` theo đoạn (`presets.speed_video`) | ✅ |
| | slow motion | `setpts`; mượt: `minterpolate=fps=60:mi_mode=mci` (nặng) | ✅ |
| | freeze | `tpad=stop_mode=clone` | ✅ |
| | reverse | `reverse` / `areverse` — chỉ clip ngắn, nạp cả vào RAM | ✅ |
| | beat cut | `librosa.beat.beat_track` → mốc cắt | 🔧 |
| Khung hình | auto-reframe 16:9→9:16 | tâm mặt (Haar) theo cảnh → crop, làm mượt | 🔧 |
| | stabilization | `vidstabdetect` + `vidstabtransform`, **không xuyên điểm cắt** | ✅ |
| | camera push | `zoompan` hoặc scale+crop theo keyframe | ✅ |
| | 3D photo zoom | cần mô hình độ sâu (MiDaS); tạm dùng Ken Burns | 🤖 |
| Tách nền | chroma key | `chromakey`/`colorkey` + khử lem màu; QA viền | ✅ |
| | smart cutout | rembg / mediapipe | 📦 |
| | mask | `alphamerge` với mặt nạ PNG (PIL); mặt nạ động = chuỗi PNG | ✅ |
| | tracking | `callouts.py track` (MIL) + `sendcmd` | ✅ |
| | screen replacement | `perspective` với 4 góc đo pixel (như thẻ TV ATT NEWS); màn hình di chuyển cần bám góc | ✅ / 🔧 |
| Chữ & đồ hoạ | caption karaoke | thẻ ASS `\k` từ mốc từ; hoặc `remotion-captions` | 🔧 |
| | title, banner, lower-third, sticker | `broadcast_kit.py`, `make_lower_thirds_ass.py`, `presets.sticker_overlay` | ✅ |
| | evidence card | `quote_card` / `fact_card` / `map_card` + **`source_strap` bắt buộc** | ✅ |
| Hiệu ứng | transition | `xfade` (fade, dissolve, wipe, slide, circle…) | ✅ |
| | glitch, RGB split | `rgbashift` (`presets.glitch_rgb`) | ✅ |
| | film burn | overlay video light-leak có quyền; tạm: `presets.light_leak` | 🔧 |
| | motion blur | `tmix=frames=3` hoặc `minterpolate` | ✅ |
| Màu | color matching | so trung bình/độ lệch từng kênh với cảnh mẫu → `colorbalance`/`eq` | 🔧 |
| | LUT | `lut3d=file.cube` (file LUT phải có quyền) | ✅ |
| | relighting | mô hình AI | 🤖 |
| | background blur | cần mặt nạ người (📦); tạm: làm mờ ngoài một elip cố định | 🔧 |
| | retouch | làm mịn nhẹ vùng mặt qua mặt nạ; bản tin giữ tối thiểu | 🔧 |
| Âm thanh | vocal isolation | demucs | 📦 |
| | denoise | `afftdn`; `arnndn` cần file `.rnnn` | ✅ / 📦 |
| | de-reverb | không có filter chuyên; `dialoguenhance` + highpass/lowpass chỉ đỡ một phần | ⛔ / 🤖 |
| | ducking | `sidechaincompress` (`presets.duck_music`) | ✅ |
| | beat detection | librosa | ✅ |
| Riêng tư & xuất | privacy blur / redaction | `boxblur` vùng cố định; vùng động theo tracker; mặt tự dò bằng Haar (có thể sót mặt nghiêng — xem lại) | ✅ / 🔧 |
| | xuất hàng loạt 16:9 / 9:16 / 1:1 | dựng lại đồ hoạ theo `--aspect` của `broadcast_kit.py`; **không crop mù** | 🔧 |
| AI hỗ trợ | gợi ý B-roll | câu trong transcript → từ khoá → tìm trong tư liệu **của người dùng**; không sinh cảnh giả cho tin | 🔧 |
| | object cleanup | inpainting AI; `delogo` chỉ cho lớp của chính mình, **không xoá watermark** | 🤖 / ⛔ |
| | generative extend | ⛔ với tin tức — bịa thêm hình ảnh không có thật | ⛔ |
| | highlight selection | `scdet` + độ ồn (`ebur128`) + từ khoá transcript → đề xuất, người dùng duyệt | 🔧 |
