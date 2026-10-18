// Tiêu đề có từ nhấn: chữ đậm trắng + cụm nhấn nghiêng có chân màu vàng (kiểu reel "one *habit*"), từng từ hiện
// từ mờ sang nét, một đường viền bo tròn tự vẽ quanh dòng chữ, đốm sáng trôi chậm trên nền tối. Toàn khung.
import React from "react";
import { AbsoluteFill, Easing, interpolate, random, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FONT, FPS, MAU } from "../chung";

export const tieuDeNhanSchema = coBan.extend({
  chu: z.string(), // phần thường
  nhan: z.string(), // phần nhấn (nghiêng, vàng)
  phu: z.string().default(""),
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const SERIF = "Georgia, 'Times New Roman', serif";

export const TieuDeNhan: React.FC<z.infer<typeof tieuDeNhanSchema>> = ({ chu, nhan, phu }) => {
  const frame = useCurrentFrame();
  const { width: W, height: H, durationInFrames } = useVideoConfig();
  const t = frame / FPS;
  const s = Math.min(W / 1920, H / 1080);
  const ra = interpolate(frame, [durationInFrames - 0.5 * FPS, durationInFrames], [1, 0], kep);
  const tu = [...chu.split(" ").map((w) => ({ w, n: false })), ...nhan.split(" ").map((w) => ({ w, n: true }))];
  const vien = interpolate(t, [0.9, 2.1], [0, 1], { ...kep, easing: Easing.inOut(Easing.cubic) });

  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 55%, #1B2340 0%, #07090F 75%)", opacity: ra }}>
      {Array.from({ length: 22 }, (_, i) => {
        const r = (8 + random(`r${i}`) * 26) * s;
        return (
          <div
            key={i}
            style={{
              position: "absolute", width: r, height: r, borderRadius: "50%",
              left: random(`x${i}`) * W, top: random(`y${i}`) * H - t * (6 + random(`v${i}`) * 14) * s,
              background: "rgba(255,205,45,0.55)", filter: `blur(${r * 0.35}px)`,
              opacity: 0.25 + 0.35 * Math.sin(t * 1.5 + random(`p${i}`) * 6.28) ** 2,
            }}
          />
        );
      })}
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", flexDirection: "column", gap: 34 * s }}>
        <div style={{ position: "relative", padding: `${26 * s}px ${70 * s}px`, display: "flex", gap: 22 * s, alignItems: "baseline" }}>
          <svg style={{ position: "absolute", inset: 0, overflow: "visible" }} width="100%" height="100%">
            <rect x="0" y="0" width="100%" height="100%" rx={70 * s} fill="none" stroke={MAU.vang} strokeWidth={4 * s}
              pathLength={1} strokeDasharray={1} strokeDashoffset={1 - vien} />
          </svg>
          {tu.map(({ w, n }, i) => {
            const vao = 0.2 + i * 0.12;
            return (
              <span
                key={i}
                style={{
                  fontFamily: n ? SERIF : FONT, fontStyle: n ? "italic" : "normal", fontWeight: n ? 400 : 800,
                  fontSize: (n ? 112 : 96) * s, color: n ? MAU.vang : "white", whiteSpace: "nowrap",
                  opacity: interpolate(t, [vao, vao + 0.35], [0, 1], kep),
                  filter: `blur(${interpolate(t, [vao, vao + 0.45], [14, 0], kep) * s}px)`,
                  translate: `0px ${interpolate(t, [vao, vao + 0.5], [24, 0], { ...kep, easing: Easing.out(Easing.cubic) }) * s}px`,
                }}
              >
                {w}
              </span>
            );
          })}
        </div>
        {phu ? (
          <div style={{ fontFamily: FONT, fontSize: 38 * s, color: "#C9D3EA", letterSpacing: 6 * s, opacity: interpolate(t, [1.6, 2.2], [0, 1], kep) }}>
            {phu}
          </div>
        ) : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
