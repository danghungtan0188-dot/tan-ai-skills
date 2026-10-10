// Đoạn tri ân (liệt sĩ, thương binh, gia đình có công, Mẹ VN anh hùng): nền tối trầm, quầng nến ấm lay nhẹ,
// từng con số hiện chậm (mờ dần lên, không đếm nhảy) đúng mốc lời đọc, nhãn chữ có chân bên dưới. Toàn khung.
import React from "react";
import { AbsoluteFill, Easing, interpolate, random, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FPS } from "../chung";

export const triAnSchema = coBan.extend({
  muc: z.array(z.object({ so: z.string(), nhan: z.string(), tai: z.number() })),
  loiDe: z.string().default(""),
  taiLoiDe: z.number().default(0),
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const CHU_CHAN = "'Times New Roman', Cambria, serif";
const KEM = "#F1E4C8";
const DONG = "#C9A46A";

export const TriAn: React.FC<z.infer<typeof triAnSchema>> = ({ muc, loiDe, taiLoiDe }) => {
  const frame = useCurrentFrame();
  const { width, durationInFrames } = useVideoConfig();
  const s = width / 1920;
  const t = frame / FPS;
  const het = durationInFrames / FPS;
  const nen = interpolate(t, [0, 1.0, het - 1.0, het], [0, 1, 1, 0], kep);
  const lay = 0.92 + 0.08 * Math.sin(t * 2.3) * Math.sin(t * 3.7 + 1);
  const motGiu = loiDe && t >= taiLoiDe;

  return (
    <AbsoluteFill style={{ background: "#07050300", opacity: nen }}>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse 60% 55% at 50% 62%, #3a2614 0%, #160d06 55%, #050302 100%)" }} />
      <AbsoluteFill
        style={{ background: `radial-gradient(circle at 50% 88%, rgba(255,170,80,${0.32 * lay}) 0%, rgba(255,140,50,0) 38%)` }}
      />
      {Array.from({ length: 28 }, (_, i) => {
        const x = random(`x${i}`) * 1920;
        const y = 1080 - ((random(`y${i}`) * 1080 + t * (6 + random(`v${i}`) * 14)) % 1100);
        return (
          <div key={i} style={{ position: "absolute", left: x * s, top: y * s, width: 3 * s, height: 3 * s, borderRadius: "50%",
            background: "#ffd9a0", opacity: 0.12 + 0.25 * Math.abs(Math.sin(t + i)), boxShadow: `0 0 ${8 * s}px ${2 * s}px rgba(255,190,110,0.35)` }} />
        );
      })}
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", opacity: motGiu ? interpolate(t, [taiLoiDe, taiLoiDe + 0.8], [1, 0.15], kep) : 1 }}>
        <div style={{ display: "flex", gap: 90 * s, alignItems: "flex-start", marginTop: -40 * s }}>
          {muc.map((m, i) => {
            const vao = interpolate(t, [m.tai, m.tai + 1.0], [0, 1], { ...kep, easing: Easing.out(Easing.cubic) });
            return (
              <div key={i} style={{ textAlign: "center", width: 360 * s, opacity: vao, translate: `0 ${(1 - vao) * 24 * s}px` }}>
                <div style={{ fontFamily: CHU_CHAN, fontWeight: 700, fontSize: 132 * s, lineHeight: 1, color: KEM,
                  textShadow: `0 0 ${30 * s}px rgba(255,180,90,0.35)` }}>{m.so}</div>
                <div style={{ width: 90 * s, height: 2 * s, background: DONG, margin: `${20 * s}px auto` }} />
                <div style={{ fontFamily: CHU_CHAN, fontStyle: "italic", fontSize: 38 * s, color: KEM, lineHeight: 1.25 }}>{m.nhan}</div>
              </div>
            );
          })}
        </div>
      </AbsoluteFill>
      {loiDe ? (
        <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", padding: `0 ${200 * s}px`,
          opacity: interpolate(t, [taiLoiDe + 0.3, taiLoiDe + 1.3], [0, 1], kep) }}>
          <div style={{ fontFamily: CHU_CHAN, fontStyle: "italic", fontSize: 64 * s, color: KEM, textAlign: "center", lineHeight: 1.35,
            textShadow: `0 0 ${24 * s}px rgba(255,180,90,0.3)` }}>{loiDe}</div>
        </AbsoluteFill>
      ) : null}
    </AbsoluteFill>
  );
};
