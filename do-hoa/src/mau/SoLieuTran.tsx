// Số liệu trận đánh kiểu phim tài liệu: dải tối mờ ngang khung, các ô số lớn đếm lên lần lượt,
// nhãn bên dưới; màu kem/đồng nhẹ. Nền trong suốt — đắp lên tư liệu chiến đấu.
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FONT, FPS } from "../chung";

export const soLieuTranSchema = coBan.extend({
  tieuDe: z.string().default(""),
  muc: z.array(z.object({ so: z.number(), nhan: z.string(), tai: z.number().default(0), tienTo: z.string().default("") })),
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const KEM = "#F3E9D2";
const DONG = "#C9A46A";

export const SoLieuTran: React.FC<z.infer<typeof soLieuTranSchema>> = ({ tieuDe, muc }) => {
  const frame = useCurrentFrame();
  const { width, durationInFrames } = useVideoConfig();
  const s = width / 1920;
  const t = frame / FPS;
  const het = durationInFrames / FPS;
  const nen = interpolate(t, [0, 0.4, het - 0.5, het], [0, 1, 1, 0], kep);

  return (
    <AbsoluteFill style={{ opacity: nen }}>
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: 300 * s,
          height: 420 * s,
          background: "linear-gradient(180deg, transparent, rgba(10,6,2,0.72) 18%, rgba(10,6,2,0.72) 82%, transparent)",
        }}
      />
      {tieuDe ? (
        <div
          style={{
            position: "absolute",
            top: 345 * s,
            width: "100%",
            textAlign: "center",
            fontFamily: FONT,
            fontStyle: "italic",
            fontSize: 40 * s,
            color: DONG,
            letterSpacing: 2 * s,
          }}
        >
          {tieuDe}
        </div>
      ) : null}
      <div style={{ position: "absolute", top: 420 * s, width: "100%", display: "flex", justifyContent: "center", gap: 120 * s }}>
        {muc.map((m, i) => {
          const vao = interpolate(t, [m.tai, m.tai + 0.5], [0, 1], { ...kep, easing: Easing.out(Easing.cubic) });
          const dem = Math.round(interpolate(t, [m.tai, m.tai + 1.2], [0, m.so], { ...kep, easing: Easing.out(Easing.quad) }));
          return (
            <div key={i} style={{ textAlign: "center", opacity: vao, translate: `0 ${(1 - vao) * 30 * s}px`, minWidth: 360 * s }}>
              <div
                style={{
                  fontFamily: FONT,
                  fontWeight: 900,
                  fontSize: 150 * s,
                  lineHeight: 1,
                  color: KEM,
                  textShadow: `0 ${4 * s}px ${16 * s}px rgba(0,0,0,0.7)`,
                }}
              >
                {m.tienTo ? <span style={{ fontSize: 56 * s, fontWeight: 700, marginRight: 14 * s, verticalAlign: "middle" }}>{m.tienTo}</span> : null}
                {dem}
              </div>
              <div style={{ width: 120 * s, height: 3 * s, background: DONG, margin: `${18 * s}px auto` }} />
              <div style={{ fontFamily: FONT, fontWeight: 700, fontSize: 40 * s, color: KEM, textShadow: `0 ${2 * s}px ${8 * s}px #000` }}>
                {m.nhan}
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
