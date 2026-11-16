// Mở đầu bản tin ATT NEWS 25 s: học nhịp mở đầu bản tin đài huyện (cắt theo nhạc, mảng màu trượt mở ảnh, ảnh bay nhiều lớp,
// chia khung, tiêu đề lớn) nhưng thiết kế theo nhận diện ATT NEWS: navy + xanh lá + vàng, khung nghiêng như banner phóng sự,
// tia sáng chéo như KetLaser. Font Montserrat VN (đủ dấu tiếng Việt) nạp từ public dir. Ảnh và mốc cắt truyền qua props.
import React from "react";
import {
  AbsoluteFill, Easing, Img, interpolate, random, spring, staticFile, useCurrentFrame, useVideoConfig,
  continueRender, delayRender,
} from "remotion";
import { z } from "zod";
import { coBan, FPS, MAU } from "../chung";

export const moDauBanTinSchema = coBan.extend({
  tieuDe: z.string().default("BẢN TIN"),
  diaDanh: z.string().default("AN THẠNH THỦY"),
  chuDe: z.array(z.string()).default(["KINH TẾ", "VĂN HÓA", "XÃ HỘI"]),
  ngay: z.string().default(""),
  moc: z.array(z.number()).length(6), // giây bắt đầu cảnh 2..7, nên khớp nhịp nhạc
  anhMo: z.string(), anhTieuDe: z.string(), anhBay: z.array(z.string()).min(6),
  khung1: z.array(z.object({ anh: z.string(), nhan: z.string() })).length(3),
  khung2: z.array(z.object({ anh: z.string(), nhan: z.string() })).length(3),
  anhTin: z.string(), tinChay: z.string(), anhKet: z.string(),
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const ra = Easing.out(Easing.cubic);
const XANH = "#1A9A4A", NAVY = MAU.navyNews, VANG = MAU.vang;
const FONT = "MontVN, Arial, sans-serif";
const NGHIENG = "skewX(-14deg)";

const PHONG = [
  ["vietnamese", "U+0102-0103, U+0110-0111, U+0128-0129, U+0168-0169, U+01A0-01A1, U+01AF-01B0, U+0300-0301, U+0303-0304, U+0308-0309, U+0323, U+0329, U+1EA0-1EF9, U+20AB"],
  ["latin-ext", "U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF"],
  ["latin", "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD"],
];
const useFonts = () => {
  const [h] = React.useState(() => delayRender("font Montserrat VN"));
  React.useEffect(() => {
    Promise.all(PHONG.map(([ten, range]) => {
      const f = new FontFace("MontVN", `url(${staticFile(`montserrat-vn-normal-${ten}.woff2`)})`, { weight: "100 900", unicodeRange: range });
      return f.load().then((ff) => document.fonts.add(ff));
    })).then(() => continueRender(h)).catch(() => continueRender(h));
  }, [h]);
};

// Ảnh phủ kín ô, đẩy chậm
const Anh: React.FC<{ src: string; p: number; zoom?: [number, number]; lech?: number; mo?: number; toi?: number; style?: React.CSSProperties }> =
  ({ src, p, zoom = [1.05, 1.15], lech = 0, mo = 0, toi = 0, style }) => (
    <div style={{ position: "absolute", inset: 0, overflow: "hidden", ...style }}>
      <Img src={staticFile(src)} style={{
        width: "100%", height: "100%", objectFit: "cover",
        scale: `${interpolate(p, [0, 1], zoom)}`, translate: `${lech * p * 60}px 0px`, filter: `blur(${mo}px) brightness(${1 - toi})`,
      }} />
    </div>
  );

// Nền navy → xanh lá, lưới điểm, tia sáng chéo trôi
const Nen: React.FC<{ t: number }> = ({ t }) => {
  const { width: W, height: H } = useVideoConfig();
  return (
    <AbsoluteFill style={{ background: `linear-gradient(125deg, #04143F 0%, ${NAVY} 45%, #0B5E33 100%)` }}>
      <svg width={W} height={H} style={{ position: "absolute" }}>
        {Array.from({ length: 26 }, (_, i) => {
          const x = (random(`x${i}`) * W + t * 18 * (random(`v${i}`) - 0.5)) % W, y = random(`y${i}`) * H + Math.sin(t + i) * 14;
          return <circle key={i} cx={x} cy={y} r={2.5} fill="#BFF5D2" opacity={0.6} />;
        })}
        {Array.from({ length: 6 }, (_, k) => {
          const x = ((k * 0.21 + t * 0.07) % 1.3 - 0.15) * W;
          return <line key={k} x1={x - H} y1={H} x2={x + H * 0.3} y2={0} stroke="#E8FFF0" strokeOpacity={0.18 + 0.12 * (k % 2)} strokeWidth={2 + (k % 3)} />;
        })}
      </svg>
    </AbsoluteFill>
  );
};

// Chữ bật từng ký tự: trượt lên + từ mờ nhòe sang nét
const ChuBat: React.FC<{ text: string; t: number; t0: number; size: number; weight?: number; color?: string; cach?: number }> =
  ({ text, t, t0, size, weight = 900, color = "#FFFFFF", cach = 0.035 }) => (
    <div style={{ display: "flex", justifyContent: "center", fontFamily: FONT, fontWeight: weight, fontSize: size, color, letterSpacing: size * 0.01, lineHeight: 1.05 }}>
      {Array.from(text).map((c, i) => {
        const p = interpolate(t, [t0 + i * cach, t0 + i * cach + 0.45], [0, 1], { ...kep, easing: ra });
        return <span key={i} style={{ display: "inline-block", whiteSpace: "pre", opacity: p, translate: `0px ${(1 - p) * size * 0.45}px`,
          filter: `blur(${(1 - p) * 14}px)`, textShadow: `0 ${size * 0.04}px ${size * 0.1}px rgba(0,10,30,0.65)` }}>{c}</span>;
      })}
    </div>
  );

// Thanh địa danh: hộp navy nghiêng mở ra, viền xanh lá, gạch vàng
const ThanhDiaDanh: React.FC<{ text: string; t: number; t0: number; size?: number }> = ({ text, t, t0, size = 74 }) => {
  const mo = interpolate(t, [t0, t0 + 0.45], [0, 1], { ...kep, easing: ra });
  const vang = interpolate(t, [t0 + 0.35, t0 + 0.8], [0, 1], { ...kep, easing: ra });
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 18 }}>
      <div style={{ transform: NGHIENG, background: NAVY, borderBottom: `8px solid ${XANH}`, padding: `${size * 0.12}px ${size * 0.6}px`,
        clipPath: `inset(0 ${(1 - mo) * 50}% 0 ${(1 - mo) * 50}%)`, boxShadow: "0 18px 40px rgba(0,0,0,0.45)" }}>
        <div style={{ transform: "skewX(14deg)", fontFamily: FONT, fontWeight: 800, fontSize: size, color: "#FFFFFF", letterSpacing: size * (0.18 - 0.1 * mo) }}>{text}</div>
      </div>
      <div style={{ width: 360 * vang, height: 10, background: VANG, borderRadius: 5 }} />
    </div>
  );
};

