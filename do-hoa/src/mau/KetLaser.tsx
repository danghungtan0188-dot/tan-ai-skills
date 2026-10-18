// Outro ATT NEWS kiểu "tia laser vẽ logo" (tham khảo đoạn kết kênh truyền hình): nền navy có lưới điểm nối
// trôi chậm, chùm tia laser chéo từ góc phải quét ngang, đầu tia vẽ viền neon của logo ATT NEWS kèm tia lửa,
// loé sáng rồi logo hiện màu thật, dòng đơn vị + câu mời theo dõi (vàng) hiện sau, mờ về đen ở 0,6 s cuối.
// Hai ô QR hai bên chỉ hiện khi truyền file (không tự chế mã QR).
import React from "react";
import {
  AbsoluteFill, Easing, Img, interpolate, random, staticFile, useCurrentFrame, useVideoConfig,
  continueRender, delayRender,
} from "remotion";
import { z } from "zod";
import { coBan, FPS, MAU } from "../chung";

export const ketLaserSchema = coBan.extend({
  font: z.string().default(""), // .ttf trong public dir; trống = Arial
  donVi: z.string().default("Trung tâm Cung ứng dịch vụ công xã An Thạnh Thủy"),
  loiMoi: z.string().default("Theo dõi ATT NEWS để nhận bản tin của xã mỗi ngày"),
  qrTrai: z.string().default(""), // ảnh QR trong public dir; trống = không hiện
  qrPhai: z.string().default(""),
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const muot = Easing.bezier(0.16, 1, 0.3, 1);
const NEON = "#8FF3FF";

const dungFont = (file: string) => {
  const [xong] = React.useState(() => (file ? delayRender("font") : null));
  React.useEffect(() => {
    if (!file || xong === null) return;
    const f = new FontFace("KLaser", `url(${staticFile(file)})`, { weight: "100 900" });
    f.load().then((ff) => { document.fonts.add(ff); continueRender(xong); }).catch(() => continueRender(xong));
  }, [file, xong]);
  return file ? "KLaser, Arial, sans-serif" : "Arial, 'Segoe UI', sans-serif";
};

// Lưới điểm nối (plexus) trôi chậm
const LuoiDiem: React.FC<{ W: number; H: number; t: number }> = ({ W, H, t }) => {
  const diem = Array.from({ length: 34 }, (_, i) => ({
    x: random(`px${i}`) * W + Math.sin(t * 0.6 + i) * 30,
    y: random(`py${i}`) * H + Math.cos(t * 0.5 + i * 1.3) * 24,
  }));
  const day: React.ReactNode[] = [];
  diem.forEach((a, i) => diem.slice(i + 1).forEach((b, j) => {
    const d = Math.hypot(a.x - b.x, a.y - b.y);
    if (d < W * 0.16) day.push(<line key={`${i}-${j}`} x1={a.x} y1={a.y} x2={b.x} y2={b.y} stroke={NEON} strokeOpacity={0.4 * (1 - d / (W * 0.16))} strokeWidth={1.5} />);
  }));
  return (
    <svg width={W} height={H} style={{ position: "absolute" }}>
      {day}
      {diem.map((p, i) => <circle key={i} cx={p.x} cy={p.y} r={3.5} fill={NEON} opacity={0.75} />)}
    </svg>
  );
};

export const KetLaser: React.FC<z.infer<typeof ketLaserSchema>> = ({ font, donVi, loiMoi, qrTrai, qrPhai }) => {
  const frame = useCurrentFrame();
  const { width: W, height: H, durationInFrames } = useVideoConfig();
  const t = frame / FPS;
  const het = durationInFrames / FPS;
  const s = W / 1920;
  const ff = dungFont(font);

  // logo ATT NEWS vẽ lại bằng vector theo tỉ lệ file gốc 268×78 (ô ATT nền sáng + ô NEWS navy)
  const lw = 1000 * s, lh = lw * 78 / 268;
  const lx = (W - lw) / 2, ly = H * 0.3;
  const w1 = lw * 0.41, gap = lw * 0.008;

  const ve = interpolate(t, [0.15, 1.45], [0, 1], { ...kep, easing: Easing.inOut(Easing.cubic) }); // tiến độ vẽ viền
  const loe = interpolate(t, [1.4, 1.55, 2.0], [0, 1, 0], kep); // loé sáng
  const mau = interpolate(t, [1.5, 1.9], [0, 1], kep); // logo hiện màu thật
  const tia = interpolate(t, [0, 0.15, 1.45, 1.7], [0, 1, 1, 0], kep);
  const dong = interpolate(t, [1.8, 2.3], [0, 1], { ...kep, easing: muot });
  const moi = interpolate(t, [2.2, 3.0], [0, 1], { ...kep, easing: Easing.inOut(Easing.quad) });
  const qr = interpolate(t, [0.3, 0.8], [0, 1], { ...kep, easing: muot });
  const tat = interpolate(t, [het - 0.6, het], [1, 0], kep);

  const dau = lx + ve * lw; // đầu bút vẽ
  const chuViSo = 2 * (lw + lh) * 1.1;
  const vien = (x: number, w: number, key: string) => (
    <rect key={key} x={x} y={ly} width={w} height={lh} rx={10 * s} fill="none" stroke={NEON} strokeWidth={5 * s}
      strokeDasharray={chuViSo} strokeDashoffset={chuViSo * (1 - ve)} />
  );

  return (
    <AbsoluteFill style={{ fontFamily: ff, opacity: tat, backgroundColor: "#000" }}>
      <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 38%, ${MAU.navyDuoi} 0%, ${MAU.navyTren} 62%, #000818 100%)` }} />
      <LuoiDiem W={W} H={H} t={t} />

      {/* viền neon + logo */}
      <svg width={W} height={H} style={{ position: "absolute", filter: `drop-shadow(0 0 ${12 * s}px ${NEON})`, opacity: 1 - mau * 0.85 }}>
        {vien(lx, w1, "a")}
        {vien(lx + w1 + gap, lw - w1 - gap, "b")}
        <text x={lx + w1 / 2} y={ly + lh * 0.74} textAnchor="middle" fontSize={lh * 0.66} fontWeight={900} fontFamily={ff}
          fill="none" stroke={NEON} strokeWidth={3 * s} strokeDasharray={3000 * s} strokeDashoffset={3000 * s * (1 - ve)}>ATT</text>
        <text x={lx + w1 + gap + (lw - w1 - gap) / 2} y={ly + lh * 0.74} textAnchor="middle" fontSize={lh * 0.62} fontWeight={900} fontFamily={ff}
          fill="none" stroke={NEON} strokeWidth={3 * s} strokeDasharray={3000 * s} strokeDashoffset={3000 * s * (1 - ve)}>NEWS</text>
      </svg>
      <svg width={W} height={H} style={{ position: "absolute", opacity: mau, filter: `drop-shadow(0 ${10 * s}px ${26 * s}px rgba(0,0,0,0.55))` }}>
        <rect x={lx} y={ly} width={w1} height={lh} rx={10 * s} fill={MAU.nenAtt} />
        <rect x={lx + w1 + gap} y={ly} width={lw - w1 - gap} height={lh} rx={10 * s} fill={MAU.navyNews} stroke="#FFFFFF" strokeOpacity={0.5} strokeWidth={2 * s} />
        <text x={lx + w1 / 2} y={ly + lh * 0.74} textAnchor="middle" fontSize={lh * 0.66} fontWeight={900} fontFamily={ff}>
          {["A", "T", "T"].map((c, i) => <tspan key={i} fill={MAU.att[i]}>{c}</tspan>)}
        </text>
        <text x={lx + w1 + gap + (lw - w1 - gap) / 2} y={ly + lh * 0.74} textAnchor="middle" fontSize={lh * 0.62} fontWeight={900} fontFamily={ff} fill="#FFFFFF">NEWS</text>
      </svg>

      {/* chùm tia laser chéo từ góc trên phải, đầu tia bám đầu bút */}
      {tia > 0 ? (
        <svg width={W} height={H} style={{ position: "absolute", mixBlendMode: "screen", opacity: tia }}>
          <defs>
            <linearGradient id="tiaL" x1="1" y1="0" x2="0" y2="1">
              <stop offset="0" stopColor={NEON} stopOpacity="0" />
              <stop offset="0.75" stopColor={NEON} stopOpacity="0.7" />
              <stop offset="1" stopColor="#FFFFFF" stopOpacity="1" />
            </linearGradient>
          </defs>
          {Array.from({ length: 7 }, (_, k) => {
            const x2 = Math.max(lx, dau - k * 70 * s), y2 = k % 2 ? ly + lh : ly;
            return (
              <g key={k}>
                <line x1={x2 + 1100 * s} y1={y2 - 1100 * s} x2={x2} y2={y2} stroke="url(#tiaL)" strokeWidth={10 * s} strokeLinecap="round" style={{ filter: `blur(${3 * s}px)` }} />
                <line x1={x2 + 1100 * s} y1={y2 - 1100 * s} x2={x2} y2={y2} stroke="#FFFFFF" strokeOpacity={0.8} strokeWidth={2.5 * s} />
                <circle cx={x2} cy={y2} r={9 * s} fill="#FFFFFF" style={{ filter: `blur(${2 * s}px)` }} />
              </g>
            );
          })}
          {/* tia lửa văng ra ở đầu bút */}
          {Array.from({ length: 22 }, (_, i) => {
            const tuoi = ((t * 3 + random(`tl${i}`)) % 1);
            const goc = Math.PI * (0.15 + random(`tg${i}`) * 0.7);
            const v = (60 + random(`tv${i}`) * 140) * s;
            const x = dau + Math.cos(goc) * v * tuoi, y = ly + lh + Math.sin(goc) * v * tuoi + 120 * s * tuoi * tuoi;
            return <circle key={i} cx={x} cy={y} r={(4 - 3 * tuoi) * s} fill="#FFD86B" opacity={1 - tuoi} />;
          })}
        </svg>
      ) : null}

      {/* loé sáng khi logo hiện màu */}
      <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% ${(ly + lh / 2) / H * 100}%, rgba(220,250,255,0.9) 0%, rgba(143,243,255,0.25) 30%, transparent 60%)`, opacity: loe }} />

      {/* dòng đơn vị + câu mời */}
      <div style={{
        position: "absolute", left: 0, right: 0, top: ly + lh + 44 * s, textAlign: "center",
        fontSize: 54 * s, fontWeight: 700, color: "#FFFFFF", letterSpacing: 0.5 * s, opacity: dong,
        translate: `0px ${(1 - dong) * 24 * s}px`, textShadow: `0 0 ${18 * s}px rgba(143,243,255,0.7), 0 ${3 * s}px ${8 * s}px rgba(0,0,0,0.6)`,
      }}>{donVi}</div>
      <div style={{
        position: "absolute", left: 0, right: 0, top: ly + lh + 134 * s, textAlign: "center",
        fontSize: 68 * s, fontWeight: 800, fontStyle: "italic", color: MAU.vang,
        clipPath: `inset(0 ${(1 - moi) * 100}% 0 0)`, textShadow: `0 ${3 * s}px ${10 * s}px rgba(0,0,0,0.65)`,
      }}>{loiMoi}</div>

      {/* QR hai bên (chỉ khi có file) */}
      {[qrTrai, qrPhai].map((q, i) => q ? (
        <div key={i} style={{
          position: "absolute", top: H * 0.6, [i ? "right" : "left"]: 110 * s, width: 250 * s, height: 250 * s,
          background: "#FFFFFF", padding: 12 * s, borderRadius: 8 * s, opacity: qr, scale: `${0.8 + 0.2 * qr}`,
          boxShadow: `0 0 ${24 * s}px rgba(143,243,255,0.6)`,
        }}>
          <Img src={staticFile(q)} style={{ width: "100%", height: "100%", objectFit: "contain" }} />
        </div>
      ) : null)}
    </AbsoluteFill>
  );
};
