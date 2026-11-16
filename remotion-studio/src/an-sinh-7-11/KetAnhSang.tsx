// 4 s ket — lam lai sat 8 s cuoi fb_reel_982349404914560 (nguoi dung: "4s cuoi chua giong video tham khao"), KHONG chep logo/QR cua dai:
// nen xanh la sang + mang luoi laser troi; 0-1,5 s tia sang ban xuong co dau sang choi + chum tia lua; 0,9-1,9 s vien neon xanh lo
// chay quanh khung + net neon chay duoi; 1,8 s chop sang, logo ATT NEWS hien + vet sang luot ngang; 2,1 s dong UBND; 2,5 s khau hieu
// vang chay tu trai sang (may khong co font viet tay du dau tieng Viet -> chu nghieng dam); 3,4-4 s mo ve den.
import React from "react";
import {AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig} from "remotion";

const NEON = "#9ffcff", VANG = "#ffe14d";
const ease = (t: number, a: number, b: number) =>
  interpolate(t, [a, b], [0, 1], {extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic)});

// diem mang luoi (co dinh theo chi so, troi nhe theo thoi gian)
const DIEM = Array.from({length: 34}).map((_, i) => ({x: (i * 577) % 1920, y: (i * 331 + 90) % 1080, p: i * 1.7}));

