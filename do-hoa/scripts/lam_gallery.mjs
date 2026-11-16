// Trang xem trước các mẫu đồ hoạ: mỗi mẫu 1 ảnh tĩnh (khung giữa) + 1 GIF ~2,5 giây rộng 480 px,
// ghép thành do-hoa/gallery/index.html. Dùng defaultProps có sẵn trong Root.tsx.
// Chạy: cd do-hoa && node scripts/lam_gallery.mjs   (thêm --lam-lai để render lại tất cả)
// Máy hay treo khi chạy nặng → bundle một lần, render từng mẫu nối tiếp, concurrency 2.
// Mẫu đã có đủ ảnh + GIF thì bỏ qua; mẫu lỗi ghi vào gallery/loi.json, không dừng cả loạt.
import { bundle } from "@remotion/bundler";
import { getCompositions, renderMedia, renderStill } from "@remotion/renderer";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const GOC = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const RA = path.join(GOC, "gallery");
const LAM_LAI = process.argv.includes("--lam-lai");
const GIAY_GIF = 2.5;

// "Dùng khi" và nhóm của từng mẫu nằm ở do-hoa/danh-muc.json (test ép mẫu nào cũng phải có).
const DANH_MUC = JSON.parse(fs.readFileSync(path.join(GOC, "danh-muc.json"), "utf8"));

// Mẫu mà khung giữa không đại diện (VetSang: giữa là lúc phủ trắng; PhuNu96: chưa có cảnh nên giữa là đen,
// màn chúc mừng ở cuối) → chọn vị trí khác, tính theo phần của thời lượng.
const VI_TRI = { VetSang: 0.3, PhuNu96: 0.85 };


const docJson = (file, macDinh) => (fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, "utf8")) : macDinh);
const ghiJson = (file, v) => fs.writeFileSync(file, JSON.stringify(v, null, 2) + "\n");

fs.mkdirSync(RA, { recursive: true });
const fileLoi = path.join(RA, "loi.json");
const fileThongTin = path.join(RA, "mau.json");
const loi = LAM_LAI ? {} : docJson(fileLoi, {});
const thongTin = docJson(fileThongTin, {});

console.log("Đóng gói dự án (một lần)…");
const serveUrl = await bundle({ entryPoint: path.join(GOC, "src", "index.ts") });
const dsMau = await getCompositions(serveUrl);
console.log(`Có ${dsMau.length} mẫu.`);

for (const [i, mau] of dsMau.entries()) {
  const anh = path.join(RA, `${mau.id}.png`);
  const gif = path.join(RA, `${mau.id}.gif`);
  thongTin[mau.id] = {
    rong: mau.width,
    cao: mau.height,
    giay: +(mau.durationInFrames / mau.fps).toFixed(1),
    trongSuot: mau.defaultCodec === "prores",
  };
  ghiJson(fileThongTin, thongTin);
  if (!LAM_LAI && fs.existsSync(anh) && fs.existsSync(gif)) {
    console.log(`[${i + 1}/${dsMau.length}] ${mau.id}: đã có, bỏ qua`);
    continue;
  }
  const giua = Math.floor(mau.durationInFrames * (VI_TRI[mau.id] ?? 0.5));
  const nua = Math.round((GIAY_GIF * mau.fps) / 2);
  const tu = Math.max(0, giua - nua);
  const den = Math.min(mau.durationInFrames - 1, giua + nua);
  try {
    console.log(`[${i + 1}/${dsMau.length}] ${mau.id}: ảnh tĩnh khung ${giua}…`);
    await renderStill({ composition: mau, serveUrl, output: anh, frame: giua, scale: 0.5, imageFormat: "png" });
    console.log(`[${i + 1}/${dsMau.length}] ${mau.id}: GIF khung ${tu}–${den}…`);
    await renderMedia({
      composition: mau,
      serveUrl,
      codec: "gif",
      outputLocation: gif,
      frameRange: [tu, den],
      everyNthFrame: 2,
      scale: 480 / mau.width,
      concurrency: 2,
      overwrite: true,
    });
    delete loi[mau.id];
  } catch (e) {
    const tin = String(e?.message ?? e).split("\n")[0].slice(0, 300);
    console.log(`  LỖI ${mau.id}: ${tin}`);
    loi[mau.id] = tin;
    for (const f of [anh, gif]) if (fs.existsSync(f) && fs.statSync(f).size === 0) fs.unlinkSync(f);
  }
  ghiJson(fileLoi, loi);
}

