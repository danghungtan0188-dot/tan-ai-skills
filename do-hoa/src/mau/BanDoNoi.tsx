// Bản đồ xã nổi khối (học từ phóng sự "Lương Hòa đồng hành cùng doanh nghiệp", 10/2026): nền xanh đêm có ranh giới
// các xã lân cận mờ; một nét trắng sáng chạy hết viền xã, phủ màu ngọc, rồi khối nổi lên (nhiều lớp lệch xuống, mép
// sáng); máy quay phóng chậm; tên xã gõ từng chữ ở góc dưới trái; cuối lóe trắng để nối sang flycam.
// `vong` / `langGieng` là toạ độ pixel bất kỳ (ví dụ lấy từ ban_do.json của BanDoVeTinh) — tự co vừa khung.
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FPS } from "../chung";

const vong = z.array(z.tuple([z.number(), z.number()]));
export const banDoNoiSchema = coBan.extend({
  font: z.string().default("Arial, 'Segoe UI', sans-serif"),
  ten: z.string(),
  vong,
  langGieng: z.array(vong).default([]),
  loeCuoi: z.boolean().default(true),
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const NGOC = "#2FB8C4", MEP = "#C8F7FF";

export const BanDoNoi: React.FC<z.infer<typeof banDoNoiSchema>> = ({ font, ten, vong: v, langGieng, loeCuoi }) => {
  const frame = useCurrentFrame();
  const { width: W, height: H, durationInFrames } = useVideoConfig();
  const t = frame / FPS, het = durationInFrames / FPS, s = H / 1080;

  // co vừa 62% chiều cao, đặt giữa
  const xs = v.map((p) => p[0]), ys = v.map((p) => p[1]);
  const [x0, x1, y0, y1] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)];
  const k = Math.min((W * 0.62) / (x1 - x0), (H * 0.62) / (y1 - y0));
  const ox = W / 2 - ((x0 + x1) / 2) * k, oy = H / 2 - ((y0 + y1) / 2) * k;
  const d = (r: [number, number][]) => r.map((p, i) => `${i ? "L" : "M"} ${(p[0] * k + ox).toFixed(1)} ${(p[1] * k + oy).toFixed(1)}`).join(" ") + " Z";
  const chuVi = v.slice(1).reduce((a, p, i) => a + Math.hypot(p[0] - v[i][0], p[1] - v[i][1]), 0) * k;

  const nen = interpolate(t, [0, 0.8], [0, 1], kep);
  const ve = interpolate(t, [0.6, 2.4], [0, 1], { ...kep, easing: Easing.inOut(Easing.cubic) });
  const phu = interpolate(t, [2.1, 2.9], [0, 1], kep);
  const noi = interpolate(t, [2.6, 3.7], [0, 1], { ...kep, easing: Easing.out(Easing.back(1.4)) });
  const so = Math.floor(interpolate(t, [3.4, 3.4 + ten.length * 0.05], [0, ten.length], kep));
  const loe = loeCuoi ? interpolate(t, [het - 0.6, het - 0.2, het], [0, 1, 1], kep) : 0;
  const phong = interpolate(t, [0, het], [0.9, 1.06]);
  const day = 22 * s * noi; // độ dày khối
  const lop = 12;

  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 45%, #13305A 0%, #0A1B36 55%, #050D1C 100%)" }}>
      <AbsoluteFill style={{ scale: `${phong}`, perspective: 1600 * s }}>
        <svg width={W} height={H} style={{ position: "absolute", transform: "rotateX(18deg)", overflow: "visible" }}>
          {langGieng.map((r, i) => <path key={i} d={d(r)} fill="none" stroke="#6F8DB8" strokeOpacity={0.35 * nen} strokeWidth={1.5 * s} />)}
          {/* thân khối: các lớp lệch xuống, tối dần */}
          {noi > 0 ? Array.from({ length: lop }, (_, i) => (
            <path key={i} d={d(v)} transform={`translate(0 ${day * (1 - i / lop)})`} fill={i === 0 ? "#0E5A66" : "#14707E"} opacity={phu} />
          )) : null}
          {/* mặt trên */}
          <path d={d(v)} fill={NGOC} fillOpacity={0.9 * phu} />
          <path d={d(v)} fill="none" stroke={MEP} strokeWidth={4 * s} strokeLinejoin="round" opacity={phu}
            style={{ filter: `drop-shadow(0 0 ${6 * s}px ${MEP})` }} />
          {/* nét trắng chạy viền */}
          <path d={d(v)} fill="none" stroke="#FFFFFF" strokeWidth={5 * s} strokeLinejoin="round"
            strokeDasharray={chuVi} strokeDashoffset={chuVi * (1 - ve)} opacity={1 - phu * 0.7}
            style={{ filter: `drop-shadow(0 0 ${10 * s}px #FFFFFF)` }} />
        </svg>
      </AbsoluteFill>
      <div style={{
        position: "absolute", left: W * 0.06, bottom: H * 0.08, fontFamily: font, fontWeight: 900, fontSize: 40 * s,
        color: "#FFFFFF", letterSpacing: 3 * s, textShadow: `0 ${2 * s}px ${8 * s}px rgba(0,0,0,0.8)`,
      }}>{ten.slice(0, so)}</div>
      <AbsoluteFill style={{ background: "radial-gradient(circle at 50% 45%, #FFFFFF 0%, rgba(220,245,255,0.9) 45%, rgba(220,245,255,0) 80%)", opacity: loe }} />
    </AbsoluteFill>
  );
};
