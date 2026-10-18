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
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const muot = Easing.bezier(0.16, 1, 0.3, 1);
const CHUYEN = 0.9; // giây vệt cọ chuyển cảnh

const dungFont = (file: string) => {
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

export const PhuNu96: React.FC<z.infer<typeof phuNu96Schema>> = ({ intro, introDai, font, canh }) => {
  const frame = useCurrentFrame();
  const { width: W, height: H, durationInFrames } = useVideoConfig();
  const t = frame / FPS;
  const het = durationInFrames / FPS;
  const ff = dungFont(font);

  // ranh giới giữa hai cảnh = điểm giữa vệt cọ
  const ranh = canh.slice(1).map((c) => c.batDau);
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
      {t > het - 4 ? <CanhHoa W={W} H={H} t={t - (het - 4)} seed="ket" so={30} /> : null}
    </AbsoluteFill>
  );
};