export const KetAnhSang: React.FC = () => {
  const t = useCurrentFrame() / useVideoConfig().fps;
  const khung = {x: 600, y: 250, w: 720, h: 260};
  const chuVi = 2 * (khung.w + khung.h);
  const chop = Math.max(0, 1 - Math.abs(t - 1.85) / 0.18);          // chop sang luc logo hien
  const diem = DIEM.map((d) => ({x: d.x + 25 * Math.sin(t * 0.8 + d.p), y: d.y + 18 * Math.cos(t * 0.7 + d.p)}));
  return (
    <AbsoluteFill style={{background: "radial-gradient(ellipse at 50% 35%, #5fe05a 0%, #23a83a 45%, #0b5d22 100%)", fontFamily: "'Segoe UI', Arial, sans-serif",
      opacity: 1 - ease(t, 3.4, 4.0)}}>
      {/* mang luoi laser */}
      <svg width={1920} height={1080} style={{position: "absolute", opacity: 0.35}}>
        {diem.map((a, i) => diem.slice(i + 1).map((b, j) => {
          const d = Math.hypot(a.x - b.x, a.y - b.y);
          return d < 420 ? <line key={`${i}-${j}`} x1={a.x} y1={a.y} x2={b.x} y2={b.y} stroke="#d9ffd0" strokeWidth={1.2} opacity={1 - d / 420} /> : null;
        }))}
        {diem.map((a, i) => <circle key={i} cx={a.x} cy={a.y} r={3} fill="#eaffe4" />)}
      </svg>
      {/* tia sang ban xuong cheo, dau sang choi */}
      {Array.from({length: 12}).map((_, i) => {
        const tre = 0.04 * i, k = ease(t, tre, tre + 0.7), mo = 1 - 0.85 * ease(t, 1.5, 2.3);
        const x0 = 260 + i * 140, dai = 560 * k;
        return (
          <div key={i} style={{position: "absolute", left: x0, top: -60, width: 10, height: dai, transformOrigin: "top center", transform: "rotate(34deg)", opacity: mo}}>
            <div style={{position: "absolute", inset: 0, borderRadius: 5, background: `linear-gradient(180deg, rgba(255,255,255,0), ${NEON} 60%, #ffffff)`,
              boxShadow: `0 0 18px ${NEON}`}} />
            <div style={{position: "absolute", left: -11, bottom: -16, width: 32, height: 32, borderRadius: "50%",
              background: "radial-gradient(circle, #ffffff 0%, rgba(255,250,200,0.9) 30%, rgba(255,230,120,0) 70%)"}} />
          </div>
        );
      })}
      {/* chum tia lua */}
      {Array.from({length: 46}).map((_, i) => {
        const t0 = 0.55 + (i % 9) * 0.05, k = Math.max(0, t - t0), g = ((i * 53) % 360) * Math.PI / 180, v = 140 + (i % 6) * 45;
        return <div key={i} style={{position: "absolute", left: 1320 + Math.cos(g) * v * k, top: 420 + Math.sin(g) * v * k + 160 * k * k, width: 5, height: 5,
          borderRadius: 3, background: "#ffd23f", boxShadow: "0 0 8px #ffb000", opacity: k > 0 ? Math.max(0, 1 - k / 1.0) : 0}} />;
      })}
      {/* vien neon chay quanh khung + net neon duoi */}
      <svg width={1920} height={1080} style={{position: "absolute", filter: `drop-shadow(0 0 10px ${NEON}) drop-shadow(0 0 26px ${NEON})`}}>
        <rect x={khung.x} y={khung.y} width={khung.w} height={khung.h} rx={30} fill="none" stroke="#ffffff" strokeWidth={5}
          strokeDasharray={chuVi} strokeDashoffset={chuVi * (1 - ease(t, 0.9, 1.8))} opacity={1 - ease(t, 1.9, 2.4)} />
        <path d={`M ${khung.x - 80} 600 Q 760 570 960 600 T ${khung.x + khung.w + 80} 600`} fill="none" stroke="#ffffff" strokeWidth={4}
          strokeDasharray={1000} strokeDashoffset={1000 * (1 - ease(t, 1.1, 1.9))} opacity={1 - ease(t, 2.0, 2.5)} />
      </svg>
      {/* chop sang */}
      <AbsoluteFill style={{background: "radial-gradient(circle at 50% 36%, rgba(255,255,255,0.95), rgba(255,255,255,0) 45%)", opacity: chop}} />
      {/* logo + vet sang luot ngang */}
      <div style={{position: "absolute", left: khung.x, top: khung.y, width: khung.w, height: khung.h, display: "flex", alignItems: "center", justifyContent: "center",
        overflow: "hidden", opacity: ease(t, 1.75, 2.0), transform: `scale(${0.9 + 0.1 * ease(t, 1.75, 2.4)})`}}>
        <Img src={staticFile("an-sinh-7-11/att_news.png")} style={{height: 170, filter: "drop-shadow(0 6px 16px rgba(0,0,0,0.35))"}} />
        <div style={{position: "absolute", top: 0, bottom: 0, left: `${-30 + 160 * ease(t, 2.0, 2.7)}%`, width: "18%", transform: "skewX(-20deg)",
          background: "linear-gradient(90deg, transparent, rgba(255,255,255,0.85), transparent)"}} />
      </div>
      {/* dong UBND voi vet sang */}
      <div style={{position: "absolute", left: 0, right: 0, top: 560, textAlign: "center", color: "#ffffff", fontSize: 44, fontWeight: 900, letterSpacing: 3,
        textShadow: "0 3px 0 #0b5d22, 0 0 18px rgba(255,255,255,0.6)", opacity: ease(t, 2.05, 2.45),
        clipPath: `inset(0 ${100 - 100 * ease(t, 2.05, 2.6)}% 0 0)`}}>ỦY BAN NHÂN DÂN XÃ AN THẠNH THỦY</div>
      {/* khau hieu vang chay tu trai sang */}
      <div style={{position: "absolute", left: 0, right: 0, top: 640, textAlign: "center", color: VANG, fontSize: 74, fontWeight: 800, fontStyle: "italic",
        textShadow: "0 4px 0 #6b5200, 0 0 22px rgba(255,225,77,0.65)", clipPath: `inset(0 ${100 - 100 * ease(t, 2.45, 3.2)}% 0 0)`}}>
        Tri ân · Sẻ chia · Lan tỏa yêu thương
      </div>
    </AbsoluteFill>
  );
};