// ---- Trang HTML ----
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
const coAnh = dsMau.filter((m) => fs.existsSync(path.join(RA, `${m.id}.png`)) && !loi[m.id]);
const theMau = (m) => {
    const t = thongTin[m.id];
    const coGif = fs.existsSync(path.join(RA, `${m.id}.gif`));
    const nhan = [`${t.giay} s`, `${t.rong}×${t.cao}`, t.trongSuot ? "nền trong suốt" : "toàn khung"].join(" · ");
    return `    <article class="the${t.trongSuot ? " trong-suot" : ""}">
      <div class="khung"><img src="${m.id}.png" alt="${m.id}" loading="lazy"${coGif ? ` data-gif="${m.id}.gif"` : ""}></div>
      <div class="chu">
        <div class="ten"><code>${m.id}</code><button type="button" data-ten="${m.id}">Chép tên</button></div>
        <p>${esc(DANH_MUC.mau[m.id]?.dungKhi ?? "(chưa có trong danh-muc.json)")}</p>
        <small>${nhan}</small>
      </div>
    </article>`;
};
const nhom = [...DANH_MUC.nhom, "Khác"];
const the = nhom
  .map((n) => {
    const ds = coAnh.filter((m) => (DANH_MUC.mau[m.id]?.nhom ?? "Khác") === n);
    return ds.length ? `  <h2>${esc(n)} <small>(${ds.length})</small></h2>\n  <div class="luoi">\n${ds.map(theMau).join("\n")}\n  </div>` : "";
  })
  .filter(Boolean)
  .join("\n");
const dsLoi = Object.entries(loi)
  .map(([id, tin]) => `      <li><code>${id}</code> — ${esc(tin)}</li>`)
  .join("\n");

const html = `<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mẫu đồ hoạ do-hoa</title>
<style>
  :root { --nen: #10141c; --the: #1a202c; --chu: #e8ecf2; --mo: #94a0b4; --vang: #ffcd2d; }
  * { box-sizing: border-box; }
  body { margin: 0; padding: 24px 16px 48px; background: var(--nen); color: var(--chu); font: 15px/1.5 "Segoe UI", Arial, sans-serif; }
  header, main, section { max-width: 1400px; margin: 0 auto; }
  h1 { margin: 0 0 4px; font-size: 24px; }
  header p { margin: 0 0 20px; color: var(--mo); }
  main h2 { margin: 28px 0 12px; font-size: 19px; } main h2 small { color: var(--mo); font-weight: 400; }
  .luoi { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }
  .the { background: var(--the); border-radius: 10px; overflow: hidden; }
  .khung { aspect-ratio: 16 / 9; background: #000; display: flex; align-items: center; justify-content: center; }
  .trong-suot .khung { background: repeating-conic-gradient(#3a4150 0 25%, #2a303c 0 50%) 0 0 / 20px 20px; }
  .khung img { width: 100%; height: 100%; object-fit: contain; display: block; }
  .chu { padding: 10px 12px 12px; }
  .ten { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
  code { color: var(--vang); font-size: 16px; font-weight: 600; }
  button { background: #2b3446; color: var(--chu); border: 1px solid #3d4860; border-radius: 6px; padding: 3px 10px; cursor: pointer; font: inherit; font-size: 13px; }
  button:hover { border-color: var(--vang); }
  .chu p { margin: 6px 0 4px; }
  small { color: var(--mo); }
  section { margin-top: 32px; }
  section li { color: var(--mo); margin-bottom: 4px; }
</style>
</head>
<body>
<header>
  <h1>Mẫu đồ hoạ (do-hoa) — ${coAnh.length} mẫu</h1>
  <p>Ảnh là khung giữa (vài mẫu lấy khung khác cho dễ nhận); rê chuột (hoặc chạm) vào ảnh để xem đoạn chuyển động ${GIAY_GIF} giây. Ô bàn cờ = nền trong suốt, đắp lên video. Tạo lại: <code>node scripts/lam_gallery.mjs</code></p>
</header>
<main>
${the}
</main>
${dsLoi ? `<section>
  <h2>Mẫu chưa có ảnh xem trước</h2>
  <ul>
${dsLoi}
  </ul>
</section>` : ""}
<script>
  for (const img of document.querySelectorAll("img[data-gif]")) {
    const tinh = img.src, gif = img.dataset.gif;
    const bat = () => { img.src = gif; }, tat = () => { img.src = tinh; };
    img.parentElement.addEventListener("mouseenter", bat);
    img.parentElement.addEventListener("mouseleave", tat);
    img.parentElement.addEventListener("click", () => (img.src.endsWith(".gif") ? tat() : bat()));
  }
  for (const nut of document.querySelectorAll("button[data-ten]")) {
    nut.addEventListener("click", async () => {
      const ten = nut.dataset.ten;
      try { await navigator.clipboard.writeText(ten); }
      catch { const o = document.createElement("textarea"); o.value = ten; document.body.append(o); o.select(); document.execCommand("copy"); o.remove(); }
      nut.textContent = "Đã chép"; setTimeout(() => (nut.textContent = "Chép tên"), 1200);
    });
  }
</script>
</body>
</html>
`;
fs.writeFileSync(path.join(RA, "index.html"), html);
console.log(`Xong: ${coAnh.length} mẫu có ảnh, ${Object.keys(loi).length} mẫu lỗi → gallery/index.html`);
