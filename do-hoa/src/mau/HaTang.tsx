// Ba lĩnh vực hạ tầng (giao thông · trường học · y tế): dải tối mờ ngang khung, mỗi biểu tượng vẽ bằng SVG
// sáng lên đúng mốc lời đọc (`tai`), vòng tròn viền đồng, nhãn bên dưới. Nền trong suốt — đè lên cảnh quay.
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FONT, FPS } from "../chung";

export const haTangSchema = coBan.extend({
  tieuDe: z.string().default(""),
  nenMo: z.boolean().default(true), // false: bo dai toi mo, chi giu chu/so (bong chu dam hon de van doc ro)
  muc: z.array(z.object({ loai: z.enum(["giao_thong", "truong_hoc", "y_te", "san_xuat", "doi_song"]), nhan: z.string(), tai: z.number() })),
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const KEM = "#F3E9D2";
const DONG = "#C9A46A";

const BieuTuong: React.FC<{ loai: string; mau: string }> = ({ loai, mau }) => (
  <svg viewBox="0 0 100 100" width="100%" height="100%" fill="none" stroke={mau} strokeWidth={4} strokeLinecap="round" strokeLinejoin="round">
    {loai === "giao_thong" ? (
      <g><path d="M38 84 L46 22 M62 84 L54 22" /><path d="M50 28 v8 M50 46 v10 M50 66 v12" strokeWidth={5} /><path d="M24 84 h52" /></g>
    ) : loai === "truong_hoc" ? (
      <g><path d="M18 46 L50 24 L82 46" /><rect x="26" y="46" width="48" height="34" /><rect x="44" y="58" width="12" height="22" />
        <path d="M50 24 v-12 l12 4 l-12 4" /><path d="M32 54 h6 M62 54 h6" /></g>
    ) : loai === "y_te" ? (
      <g><circle cx="50" cy="52" r="30" /><path d="M50 36 v32 M34 52 h32" strokeWidth={8} /></g>
    ) : loai === "san_xuat" ? (
      <g><path d="M50 82 V40" /><path d="M50 58 C36 56 30 46 30 36 C42 38 50 46 50 58" /><path d="M50 50 C64 48 70 38 70 28 C58 30 50 38 50 50" /><path d="M26 82 h48" /></g>
    ) : (
      <g><circle cx="36" cy="34" r="10" /><circle cx="64" cy="34" r="10" /><path d="M18 78 C18 60 30 52 36 52 C42 52 50 58 50 66" /><path d="M82 78 C82 60 70 52 64 52 C58 52 50 58 50 66" /></g>
    )}
  </svg>
);

export const HaTang: React.FC<z.infer<typeof haTangSchema>> = ({ tieuDe, muc, nenMo }) => {
  const frame = useCurrentFrame();
  const { width, durationInFrames } = useVideoConfig();
  const s = width / 1920;
  const t = frame / FPS;
  const het = durationInFrames / FPS;
  const nen = interpolate(t, [0, 0.4, het - 0.5, het], [0, 1, 1, 0], kep);
  return (
    <AbsoluteFill style={{ opacity: nen }}>
      {nenMo ? (
      <div style={{ position: "absolute", left: 0, right: 0, top: 290 * s, height: 440 * s,
        background: "linear-gradient(180deg, transparent, rgba(6,12,28,0.72) 18%, rgba(6,12,28,0.72) 82%, transparent)" }} />
      ) : null}
      {tieuDe ? (
        <div style={{ position: "absolute", top: 330 * s, width: "100%", textAlign: "center", fontFamily: FONT, fontStyle: "italic",
          fontSize: 40 * s, color: DONG, letterSpacing: 2 * s, textShadow: nenMo ? undefined : `0 0 ${6 * s}px rgba(0,0,0,0.9), 0 ${3 * s}px ${14 * s}px rgba(0,0,0,0.85)` }}>{tieuDe}</div>
      ) : null}
      <div style={{ position: "absolute", top: 400 * s, width: "100%", display: "flex", justifyContent: "center", gap: 130 * s }}>
        {muc.map((m, i) => {
          const vao = interpolate(t, [m.tai, m.tai + 0.6], [0, 1], { ...kep, easing: Easing.out(Easing.back(1.5)) });
          const mo = 0.35 + 0.65 * vao;
          return (
            <div key={i} style={{ textAlign: "center", width: 260 * s, opacity: interpolate(t, [0.2 + i * 0.15, 0.7 + i * 0.15], [0, 1], kep) }}>
              <div style={{ width: 200 * s, height: 200 * s, margin: "0 auto", borderRadius: "50%", border: `${4 * s}px solid ${DONG}`,
                background: `rgba(201,164,106,${0.08 + 0.22 * vao})`, padding: 36 * s, boxSizing: "border-box", opacity: mo,
                scale: 0.9 + 0.12 * vao, boxShadow: `0 0 ${46 * vao * s}px rgba(255,200,120,${0.45 * vao})` }}>
                <BieuTuong loai={m.loai} mau={vao > 0.5 ? "#FFE7B0" : KEM} />
              </div>
              <div style={{ marginTop: 24 * s, fontFamily: FONT, fontWeight: 700, fontSize: 40 * s, color: KEM, opacity: mo,
                textShadow: nenMo ? `0 ${2 * s}px ${8 * s}px #000` : `0 0 ${6 * s}px rgba(0,0,0,0.9), 0 ${3 * s}px ${14 * s}px rgba(0,0,0,0.85)` }}>{m.nhan}</div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
