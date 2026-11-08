# Chuyển cảnh GPU kiểu CapCut (gpufx)

154 chuyển cảnh viết lại bằng shader, mô phỏng chuyển cảnh CapCut cùng tên, từ repo [tqk2811/FFmpegGpuFilter](https://github.com/tqk2811/FFmpegGpuFilter) (MIT). Đây là bản viết lại, không phải tài nguyên gốc của CapCut. Ảnh đi kèm 7 hiệu ứng có giấy phép riêng (CC0, OFL, phạm vi công cộng), ghi trong thư mục `textures/` của từng hiệu ứng.

**Chưa chạy trên máy này.** Tác giả chỉ thử trên Windows với NVIDIA RTX 4060 và Intel UHD (card của máy này là Intel UHD). Lần đầu dùng: thử một chuyển cảnh giữa 2 clip vài giây, xem máy có nóng không rồi mới dùng thật.

## Ở đâu, cần gì

- Mã nguồn và gói hiệu ứng: `D:\GitHub\FFmpegGpuFilter\packages\gpufx\capcut\<tên>\` (chỉ có trên máy này, commit `1e823d1`).
- Cần bản FFmpeg có bộ lọc `gpufx`: tải `ffmpeg-gpufx-win64.zip` ở trang Releases của repo hoặc tự build. Phải hỏi người dùng trước khi tải, để ở thư mục riêng, **không thay FFmpeg đang dùng**. Gói `.zip` của từng hiệu ứng nằm trong `gpufx-packages.zip` cùng trang.
- Mọi hiệu ứng đều là chuyển cảnh: 2 đầu vào cùng kích thước, tham số `progress` chạy từ 0 đến 1. Cột "Dài" là độ dài mặc định trong CapCut.

## Lệnh mẫu (Intel trên Windows)

Chuyển cảnh 0,8 giây bắt đầu ở giây 3 giữa hai đoạn cùng kích thước. Intel trên Windows phải dùng `gpufx_upload`/`gpufx_download` thay cho `hwupload`/`hwdownload`; cú pháp chính xác lấy theo README của repo trước khi chạy:

```bash
<ffmpeg-gpufx> -init_hw_device vulkan=vk:0,disable_multiplane=1 -filter_hw_device vk -i a.mp4 -i b.mp4 -filter_complex "[0][1]gpufx=graph='film-wipe.zip=progress=clip((t-3)/0.8\,0\,1)',gpufx_download,format=yuv420p" -c:v libx264 -preset faster ra.mp4
```

Video marketing nhịp nhanh: chỉ dùng ở chỗ đổi ý lớn, không đặt sát câu nói đang có đồ họa. Bản tin, phim tài liệu: tránh nhóm Glitch, Lễ và Tuyết.

## Lễ, tình yêu, Tết, tiền (11)

| Gói | Tên CapCut | Dài | Trông thế nào |
|---|---|---|---|
| `2024-recap` | 2024 Recap | – | The first clip shrinks into a rounded photo card on a phone chat screen with confetti and a greeting… |
| `3d-heart-balloon` | 3D Heart Balloon | 0.8 s | A swarm of glossy pink heart balloons and bubbles pours in and rushes past the camera |
| `dollar-bills-ii` | Dollar Bills II | – | A burst of banknotes explodes from the centre of the first clip, one note flies into the camera to hide… |
| `firework-light` | Firework Light | 0.8 s | A burst of warm sparkles rises from the bottom and floods the frame |
| `heart-wipe-2` | Heart Wipe 2 | 0.8 s | A heart with two faint echoes opens over the first clip to show the second, wobbles |
| `love-shockwave` | Love Shockwave | 0.8 s | A glowing pixel-art heart grows from the centre of the first clip, with the second clip inside, until it… |
| `love-theme` | Love Theme | 0.8 s | A pixel-art curtain of pink hearts climbs over the first clip in stop-motion steps and leaves upward over… |
| `petal-wind` | Petal Wind | 0.8 s | A gust of red rose petals sweeps across the frame |
| `red-envelope` | Red Envelope | 0.8 s | A red envelope tumbles in over the first clip, is tapped and tears open, and the second clip bursts out of… |
| `sakura-flip` | Sakura Flip | 0.8 s | A giant cherry blossom petal sweeps across the frame among drifting petals and flips over |
| `turning-heart` | Turning Heart | 0.8 s | A glossy heart spins up, bursts into a pink heart that floods the frame |

## Tuyết (4)

| Gói | Tên CapCut | Dài | Trông thế nào |
|---|---|---|---|
| `3d-snowflake` | 3D Snowflake | 0.8 s | Snow falls over the first clip |
| `snow-cleared` | Snow Cleared | 1.47 s | Streaking snow builds into a white-out that hides a dip from the first clip to the second |
| `snow-scatter` | Snow Scatter | 0.8 s | A burst of sparks flies out of the centre and snowflakes drift and fade over the second clip |
| `snow-surround` | Snow Surround | 0.8 s | A glowing, wobbling ring of light grows out of the centre full of snowflakes, which |

## Glitch, TV, điện tử (17)

| Gói | Tên CapCut | Dài | Trông thế nào |
|---|---|---|---|
| `blu-ray-scanning` | Blu-ray Scanning | 1.47 s | A glowing blue scan line sweeps from the foreground to the background of the first clip, rippling the… |
| `captcha-switch-2` | Captcha Switch 2 | – | A captcha card pops up over the first clip, a cursor drags its slider to line up two rotated rings showing… |
| `crt-2-digital` | CRT 2 Digital | 0.8 s | The camera pulls back from the first clip to an old TV in a dim room |
| `digital-paint` | Digital Paint | 0.8 s | The first clip flares with a pulsing glow, brush strokes paint a black-dot halftone of the second clip over it |
| `double-glitch` | Double Glitch | 0.8 s | A hard cut hidden under a short burst of horizontal glitch: the frame slides and mirror-wraps, streaks… |
| `invert-transition` | Invert Transition | – | Handheld-shaking cut from the first clip to the second, hidden under a light-leak flash blended in… |
| `negative-flash` | Negative Flash | – | The first clip flickers under a punchy grade with two quick negative flashes |
| `negative-glitch` | Negative Glitch | 0.8 s | The picture flips to its negative, flares in exposure, shakes and zooms out with mirrored edges and a… |
| `pixel-vibe` | Pixel Vibe | 0.8 s | A halftone dot screen fades over the frame |
| `rainbow-strobe` | Rainbow Strobe | 0.8 s | Coloured bokeh lights strobe over the frame in screen blend, the picture cuts to a brightened second clip… |
| `record-scratch` | Record Scratch | 0.8 s | The first clip is shoved sideways with a bounce |
| `signal-glitch-2` | Signal Glitch 2 | 0.8 s | Glitch into the second clip: the colour channels drift apart, the picture jolts sideways with a motion… |
| `thermal-imaging-3` | Thermal Imaging 3 | 0.8 s | The second clip burns in from its highlights down to its shadows |
| `tv-flickers` | TV Flickers | 0.8 s | Tinted CRT scanlines fade in |
| `tv-glitch` | TV Glitch | 0.8 s | Cut to the second clip behind a bulging CRT lens, banded TV static, jumping picture shifts and colour fringing |
| `tv-shift` | TV Shift | 0.8 s | The first clip loses colour under flickering dark TV scanlines |
| `whiteout-pixel` | Whiteout Pixel | – | The picture turns into a zooming RGB dot screen, cuts to the second clip under a white light sweep |

## Giấy, vẽ tay, cọ (22)

| Gói | Tên CapCut | Dài | Trông thế nào |
|---|---|---|---|
| `brush-portal` | Brush Portal | 0.6 s | The second clip is painted in through a swirling brush stroke that grows from the centre, with a glowing… |
| `cartoon-inksplash` | Cartoon Inksplash | 0.8 s | Cartoon ink splats burst from the centre and spread until the second clip, seen through them, fills the frame |
| `comic-cut` | Comic Cut | – | The first clip cracks down the middle and tears into two paper-edged halves that fly apart over a halftone… |
| `doodle-scratch` | Doodle Scratch | 0.8 s | Chalk doodles and scratched photo cut-outs jolt the first clip, the second clip shows through the dark… |
| `film-blur` | Film Blur | 0.8 s | Hard cut hidden under a burst of warm, high-contrast light leak screened over the picture |
| `film-erase` | Film Erase | 0.8 s | Flickering film-burn light leaks wash over the clips |
| `film-wipe` | Film Wipe | 0.8 s | The first clip shrinks into a frame of a film strip that races down the screen under a vertical motion… |
| `glowing-graffiti` | Glowing Graffiti | 0.8 s | A red light leak and drifting sparks are screened over the picture |
| `neon-graffiti` | Neon Graffiti | 0.8 s | Yellow neon scribbles flicker over the first clip, which jolts and stretches into a white flash, and the… |
| `paintbrush-wipe` | Paintbrush Wipe | 0.8 s | The second clip is painted over the first in dry-brush strokes sweeping from the top left down to the right |
| `paper-ball` | Paper Ball | 0.67 s | A crumpled paper ball lands on the first clip, unfolds into a sheet and tears open onto the second clip |
| `paper-unfold` | Paper Unfold | 0.8 s | Crumpled newspaper climbs over the first clip |
| `pink-grunge` | Pink Grunge | 0.8 s | The picture flips to a shaking, motion-blurred negative under a flickering pink and red grunge light leak,… |
| `reveal-brush` | Reveal Brush | 0.8 s | Zig-zag brush strokes paint the second clip over the first |
| `slide-film` | Slide Film | 0.8 s | The first clip shrinks into a rounded frame and squashes into a blurred, glowing strip of film frames |
| `split-graffiti` | Split Graffiti | 0.8 s | White chalk-like scribbles sweep over the first clip |
| `tear-apart` | Tear Apart | 0.8 s | A white flash |
| `tearing-paper` | Tearing Paper | – | A ragged tear runs across the middle of the first clip |
| `tearoff-reveal` | Tearoff Reveal | – | A perforated strip is torn down the middle of the first clip |
| `twinkle-zoom` | Twinkle Zoom | 0.8 s | Dissolve to the second clip |
| `varnish-wash` | Varnish Wash | 1.47 s | A burst of glossy liquid blobs sprays out and merges into a metallic pool that refracts the second clip… |
| `whip-tear` | Whip Tear | 0.8 s | The first clip tears down the middle and the two halves bow and whip off to the sides with motion blur and… |

## Xoay, lật 3D (20)

| Gói | Tên CapCut | Dài | Trông thế nào |
|---|---|---|---|
| `centerfold-wipe` | Centerfold Wipe | – | The first clip rolls up like a sheet of paper from the top edge down, catching the light on the curl, and… |
| `cube-roll` | Cube Roll | – | The first clip is the front of a cube that tumbles a quarter turn on all three axes, its faces washing out… |
| `cube-rotate` | Cube Rotate | 0.8 s | The two clips sit on two faces of a cube that turns a quarter turn to the left in perspective, the first… |
| `cube-spins-2` | Cube Spins 2 | – | The first clip shrinks away onto a spinning cube that splits into two halves |
| `dial-turn` | Dial Turn | 0.8 s | The first clip whips off to the left with a growing horizontal motion blur |
| `fan-out` | Fan Out | 0.8 s | Gold, white and |
| `flip-fill` | Flip Fill | 0.8 s | A rounded card of the second input swings up over the first, flips over in 3D and bursts open with a… |
| `flip-page` | Flip Page | 0.8 s | Peel pages off from the bottom-left corner, two of the first input and |
| `fold-over` | Fold Over | 0.8 s | The second clip swings down in perspective from a hinge on the top edge, with motion blur, over the first… |
| `geometry` | Geometry | 0.8 s | Flat geometric shapes - blocks, a circle that breaks into a spinning pinwheel and corner wedges - slide,… |
| `open` | Open | – | The first clip splits down the middle and both halves swing open in perspective |
| `polygonal-unfold` | Polygonal Unfold | – | A crumpled paper polygon pops up over the first clip, tears open onto the second clip and unfolds outwards… |
| `roll-up-slide` | Roll-up Slide | 1.47 s | The first input rolls up diagonally like a page curling onto a cylinder, revealing the second |
| `rotating-disk` | Rotating Disk | 0.8 s | The first clip spins away under a rotational blur |
| `spinning-box` | Spinning Box | 0.8 s | A glowing box of the second clip pops up in the centre, spins a quarter turn and stretches open to fill… |
| `stack-rotate` | Stack & Rotate | 0.8 s | The first clip shrinks into a tilted card among blurred side cards |
| `turn-table` | Turn Table | 0.8 s | Swing the first input away on a giant turntable under an arc blur |
| `twist-flip` | Twist Flip | 0.8 s | The first clip darkens and twists about the diagonal like a ribbon, pinching at the centre, and untwists… |
| `twist-turn` | Twist Turn | 0.8 s | The first clip tips back and twists away as a card |
| `zip-flip` | Zip Flip | 1.47 s | The first clip twists shut row by row around a vertical axis and the second clip untwists out of it |

## Chớp sáng, phát sáng (13)

| Gói | Tên CapCut | Dài | Trông thế nào |
|---|---|---|---|
| `bubble-blur` | Bubble Blur | 0.8 s | Both clips soften into a ring-shaped bokeh where bright spots bloom into hollow bubbles, cross-fading at… |
| `bubbly-dream` | Bubbly Dream | 0.8 s | The first clip breaks up into a foam of wobbly bubbles that shrink and pop to reveal the second clip |
| `dazzle-pulse` | Dazzle Pulse | 0.8 s | A bright pulse: the frame swells, ripples, flares in exposure and shakes with a zoom blur and a colour… |
| `elastic-glowing` | Elastic & Glowing | 0.8 s | Squash and stretch the first input into a glowing fisheye zoom flash |
| `flash-split` | Flash Split | – | Hard cut to the second clip framed by two white flashes, first over the left half of the first clip |
| `golden-sand` | Golden Sand | 0.8 s | The first clip bursts into glowing golden sand that sweeps down the frame |
| `heat-flash` | Heat Flash | 0.8 s | The first clip blooms into a warm orange glow |
| `hot-shimmers` | Hot Shimmers | 0.8 s | Dissolve to the second clip through a heat-haze warp with a bright glow on the highlights and a zoom blur… |
| `photon-portal` | Photon Portal | 1.47 s | A violet energy ring bursts open over the shaking first clip, the second clip shows through its glowing… |
| `spotlight` | Spotlight | 0.8 s | A glowing light beam grows down from the top showing the second clip mirrored inside it, floods the… |
| `subject-flash` | Subject Flash | 0.8 s | The first clip twists away about its vertical axis |
| `sunset-flash` | Sunset Flash | 0.8 s | Hard cut hidden under a warm orange-to-white light leak that cools to deep red and fades |
| `transform-shimmer` | Transform Shimmer | 0.8 s | Fade to the second clip through a soft blur that swells and clears again |

## Gợn, mờ, xoáy (15)

| Gói | Tên CapCut | Dài | Trông thế nào |
|---|---|---|---|
| `big-wave` | Big Wave | 0.8 s | The first clip swells through a fisheye bulge into a turbulent zoom-blurred wave with a prism split and… |
| `blurred-switch` | Blurred Switch | – | White flashes, a horizontal blur burst and half-screen white and black strobes over a quick dissolve to… |
| `dispersion-trail` | Dispersion Trail | 0.8 s | The first clip blooms into a white glow, a curtain of blurred rainbow light streaks drifts diagonally… |
| `dispersion-trail-2` | Dispersion Trail 2 | 0.8 s | Coloured light streaks rush diagonally over the first clip, a cyan glare floods the frame white and fades… |
| `dramatic-vortex` | Dramatic Vortex | 0.8 s | The first clip grows and whirls away in a twisting, colour-split blur with an exposure flash, and the… |
| `glassblock-zoom-2` | Glassblock Zoom 2 | 0.8 s | Cut to the second clip inside a 5x mirrored zoom blur with chromatic fringes |
| `hexa-mosaic` | Hexa Mosaic | 0.8 s | Hard cut at the midpoint hidden by a sideways block-noise scramble, a red/green/blue scale split, a bright… |
| `horizontal-blur` | Horizontal Blur | – | Dissolve to the second clip through a horizontal blur and a bright exposure flash |
| `ripple-switch` | Ripple Switch | 0.8 s | The second clip drops in from the top, oversized and smeared by a vertical motion blur |
| `ripple-vibe` | Ripple Vibe | 0.8 s | The picture shakes, flares bright and ripples sideways in noisy waves |
| `shaky-inhale` | Shaky Inhale | 0.8 s | Suck the first input inward under a shaking zoom blur and a white glow |
| `sharding-pulse` | Sharding Pulse | 1.47 s | The picture breaks into a 10x10 grid of tiles that spread apart and pulse toward and away from the camera… |
| `tremor` | Tremor | 0.8 s | The first clip trembles and zooms in under a closing vignette and a lens bulge |
| `whirl` | Whirl | 0.8 s | The second clip flies up from the bottom as a round-cornered card, tumbling in 3D with motion blur and… |
| `wide-ripple` | Wide Ripple | 0.8 s | The picture swells and drifts sideways through a pinching wide-angle lens with a zoom blur, warm toning… |

## Lướt, trượt, phóng (51)

| Gói | Tên CapCut | Dài | Trông thế nào |
|---|---|---|---|
| `arrow-up` | Arrow Up | 0.8 s | An upward chevron wipe reveals the second clip, trailed by two gold chevron stripes |
| `big-picture` | Big Picture | 0.8 s | A white crop-frame icon slides in and opens into a box that reveals the second clip and grows to fill the… |
| `black-fade` | Black Fade | 1.47 s | Fade the first input to black |
| `break-swipe` | Break Swipe | 0.8 s | The second clip is typed in over the first in five snaking horizontal strips, the uncovered part smeared… |
| `collage-shift` | Collage Shift | 0.8 s | The first clip splits into two rows of repeated tiles that shrink and slide apart in opposite directions… |
| `color-wipe` | Color Wipe | 0.8 s | The picture turns black and white |
| `contrast-split` | Contrast Split | – | Hard cut hidden under a punchy analogue-video grade with a vignette and an exposure swell, a two-frame… |
| `crop-switch` | Crop Switch | 0.8 s | Cropped panels of the second clip pop up over the first with drop shadows and jolts |
| `delay-zoom` | Delay Zoom | 0.8 s | The first clip eases back into a mirrored, RGB-split zoom blur and flares bright |
| `diagonal-wipes` | Diagonal Wipes | – | Three diagonal strips switch from the first clip to the second one after another, each zooming in,… |
| `drag-up-switch` | Drag-up Switch | 1.47 s | The first clip zooms in and is dragged up out of frame with the second clip stacked beneath it, bulging… |
| `expand-fade` | Expand Fade | 1.47 s | The second clip opens out from a soft vertical band in the centre and spreads to both side edges |
| `fade-up` | Fade Up | 0.8 s | The first clip rises, grows and fades out over the second through a zoom blur and a gentle wave, with a… |
| `fisheye-wipe` | Fisheye Wipe | 0.8 s | The first clip is sucked into a fisheye pinch with a turbulent shake and a zoom blur, and the second clip… |
| `fisheye-zoom` | Fisheye Zoom | 0.8 s | The first clip bulges into a fisheye disc that shrinks to the centre under a growing zoom blur, uncovering… |
| `flying-rectangle` | Flying Rectangle | 0.8 s | The first clip zooms in through a black frame that closes into a band, tilts upright and flies away |
| `frame-swipe` | Frame Swipe | – | Hard cut at the midpoint hidden by a push-in and leftward slide of the first clip, a strong sideways… |
| `gradual-fade` | Gradual Fade | 0.8 s | Dissolves the first input into the second |
| `image-drop` | Image Drop | 0.8 s | The picture sags downward and smears in a vertical motion blur, cuts to the second clip and springs back… |
| `layers` | Layers | 1.47 s | A glowing hole opens in the bulging, spinning first clip and stacked rings cut from both clips spin out of… |
| `left-transition` | Left Transition | – | Both clips slide left with a strong motion blur, the second clip entering from the right, under a warm… |
| `mix` | Mix | 0.8 s | Linear dissolve from the first input to the second |
| `phone-reveal` | Phone Reveal | 0.8 s | A phone spins up from the bottom, its lock screen slides away and the view dives into its screen to reveal… |
| `pull-away` | Pull Away | 1.47 s | The first clip splits along its middle and its halves slide off up and down, uncovering the second clip as… |
| `pull-out` | Pull Out | 0.8 s | Zoom out of the first input with a radial blur |
| `push-away-2` | Push Away 2 | 0.8 s | The first clip pinches, shrinks and turns away with a camera shake |
| `red-swipe` | Red Swipe | 0.8 s | Pixel-sorted vertical streaks melt the first clip down |
| `screen-switch` | Screen Switch | 0.8 s | The first clip shrinks into a rounded, lens-curved card that flies up out of frame with motion blur |
| `shuriken-switch` | Shuriken Switch | 1.4667 s | The first clip spins away into the distance under a rotational blur |
| `sideway-bounce` | Sideway Bounce | 0.8 s | The picture zooms in and is knocked sideways by a fading wobble with motion smear and a bright glow,… |
| `silky-switch` | Silky Switch | 0.8 s | The first clip rounds its corners, shrinks and slides off to the left |
| `slanted-swipe` | Slanted Swipe | – | The first clip smears into a strong slanted motion blur with fast black flicker, cuts to the second clip… |
| `slice-reveal` | Slice Reveal | 0.8 s | The first clip is cut along a diagonal and its two halves slide apart sideways with motion blur and soft… |
| `slide-bars` | Slide Bars | 0.8 s | Four horizontal strips of the second clip slide in from alternating sides with motion blur |
| `slide-right` | Slide Right | – | Both clips slide right together, the second clip pushing in from the left, with ease-in-out |
| `snap-zoom` | Snap Zoom | 0.8 s | The first clip shrinks into a pinched, magnified bubble under zoom streaks |
| `snapshot-glam` | Snapshot Glam | 0.8 s | The first clip tips back and away like a photo card, the second swings up from below with a slight twist… |
| `split-2` | Split II | – | The top and bottom halves slide sideways in opposite directions with motion blur, revealing the second clip |
| `split-transition` | Split Transition | 0.8 s | The first input wipes away in two halves, split down the middle, over a pulsing glow of the second one… |
| `square-out` | Square Out | 0.8 s | A window opens from the centre of the first clip, pushing its four sides outward, and reveals the second… |
| `streamer` | Streamer I | 0.8 s | A wobbly hole with a glowing golden rim grows out of the zooming first clip and reveals the shrinking… |
| `target-zoom` | Target Zoom | 0.8 s | An aiming reticle locks onto a point, the picture swirls and bulges into it, and the second clip unwinds… |
| `tilt-fill` | Tilt Fill | 0.8 s | A tilted window onto the second clip opens from a line, widens into a band and fills the frame |
| `tilt-slide` | Tilt Slide | – | The frame pulls back into a rounded card and a strip of cards slides left with a perspective tilt until… |
| `torn-wipe` | Torn Wipe | 0.8 s | Torn-paper strips of the two clips slide in from every side before the second clip takes over |
| `triple-slide` | Triple Slide | 0.8 s | The frame splits into three columns that slide vertically in opposite directions with motion blur, pushing… |
| `vertical-swipe` | Vertical Swipe | – | Both clips slide down with a short motion blur, the second clip entering from the top |
| `wipe-right` | Wipe Right | 0.8 s | Hard-edged wipe that reveals the second input from left to right |
| `wipe-switch` | Wipe Switch | 0.8 s | A silver bar sweeps down the frame, uncovering the second clip above it |
| `wipers` | Wipers | – | A wiper blade hinged at the top-left corner sweeps the first clip away to a greyscale second clip |
| `zoom-switch` | Zoom Switch | 0.8 s | The picture punches in and snaps back |

## Khác (1)

| Gói | Tên CapCut | Dài | Trông thế nào |
|---|---|---|---|
| `angle-swap` | Angle Swap | 0.8 s | Hard cut at the midpoint hidden by a tilted push-in and pull-back with motion blur, a diamond bokeh, an… |
