// Video vị trí nhà 9:16 từ một toạ độ (học ý tưởng từ Vị Trí Studio, 11/2026; giao diện riêng): ảnh vệ tinh tràn khung,
// ghim nhà + vòng bán kính → đường lớn phát sáng → bay tới từng tiện ích, vẽ đường đi thật kèm số km → thẻ giá → liên hệ.
// Props sinh bằng skills/ban-do-video/scripts/props_vi_tri.py; toạ độ theo pixel ảnh nền `nen`.
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FPS } from "../chung";

const diem = z.tuple([z.number(), z.number()]);
const duong = z.array(diem);
export const viTriNhaSchema = coBan.extend({
  font: z.string().default(""),
  nen: z.object({ file: z.string(), w: z.number(), h: z.number(), mPx: z.number() }),
  nha: z.object({ xy: diem }),
  tieuDe: z.object({ lon: z.string(), phu: z.string() }),
  banKinhPx: z.number(),
  duongLon: z.array(z.object({ ten: z.string(), net: z.array(duong), nhan: diem })).default([]),
  diem: z.array(z.object({ ten: z.string(), loai: z.string(), doan: z.string(), xy: diem, duong, tu: z.number(), ve: z.number(), den: z.number() })),
  the: z.object({ tu: z.number(), gia: z.string(), ten: z.string(), dong: z.array(z.string()) }).nullable().default(null),
  ket: z.object({ tu: z.number(), ten: z.string(), sdt: z.string() }).nullable().default(null),
  canh: z.array(z.object({ tu: z.number(), giay: z.number(), cx: z.number(), cy: z.number(), zoom: z.number() })),
  cau_doc: z.array(z.object({ chu: z.string(), batDau: z.number(), ketThuc: z.number() })).default([]),
  nguon: z.array(z.string()).default([]),
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const VANG = "#FFC53D", DO = "#E5383B", XANH = "#7DE2FF";
const dPath = (p: [number, number][]) => p.map((q, i) => `${i ? "L" : "M"} ${q[0]} ${q[1]}`).join(" ");
const doDai = (p: [number, number][]) => p.slice(1).reduce((s, q, i) => s + Math.hypot(q[0] - p[i][0], q[1] - p[i][1]), 0);

const mayQuay = (canh: z.infer<typeof viTriNhaSchema>["canh"], t: number) => {
  let i = 0;
  canh.forEach((c, j) => { if (t >= c.tu) i = j; });
  const a = canh[i];
  if (i === 0) return a;
  const b = canh[i - 1];
  const p = interpolate(t, [a.tu, a.tu + a.giay], [0, 1], { ...kep, easing: Easing.inOut(Easing.quad) }); // props_vi_tri.py tính giay theo đỉnh của easing này
  return { ...a, cx: b.cx + (a.cx - b.cx) * p, cy: b.cy + (a.cy - b.cy) * p, zoom: Math.exp(Math.log(b.zoom) + (Math.log(a.zoom) - Math.log(b.zoom)) * p) };
};

const Vien: React.FC<{ children: React.ReactNode; style?: React.CSSProperties }> = ({ children, style }) => (
  <div style={{ background: "rgba(7,12,18,0.82)", borderRadius: 18, padding: "12px 26px", textAlign: "center", ...style }}>{children}</div>
);

export const ViTriNha: React.FC<z.infer<typeof viTriNhaSchema>> = (p) => {
  const frame = useCurrentFrame();
  const { width: W, height: H, durationInFrames } = useVideoConfig();
  const t = frame / FPS, het = durationInFrames / FPS, s = W / 1080;
  const cam = mayQuay(p.canh, t);
  const k = 1 / cam.zoom; // nét dày cố định trên màn hình
  const man = (q: [number, number]) => [(q[0] - cam.cx) * cam.zoom + W / 2, (q[1] - cam.cy) * cam.zoom + H / 2];
  const dauTien = p.diem.length ? p.diem[0].tu : het;

  const veVong = interpolate(t, [0.3, 1.8], [0, 1], { ...kep, easing: Easing.inOut(Easing.cubic) });
  const veDuong = interpolate(t, [2.4, 3.8], [0, 1], { ...kep, easing: Easing.inOut(Easing.cubic) });
  const anNhanDuong = interpolate(t, [2.8, 3.3, dauTien - 0.2, dauTien + 0.3], [0, 1, 1, 0], kep);
  const anVong = interpolate(t, [dauTien, dauTien + 0.6], [1, 0.25], kep);
  const dangO = p.diem.find((d) => t >= d.tu && t < d.den);
  const hienThe = p.the ? interpolate(t, [p.the.tu, p.the.tu + 0.5], [0, 1], { ...kep, easing: Easing.out(Easing.cubic) }) : 0;
  const hienKet = p.ket ? interpolate(t, [p.ket.tu, p.ket.tu + 0.5], [0, 1], { ...kep, easing: Easing.out(Easing.cubic) }) : 0;
  const tat = interpolate(t, [het - 0.5, het], [1, 0], kep);
  const cau = p.cau_doc.find((c) => t >= c.batDau && t < c.ketThuc);
  const [nx, ny] = man(p.nha.xy);
  const nay = 1 + 0.06 * Math.sin(t * 4);

  return (
    <AbsoluteFill style={{ background: "#05080A", opacity: tat, fontFamily: p.font || "Arial, 'Segoe UI', sans-serif" }}>
      <div style={{ position: "absolute", left: 0, top: 0, transformOrigin: "0 0",
        transform: `translate(${W / 2}px, ${H / 2}px) scale(${cam.zoom}) translate(${-cam.cx}px, ${-cam.cy}px)` }}>
        <Img src={staticFile(p.nen.file)} style={{ position: "absolute", width: p.nen.w, height: p.nen.h, filter: "brightness(0.68) saturate(0.9)" }} />
        <svg width={p.nen.w} height={p.nen.h} style={{ position: "absolute", overflow: "visible" }}>
          <circle cx={p.nha.xy[0]} cy={p.nha.xy[1]} r={p.banKinhPx} fill="rgba(255,255,255,0.05)" stroke="#FFFFFF" strokeOpacity={0.9 * anVong}
            strokeWidth={3 * k * s} pathLength={1} strokeDasharray={`${0.008 * veVong} ${0.008}`} fillOpacity={veVong} />
          {p.duongLon.map((d, i) => d.net.map((n, j) => {
            const l = doDai(n);
            return <path key={`${i}-${j}`} d={dPath(n)} fill="none" stroke={VANG} strokeWidth={5 * k * s} strokeLinecap="round" opacity={0.85 * anVong}
              strokeDasharray={l} strokeDashoffset={l * (1 - veDuong)} style={{ filter: `drop-shadow(0 0 ${4 * k * s}px ${VANG})` }} />;
          }))}
        </svg>
      </div>

      {/* ghim nhà nằm dưới tuyến: tiện ích sát nhà (vài trăm mét) không bị ghim che mất đường đi */}
      <svg width={84 * s * nay} height={108 * s * nay} viewBox="0 0 84 108" style={{ position: "absolute", left: nx, top: ny, translate: "-50% -100%", filter: "drop-shadow(0 4px 8px rgba(0,0,0,0.7))" }}>
        <path d="M42 106 C30 82 4 62 4 40 A38 38 0 0 1 80 40 C80 62 54 82 42 106 Z" fill={DO} stroke="#fff" strokeWidth="5" />
        <path d="M42 20 L64 40 H57 V60 H47 V47 H37 V60 H27 V40 H20 Z" fill="#fff" />
      </svg>

      <div style={{ position: "absolute", left: 0, top: 0, transformOrigin: "0 0",
        transform: `translate(${W / 2}px, ${H / 2}px) scale(${cam.zoom}) translate(${-cam.cx}px, ${-cam.cy}px)` }}>
        <svg width={p.nen.w} height={p.nen.h} style={{ position: "absolute", overflow: "visible" }}>
          {p.diem.map((d, i) => {
            if (t < d.tu) return null;
            const l = doDai(d.duong), ve = interpolate(t, [d.ve, d.ve + 1.6], [0, 1], { ...kep, easing: Easing.inOut(Easing.quad) });
            const dang = dangO === d;
            return (
              <g key={i} opacity={dang ? 1 : 0.4}>
                <path d={dPath(d.duong)} fill="none" stroke="#000" strokeOpacity={0.55} strokeWidth={10 * k * s} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={l} strokeDashoffset={l * (1 - ve)} />
                <path d={dPath(d.duong)} fill="none" stroke={XANH} strokeWidth={6 * k * s} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={l} strokeDashoffset={l * (1 - ve)}
                  style={{ filter: `drop-shadow(0 0 ${5 * k * s}px ${XANH})` }} />
                {ve >= 1 ? <circle cx={d.xy[0]} cy={d.xy[1]} r={13 * k * s} fill={XANH} stroke="#fff" strokeWidth={4 * k * s} /> : null}
              </g>
            );
          })}
        </svg>
      </div>

      {/* nhãn đường lớn ở cảnh toàn: props_vi_tri.py đã đặt sao cho không đụng nhau */}
      {anNhanDuong > 0 ? p.duongLon.map((d, i) => {
        const [x, y] = man(d.nhan);
        return <div key={i} style={{ position: "absolute", left: x, top: y, translate: "-50% -50%", opacity: anNhanDuong, whiteSpace: "nowrap", fontSize: 30 * s, fontWeight: 800,
          color: "#111", background: VANG, borderRadius: 10 * s, padding: `${6 * s}px ${14 * s}px` }}>{d.ten}</div>;
      }) : null}

      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0.6) 0%, transparent 24%, transparent 66%, rgba(0,0,0,0.75) 100%)" }} />

      {/* tiêu đề mở, rồi tên tiện ích đang tới */}
      <div style={{ position: "absolute", left: 60 * s, right: 60 * s, top: 170 * s, display: "flex", flexDirection: "column", alignItems: "center", gap: 14 * s }}>
        {t < dauTien ? (
          <>
            <Vien style={{ fontSize: 66 * s, fontWeight: 900, color: "#fff" }}>{p.tieuDe.lon}</Vien>
            <Vien style={{ fontSize: 34 * s, fontWeight: 800, color: "#111", background: VANG, padding: `${8 * s}px ${22 * s}px` }}>{p.tieuDe.phu}</Vien>
          </>
        ) : dangO ? (
          <>
            <Vien style={{ fontSize: 50 * s, fontWeight: 900, color: "#fff", lineHeight: 1.2 }}>{dangO.ten}</Vien>
            <Vien style={{ fontSize: 38 * s, fontWeight: 800, color: "#111", background: VANG, padding: `${8 * s}px ${22 * s}px` }}>{dangO.doan}</Vien>
          </>
        ) : null}
      </div>

      {/* phụ đề */}
      {cau && !hienThe ? (
        <div style={{ position: "absolute", left: 70 * s, right: 70 * s, bottom: 340 * s, textAlign: "center", fontSize: 44 * s, fontWeight: 800, color: "#fff", lineHeight: 1.3, textShadow: `0 ${3 * s}px ${10 * s}px #000` }}>{cau.chu}</div>
      ) : null}

      {/* thẻ giá */}
      {p.the && hienThe > 0 && !hienKet ? (
        <div style={{ position: "absolute", left: 60 * s, right: 60 * s, top: 250 * s, opacity: hienThe, translate: `0 ${(1 - hienThe) * 40 * s}px`, background: "rgba(7,12,18,0.92)",
          border: `3px solid ${VANG}`, borderRadius: 28 * s, padding: `${40 * s}px ${44 * s}px`, color: "#fff" }}>
          <div style={{ fontSize: 30 * s, letterSpacing: 4 * s, color: "#BFC8D0", fontWeight: 700 }}>GIÁ BÁN</div>
          <div style={{ fontSize: 118 * s, fontWeight: 900, color: VANG, lineHeight: 1.15 }}>{p.the.gia}</div>
          <div style={{ fontSize: 46 * s, fontWeight: 800, lineHeight: 1.25 }}>{p.the.ten}</div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 14 * s, marginTop: 22 * s }}>
            {p.the.dong.map((d, i) => <div key={i} style={{ fontSize: 32 * s, fontWeight: 700, border: "2px solid rgba(255,255,255,0.4)", borderRadius: 12 * s, padding: `${6 * s}px ${16 * s}px` }}>{d}</div>)}
          </div>
        </div>
      ) : null}

      {/* thẻ liên hệ */}
      {p.ket && hienKet > 0 ? (
        <AbsoluteFill style={{ background: `rgba(5,8,10,${0.86 * hienKet})`, alignItems: "center", justifyContent: "center", opacity: hienKet }}>
          <div style={{ fontSize: 48 * s, fontWeight: 800, color: "#fff" }}>{p.ket.ten}</div>
          <div style={{ marginTop: 26 * s, fontSize: 92 * s, fontWeight: 900, color: "#111", background: VANG, borderRadius: 24 * s, padding: `${14 * s}px ${44 * s}px` }}>{p.ket.sdt}</div>
        </AbsoluteFill>
      ) : null}

      {/* nguồn dữ liệu */}
      <div style={{ position: "absolute", left: 40 * s, right: 40 * s, bottom: 220 * s, textAlign: "center", fontSize: 20 * s, color: "rgba(235,240,240,0.8)", lineHeight: 1.4, textShadow: "0 0 4px #000" }}>
        {p.nguon.map((n, i) => <div key={i}>{n}</div>)}
      </div>
    </AbsoluteFill>
  );
};
