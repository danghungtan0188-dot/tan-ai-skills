// Banner tên / chức vụ (lower-third), nền trong suốt để đắp lên video.
// Vị trí theo phong-cach-att-news.md: dưới trái, hộp bắt đầu ở 65,5% chiều cao, kết thúc trên dòng phụ đề.
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FONT, FPS, MAU } from "../chung";

export const lowerThirdSchema = coBan.extend({
  ten: z.string(),
  chucVu: z.string().default(""),
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const muot = Easing.bezier(0.16, 1, 0.3, 1);

export const LowerThird: React.FC<z.infer<typeof lowerThirdSchema>> = ({ ten, chucVu, tiLe }) => {
  const frame = useCurrentFrame();
  const { width, height, durationInFrames } = useVideoConfig();
  const doc = tiLe === "9:16";
  const s = width / (doc ? 1080 : 1920);
  const het = durationInFrames;
  const mo = interpolate(frame, [0.15 * FPS, 0.75 * FPS, het - 0.45 * FPS, het - 0.1 * FPS], [0, 100, 100, 0], {
    ...kep,
    easing: muot,
  });
  const vach = interpolate(frame, [0, 0.3 * FPS, het - 0.15 * FPS, het], [0, 1, 1, 0], kep);

  return (
    <AbsoluteFill>
      <div
        style={{
          position: "absolute",
          left: (doc ? 50 : 46) * s,
          top: doc ? 0.615 * height : 0.655 * height,
          maxWidth: (doc ? 980 : 1300) * s,
          display: "flex",
          fontFamily: FONT,
        }}
      >
        <div style={{ width: 12 * s, background: MAU.vang, scale: `1 ${vach}`, transformOrigin: "bottom" }} />
        <div style={{ clipPath: `inset(0 ${100 - mo}% 0 0)` }}>
          <div
            style={{
              background: "rgba(0, 28, 100, 0.92)",
              padding: `${14 * s}px ${34 * s}px ${14 * s}px ${26 * s}px`,
              color: "white",
              fontWeight: 700,
              fontSize: (doc ? 52 : 50) * s,
              lineHeight: 1.2,
            }}
          >
            {ten}
          </div>
          {chucVu ? (
            <div
              style={{
                background: "rgba(255, 255, 255, 0.95)",
                padding: `${8 * s}px ${34 * s}px ${8 * s}px ${26 * s}px`,
                color: MAU.navyNews,
                fontSize: (doc ? 36 : 34) * s,
                lineHeight: 1.25,
                translate: interpolate(frame, [0.45 * FPS, 0.95 * FPS], ["-30px 0px", "0px 0px"], { ...kep, easing: muot }),
              }}
            >
              {chucVu}
            </div>
          ) : null}
        </div>
      </div>
    </AbsoluteFill>
  );
};
