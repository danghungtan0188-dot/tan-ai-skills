// Số liệu chiến công kiểu phim tài liệu cao cấp, đắp lên tư liệu đen trắng: không dải tối, không quầng tối
// (chữ nổi nhờ bóng đậm nhiều lớp). Mỗi mục: số đếm lên ánh kim kem–vàng, vạch vàng mảnh mọc ra,
// nhãn chữ nhỏ; giữa các mục có vạch dọc mảnh. Vệt sáng lướt qua số khi đếm xong. Đặt ở 1/3 trên khung
// để không đè phụ đề. `tai`: giây mục hiện (khớp lúc lời đọc nhắc tới con số). Nền trong suốt.
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FONT, FPS } from "../chung";

export const soLieuChienCongSchema = coBan.extend({
  tieuDe: z.string().default(""), // dòng nghiêng nhỏ phía trên, vd "Kết quả trận đánh"
  cao: z.number().default(250), // px từ mép trên (khung 1080p) tới hàng số
  muc: z.array(
    z.object({
      so: z.number(),
      nhan: z.string(),
      tai: z.number().default(0),
      tienTo: z.string().default(""), // "trên", "hơn"
      donVi: z.string().default(""), // "tấn"
    }),
  ),
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const ra = Easing.out(Easing.cubic);
const KEM = "#F6EEDC";
const VANG = "#D8B26A";
const soVN = (x: number) => Math.round(x).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");

export const SoLieuChienCong: React.FC<z.infer<typeof soLieuChienCongSchema>> = ({ tieuDe, cao, muc }) => {
  const frame = useCurrentFrame();
  const { width, durationInFrames } = useVideoConfig();
  const s = width / 1920;
  const t = frame / FPS;
  const het = durationInFrames / FPS;
  const dau = Math.min(...muc.map((m) => m.tai), 0.3);
  const tong = interpolate(t, [Math.max(0, dau - 0.3), dau + 0.2, het - 0.5, het], [0, 1, 1, 0], kep);
  const bong = `0 0 ${4 * s}px rgba(0,0,0,0.95), 0 0 ${10 * s}px rgba(0,0,0,0.8), 0 ${3 * s}px ${22 * s}px rgba(0,0,0,0.9)`;

  return (
    <AbsoluteFill style={{ opacity: tong }}>
      {/* không dùng quầng tối dải rộng: alpha mờ dần khi đắp lên YUV tạo vòng sáng; chữ tự nổi nhờ bóng đậm */}
      {tieuDe ? (
        <div
          style={{
            position: "absolute",
            top: (cao - 70) * s,
            width: "100%",
            textAlign: "center",
            fontFamily: FONT,
            fontStyle: "italic",
            fontSize: 38 * s,
            letterSpacing: 3 * s,
            color: VANG,
            textShadow: bong,
            opacity: interpolate(t, [dau - 0.2, dau + 0.4], [0, 1], kep),
          }}
        >
          {tieuDe}
        </div>
      ) : null}
      <div style={{ position: "absolute", top: cao * s, width: "100%", display: "flex", justifyContent: "center", alignItems: "flex-start" }}>
        {muc.map((m, i) => {
          const vao = interpolate(t, [m.tai, m.tai + 0.55], [0, 1], { ...kep, easing: ra });
          const dem = interpolate(t, [m.tai, m.tai + 1.3], [0, m.so], { ...kep, easing: Easing.out(Easing.quad) });
          const vach = interpolate(t, [m.tai + 0.25, m.tai + 0.95], [0, 1], { ...kep, easing: ra });
          const sang = interpolate(t, [m.tai + 1.2, m.tai + 2.0], [-0.4, 1.4], kep);
          return (
            <React.Fragment key={i}>
              {i > 0 ? (
                <div
                  style={{
                    width: 2 * s,
                    height: 190 * s,
                    marginTop: 20 * s,
                    background: `linear-gradient(180deg, transparent, ${VANG} 30%, ${VANG} 70%, transparent)`,
                    opacity: 0.7 * vao,
                  }}
                />
              ) : null}
              <div
                style={{
                  minWidth: 380 * s,
                  padding: `0 ${50 * s}px`,
                  textAlign: "center",
                  opacity: vao,
                  translate: `0 ${(1 - vao) * 26 * s}px`,
                  filter: `blur(${(1 - vao) * 6 * s}px)`,
                }}
              >
                <div style={{ position: "relative", display: "inline-block", fontFamily: FONT, lineHeight: 1 }}>
                  {m.tienTo ? (
                    <span style={{ fontSize: 50 * s, fontWeight: 700, color: KEM, marginRight: 16 * s, textShadow: bong, verticalAlign: "38%" }}>
                      {m.tienTo}
                    </span>
                  ) : null}
                  <span
                    style={{
                      fontSize: 168 * s,
                      fontWeight: 700,
                      letterSpacing: -2 * s,
                      backgroundImage: `linear-gradient(105deg, ${KEM} 0%, ${KEM} ${sang * 100 - 12}%, #FFFFFF ${sang * 100}%, ${KEM} ${sang * 100 + 12}%, #E9D4A6 100%)`,
                      WebkitBackgroundClip: "text",
                      backgroundClip: "text",
                      color: "transparent",
                      filter: `drop-shadow(0 0 ${4 * s}px rgba(0,0,0,0.95)) drop-shadow(0 ${4 * s}px ${14 * s}px rgba(0,0,0,0.9))`,
                    }}
                  >
                    {soVN(dem)}
                  </span>
                  {m.donVi ? (
                    <span style={{ fontSize: 56 * s, fontWeight: 700, color: KEM, marginLeft: 14 * s, textShadow: bong }}>{m.donVi}</span>
                  ) : null}
                </div>
                <div
                  style={{
                    width: 150 * s,
                    height: 3 * s,
                    margin: `${20 * s}px auto ${16 * s}px`,
                    background: `linear-gradient(90deg, transparent, ${VANG}, transparent)`,
                    scale: `${vach} 1`,
                  }}
                />
                <div
                  style={{
                    fontFamily: FONT,
                    fontWeight: 700,
                    fontSize: 38 * s,
                    letterSpacing: 1.5 * s,
                    color: KEM,
                    textShadow: bong,
                    whiteSpace: "nowrap",
                    opacity: vach,
                  }}
                >
                  {m.nhan}
                </div>
              </div>
            </React.Fragment>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
