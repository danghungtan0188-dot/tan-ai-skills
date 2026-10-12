// Thẻ tiêu chí kiểu phim tài liệu: nền nâu trầm, `so` thẻ "TIÊU CHÍ n" hiện lần lượt; thẻ trong `dat` sáng lên đúng
// mốc lời đọc (`taiDat`), các thẻ khác mờ. Tới `taiHoiTu` thẻ không đạt tan đi, thẻ đạt dồn vào giữa; tới `taiKet`
// vạch đồng kéo ra và dòng kết luận hiện bên dưới. Chỉ ghi số tiêu chí — nội dung tiêu chí không tự viết. Toàn khung.
// kieu "rucro": từ `taiHoiTu` nền bừng sáng kiểu VHTV (tâm sáng tỏa tia, vệt sáng bay ra, hạt lấp lánh, bóng hàng dừa,
// mái nhà, cột cờ ở đáy) màu xanh lam đậm + vàng kim; kết luận chữ vàng kim lớn (xuống dòng bằng \n).
import React from "react";
import { AbsoluteFill, Easing, interpolate, random, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FPS } from "../chung";

export const tieuChiSchema = coBan.extend({
  tieuDe: z.string().default(""),
  so: z.number().default(5),
  dat: z.array(z.number()),
  taiHien: z.number().default(0.5),
  taiDat: z.array(z.number()),
  dongDat: z.string().default(""),
  taiHoiTu: z.number(),
  ketLuan: z.string().default(""),
  taiKet: z.number(),
  kieu: z.enum(["tram", "rucro"]).default("tram"),
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const CHU_CHAN = "'Times New Roman', Cambria, serif";
const KEM = "#F1E4C8";
const DONG = "#C9A46A";
const W_THE = 230;
const KHE = 46;

const VANG = "#FFD98A";
const TOI = "#04102b";

// bóng làng quê ở đáy khung (toạ độ 1920x1080): hàng dừa, mái nhà, cột cờ; đường chân trời viền vàng kim
const Dua: React.FC<{ x: number; h: number; ng: number }> = ({ x, h, ng }) => (
  <g transform={`translate(${x} 960) rotate(${ng})`}>
    <path d={`M0,0 Q${ng * 3},${-h / 2} 4,${-h}`} stroke={TOI} strokeWidth={9} fill="none" />
    {[-110, -70, -35, 0, 35, 70, 110].map((a) => {
      const dx = Math.sin((a * Math.PI) / 180) * 120;
      return <path key={a} d={`M4,${-h} q${dx / 2},${-30 + Math.abs(a) * 0.45} ${dx},${Math.abs(a) * 0.9 - 10}`}
        stroke={TOI} strokeWidth={10} fill="none" strokeLinecap="round" />;
    })}
  </g>
);

const BongLang: React.FC = () => (
  <svg width="100%" height="100%" viewBox="0 0 1920 1080" preserveAspectRatio="none" style={{ position: "absolute", inset: 0 }}>
    <defs>
      <linearGradient id="vienVang" x1="0" x2="1">
        <stop offset="0" stopColor={VANG} stopOpacity="0" /><stop offset="0.5" stopColor={VANG} /><stop offset="1" stopColor={VANG} stopOpacity="0" />
      </linearGradient>
    </defs>
    {[[160, 230, -4], [300, 280, 3], [520, 200, 6], [1480, 300, -3], [1640, 240, 5], [1780, 270, -2]].map(([x, h, n]) => <Dua key={x} x={x} h={h} ng={n} />)}
    <path d="M380,960 l70,-55 l70,55 z M700,965 l55,-40 l55,40 z M1180,965 l90,-70 l90,70 z M1290,960 l60,-45 l60,45 z" fill={TOI} />
    <rect x="1003" y="760" width="5" height="200" fill={TOI} />
    <path d="M1008,764 q40,-12 80,4 q-40,14 -80,30 z" fill={TOI} />
    <path d="M0,1080 L0,975 Q960,905 1920,975 L1920,1080 Z" fill="#030b22" />
    <path d="M0,975 Q960,905 1920,975" stroke="url(#vienVang)" strokeWidth={4} fill="none" />
  </svg>
);

const NenRucRo: React.FC<{ t: number; s: number }> = ({ t, s }) => (
  <AbsoluteFill>
    <AbsoluteFill style={{ background: "radial-gradient(circle at 50% 44%, #3d86ee 0%, #1747a0 26%, #0a2361 58%, #040d29 100%)" }} />
    <AbsoluteFill style={{ background: "repeating-conic-gradient(from 0deg at 50% 44%, rgba(255,217,138,0.16) 0deg 3deg, transparent 3deg 14deg)",
      rotate: `${t * 3}deg`, transformOrigin: "50% 44%", mixBlendMode: "screen",
      WebkitMaskImage: "radial-gradient(circle at 50% 44%, black 0%, transparent 62%)" }} />
    <svg width={1920 * s} height={1080 * s} viewBox="0 0 1920 1080" style={{ position: "absolute" }}>
      {Array.from({ length: 46 }, (_, i) => {
        const a = random(`a${i}`) * Math.PI * 2;
        const r = ((t * (0.22 + random(`v${i}`) * 0.3) + random(`p${i}`)) % 1) * 1250;
        const L = 90 + random(`l${i}`) * 140;
        const r1 = Math.max(0, r - L);
        return (
          <g key={i} opacity={Math.min(1, r / 200)}>
            <line x1={960 + Math.cos(a) * r1} y1={475 + Math.sin(a) * r1} x2={960 + Math.cos(a) * r} y2={475 + Math.sin(a) * r}
              stroke={VANG} strokeOpacity={0.55} strokeWidth={2.5} strokeLinecap="round" />
            <circle cx={960 + Math.cos(a) * r} cy={475 + Math.sin(a) * r} r={5 + random(`r${i}`) * 4} fill="#FFF3D6"
              style={{ filter: "drop-shadow(0 0 8px #FFD98A)" }} />
          </g>
        );
      })}
      {Array.from({ length: 70 }, (_, i) => (
        <circle key={`b${i}`} cx={random(`bx${i}`) * 1920} cy={random(`by${i}`) * 900} r={1.5 + random(`br${i}`) * 3.5} fill="#FFF0C8"
          opacity={0.15 + 0.6 * Math.abs(Math.sin(t * (1 + random(`bt${i}`) * 2) + i))} />
      ))}
    </svg>
    <AbsoluteFill style={{ background: "radial-gradient(circle at 50% 44%, rgba(255,247,225,0.85) 0%, rgba(255,215,140,0.35) 7%, transparent 22%)",
      opacity: 0.85 + 0.15 * Math.sin(t * 2.2) }} />
    <BongLang />
  </AbsoluteFill>
);

export const TieuChi: React.FC<z.infer<typeof tieuChiSchema>> = (p) => {
  const frame = useCurrentFrame();
  const { width, durationInFrames } = useVideoConfig();
  const s = width / 1920;
  const t = frame / FPS;
  const het = durationInFrames / FPS;
  const nen = interpolate(t, [0, 0.6, het - 0.8, het], [0, 1, 1, 0], kep);
  const hoiTu = interpolate(t, [p.taiHoiTu, p.taiHoiTu + 1.4], [0, 1], { ...kep, easing: Easing.inOut(Easing.cubic) });
  const ket = interpolate(t, [p.taiKet, p.taiKet + 1.2], [0, 1], { ...kep, easing: Easing.out(Easing.cubic) });
  const tong = p.so * W_THE + (p.so - 1) * KHE;
  const x0 = (1920 - tong) / 2;
  const tongDat = p.dat.length * W_THE + (p.dat.length - 1) * 24;
  const xDat0 = (1920 - tongDat) / 2;
  const daDat = p.taiDat.filter((x) => t >= x + 0.3).length;
  const rucRo = p.kieu === "rucro" ? interpolate(t, [p.taiHoiTu - 0.2, p.taiHoiTu + 1.3], [0, 1], kep) : 0;

  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse 75% 70% at 50% 45%, #3a2a18 0%, #1a1108 70%, #0a0603 100%)", opacity: nen }}>
      {rucRo > 0 ? <AbsoluteFill style={{ opacity: rucRo }}><NenRucRo t={t} s={s} /></AbsoluteFill> : null}
      {p.tieuDe ? (
        <div style={{ position: "absolute", top: 120 * s, left: 0, right: 0, textAlign: "center", fontFamily: CHU_CHAN, fontStyle: "italic",
          fontSize: 50 * s, color: KEM, opacity: interpolate(t, [0.2, 1.0], [0, 1], kep) * (1 - hoiTu) }}>{p.tieuDe}</div>
      ) : null}
      {Array.from({ length: p.so }, (_, i) => {
        const n = i + 1;
        const k = p.dat.indexOf(n);
        const vao = interpolate(t, [p.taiHien + i * 0.18, p.taiHien + i * 0.18 + 0.6], [0, 1], { ...kep, easing: Easing.out(Easing.cubic) });
        const sang = k >= 0 ? interpolate(t, [p.taiDat[k], p.taiDat[k] + 0.6], [0, 1], { ...kep, easing: Easing.out(Easing.back(1.6)) }) : 0;
        const xGoc = x0 + i * (W_THE + KHE);
        const x = k >= 0 ? xGoc + (xDat0 + k * (W_THE + 24) - xGoc) * hoiTu : xGoc;
        const y = 340 - 60 * hoiTu - (p.kieu === "rucro" ? 150 * ket : 0);
        // chưa tới lời đọc thì mọi thẻ mờ như nhau — không lộ thẻ đạt trước
        const mo = k >= 0 ? 0.45 + 0.55 * sang : 0.45 * (1 - hoiTu);
        return (
          <div key={n} style={{ position: "absolute", left: x * s, top: y * s, width: W_THE * s, height: 300 * s, opacity: vao * mo,
            translate: `0 ${(1 - vao) * 30 * s}px`, scale: 1 + 0.06 * sang * (1 - hoiTu),
            border: `${3 * s}px solid ${sang > 0.5 ? DONG : "rgba(201,164,106,0.45)"}`, borderRadius: 6 * s,
            // nền rực rỡ: thẻ nền xanh đặc để vệt sáng không xuyên qua chữ số
            background: rucRo > 0 ? `linear-gradient(rgba(8,26,74,${0.88 * rucRo}), rgba(4,14,44,${0.92 * rucRo})), rgba(241,228,200,${0.04 + 0.14 * sang})`
              : `rgba(241,228,200,${0.04 + 0.14 * sang})`, boxShadow: `0 0 ${50 * sang * s}px rgba(255,190,110,${0.35 * sang})`,
            display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
            <div style={{ fontFamily: CHU_CHAN, fontSize: 30 * s, letterSpacing: 4 * s, color: KEM, opacity: 0.85 }}>TIÊU CHÍ</div>
            <div style={{ fontFamily: CHU_CHAN, fontWeight: 700, fontSize: 150 * s, lineHeight: 1.05, color: sang > 0.5 ? "#FFE7B0" : KEM }}>{n}</div>
            <svg width={60 * s} height={44 * s} viewBox="0 0 60 44" style={{ opacity: sang }}>
              <path d="M6 22 L24 38 L54 6" fill="none" stroke={DONG} strokeWidth={7} strokeLinecap="round" strokeLinejoin="round"
                strokeDasharray="80" strokeDashoffset={80 * (1 - sang)} />
            </svg>
          </div>
        );
      })}
      {p.dongDat ? (
        <div style={{ position: "absolute", top: 700 * s, left: 0, right: 0, textAlign: "center", fontFamily: CHU_CHAN, fontStyle: "italic",
          fontSize: 52 * s, color: KEM, opacity: interpolate(daDat, [p.dat.length - 0.5, p.dat.length], [0, 1], kep) * (1 - hoiTu) }}>{p.dongDat}</div>
      ) : null}
      {p.kieu === "rucro" ? (
        <div style={{ position: "absolute", top: 500 * s, left: 0, right: 0, textAlign: "center", whiteSpace: "pre-line",
          fontFamily: "Arial, 'Segoe UI', sans-serif", fontWeight: 900, fontSize: 112 * s, lineHeight: 1.12, letterSpacing: 2 * s,
          background: "linear-gradient(180deg, #FFF6D8 0%, #FFD36E 45%, #C8892A 70%, #FFE6A3 100%)", WebkitBackgroundClip: "text",
          backgroundClip: "text", color: "transparent", opacity: ket, scale: 0.9 + 0.1 * ket,
          filter: `drop-shadow(0 ${4 * s}px 0 #7a4a10) drop-shadow(0 0 ${28 * s}px rgba(255,200,100,0.55))` }}>{p.ketLuan}</div>
      ) : (
        <>
          <div style={{ position: "absolute", left: (960 - 380 * ket) * s, top: 640 * s, width: 760 * ket * s, height: 3 * s, background: DONG }} />
          {p.ketLuan ? (
            <div style={{ position: "absolute", top: 680 * s, left: 0, right: 0, textAlign: "center", fontFamily: CHU_CHAN, fontWeight: 700,
              fontSize: 78 * s, letterSpacing: 3 * s, color: "#FFE7B0", opacity: ket, translate: `0 ${(1 - ket) * 20 * s}px`,
              textShadow: `0 0 ${36 * s}px rgba(255,180,90,0.45)` }}>{p.ketLuan}</div>
          ) : null}
        </>
      )}
    </AbsoluteFill>
  );
};