// Logo ATT NEWS vẽ lại (ô ATT nền sáng + ô NEWS navy), theo tỉ lệ file gốc 268×78
const Logo: React.FC<{ w: number }> = ({ w }) => {
  const h = w * 78 / 268, w1 = w * 0.41;
  return (
    <svg width={w} height={h} style={{ filter: "drop-shadow(0 10px 22px rgba(0,0,0,0.5))" }}>
      <rect x={0} y={0} width={w1} height={h} rx={8} fill={MAU.nenAtt} />
      <rect x={w1 + 4} y={0} width={w - w1 - 4} height={h} rx={8} fill={NAVY} stroke="#FFFFFF" strokeOpacity={0.5} strokeWidth={2} />
      <text x={w1 / 2} y={h * 0.74} textAnchor="middle" fontSize={h * 0.66} fontWeight={900} fontFamily={FONT}>
        {["A", "T", "T"].map((c, i) => <tspan key={i} fill={MAU.att[i]}>{c}</tspan>)}
      </text>
      <text x={w1 + 4 + (w - w1 - 4) / 2} y={h * 0.74} textAnchor="middle" fontSize={h * 0.62} fontWeight={900} fontFamily={FONT} fill="#FFFFFF">NEWS</text>
    </svg>
  );
};

// Chùm sáng quét chéo một lần
const Quet: React.FC<{ t: number; t0: number; dai?: number }> = ({ t, t0, dai = 0.7 }) => {
  const p = (t - t0) / dai;
  if (p < 0 || p > 1) return null;
  return <AbsoluteFill style={{ background: `linear-gradient(115deg, transparent ${p * 140 - 40}%, rgba(255,255,255,0.55) ${p * 140 - 25}%, transparent ${p * 140 - 10}%)`, mixBlendMode: "screen" }} />;
};

