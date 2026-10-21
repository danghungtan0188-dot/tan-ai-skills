// Video ghép "96 năm Hội LHPN Việt Nam": intro tranh giấy (video đã render) tách đôi như cửa mở, rồi các cảnh
// ảnh + lời đọc. Mỗi cảnh: nền là chính ảnh làm mờ trôi chậm, hạt sáng bokeh + cánh hoa rơi, ảnh trong khung
// giấy trắng xoay 3D vào rồi đung đưa, vệt sáng quét qua; bên phải số cảnh viền mảnh, tiêu đề vàng gạch bút
// lông, lời đọc hiện từng chữ (từ khoá tô vàng). Chuyển cảnh bằng vệt cọ hồng–vàng quét chéo.
// Tiếng (giọng + nhạc) ghép sau bằng ffmpeg; mốc thời gian lấy từ moc.json của giọng đọc.
import React from "react";
import {
  AbsoluteFill, Easing, Img, interpolate, OffthreadVideo, random, Sequence, spring, staticFile,
  useCurrentFrame, useVideoConfig, continueRender, delayRender,
} from "remotion";
import { z } from "zod";
import { coBan, FPS } from "../chung";

const cauSchema = z.object({ chu: z.string(), batDau: z.number(), ketThuc: z.number() });
const canhSchema = z.object({
  anh: z.string(), // tên file trong public dir
  tiLeAnh: z.number(), // rộng / cao
  so: z.string(),
  tieuDe: z.string(),
  batDau: z.number(),
  ketThuc: z.number(),
  cau: z.array(cauSchema),
  nhan: z.array(z.string()).default([]), // cụm từ tô vàng
  ketChu: z.string().default(""), // câu lớn hiện sau câu đọc cuối của cảnh (cảnh kết)
});

