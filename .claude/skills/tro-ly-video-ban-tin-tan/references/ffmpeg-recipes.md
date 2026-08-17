# FFmpeg Recipes — CapCut-style Library

Các lệnh dưới đây là công thức chạy được. Thay INPUT/OUTPUT, timecode, font và kích thước theo dự án.

## 1. TRANSITIONS

### Fade in + fade out
```bash
ffmpeg -y -i INPUT.mp4 -vf "fade=t=in:st=0:d=0.5,fade=t=out:st=9.5:d=0.5" -c:a copy OUTPUT.mp4
```

### Dissolve giữa hai clip
```bash
ffmpeg -y -i A.mp4 -i B.mp4 -filter_complex "[0:v][1:v]xfade=transition=dissolve:duration=0.6:offset=4.4[v];[0:a][1:a]acrossfade=d=0.6[a]" -map "[v]" -map "[a]" OUTPUT.mp4
```

### Wipe left
```bash
ffmpeg -y -i A.mp4 -i B.mp4 -filter_complex "[0:v][1:v]xfade=transition=wipeleft:duration=0.5:offset=4.5[v]" -map "[v]" OUTPUT.mp4
```

### Slide left
```bash
ffmpeg -y -i A.mp4 -i B.mp4 -filter_complex "[0:v][1:v]xfade=transition=slideleft:duration=0.5:offset=4.5[v]" -map "[v]" OUTPUT.mp4
```

### Circle open / close
```bash
ffmpeg -y -i A.mp4 -i B.mp4 -filter_complex "[0:v][1:v]xfade=transition=circleopen:duration=0.6:offset=4.4[v]" -map "[v]" OPEN.mp4
ffmpeg -y -i A.mp4 -i B.mp4 -filter_complex "[0:v][1:v]xfade=transition=circleclose:duration=0.6:offset=4.4[v]" -map "[v]" CLOSE.mp4
```

## 2. TEXT

### Banner tiêu đề
```bash
ffmpeg -y -i INPUT.mp4 -vf "drawbox=x=120:y=h-230:w=w-240:h=150:color=0x06224A@0.88:t=fill:enable='between(t,2,10)',drawtext=fontfile=FONT.ttf:text='AN THẠNH THỦY ĐẨY MẠNH BÌNH DÂN HỌC VỤ SỐ':fontcolor=white:fontsize=48:x=170:y=h-190:enable='between(t,2,10)'" OUTPUT.mp4
```

### Fade chữ
```bash
ffmpeg -y -i INPUT.mp4 -vf "drawtext=fontfile=FONT.ttf:text='ATT NEWS':fontsize=52:fontcolor=white@'if(lt(t,1),t,if(lt(t,5),1,6-t))':x=80:y=80:enable='between(t,0,6)'" OUTPUT.mp4
```

### Typewriter
```bash
ffmpeg -y -i INPUT.mp4 -vf "drawtext=fontfile=FONT.ttf:text='BÌNH DÂN HỌC VỤ SỐ':fontsize=52:fontcolor=white:x=120:y=850:enable='between(t,2,8)':text_shaping=1" OUTPUT.mp4
```
Ghi chú: typewriter chính xác theo từng ký tự nên tạo ASS/subtitle hoặc render text frame-by-frame; không giả vờ rằng drawtext tự cắt chuỗi UTF-8 an toàn.

### Đếm ngược 5 giây
```bash
ffmpeg -y -f lavfi -i color=c=black:s=1920x1080:d=5 -vf "drawtext=fontfile=FONT.ttf:text='%{eif\\:5-t\\:d}':fontsize=220:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2" COUNTDOWN.mp4
```

## 3. FILTERS

### Natural
```bash
ffmpeg -y -i INPUT.mp4 -vf "eq=brightness=0.02:contrast=1.04:saturation=1.04" OUTPUT.mp4
```

### Vibrant
```bash
ffmpeg -y -i INPUT.mp4 -vf "eq=contrast=1.08:saturation=1.18:brightness=0.02" OUTPUT.mp4
```

### Cinematic
```bash
ffmpeg -y -i INPUT.mp4 -vf "eq=contrast=1.12:saturation=0.92:brightness=-0.01,colorbalance=bs=.04:rs=-.02" OUTPUT.mp4
```

### Black & White
```bash
ffmpeg -y -i INPUT.mp4 -vf "hue=s=0,eq=contrast=1.08" OUTPUT.mp4
```

### Vintage
```bash
ffmpeg -y -i INPUT.mp4 -vf "colorchannelmixer=.9:.1:0:0:.05:.85:.1:0:.1:.1:.75,eq=contrast=0.95:saturation=0.85" OUTPUT.mp4
```

### Vignette
```bash
ffmpeg -y -i INPUT.mp4 -vf "vignette=PI/5" OUTPUT.mp4
```

## 4. EFFECTS

### Ken Burns ảnh
```bash
ffmpeg -y -loop 1 -i PHOTO.jpg -vf "scale=8000:-1,zoompan=z='min(zoom+0.0008,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=150:s=1920x1080:fps=30" -t 5 OUTPUT.mp4
```

### Slow motion 0.5x
```bash
ffmpeg -y -i INPUT.mp4 -filter_complex "[0:v]setpts=2.0*PTS[v];[0:a]atempo=0.5[a]" -map "[v]" -map "[a]" OUTPUT.mp4
```

### Speed 2x
```bash
ffmpeg -y -i INPUT.mp4 -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" -map "[v]" -map "[a]" OUTPUT.mp4
```

### Speed ramp theo đoạn
```bash
ffmpeg -y -i INPUT.mp4 -filter_complex "[0:v]trim=0:3,setpts=PTS-STARTPTS[v0];[0:v]trim=3:6,setpts=0.5*(PTS-STARTPTS)[v1];[0:v]trim=6:10,setpts=PTS-STARTPTS[v2];[v0][v1][v2]concat=n=3:v=1:a=0[v]" -map "[v]" OUTPUT.mp4
```

