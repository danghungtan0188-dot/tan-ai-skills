// Bản đồ vệ tinh giải thích theo lời đọc (học từ reel "Góc nhìn quy hoạch — Sông Đáy"): thẻ bản đồ bo góc viền
// xanh ngọc trên nền lưới tối; trong thẻ cố định tiêu đề, mũi tên Bắc, bản đồ nhỏ định vị, thước tỷ lệ, phụ đề,
// dòng nguồn và thanh tiến độ. Máy quay trượt/phóng giữa các cảnh (`canh`); các lớp (kênh phát sáng, ranh giới,
// đường, cầu, ô số liệu) hiện đúng mốc lời đọc trong `moc`. Toạ độ tất cả theo pixel của ảnh nền `nen`; ảnh cận
// `can` (độ phân giải cao hơn) đặt chồng đúng chỗ để phóng sát vẫn nét.
import React from "react";
import {
  AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig, continueRender, delayRender,
} from "remotion";
import { z } from "zod";
import { coBan, FPS } from "../chung";

const diem = z.tuple([z.number(), z.number()]);
const duong = z.array(diem);
export const banDoVeTinhSchema = coBan.extend({
  font: z.string().default(""),
  nen: z.object({ file: z.string(), w: z.number(), h: z.number(), mPx: z.number() }), // mPx: mét / pixel ảnh nền
  can: z.object({ file: z.string(), x: z.number(), y: z.number(), w: z.number(), h: z.number() }).nullable().default(null),
  tieuDe: z.object({ nho: z.string(), lon: z.string(), phu: z.string() }),
  nguon: z.array(z.string()).default([]),
  xa: z.object({ ten: z.string(), vong: duong, nhan: diem }),
  kenh: z.object({ ten: z.string(), duong, nhan: diem }),
  langGieng: z.array(z.object({ ten: z.string(), xy: diem })).default([]),
  tuyen: z.array(z.object({ ten: z.string(), mau: z.string(), net: z.array(duong), nhan: diem })).default([]),
  cau: z.object({ ten: z.string(), phu: z.string(), xy: diem }).nullable().default(null),
  so: z.object({ gia: z.string(), donVi: z.string(), dong: z.string() }).nullable().default(null),
  canh: z.array(z.object({ tu: z.number(), cx: z.number(), cy: z.number(), zoom: z.number() })), // máy quay tới cảnh này từ giây `tu`
  moc: z.object({ kenh: z.number(), xa: z.number(), so: z.number(), tuyen: z.number(), cau: z.number(), het: z.number() }),
  cau_doc: z.array(z.object({ chu: z.string(), batDau: z.number(), ketThuc: z.number(), nhan: z.array(z.string()).default([]),
    tu: z.array(z.number()).default([]) })), // tu: mốc từng chữ thật (moc_tung_chu.py); trống thì chia đều
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const muot = Easing.bezier(0.45, 0, 0.2, 1);
const NGOC = "#3FF0D0", VANG = "#FFCD2D", VIEN = "#2BD9A6";

const useFont = (file: string) => {
  const [xong] = React.useState(() => (file ? delayRender("font") : null));
  React.useEffect(() => {
    if (!file || xong === null) return;
    const f = new FontFace("BDVT", `url(${staticFile(file)})`, { weight: "100 900" });
    f.load().then((ff) => { document.fonts.add(ff); continueRender(xong); }).catch(() => continueRender(xong));
  }, [file, xong]);
  return file ? "BDVT, Arial, sans-serif" : "Arial, 'Segoe UI', sans-serif";
};

const dPath = (p: [number, number][]) => p.map((q, i) => `${i ? "L" : "M"} ${q[0]} ${q[1]}`).join(" ");
const doDai = (p: [number, number][]) => p.slice(1).reduce((s, q, i) => s + Math.hypot(q[0] - p[i][0], q[1] - p[i][1]), 0);

// máy quay: nội suy cảnh trước → cảnh sau trong 1,4 giây kể từ `tu`
const mayQuay = (canh: { tu: number; cx: number; cy: number; zoom: number }[], t: number) => {
  let a = canh[0];
  for (const c of canh) if (t >= c.tu) a = c;
  const i = canh.indexOf(a);
  if (i === 0) return a;
  const truoc = canh[i - 1];
  const p = interpolate(t, [a.tu, a.tu + 1.4], [0, 1], { ...kep, easing: muot });
  const lz = Math.log(truoc.zoom) + (Math.log(a.zoom) - Math.log(truoc.zoom)) * p; // phóng theo log cho đều mắt
  return { tu: a.tu, cx: truoc.cx + (a.cx - truoc.cx) * p, cy: truoc.cy + (a.cy - truoc.cy) * p, zoom: Math.exp(lz) };
};

export const BanDoVeTinh: React.FC<z.infer<typeof banDoVeTinhSchema>> = (p) => {
  const frame = useCurrentFrame();
  const { width: W, height: H, durationInFrames } = useVideoConfig();
  const t = frame / FPS;
  const het = durationInFrames / FPS;
  const s = W / 1080;
  const ff = useFont(p.font);

  // thẻ bản đồ
  const le = 34 * s, the = { x: le, y: 70 * s, w: W - 2 * le, h: H - 140 * s };
  const cam = mayQuay(p.canh, t);
  const tamX = the.x + the.w / 2, tamY = the.y + the.h * 0.48;
  const man = (q: [number, number]) => [(q[0] - cam.cx) * cam.zoom + tamX, (q[1] - cam.cy) * cam.zoom + tamY];
  const k = 1 / cam.zoom; // nét có độ dày cố định trên màn hình

  const veKenh = interpolate(t, [p.moc.kenh, p.moc.kenh + 2.2], [0, 1], { ...kep, easing: Easing.inOut(Easing.cubic) });
  const veXa = interpolate(t, [p.moc.xa, p.moc.xa + 2.0], [0, 1], { ...kep, easing: Easing.inOut(Easing.quad) });
  const hienSo = interpolate(t, [p.moc.so, p.moc.so + 0.5], [0, 1], { ...kep, easing: muot });
  const tatSo = interpolate(t, [p.moc.tuyen - 0.4, p.moc.tuyen], [1, 0], kep);
  const veTuyen = interpolate(t, [p.moc.tuyen, p.moc.tuyen + 1.8], [0, 1], { ...kep, easing: Easing.inOut(Easing.cubic) });
  const hienCau = interpolate(t, [p.moc.cau + 0.8, p.moc.cau + 1.3], [0, 1], { ...kep, easing: muot });
  // tối nền khi có ô số; tuyến đến sớm hơn so+1 giây (hoặc moc.so = moc.tuyen) thì mốc không còn tăng dần → Remotion báo lỗi
  const hetToi = Math.max(p.moc.tuyen, p.moc.so + 1.01);
  const toi = interpolate(t, [p.moc.so, p.moc.so + 0.6, hetToi - 0.4, hetToi], [0, 0.25, 0.25, 0], kep);
  const tat = interpolate(t, [het - 0.8, het], [1, 0], kep);
  const lK = doDai(p.kenh.duong), lX = doDai(p.xa.vong);
  const nhat = interpolate(cam.zoom, [0.8, 1.8], [1, 0.15], kep); // phóng sát: để lộ lòng kênh thật trên ảnh

  // thước tỷ lệ: chọn 500 m / 1 km / 2 km cho vừa ~180 px
  const mMan = p.nen.mPx / cam.zoom;
  const thuoc = [500, 1000, 2000, 5000].find((m) => m / mMan >= 120 * s) ?? 5000;

  // phụ đề: câu đang đọc, chữ hiện dần, từ khoá vàng
  const cau = p.cau_doc.find((c) => t >= c.batDau - 0.2 && t < c.ketThuc + 0.3);

  // Nhãn: đặt theo thứ tự ưu tiên; khung chữ đụng nhãn đã đặt hoặc ô che thì đẩy lên từng dòng, có đường kẻ nối về
  // điểm (học từ GeoReel). Gần mép thẻ thì canh vào trong để không bị mép cắt.
  const daDat: { l: number; r: number; t: number; b: number }[] = [];
  const che: { l: number; r: number; t: number; b: number }[] = [];
  const nhan = (q: [number, number], chu: string, mau: string, co: number, an: number, key: string, phu?: string) => {
    if (an <= 0) return null;
    const [x, y0] = man(q);
    const canLe = x > the.x + the.w * 0.72 ? "right" : x < the.x + the.w * 0.28 ? "left" : "center";
    const rong = chu.length * co * 0.66 * s + 8 * s, cao = co * (phu ? 1.95 : 1.3) * s;
    const l = canLe === "right" ? x - rong : canLe === "left" ? x : x - rong / 2;
    // vùng được đặt nhãn: trong thẻ, dưới tiêu đề + bản đồ nhỏ, trên thước tỷ lệ + phụ đề
    const vung = { l: the.x + 24 * s, r: the.x + the.w - 24 * s, t: the.y + 250 * s, b: the.y + the.h - 470 * s };
    let day = -1;
    for (let k2 = 0; k2 <= 6; k2++) {
      const r = { l, r: l + rong, t: y0 - cao / 2 - k2 * cao, b: y0 + cao / 2 - k2 * cao };
      const trongVung = r.l >= vung.l && r.r <= vung.r && r.t >= vung.t && r.b <= vung.b;
      if (trongVung && ![...daDat, ...che].some((o) => o.l < r.r && r.l < o.r && o.t < r.b && r.t < o.b)) { day = k2 * cao; break; }
    }
    if (day < 0) return null; // không còn chỗ: ẩn nhãn, không để mép cắt hay đè
    daDat.push({ l, r: l + rong, t: y0 - cao / 2 - day, b: y0 + cao / 2 - day });
    const y = y0 - day;
    return (
      <React.Fragment key={key}>
      {day > 0 ? <div style={{ position: "absolute", left: x - 1, top: y + cao / 2, width: 2, height: day - cao / 2, background: mau, opacity: an * 0.8 }} /> : null}
      <div style={{
        position: "absolute", left: x, top: y, translate: canLe === "right" ? "-100% -50%" : canLe === "left" ? "0 -50%" : "-50% -50%",
        opacity: an, textAlign: canLe as "left", whiteSpace: "nowrap", pointerEvents: "none",
      }}>
        <div style={{ fontSize: co * s, fontWeight: 800, color: mau, letterSpacing: 2 * s, textShadow: `0 0 ${8 * s}px rgba(0,0,0,0.95), 0 ${2 * s}px ${4 * s}px #000` }}>{chu}</div>
        {phu ? <div style={{ fontSize: co * 0.62 * s, fontWeight: 700, color: "#DDE7E4", letterSpacing: 1.5 * s, textShadow: "0 0 6px #000" }}>{phu}</div> : null}
      </div>
      </React.Fragment>
    );
  };
  // ô số liệu nằm dưới tiêu đề; khi đang hiện thì là vùng cấm của nhãn
  const oSo = { l: the.x, r: the.x + the.w, t: the.y + 230 * s, b: the.y + 470 * s };
  if (p.so && hienSo * tatSo > 0.05) che.push(oSo);

  return (
    <AbsoluteFill style={{ fontFamily: ff, backgroundColor: "#05080A", opacity: tat }}>
      {/* nền lưới + ánh vàng hắt từ dưới */}
      <AbsoluteFill style={{
        backgroundImage: "linear-gradient(rgba(255,255,255,0.10) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.10) 1px, transparent 1px)",
        backgroundSize: `${120 * s}px ${120 * s}px`,
      }} />
      <AbsoluteFill style={{ background: "radial-gradient(ellipse 90% 40% at 50% 100%, rgba(255,190,40,0.35), transparent 70%)" }} />

      {/* thẻ bản đồ */}
      <div style={{
        position: "absolute", left: the.x, top: the.y, width: the.w, height: the.h, borderRadius: 40 * s, overflow: "hidden",
        border: `${9 * s}px solid ${VIEN}`, boxShadow: `0 0 ${40 * s}px rgba(43,217,166,0.35)`, background: "#0B1412",
      }}>
        {/* lớp bản đồ theo toạ độ ảnh nền */}
        <div style={{ position: "absolute", left: 0, top: 0, transformOrigin: "0 0",
          transform: `translate(${tamX - the.x - 9 * s}px, ${tamY - the.y - 9 * s}px) scale(${cam.zoom}) translate(${-cam.cx}px, ${-cam.cy}px)` }}>
          <Img src={staticFile(p.nen.file)} style={{ position: "absolute", width: p.nen.w, height: p.nen.h, filter: "brightness(0.62) saturate(0.85) contrast(1.05)" }} />
          {p.can ? (
            <Img src={staticFile(p.can.file)} style={{
              position: "absolute", left: p.can.x, top: p.can.y, width: p.can.w, height: p.can.h, filter: "brightness(0.62) saturate(0.85) contrast(1.05)",
              opacity: interpolate(cam.zoom, [0.9, 1.4], [0, 1], kep), // chỉ hiện khi phóng sát
              maskImage: "radial-gradient(ellipse 50% 50% at 50% 50%, #000 70%, transparent 100%)",
            }} />
          ) : null}
          <svg width={p.nen.w} height={p.nen.h} style={{ position: "absolute", overflow: "visible" }}>
            <defs>
              <filter id="phat" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation={6 * k * s} /></filter>
            </defs>
            <rect x={-p.nen.w} y={-p.nen.h} width={p.nen.w * 3} height={p.nen.h * 3} fill="#000" opacity={toi} />
            {/* ranh giới xã: nền vàng mờ + viền vẽ dần */}
            <path d={dPath(p.xa.vong)} fill={VANG} fillOpacity={0.08 * veXa} stroke="none" />
            <path d={dPath(p.xa.vong)} fill="none" stroke={VANG} strokeWidth={4.5 * k * s} strokeLinejoin="round"
              strokeDasharray={lX} strokeDashoffset={lX * (1 - veXa)} style={{ filter: `drop-shadow(0 0 ${5 * k * s}px rgba(255,205,45,0.9))` }} />
            {/* tuyến đường */}
            {p.tuyen.map((tu, i) => tu.net.map((n, j) => {
              const l = doDai(n);
              return <path key={`${i}-${j}`} d={dPath(n)} fill="none" stroke={tu.mau} strokeWidth={4 * k * s} strokeLinecap="round" opacity={0.95}
                strokeDasharray={l} strokeDashoffset={l * (1 - veTuyen)} style={{ filter: `drop-shadow(0 0 ${4 * k * s}px ${tu.mau})` }} />;
            }))}
            {/* kênh phát sáng: quầng mờ + lõi sáng + nét đứt chạy */}
            <path d={dPath(p.kenh.duong)} fill="none" stroke={NGOC} strokeWidth={26 * k * s} strokeLinecap="round" opacity={0.55 * nhat}
              strokeDasharray={lK} strokeDashoffset={lK * (1 - veKenh)} filter="url(#phat)" />
            <path d={dPath(p.kenh.duong)} fill="none" stroke={NGOC} strokeWidth={9 * k * s} strokeLinecap="round" opacity={nhat}
              strokeDasharray={lK} strokeDashoffset={lK * (1 - veKenh)} />
            {veKenh >= 1 ? (
              <path d={dPath(p.kenh.duong)} fill="none" stroke="#FFFFFF" strokeOpacity={0.85} strokeWidth={2.5 * k * s}
                strokeDasharray={`${18 * k * s} ${22 * k * s}`} strokeDashoffset={-t * 60 * k * s} />
            ) : null}
            {/* đầu bút lóe khi kênh đang vẽ */}
            {veKenh > 0 && veKenh < 1 ? (() => {
              let con = lK * veKenh, q = p.kenh.duong[0];
              for (let i = 1; i < p.kenh.duong.length; i++) {
                const a = p.kenh.duong[i - 1], b = p.kenh.duong[i], d = Math.hypot(b[0] - a[0], b[1] - a[1]);
                if (con <= d) { q = [a[0] + (b[0] - a[0]) * con / d, a[1] + (b[1] - a[1]) * con / d]; break; }
                con -= d;
              }
              return <circle cx={q[0]} cy={q[1]} r={12 * k * s} fill="#FFFFFF" style={{ filter: `drop-shadow(0 0 ${14 * k * s}px ${NGOC})` }} />;
            })() : null}
            {/* cầu: ghim vàng có vòng toả */}
            {p.cau && hienCau > 0 ? (
              <g transform={`translate(${p.cau.xy[0]} ${p.cau.xy[1]})`} opacity={hienCau}>
                <circle r={(14 + 26 * ((t * 1.2) % 1)) * k * s} fill="none" stroke={VANG} strokeWidth={3 * k * s} opacity={1 - ((t * 1.2) % 1)} />
                <circle r={9 * k * s} fill={VANG} stroke="#000" strokeWidth={2 * k * s} />
              </g>
            ) : null}
          </svg>
        </div>

        {/* nhãn (không gian màn hình, cỡ chữ cố định) */}
        <div style={{ position: "absolute", inset: 0, left: -the.x - 9 * s, top: -the.y - 9 * s, width: W, height: H }}>
          {/* thứ tự = ưu tiên đặt nhãn: cầu, xã, kênh, tuyến, xã lân cận */}
          {p.cau ? nhan([p.cau.xy[0] + 30 / cam.zoom, p.cau.xy[1] - 60 / cam.zoom], p.cau.ten, VANG, 36, hienCau, "cau", p.cau.phu) : null}
          {nhan(p.xa.nhan, p.xa.ten, VANG, 34, veXa, "xa")}
          {nhan(p.kenh.nhan, p.kenh.ten, NGOC, 32, veKenh, "kenh")}
          {p.tuyen.map((tu, i) => nhan(tu.nhan, tu.ten, tu.mau, 28, veTuyen, `t${i}`))}
          {p.langGieng.map((g, i) => nhan(g.xy, g.ten, "rgba(255,255,255,0.72)", 22, veXa * (1 - interpolate(t, [p.moc.cau, p.moc.cau + 0.6], [0, 1], kep)), `g${i}`))}
        </div>

        {/* vignette trên/dưới cho chữ dễ đọc */}
        <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0.75) 0%, transparent 22%, transparent 62%, rgba(0,0,0,0.85) 100%)" }} />

        {/* tiêu đề */}
        <div style={{ position: "absolute", left: 48 * s, top: 54 * s }}>
          <div style={{ fontSize: 22 * s, letterSpacing: 7 * s, color: "#C9D6D2", fontWeight: 700 }}>{p.tieuDe.nho}</div>
          <div style={{ fontSize: 76 * s, fontWeight: 900, color: "#FFFFFF", lineHeight: 1.05, textShadow: "0 4px 12px rgba(0,0,0,0.7)" }}>{p.tieuDe.lon}</div>
          <div style={{ fontSize: 24 * s, color: "#AFC0BB", fontWeight: 600, letterSpacing: 1 * s }}>{p.tieuDe.phu}</div>
        </div>

        {/* mũi tên Bắc + bản đồ nhỏ định vị */}
        <div style={{ position: "absolute", right: 48 * s, top: 54 * s, display: "flex", flexDirection: "column", alignItems: "center", gap: 14 * s }}>
          <svg width={34 * s} height={50 * s} viewBox="0 0 34 50"><path d="M17 0 L31 34 L17 26 L3 34 Z" fill="#FFFFFF" /><text x="17" y="49" textAnchor="middle" fontSize="13" fontWeight="800" fill="#FFFFFF">N</text></svg>
          <div style={{ width: 150 * s, height: 150 * s * p.nen.h / p.nen.w, border: "1.5px solid rgba(255,255,255,0.45)", borderRadius: 6 * s, overflow: "hidden", position: "relative", background: "#000" }}>
            <Img src={staticFile(p.nen.file)} style={{ width: "100%", height: "100%", filter: "brightness(0.5)" }} />
            <svg viewBox={`0 0 ${p.nen.w} ${p.nen.h}`} style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }}>
              <path d={dPath(p.kenh.duong)} fill="none" stroke={NGOC} strokeWidth={40} />
              <path d={dPath(p.xa.vong)} fill="none" stroke={VANG} strokeWidth={22} opacity={veXa} />
              {(() => {
                const vw = the.w / cam.zoom, vh = the.h / cam.zoom;
                return <rect x={cam.cx - vw / 2} y={cam.cy - vh * 0.48} width={vw} height={vh} fill="none" stroke="#FFFFFF" strokeWidth={24} />;
              })()}
            </svg>
          </div>
        </div>

        {/* ô số liệu */}
        {p.so && hienSo * tatSo > 0 ? (
          <div style={{
            position: "absolute", left: 48 * s, right: 48 * s, top: 250 * s, opacity: hienSo * tatSo, translate: `0 ${(1 - hienSo) * 30 * s}px`,
            background: "rgba(6,18,16,0.82)", border: `2px solid ${VIEN}`, borderRadius: 18 * s, padding: `${22 * s}px ${30 * s}px`,
            boxShadow: `0 0 ${30 * s}px rgba(43,217,166,0.3)`,
          }}>
            <div style={{ display: "flex", alignItems: "baseline", gap: 16 * s }}>
              <div style={{ fontSize: 96 * s, fontWeight: 900, color: NGOC, lineHeight: 1 }}>
                {(() => { const g = parseFloat(p.so.gia.replace(",", ".")); const v = g * interpolate(t, [p.moc.so, p.moc.so + 1.2], [0, 1], { ...kep, easing: Easing.out(Easing.cubic) }); return v.toFixed(1).replace(".", ","); })()}
              </div>
              <div style={{ fontSize: 44 * s, fontWeight: 800, color: "#FFFFFF" }}>{p.so.donVi}</div>
            </div>
            <div style={{ fontSize: 28 * s, color: "#C9D6D2", fontWeight: 600, marginTop: 8 * s }}>{p.so.dong}</div>
          </div>
        ) : null}

        {/* thước tỷ lệ */}
        <div style={{ position: "absolute", left: 48 * s, bottom: 420 * s, display: "flex", alignItems: "center", gap: 12 * s }}>
          <div style={{ width: thuoc / mMan, height: 12 * s, borderLeft: "2px solid #fff", borderRight: "2px solid #fff", position: "relative" }}>
            <div style={{ position: "absolute", left: 0, right: 0, top: 5 * s, height: 2, background: "#fff" }} />
          </div>
          <div style={{ fontSize: 22 * s, color: "#fff", fontWeight: 700 }}>{thuoc >= 1000 ? `${thuoc / 1000} km` : `${thuoc} m`}</div>
        </div>

        {/* phụ đề */}
        {cau ? (
          <div key={cau.batDau} style={{ position: "absolute", left: 60 * s, right: 60 * s, bottom: 140 * s, display: "flex", flexWrap: "wrap", justifyContent: "center", rowGap: 4 * s, fontSize: 50 * s, fontWeight: 800, lineHeight: 1.3,
            opacity: interpolate(t, [cau.ketThuc + 0.05, cau.ketThuc + 0.3], [1, 0], kep), textShadow: `0 ${3 * s}px ${10 * s}px #000` }}>
            {cau.chu.split(" ").map((w, i, a) => {
              const vao = cau.tu.length === a.length ? cau.tu[i] : cau.batDau + (i / a.length) * (cau.ketThuc - cau.batDau) * 0.85;
              const vang = cau.nhan.some((n) => n.split(" ").some((k) => k === w || k === w.replace(/[,.]$/, ""))); // giữ dấu phẩy trong số "8,3"
              return <span key={i} style={{ color: t >= vao ? (vang ? VANG : "#FFFFFF") : "rgba(255,255,255,0.38)", marginRight: 12 * s }}>{w}</span>;
            })}
          </div>
        ) : null}

        {/* nguồn + thanh tiến độ */}
        <div style={{ position: "absolute", left: 48 * s, right: 48 * s, bottom: 40 * s }}>
          {p.nguon.map((n, i) => <div key={i} style={{ fontSize: 17 * s, color: "rgba(220,230,226,0.7)", lineHeight: 1.45 }}>{n}</div>)}
          <div style={{ marginTop: 12 * s, height: 3 * s, background: "rgba(255,255,255,0.15)" }}>
            <div style={{ width: `${(t / het) * 100}%`, height: "100%", background: VIEN }} />
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