export const phuNu96Schema = coBan.extend({
  intro: z.string().default(""), // video intro trong public dir; trống = bỏ
  introDai: z.number().default(6),
  font: z.string().default(""), // file .ttf trong public dir; trống = Arial
  canh: z.array(canhSchema),
  // màn kết phủ toàn khung sau câu đọc cuối cùng
  ketTren: z.string().default("Chúc mừng"),
  ketDau: z.number().default(0), // > 0: màn chúc mừng đứng ngay sau intro (giây) thay vì cuối phim
  ketLon: z.string().default("20/10"),
  ketDuoi: z.string().default(""),
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const muot = Easing.bezier(0.16, 1, 0.3, 1);
const CHUYEN = 0.9; // giây vệt cọ chuyển cảnh

const useFont = (file: string) => {
  const [xong] = React.useState(() => (file ? delayRender("font") : null));
  React.useEffect(() => {
    if (!file || xong === null) return;
    const f = new FontFace("PN96", `url(${staticFile(file)})`, { weight: "100 900" });
    f.load().then((ff) => { document.fonts.add(ff); continueRender(xong); }).catch(() => continueRender(xong));
  }, [file, xong]);
  return file ? "PN96, Arial, sans-serif" : "Arial, 'Segoe UI', sans-serif";
};

// Hạt sáng bokeh trôi lên + nhấp nháy
const Bokeh: React.FC<{ W: number; H: number; t: number; seed: string }> = ({ W, H, t, seed }) => (
  <AbsoluteFill style={{ mixBlendMode: "screen" }}>
    {Array.from({ length: 26 }, (_, i) => {
      const r = (14 + random(`${seed}r${i}`) * 46) * (H / 1080);
      const x = random(`${seed}x${i}`) * W;
      const y = ((random(`${seed}y${i}`) * H - t * (12 + random(`${seed}v${i}`) * 30)) % H + H) % H;
      const a = 0.18 + 0.32 * (0.5 + 0.5 * Math.sin(t * 2 + i));
      const mau = i % 3 === 0 ? "255,214,140" : "255,170,205";
      return <div key={i} style={{ position: "absolute", left: x - r, top: y - r, width: 2 * r, height: 2 * r, borderRadius: "50%", background: `radial-gradient(circle, rgba(${mau},${a}) 0%, rgba(${mau},0) 70%)` }} />;
    })}
  </AbsoluteFill>
);

// Cánh hoa rơi chao nghiêng
const CanhHoa: React.FC<{ W: number; H: number; t: number; seed: string; so?: number }> = ({ W, H, t, seed, so = 16 }) => (
  <svg width={W} height={H} style={{ position: "absolute", filter: "drop-shadow(0 4px 4px rgba(80,10,40,0.3))" }}>
    {Array.from({ length: so }, (_, i) => {
      const s = H / 1080;
      const tuoi = t - random(`${seed}b${i}`) * 6;
      if (tuoi < 0) return null;
      const x = random(`${seed}x${i}`) * W + Math.sin(tuoi * 1.5 + i) * 50 * s;
      const y = ((tuoi * (90 + random(`${seed}v${i}`) * 80) * s) % (H + 80 * s)) - 40 * s;
      const r = (12 + random(`${seed}r${i}`) * 12) * s;
      return (
        <path key={i} d={`M 0 0 C ${-r * 0.6} ${-r * 0.4} ${-r * 0.4} ${-r * 1.2} 0 ${-r * 1.4} C ${r * 0.4} ${-r * 1.2} ${r * 0.6} ${-r * 0.4} 0 0 Z`}
          transform={`translate(${x} ${y}) rotate(${tuoi * 80 + i * 37}) scale(1 ${0.55 + 0.45 * Math.abs(Math.sin(tuoi * 2 + i))})`}
          fill={i % 4 === 0 ? "#FFD9E6" : "#F48FB1"} stroke="#FFF0F5" strokeWidth={r * 0.1} />
      );
    })}
  </svg>
);

// ---- Trang trí kiểu thiệp chúc mừng (vẽ lại bằng vector): hoa hồng đỏ, ngọc trai bóng, kim tuyến, dải lụa ----

// Một bông hồng: đế đỏ sẫm + các lớp cánh xoắn vào tâm
const Hong: React.FC<{ x: number; y: number; r: number; xoay: number; id: string }> = ({ x, y, r, xoay, id }) => (
  <g transform={`translate(${x} ${y}) rotate(${xoay})`}>
    <defs>
      <radialGradient id={`hg${id}`} cx="0.45" cy="0.4" r="0.65">
        <stop offset="0" stopColor="#FF4D5E" /><stop offset="0.55" stopColor="#D0122B" /><stop offset="1" stopColor="#7A0414" />
      </radialGradient>
    </defs>
    <circle r={r} fill={`url(#hg${id})`} />
    {Array.from({ length: 7 }, (_, k) => {
      const rr = r * (0.95 - k * 0.12);
      const g = k * 52;
      return (
        <path key={k} d={`M ${-rr} 0 A ${rr} ${rr * 0.86} 0 0 1 ${rr} 0 A ${rr * 0.85} ${rr * 0.5} 0 0 0 ${-rr} 0 Z`} transform={`rotate(${g})`}
          fill={k % 2 ? "#E8263D" : "#B30E26"} stroke="#FF8090" strokeOpacity={0.7} strokeWidth={r * 0.025} />
      );
    })}
    <circle r={r * 0.14} fill="#8E0619" />
  </g>
);

const La: React.FC<{ x: number; y: number; d: number; xoay: number }> = ({ x, y, d, xoay }) => (
  <g transform={`translate(${x} ${y}) rotate(${xoay})`}>
    <path d={`M 0 0 C ${d * 0.3} ${-d * 0.32} ${d * 0.75} ${-d * 0.3} ${d} 0 C ${d * 0.75} ${d * 0.3} ${d * 0.3} ${d * 0.32} 0 0 Z`} fill="#2E8B3A" stroke="#1B5E25" strokeWidth={d * 0.03} />
    <path d={`M ${d * 0.05} 0 L ${d * 0.92} 0`} stroke="#9BD27A" strokeWidth={d * 0.025} />
  </g>
);

// Bó 3 bông hồng + lá, bật vào bằng spring rồi đung đưa nhẹ
export const BoHong: React.FC<{ x: number; y: number; s: number; t: number; id: string; lat?: boolean }> = ({ x, y, s, t, id, lat }) => {
  const vao = spring({ frame: Math.round(t * FPS), fps: FPS, config: { damping: 11, stiffness: 90 } });
  return (
    <svg width={420 * s} height={380 * s} style={{
      position: "absolute", left: x - 210 * s, top: y - 190 * s, overflow: "visible",
      scale: `${(lat ? -1 : 1) * vao} ${vao}`, rotate: `${Math.sin(t * 1.1) * 3}deg`,
      filter: `drop-shadow(0 ${10 * s}px ${14 * s}px rgba(40,0,10,0.45))`,
    }}>
      <g transform={`translate(${210 * s} ${190 * s})`}>
        <La x={-40 * s} y={20 * s} d={150 * s} xoay={150} />
        <La x={10 * s} y={40 * s} d={140 * s} xoay={95} />
        <La x={30 * s} y={-30 * s} d={130 * s} xoay={-60} />
        <La x={-30 * s} y={-40 * s} d={120 * s} xoay={-130} />
        <Hong x={-60 * s} y={-30 * s} r={70 * s} xoay={10} id={`${id}a`} />
        <Hong x={55 * s} y={-5 * s} r={64 * s} xoay={-40} id={`${id}b`} />
        <Hong x={-5 * s} y={55 * s} r={60 * s} xoay={70} id={`${id}c`} />
      </g>
    </svg>
  );
};

// Ngọc trai bóng hồng–trắng trôi nhấp nhô
export const NgocTrai: React.FC<{ W: number; H: number; t: number; seed: string; so?: number }> = ({ W, H, t, seed, so = 9 }) => (
  <AbsoluteFill>
    {Array.from({ length: so }, (_, i) => {
      const s = H / 1080;
      const r = (22 + random(`${seed}nr${i}`) * 34) * s;
      const x = random(`${seed}nx${i}`) * W + Math.sin(t * 0.5 + i) * 26 * s;
      // chỉ ở dải mép trên / dưới: không đè tiêu đề và lời đọc
      const y = (i % 2 ? H * 0.02 + random(`${seed}ny${i}`) * H * 0.1 : H * 0.86 + random(`${seed}ny${i}`) * H * 0.12) + Math.cos(t * 0.7 + i * 2) * 22 * s;
      const hong = i % 3 !== 0;
      return (
        <div key={i} style={{
          position: "absolute", left: x - r, top: y - r, width: 2 * r, height: 2 * r, borderRadius: "50%",
          background: hong
            ? "radial-gradient(circle at 34% 30%, #FFFFFF 0%, #FFD3EC 18%, #F48CC8 55%, #B84D93 100%)"
            : "radial-gradient(circle at 34% 30%, #FFFFFF 0%, #F6F1FF 25%, #D9CCF0 65%, #9C8BC4 100%)",
          boxShadow: `0 ${6 * s}px ${14 * s}px rgba(60,0,30,0.35), inset ${-4 * s}px ${-6 * s}px ${10 * s}px rgba(90,20,70,0.35)`,
          opacity: interpolate(t, [0, 0.6], [0, 0.95], kep),
        }} />
      );
    })}
  </AbsoluteFill>
);

// Kim tuyến dạng thanh (tím / vàng / hồng) lật 3D khi rơi
export const KimTuyen: React.FC<{ W: number; H: number; t: number; seed: string; so?: number }> = ({ W, H, t, seed, so = 18 }) => (
  <AbsoluteFill>
    {Array.from({ length: so }, (_, i) => {
      const s = H / 1080;
      const v = (40 + random(`${seed}kv${i}`) * 50) * s;
      const y = ((random(`${seed}ky${i}`) * H + t * v) % (H + 100 * s)) - 50 * s;
      const x = random(`${seed}kx${i}`) * W + Math.sin(t * 1.3 + i) * 30 * s;
      const [a, b] = [["#B57CFF", "#6A2FD1"], ["#FFE27A", "#E0A21C"], ["#FF9CC2", "#D94C86"]][i % 3];
      const lat = Math.cos(t * (2 + random(`${seed}kl${i}`) * 3) + i);
      return (
        <div key={i} style={{
          position: "absolute", left: x, top: y, width: 18 * s, height: 46 * s, borderRadius: 3 * s,
          background: `linear-gradient(${lat > 0 ? 90 : 270}deg, ${a}, ${b})`,
          rotate: `${random(`${seed}kg${i}`) * 360 + t * 40}deg`, scale: `1 ${Math.max(0.12, Math.abs(lat))}`,
          boxShadow: `0 ${3 * s}px ${6 * s}px rgba(40,0,30,0.3)`, opacity: interpolate(t, [0, 0.5], [0, 0.9], kep),
        }} />
      );
    })}
  </AbsoluteFill>
);

// Dải lụa lượn sóng ở mép trên và mép dưới
export const DaiLua: React.FC<{ W: number; H: number; t: number }> = ({ W, H, t }) => {
  const song = (y0: number, bien: number, pha: number, day: number) => {
    const d = Array.from({ length: 25 }, (_, k) => {
      const x = (k / 24) * W;
      return `${k ? "L" : "M"} ${x} ${y0 + Math.sin(k / 24 * Math.PI * 2.2 + t * 0.9 + pha) * bien}`;
    }).join(" ");
    return { d, day };
  };
  const s = H / 1080;
  const dai = [
    { ...song(H * 0.06, 22 * s, 0, 30 * s), mau: "rgba(255,214,235,0.55)" },
    { ...song(H * 0.09, 18 * s, 1.6, 14 * s), mau: "rgba(255,255,255,0.45)" },
    { ...song(H * 0.93, 24 * s, 2.4, 34 * s), mau: "rgba(255,190,220,0.5)" },
    { ...song(H * 0.96, 16 * s, 4.0, 14 * s), mau: "rgba(255,255,255,0.45)" },
  ];
  return (
    <svg width={W} height={H} style={{ position: "absolute", filter: `blur(${1.2 * s}px)` }}>
      {dai.map((x, i) => <path key={i} d={x.d} fill="none" stroke={x.mau} strokeWidth={x.day} strokeLinecap="round" />)}
    </svg>
  );
};

// Một chữ của câu đang đọc: trồi lên + bỏ mờ theo thứ tự
const Chu: React.FC<{ chu: string; t: number; vao: number; vang: boolean; s: number }> = ({ chu, t, vao, vang, s }) => (
  <span style={{
    display: "inline-block", marginRight: 14 * s, color: vang ? "#FFD86B" : "#FFFFFF",
    opacity: interpolate(t, [vao, vao + 0.35], [0, 1], kep),
    translate: `0px ${interpolate(t, [vao, vao + 0.45], [22, 0], { ...kep, easing: muot }) * s}px`,
    filter: `blur(${interpolate(t, [vao, vao + 0.35], [8, 0], kep) * s}px)`,
  }}>
    {chu}
  </span>
);

const Canh: React.FC<{ c: z.infer<typeof canhSchema>; font: string; W: number; H: number }> = ({ c, font, W, H }) => {
  const frame = useCurrentFrame(); // tính từ đầu Sequence
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const tuyetDoi = c.batDau + t;
  const dai = c.ketThuc - c.batDau;
  const s = H / 1080;

  // khung ảnh: cao theo tỉ lệ, đặt ở 1/3 trái
  const caoKhung = c.tiLeAnh < 0.75 ? H * 0.84 : H * 0.74;
  const rongKhung = caoKhung * c.tiLeAnh;
  const vaoKhung = spring({ frame, fps, config: { damping: 14, stiffness: 70, mass: 0.9 } });
  const xoayY = interpolate(vaoKhung, [0, 1], [38, 9]) + Math.sin(t * 0.8) * 3;
  const xoayX = Math.sin(t * 0.6 + 1) * 1.6;
  const queSang = interpolate(t, [0.7, 1.9], [-0.6, 1.4], kep);

  // câu đang đọc (mốc tuyệt đối)
  const cau = c.cau.find((x) => tuyetDoi >= x.batDau - 0.25 && tuyetDoi < x.ketThuc + 0.35) ?? null;
  const chuCau = cau ? cau.chu.split(" ") : [];
  const daiCau = cau ? Math.max(0.6, cau.ketThuc - cau.batDau) : 1;
  const laVang = (i: number) => c.nhan.some((n) => {
    const tu = n.split(" ");
    for (let k = 0; k < tu.length; k++) {
      const dau = i - k;
      if (dau >= 0 && tu.every((w, j) => (chuCau[dau + j] ?? "").replace(/[,.!;:]/g, "") === w)) return true;
    }
    return false;
  });
  const raCau = cau ? interpolate(tuyetDoi, [cau.ketThuc + 0.05, cau.ketThuc + 0.35], [1, 0], kep) : 0;
  const cuoi = c.cau.length ? c.cau[c.cau.length - 1].ketThuc : 0; // hết câu đọc cuối của cảnh

  const tieuDeVao = interpolate(t, [0.4, 1.1], [0, 1], { ...kep, easing: muot });
  const gach = interpolate(t, [0.8, 1.6], [0, 1], { ...kep, easing: muot });

  return (
    <AbsoluteFill style={{ fontFamily: font, overflow: "hidden", backgroundColor: "#2A0B1E" }}>
      {/* nền: chính ảnh làm mờ, trôi chậm */}
      <AbsoluteFill style={{ scale: `${1.18 + 0.06 * (t / dai)}`, translate: `${-30 * s * (t / dai)}px 0px` }}>
        <Img src={staticFile(c.anh)} style={{ width: "100%", height: "100%", objectFit: "cover", filter: "blur(36px) brightness(0.82) saturate(1.35)" }} />
      </AbsoluteFill>
      <AbsoluteFill style={{ background: "linear-gradient(100deg, rgba(120,20,70,0.08) 0%, rgba(110,18,64,0.32) 55%, rgba(80,10,48,0.55) 100%)" }} />
      <Bokeh W={W} H={H} t={tuyetDoi} seed={c.so} />
      <DaiLua W={W} H={H} t={tuyetDoi} />
      <NgocTrai W={W} H={H} t={t} seed={`n${c.so}`} />
      <KimTuyen W={W} H={H} t={t} seed={`k${c.so}`} so={14} />

      {/* số cảnh viền mảnh, chìm phía sau chữ */}
      <div style={{
        position: "absolute", right: 60 * s, bottom: 10 * s, fontSize: 320 * s, fontWeight: 900, lineHeight: 1,
        color: "transparent", WebkitTextStroke: `${3 * s}px rgba(255,214,140,0.38)`,
        opacity: interpolate(t, [0.2, 1], [0, 1], kep), translate: `${interpolate(t, [0.2, 1.2], [60, 0], { ...kep, easing: muot }) * s}px 0px`,
      }}>{c.so}</div>

      {/* khung ảnh giấy trắng xoay 3D */}
      <div style={{ position: "absolute", left: W * 0.07, top: (H - caoKhung) / 2, width: rongKhung, height: caoKhung, perspective: 1800 * s }}>
        <div style={{
          width: "100%", height: "100%", transform: `rotateY(${xoayY}deg) rotateX(${xoayX}deg) translateX(${(1 - vaoKhung) * -260 * s}px)`,
          opacity: interpolate(vaoKhung, [0, 0.35], [0, 1], kep),
          background: "#FFF8F2", padding: 16 * s, boxSizing: "border-box", borderRadius: 8 * s,
          boxShadow: `0 ${30 * s}px ${60 * s}px rgba(30,0,15,0.55), 0 0 0 ${2 * s}px rgba(255,215,150,0.6)`,
        }}>
          <div style={{ width: "100%", height: "100%", overflow: "hidden", borderRadius: 4 * s, position: "relative" }}>
            <Img src={staticFile(c.anh)} style={{ width: "100%", height: "100%", objectFit: "cover", scale: `${1 + 0.07 * (t / dai)}` }} />
            <div style={{
              position: "absolute", inset: 0, mixBlendMode: "overlay",
              background: `linear-gradient(115deg, transparent ${queSang * 100 - 18}%, rgba(255,255,255,0.85) ${queSang * 100}%, transparent ${queSang * 100 + 18}%)`,
            }} />
          </div>
        </div>
      </div>

      {/* bó hồng cài góc trên trái khung ảnh */}
      {t > 0.7 ? <BoHong x={W * 0.07 + 30 * s} y={(H - caoKhung) / 2 + 40 * s} s={0.62 * s} t={t - 0.7} id={`c${c.so}`} /> : null}

      {/* tiêu đề + lời đọc ở bên phải */}
      <div style={{ position: "absolute", left: W * 0.07 + rongKhung + W * 0.06, right: W * 0.05, top: H * 0.13, bottom: H * 0.2, display: "flex", flexDirection: "column", gap: 26 * s }}>
        <div style={{ opacity: tieuDeVao, translate: `0px ${(1 - tieuDeVao) * 30 * s}px` }}>
          <div style={{ fontSize: 30 * s, fontWeight: 700, letterSpacing: 6 * s, color: "#FFC1D6" }}>20/10/1930 – 20/10/2026</div>
          <div style={{ fontSize: 66 * s, fontWeight: 900, lineHeight: 1.12, color: "#FFD86B", textShadow: `0 ${4 * s}px ${14 * s}px rgba(40,0,20,0.6)` }}>{c.tieuDe}</div>
          <svg width={420 * s} height={22 * s} style={{ marginTop: 8 * s }}>
            <path d={`M ${4 * s} ${14 * s} C ${120 * s} ${4 * s}, ${280 * s} ${20 * s}, ${414 * s} ${8 * s}`} fill="none" stroke="#F06A93" strokeWidth={9 * s} strokeLinecap="round"
              strokeDasharray={440 * s} strokeDashoffset={(1 - gach) * 440 * s} />
          </svg>
        </div>
        <div style={{ flex: 1, display: "flex", alignItems: "center" }}>
          {cau ? (
            <div key={cau.batDau} style={{ fontSize: 58 * s, fontWeight: 700, lineHeight: 1.38, opacity: raCau, textShadow: `0 ${3 * s}px ${12 * s}px rgba(30,0,15,0.75)` }}>
              {chuCau.map((w, i) => (
                <Chu key={i} chu={w} t={tuyetDoi} s={s} vang={laVang(i)} vao={cau.batDau - 0.2 + (i / Math.max(1, chuCau.length)) * daiCau * 0.75} />
              ))}
            </div>
          ) : c.ketChu && tuyetDoi > cuoi + 0.3 ? (
            <div style={{
              fontSize: 96 * s, fontWeight: 900, lineHeight: 1.1, color: "#FFD86B",
              textShadow: `0 0 ${30 * s}px rgba(255,200,90,0.75), 0 ${4 * s}px ${14 * s}px rgba(40,0,20,0.6)`,
              scale: `${interpolate(tuyetDoi, [cuoi + 0.3, cuoi + 1.0], [1.4, 1], { ...kep, easing: muot })}`,
              opacity: interpolate(tuyetDoi, [cuoi + 0.3, cuoi + 0.7], [0, 1], kep),
            }}>{c.ketChu}</div>
          ) : null}
        </div>
      </div>

      <CanhHoa W={W} H={H} t={t + 3} seed={`p${c.so}`} so={14} />
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at center, transparent 55%, rgba(20,0,10,0.55) 100%)" }} />
    </AbsoluteFill>
  );
};

// Màn kết toàn khung: nền chuyển sắc + tia sáng xoay, cánh hoa bung toả, sao lấp lánh,
// "Chúc mừng" trắng phát sáng, "20/10" vàng ánh kim nổi khối có vệt sáng lướt, dải băng đỏ dòng phụ.
const MANKet: React.FC<{ W: number; H: number; t: number; font: string; tren: string; lon: string; duoi: string }> = ({ W, H, t, font, tren, lon, duoi }) => {
  const s = H / 1080;
  const vao = interpolate(t, [0, 0.6], [0, 1], { ...kep, easing: muot });
  const nay = spring({ frame: Math.round((t - 0.35) * FPS), fps: FPS, config: { damping: 9, stiffness: 120, mass: 0.8 } });
  const quet = interpolate(t, [1.1, 2.1], [-30, 130], kep);
  const bang = interpolate(t, [0.9, 1.6], [0, 1], { ...kep, easing: muot });
  const tia = Array.from({ length: 18 }, (_, i) => i * 20);
  const cx = W / 2, cy = H * 0.47;
  return (
    <AbsoluteFill style={{ fontFamily: font, opacity: vao }}>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 45%, #E8507F 0%, #A3164F 45%, #4A0626 100%)" }} />
      {/* tia sáng xoay */}
      <svg width={W} height={H} style={{ position: "absolute", opacity: 0.16, mixBlendMode: "screen" }}>
        <g transform={`translate(${cx} ${cy}) rotate(${t * 10})`}>
          {tia.map((g) => (
            <path key={g} d={`M 0 0 L ${W} ${-W * 0.09} L ${W} ${W * 0.09} Z`} transform={`rotate(${g})`} fill="url(#tiaMau)" />
          ))}
        </g>
        <defs>
          <linearGradient id="tiaMau" x1="0" x2="1">
            <stop offset="0" stopColor="#FFE9A8" stopOpacity="0.9" />
            <stop offset="1" stopColor="#FFE9A8" stopOpacity="0" />
          </linearGradient>
        </defs>
      </svg>
      {/* cánh hoa bung toả từ tâm */}
      <svg width={W} height={H} style={{ position: "absolute" }}>
        {Array.from({ length: 46 }, (_, i) => {
          const goc = random(`kg${i}`) * Math.PI * 2;
          const v = (380 + random(`kv${i}`) * 620) * s;
          const tt = Math.max(0, t - 0.3);
          const x = cx + Math.cos(goc) * v * (1 - Math.exp(-tt * 1.6));
          const y = cy + Math.sin(goc) * v * (1 - Math.exp(-tt * 1.6)) + 60 * s * tt * tt;
          const r = (14 + random(`kr${i}`) * 16) * s;
          const mau = ["#FFD9E6", "#F48FB1", "#FFD86B", "#FFFFFF"][i % 4];
          return t > 0.3 ? (
            <path key={i} d={`M 0 0 C ${-r * 0.6} ${-r * 0.4} ${-r * 0.4} ${-r * 1.2} 0 ${-r * 1.4} C ${r * 0.4} ${-r * 1.2} ${r * 0.6} ${-r * 0.4} 0 0 Z`}
              transform={`translate(${x} ${y}) rotate(${tt * 160 + i * 31})`} fill={mau} opacity={0.95} />
          ) : null;
        })}
      </svg>
      {/* sao lấp lánh */}
      {Array.from({ length: 22 }, (_, i) => {
        const x = random(`sx${i}`) * W, y = random(`sy${i}`) * H;
        const nhay = Math.max(0, Math.sin(t * 5 + i * 1.7));
        const r = (10 + random(`sr${i}`) * 16) * s;
        return (
          <svg key={i} width={r * 2} height={r * 2} style={{ position: "absolute", left: x - r, top: y - r, opacity: nhay * vao, scale: `${0.6 + 0.6 * nhay}` }}>
            <path d={`M ${r} 0 Q ${r * 1.12} ${r * 0.88} ${r * 2} ${r} Q ${r * 1.12} ${r * 1.12} ${r} ${r * 2} Q ${r * 0.88} ${r * 1.12} 0 ${r} Q ${r * 0.88} ${r * 0.88} ${r} 0 Z`} fill="#FFF6C8" />
          </svg>
        );
      })}
      <NgocTrai W={W} H={H} t={t} seed="ket" so={10} />
      <KimTuyen W={W} H={H} t={t} seed="ket" so={22} />
      {t > 0.5 ? <BoHong x={W * 0.13} y={H * 0.2} s={0.95 * s} t={t - 0.5} id="k1" /> : null}
      {t > 0.8 ? <BoHong x={W * 0.88} y={H * 0.82} s={0.8 * s} t={t - 0.8} id="k2" lat /> : null}
      {/* chữ */}
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", paddingBottom: H * 0.1 }}>
        <div style={{
          fontSize: 130 * s, fontWeight: 900, color: "#FFFFFF", fontStyle: "italic",
          WebkitTextStroke: `${3 * s}px #F06A93`, paintOrder: "stroke fill",
          textShadow: `0 0 ${34 * s}px rgba(255,190,220,0.95)`,
          translate: `0px ${(1 - vao) * -60 * s}px`, marginBottom: 6 * s,
        }}>{tren}</div>
        <div style={{ position: "relative", fontSize: 330 * s, fontWeight: 900, lineHeight: 1, scale: `${0.3 + 0.7 * nay}` }}>
          {/* lớp nổi khối phía sau */}
          <div style={{ position: "absolute", inset: 0, color: "#7A0A2E", translate: `${10 * s}px ${14 * s}px`, filter: `drop-shadow(0 ${16 * s}px ${30 * s}px rgba(40,0,15,0.6))` }}>{lon}</div>
          {/* mặt chữ vàng ánh kim + vệt sáng lướt */}
          <div style={{
            position: "relative", color: "transparent", WebkitBackgroundClip: "text", backgroundClip: "text",
            backgroundImage: `linear-gradient(105deg, transparent ${quet - 12}%, rgba(255,255,255,0.95) ${quet}%, transparent ${quet + 12}%), linear-gradient(180deg, #FFF8D6 0%, #FFD86B 42%, #E9A23B 70%, #FFE7A0 100%)`,
          }}>{lon}</div>
        </div>
        {duoi ? (
          <div style={{ marginTop: 26 * s, scale: `${bang} 1`, opacity: bang, background: "#C8102E", padding: `${14 * s}px ${46 * s}px`, borderRadius: 6 * s,
            boxShadow: `0 ${10 * s}px ${24 * s}px rgba(40,0,15,0.5), inset 0 0 0 ${3 * s}px #F7C873` }}>
            <div style={{ fontSize: 40 * s, fontWeight: 700, color: "#FFE7A0", letterSpacing: 1 * s, opacity: interpolate(bang, [0.6, 1], [0, 1], kep) }}>{duoi}</div>
          </div>
        ) : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// Vệt cọ hồng–vàng quét chéo che kín giữa hai cảnh
const VetCo: React.FC<{ W: number; H: number; p: number }> = ({ W, H, p }) => {
  const x = interpolate(p, [0, 1], [-1.6, 1.6]) * W;
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div style={{
        position: "absolute", top: -H * 0.5, left: x - W * 0.35, width: W * 0.75, height: H * 2, rotate: "18deg",
        background: "linear-gradient(90deg, rgba(240,106,147,0) 0%, #F06A93 14%, #F7A8C4 45%, #FFD86B 72%, rgba(255,216,107,0) 100%)",
        boxShadow: `0 0 ${H * 0.08}px rgba(255,200,220,0.8)`,
      }} />
    </AbsoluteFill>
  );
};

export const PhuNu96: React.FC<z.infer<typeof phuNu96Schema>> = ({ intro, introDai, font, canh, ketTren, ketLon, ketDuoi, ketDau }) => {
  const frame = useCurrentFrame();
  const { width: W, height: H, durationInFrames } = useVideoConfig();
  const t = frame / FPS;
  const het = durationInFrames / FPS;
  const ff = useFont(font);

  // ranh giới giữa hai cảnh = điểm giữa vệt cọ
  const ranh = (ketDau > 0 ? canh : canh.slice(1)).map((c) => c.batDau);
  const fr = (sec: number) => Math.round(sec * FPS);

  // intro tách đôi như cửa mở trong 1 giây cuối, lộ cảnh 1 phía dưới
  const cua = intro ? interpolate(t, [introDai - 1.1, introDai], [0, 1], { ...kep, easing: Easing.in(Easing.cubic) }) : 1;
  const ketThuc = interpolate(t, [het - 1.0, het], [1, 0], kep);

  return (
    <AbsoluteFill style={{ backgroundColor: "#000", opacity: ketThuc }}>
      {canh.map((c, i) => {
        const tu = i === 0 ? c.batDau : c.batDau;
        const den = i + 1 < canh.length ? canh[i + 1].batDau : het;
        return (
          <Sequence key={c.so} from={fr(tu)} durationInFrames={Math.max(1, fr(den) - fr(tu))}>
            <Canh c={c} font={ff} W={W} H={H} />
          </Sequence>
        );
      })}
      {/* màn chúc mừng ngay sau intro: nằm dưới cửa giấy và dưới vệt cọ sang cảnh 1 */}
      {ketDau > 0 && t >= canh[0].batDau - ketDau && t < canh[0].batDau ? (
        <MANKet W={W} H={H} t={t - (canh[0].batDau - ketDau)} font={ff} tren={ketTren} lon={ketLon} duoi={ketDuoi} />
      ) : null}
      {ranh.map((b) => {
        const p = interpolate(t, [b - CHUYEN / 2, b + CHUYEN / 2], [0, 1], kep);
        return p > 0 && p < 1 ? <VetCo key={b} W={W} H={H} p={p} /> : null;
      })}
      {intro && cua < 1 ? (
        <AbsoluteFill>
          <Sequence durationInFrames={fr(introDai)}>
            <AbsoluteFill style={{ clipPath: "inset(0 50% 0 0)", translate: `${-cua * W * 0.55}px 0px`, filter: "drop-shadow(10px 0 24px rgba(0,0,0,0.6))" }}>
              <OffthreadVideo src={staticFile(intro)} muted />
            </AbsoluteFill>
            <AbsoluteFill style={{ clipPath: "inset(0 0 0 50%)", translate: `${cua * W * 0.55}px 0px`, filter: "drop-shadow(-10px 0 24px rgba(0,0,0,0.6))" }}>
              <OffthreadVideo src={staticFile(intro)} muted />
            </AbsoluteFill>
          </Sequence>
        </AbsoluteFill>
      ) : null}
      {(() => {
        if (ketDau > 0) return null;
        const cuoiCung = canh.length ? canh[canh.length - 1].cau : [];
        const tKet = (cuoiCung.length ? cuoiCung[cuoiCung.length - 1].ketThuc : het - 4) + 0.3;
        return t >= tKet ? <MANKet W={W} H={H} t={t - tKet} font={ff} tren={ketTren} lon={ketLon} duoi={ketDuoi} /> : null;
      })()}
    </AbsoluteFill>
  );
};
