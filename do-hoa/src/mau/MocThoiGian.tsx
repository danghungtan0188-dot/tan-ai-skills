// Trục mốc thời gian kiểu phim tài liệu: nền nâu trầm, trục ngang các năm; mốc nào tới `tai` thì sáng lên,
// mốc đang nói có quầng sáng và dòng chú thích lớn bên dưới. Mốc có `tai` lớn hơn thời lượng = chỉ hiện mờ. Toàn khung.
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FPS } from "../chung";

export const mocThoiGianSchema = coBan.extend({
  moc: z.array(z.object({ nam: z.string(), nhan: z.string(), tai: z.number() })),
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const CHU_CHAN = "'Times New Roman', Cambria, serif";
const KEM = "#F1E4C8";
const DONG = "#C9A46A";

export const MocThoiGian: React.FC<z.infer<typeof mocThoiGianSchema>> = ({ moc }) => {
  const frame = useCurrentFrame();
  const { width, durationInFrames } = useVideoConfig();
  const s = width / 1920;
  const t = frame / FPS;
  const het = durationInFrames / FPS;
  const nen = interpolate(t, [0, 0.6, het - 0.6, het], [0, 1, 1, 0], kep);
  const x = (i: number) => 220 + (1480 * i) / Math.max(1, moc.length - 1);
  const dangNoi = moc.reduce((k, m, i) => (t >= m.tai ? i : k), -1);
  // vạch sáng chạy tới mốc đang nói
  const tu = dangNoi > 0 ? x(dangNoi - 1) : x(0);
  const den = dangNoi >= 0 ? x(dangNoi) : x(0);
  const chay = dangNoi >= 0 ? interpolate(t, [moc[dangNoi].tai - 0.2, moc[dangNoi].tai + 0.8], [0, 1], { ...kep, easing: Easing.inOut(Easing.cubic) }) : 0;
  const vachSang = tu + (den - tu) * (dangNoi > 0 ? chay : 1);

  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse 75% 70% at 50% 50%, #3a2a18 0%, #1a1108 70%, #0a0603 100%)", opacity: nen }}>
      <svg width={1920 * s} height={1080 * s} viewBox="0 0 1920 1080" style={{ position: "absolute" }}>
        <line x1={x(0)} y1={470} x2={x(moc.length - 1)} y2={470} stroke={DONG} strokeOpacity={0.3} strokeWidth={3} />
        {dangNoi >= 0 ? <line x1={x(0)} y1={470} x2={vachSang} y2={470} stroke={DONG} strokeWidth={5} /> : null}
        {moc.map((m, i) => {
          const sang = i < dangNoi ? 1 : i === dangNoi ? chay : 0;
          return (
            <g key={i}>
              {i === dangNoi ? <circle cx={x(i)} cy={470} r={34 * chay} fill="rgba(255,200,120,0.18)" /> : null}
              <circle cx={x(i)} cy={470} r={i === dangNoi ? 14 : 10} fill={sang > 0.5 ? KEM : "#4a3a28"} stroke={DONG} strokeWidth={3} />
              <text x={x(i)} y={420} textAnchor="middle" fill={KEM} fillOpacity={0.35 + 0.65 * sang}
                style={{ fontFamily: CHU_CHAN, fontWeight: 700, fontSize: i === dangNoi ? 62 : 44 }}>{m.nam}</text>
            </g>
          );
        })}
      </svg>
      {moc.map((m, i) => {
        if (i !== dangNoi) return null;
        const hien = interpolate(t, [m.tai + 0.3, m.tai + 1.1], [0, 1], { ...kep, easing: Easing.out(Easing.cubic) });
        return (
          <div key={i} style={{ position: "absolute", left: 0, right: 0, top: 560 * s, textAlign: "center", opacity: hien,
            translate: `0 ${(1 - hien) * 20 * s}px` }}>
            <div style={{ width: 90 * s, height: 2 * s, background: DONG, margin: `0 auto ${26 * s}px` }} />
            <div style={{ fontFamily: CHU_CHAN, fontStyle: "italic", fontSize: 58 * s, color: KEM, lineHeight: 1.3,
              textShadow: `0 0 ${24 * s}px rgba(255,180,90,0.3)` }}>{m.nhan}</div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
