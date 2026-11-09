# Chuyển động lò xo

GSAP không có sẵn kiểu lò xo như `spring()` của Remotion. Hàm dưới tạo kiểu chuyển động đó cho GSAP: vượt qua đích một chút rồi dừng êm, đúng mốc cuối, nên vẫn tua được.

```js
// do_tat: 0.3 nảy nhiều · 0.5 nảy vừa · 0.8 gần như không nảy
function loXo(do_tat = 0.5) {
  const w = 6 / do_tat;
  const wd = w * Math.sqrt(1 - do_tat * do_tat);
  const x = (t) => 1 - Math.exp(-do_tat * w * t) * (Math.cos(wd * t) + (do_tat * w / wd) * Math.sin(wd * t));
  const cuoi = x(1);
  return (t) => (t >= 1 ? 1 : x(t) + (1 - cuoi) * t);
}
```

Dùng trong thẻ:

```js
tl.fromTo("#the", { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.7, ease: loXo(0.5) }, 0);
```

**Dùng khi:** khối, thẻ, nút, con số bật ra. Hợp các phong cách vui như Pop Art, Clay 3D, Neo-brutalism, Doodle.

**Tránh:** chữ dài, dòng phụ đề (nảy làm khó đọc và nhòe dấu tiếng Việt); phong cách nghiêm túc như Editorial, Minimal sang trọng, bản tin, phim tài liệu.

**Kiểm:** thời lượng tối thiểu 0,5 giây để kịp nảy; xem khung ở giữa chuyển động, chữ trên khối không được vượt khỏi khung hình.
