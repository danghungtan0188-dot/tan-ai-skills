// Ảnh kết toàn khung (vd. cờ Đơn vị Anh hùng): phủ kín khung, máy đẩy chậm vào một điểm, một vệt sáng vàng
// lướt chéo qua sau `taiSang` giây, tối góc nhẹ. Toàn khung. Ảnh đọc qua staticFile (--public-dir).
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FPS } from "../chung";

export const anhKetSchema = coBan.extend({
  anh: z.string(),
  tamX: z.number().default(50), // % — điểm máy đẩy vào
  tamY: z.number().default(40),
  zoom: z.number().default(0.1),
  taiSang: z.number().default(1.5),
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

export const AnhKet: React.FC<z.infer<typeof anhKetSchema>> = ({ anh, tamX, tamY, zoom, taiSang }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const t = frame / FPS;
  const day = interpolate(frame, [0, durationInFrames], [1, 1 + zoom], { ...kep, easing: Easing.inOut(Easing.quad) });
  const sang = interpolate(t, [taiSang, taiSang + 1.6], [-30, 130], { ...kep, easing: Easing.inOut(Easing.cubic) });

  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <AbsoluteFill style={{ scale: day, transformOrigin: `${tamX}% ${tamY}%` }}>
        <Img src={staticFile(anh)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
        <AbsoluteFill
          style={{
            background: `linear-gradient(110deg, transparent ${sang - 10}%, rgba(255,236,170,0.45) ${sang}%, transparent ${sang + 10}%)`,
            mixBlendMode: "screen",
          }}
        />
      </AbsoluteFill>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse 80% 75% at 50% 45%, transparent 60%, rgba(0,0,0,0.45) 100%)" }} />
    </AbsoluteFill>
  );
};
