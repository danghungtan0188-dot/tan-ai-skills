// Thẻ mốc lịch sử toàn khung cho phim tài liệu (thay nền nâu trơn): nền than ấm có khói trôi chậm và
// tàn lửa bay lên, đường thời gian vàng mảnh chạy từ giữa ra, năm lớn vẽ viền rồi đổ đầy, dòng chính
// hiện dần, dòng phụ nghiêng. Có thể kèm 2–4 "trụ" (biểu tượng + nhãn) hiện lần lượt theo lời đọc.
import React from "react";
import { AbsoluteFill, Easing, interpolate, random, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FONT, FPS } from "../chung";

export const mocLichSuSchema = coBan.extend({
  nam: z.string().default(""),
  chu: z.string(),
  phu: z.string().default(""),
  taiChu: z.number().default(0.9),
  nenTrongSuot: z.boolean().default(false), // true: bo nen than/khoi/tan lua, chi giu chu + duong vang + tru de dat len tu lieu
  tru: z
    .array(z.object({ bieuTuong: z.enum(["lua", "thu", "nha", "co", "sung"]), nhan: z.string(), tai: z.number() }))
    .default([]),
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const ra = Easing.out(Easing.cubic);
const VANG = "#D8B26A";
const KEM = "#F3E9D2";

const BieuTuong: React.FC<{ loai: string; c: number }> = ({ loai, c }) => {
  const p = { fill: "none", stroke: VANG, strokeWidth: 3, strokeLinecap: "round" as const, strokeLinejoin: "round" as const };
  return (
    <svg width={c} height={c} viewBox="0 0 64 64">
      {loai === "lua" ? (
        <g {...p}>
          <path d="M32 58 V22" />
          <path d="M32 26 C24 22 22 14 24 8 C30 11 33 17 32 26" />
          <path d="M32 36 C22 33 18 25 19 18 C27 20 31 27 32 36" />
          <path d="M32 36 C42 33 46 25 45 18 C37 20 33 27 32 36" />
          <path d="M32 46 C23 44 18 37 18 31 C26 32 31 38 32 46" />
          <path d="M32 46 C41 44 46 37 46 31 C38 32 33 38 32 46" />
        </g>
      ) : null}
      {loai === "thu" ? (
        <g {...p}>
          <rect x="8" y="16" width="48" height="34" rx="3" />
          <path d="M8 18 L32 36 L56 18" />
        </g>
      ) : null}
      {loai === "nha" ? (
        <g {...p}>
          <path d="M8 30 L32 10 L56 30" />
          <path d="M14 26 V54 H50 V26" />
          <path d="M27 54 V40 H37 V54" />
        </g>
      ) : null}
      {loai === "co" ? (
        <g {...p}>
          <path d="M14 58 V6" />
          <path d="M14 8 H52 L46 19 L52 30 H14" />
        </g>
      ) : null}
      {loai === "sung" ? (
        <g {...p}>
          <path d="M6 26 H44 L58 22 V30 L44 30 H26 L22 44 H14 L18 30 H6 Z" />
        </g>
      ) : null}
    </svg>
  );
};

export const MocLichSu: React.FC<z.infer<typeof mocLichSuSchema>> = ({ nam, chu, phu, taiChu, tru, nenTrongSuot }) => {
  const frame = useCurrentFrame();
  const { width, height, durationInFrames } = useVideoConfig();
  const s = width / 1920;
  const t = frame / FPS;
  const het = durationInFrames / FPS;
  const toan = interpolate(t, [0, 0.5, het - 0.6, het], [0, 1, 1, 0], kep);
  const duong = interpolate(t, [0.2, 1.4], [0, 1], { ...kep, easing: Easing.inOut(Easing.cubic) });
  const vien = interpolate(t, [0.3, 1.5], [1, 0], { ...kep, easing: Easing.inOut(Easing.quad) });
  const day = interpolate(t, [1.2, 1.9], [0, 1], { ...kep, easing: ra });
  const vaoChu = interpolate(t, [taiChu, taiChu + 0.8], [0, 1], { ...kep, easing: ra });
  const vaoPhu = interpolate(t, [taiChu + 0.5, taiChu + 1.2], [0, 1], { ...kep, easing: ra });
  const coTru = tru.length > 0;
  const yDuong = coTru ? 0.43 : 0.52;

  // tàn lửa bay lên: vị trí cố định theo seed để render xác định
  const tan = Array.from({ length: 46 }, (_, i) => {
    const x0 = random(`x${i}`) * width;
    const v = 18 + random(`v${i}`) * 40;
    const pha = random(`p${i}`) * height;
    const y = height - ((pha + t * v * s * 2) % (height * 1.1));
    const r = (1 + random(`r${i}`) * 2.6) * s;
    const nhay = 0.35 + 0.65 * Math.abs(Math.sin(t * (1.5 + random(`n${i}`) * 3) + i));
    return { x: x0 + Math.sin(t * 0.6 + i) * 18 * s, y, r, a: nhay * (0.25 + random(`a${i}`) * 0.5) };
  });

  return (
    <AbsoluteFill style={{ background: nenTrongSuot ? undefined : "#0B0A09", opacity: toan, overflow: "hidden" }}>
      {nenTrongSuot ? null : (<>
      {/* khói: hai lớp nhiễu trôi ngược chiều */}
      <svg width={width} height={height} style={{ position: "absolute", inset: 0 }}>
        <defs>
          <filter id="khoi" x="0" y="0" width="100%" height="100%">
            <feTurbulence type="fractalNoise" baseFrequency={0.0016 / s} numOctaves={4} seed={7} />
            <feColorMatrix values="0 0 0 0 0.55  0 0 0 0 0.45  0 0 0 0 0.33  0 0 0 0.85 -0.28" />
          </filter>
        </defs>
        <rect x={-width * 0.3 + t * 22 * s} y={-height * 0.1} width={width * 1.6} height={height * 1.2} filter="url(#khoi)" opacity={0.55} />
        <rect x={-width * 0.1 - t * 14 * s} y={-height * 0.05} width={width * 1.4} height={height * 1.1} filter="url(#khoi)" opacity={0.3} transform={`scale(-1,1) translate(${-width},0)`} />
      </svg>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 48%, rgba(70,48,22,0.35) 0%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.75) 100%)" }} />
      {tan.map((e, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            left: e.x,
            top: e.y,
            width: e.r * 2,
            height: e.r * 2,
            borderRadius: "50%",
            background: "#FFC977",
            opacity: e.a * toan,
            boxShadow: `0 0 ${6 * s}px ${2 * s}px rgba(255,170,80,0.55)`,
          }}
        />
      ))}
      </>)}
      {/* đường thời gian */}
      <div
        style={{
          position: "absolute",
          top: height * yDuong,
          left: width * 0.5 - (width * 0.36 * duong),
          width: width * 0.72 * duong,
          height: 2 * s,
          background: `linear-gradient(90deg, transparent, ${VANG} 18%, ${VANG} 82%, transparent)`,
          boxShadow: `0 0 ${10 * s}px rgba(216,178,106,0.6)`,
        }}
      />
      <div
        style={{
          position: "absolute",
          top: height * yDuong - 9 * s,
          left: width * 0.5 - 9 * s,
          width: 18 * s,
          height: 18 * s,
          borderRadius: "50%",
          background: VANG,
          scale: String(duong),
          boxShadow: `0 0 ${(14 + 10 * Math.sin(t * 3)) * s}px ${4 * s}px rgba(255,200,120,0.7)`,
        }}
      />
      {nam ? (
        <svg
          width={width}
          height={260 * s}
          style={{ position: "absolute", left: 0, top: height * yDuong - 250 * s }}
        >
          <text
            x="50%"
            y={200 * s}
            textAnchor="middle"
            fontFamily={FONT}
            fontWeight={900}
            fontSize={220 * s}
            letterSpacing={18 * s}
            fill={`rgba(243,233,210,${day})`}
            stroke={VANG}
            strokeWidth={2.5 * s}
            strokeDasharray={1400 * s}
            strokeDashoffset={1400 * s * vien}
            style={{ filter: `drop-shadow(0 ${4 * s}px ${18 * s}px rgba(0,0,0,0.8))` }}
          >
            {nam}
          </text>
        </svg>
      ) : null}
      <div
        style={{
          position: "absolute",
          top: height * yDuong + (nam ? 46 : -150) * s,
          width: "100%",
          textAlign: "center",
          fontFamily: FONT,
          fontWeight: 700,
          fontSize: (nam ? 66 : 104) * s,
          letterSpacing: interpolate(vaoChu, [0, 1], [16, 6]) * s,
          color: KEM,
          opacity: vaoChu,
          translate: `0 ${(1 - vaoChu) * 22 * s}px`,
          textShadow: `0 ${4 * s}px ${18 * s}px rgba(0,0,0,0.85)`,
          whiteSpace: "nowrap",
        }}
      >
        {chu}
      </div>
      {phu ? (
        <div
          style={{
            position: "absolute",
            top: height * yDuong + (nam ? 140 : 34) * s,
            width: "100%",
            textAlign: "center",
            fontFamily: FONT,
            fontStyle: "italic",
            fontSize: 42 * s,
            letterSpacing: 2 * s,
            color: VANG,
            opacity: vaoPhu,
            textShadow: `0 ${2 * s}px ${10 * s}px #000`,
            whiteSpace: "nowrap",
          }}
        >
          {phu}
        </div>
      ) : null}
      {coTru ? (
        <div style={{ position: "absolute", top: height * 0.52, width: "100%", display: "flex", justifyContent: "center", gap: 130 * s }}>
          {tru.map((x, i) => {
            const v = interpolate(t, [x.tai, x.tai + 0.6], [0, 1], { ...kep, easing: ra });
            return (
              <div key={i} style={{ textAlign: "center", opacity: v, translate: `0 ${(1 - v) * 30 * s}px`, width: 360 * s }}>
                <div
                  style={{
                    width: 150 * s,
                    height: 150 * s,
                    margin: "0 auto",
                    borderRadius: "50%",
                    border: `2px solid rgba(216,178,106,${0.35 + 0.4 * v})`,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    // tren tu lieu: nen tron mau dac nua trong (gradient alpha mo dan dat len YUV de lo vong)
                    background: nenTrongSuot ? "rgba(10,8,6,0.55)" : "radial-gradient(circle, rgba(216,178,106,0.16), rgba(0,0,0,0) 70%)",
                    boxShadow: `0 0 ${24 * s * v}px rgba(216,178,106,0.35)`,
                  }}
                >
                  <BieuTuong loai={x.bieuTuong} c={84 * s} />
                </div>
                <div
                  style={{
                    marginTop: 26 * s,
                    fontFamily: FONT,
                    fontWeight: 700,
                    fontSize: 42 * s,
                    color: KEM,
                    letterSpacing: 1 * s,
                    textShadow: `0 ${2 * s}px ${10 * s}px #000`,
                    whiteSpace: "nowrap",
                  }}
                >
                  {x.nhan}
                </div>
              </div>
            );
          })}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