// Khung nghiêng chứa ảnh + nhãn
const KhungNghieng: React.FC<{ anh: string; nhan: string; t: number; t0: number; i: number; tCanh: number }> = ({ anh, nhan, t, t0, i, tCanh }) => {
  const { width: W, height: H } = useVideoConfig();
  const v = spring({ frame: Math.round((t - t0 - i * 0.12) * FPS), fps: FPS, config: { damping: 18, mass: 0.8 } });
  const bw = W / 3 + 60, x = i * (W / 3) - 30, huong = i % 2 ? 1 : -1;
  const p = Math.min(1, (t - t0) / tCanh);
  return (
    <div style={{ position: "absolute", left: x, top: 0, width: bw, height: H, transform: `${NGHIENG} translateY(${(1 - v) * H * huong}px)`,
      overflow: "hidden", borderRight: `6px solid ${i === 1 ? VANG : XANH}` }}>
      <div style={{ position: "absolute", inset: "0 -120px", transform: "skewX(14deg)" }}>
        <Anh src={anh} p={p} zoom={[1.12, 1.02]} lech={huong} />
        <div style={{ position: "absolute", inset: 0, background: "linear-gradient(180deg, transparent 55%, rgba(0,12,40,0.85) 100%)" }} />
        <div style={{ position: "absolute", left: 160, right: 140, bottom: 120, fontFamily: FONT, fontWeight: 800, fontSize: 40, color: "#FFFFFF",
          opacity: interpolate(t, [t0 + 0.4 + i * 0.12, t0 + 0.8 + i * 0.12], [0, 1], kep), borderLeft: `8px solid ${VANG}`, paddingLeft: 18 }}>{nhan}</div>
      </div>
    </div>
  );
};

