// Vòng HUD đếm số kiểu promo đài truyền hình: vòng ống kính có vạch chia, mũi tên, vòng nét đứt xoay ngược nhau,
// hai thanh đo hai bên dâng theo số. Số đếm nhanh rồi chậm dần khi gần đích. Cuối clip số vỡ thành ô vuông,
// lộ logo ATT giữa vòng. Học từ reel THĐT (10/2026); hình tự vẽ bằng SVG, không lấy tài nguyên của video mẫu.
// Nền trong suốt: đắp lên montage cắt nhanh (xem hieu-ung-video/references/ky-thuat-tu-video-mau.md).
import React from "react";
import { AbsoluteFill, Easing, interpolate, random, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FONT, FPS, LogoATT, soVN } from "../chung";

export const hudDemSoSchema = coBan.extend({
  tu: z.number().default(0),
  den: z.number().default(100),
  tai: z.number().min(0).default(0.3), // giây bắt đầu đếm
  denLuc: z.number().min(0).default(4), // giây chạm số đích
  voO: z.boolean().default(true), // vỡ ô vuông rồi lộ logo ở 0,8 giây cuối
  mau: z.string().default("#FFFFFF"),
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const LUOI = 10; // số ô mỗi cạnh vùng số khi vỡ
const VO = 0.8; // giây vỡ ô

export const HudDemSo: React.FC<z.infer<typeof hudDemSoSchema>> = (p) => {
  const frame = useCurrentFrame();
  const { width, height, durationInFrames } = useVideoConfig();
  const t = frame / FPS;
  const r = Math.min(width, height) * 0.4;
  const cx = width / 2;
  const cy = height / 2;

  const vao = interpolate(t, [0, 0.4], [0, 1], { ...kep, easing: Easing.bezier(0.16, 1, 0.3, 1) });
  const ra = interpolate(frame, [durationInFrames - 6, durationInFrames], [1, 0], kep);
  const tien = interpolate(t, [p.tai, p.denLuc], [0, 1], { ...kep, easing: Easing.out(Easing.poly(1.5)) });
  const so = Math.round(p.tu + (p.den - p.tu) * tien);
  const batDauVo = p.voO ? (durationInFrames / FPS) - VO : Infinity;
  const vo = interpolate(t, [batDauVo, batDauVo + VO * 0.6], [0, 1], kep);

  const net = Math.max(2, r * 0.012);
  const quay = t * 12; // độ/giây

  // vạch chia vòng ngoài
  const vach = Array.from({ length: 120 }, (_, i) => {
    const g = (i * 3 * Math.PI) / 180;
    const dai = i % 10 === 0 ? r * 0.06 : r * 0.03;
    return (
      <line key={i} x1={Math.cos(g) * r * 1.04} y1={Math.sin(g) * r * 1.04}
        x2={Math.cos(g) * (r * 1.04 + dai)} y2={Math.sin(g) * (r * 1.04 + dai)}
        stroke={p.mau} strokeWidth={net * 0.6} opacity={0.75} />
    );
  });

  // mũi tên tam giác rỗng ở 4 hướng, chỉ vào tâm
  const muiTen = [0, 90, 180, 270].map((goc) => (
    <polygon key={goc} transform={`rotate(${goc}) translate(0 ${-r * 0.93})`}
      points={`${-r * 0.05},${-r * 0.04} ${r * 0.05},${-r * 0.04} 0,${r * 0.05}`}
      fill="none" stroke={p.mau} strokeWidth={net} />
  ));

  // thanh đo hai bên: khung mảnh + mức dâng theo số
  const thanh = (x: number) => {
    const cao = height * 0.55;
    const y0 = cy - cao / 2;
    return (
      <g>
        <rect x={x - net * 3} y={y0} width={net * 6} height={cao} fill="none" stroke={p.mau} strokeWidth={net * 0.6} opacity={0.6} />
        <rect x={x - net * 3} y={y0 + cao * (1 - tien)} width={net * 6} height={cao * tien} fill={p.mau} opacity={0.85} />
      </g>
    );
  };

  const coChu = r * 0.42;
  const kieuSo: React.CSSProperties = {
    fontFamily: FONT, fontWeight: 700, fontSize: coChu, color: p.mau, lineHeight: 1,
    textShadow: `0 0 ${r * 0.05}px rgba(255,255,255,.6)`, fontVariantNumeric: "tabular-nums",
  };
  const hop = r * 1.1; // vùng vuông quanh số, chia LUOI×LUOI ô khi vỡ
  const o = hop / LUOI;

  return (
    <AbsoluteFill style={{ opacity: vao * ra }}>
      <svg width={width} height={height} style={{ position: "absolute" }}>
        {thanh(cx - r * 1.5)}
        {thanh(cx + r * 1.5)}
        <g transform={`translate(${cx} ${cy}) scale(${0.7 + 0.3 * vao})`}>
          <g transform={`rotate(${quay})`}>{vach}</g>
          <circle r={r} fill="none" stroke={p.mau} strokeWidth={net * 1.6} />
          {muiTen}
          <circle r={r * 0.82} fill="none" stroke={p.mau} strokeWidth={net * 0.5} strokeDasharray={`${net} ${net * 2}`}
            transform={`rotate(${-quay * 1.5})`} opacity={0.7} />
          <circle r={r * 0.68} fill="none" stroke={p.mau} strokeWidth={net * 0.5} strokeDasharray={`${net * 4} ${net * 3}`}
            transform={`rotate(${quay * 2})`} opacity={0.55} />
          {/* cung sáng chạy vòng */}
          <circle r={r * 0.75} fill="none" stroke={p.mau} strokeWidth={net * 1.2}
            strokeDasharray={`${r * 0.9} ${r * 4}`} transform={`rotate(${quay * 4 - 90})`} opacity={0.9} />
        </g>
        {/* ô vuông bay ra quanh vùng số khi vỡ */}
        {vo > 0 &&
          Array.from({ length: 90 }, (_, i) => {
            const hien = random(`hien${i}`) * 0.6;
            const a = interpolate(vo, [hien, hien + 0.15, hien + 0.4], [0, 0.9, 0], kep);
            // bám lưới ô để ra mảng khảm vuông vức như mẫu, không rải lộn xộn
            const x = cx + Math.floor((random(`x${i}`) - 0.5) * 16) * o;
            const y = cy + Math.floor((random(`y${i}`) - 0.5) * 16) * o;
            const c = random(`c${i}`) > 0.3 ? o * 0.92 : o * 0.45;
            return <rect key={i} x={x} y={y} width={c} height={c} fill={random(`m${i}`) > 0.5 ? "#0B2E22" : "#3E8C6C"} opacity={a} />;
          })}
      </svg>

      {/* số: cắt thành ô, mỗi ô biến mất ở một thời điểm ngẫu nhiên khi vỡ */}
      <div style={{ position: "absolute", left: cx - hop / 2, top: cy - hop / 2, width: hop, height: hop }}>
        {Array.from({ length: LUOI * LUOI }, (_, k) => {
          const i = k % LUOI;
          const j = Math.floor(k / LUOI);
          const mat = vo > 0 && vo >= random(`o${k}`) * 0.85;
          if (mat) return null;
          return (
            <div key={k} style={{ position: "absolute", left: i * o, top: j * o, width: o + 0.5, height: o + 0.5, overflow: "hidden" }}>
              <div style={{ position: "absolute", left: -i * o, top: -j * o, width: hop, height: hop,
                display: "flex", alignItems: "center", justifyContent: "center", ...kieuSo }}>
                {soVN(so)}
              </div>
            </div>
          );
        })}
      </div>

      {p.voO ? (
        <div style={{ position: "absolute", left: 0, top: 0, width, height, display: "flex", alignItems: "center",
          justifyContent: "center", opacity: interpolate(vo, [0.5, 1], [0, 1], kep),
          transform: `scale(${interpolate(vo, [0.5, 1], [0.85, 1], kep)})` }}>
          <LogoATT cao={r * 0.28} />
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
