// Intro tranh giấy nhiều lớp (kiểu lễ hội Trung thu): trời hoàng hôn, trăng lên, núi – mây – sóng cắt giấy
// đổ bóng chồng lớp, máy đẩy tới tạo chiều sâu. Chữ vàng viền tối mờ-nét hiện vào, cuối cùng cả tranh tách đôi
// như cửa mở để lộ video bên dưới (nền trong suốt). Hình vẽ toàn bằng SVG tự dựng, không dùng ảnh ngoài.
import React from "react";
import { AbsoluteFill, Easing, interpolate, random, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FONT, FPS } from "../chung";

export const tranhGiaySchema = coBan.extend({
  dongTren: z.string().default(""),
  dongChinh: z.string(),
  dongDuoi: z.string().default(""),
  moCua: z.boolean().default(true), // cuối clip tách đôi lộ video; false = giữ tranh tới hết
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const muot = Easing.bezier(0.16, 1, 0.3, 1);

// Sóng: dải lượn đều + vòng xoắn ở đỉnh sóng, như giấy cắt.
const Song: React.FC<{ W: number; H: number; y: number; bien: number; buoc: number; mau: string; vien: string }> = ({
  W, H, y, bien, buoc, mau, vien,
}) => {
  let d = `M ${-buoc} ${y}`;
  for (let x = -buoc; x < W + buoc; x += buoc) d += ` q ${buoc / 4} ${-bien} ${buoc / 2} 0 t ${buoc / 2} 0`;
  d += ` L ${W + buoc} ${H + 50} L ${-buoc} ${H + 50} Z`;
  const xoan = [];
  for (let x = -buoc + buoc / 4; x < W + buoc; x += buoc)
    xoan.push(<circle key={x} cx={x} cy={y - bien * 0.35} r={bien * 0.32} fill="none" stroke={vien} strokeWidth={bien * 0.1} />);
  return (
    <g>
      <path d={d} fill={mau} stroke={vien} strokeWidth={bien * 0.12} />
      {xoan}
    </g>
  );
};

// Mây tường vân: cụm tròn chồng nhau trên một đế bo tròn.
const May: React.FC<{ x: number; y: number; r: number }> = ({ x, y, r }) => (
  <g>
    {[[-1.4, 0.2], [-0.6, -0.5], [0.4, -0.7], [1.3, 0], [0, 0.1]].map(([dx, dy], i) => (
      <circle key={i} cx={x + dx * r} cy={y + dy * r} r={r * (i === 4 ? 1.1 : 0.85)} fill="#FFF4DC" stroke="#E0A93A" strokeWidth={r * 0.08} />
    ))}
    <rect x={x - 2.4 * r} y={y + 0.3 * r} width={4.8 * r} height={0.9 * r} rx={0.45 * r} fill="#FFF4DC" stroke="#E0A93A" strokeWidth={r * 0.08} />
  </g>
);

const BONG = "drop-shadow(0 10px 14px rgba(0,0,0,0.45))";

const Tranh: React.FC<{ W: number; H: number; tien: number; trang: number }> = ({ W, H, tien, trang }) => {
  // tien 0→1: máy đẩy tới. Lớp càng gần càng phóng to/trôi xuống nhiều.
  const lop = (sau: number) => ({ scale: 1 + sau * 0.25 * tien, translate: `0px ${sau * 60 * tien}px`, filter: BONG });
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ background: "linear-gradient(180deg, #0B1640 0%, #2B2F7A 40%, #E0663A 72%, #F6B04A 85%)" }} />
      {/* trăng */}
      <AbsoluteFill>
        <div
          style={{
            position: "absolute", left: W / 2 - H * 0.16, top: interpolate(trang, [0, 1], [H * 0.62, H * 0.22]),
            width: H * 0.32, height: H * 0.32, borderRadius: "50%",
            background: "radial-gradient(circle at 40% 38%, #FFFBE6 0%, #FFE08A 55%, #F2B64A 100%)",
            boxShadow: `0 0 ${H * 0.12}px ${H * 0.04}px rgba(255,214,120,0.7)`,
          }}
        />
      </AbsoluteFill>
      <svg width={W} height={H} style={{ position: "absolute", ...lop(0.2) }}>
        <path d={`M0 ${H * 0.62} L${W * 0.15} ${H * 0.45} L${W * 0.3} ${H * 0.6} L${W * 0.48} ${H * 0.4} L${W * 0.66} ${H * 0.58} L${W * 0.85} ${H * 0.43} L${W} ${H * 0.6} L${W} ${H} L0 ${H} Z`} fill="#1F6F78" stroke="#E0A93A" strokeWidth={4} />
      </svg>
      <svg width={W} height={H} style={{ position: "absolute", ...lop(0.4), translate: `${interpolate(tien, [0, 1], [0, -W * 0.04])}px ${24 * tien}px` }}>
        <May x={W * 0.18} y={H * 0.3} r={H * 0.045} />
        <May x={W * 0.8} y={H * 0.24} r={H * 0.055} />
      </svg>
      <svg width={W} height={H} style={{ position: "absolute", ...lop(0.6) }}>
        <Song W={W} H={H} y={H * 0.7} bien={H * 0.06} buoc={W * 0.12} mau="#2E8C8A" vien="#F3D27A" />
      </svg>
      <svg width={W} height={H} style={{ position: "absolute", ...lop(0.8) }}>
        <Song W={W} H={H} y={H * 0.8} bien={H * 0.075} buoc={W * 0.16} mau="#1B4E6B" vien="#F6E2A8" />
      </svg>
      <svg width={W} height={H} style={{ position: "absolute", ...lop(1) }}>
        <Song W={W} H={H} y={H * 0.92} bien={H * 0.09} buoc={W * 0.21} mau="#0F2C4A" vien="#FFE9B0" />
      </svg>
    </AbsoluteFill>
  );
};