export const MoDauBanTin: React.FC<z.infer<typeof moDauBanTinSchema>> = (p) => {
  useFonts();
  const frame = useCurrentFrame();
  const { width: W, height: H, durationInFrames } = useVideoConfig();
  const t = frame / FPS, het = durationInFrames / FPS;
  const [A1, A2, A3, A4, A5, A6] = p.moc;
  // chuyển cảnh: lóe trắng + phóng nhòe 5 khung quanh mỗi mốc
  const gan = Math.min(...p.moc.map((m) => Math.abs(t - m)));
  const loe = gan < 0.17 ? 1 - gan / 0.17 : 0;
  let canh: React.ReactNode;

  if (t < A1) {   // 3 khung nghiêng trượt mở ảnh mở đầu + địa danh hiện từng chữ
    const q = t / A1;
    canh = (
      <AbsoluteFill>
        <Nen t={t} />
        {[0, 1, 2].map((i) => {
          const v = interpolate(t, [0.15 + i * 0.15, 0.85 + i * 0.15], [0, 1], { ...kep, easing: ra });
          return (
            <div key={i} style={{ position: "absolute", left: i * (W / 3) - 40, top: 0, width: W / 3 + 80, height: H, overflow: "hidden",
              transform: `${NGHIENG} translateY(${(1 - v) * (i % 2 ? -H : H)}px)` }}>
              <div style={{ position: "absolute", top: 0, left: -(i * (W / 3) - 40) - 140, width: W + 280, height: H, transform: "skewX(14deg)" }}>
                <Anh src={p.anhMo} p={q} zoom={[1.18, 1.06]} toi={0.15} />
              </div>
            </div>
          );
        })}
        <div style={{ position: "absolute", bottom: 120, width: "100%" }}><ChuBat text={p.diaDanh} t={t} t0={0.9} size={64} weight={800} cach={0.05} /></div>
      </AbsoluteFill>
    );
  } else if (t < A2) {   // tiêu đề lớn trên ảnh nhòe
    const q = (t - A1) / (A2 - A1);
    canh = (
      <AbsoluteFill>
        <Anh src={p.anhTieuDe} p={q} zoom={[1.15, 1.25]} mo={7} toi={0.45} />
        <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 50%, transparent 30%, rgba(0,10,35,0.75) 100%)" }} />
        <div style={{ position: "absolute", top: 120, width: "100%", display: "flex", justifyContent: "center",
          opacity: interpolate(t, [A1 + 0.1, A1 + 0.5], [0, 1], kep) }}><Logo w={300} /></div>
        <div style={{ position: "absolute", top: 300, width: "100%" }}><ChuBat text={p.tieuDe} t={t} t0={A1 + 0.25} size={250} /></div>
        <div style={{ position: "absolute", top: 600, width: "100%" }}><ThanhDiaDanh text={p.diaDanh} t={t} t0={A1 + 0.75} /></div>
        <Quet t={t} t0={A1 + 1.6} dai={0.9} />
      </AbsoluteFill>
    );
  } else if (t < A3) {   // thẻ ảnh 3D xoay vòng + chủ đề hiện theo nhịp
    const q = (t - A2) / (A3 - A2), n = p.anhBay.length;
    const the = p.anhBay.map((src, i) => {
      const goc = (i / n) * 360 + q * 70, rad = (goc * Math.PI) / 180, z = Math.cos(rad);
      return { src, i, goc, z, x: Math.sin(rad) * 760 };
    }).sort((a, b) => a.z - b.z);
    canh = (
      <AbsoluteFill>
        <Nen t={t} />
        <AbsoluteFill style={{ perspective: 1800 }}>
          {the.map(({ src, i, goc, z, x }) => (
            <div key={i} style={{ position: "absolute", left: W / 2 - 300 + x, top: H / 2 - 190, width: 600, height: 380, borderRadius: 14, overflow: "hidden",
              transform: `translateZ(${z * 360}px) rotateY(${-Math.sin((goc * Math.PI) / 180) * 35}deg)`,
              filter: `blur(${(1 - z) * 2.5}px) brightness(${0.55 + 0.45 * (z + 1) / 2})`, border: "4px solid rgba(255,255,255,0.85)",
              boxShadow: "0 25px 60px rgba(0,0,0,0.5)" }}>
              <Img src={staticFile(src)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
            </div>
          ))}
        </AbsoluteFill>
        <div style={{ position: "absolute", bottom: 110, width: "100%", display: "flex", justifyContent: "center", gap: 34 }}>
          {p.chuDe.map((c, i) => {
            const a = interpolate(t, [A2 + 0.3 + i * 0.72, A2 + 0.6 + i * 0.72], [0, 1], { ...kep, easing: ra });
            return (
              <div key={i} style={{ display: "flex", alignItems: "center", gap: 34, opacity: a, scale: `${0.7 + 0.3 * a}` }}>
                {i ? <div style={{ width: 16, height: 16, background: VANG, transform: "rotate(45deg)" }} /> : null}
                <div style={{ fontFamily: FONT, fontWeight: 900, fontSize: 70, color: "#FFFFFF", textShadow: "0 6px 18px rgba(0,0,0,0.6)" }}>{c}</div>
              </div>
            );
          })}
        </div>
      </AbsoluteFill>
    );
  } else if (t < A5) {   // chia 3 khung nghiêng, đổi bộ ảnh ở A4, chùm sáng quét
    const bo = t < A4 ? p.khung1 : p.khung2, t0 = t < A4 ? A3 : A4, tCanh = t < A4 ? A4 - A3 : A5 - A4;
    canh = (
      <AbsoluteFill>
        <Nen t={t} />
        {bo.map((k, i) => <KhungNghieng key={`${t0}-${i}`} anh={k.anh} nhan={k.nhan} t={t} t0={t0} i={i} tCanh={tCanh} />)}
        <Quet t={t} t0={t0 + 0.8} dai={0.8} />
      </AbsoluteFill>
    );
  } else if (t < A6) {   // ảnh toàn + thanh tin chạy kiểu đài
    const q = (t - A5) / (A6 - A5), v = interpolate(t, [A5 + 0.1, A5 + 0.5], [0, 1], { ...kep, easing: ra });
    canh = (
      <AbsoluteFill>
        <Anh src={p.anhTin} p={q} zoom={[1.06, 1.14]} lech={0.8} toi={0.1} />
        <div style={{ position: "absolute", left: 0, right: 0, bottom: 110, height: 96, display: "flex", translate: `${(v - 1) * W}px 0px` }}>
          <div style={{ background: XANH, transform: NGHIENG, marginLeft: -20, padding: "0 46px", display: "flex", alignItems: "center", zIndex: 2 }}>
            <span style={{ transform: "skewX(14deg)", fontFamily: FONT, fontWeight: 900, fontSize: 46, color: "#FFFFFF" }}>TIN TỨC</span>
          </div>
          <div style={{ flex: 1, background: "rgba(0,28,100,0.92)", overflow: "hidden", display: "flex", alignItems: "center", borderTop: `4px solid ${VANG}` }}>
            <span style={{ whiteSpace: "nowrap", fontFamily: FONT, fontWeight: 700, fontSize: 44, color: "#FFFFFF", translate: `${W * 0.9 - (t - A5) * 420}px 0px` }}>{p.tinChay}</span>
          </div>
        </div>
      </AbsoluteFill>
    );
  } else {   // khối kết: logo + tiêu đề + địa danh trên ảnh nhòe, tia sáng
    const q = (t - A6) / (het - A6);
    canh = (
      <AbsoluteFill>
        <Anh src={p.anhKet} p={q} zoom={[1.2, 1.08]} mo={5} toi={0.5} />
        <Nen t={t} />
        <AbsoluteFill style={{ opacity: 0.0 }} />
        <div style={{ position: "absolute", top: 150, width: "100%", display: "flex", justifyContent: "center",
          opacity: interpolate(t, [A6 + 0.1, A6 + 0.5], [0, 1], kep), scale: `${interpolate(t, [A6 + 0.1, A6 + 0.6], [0.85, 1], { ...kep, easing: ra })}` }}><Logo w={380} /></div>
        <div style={{ position: "absolute", top: 330, width: "100%" }}><ChuBat text={p.tieuDe} t={t} t0={A6 + 0.35} size={240} /></div>
        <div style={{ position: "absolute", top: 620, width: "100%" }}><ThanhDiaDanh text={p.diaDanh} t={t} t0={A6 + 0.85} /></div>
        {p.ngay ? <div style={{ position: "absolute", top: 820, width: "100%", textAlign: "center", fontFamily: FONT, fontWeight: 600, fontSize: 40,
          color: "#DDF7E6", opacity: interpolate(t, [A6 + 1.3, A6 + 1.8], [0, 1], kep), letterSpacing: 6 }}>{p.ngay}</div> : null}
        <Quet t={t} t0={A6 + 2.0} dai={1.0} />
      </AbsoluteFill>
    );
  }
  const tat = interpolate(t, [het - 0.5, het], [1, 0], kep);
  return (
    <AbsoluteFill style={{ backgroundColor: "#000", opacity: tat }}>
      <AbsoluteFill style={{ scale: `${1 + loe * 0.06}`, filter: loe ? `blur(${loe * 6}px)` : undefined }}>{canh}</AbsoluteFill>
      <AbsoluteFill style={{ backgroundColor: "#FFFFFF", opacity: loe * 0.7 }} />
    </AbsoluteFill>
  );
};
