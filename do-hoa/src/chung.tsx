// Màu, chữ, logo dùng chung — lấy đúng từ make_att_bugs.py / make_outro.py (phong cách ATT NEWS).
import React from "react";
import { CalculateMetadataFunction, Easing, interpolate } from "remotion";
import { z } from "zod";

export const FPS = 30;
export const FONT = "Arial, 'Segoe UI', sans-serif";

export const MAU = {
  navyTren: "#00164E",
  navyDuoi: "#0A3C92",
  navyNews: "#001C64",
  vang: "#FFCD2D",
  xanhNhat: "#A8C6F5",
  nenAtt: "#E8F2F4",
  att: ["#CE2027", "#007A3D", "#1A3CAA"],
};

export const NEN_NAVY = `linear-gradient(180deg, ${MAU.navyTren} 0%, ${MAU.navyDuoi} 100%)`;

export const coBan = z.object({
  tiLe: z.enum(["16:9", "9:16"]).default("16:9"),
  thoiLuong: z.number().min(1).max(120),
});

export const KICH_THUOC = { "16:9": [1920, 1080], "9:16": [1080, 1920] } as const;

/** Kích thước theo tỉ lệ, thời lượng theo giây; trong suốt thì mặc định xuất ProRes 4444 có kênh alpha. */
export const metadata =
  <T extends z.infer<typeof coBan>>(trongSuot: boolean): CalculateMetadataFunction<T> =>
  ({ props }) => {
    const [width, height] = KICH_THUOC[props.tiLe];
    return {
      width,
      height,
      durationInFrames: Math.round(props.thoiLuong * FPS),
      ...(trongSuot
        ? {
            defaultCodec: "prores",
            defaultProResProfile: "4444",
            defaultPixelFormat: "yuva444p10le",
            defaultVideoImageFormat: "png",
          }
        : // khung JPEG cho ra yuvj420p (dải màu PC) — nhiều trình phát không mở; PNG cho yuv420p chuẩn
          { defaultPixelFormat: "yuv420p", defaultVideoImageFormat: "png" }),
    };
  };

/** Vào trong `vao` giây, ra trong `ra` giây cuối: 0 → 1 → 0. */
export const vaoRa = (frame: number, tong: number, vao = 0.5, ra = 0.5) =>
  interpolate(frame, [0, vao * FPS, tong - ra * FPS, tong], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

/** Số kiểu Việt Nam: 12.500 ; 3,5 */
export const soVN = (n: number, le = 0) =>
  n.toLocaleString("vi-VN", { minimumFractionDigits: le, maximumFractionDigits: le });

export const LogoATT: React.FC<{ cao: number }> = ({ cao }) => {
  const bo = Math.max(3, Math.round(cao * 0.064));
  const dem = Math.round(cao * 0.17);
  return (
    <div style={{ display: "flex", height: cao, fontFamily: FONT, fontWeight: 700 }}>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          padding: `0 ${dem}px`,
          background: MAU.nenAtt,
          border: "2px solid white",
          borderRadius: bo,
          fontSize: cao * 0.59,
          zIndex: 1,
        }}
      >
        {"ATT".split("").map((c, i) => (
          <span key={i} style={{ color: MAU.att[i] }}>
            {c}
          </span>
        ))}
      </div>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          marginLeft: -bo,
          padding: `0 ${dem + 3}px 0 ${dem + bo}px`,
          background: MAU.navyNews,
          borderRadius: bo,
          color: "white",
          fontSize: cao * 0.51,
        }}
      >
        NEWS
      </div>
    </div>
  );
};