### Freeze frame 2 giây tại mốc 5s
```bash
ffmpeg -y -i INPUT.mp4 -filter_complex "[0:v]trim=0:5,setpts=PTS-STARTPTS[a];[0:v]trim=5:5.04,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=2[b];[0:v]trim=start=5.04,setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0[v]" -map "[v]" OUTPUT.mp4
```

## 5. STICKERS

### Logo góc phải
```bash
ffmpeg -y -i INPUT.mp4 -i LOGO.png -filter_complex "[1:v]scale=180:-1[logo];[0:v][logo]overlay=W-w-40:40" OUTPUT.mp4
```

### Facebook/Zalo nhỏ gọn
```bash
ffmpeg -y -i INPUT.mp4 -i SOCIAL.png -filter_complex "[1:v]scale=140:-1[s];[0:v][s]overlay=W-w-35:H-h-35:enable='between(t,20,79)'" OUTPUT.mp4
```
Mặc định social chỉ khoảng 4-8% chiều rộng video. Không dùng panel lớn nếu người dùng không yêu cầu.

### Khung viền
```bash
ffmpeg -y -i INPUT.mp4 -vf "drawbox=x=8:y=8:w=iw-16:h=ih-16:color=white@0.65:t=3" OUTPUT.mp4
```

## 6. ADJUSTMENT

### Sáng / tương phản / bão hòa
```bash
ffmpeg -y -i INPUT.mp4 -vf "eq=brightness=0.03:contrast=1.06:saturation=1.05" OUTPUT.mp4
```

### Sharpen nhẹ
```bash
ffmpeg -y -i INPUT.mp4 -vf "unsharp=5:5:0.45:5:5:0" OUTPUT.mp4
```

### Giảm rung — 2 pass vidstab
```bash
ffmpeg -y -i INPUT.mp4 -vf "vidstabdetect=shakiness=5:accuracy=15:result=transforms.trf" -f null -
ffmpeg -y -i INPUT.mp4 -vf "vidstabtransform=input=transforms.trf:smoothing=20:zoom=2" -c:v libx264 -crf 20 -c:a copy OUTPUT.mp4
```
**Cảnh báo:** FFmpeg build có thể không có `vidstabdetect/vidstabtransform`. Kiểm tra bằng `ffmpeg -filters | grep vidstab`. Stabilization có thể crop, zoom, méo biên hoặc làm cảnh tệ hơn; luôn preview đoạn mẫu trước.

## 7. CAPTIONS

### Cháy phụ đề SRT vào hình
```bash
ffmpeg -y -i INPUT.mp4 -vf "subtitles=sub.srt" -c:a copy OUTPUT.mp4
```

### Phụ đề có style + vùng an toàn
```bash
ffmpeg -y -i INPUT.mp4 -vf "subtitles=sub.srt:force_style='FontName=Arial,FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,Shadow=1,Alignment=2,MarginV=40'" -c:a copy OUTPUT.mp4
```
`Alignment=2` là giữa–dưới. `MarginV` là khoảng cách tính từ mép dưới; đặt ≥8% chiều cao khung (1080p → ~86, 720p → ~58) để không đụng vùng UI của Facebook/TikTok.

### Hộp nền mờ khi nền sáng hoặc nhiều chi tiết
```bash
ffmpeg -y -i INPUT.mp4 -vf "subtitles=sub.srt:force_style='FontName=Arial,FontSize=18,BorderStyle=3,BackColour=&H80000000,MarginV=40'" -c:a copy OUTPUT.mp4
```
`BorderStyle=3` đổi viền thành hộp nền. Màu ASS là `&HAABBGGRR` — `&H80000000` là đen trong suốt 50%.

### Cháy phụ đề ASS (karaoke, caption theo từ, nhiều style)
```bash
ffmpeg -y -i INPUT.mp4 -vf "ass=sub.ass" -c:a copy OUTPUT.mp4
```
Dùng ASS khi cần highlight theo từ hoặc nhiều kiểu chữ trong cùng video; SRT không làm được.

### Dịch toàn bộ timestamp
```bash
ffmpeg -y -itsoffset 2.5 -i sub.srt -c copy shifted.srt
```
Dịch cả file đi 2,5 giây. Chỉ đúng khi cắt **một khối ở đầu**. Nếu cắt nhiều đoạn giữa video thì phải tính lại từng cue theo timeline mới, không dùng lệnh này.

**Lỗi thường gặp trên Windows:** filter `subtitles`/`ass` hiểu dấu `:` trong `C:\...` là dấu phân cách tham số. Chạy `ffmpeg` từ đúng thư mục chứa file phụ đề và truyền đường dẫn tương đối (`sub.srt`), đừng truyền đường dẫn tuyệt đối.

**Thứ tự:** burn phụ đề **sau cùng**, sau khi đã chốt crop, màu và ghép. Crop sau khi burn sẽ cắt cụt chữ.

## Render video dài chống timeout
Chia đoạn:
```bash
ffmpeg -y -ss 0 -to 25 -i INPUT.mp4 ... PART1.mp4
ffmpeg -y -ss 25 -to 50 -i INPUT.mp4 ... PART2.mp4
ffmpeg -y -ss 50 -i INPUT.mp4 ... PART3.mp4
```
Tạo `concat.txt`:
```text
file 'PART1.mp4'
file 'PART2.mp4'
file 'PART3.mp4'
```
Ghép:
```bash
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy MERGED.mp4
```
Nếu thông số codec giữa các part không đồng nhất, re-encode MERGED thay vì `-c copy`.
