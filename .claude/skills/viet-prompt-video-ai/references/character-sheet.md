# Bảng nhân vật

Tạo bảng này bằng công cụ tạo ảnh trước, rồi dùng làm ảnh tham chiếu cho các cảnh video. Chỉ dùng ảnh của chính người dùng hoặc người đã đồng ý.

## Bảng 6 góc mặt (tỉ lệ 3:2)

Đầu vào: `@image1` là ảnh chính diện, rõ mặt.

```text
Studio photo reference sheet of the same person as @image1. Keep the face, hair, skin texture and any facial accessories exactly the same, with no beautification. Do not mirror or swap sides. Ignore the clothing and background of @image1; the person wears a plain white crew-neck t-shirt.

One image split into a 3x2 grid of equal portrait panels with thin white gutters and a neutral mid-grey background.
Top row: left profile, straight front view, right profile.
Bottom row: three-quarter view turned left, back of the head, three-quarter view turned right.

The eyes follow the direction of the head. Show the whole head, neck and shoulders, with the same head size, eye line and camera distance in every panel. 85mm lens, soft even studio light, neutral expression, mouth closed. No text, labels, numbers or watermark.
```

## Bảng trang phục mặt trước và sau (tỉ lệ 1:1)

Đầu vào: `@image1` là ảnh có bộ đồ, người mặc hoặc ảnh sản phẩm đều được.

```text
Clothing reference sheet of the exact outfit in @image1. Keep the cut, colours, fabric, patterns, logos and details unchanged. Ignore the person and background of @image1.

One image split into two equal panels with a thin white gutter and a neutral light-grey background. Left panel: front view. Right panel: back view. Show the whole outfit at the same scale in both panels, on an invisible mannequin, with soft even light. No text, labels, numbers or watermark.
```

## Dùng trong prompt video

```text
Character A corresponds to @Image 1 for the face and hair only. Do not use its background or t-shirt.
Character A wears the outfit in @Image 2. Do not use its background.
```

**Soát:** mặt có giống ảnh gốc ở cả 6 ô không; trái và phải có bị đổi không; khuyên tai, nốt ruồi có đúng bên không. Nếu sai thì tạo lại trước khi làm video, vì lỗi ở bảng sẽ lặp lại trong mọi cảnh.
