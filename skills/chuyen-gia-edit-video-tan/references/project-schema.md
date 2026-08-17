# Hợp đồng project JSON

```json
{
  "editing": {"cut_authorized": false, "preserve_source_duration": true, "preserve_scene_order": true},
  "output": {"path":"edit/final.mp4","width":1920,"height":1080,"fps":30,"crf":18},
  "clips": [
    {"path":"a.mp4","in":0,"out":4.2,"filter":"news_clean","adjust":{"brightness":0.02,"contrast":1.04},"speed":1.0},
    {"path":"b.mp4","in":3,"out":7,"filter":"vibrant","speed":1.15,"transition":{"name":"flash_burst","duration":0.25}}
  ],
  "text": [{"text":"ATT NEWS","start":0.3,"end":3.5,"preset":"title_clean","x":"center","y":120}],
  "stickers": [{"path":"logo.png","start":0,"end":8,"x":70,"y":55,"width":150,"opacity":0.95}],
  "captions": {"path":"captions.ass","preset":"news_subtitle"},
  "lower_thirds": {"path":"lower-thirds.ass"},
  "music": {"path":"music.mp3","volume":0.16,"ducking":true},
  "effects": [{"preset":"flash_white","start":4.0,"duration":0.12,"strength":0.7}]
}
```

`clips` bắt buộc. Mặc định `cut_authorized=false`: phải giữ toàn bộ thời lượng và thứ tự của nguồn. Muốn cắt phải có xác nhận rõ của người dùng rồi mới đổi thành `true`. Khi được phép cắt, `out > in` và transition không dài quá nửa clip ngắn hơn. Thời gian overlay tính theo timeline đầu ra sau phần chồng transition.

`lower_thirds.path` là ASS tạo từ hợp đồng trong `lower-third-contract.md`. Khi đồng thời có caption, kiểm tra hai vùng không chồng nhau.
