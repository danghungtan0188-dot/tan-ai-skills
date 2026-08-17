# Stickers / icon overlay

**Nguyên tắc bắt buộc:** không tải logo/sticker có bản quyền (Facebook, TikTok, Zalo chính chủ...) từ nguồn ngoài về dùng — tự dựng bằng hình khối + chữ (đủ để nhận diện, không phải bản sao logo chính thức). Đã dùng thật trong dự án cho icon Facebook/Zalo góc video.

## Icon badge tròn/vuông đơn giản (đã dùng thật)

```bash
F='drawbox=x=40:y=976:w=64:h=64:color=0x1877F2@0.95:t=fill,'
F+='drawbox=x=116:y=976:w=64:h=64:color=0x0068FF@0.95:t=fill,'
F+="drawtext=fontfile='C\:/Windows/Fonts/arialbd.ttf':textfile='chu_f.txt':fontsize=36:fontcolor=white:x=40+(64-tw)/2:y=976+(64-th)/2-4,"
F+="drawtext=fontfile='C\:/Windows/Fonts/segoeuib.ttf':textfile='chu_zalo.txt':fontsize=17:fontcolor=white:x=116+(64-tw)/2:y=976+(64-th)/2-4"
ffmpeg -i input.mp4 -vf "$F" -c:v libx264 -preset fast -crf 19 -pix_fmt yuv420p -c:a copy output.mp4
```

Mã màu badge tham khảo (đúng thương hiệu, không phải logo):
- Facebook: `0x1877F2`
- Zalo: `0x0068FF`
- TikTok: `0x000000` (nền đen, chữ trắng/hồng `0xFE2C55`/xanh `0x25F4EE`)
- YouTube: `0xFF0000`
- Website/globe: `0x4A90D9` hoặc theo màu thương hiệu

**Luôn kiểm tra vị trí không đè lên logo/chữ có sẵn trong khung hình** — trích 1 frame xem trước khi áp toàn video (bài học thực tế: icon từng bị đặt đè lên logo kênh đã có sẵn, phải dời chỗ).

## Khung viền (border/frame overlay)

```
drawbox=x=20:y=20:w=iw-40:h=ih-40:color=white@0.8:t=4
```
Khung viền mỏng cách mép 20px, dày 4px — dùng cho hiệu ứng "polaroid"/khung ảnh.

## Sticker động (nhấp nháy/di chuyển)

Icon/badge tĩnh dùng `drawbox`/`drawtext` là đủ cho hầu hết nhu cầu. Sticker có chuyển động phức tạp (nảy, xoay, bay vào khung hình) nên dựng qua HyperFrames (xem `hyperframes-animation`) rồi render ra clip nền trong suốt (WebM alpha hoặc PNG sequence), ghép bằng:
```
ffmpeg -i main.mp4 -i sticker.webm -filter_complex "[0:v][1:v]overlay=x=<X>:y=<Y>:enable='between(t,<BAT_DAU>,<KET_THUC>)'" output.mp4
```
