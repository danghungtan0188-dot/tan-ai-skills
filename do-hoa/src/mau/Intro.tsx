// Intro bản tin: logo ATT NEWS bật vào, vạch vàng quét, tiêu đề trượt lên từng dòng, rồi mờ dần lộ video bên dưới.
import React from "react";
import { AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FONT, FPS, LogoATT, MAU, NEN_NAVY } from "../chung";

export const introSchema = coBan.extend({
  tieuDe: z.string(),
  phuDe: z.string().default(""),
  ngay: z.string().default(""),
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

export const Intro: React.FC<z.infer<typeof introSchema>> = ({ tieuDe, phuDe, ngay, tiLe }) => {
  const frame = useCurrentFrame();
  const { width, durationInFrames } = useVideoConfig();
  const doc = tiLe === "9:16";
  const s = width / (doc ? 1080 : 1920);
  const dong = tieuDe.split("\n");
  const ra = interpolate(frame, [durationInFrames - 0.6 * FPS, durationInFrames], [1, 0], {
    ...kep,
    easing: Easing.in(Easing.cubic),
  });

  return (
    <AbsoluteFill style={{ opacity: ra }}>
      <AbsoluteFill style={{ background: NEN_NAVY }} />
      <AbsoluteFill
        style={{
          background: "radial-gradient(ellipse at 50% 45%, rgba(40,110,220,0.45) 0%, rgba(40,110,220,0) 60%)",
          scale: interpolate(frame, [0, durationInFrames], [1, 1.15], kep),
        }}
      />
      <AbsoluteFill
        style={{
          justifyContent: "center",
          alignItems: "center",
          padding: `0 ${(doc ? 80 : 160) * s}px`,
          fontFamily: FONT,
          textAlign: "center",
        }}
      >
        <div
          style={{
            scale: spring({ frame, fps: FPS, config: { damping: 14, mass: 0.8 } }),
            marginBottom: 48 * s,
          }}
        >
          <LogoATT cao={(doc ? 110 : 120) * s} />
        </div>
        <div
          style={{
            height: 8 * s,
            width: interpolate(frame, [0.35 * FPS, 0.9 * FPS], [0, (doc ? 700 : 1100) * s], {
              ...kep,
              easing: Easing.bezier(0.16, 1, 0.3, 1),
            }),
            background: MAU.vang,
            borderRadius: 4 * s,
            marginBottom: 44 * s,
          }}
        />
        {dong.map((d, i) => (
          <div key={i} style={{ overflow: "hidden" }}>
            <div
              style={{
                color: "white",
                fontWeight: 700,
                fontSize: (doc ? 84 : 92) * s,
                lineHeight: 1.18,
                translate: interpolate(frame, [(0.6 + i * 0.15) * FPS, (1.2 + i * 0.15) * FPS], ["0px 120px", "0px 0px"], {
                  ...kep,
                  easing: Easing.bezier(0.16, 1, 0.3, 1),
                }),
              }}
            >
              {d}
            </div>
          </div>
        ))}
        {phuDe ? (
          <div
            style={{
              color: MAU.xanhNhat,
              fontSize: (doc ? 46 : 48) * s,
              marginTop: 28 * s,
              opacity: interpolate(frame, [1.3 * FPS, 1.8 * FPS], [0, 1], kep),
            }}
          >
            {phuDe}
          </div>
        ) : null}
        {ngay ? (
          <div
            style={{
              color: MAU.vang,
              fontSize: (doc ? 40 : 38) * s,
              fontWeight: 700,
              marginTop: 36 * s,
              letterSpacing: 2 * s,
              opacity: interpolate(frame, [1.6 * FPS, 2.1 * FPS], [0, 1], kep),
            }}
          >
            {ngay}
          </div>
        ) : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
