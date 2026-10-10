// Ảnh tư liệu kiểu phim tài liệu: tấm ảnh in viền trắng, bóng đổ, hơi nghiêng, đặt trên nền giấy cũ,
// máy đẩy chậm vào; chú thích chữ nghiêng có chân dưới ảnh. Dùng cho ảnh nhỏ/ảnh chụp từ sách —
// không phóng toàn màn hình nên không lộ mờ. Toàn khung (không trong suốt). Ảnh đọc qua staticFile (--public-dir).
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FPS } from "../chung";

export const anhTuLieuSchema = coBan.extend({
  anh: z.string(),
  chuThich: z.string().default(""),
  chuThichPhu: z.string().default(""),
  nghieng: z.number().default(-2),
  dichLen: z.number().default(0), // px (khung 1080p) day tam anh len, tranh de dong phu de loi binh
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const CHU_CHAN = "'Times New Roman', Cambria, serif"; // Georgia thiếu dấu tiếng Việt chồng (ầ, ấ)

export const AnhTuLieu: React.FC<z.infer<typeof anhTuLieuSchema>> = ({ anh, chuThich, chuThichPhu, nghieng, dichLen }) => {
  const frame = useCurrentFrame();
  const { width, durationInFrames } = useVideoConfig();
  const s = width / 1920;
  const t = frame / FPS;
  const vao = spring({ frame, fps: FPS, config: { damping: 18, mass: 1.1 } });
  const day = interpolate(frame, [0, durationInFrames], [1, 1.06], { ...kep, easing: Easing.inOut(Easing.quad) });
  const chu = interpolate(t, [0.6, 1.3], [0, 1], kep);

  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse 80% 75% at 50% 45%, #d9c7a4 0%, #b89d71 55%, #6f5636 100%)" }}>
      {/* vân giấy cũ */}
      <svg width={1920 * s} height={1080 * s} style={{ position: "absolute", opacity: 0.35, mixBlendMode: "multiply" }}>
        <filter id="giay">
          <feTurbulence type="fractalNoise" baseFrequency="0.012 0.05" numOctaves="4" seed="4" />
          <feColorMatrix type="matrix" values="0 0 0 0 0.45  0 0 0 0 0.35  0 0 0 0 0.22  0 0 0 0.9 0" />
        </filter>
        <rect width="100%" height="100%" filter="url(#giay)" />
      </svg>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", scale: day }}>
        <div
          style={{
            background: "#f7f3ea",
            padding: `${22 * s}px ${22 * s}px ${chuThich ? 110 * s : 22 * s}px`,
            boxShadow: `0 ${24 * s}px ${50 * s}px rgba(30,15,0,0.55), 0 ${4 * s}px ${8 * s}px rgba(0,0,0,0.3)`,
            rotate: `${nghieng + (1 - vao) * 4}deg`,
            translate: `0 ${((1 - vao) * 120 - dichLen) * s}px`,
            opacity: Math.min(1, vao * 1.4),
            position: "relative",
          }}
        >
          <Img src={staticFile(anh)} style={{ display: "block", width: 1180 * s, height: "auto", filter: "sepia(0.15) contrast(1.05)" }} />
          {chuThich ? (
            <div
              style={{
                position: "absolute",
                left: 0,
                right: 0,
                bottom: 18 * s,
                textAlign: "center",
                fontFamily: CHU_CHAN,
                color: "#3b2a18",
                opacity: chu,
              }}
            >
              <div style={{ fontSize: 34 * s, fontStyle: "italic", fontWeight: 700 }}>{chuThich}</div>
              {chuThichPhu ? <div style={{ fontSize: 28 * s, fontStyle: "italic", marginTop: 4 * s }}>{chuThichPhu}</div> : null}
            </div>
          ) : null}
        </div>
      </AbsoluteFill>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse 75% 70% at 50% 45%, transparent 60%, rgba(40,20,0,0.55) 100%)" }} />
    </AbsoluteFill>
  );
};
