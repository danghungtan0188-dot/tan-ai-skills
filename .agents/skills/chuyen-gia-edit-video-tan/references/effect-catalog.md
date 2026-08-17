# Danh mục preset code

Tên dưới đây là preset nội bộ, không phải tên chính thức của CapCut.

## Text

`title_clean`, `lower_third`, `news_banner`, `gold_impact_title`, `typewriter`, `fade_up`, `pop`, `karaoke_word`, `countdown`.

## Stickers

`logo`, `social_icon`, `emoji`, `callout`, `animated_overlay`; nhận `path`, `x`, `y`, `width`, `opacity`, `start`, `end`, `fade`, `loop`, `rotation`.

## Effects

| Preset | Tái tạo | Dùng |
|---|---|---|
| `flash_white` | overlay trắng 2–6 frame | beat/cao trào |
| `light_leak` | gradient/video alpha, blend screen | mở cụm cảnh |
| `zoom_blur` | scale nhanh + blur/zoompan gần đúng | transition ngắn |
| `shake` | crop lớn rồi dịch x/y | impact ≤0,4 s |
| `glitch_rgb` | tách RGB và offset | montage ≤0,25 s |
| `film_grain` | noise thấp + vignette | cinematic |
| `freeze` | `tpad=stop_mode=clone` | nhấn nhân vật |
| `speed_ramp` | chia đoạn + `setpts`/`atempo` | chuyển động rõ |
| `ken_burns` | `zoompan` | ảnh tĩnh |

## Transitions

Hỗ trợ `cut`, `fade`, `dissolve`, `dip_black`, `dip_white`, `wipe_left/right/up/down`, `slide_left/right/up/down`, `circle_open/close`, `radial`, `zoom`, `blur`, `whip_left/right`, `flash_burst`. Preset tổng hợp tự hạ cấp về xfade tương thích nếu cần.

## Captions

`sentence_box`, `word_highlight`, `news_subtitle`, `speaker_label`. Với 16:9, caption ở vùng dưới 8–12% nhưng nằm trên ticker; 9:16 tránh vùng UI nền tảng.

## Filters

`natural`, `vibrant`, `cinematic`, `warm`, `cool`, `bw`, `vintage`, `news_clean`. Chỉnh theo cảnh và giảm strength nếu da đỏ/cháy.

## Adjustment

`brightness`, `contrast`, `saturation`, `gamma`, `temperature`, `tint`, `sharpen`, `denoise`, `vignette`, `stabilize`, `crop`, `rotate`, `speed`, `volume`, `ducking`, `loudness_normalize`.

Stabilization dùng hai lượt `vidstabdetect`/`vidstabtransform` nếu FFmpeg hỗ trợ; nếu không, báo rõ.
