// Bản đồ xã, kiểu clip TikTok "ranh giới xã": (1) ảnh bản đồ định vị + ghim + nhãn tỉnh,
// (2) chuyển sang bản đồ ranh giới — viền vàng chạy quanh, tô tím, chữ vàng gõ dần tên từng xã cũ.
// Cảnh 2 vẽ hoàn toàn bằng vector (nền vân đất, kênh, ranh giới) nên không mờ khi phóng to.
// Ảnh định vị đọc qua staticFile (render với --public-dir). Toạ độ ranh giới/nhãn/kênh theo hệ pixel của bản đồ gốc đã dò.
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FONT, FPS } from "../chung";

const diem = z.array(z.tuple([z.number(), z.number()]));

export const banDoXaSchema = coBan.extend({
  anhDinhVi: z.string().default(""),
  nhanDinhVi: z.array(z.string()).default([]),
  ghim: z.tuple([z.number(), z.number()]).default([0.5, 0.5]), // phần trăm khung, cảnh định vị
  chuyenCanh: z.number().default(2.5), // giây bắt đầu chuyển sang bản đồ ranh giới
  khung: z.tuple([z.number(), z.number(), z.number(), z.number()]), // viewBox x, y, w, h (16:9)
  ranhGioi: diem,
  duongChia: z.array(diem).default([]),
  kenh: z.object({ duong: diem, ten: z.string(), x: z.number(), y: z.number(), goc: z.number() }).optional(),
  veVien: z.tuple([z.number(), z.number()]).default([2.6, 3.4]),
  nhan: z.array(z.object({ chu: z.string(), x: z.number(), y: z.number(), tai: z.number() })).default([]),
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const muot = Easing.bezier(0.16, 1, 0.3, 1);
const VANG = "#FFE81A";
const TIM = "rgba(150, 30, 150, 0.62)";
const CHU = { fontFamily: FONT, fontWeight: 900, letterSpacing: 1, textTransform: "uppercase" } as const;

const duong = (ds: [number, number][], kin: boolean) =>
  ds.map(([x, y], i) => `${i ? "L" : "M"}${x} ${y}`).join(" ") + (kin ? " Z" : "");

export const BanDoXa: React.FC<z.infer<typeof banDoXaSchema>> = (p) => {
  const frame = useCurrentFrame();
  const { width, durationInFrames } = useVideoConfig();
  const s = width / 1920;
  const t = frame / FPS;
  const [kx, ky, kw, kh] = p.khung;

  // cảnh 1 — định vị
  const zoom1 = interpolate(t, [0, p.chuyenCanh + 0.5], [1, 1.12], kep);
  const ghimVao = spring({ frame, fps: FPS, delay: 0.15 * FPS, config: { damping: 11 } });
  const nhanVao = spring({ frame, fps: FPS, delay: 0.35 * FPS, config: { damping: 13 } });
  const songGhim = (t * 1.4) % 1;

  // cảnh 2 — ranh giới
  const lo2 = interpolate(t, [p.chuyenCanh, p.chuyenCanh + 0.45], [0, 1], { ...kep, easing: muot });
  const zoom2 = interpolate(frame, [p.chuyenCanh * FPS, durationInFrames], [1.06, 1], { ...kep, easing: muot });
  const vien = interpolate(t, p.veVien, [1, 0], { ...kep, easing: Easing.inOut(Easing.cubic) });
  const to = interpolate(t, [p.veVien[0] + 0.4, p.veVien[1] + 0.3], [0, 1], kep);
  const chia = interpolate(t, [p.veVien[1], p.veVien[1] + 0.5], [0, 1], kep);
  const coChu = 19 * (kw / 753); // cỡ chữ theo đơn vị ảnh, giữ cùng cỡ khi đổi khung

  return (
    <AbsoluteFill style={{ backgroundColor: "#0d1a10" }}>
      {p.anhDinhVi ? (
        <AbsoluteFill style={{ opacity: 1 - lo2 }}>
          <AbsoluteFill style={{ scale: zoom1, transformOrigin: `${p.ghim[0] * 100}% ${p.ghim[1] * 100}%` }}>
            <Img src={staticFile(p.anhDinhVi)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
            <div
              style={{
                position: "absolute",
                left: `${p.ghim[0] * 100}%`,
                top: `${p.ghim[1] * 100}%`,
                width: 0,
                height: 0,
              }}
            >
              <div
                style={{
                  position: "absolute",
                  left: -60 * s * (0.4 + songGhim),
                  top: -60 * s * (0.4 + songGhim),
                  width: 120 * s * (0.4 + songGhim),
                  height: 120 * s * (0.4 + songGhim),
                  borderRadius: "50%",
                  border: `${5 * s}px solid ${VANG}`,
                  opacity: (1 - songGhim) * ghimVao,
                }}
              />
              <svg
                width={64 * s}
                height={84 * s}
                viewBox="0 0 64 84"
                style={{ position: "absolute", left: -32 * s, top: -84 * s, scale: ghimVao, transformOrigin: "50% 100%" }}
              >
                <path d="M32 2C16 2 4 14 4 30c0 21 28 52 28 52s28-31 28-52C60 14 48 2 32 2z" fill={VANG} stroke="#000" strokeWidth="4" />
                <circle cx="32" cy="30" r="10" fill="#000" />
              </svg>
            </div>
          </AbsoluteFill>
          <div
            style={{
              ...CHU,
              position: "absolute",
              left: `${p.ghim[0] * 100}%`,
              top: `${p.ghim[1] * 100}%`,
              translate: `-50% ${-290 * s}px`,
              textAlign: "center",
              fontSize: 76 * s,
              lineHeight: 1.12,
              color: "#111",
              WebkitTextStroke: `${10 * s}px #fff`,
              paintOrder: "stroke fill",
              whiteSpace: "nowrap",
              scale: nhanVao,
            }}
          >
            {p.nhanDinhVi.map((d) => (
              <div key={d}>{d}</div>
            ))}
          </div>
        </AbsoluteFill>
      ) : null}

      <AbsoluteFill style={{ opacity: p.anhDinhVi ? lo2 : 1, scale: zoom2 }}>
        <svg width="100%" height="100%" viewBox={`${kx} ${ky} ${kw} ${kh}`} preserveAspectRatio="xMidYMid slice">
          <defs>
            <filter id="van-dat" x="0" y="0" width="100%" height="100%">
              <feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="4" seed="7" />
              <feColorMatrix
                type="matrix"
                values="0 0 0 0 0.16  0 0 0 0 0.22  0 0 0 0 0.12  0.9 0.6 0 0 -0.35"
              />
            </filter>
            <filter id="van-nho" x="0" y="0" width="100%" height="100%">
              <feTurbulence type="fractalNoise" baseFrequency="0.6" numOctaves="2" seed="3" />
              <feColorMatrix type="matrix" values="0 0 0 0 0.9  0 0 0 0 0.9  0 0 0 0 0.8  0 0 0 0.12 0" />
            </filter>
            <radialGradient id="nen" cx="50%" cy="45%" r="75%">
              <stop offset="0%" stopColor="#3b4a2c" />
              <stop offset="100%" stopColor="#1c2616" />
            </radialGradient>
            <clipPath id="trong-xa">
              <path d={duong(p.ranhGioi, true)} />
            </clipPath>
          </defs>
          <rect x={kx - kw} y={ky - kh} width={kw * 3} height={kh * 3} fill="url(#nen)" />
          <rect x={kx - kw} y={ky - kh} width={kw * 3} height={kh * 3} filter="url(#van-dat)" />
          <rect x={kx - kw} y={ky - kh} width={kw * 3} height={kh * 3} filter="url(#van-nho)" />
          {p.kenh ? (
            <g>
              <path d={duong(p.kenh.duong, false)} fill="none" stroke="#5b4630" strokeWidth={13} strokeLinecap="round" />
              <path d={duong(p.kenh.duong, false)} fill="none" stroke="#8a6d4b" strokeWidth={9} strokeLinecap="round" />
              <text
                x={p.kenh.x}
                y={p.kenh.y}
                transform={`rotate(${p.kenh.goc} ${p.kenh.x} ${p.kenh.y})`}
                textAnchor="middle"
                style={{ fontFamily: FONT, fontWeight: 700, fontStyle: "italic", fontSize: coChu * 0.55, fill: "#e8f4ff", opacity: to }}
              >
                {p.kenh.ten}
              </text>
            </g>
          ) : null}
          <g clipPath="url(#trong-xa)" opacity={to}>
            <rect x={kx - kw} y={ky - kh} width={kw * 3} height={kh * 3} fill={TIM} />
          </g>
          {p.duongChia.map((d, i) => (
            <path
              key={i}
              d={duong(d, false)}
              fill="none"
              stroke={VANG}
              strokeWidth={1.6}
              strokeDasharray="5 4"
              opacity={chia * 0.85}
            />
          ))}
          <path
            d={duong(p.ranhGioi, true)}
            pathLength={1}
            fill="none"
            stroke={VANG}
            strokeWidth={3.2}
            strokeLinejoin="round"
            strokeDasharray="1 1"
            strokeDashoffset={vien}
            style={{ filter: "drop-shadow(0 0 2px rgba(0,0,0,0.9))" }}
          />
          {p.nhan.map((n) => {
            const ky_tu = Array.from(n.chu);
            const da = Math.floor(interpolate(t, [n.tai, n.tai + ky_tu.length * 0.045], [0, ky_tu.length], kep));
            if (da === 0) return null;
            const dangGo = da < ky_tu.length || Math.floor(t * 3) % 2 === 0;
            return (
              <text
                key={n.chu}
                x={n.x}
                y={n.y}
                textAnchor="middle"
                style={{ ...CHU, fontSize: coChu, fill: VANG, stroke: "#1a001a", strokeWidth: coChu * 0.14, paintOrder: "stroke fill" }}
              >
                {ky_tu.slice(0, da).join("")}
                {dangGo && t < n.tai + ky_tu.length * 0.045 + 0.6 ? "_" : ""}
              </text>
            );
          })}
        </svg>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