export const TranhGiay: React.FC<z.infer<typeof tranhGiaySchema>> = ({ dongTren, dongChinh, dongDuoi, moCua }) => {
  const frame = useCurrentFrame();
  const { width: W, height: H, durationInFrames } = useVideoConfig();
  const t = frame / FPS;
  const het = durationInFrames / FPS;
  const s = Math.min(W / 1920, H / 1080);
  const tien = interpolate(frame, [0, durationInFrames], [0, 1], { ...kep, easing: Easing.inOut(Easing.quad) });
  const trang = interpolate(t, [0, 2.5], [0, 1], { ...kep, easing: muot });
  const cua = moCua ? interpolate(t, [het - 1.2, het], [0, 1], { ...kep, easing: Easing.in(Easing.cubic) }) : 0;

  const chu = (vao: number, co: number, mau: string, dam: boolean) => ({
    fontFamily: FONT, fontWeight: 900, fontSize: co * s, color: mau, textAlign: "center" as const, lineHeight: 1.15,
    opacity: interpolate(t, [vao, vao + 0.6], [0, 1], kep),
    filter: `blur(${interpolate(t, [vao, vao + 0.7], [18, 0], kep) * s}px)`,
    scale: interpolate(t, [vao, vao + 0.9], [1.25, 1], { ...kep, easing: muot }),
    ...(dam
      ? { WebkitTextStroke: `${6 * s}px #3A1C05`, paintOrder: "stroke fill", textShadow: `0 0 ${24 * s}px rgba(255,200,80,0.85)` }
      : { WebkitTextStroke: `${3 * s}px #2A1404`, paintOrder: "stroke fill", textShadow: `0 ${3 * s}px ${8 * s}px rgba(0,0,0,0.6)` }),
  });

  // Đốm sáng lấp lánh, vị trí cố định theo seed để render lại vẫn y hệt.
  const dom = Array.from({ length: 28 }, (_, i) => {
    const x = random(`x${i}`) * W, y = random(`y${i}`) * H * 0.6;
    const nhay = 0.5 + 0.5 * Math.sin(t * 4 + random(`p${i}`) * 6.28);
    return <div key={i} style={{ position: "absolute", left: x, top: y, width: 6 * s, height: 6 * s, borderRadius: "50%", background: "#FFE9A8", opacity: nhay * trang, boxShadow: `0 0 ${10 * s}px #FFD36A` }} />;
  });

  const noiDung = (
    <AbsoluteFill>
      <Tranh W={W} H={H} tien={tien} trang={trang} />
      {dom}
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", paddingBottom: H * 0.18, gap: 10 * s }}>
        {dongTren ? <div style={chu(1.0, 54, "#FFE7A0", false)}>{dongTren}</div> : null}
        <div style={chu(1.3, 104, "#FFD23F", true)}>{dongChinh}</div>
        {dongDuoi ? <div style={chu(1.9, 50, "#FFF4DC", false)}>{dongDuoi}</div> : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );

  // Cửa mở: hai nửa tranh trượt sang hai bên, lộ nền trong suốt (video bên dưới).
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ clipPath: "inset(0 50% 0 0)", translate: `${-cua * W * 0.55}px 0px` }}>{noiDung}</AbsoluteFill>
      <AbsoluteFill style={{ clipPath: "inset(0 0 0 50%)", translate: `${cua * W * 0.55}px 0px` }}>{noiDung}</AbsoluteFill>
    </AbsoluteFill>
  );
};
