// Chữ lớn đè trên flycam (kiểu "XÃ VĨNH HỰU" của phóng sự truyền hình): trắng hơi trong, giãn chữ dần,
// một vệt sáng chéo lướt qua; vào/ra mờ. Nền trong suốt.
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FONT, FPS } from "../chung";

export const tieuDeLonSchema = coBan.extend({
  chu: z.string(),
  co: z.number().default(150),
  phu: z.string().default(""), // dòng phụ nhỏ hơn, hiện sau dòng chính
  nenSang: z.boolean().default(false), // đè trên nền sáng (mây trắng): chữ xanh lam đậm, quầng sáng trắng
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

export const TieuDeLon: React.FC<z.infer<typeof tieuDeLonSchema>> = ({ chu, co, phu, nenSang }) => {
  const frame = useCurrentFrame();
  const { width, height, durationInFrames } = useVideoConfig();
  const s = width / 1920;
  const t = frame / FPS;
  const het = durationInFrames / FPS;
  const mo = interpolate(t, [0, 0.6, het - 0.6, het], [0, 1, 1, 0], kep);
  const gian = interpolate(t, [0, het], [4, 22], kep);
  const vach = interpolate(t, [0.3, 1.6], [-0.3 * width, 1.3 * width], { ...kep, easing: Easing.inOut(Easing.cubic) });
  const vaoPhu = interpolate(t, [0.8, 1.4], [0, 1], { ...kep, easing: Easing.out(Easing.cubic) });
  const mauChinh = nenSang ? "#0B2A63" : "rgba(255,255,255,0.82)";
  const mauPhu = nenSang ? "#123E86" : "rgba(255,255,255,0.9)";
  const bong = (r: number, a: number) => (nenSang ? `0 0 ${r * 1.4 * s}px rgba(255,255,255,0.95), 0 0 ${r * 0.5 * s}px rgba(255,255,255,0.9)`
    : `0 ${4 * s}px ${r * s}px rgba(0,0,0,${a})`);

  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", opacity: mo }}>
      <div
        style={{
          fontFamily: FONT,
          fontWeight: 900,
          fontSize: co * s,
          letterSpacing: gian * s,
          color: mauChinh,
          textShadow: bong(18, 0.45),
          whiteSpace: "nowrap",
        }}
      >
        {chu}
      </div>
      {phu ? (
        <div
          style={{
            marginTop: 18 * s,
            fontFamily: FONT,
            fontWeight: 700,
            fontSize: co * 0.55 * s,
            letterSpacing: (gian * 0.6 + 2) * s,
            color: mauPhu,
            textShadow: bong(14, 0.5),
            whiteSpace: "nowrap",
            opacity: vaoPhu,
            translate: `0 ${(1 - vaoPhu) * 20 * s}px`,
          }}
        >
          {phu}
        </div>
      ) : null}
      <div
        style={{
          position: "absolute",
          left: vach,
          top: -height * 0.2,
          width: 5 * s,
          height: height * 1.4,
          rotate: "-30deg",
          background: "linear-gradient(180deg, transparent, white 35%, white 65%, transparent)",
          boxShadow: `0 0 ${20 * s}px ${6 * s}px rgba(255,255,255,0.6)`,
        }}
      />
    </AbsoluteFill>
  );
};
