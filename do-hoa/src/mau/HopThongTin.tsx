// Hộp thông tin kiểu phóng sự truyền hình (đo từ phóng sự VHTV): vạch trắng dọc bên trái,
// dòng đầu nghiêng nét thường, các dòng sau đậm có bóng đổ; nằm góc trái dưới. Nền trong suốt —
// khi đắp, làm mờ video phía sau trong lúc hộp hiện để chữ nổi (việc của ffmpeg).
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FONT, FPS } from "../chung";

export const hopThongTinSchema = coBan.extend({
  dongNghieng: z.string().default(""),
  dong: z.array(z.string()),
  cachDay: z.number().default(70), // px từ đáy khung 1080p; nâng lên khi có phụ đề
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const ra = Easing.out(Easing.cubic);

export const HopThongTin: React.FC<z.infer<typeof hopThongTinSchema>> = ({ dongNghieng, dong, cachDay }) => {
  const frame = useCurrentFrame();
  const { width, durationInFrames } = useVideoConfig();
  const s = width / 1920;
  const t = frame / FPS;
  const het = durationInFrames / FPS;
  const tat = interpolate(t, [het - 0.4, het], [1, 0], kep);
  const vach = interpolate(t, [0, 0.35], [0, 1], { ...kep, easing: ra });
  const bong = `${4 * s}px ${5 * s}px 0 rgba(0,0,0,0.55), 0 0 ${18 * s}px rgba(0,0,0,0.45)`;
  const tatCa = [...(dongNghieng ? [dongNghieng] : []), ...dong];

  return (
    <AbsoluteFill style={{ opacity: tat }}>
      <div
        style={{
          position: "absolute",
          left: 180 * s,
          bottom: cachDay * s,
          width: 12 * s,
          height: (dongNghieng ? 92 : 0) * s + dong.length * 112 * s,
          background: "white",
          boxShadow: bong,
          transformOrigin: "50% 100%",
          scale: `1 ${vach}`,
        }}
      />
      <div style={{ position: "absolute", left: 240 * s, bottom: cachDay * s, fontFamily: FONT }}>
        {tatCa.map((d, i) => {
          const nghieng = dongNghieng && i === 0;
          const vao = interpolate(t, [0.15 + i * 0.12, 0.55 + i * 0.12], [0, 1], { ...kep, easing: ra });
          return (
            <div
              key={i}
              style={{
                height: (nghieng ? 92 : 112) * s,
                display: "flex",
                alignItems: "center",
                paddingLeft: nghieng ? 0 : 36 * s,
                fontSize: (nghieng ? 56 : 66) * s,
                fontWeight: nghieng ? 500 : 900,
                fontStyle: nghieng ? "italic" : "normal",
                color: "white",
                textShadow: bong,
                whiteSpace: "nowrap",
                opacity: vao,
                translate: `${(1 - vao) * -60 * s}px 0`,
              }}
            >
              {d}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
