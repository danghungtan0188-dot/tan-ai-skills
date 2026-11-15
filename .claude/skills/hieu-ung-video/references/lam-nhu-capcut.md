# Làm như CapCut bằng thứ đã có

Bảng tra theo đúng 8 mục trên thanh công cụ CapCut (Text, Stickers, Effects, Transitions, Captions, Filters, Adjustment, Templates). Mỗi mục ghi: trong repo đã có gì, nguồn mở nào lấy thêm được, khi nào nên dùng cái nào.

**Không lấy hiệu ứng độc quyền của CapCut ra ngoài CapCut.** Mẫu chữ, sticker, hiệu ứng, bộ lọc của CapCut thuộc ByteDance. Muốn đúng "đồ CapCut" thì dựng trong CapCut (xem mục cuối).

Cập nhật 15/11/2026. Ba repo ngoài đã tải bản nông về `D:\GitHub\ngoai\`, **chưa cài, chưa chạy**.

## Bảng 8 mục

| Mục CapCut | Trong repo đã có | Lấy thêm (nguồn mở) | Dùng cái nào |
|---|---|---|---|
| **Text** (chữ, chữ động) | [chu-va-hoat-hinh.md](chu-va-hoat-hinh.md). Skill `motion-graphics-tan`: 20 phong cách (Swiss, Kinetic Type, Neon…) và 16 thẻ kỹ thuật (`tieu-de-mo-dau`, `so-dem-chay`, `so-muc-to`, `chu-ma-nen`…). Font Việt: Montserrat VN, Inter VN, Playfair VN | Bộ GSAP (`gsap-*`, đã cài toàn cục): SplitText tách chữ từng ký tự | Tiêu đề, số liệu → thẻ `motion-graphics-tan`. Chữ bám theo câu nói → `video-marketing` |
| **Stickers** (icon, nhãn) | [nhan-dan-sticker.md](nhan-dan-sticker.md). Thẻ `khoanh-tay` (vòng đỏ vẽ tay), `o-binh-luan`, `con-tro-gia` | Icon tự vẽ bằng SVG. Không tải logo của người khác | Tự dựng bằng hình + chữ, như luật của skill này |
| **Effects** (hiệu ứng hình) | [ky-thuat-tu-video-mau.md](ky-thuat-tu-video-mau.md) (glitch, bloom, vạn hoa, mây mở cảnh). Mẫu Remotion `HudDemSo`, `AnhBayVao`. Skill `video-marketing`: hiệu ứng nằm **sau** người nói (`tach_nguoi` + `ghep_lop`) | 455 mẫu registry HyperFrames ([hoc-tu-hyperframes.md](hoc-tu-hyperframes.md)) | Hiệu ứng sau người nói là thứ CapCut khó làm. Đây là điểm mạnh riêng của repo |
| **Transitions** (chuyển cảnh) | [chuyen-canh.md](chuyen-canh.md) (ffmpeg `xfade`: fade, wipe, slide, circle, zoom). Mẫu Remotion `GhepCanh` | **gl-transitions** (MIT, 2.252 sao): 248 chuyển cảnh GLSL ở `D:\GitHub\ngoai\gl-transitions`. **FFmpegGpuFilter-packages-capcut** (MIT): 155 chuyển cảnh mang tên CapCut, viết lại từ đầu, không chứa đồ CapCut, ở `D:\GitHub\ngoai\FFmpegGpuFilter-packages-capcut`. Danh mục cũ: [chuyen-canh-gpufx.md](chuyen-canh-gpufx.md) | Mặc định dùng `xfade` (nhẹ, chạy ngay). gl-transitions và gpufx cần bản FFmpeg riêng hoặc trình chạy GLSL: **hỏi người dùng trước**, thử 1 chuyển cảnh giữa 2 clip ngắn |
| **Captions** (phụ đề) | Thẻ `phu-de-to-tu` (tô màu từ khóa). `tan_studio` (script → giọng → phụ đề → MP4). Skill `remotion-captions`. Phụ đề song ngữ, tự tránh mặt (YuNet) trong `bien-tap-video-thong-minh-song-ngu-tan` | — | Video người nói → `phu-de-to-tu`. Bản tin ATT NEWS → **không** phụ đề (theo phong cách đã chốt) |
| **Filters** (bộ lọc màu) | [bo-loc-mau.md](bo-loc-mau.md) (vintage, đen trắng, ấm/lạnh, teal-orange, vignette) | LUT `.cube` miễn phí (ffmpeg `lut3d`) | Tư liệu tài liệu/bản tin: **không tô màu** (theo phong cách phim tài liệu). Video quảng cáo: một bộ lọc cho cả video, không đổi giữa chừng |
| **Adjustment** (sáng, tương phản, nét) | [hieu-chinh.md](hieu-chinh.md). Âm thanh: luật loudnorm 2 lượt `linear=true` | — | Đo trước và sau khi chỉnh. Không ép limiter quá 3 dB |
| **Templates** (mẫu dựng sẵn) | 20 mẫu phong cách và 16 thẻ trong `motion-graphics-tan` (render bằng `render_mau.py`). Mẫu Remotion trong `do-hoa/` (intro, số liệu, lower-third). Bộ tiếng động `sfx` (MIT) | Mixkit: mẫu Premiere/After Effects/DaVinci miễn phí, không cần đăng ký (không dùng được trực tiếp trong repo, chỉ tham khảo) | Dựng video mới: chọn phong cách trước, dùng lại thẻ, chỉ đổi chữ và màu |

## Hiệu ứng trend (glitch, VHS, rung, zoom giật)

Đã có sẵn: tách RGB + vạch glitch, vệt sáng, lóe trắng (preset `glitch_rgb`, `light_leak`, `flash_white` trong [ky-thuat-tu-video-mau.md](ky-thuat-tu-video-mau.md)); mẫu HyperFrames `chromatic-glitch`, `camera-shake`, `whip-pan` ([hoc-tu-hyperframes.md](hoc-tu-hyperframes.md)).

Ba công thức ffmpeg thêm dưới đây đã **chạy thử ngày 15/11** trên clip thử 540×960, 2 giây: ra đúng 60 khung, đúng kích thước, đã soát ảnh từng khung. Đổi `540:960` cho đúng khung của video thật.

| Hiệu ứng | Bộ lọc (`-vf`) | Ghi chú |
|---|---|---|
| **VHS** (băng từ cũ) | `rgbashift=rh=4:bh=-4,gblur=sigma=0.8,noise=alls=12:allf=t,eq=saturation=0.85:contrast=1.05,drawgrid=w=iw:h=4:t=1:c=black@0.25` | Lệch màu nhẹ, mờ nhẹ, nhiễu hạt, vạch quét ngang. Dùng cho cảnh hồi tưởng. Không dùng cho tư liệu bản tin |
| **Rung máy** | `scale=iw*1.06:-2,crop=540:960:x='(iw-540)/2+12*sin(t*47)':y='(ih-960)/2+10*sin(t*61)'` | Phóng 6% rồi xê dịch. Chỉ áp cho **đoạn 0,3–0,6 giây** lúc có tiếng động mạnh, không áp cả clip (gây chóng mặt) |
| **Zoom giật** (punch-in) | `scale=w='iw*if(between(t,1,1.5),1.15,1)':h=-2:eval=frame,crop=540:960` | Phóng 15% đúng lúc nhấn chữ hoặc theo nhịp nhạc. Đổi `1,1.5` thành giây cần nhấn |

Luôn kèm `-threads 2`, x264 `-preset faster`. Mỗi file chỉ `-i` một lần (hook `guard_video` chặn đọc một file hai lần).

**Repo ngoài đã soát (15/11), không lấy:**

| Repo | Sao | Lý do không lấy |
|---|---|---|
| ntsc-rs (VHS rất thật, app + plugin After Effects/Premiere) | 2.721 | Giấy phép không rõ. Chỉ dùng như một app riêng nếu cần VHS thật |
| video-fx (Python, 150 hiệu ứng) | 0 | Repo mới, chưa ai dùng. Công thức ffmpeg ở trên đủ cho việc hay gặp |
| reactvideoeditor/remotion-templates | 292 | Không ghi giấy phép. Chỉ đọc tham khảo |
| remotion-open-fx (npm) | — | Repo gốc trên GitHub đã bị xóa |
| remotion-glitch-effect, pyeffects | 4 / 3 | Quá nhỏ, công thức sẵn có đã làm được |

## Âm thanh (CapCut để trong mục Audio)

- Tiếng động tự tạo: `motion-graphics-tan/scripts/sfx` (MIT), cách dùng trong [tieng-dong.md](../../motion-graphics-tan/references/tieng-dong.md). Đã master −14 LUFS, đỉnh ≤ −2 dBFS.
- Chỉ đặt tiếng "vút" ở chỗ đổi phần hoặc khi hiện số, không đặt ở mọi thẻ.

## Khi thật sự cần "đồ CapCut"

CapCut có sẵn trên máy (`AppData\Local\CapCut`). Hiệu ứng của CapCut chỉ dùng **bên trong CapCut**.

- Cách tay: dựng thô bằng repo (cắt, giọng, phụ đề), xuất MP4, mở trong CapCut thêm hiệu ứng rồi xuất lại.
- Cách tự động: thư viện **pyCapCut** (752 sao, `D:\GitHub\ngoai\pyCapCut`) tạo file nháp CapCut có sẵn chữ động, hiệu ứng, chuyển cảnh, bộ lọc. Người dùng mở CapCut và tự bấm xuất.
  - Theo bộ dữ liệu của thư viện, CapCut có khoảng 1.580 hiệu ứng cảnh, 250 hiệu ứng nhân vật, 450 bộ lọc, 1.100 chuyển cảnh, 360 kiểu chữ vào/ra/lặp và 350 font. Con số đếm từ mã nguồn, có thể lệch nhẹ.
  - Repo **không ghi giấy phép**: được đọc và dùng trên máy, **không chép mã hay danh sách tên vào repo này** (repo công khai).
  - Ngày 15/11 người dùng **chưa muốn cài**. Muốn dùng phải hỏi lại trước khi cài (cần thêm 3 thư viện: `pymediainfo`, `imageio`, `uiautomation`).
  - Hiệu ứng có nhãn Pro cần tài khoản CapCut Pro.

## Thứ tự chọn công cụ

1. Có sẵn trong repo và chạy được ngay (ffmpeg, thẻ HyperFrames, mẫu Remotion) → dùng trước.
2. Cần hiệu ứng lạ hơn → thẻ mới bằng HyperFrames/GSAP theo luật của `motion-graphics-tan`.
3. Cần đúng hiệu ứng CapCut → dựng thô bằng repo, hoàn thiện trong CapCut.

Máy hay sập khi chạy nặng: mỗi lần một việc nặng, ffmpeg `-threads 2`, render từng thẻ một.
