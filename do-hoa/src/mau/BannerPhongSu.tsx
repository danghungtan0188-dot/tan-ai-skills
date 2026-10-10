// Banner tên kiểu phóng sự truyền hình (đo từ phóng sự VHTV, khung 1920x1080):
// huy hiệu "PHÓNG SỰ" hình bình hành + thanh 2 tầng (tên trên nền xanh đậm, địa danh trên nền xanh nhạt),
// mép nghiêng ~14°, nằm ở 77–87,5% chiều cao. Vào: trượt từ phải 0,35 s, chữ quét từ trái, vòng huy hiệu bung + xoay.
// Thông số đầy đủ: skills/bien-tap-video-thong-minh-song-ngu-tan/references/banner-phong-su.md
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FONT, FPS } from "../chung";

export const bannerPhongSuSchema = coBan.extend({
  ten: z.string(),
  diaChi: z.string().default(""),
  nhan: z.string().default("PHÓNG SỰ"),
  mauDam: z.string().default("#169A4D"),
  mauHuyHieu: z.string().default("#0BA44D"),
  mauNhat: z.string().default("#CBDBBE"),
  dichLen: z.number().default(0), // px (khung 1080p) day banner len khi phu de 2 dong nam ngay duoi
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const ra = Easing.out(Easing.cubic);
const NGHIENG = "skewX(-14deg)";

export const BannerPhongSu: React.FC<z.infer<typeof bannerPhongSuSchema>> = (p) => {
  const frame = useCurrentFrame();
  const { width, durationInFrames } = useVideoConfig();
  const s = width / 1920;
  const t = frame / FPS;
  const het = durationInFrames / FPS;

  const truotHuy = interpolate(t, [0, 0.3], [1500, 0], { ...kep, easing: ra });
  const truotThanh = interpolate(t, [0.05, 0.38], [1500, 0], { ...kep, easing: ra });
  const chu = interpolate(t, [0.3, 0.6], [0, 100], { ...kep, easing: ra });
  const vong = interpolate(t, [0.3, 0.6], [0, 1], { ...kep, easing: Easing.out(Easing.back(1.6)) });
  const xoay = t * 140;
  const chuNhan = interpolate(t, [0.45, 0.65], [0, 1], kep);
  const chuKy = (t - 0.8) % 2.5;
  const loe = t > 0.8 ? interpolate(chuKy, [0, 0.5], [-40, 140], kep) : -40;
  const roi = interpolate(t, [het - 0.4, het], [0, 1], { ...kep, easing: Easing.in(Easing.cubic) });

  const vien = `${3 * s}px solid rgba(255,255,255,0.95)`;
  const bong = `0 ${4 * s}px ${12 * s}px rgba(0,0,0,0.35)`;

  return (
    <AbsoluteFill style={{ opacity: 1 - roi, translate: `${-roi * 120 * s}px 0` }}>
      {/* huy hiệu */}
      <div
        style={{
          position: "absolute",
          left: 200 * s,
          top: (830 - p.dichLen) * s,
          width: 205 * s,
          height: 115 * s,
          translate: `${truotHuy * s}px 0`,
          transform: NGHIENG,
          background: p.mauHuyHieu,
          border: vien,
          borderRadius: 12 * s,
          boxShadow: bong,
          overflow: "hidden",
        }}
      >
        <div
          style={{
            position: "absolute",
            left: "50%",
            top: "50%",
            width: 92 * s,
            height: 92 * s,
            marginLeft: -46 * s,
            marginTop: -46 * s,
            borderRadius: "50%",
            border: `${2.5 * s}px solid rgba(255,255,255,0.85)`,
            borderTopColor: "transparent",
            scale: vong,
            rotate: `${xoay}deg`,
          }}
        />
        <div
          style={{
            position: "absolute",
            inset: 0,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            transform: "skewX(14deg)",
            fontFamily: FONT,
            fontWeight: 900,
            fontSize: 34 * s,
            color: "white",
            opacity: chuNhan,
            textShadow: `0 ${2 * s}px ${4 * s}px rgba(0,0,0,0.35)`,
            whiteSpace: "nowrap",
          }}
        >
          {p.nhan}
        </div>
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: `linear-gradient(100deg, transparent ${loe - 15}%, rgba(255,255,255,0.75) ${loe}%, transparent ${loe + 15}%)`,
          }}
        />
      </div>

      {/* thanh 2 tầng */}
      <div
        style={{
          position: "absolute",
          left: 415 * s,
          top: (832 - p.dichLen) * s,
          width: 1315 * s,
          height: 111 * s,
          translate: `${truotThanh * s}px 0`,
          transform: NGHIENG,
          border: vien,
          borderRadius: 10 * s,
          boxShadow: bong,
          overflow: "hidden",
          background: p.mauNhat,
        }}
      >
        <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: "48%", background: p.mauDam }} />
        <div
          style={{
            position: "absolute",
            left: 0,
            top: "52%",
            width: 70 * s,
            bottom: 0,
            background: p.mauDam,
          }}
        />
        <div
          style={{
            position: "absolute",
            left: 120 * s,
            right: 30 * s,
            top: 0,
            bottom: 0,
            transform: "skewX(14deg)",
            fontFamily: FONT,
            fontWeight: 700,
            clipPath: `inset(0 ${100 - chu}% 0 0)`,
          }}
        >
          <div style={{ height: "48%", display: "flex", alignItems: "center", fontSize: 44 * s, fontWeight: 800, color: "white" }}>{p.ten}</div>
          <div style={{ height: "52%", display: "flex", alignItems: "center", fontSize: 40 * s, fontWeight: 800, color: p.mauDam }}>
            {p.diaChi}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
