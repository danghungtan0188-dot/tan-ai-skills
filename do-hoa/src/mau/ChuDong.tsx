// "Chữ là nội dung" (kinetic typography) cho Reels/TikTok: chữ bật ra theo giọng đọc, từ đang đọc tô vàng.
// Mốc từng câu lấy từ phụ đề; trong câu, mốc từng từ chia theo số ký tự (ước lượng, giống tan_studio/subtitles.py).
import { Audio } from "@remotion/media";
import React from "react";
import { AbsoluteFill, Easing, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FONT, FPS, LogoATT, MAU, NEN_NAVY } from "../chung";

export const chuDongSchema = coBan.extend({
  cau: z.array(z.object({ chu: z.string(), start: z.number(), end: z.number() })),
  amThanh: z.string().default(""),
  tieuDe: z.string().default(""),
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

const mocTu = (chu: string, start: number, end: number) => {
  const tu = chu.split(/\s+/).filter(Boolean);
  const tong = tu.reduce((a, w) => a + w.length + 1, 0);
  let t = start;
  return tu.map((w) => {
    const bd = t;
    t += ((end - start) * (w.length + 1)) / tong;
    return { w, bd };
  });
};

export const ChuDong: React.FC<z.infer<typeof chuDongSchema>> = ({ cau, amThanh, tieuDe, tiLe }) => {
  const frame = useCurrentFrame();
  const { width, durationInFrames } = useVideoConfig();
  const giay = frame / FPS;
  const doc = tiLe === "9:16";
  const s = width / (doc ? 1080 : 1920);
  const i = cau.findIndex((c, k) => giay >= c.start && giay < (cau[k + 1]?.start ?? Infinity));
  const c = i >= 0 ? cau[i] : null;

  return (
    <AbsoluteFill style={{ background: NEN_NAVY, fontFamily: FONT }}>
      {amThanh ? <Audio src={staticFile(amThanh)} /> : null}
      <AbsoluteFill
        style={{
          background: "radial-gradient(circle at 50% 50%, rgba(40,110,220,0.5) 0%, rgba(40,110,220,0) 55%)",
          translate: `${interpolate(frame, [0, durationInFrames], [-120, 120]) * s}px 0`,
        }}
      />
      <div style={{ position: "absolute", top: 90 * s, width: "100%", display: "flex", justifyContent: "center" }}>
        <LogoATT cao={80 * s} />
      </div>
      {tieuDe ? (
        <div
          style={{
            position: "absolute",
            top: 210 * s,
            width: "100%",
            textAlign: "center",
            color: MAU.vang,
            fontWeight: 700,
            fontSize: 44 * s,
            letterSpacing: 2 * s,
          }}
        >
          {tieuDe.toUpperCase()}
        </div>
      ) : null}
      {c ? (
        <AbsoluteFill
          key={i}
          style={{
            justifyContent: "center",
            alignItems: "center",
            padding: `0 ${(doc ? 80 : 200) * s}px`,
            translate: interpolate(giay, [c.start, c.start + 0.25], ["0px 40px", "0px 0px"], {
              ...kep,
              easing: Easing.bezier(0.16, 1, 0.3, 1),
            }),
          }}
        >
          <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", columnGap: 22 * s, rowGap: 8 * s }}>
            {mocTu(c.chu, c.start, c.end).map(({ w, bd }, k, all) => {
              const dangDoc = giay >= bd && giay < (all[k + 1]?.bd ?? c.end);
              return (
                <span
                  key={k}
                  style={{
                    color: dangDoc ? MAU.vang : "white",
                    fontWeight: 700,
                    fontSize: (doc ? 96 : 88) * s,
                    lineHeight: 1.2,
                    opacity: interpolate(giay, [bd - 0.08, bd + 0.06], [0, 1], kep),
                    scale: interpolate(giay, [bd - 0.08, bd + 0.06, bd + 0.2], [0.6, 1.12, 1], kep),
                  }}
                >
                  {w}
                </span>
              );
            })}
          </div>
        </AbsoluteFill>
      ) : null}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          height: 10 * s,
          width: `${(frame / durationInFrames) * 100}%`,
          background: MAU.vang,
        }}
      />
    </AbsoluteFill>
  );
};
