# Remotion video

<p align="center">
  <a href="https://github.com/remotion-dev/logo">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://github.com/remotion-dev/logo/raw/main/animated-logo-banner-dark.apng">
      <img alt="Animated Remotion Logo" src="https://github.com/remotion-dev/logo/raw/main/animated-logo-banner-light.gif">
    </picture>
  </a>
</p>

Welcome to your Remotion project!

## Commands

**Install Dependencies**

```console
npm i --loglevel=error
```

**Start Preview**

```console
npm run dev
```

**Render video**

```console
npx remotion render
```

**Upgrade Remotion**

```console
npx remotion upgrade
```

## Danh mục mẫu

`danh-muc.json` ghi **nhóm** và **dùng khi nào** cho từng mẫu trong `src/Root.tsx`. Thêm mẫu mới thì thêm một dòng ở đây —
`tests/test_danh_muc_do_hoa.py` báo đỏ nếu mẫu chưa có trong danh mục, danh mục còn mẫu đã xoá, hoặc file `src/mau/*.tsx` chưa đăng ký.

## Trang xem trước mẫu (gallery)

Tạo trên máy (không đưa lên git — ảnh/GIF nặng), rồi mở `gallery/index.html`: mẫu xếp theo nhóm, ảnh khung giữa,
rê chuột xem GIF 2,5 giây, nút **Chép tên** chép Id mẫu.

```console
node scripts/lam_gallery.mjs
```

- Bundle một lần, render từng mẫu nối tiếp, `concurrency` 2 (máy hay treo khi chạy nặng). Mỗi mẫu ~20–40 giây.
- Mẫu đã có đủ `<Id>.png` + `<Id>.gif` thì bỏ qua → chạy lại chỉ làm mẫu mới/mẫu lỗi. Render lại tất cả: thêm `--lam-lai`.
- Mẫu lỗi ghi vào `gallery/loi.json` và hiện ở cuối trang, không dừng cả loạt. Mẫu cần ảnh/video trong `public/`
  (vd. `anh.png`) sẽ lỗi khi `public/` trống.

## Số hình/giây: mạng xã hội 30, phát sóng 25

Mặc định đồ họa dựng 30 hình/giây (khớp video điện thoại). **Bản phát sóng (hệ 50 Hz, 25 hình/giây)** phải dựng thẳng ở 25 —
đổi 30 → 25 sau khi render sẽ bỏ 1/6 số hình, chữ chạy và lia bản đồ bị giật:

```console
REMOTION_FPS=25 npx remotion render src/index.ts ChuChay out/chu-chay.mov --props=props.json
```

(PowerShell: `$env:REMOTION_FPS=25; npx remotion render …`.) Thời lượng tính theo giây nên không đổi; `tests/test_fps_do_hoa.py` cấm ghi cứng fps.
## Xuất đồ họa nền trong suốt

Mẫu nền trong suốt (`LowerThird`, `ChuChay`, `SoLieuChienCong`…) mặc định ra **ProRes 4444** `.mov` — dùng cho Premiere, Resolve, Shotcut:

```console
npx remotion render src/index.ts ChuChay out/chu-chay.mov --props=props.json
```

Cần **WebM có kênh trong suốt** cho OBS / trình duyệt (phát trực tiếp): chuyển từ bản `.mov` trên
(Remotion không cho đổi thẳng sang vp9 vì mẫu đã đặt sẵn ProRes 4444):

```console
ffmpeg -i out/chu-chay.mov -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 32 -row-mt 1 -threads 2 -an out/chu-chay.webm
```

Kiểm: `ffprobe` phải thấy `alpha_mode=1`; khi xem lại bằng ffmpeg phải giải mã bằng `-c:v libvpx-vp9` (bộ giải mã mặc định bỏ kênh trong suốt).
Ý tưởng xuất song song hai định dạng học từ `iart-ai/lower-thirds-skills` (MIT); lệnh viết lại và đã chạy thử (16/11/2026).

## Bản đồ giật 12 hình/giây

`BanDoNoi` có `nhip12: true`: chuyển động giữ mỗi hình 2,5 khung (12 hình/giây trên video 30 hình/giây) cho ra chất đồ họa
kiểu bản đồ Vox thay vì chuyển động quay phim. Mặc định tắt. Ý tưởng từ `iart-ai/map-animation-skills` (MIT), viết lại.

## Docs

Get started with Remotion by reading the [fundamentals page](https://www.remotion.dev/docs/the-fundamentals).

## Help

We provide help on our [Discord server](https://discord.gg/6VzzNDwUwV).

## Issues

Found an issue with Remotion? [File an issue here](https://github.com/remotion-dev/remotion/issues/new).

## License

Note that for some entities a company license is needed. [Read the terms here](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md).
