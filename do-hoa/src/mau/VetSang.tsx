// Vệt sáng quét chéo để chuyển cảnh (kiểu phóng sự truyền hình): vài vạch trắng mảnh + một dải sáng rộng
// lướt từ trái sang phải. Nền trong suốt — đắp đúng điểm cắt, giữa vệt sáng che mối nối.
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan } from "../chung";

export const vetSangSchema = coBan.extend({
  goc: z.number().default(-32),
});

const VACH = [
  { tre: 0, rong: 3, lech: -260 },
  { tre: 0.06, rong: 9, lech: -120 },
  { tre: 0.1, rong: 2, lech: 0 },
  { tre: 0.16, rong: 14, lech: 90 },
  { tre: 0.2, rong: 4, lech: 230 },
];

export const VetSang: React.FC<z.infer<typeof vetSangSchema>> = ({ goc }) => {
  const frame = useCurrentFrame();
  const { width, height, durationInFrames } = useVideoConfig();
  const p = frame / durationInFrames;
  const di = (tre: number) =>
    interpolate(p, [tre, tre + 0.72], [-0.35 * width, 1.35 * width], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.inOut(Easing.cubic),
    });
  const loe = interpolate(p, [0.3, 0.5, 0.7], [0, 0.55, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const dai = Math.hypot(width, height) * 1.4;

  return (
    <AbsoluteFill>
      {VACH.map((v, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            left: di(v.tre) + v.lech,
            top: height / 2 - dai / 2,
            width: v.rong,
            height: dai,
            rotate: `${goc}deg`,
            background: "linear-gradient(180deg, transparent, rgba(255,255,255,0.95) 30%, rgba(255,255,255,0.95) 70%, transparent)",
            boxShadow: `0 0 ${v.rong * 3}px ${v.rong}px rgba(255,255,255,0.55)`,
          }}
        />
      ))}
      <div
        style={{
          position: "absolute",
          left: di(0.08) - 260,
          top: height / 2 - dai / 2,
          width: 420,
          height: dai,
          rotate: `${goc}deg`,
          background: "linear-gradient(90deg, transparent, rgba(255,255,255,0.35), transparent)",
          filter: "blur(18px)",
        }}
      />
      <AbsoluteFill style={{ background: "white", opacity: loe }} />
    </AbsoluteFill>
  );
};
