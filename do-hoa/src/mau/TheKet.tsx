// Thẻ kết kiểu phim tài liệu: nền nâu trầm có quầng hổ phách, tia sáng mờ, bụi sáng trôi, hạt film, tối góc,
// bóng rặng dừa – dòng kênh; chữ vàng đồng nổi khối có vệt sáng quét; logo ATT NEWS góc trên phải. Toàn khung.
import React from "react";
import { AbsoluteFill, Easing, interpolate, random, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FONT, FPS, LogoATT } from "../chung";

export const theKetSchema = coBan.extend({
  dong1: z.string(),
  dong2: z.string().default(""),
  chiChu: z.boolean().default(false), // true: chỉ chữ + logo, nền trong suốt để đắp lên nền khác
  treChu: z.number().default(0), // giây chữ bắt đầu vào
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const VANG_KIM = "linear-gradient(180deg, #fff6dc 0%, #f1d08a 40%, #c4913f 64%, #f2d79c 84%, #8a5a1c 100%)";
const KHOI = Array.from({ length: 6 }, (_, i) => `0 ${i + 1}px 0 ${i < 3 ? "#7a5320" : "#4a3010"}`)
  .concat(["0 14px 22px rgba(0,0,0,0.8)", "0 0 46px rgba(230,170,80,0.28)"])
  .join(", ");

// Một cây dừa: thân cong + tàu lá rủ. Toạ độ khung 1920x1080, gốc ở (x, day).
const cayDua = (x: number, day: number, cao: number, nghieng: number) => {
  const ngonX = x + nghieng;
  const ngonY = day - cao;
  const than = `M${x - 7} ${day} Q${x + nghieng * 0.2} ${day - cao * 0.55} ${ngonX - 3} ${ngonY} L${ngonX + 3} ${ngonY} Q${
    x + nghieng * 0.2 + 8
  } ${day - cao * 0.55} ${x + 7} ${day} Z`;
  const la = [-160, -125, -95, -60, -25, 10, 40].map((g) => {
    const r = (g * Math.PI) / 180;
    const dai = cao * 0.48;
    const ex = ngonX + Math.cos(r) * dai;
    const ey = ngonY + Math.sin(r) * dai * 0.55 + dai * 0.35;
    const cx = ngonX + Math.cos(r) * dai * 0.55;
    const cy = ngonY + Math.sin(r) * dai * 0.6 - dai * 0.12;
    return `M${ngonX} ${ngonY} Q${cx} ${cy - 22} ${ex} ${ey} Q${cx} ${cy + 14} ${ngonX} ${ngonY + 10} Z`;
  });
  return [than, ...la].join(" ");
};

const DUA: [number, number, number][] = [
  [90, 300, 40], [210, 230, -30], [330, 340, 55], [470, 250, 20], [1420, 260, -25], [1560, 330, 45],
  [1690, 240, -40], [1820, 310, 30], [600, 190, -15], [1300, 200, 18],
];

export const TheKet: React.FC<z.infer<typeof theKetSchema>> = ({ dong1, dong2, chiChu, treChu }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const t = frame / FPS;
  const cx = 960;
  const cy = 250;

  const xoay = interpolate(frame, [0, durationInFrames], [0, 9]);
  const chop = interpolate(t, [0, 0.6], [1, 0], kep);
  const tat = interpolate(frame, [durationInFrames - 0.6 * FPS, durationInFrames], [0, 1], kep);
  const vao1 = spring({ frame, fps: FPS, delay: (0.15 + treChu) * FPS, config: { damping: 14, mass: 0.9 } });
  const vao2 = spring({ frame, fps: FPS, delay: (0.55 + treChu) * FPS, config: { damping: 15 } });
  const quet = interpolate(t - treChu, [1.2, 2.3], [-30, 130], { ...kep, easing: Easing.inOut(Easing.cubic) });
  const logo = interpolate(t - treChu, [0.3, 0.9], [0, 1], kep);

  const chu = (noiDung: string, co: number, vao: number, mo: number) => (
    <div style={{ position: "relative", whiteSpace: "nowrap", marginBottom: co * 0.06, opacity: vao, scale: 1.25 - 0.25 * vao, filter: `blur(${(1 - vao) * 10}px)` }}>
      <div style={{ fontSize: co, color: "#d89a1a", textShadow: KHOI, paddingTop: co * 0.18 }}>{noiDung}</div>
      <div
        style={{
          position: "absolute",
          inset: 0,
          fontSize: co,
          paddingTop: co * 0.18,
          backgroundImage: VANG_KIM,
          WebkitBackgroundClip: "text",
          backgroundClip: "text",
          color: "transparent",
        }}
      >
        {noiDung}
      </div>
      <div
        style={{
          position: "absolute",
          inset: 0,
          fontSize: co,
          paddingTop: co * 0.18,
          backgroundImage: `linear-gradient(105deg, transparent ${quet - 12 + mo}%, rgba(255,255,255,0.95) ${quet + mo}%, transparent ${
            quet + 12 + mo
          }%)`,
          WebkitBackgroundClip: "text",
          backgroundClip: "text",
          color: "transparent",
        }}
      >
        {noiDung}
      </div>
    </div>
  );

  const lopChu = (
    <>
      <AbsoluteFill
        style={{
          justifyContent: "center",
          alignItems: "center",
          fontFamily: FONT,
          fontWeight: 900,
          textAlign: "center",
          lineHeight: 1.05,
          paddingBottom: 60,
        }}
      >
        {chu(dong1, 168, vao1, 0)}
        {dong2 ? <div style={{ marginTop: 6 }}>{chu(dong2, dong2.length > 20 ? 96 : 112, vao2, -15)}</div> : null}
      </AbsoluteFill>

      <div style={{ position: "absolute", top: 54, right: 70, opacity: logo, scale: 0.9 + 0.1 * logo }}>
        <LogoATT cao={78} />
      </div>

    </>
  );
  if (chiChu) return <AbsoluteFill>{lopChu}</AbsoluteFill>;

  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse 65% 70% at 50% 34%, #8a5e2c 0%, #4a3016 26%, #241709 55%, #0b0704 100%)" }}>
      {/* tia sáng xoay */}
      <svg width={1920} height={1080} style={{ position: "absolute", mixBlendMode: "screen", filter: "blur(7px)" }}>
        <defs>
          <radialGradient id="tia" cx={cx} cy={cy} r={1200} gradientUnits="userSpaceOnUse">
            <stop offset="0" stopColor="#ffdca8" stopOpacity="0.22" />
            <stop offset="1" stopColor="#c88a3a" stopOpacity="0" />
          </radialGradient>
        </defs>
        <g transform={`rotate(${xoay} ${cx} ${cy})`}>
          {Array.from({ length: 24 }, (_, i) => {
            const a = (i / 24) * Math.PI * 2;
            const w = 0.045 + random(`w${i}`) * 0.05;
            const R = 2200;
            return (
              <path
                key={i}
                d={`M${cx} ${cy} L${cx + Math.cos(a - w) * R} ${cy + Math.sin(a - w) * R} L${cx + Math.cos(a + w) * R} ${cy + Math.sin(a + w) * R} Z`}
                fill="url(#tia)"
                opacity={0.25 + random(`o${i}`) * 0.5}
              />
            );
          })}
        </g>
        {/* vệt sáng bắn ra */}
        {Array.from({ length: 16 }, (_, i) => {
          const a = random(`a${i}`) * Math.PI * 2;
          const tre = random(`d${i}`) * 3;
          const tien = ((t * 0.22 + tre) % 1.6) / 1.6;
          const r0 = 120 + tien * 1300;
          const dai = 60 + random(`l${i}`) * 220;
          return (
            <line
              key={i}
              x1={cx + Math.cos(a) * r0}
              y1={cy + Math.sin(a) * r0}
              x2={cx + Math.cos(a) * (r0 + dai)}
              y2={cy + Math.sin(a) * (r0 + dai)}
              stroke="#ffe2b0"
              strokeWidth={1.5 + random(`s${i}`) * 2.5}
              strokeLinecap="round"
              opacity={Math.sin(tien * Math.PI) * 0.3}
            />
          );
        })}
      </svg>

      {/* bóng rặng dừa, dòng kênh, chân trời phát sáng */}
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <defs>
          <linearGradient id="dat" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#1a1009" />
            <stop offset="1" stopColor="#050302" />
          </linearGradient>
          <linearGradient id="kenh" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0" stopColor="#d9a35a" stopOpacity="0" />
            <stop offset="0.5" stopColor="#ffdca0" stopOpacity="0.8" />
            <stop offset="1" stopColor="#d9a35a" stopOpacity="0" />
          </linearGradient>
        </defs>
        <ellipse cx={960} cy={985} rx={1100} ry={60} fill="#d08a3a" opacity={0.3} style={{ filter: "blur(30px)" }} />
        {DUA.map(([x, cao, ng], i) => (
          <path key={i} d={cayDua(x, 990, cao, ng)} fill="url(#dat)" opacity={0.92} />
        ))}
        <path d="M0 960 Q480 940 960 958 T1920 950 L1920 1080 L0 1080 Z" fill="url(#dat)" />
        <rect x={0} y={1000} width={1920} height={6} fill="url(#kenh)" opacity={0.6 + 0.4 * Math.sin(t * 4)} />
        <rect x={200} y={1022} width={1520} height={3} fill="url(#kenh)" opacity={0.45 + 0.3 * Math.sin(t * 5 + 1)} />
      </svg>

      {/* hạt sáng bay lên */}
      {Array.from({ length: 70 }, (_, i) => {
        const x = random(`px${i}`) * 1920;
        const tocDo = 8 + random(`pv${i}`) * 26;
        const y = 1080 - ((random(`py${i}`) * 1080 + t * tocDo) % 1100);
        const co = 1.5 + random(`pr${i}`) * 3.5;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: x,
              top: y,
              width: co,
              height: co,
              borderRadius: "50%",
              background: "#ffe6bd",
              boxShadow: `0 0 ${co * 3}px ${co}px rgba(230,170,90,0.45)`,
              opacity: 0.15 + 0.45 * Math.abs(Math.sin(t * 1.5 + i)),
            }}
          />
        );
      })}

      {lopChu}
      {/* tối góc + hạt film */}
      <AbsoluteFill style={{ background: "radial-gradient(ellipse 75% 70% at 50% 45%, transparent 55%, rgba(0,0,0,0.75) 100%)" }} />
      <svg width={1920} height={1080} style={{ position: "absolute", opacity: 0.16, mixBlendMode: "overlay" }}>
        <filter id="hat">
          <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed={frame % 12} />
        </filter>
        <rect width={1920} height={1080} filter="url(#hat)" />
      </svg>
      <AbsoluteFill style={{ background: "black", opacity: chop }} />
      <AbsoluteFill style={{ background: "black", opacity: tat }} />
    </AbsoluteFill>
  );
};
