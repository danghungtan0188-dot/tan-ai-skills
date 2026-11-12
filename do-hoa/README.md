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

## Trang xem trước mẫu (gallery)

Mở `gallery/index.html` để xem mọi mẫu: ảnh khung giữa, rê chuột vào xem GIF 2,5 giây, nút **Chép tên** chép Id mẫu.

Tạo lại (sau khi thêm/sửa mẫu trong `src/Root.tsx`):

```console
node scripts/lam_gallery.mjs
```

- Bundle một lần, render từng mẫu nối tiếp, `concurrency` 2 (máy hay treo khi chạy nặng). Mỗi mẫu ~20–40 giây.
- Mẫu đã có đủ `<Id>.png` + `<Id>.gif` thì bỏ qua → chạy lại chỉ làm mẫu mới/mẫu lỗi. Render lại tất cả: thêm `--lam-lai`.
- Mẫu lỗi ghi vào `gallery/loi.json` và hiện ở cuối trang, không dừng cả loạt. Mẫu cần ảnh/video trong `public/`
  (vd. `anh.png`) sẽ lỗi khi `public/` trống; mẫu dùng `OffthreadVideo` lỗi `spawn UNKNOWN` vì Windows chặn `remotion.exe`.
- Dòng "dùng khi" sửa trong bảng `DUNG_KHI` ở đầu script; mẫu chưa có trong bảng thì lấy câu đầu chú thích của file `.tsx`.

## Docs

Get started with Remotion by reading the [fundamentals page](https://www.remotion.dev/docs/the-fundamentals).

## Help

We provide help on our [Discord server](https://discord.gg/6VzzNDwUwV).

## Issues

Found an issue with Remotion? [File an issue here](https://github.com/remotion-dev/remotion/issues/new).

## License

Note that for some entities a company license is needed. [Read the terms here](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md).
