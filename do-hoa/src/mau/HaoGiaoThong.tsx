// Sơ đồ minh họa "rào làng chiến đấu" (không phải bản đồ đo đạc — góc ghi rõ "Sơ đồ minh họa"): nền giấy cũ,
// các tuyến giao thông hào răng cưa vẽ dần, số km đếm lên; sau đó công sự (ô vuông) và mô ngăn địch (gò) hiện
// theo mốc lời đọc. Toàn khung, toạ độ theo khung 1920x1080.
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FONT, FPS } from "../chung";

const diem = z.tuple([z.number(), z.number()]);
export const haoGiaoThongSchema = coBan.extend({
  tieuDe: z.string().default(""),
  tuyen: z.array(z.object({ ten: z.string(), diem: z.array(diem), tai: z.number(), lau: z.number().default(2) })),
  km: z.object({ so: z.number(), tienTo: z.string().default(""), tai: z.number(), lau: z.number().default(2) }),
  congSu: z.object({ nhan: z.string(), diem: z.array(diem), tai: z.number() }).optional(),
  moNgan: z.object({ nhan: z.string(), diem: z.array(diem), tai: z.number() }).optional(),
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const NAU = "#3b2a18";
const DONG = "#8a5a22";
const CHU_CHAN = "'Times New Roman', Cambria, serif";

// đường răng cưa giữa các điểm (giao thông hào đào gấp khúc)
const rangCua = (ds: [number, number][]) => {
  let d = `M${ds[0][0]},${ds[0][1]}`;
  for (let i = 1; i < ds.length; i++) {
    const [ax, ay] = ds[i - 1];
    const [bx, by] = ds[i];
    const n = Math.max(2, Math.round(Math.hypot(bx - ax, by - ay) / 70));
    const nx = -(by - ay) / Math.hypot(bx - ax, by - ay);
    const ny = (bx - ax) / Math.hypot(bx - ax, by - ay);
    for (let k = 1; k <= n; k++) {
      const lech = k === n ? 0 : (k % 2 ? 16 : -16);
      d += ` L${ax + ((bx - ax) * k) / n + nx * lech},${ay + ((by - ay) * k) / n + ny * lech}`;
    }
  }
  return d;
};

export const HaoGiaoThong: React.FC<z.infer<typeof haoGiaoThongSchema>> = ({ tieuDe, tuyen, km, congSu, moNgan }) => {
  const frame = useCurrentFrame();
  const { width, durationInFrames } = useVideoConfig();
  const s = width / 1920;
  const t = frame / FPS;
  const het = durationInFrames / FPS;
  const nen = interpolate(t, [0, 0.6, het - 0.6, het], [0, 1, 1, 0], kep);
  const day = interpolate(frame, [0, durationInFrames], [1, 1.05], kep);
  const so = interpolate(t, [km.tai, km.tai + km.lau], [0, km.so], { ...kep, easing: Easing.out(Easing.cubic) });
  const hienKm = interpolate(t, [km.tai - 0.2, km.tai + 0.4], [0, 1], kep);
  const nhom = (g: { nhan: string; diem: [number, number][]; tai: number } | undefined, ve: (x: number, y: number) => React.ReactNode) =>
    g ? g.diem.map(([x, y], i) => {
      const h = interpolate(t, [g.tai + i * 0.15, g.tai + i * 0.15 + 0.4], [0, 1], { ...kep, easing: Easing.out(Easing.back(2)) });
      return <g key={i} opacity={h} transform={`translate(${x} ${y}) scale(${h})`}>{ve(0, 0)}</g>;
    }) : null;

  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse 80% 75% at 50% 45%, #e2d2b0 0%, #c4ab7f 60%, #7a5e3a 100%)", opacity: nen }}>
      <svg width={1920 * s} height={1080 * s} style={{ position: "absolute", opacity: 0.3, mixBlendMode: "multiply" }}>
        <filter id="giay3">
          <feTurbulence type="fractalNoise" baseFrequency="0.012 0.05" numOctaves="4" seed="4" />
          <feColorMatrix type="matrix" values="0 0 0 0 0.45  0 0 0 0 0.35  0 0 0 0 0.22  0 0 0 0.9 0" />
        </filter>
        <rect width="100%" height="100%" filter="url(#giay3)" />
      </svg>
      <AbsoluteFill style={{ scale: day }}>
        <svg width={1920 * s} height={1080 * s} viewBox="0 0 1920 1080">
          {tuyen.map((tu, i) => {
            const k = interpolate(t, [tu.tai, tu.tai + tu.lau], [0, 1], { ...kep, easing: Easing.inOut(Easing.quad) });
            const cuoi = tu.diem[tu.diem.length - 1];
            return (
              <g key={i}>
                <path d={rangCua(tu.diem)} pathLength={1} fill="none" stroke="#5a4128" strokeOpacity={0.35} strokeWidth={22}
                  strokeLinejoin="round" strokeDasharray="1 1" strokeDashoffset={1 - k} />
                <path d={rangCua(tu.diem)} pathLength={1} fill="none" stroke={DONG} strokeWidth={8} strokeLinejoin="round"
                  strokeDasharray="1 1" strokeDashoffset={1 - k} />
                <text x={cuoi[0]} y={cuoi[1] - 34} textAnchor="middle" fill={NAU} opacity={interpolate(k, [0.85, 1], [0, 1], kep)}
                  style={{ fontFamily: CHU_CHAN, fontStyle: "italic", fontSize: 36 }}>{tu.ten}</text>
              </g>
            );
          })}
          {nhom(congSu, () => <rect x={-16} y={-16} width={32} height={32} fill="#f3e8cf" stroke={NAU} strokeWidth={5} />)}
          {nhom(moNgan, () => <path d="M-26,12 Q0,-26 26,12 Z" fill="#7a5a34" stroke={NAU} strokeWidth={4} />)}
        </svg>
      </AbsoluteFill>
      {tieuDe ? (
        <div style={{ position: "absolute", top: 70 * s, left: 0, right: 0, textAlign: "center", fontFamily: CHU_CHAN,
          fontStyle: "italic", fontSize: 54 * s, color: NAU }}>{tieuDe}</div>
      ) : null}
      <div style={{ position: "absolute", right: 120 * s, bottom: 250 * s, textAlign: "right", opacity: hienKm, fontFamily: FONT, color: NAU }}>
        <span style={{ fontSize: 46 * s }}>{km.tienTo}</span>
        <span style={{ fontSize: 130 * s, fontWeight: 800 }}>{Math.round(so)}</span>
        <span style={{ fontSize: 56 * s, fontWeight: 700 }}> km</span>
        <div style={{ fontFamily: CHU_CHAN, fontStyle: "italic", fontSize: 36 * s }}>giao thông hào</div>
      </div>
      <div style={{ position: "absolute", left: 120 * s, bottom: 250 * s, fontFamily: CHU_CHAN, fontSize: 34 * s, color: NAU, lineHeight: 1.6 }}>
        {congSu ? <div style={{ opacity: interpolate(t, [congSu.tai, congSu.tai + 0.5], [0, 1], kep) }}>
          <span style={{ display: "inline-block", width: 24 * s, height: 24 * s, background: "#f3e8cf", border: `${4 * s}px solid ${NAU}`, marginRight: 14 * s }} />
          {congSu.nhan}</div> : null}
        {moNgan ? <div style={{ opacity: interpolate(t, [moNgan.tai, moNgan.tai + 0.5], [0, 1], kep) }}>
          <span style={{ display: "inline-block", width: 0, height: 0, borderLeft: `${16 * s}px solid transparent`, borderRight: `${16 * s}px solid transparent`,
            borderBottom: `${22 * s}px solid #7a5a34`, marginRight: 14 * s }} />
          {moNgan.nhan}</div> : null}
      </div>
      <div style={{ position: "absolute", left: 40 * s, top: 30 * s, fontFamily: FONT, fontSize: 24 * s, color: NAU, opacity: 0.7 }}>Sơ đồ minh họa</div>
    </AbsoluteFill>
  );
};
