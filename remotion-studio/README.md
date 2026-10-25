# Remotion Studio cho tan-ai-skills

Engine Remotion dùng song song với HyperFrames. Composition `AttNews` nhận props JSON nên có thể dùng audio, SRT, ảnh hoặc clip do `tan_studio` và các skill video hiện tại tạo ra.

```powershell
npm install
npm run dev
npm run still:sample
```

Chuẩn bị một dự án thật:

```powershell
python scripts/prepare_project.py `
  --title "Bản tin hôm nay" `
  --subtitle "Xã An Thạnh Thủy" `
  --video "C:\du-an\clip.mp4" `
  --audio "C:\du-an\giong-doc.wav" `
  --captions "C:\du-an\phu-de.srt"

npx remotion studio src/index.ts --props=props/generated.json
npx remotion render src/index.ts AttNews out/ban-tin.mp4 --props=props/generated.json
```

`prepare_project.py` chỉ đọc file nguồn, chép bản có hash vào `public/assets/` và không ghi đè media gốc. Nếu không truyền `--duration`, script lấy thời lượng từ audio trước, sau đó tới video bằng `ffprobe`.

Trước khi giao video, chạy QA từ gốc repo:

```powershell
python scripts/video_qa.py remotion-studio/out/ban-tin.mp4 --strict --audio
```

Không commit media trong `public/assets/`, file render trong `out/`, hoặc dữ liệu giọng cá nhân.
