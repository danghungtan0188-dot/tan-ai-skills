// Thẻ số liệu: con số lớn đếm lên, kèm (tuỳ chọn) biểu đồ cột ngang mọc lần lượt. Vào/ra mờ để lộ video bên dưới.
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FONT, FPS, LogoATT, MAU, NEN_NAVY, soVN, vaoRa } from "../chung";

export const soLieuSchema = coBan.extend({
  tieuDe: z.string(),
  giaTri: z.number(),
  soLe: z.number().int().min(0).max(3).default(0),
  tienTo: z.string().default(""),
  donVi: z.string().default(""),
  moTa: z.string().default(""),
  cot: z.array(z.object({ nhan: z.string(), giaTri: z.number() })).default([]),
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const muot = Easing.bezier(0.16, 1, 0.3, 1);

export const SoLieu: React.FC<z.infer<typeof soLieuSchema>> = (p) => {
  const frame = useCurrentFrame();
  const { width, durationInFrames } = useVideoConfig();
  const doc = p.tiLe === "9:16";
  const s = width / (doc ? 1080 : 1920);
  const dem = interpolate(frame, [0.4 * FPS, 1.9 * FPS], [0, p.giaTri], { ...kep, easing: Easing.out(Easing.cubic) });
  const lon = Math.max(...p.cot.map((c) => c.giaTri), 1);
  const rongCot = (doc ? 640 : 900) * s;

  return (
    <AbsoluteFill style={{ opacity: vaoRa(frame, durationInFrames, 0.4, 0.5) }}>
      <AbsoluteFill style={{ background: NEN_NAVY }} />
      <div style={{ position: "absolute", top: 60 * s, right: (doc ? 60 : 80) * s }}>
        <LogoATT cao={70 * s} />
      </div>
      <AbsoluteFill
        style={{
          justifyContent: "center",
          alignItems: "center",
          fontFamily: FONT,
          padding: `0 ${(doc ? 80 : 160) * s}px`,
          textAlign: "center",
        }}
      >
        <div
          style={{
            color: "white",
            fontWeight: 700,
            fontSize: (doc ? 64 : 62) * s,
            lineHeight: 1.2,
            translate: interpolate(frame, [0, 0.6 * FPS], ["0px 40px", "0px 0px"], { ...kep, easing: muot }),
          }}
        >
          {p.tieuDe}
        </div>
        <div
          style={{
            color: MAU.vang,
            fontWeight: 700,
            fontSize: (doc ? 190 : 210) * s,
            lineHeight: 1.1,
            marginTop: 20 * s,
            fontVariantNumeric: "tabular-nums",
            scale: interpolate(frame, [1.8 * FPS, 2.05 * FPS, 2.3 * FPS], [1, 1.06, 1], kep),
          }}
        >
          {p.tienTo}
          {soVN(dem, p.soLe)}
          <span style={{ fontSize: (doc ? 90 : 100) * s, marginLeft: 12 * s }}>{p.donVi}</span>
        </div>
        {p.moTa ? (
          <div
            style={{
              color: MAU.xanhNhat,
              fontSize: (doc ? 46 : 44) * s,
              marginTop: 10 * s,
              opacity: interpolate(frame, [1.2 * FPS, 1.7 * FPS], [0, 1], kep),
            }}
          >
            {p.moTa}
          </div>
        ) : null}
        {p.cot.length ? (
          <div style={{ marginTop: 50 * s, display: "flex", flexDirection: "column", gap: 22 * s }}>
            {p.cot.map((c, i) => {
              const bd = (1.6 + i * 0.25) * FPS;
              return (
                <div key={i} style={{ display: "flex", alignItems: "center", gap: 20 * s }}>
                  <div
                    style={{
                      width: (doc ? 220 : 280) * s,
                      textAlign: "right",
                      color: "white",
                      fontSize: (doc ? 38 : 36) * s,
                    }}
                  >
                    {c.nhan}
                  </div>
                  <div
                    style={{
                      height: (doc ? 46 : 44) * s,
                      borderRadius: 6 * s,
                      background: i === p.cot.length - 1 ? MAU.vang : MAU.xanhNhat,
                      width: interpolate(frame, [bd, bd + 0.7 * FPS], [0, (rongCot * c.giaTri) / lon], {
                        ...kep,
                        easing: muot,
                      }),
                    }}
                  />
                  <div
                    style={{
                      color: "white",
                      fontWeight: 700,
                      fontSize: (doc ? 38 : 36) * s,
                      opacity: interpolate(frame, [bd + 0.5 * FPS, bd + 0.8 * FPS], [0, 1], kep),
                    }}
                  >
                    {soVN(c.giaTri, p.soLe)}
                  </div>
                </div>
              );
            })}
          </div>
        ) : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
