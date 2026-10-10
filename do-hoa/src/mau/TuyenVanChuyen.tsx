// Sơ đồ minh họa tuyến vận chuyển (không phải bản đồ đo đạc — góc ghi rõ "Sơ đồ minh họa"):
// nền giấy cũ, kênh và quốc lộ vẽ mảnh; đường đi nét đứt màu đồng vẽ dần, chấm sáng chạy theo,
// tên từng điểm hiện khi chấm tới (mốc `tai` khớp lời đọc). Toàn khung, toạ độ theo khung 1920x1080.
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FONT, FPS } from "../chung";

const diem = z.object({ ten: z.string(), x: z.number(), y: z.number(), tai: z.number(), canhTrai: z.boolean().default(false) });

export const tuyenVanChuyenSchema = coBan.extend({
  tieuDe: z.string().default(""),
  diem: z.array(diem),
  kenh: z.object({ ten: z.string(), tu: z.tuple([z.number(), z.number()]), den: z.tuple([z.number(), z.number()]) }).optional(),
  duong: z.object({ ten: z.string(), tu: z.tuple([z.number(), z.number()]), den: z.tuple([z.number(), z.number()]) }).optional(),
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const NAU = "#3b2a18";
const DONG = "#9c6b2c";
const CHU_CHAN = "'Times New Roman', Cambria, serif";

export const TuyenVanChuyen: React.FC<z.infer<typeof tuyenVanChuyenSchema>> = ({ tieuDe, diem: ds, kenh, duong }) => {
  const frame = useCurrentFrame();
  const { width, durationInFrames } = useVideoConfig();
  const s = width / 1920;
  const t = frame / FPS;
  const vao = interpolate(t, [0, 0.6], [0, 1], kep);
  const day = interpolate(frame, [0, durationInFrames], [1, 1.04], kep);

  // vị trí chấm theo thời gian: nội suy tuyến tính giữa các điểm theo mốc tai
  const doan = ds.slice(1).map((d, i) => ({ a: ds[i], b: d }));
  const tienDo = (d: { a: { tai: number }; b: { tai: number } }) =>
    interpolate(t, [d.a.tai, d.b.tai], [0, 1], { ...kep, easing: Easing.inOut(Easing.quad) });
  let cham: [number, number] = [ds[0].x, ds[0].y];
  doan.forEach((d) => {
    const k = tienDo(d);
    if (t >= d.a.tai) cham = [d.a.x + (d.b.x - d.a.x) * k, d.a.y + (d.b.y - d.a.y) * k];
  });

  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse 80% 75% at 50% 45%, #e2d2b0 0%, #c4ab7f 60%, #7a5e3a 100%)", opacity: vao }}>
      <svg width={1920 * s} height={1080 * s} style={{ position: "absolute", opacity: 0.3, mixBlendMode: "multiply" }}>
        <filter id="giay2">
          <feTurbulence type="fractalNoise" baseFrequency="0.012 0.05" numOctaves="4" seed="9" />
          <feColorMatrix type="matrix" values="0 0 0 0 0.45  0 0 0 0 0.35  0 0 0 0 0.22  0 0 0 0.9 0" />
        </filter>
        <rect width="100%" height="100%" filter="url(#giay2)" />
      </svg>
      <AbsoluteFill style={{ scale: day }}>
        <svg width={1920 * s} height={1080 * s} viewBox="0 0 1920 1080">
          {kenh ? (
            <g>
              <line x1={kenh.tu[0]} y1={kenh.tu[1]} x2={kenh.den[0]} y2={kenh.den[1]} stroke="#5d7f8f" strokeWidth={16} strokeLinecap="round" opacity={0.55} />
              <text x={(kenh.tu[0] + kenh.den[0]) / 2 + 30} y={(kenh.tu[1] + kenh.den[1]) / 2} fill="#35525e"
                style={{ fontFamily: CHU_CHAN, fontStyle: "italic", fontSize: 34 }}>{kenh.ten}</text>
            </g>
          ) : null}
          {duong ? (
            <g>
              <line x1={duong.tu[0]} y1={duong.tu[1]} x2={duong.den[0]} y2={duong.den[1]} stroke="#6b5a45" strokeWidth={7} strokeDasharray="2 0" opacity={0.6} />
              <line x1={duong.tu[0]} y1={duong.tu[1]} x2={duong.den[0]} y2={duong.den[1]} stroke="#efe3c8" strokeWidth={2} strokeDasharray="14 10" opacity={0.8} />
              <text x={duong.tu[0] + 20} y={duong.tu[1] - 18} fill="#4f402e" style={{ fontFamily: CHU_CHAN, fontStyle: "italic", fontSize: 32 }}>
                {duong.ten}
              </text>
            </g>
          ) : null}
          {doan.map((d, i) => {
            const k = tienDo(d);
            return (
              <line key={i} x1={d.a.x} y1={d.a.y} x2={d.a.x + (d.b.x - d.a.x) * k} y2={d.a.y + (d.b.y - d.a.y) * k}
                stroke={DONG} strokeWidth={7} strokeDasharray="18 12" strokeLinecap="round" />
            );
          })}
          {ds.map((d, i) => {
            const hien = interpolate(t, [d.tai - 0.1, d.tai + 0.4], [0, 1], kep);
            return (
              <g key={i} opacity={hien}>
                <circle cx={d.x} cy={d.y} r={15} fill="#f7efdc" stroke={NAU} strokeWidth={5} />
                <text x={d.canhTrai ? d.x - 30 : d.x + 30} y={d.y + 12} textAnchor={d.canhTrai ? "end" : "start"} fill={NAU}
                  style={{ fontFamily: CHU_CHAN, fontWeight: 700, fontSize: 44 }}>{d.ten}</text>
              </g>
            );
          })}
          <circle cx={cham[0]} cy={cham[1]} r={13} fill="#fff6dc" style={{ filter: "drop-shadow(0 0 10px #ffd27a)" }} />
        </svg>
      </AbsoluteFill>
      {tieuDe ? (
        <div style={{ position: "absolute", top: 60 * s, left: 90 * s, fontFamily: CHU_CHAN, fontWeight: 700, fontSize: 48 * s, color: NAU }}>
          {tieuDe}
        </div>
      ) : null}
      <div style={{ position: "absolute", bottom: 40 * s, right: 60 * s, fontFamily: FONT, fontStyle: "italic", fontSize: 26 * s, color: "#5a4630" }}>
        Sơ đồ minh họa
      </div>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse 75% 70% at 50% 45%, transparent 60%, rgba(40,20,0,0.5) 100%)" }} />
    </AbsoluteFill>
  );
};
