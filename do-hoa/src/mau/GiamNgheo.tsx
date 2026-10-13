// Biểu đồ giảm nghèo: hai cột "trước" và "nay" trên dải tối mờ; cột trước mọc lên đúng `taiTruoc`, cột nay mọc
// (rất thấp) đúng `taiNay`, mũi tên chéo xuống nối hai cột, số đếm kiểu Việt Nam (0,58%). Nền trong suốt — đè lên cảnh quay.
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FONT, FPS } from "../chung";

export const giamNgheoSchema = coBan.extend({
  tieuDe: z.string().default("Tỷ lệ hộ nghèo"),
  truoc: z.object({ so: z.number(), nhan: z.string(), tienTo: z.string().default(""), soLe: z.number().default(0) }),
  nay: z.object({ so: z.number(), nhan: z.string(), tienTo: z.string().default(""), soLe: z.number().default(2) }),
  taiTruoc: z.number(),
  taiNay: z.number(),
  nenMo: z.boolean().default(true), // false: bo dai toi mo, chi giu chu/so (bong chu dam hon de van doc ro)
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const KEM = "#F3E9D2";
const DONG = "#C9A46A";
const soVN = (x: number, le: number) => {
  const [nguyen, phan] = x.toFixed(le).split(".");
  return nguyen.replace(/\B(?=(\d{3})+(?!\d))/g, ".") + (phan ? "," + phan : "");
};

export const GiamNgheo: React.FC<z.infer<typeof giamNgheoSchema>> = ({ tieuDe, truoc, nay, taiTruoc, taiNay, nenMo }) => {
  const frame = useCurrentFrame();
  const { width, durationInFrames } = useVideoConfig();
  const s = width / 1920;
  const t = frame / FPS;
  const het = durationInFrames / FPS;
  const nen = interpolate(t, [0, 0.4, het - 0.5, het], [0, 1, 1, 0], kep);
  const CAO = 330; // chieu cao cot "truoc" (lon nhat), px khung 1080p
  const cot = (x: { so: number }, tai: number) => interpolate(t, [tai, tai + 1.2], [0, x.so / 100], { ...kep, easing: Easing.out(Easing.cubic) });
  const k1 = cot(truoc, taiTruoc);
  const k2 = cot(nay, taiNay);
  const muiTen = interpolate(t, [taiNay - 0.2, taiNay + 0.8], [0, 1], { ...kep, easing: Easing.inOut(Easing.quad) });
  const Cot = ({ k, x, mau, sang }: { k: number; x: { so: number; nhan: string; tienTo: string; soLe: number }; mau: string; sang: boolean }) => (
    <div style={{ width: 300 * s, textAlign: "center" }}>
      <div style={{ height: (CAO + 120) * s, display: "flex", flexDirection: "column", justifyContent: "flex-end", alignItems: "center" }}>
        <div style={{ fontFamily: FONT, fontWeight: 900, fontSize: 96 * s, color: sang ? "#FFE7B0" : KEM, lineHeight: 1.1, opacity: k > 0 ? 1 : 0,
          textShadow: nenMo ? `0 ${4 * s}px ${14 * s}px rgba(0,0,0,0.7)` : `0 0 ${6 * s}px rgba(0,0,0,0.9), 0 ${3 * s}px ${14 * s}px rgba(0,0,0,0.85)` }}>
          {x.tienTo ? <span style={{ fontSize: 42 * s, fontWeight: 700, marginRight: 8 * s }}>{x.tienTo}</span> : null}
          {soVN(k * 100, x.soLe)}<span style={{ fontSize: 52 * s }}>%</span>
        </div>
        <div style={{ width: 150 * s, height: Math.max(k > 0 ? 6 : 0, ((k * 100) / truoc.so) * CAO) * s, marginTop: 14 * s, background: mau, borderRadius: `${6 * s}px ${6 * s}px 0 0`,
          boxShadow: sang ? `0 0 ${30 * s}px rgba(255,200,120,0.5)` : "none" }} />
      </div>
      <div style={{ height: 3 * s, background: DONG }} />
      <div style={{ marginTop: 18 * s, fontFamily: FONT, fontWeight: 700, fontSize: 36 * s, color: KEM, textShadow: nenMo ? `0 ${2 * s}px ${8 * s}px #000` : `0 0 ${6 * s}px rgba(0,0,0,0.9), 0 ${3 * s}px ${14 * s}px rgba(0,0,0,0.85)` }}>{x.nhan}</div>
    </div>
  );
  return (
    <AbsoluteFill style={{ opacity: nen }}>
      {nenMo ? (
      <div style={{ position: "absolute", left: 0, right: 0, top: 150 * s, height: 700 * s,
        background: "linear-gradient(180deg, transparent, rgba(6,12,28,0.74) 14%, rgba(6,12,28,0.74) 86%, transparent)" }} />
      ) : null}
      <div style={{ position: "absolute", top: 190 * s, width: "100%", textAlign: "center", fontFamily: FONT, fontStyle: "italic", fontSize: 42 * s,
        color: DONG, letterSpacing: 2 * s, textShadow: nenMo ? undefined : `0 0 ${6 * s}px rgba(0,0,0,0.9), 0 ${3 * s}px ${14 * s}px rgba(0,0,0,0.85)` }}>{tieuDe}</div>
      <div style={{ position: "absolute", top: 250 * s, width: "100%", display: "flex", justifyContent: "center", gap: 260 * s }}>
        <Cot k={k1} x={truoc} mau="rgba(243,233,210,0.55)" sang={false} />
        <Cot k={k2} x={nay} mau="#E2B65C" sang />
      </div>
      <svg width={1920 * s} height={1080 * s} viewBox="0 0 1920 1080" style={{ position: "absolute" }}>
        <path d="M900 420 Q960 470 1030 640" stroke={DONG} strokeWidth={6} fill="none" strokeDasharray="420" strokeDashoffset={420 * (1 - muiTen)} strokeLinecap="round" />
        <path d="M1008 618 L1032 646 L1044 610" stroke={DONG} strokeWidth={6} fill="none" opacity={muiTen > 0.95 ? 1 : 0} strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </AbsoluteFill>
  );
};
