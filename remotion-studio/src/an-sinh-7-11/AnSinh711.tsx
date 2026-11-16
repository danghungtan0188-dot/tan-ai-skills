// Video tuyen truyen "Chuong trinh an sinh xa hoi 7/11/2026 — xa An Thanh Thuy": chi do hoa + anh lanh dao + anh 3 dia diem
// (nguoi dung dan: khong lay anh/khuc video khac). Moc theo giong doc: T[id] = giay bat dau cau (data.ts sinh tu moc.json).
// Tong do tham + vang kim trang trong; 3 canh dia diem: anh nho ben trai, noi dung chinh ben phai (theo y nguoi dung).
import React from "react";
import {AbsoluteFill, Audio, Easing, Img, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig} from "remotion";
import {DURATION_S, SUB, T} from "./data";

const C = {do: "#7a0f16", doDam: "#3d0609", vang: "#f2c75c", vangNhat: "#ffe7a3", kem: "#fff6e2", muc: "#2a1406", trang: "#ffffff"};
const FONT = "'Segoe UI', 'Arial', sans-serif";
const A = (p: string) => staticFile(`an-sinh-7-11/${p}`);

const useSec = () => useCurrentFrame() / useVideoConfig().fps;
const ease = (t: number, a: number, b: number) =>
  interpolate(t, [a, b], [0, 1], {extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic)});
const soVN = (x: number) => Math.round(x).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");

// **chu** -> to vang dam
const Rich: React.FC<{text: string; mau?: string}> = ({text, mau = "#b3261e"}) => (
  <>{text.split(/(\*\*[^*]+\*\*)/).map((p, i) => p.startsWith("**")
    ? <span key={i} style={{color: mau, fontWeight: 800}}>{p.slice(2, -2)}</span> : <span key={i}>{p}</span>)}</>
);

const Nen: React.FC = () => {
  const t = useSec();
  return (
    <AbsoluteFill style={{background: "radial-gradient(ellipse at 50% 30%, #4cc954 0%, #23a03a 45%, #0b5a22 100%)"}}>
      {/* nen xanh la + mang luoi laser troi nhe — giong 4 s ket (nguoi dung 29/10: "thay mau nen sang mau xanh nhu cuoi video") */}
      <svg width={1920} height={1080} style={{position: "absolute", opacity: 0.3}}>
        {(() => {
          const d = Array.from({length: 30}).map((_, i) => ({x: ((i * 577) % 1920) + 30 * Math.sin(t * 0.25 + i * 1.7), y: ((i * 331 + 90) % 1080) + 22 * Math.cos(t * 0.22 + i * 1.3)}));
          return <>{d.map((a, i) => d.slice(i + 1).map((b, j) => {
            const k = Math.hypot(a.x - b.x, a.y - b.y);
            return k < 400 ? <line key={`${i}-${j}`} x1={a.x} y1={a.y} x2={b.x} y2={b.y} stroke="#e4ffdc" strokeWidth={1.2} opacity={1 - k / 400} /> : null;
          }))}{d.map((a, i) => <circle key={i} cx={a.x} cy={a.y} r={3} fill="#f0ffe9" />)}</>;
        })()}
      </svg>
      {/* tia sang vang hinh nan quat xoay cham — giu lai theo y nguoi dung */}
      <div style={{position: "absolute", left: 960 - 1400, top: -1400, width: 2800, height: 2800, opacity: 0.18,
        background: `repeating-conic-gradient(from ${t * 3}deg at 50% 50%, ${C.vang} 0deg 4deg, transparent 4deg 18deg)`,
        maskImage: "radial-gradient(circle, black 0%, transparent 60%)", WebkitMaskImage: "radial-gradient(circle, black 0%, transparent 60%)"}} />
      {/* bui sang bay nhe */}
      {Array.from({length: 26}).map((_, i) => {
        const x = (i * 397) % 1920, y = (1080 + 80 - ((t * (14 + (i % 5) * 6) + i * 131) % 1240));
        return <div key={i} style={{position: "absolute", left: x + 20 * Math.sin(t / 2 + i), top: y, width: 4 + (i % 3) * 2, height: 4 + (i % 3) * 2,
          borderRadius: "50%", background: C.vangNhat, opacity: 0.25 + 0.2 * Math.sin(t + i), filter: "blur(1px)"}} />;
      })}
      {/* hoa van vien duoi */}
      <div style={{position: "absolute", left: 0, right: 0, bottom: 0, height: 10, background: `linear-gradient(90deg, transparent, ${C.vang}, transparent)`, opacity: 0.7}} />
    </AbsoluteFill>
  );
};

// chu vang anh kim co vet sang luot qua
const ChuVang: React.FC<{children: React.ReactNode; size: number; t: number; tre?: number; style?: React.CSSProperties}> = ({children, size, t, tre = 0, style}) => (
  <div style={{fontSize: size, fontWeight: 900, lineHeight: 1.12, letterSpacing: 1, textAlign: "center",
    // KHONG dung background-clip:text: anh tinh (still) hien dung nhung render ca phim ra khoi vang dac -> chu vang dac + bong
    color: "#f6cf6a", textShadow: `0 2px 0 #a8741f, 0 6px 18px rgba(0,0,0,0.55), 0 0 ${18 + 8 * Math.sin((t - tre) * 2)}px rgba(255,214,120,0.45)`, ...style}}>
    {children}
  </div>
);

const Dau: React.FC<{nhan: string}> = ({nhan}) => (
  <div style={{position: "absolute", left: 70, top: 40, right: 70, display: "flex", alignItems: "center", gap: 18}}>
    <div style={{width: 10, height: 54, background: C.vang, borderRadius: 4}} />
    <div style={{display: "flex", flexDirection: "column"}}>
      <span style={{color: C.vang, fontSize: 22, fontWeight: 800, letterSpacing: 3}}>CHƯƠNG TRÌNH AN SINH XÃ HỘI · 07/11/2026</span>
      <span style={{color: C.kem, fontSize: 36, fontWeight: 800}}>{nhan}</span>
    </div>
    <div style={{flex: 1}} />
    <Img src={A("att_news.png")} style={{height: 56}} />
  </div>
);

// phu de tieng Viet duoi khung (vung an toan, khong de len noi dung)
const PhuDe: React.FC = () => {
  const t = useSec();
  const s = SUB.find(([a, b]) => t >= a && t < b);
  if (!s) return null;
  const a = ease(t, s[0], s[0] + 0.2) * (1 - ease(t, s[1] - 0.15, s[1]));
  return (
    <div style={{position: "absolute", left: 0, right: 0, bottom: 34, display: "flex", justifyContent: "center", opacity: a}}>
      <div style={{maxWidth: 1600, padding: "10px 30px", borderRadius: 12, background: "rgba(4,30,12,0.78)", color: C.trang, fontSize: 42,
        fontWeight: 600, textAlign: "center", lineHeight: 1.3, borderBottom: `3px solid ${C.vang}`}}>{s[2]}</div>
    </div>
  );
};

// bieu tuong 2 tong: net `mau` + mang to `phu` — chi tiet hon ban net manh cu (nguoi dung: "bieu tuong nen dep hon")
const IconTron: React.FC<{loai: string; size: number; mau?: string; phu?: string}> = ({loai, size, mau = C.muc, phu = "rgba(122,15,22,0.18)"}) => (
  <svg viewBox="0 0 100 100" width={size} height={size} fill="none" stroke={mau} strokeWidth={5} strokeLinecap="round" strokeLinejoin="round">
    {loai === "qua" ? <g><rect x="20" y="44" width="60" height="38" rx="4" fill={phu} /><rect x="14" y="32" width="72" height="14" rx="3" fill={phu} />
        <path d="M50 32v50M14 39h72" /><path d="M50 32c-4-14-24-16-22-4c2 7 22 4 22 4zM50 32c4-14 24-16 22-4c-2 7-22 4-22 4z" fill={phu} /></g>
      : loai === "sach" ? <g><path d="M50 28c-10-7-26-7-34-3v52c8-4 24-4 34 3c10-7 26-7 34-3V25c-8-4-24-4-34 3z" fill={phu} /><path d="M50 28v52" />
        <path d="M24 38c6-2 14-2 20 1M24 50c6-2 14-2 20 1M56 39c6-3 14-3 20-1M56 51c6-3 14-3 20-1" strokeWidth={3} /></g>
      : loai === "yte" ? <g><path d="M50 84C24 66 14 52 14 38a18 18 0 0 1 36-6a18 18 0 0 1 36 6c0 14-10 28-36 46z" fill={phu} />
        <path d="M50 38v26M37 51h26" strokeWidth={8} /></g>
      : loai === "gio" ? <g><circle cx="50" cy="52" r="32" fill={phu} /><path d="M50 32v20l13 9" strokeWidth={6} />
        <path d="M50 22v5M50 77v5M20 52h5M75 52h5M36 12h28" strokeWidth={4} /></g>
      : loai === "ghim" ? <g><path d="M50 88c-16-20-26-32-26-48a26 26 0 0 1 52 0c0 16-10 28-26 48z" fill={phu} />
        <path d="M50 30l3.5 7 7.5 1-5.5 5 1.5 7.5-7-3.8-7 3.8 1.5-7.5-5.5-5 7.5-1z" fill={mau} strokeWidth={1} /></g>
      : loai === "nguoi" ? <g><circle cx="50" cy="30" r="11" fill={phu} /><circle cx="24" cy="40" r="8" /><circle cx="76" cy="40" r="8" />
        <path d="M30 80c0-18 9-28 20-28s20 10 20 28" fill={phu} /><path d="M8 78c0-12 7-20 16-20M92 78c0-12-7-20-16-20" /></g>
      : loai === "giayto" ? <g><path d="M26 14h34l16 16v56H26z" fill={phu} /><path d="M60 14v16h16" /><path d="M36 44h28M36 56h28M36 68h14" strokeWidth={4} /></g>
      : loai === "dienthoai" ? <g><rect x="30" y="12" width="40" height="76" rx="7" fill={phu} /><path d="M44 78h12" />
        <path d="M78 30c5 5 5 13 0 18M86 24c9 9 9 22 0 31" strokeWidth={4} /></g>
      : loai === "danhsach" ? <g><rect x="18" y="14" width="64" height="74" rx="6" fill={phu} /><path d="M40 14v-4h20v4" />
        <path d="M28 36l5 5 9-9M28 56l5 5 9-9M28 76l5 5 9-9" strokeWidth={4} /><path d="M50 37h22M50 57h22M50 77h16" strokeWidth={4} /></g>
      : loai === "mat" ? <g><path d="M8 50c11-20 26-30 42-30s31 10 42 30c-11 20-26 30-42 30S19 70 8 50z" fill={phu} />
        <circle cx="50" cy="50" r="15" /><circle cx="50" cy="50" r="6" fill={mau} /><circle cx="56" cy="44" r="3" fill="#fff" stroke="none" /></g>
      : <g><circle cx="50" cy="50" r="34" fill={phu} /><path d="M32 51l13 13 24-27" strokeWidth={8} /></g>}
  </svg>
);

// huy hieu tron: vien vang xoay cham + loi do tham + bieu tuong vang + sao lap lanh
const HuyHieu: React.FC<{loai: string; size?: number; a?: number}> = ({loai, size = 96, a = 1}) => {
  const t = useCurrentFrame() / 30;
  const lap = 0.5 + 0.5 * Math.sin(t * 3 + size);
  return (
    <div style={{flex: "none", position: "relative", width: size, height: size, transform: `scale(${0.6 + 0.4 * a})`, opacity: a}}>
      <svg width={size} height={size} viewBox="0 0 100 100" style={{position: "absolute", inset: 0, transform: `rotate(${t * 25}deg)`}}>
        <circle cx="50" cy="50" r="47" fill="none" stroke={C.vangNhat} strokeWidth="2.5" strokeDasharray="6 5" />
      </svg>
      <div style={{position: "absolute", inset: size * 0.07, borderRadius: "50%", background: `radial-gradient(circle at 35% 30%, ${C.vangNhat}, ${C.vang} 50%, #a8741f)`,
        boxShadow: `0 8px 22px rgba(0,0,0,0.45), 0 0 ${10 + 14 * lap}px rgba(255,214,120,0.55)`}} />
      <div style={{position: "absolute", inset: size * 0.15, borderRadius: "50%", background: `radial-gradient(circle at 40% 35%, #b51d26, ${C.do} 60%, #4a070c)`,
        display: "flex", alignItems: "center", justifyContent: "center", boxShadow: "inset 0 3px 8px rgba(0,0,0,0.5)"}}>
        <IconTron loai={loai} size={size * 0.5} mau={C.vangNhat} phu="rgba(255,214,120,0.28)" />
      </div>
      <svg width={size * 0.3} height={size * 0.3} viewBox="0 0 20 20" style={{position: "absolute", right: -size * 0.02, top: -size * 0.02, opacity: lap, transform: `scale(${0.6 + 0.5 * lap})`}}>
        <path d="M10 0l2 8 8 2-8 2-2 8-2-8-8-2 8-2z" fill="#fff8dc" />
      </svg>
    </div>
  );
};

// vet sang luot qua the luc the hien ra (dat trong the co position relative + overflow hidden)
const Quet: React.FC<{t: number; at: number}> = ({t, at}) => {
  const k = ease(t, at + 0.1, at + 1.0);
  if (k <= 0 || k >= 1) return null;
  return <div style={{position: "absolute", top: 0, bottom: 0, left: `${-40 + 160 * k}%`, width: "30%", pointerEvents: "none",
    background: "linear-gradient(100deg, transparent, rgba(255,255,255,0.75), transparent)", transform: "skewX(-20deg)"}} />;
};

// hoa van duoi tieu de: vach vang - hinh thoi - vach vang, chay ra tu giua
const HoaVan: React.FC<{t: number; at: number; rong?: number}> = ({t, at, rong = 700}) => {
  const k = ease(t, at, at + 0.9);
  return (
    <div style={{display: "flex", alignItems: "center", justifyContent: "center", gap: 14, marginTop: 14, opacity: k}}>
      <div style={{width: (rong / 2) * k, height: 3, background: `linear-gradient(90deg, transparent, ${C.vang})`}} />
      <svg width="34" height="34" viewBox="0 0 34 34" style={{transform: `rotate(${45 + 180 * (1 - k)}deg)`}}>
        <rect x="9" y="9" width="16" height="16" fill={C.vang} /><rect x="13" y="13" width="8" height="8" fill={C.do} />
      </svg>
      <div style={{width: (rong / 2) * k, height: 3, background: `linear-gradient(270deg, transparent, ${C.vang})`}} />
    </div>
  );
};

// tia lap lanh bung ra quanh con so luc dem xong
const BungSao: React.FC<{t: number; at: number}> = ({t, at}) => {
  const k = t - at - 1.2;
  if (k < 0 || k > 0.9) return null;
  return <>{Array.from({length: 8}).map((_, i) => {
    const g = (i / 8) * Math.PI * 2, d = 20 + 70 * k;
    return <div key={i} style={{position: "absolute", left: "50%", top: "50%", width: 8, height: 8, borderRadius: 4, background: C.vang,
      boxShadow: `0 0 10px ${C.vang}`, transform: `translate(${Math.cos(g) * d - 4}px, ${Math.sin(g) * d - 4}px)`, opacity: 1 - k / 0.9}} />;
  })}</>;
};

// ================= CANH 1: MO DAU =================
const MoDau: React.FC<{o: number}> = ({o}) => {
  const t = useSec() + o;   // t = giay tuyet doi trong phim
  const {fps} = useVideoConfig();
  const f = useCurrentFrame();
  const ba = [["qua", "Phần quà nghĩa tình", T.c1_01], ["sach", "Suất học bổng tiếp sức đến trường", T.c1_02], ["yte", "Khám, điều trị bệnh kịp thời", T.c1_03]] as const;
  const giaiDoan = t < T.c1_05 - 0.3 ? 0 : t < T.c1_07 - 0.3 ? 1 : t < T.c1_09 - 0.3 ? 2 : 3;
  const ra = (k: number) => giaiDoan === k ? 1 : 0;
  return (
    <AbsoluteFill>
      {/* 1a: ba gia tri se chia */}
      <AbsoluteFill style={{alignItems: "center", justifyContent: "center", gap: 30, flexDirection: "row", opacity: ra(0) * ease(t, 0, 0.6)}}>
        {ba.map(([loai, nhan, at], i) => {
          const a = spring({frame: f - Math.round((at - o) * fps), fps, config: {damping: 13}});
          return (
            <div key={i} style={{width: 560, display: "flex", flexDirection: "column", alignItems: "center", gap: 26, opacity: Math.min(1, a), transform: `translateY(${(1 - a) * 60}px)`}}>
              <HuyHieu loai={loai} size={220} a={Math.min(1, a)} />
              <div style={{color: C.kem, fontSize: 48, fontWeight: 800, textAlign: "center", lineHeight: 1.25}}>{nhan}</div>
            </div>
          );
        })}
      </AbsoluteFill>
      {/* 1b: ten chuong trinh + ngay */}
      <AbsoluteFill style={{alignItems: "center", justifyContent: "center", flexDirection: "column", opacity: ra(1) * ease(t, T.c1_05 - 0.3, T.c1_05 + 0.4)}}>
        <div style={{color: C.vang, fontSize: 34, fontWeight: 800, letterSpacing: 8, opacity: ease(t, T.c1_05, T.c1_05 + 0.6)}}>TRI ÂN · SẺ CHIA</div>
        <ChuVang size={112} t={t} tre={T.c1_05} style={{marginTop: 14, transform: `scale(${0.92 + 0.08 * ease(t, T.c1_05, T.c1_05 + 1)})`}}>LAN TỎA YÊU THƯƠNG<br />AN SINH XÃ HỘI</ChuVang>
        <HoaVan t={t} at={T.c1_05 + 0.6} rong={900} />
        <div style={{marginTop: 34, display: "flex", alignItems: "center", gap: 20, padding: "16px 40px", borderRadius: 60, border: `3px solid ${C.vang}`,
          background: "rgba(0,0,0,0.28)", opacity: ease(t, T.c1_06, T.c1_06 + 0.5)}}>
          <HuyHieu loai="gio" size={64} />
          <span style={{color: C.kem, fontSize: 44, fontWeight: 800}}>THỨ BẢY · 07/11/2026</span>
        </div>
        <div style={{marginTop: 20, color: C.vangNhat, fontSize: 32, fontWeight: 700, letterSpacing: 2, opacity: ease(t, T.c1_06 + 0.5, T.c1_06 + 1)}}>XÃ AN THẠNH THỦY · TỈNH ĐỒNG THÁP</div>
      </AbsoluteFill>
      {/* 1c: gioi thieu lanh dao */}
      <AbsoluteFill style={{opacity: ra(2) * ease(t, T.c1_07 - 0.3, T.c1_07 + 0.4)}}>
        {[["lanh_dao_1.jpg", T.c1_07, T.c1_08], ["lanh_dao_2.jpg", T.c1_08, 1e9]].map(([anh, a0, a1], i) => (
          <div key={i} style={{position: "absolute", left: 180, top: 150, width: 560, height: 740, borderRadius: 20, overflow: "hidden",
            border: `8px solid ${C.vang}`, boxShadow: "0 0 60px rgba(242,199,92,0.45), 0 30px 60px rgba(0,0,0,0.5)",
            opacity: ease(t, (a0 as number) - 0.2, (a0 as number) + 0.5) * (1 - ease(t, (a1 as number) - 0.3, (a1 as number) + 0.3))}}>
            <Img src={A(anh as string)} style={{width: "100%", height: "100%", objectFit: "cover", objectPosition: "top",
              transform: `scale(${1.02 + 0.05 * ease(t, a0 as number, (a0 as number) + 8)})`}} />
          </div>
        ))}
        <div style={{position: "absolute", left: 830, top: 300, width: 960}}>
          <div style={{color: C.vang, fontSize: 36, fontWeight: 700, letterSpacing: 3, opacity: ease(t, T.c1_07 + 0.3, T.c1_07 + 0.8)}}>NGUYÊN PHÓ CHỦ TỊCH NƯỚC</div>
          <div style={{marginTop: 10, transform: `translateX(${(1 - ease(t, T.c1_07 + 0.5, T.c1_07 + 1.2)) * 40}px)`, opacity: ease(t, T.c1_07 + 0.5, T.c1_07 + 1.2)}}>
            <ChuVang size={76} t={t} tre={T.c1_07} style={{textAlign: "left", whiteSpace: "nowrap"}}>ĐẶNG THỊ NGỌC THỊNH</ChuVang>
          </div>
          <div style={{marginTop: 18, width: 520 * ease(t, T.c1_07 + 0.9, T.c1_07 + 1.8), height: 4, background: C.vang}} />
          <div style={{marginTop: 22, color: C.kem, fontSize: 42, fontWeight: 600, lineHeight: 1.4, opacity: ease(t, T.c1_08, T.c1_08 + 0.5)}}>
            cùng Đoàn công tác đến thăm, tặng quà và thực hiện<br />các hoạt động an sinh xã hội tại xã An Thạnh Thủy
          </div>
        </div>
      </AbsoluteFill>
      {/* 1d: doi tuong huong toi */}
      <AbsoluteFill style={{alignItems: "center", justifyContent: "center", flexDirection: "column", opacity: ra(3) * ease(t, T.c1_09 - 0.3, T.c1_09 + 0.4)}}>
        <ChuVang size={64} t={t} tre={T.c1_09}>CHƯƠNG TRÌNH HƯỚNG ĐẾN</ChuVang>
        <HoaVan t={t} at={T.c1_09 + 0.2} rong={700} />
        <div style={{marginTop: 50, display: "flex", gap: 40}}>
          {[["qua", "Người có công\nvới cách mạng"], ["nguoi", "Người dân có\nhoàn cảnh khó khăn"], ["sach", "Học sinh hiếu học\nvượt khó"]].map(([loai, nhan], i) => {
            const a = ease(t, T.c1_09 + 0.4 + i * 1.3, T.c1_09 + 0.9 + i * 1.3);
            return (
              <div key={i} style={{position: "relative", overflow: "hidden", width: 500, padding: "34px 20px", borderRadius: 26, background: "rgba(255,246,226,0.95)",
                display: "flex", flexDirection: "column", alignItems: "center", gap: 18, boxShadow: "0 20px 40px rgba(0,0,0,0.35)", opacity: a,
                transform: `translateY(${(1 - a) * 40}px)`}}>
                <Quet t={t} at={T.c1_09 + 0.4 + i * 1.3} />
                <HuyHieu loai={loai} size={140} />
                <div style={{color: C.do, fontSize: 44, fontWeight: 800, textAlign: "center", whiteSpace: "pre-line", lineHeight: 1.25}}>{nhan}</div>
              </div>
            );
          })}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ================= CANH 2-4: DIA DIEM (anh nho trai, noi dung phai) =================
type Muc = {loai: string; at: number; so?: number; donVi?: string; dong: string; phu?: string};
type DiaDiem = {gio: string; anh: string; anhChinh?: string; tieuDe: string; noi: string; muc: Muc[]; nhan?: {at: number; text: string}};

const CanhDiaDiem: React.FC<{o: number; d: DiaDiem; het: number}> = ({o, d, het}) => {
  const t = useSec() + o;
  const {fps} = useVideoConfig();
  const f = useCurrentFrame();
  const vao = spring({frame: f, fps, config: {damping: 15}});
  return (
    <AbsoluteFill style={{opacity: 1 - ease(t, het - 0.4, het)}}>
      {/* anh chinh NGANG (poster nguoi dung ghep, 1536x1024) neu co; khong thi anh DOC 554x941 */}
      <div style={{position: "absolute", left: d.anhChinh ? 70 : 90, top: d.anhChinh ? 190 : 150, width: d.anhChinh ? 900 : 470, height: d.anhChinh ? 600 : 800,
        borderRadius: 24, overflow: "hidden", border: `6px solid ${C.vang}`,
        boxShadow: "0 0 50px rgba(242,199,92,0.35), 0 30px 60px rgba(0,0,0,0.45)", transform: `translateX(${(1 - vao) * -80}px)`, opacity: vao}}>
        <Img src={A(d.anhChinh ?? d.anh)} style={{width: "100%", height: "100%", objectFit: "cover", objectPosition: "top", transform: `scale(${1.01 + 0.04 * ease(t, o, het)})`}} />
      </div>
      <div style={{position: "absolute", left: d.anhChinh ? 1010 : 640, top: 160, width: d.anhChinh ? 840 : 1200}}>
        <div style={{opacity: ease(t, o + 0.2, o + 0.7), transform: `translateY(${(1 - ease(t, o + 0.2, o + 0.7)) * 20}px)`}}>
          <ChuVang size={d.anhChinh ? 44 : 54} t={t} tre={o} style={{textAlign: "left", whiteSpace: "pre-line"}}>{d.tieuDe}</ChuVang>
        </div>
        <div style={{marginTop: 18, display: "flex", gap: 30, alignItems: "center", color: C.kem, fontSize: 32, fontWeight: 700, opacity: ease(t, o + 0.5, o + 1)}}>
          <span style={{display: "flex", alignItems: "center", gap: 10, padding: "6px 22px", borderRadius: 40, background: C.vang, color: C.muc, fontWeight: 900, whiteSpace: "nowrap", flex: "none"}}>
            <IconTron loai="gio" size={38} />{d.gio} · 07/11/2026</span>
          <span style={{display: "flex", alignItems: "center", gap: 8}}><IconTron loai="ghim" size={38} />{d.noi.replace(/\n/g, " ")}</span>
        </div>
        <div style={{marginTop: 20, display: "flex", flexDirection: "column", gap: 14}}>
          {d.muc.map((m, i) => {
            const a = ease(t, m.at - 0.15, m.at + 0.4);
            const dem = m.so ? m.so * ease(t, m.at, m.at + 1.3) : 0;
            return (
              <div key={i} style={{position: "relative", overflow: "hidden", display: "flex", alignItems: "center", gap: 20, padding: "10px 22px", borderRadius: 20,
                background: "rgba(255,246,226,0.96)", boxShadow: "0 14px 30px rgba(0,0,0,0.3)", opacity: a, transform: `translateX(${(1 - a) * 60}px)`}}>
                <Quet t={t} at={m.at} />
                <HuyHieu loai={m.loai} size={80} />
                {m.so ? <div style={{position: "relative", flex: "none", minWidth: 140, color: C.do, fontSize: 62, fontWeight: 900, textAlign: "center"}}><BungSao t={t} at={m.at} />
                  {soVN(dem)}<span style={{fontSize: 30}}>{m.donVi ?? ""}</span></div> : null}
                <div style={{display: "flex", flexDirection: "column"}}>
                  <div style={{color: C.muc, fontSize: 34, fontWeight: 700, lineHeight: 1.2}}><Rich text={m.dong} /></div>
                  {m.phu ? <div style={{color: "#7a4b12", fontSize: 28, fontWeight: 600, marginTop: 2}}>{m.phu}</div> : null}
                </div>
              </div>
            );
          })}
        </div>
        {d.nhan ? (
          <div style={{marginTop: 16, padding: "10px 22px", borderRadius: 18, border: `3px solid ${C.vang}`, background: "rgba(0,0,0,0.3)", color: C.vangNhat,
            fontSize: 32, fontWeight: 800, display: "flex", alignItems: "center", gap: 14, opacity: ease(t, d.nhan.at - 0.2, d.nhan.at + 0.4),
            boxShadow: `0 0 ${20 + 14 * Math.sin(t * 4)}px rgba(242,199,92,0.45)`}}>
            <HuyHieu loai="dienthoai" size={52} />{d.nhan.text}
          </div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};

// ================= CANH 5: LUU Y =================
const LuuY: React.FC<{o: number; het: number}> = ({o, het}) => {
  const t = useSec() + o;
  const muc = [
    ["danhsach", "Theo dõi **thông báo, giấy mời**; có mặt **đúng giờ, đúng địa điểm**", T.c5_03],
    ["giayto", "Khám bệnh: mang **giấy tờ tùy thân, hồ sơ khám bệnh, đơn thuốc** (nếu có)", T.c5_05],
    ["mat", "Khám mắt: liên hệ **Trưởng ấp** hoặc **Trạm Y tế xã** để đăng ký", T.c5_07],
    ["qua", "Quà, học bổng: theo **danh sách** địa phương, nhà trường; **không tự ý tập trung**", T.c5_10],
  ] as const;
  return (
    <AbsoluteFill style={{opacity: 1 - ease(t, het - 0.4, het)}}>
      <div style={{position: "absolute", left: 0, right: 0, top: 150, display: "flex", justifyContent: "center", opacity: ease(t, o + 0.1, o + 0.6)}}>
        <div style={{display: "flex", alignItems: "center", gap: 18, padding: "14px 48px", borderRadius: 60, background: C.vang}}>
          <IconTron loai="danhsach" size={54} /><span style={{color: C.do, fontSize: 50, fontWeight: 900, letterSpacing: 2}}>NGƯỜI DÂN CẦN LƯU Ý</span>
        </div>
      </div>
      <div style={{position: "absolute", left: 200, right: 200, top: 290, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 30}}>
        {muc.map(([loai, x, at], i) => {
          const a = ease(t, at - 0.2, at + 0.4);
          return (
            <div key={i} style={{position: "relative", overflow: "hidden", display: "flex", gap: 22, alignItems: "center", padding: "26px 28px", borderRadius: 24,
              background: "rgba(255,246,226,0.96)", minHeight: 250, boxShadow: "0 16px 34px rgba(0,0,0,0.35)", opacity: a, transform: `scale(${0.9 + 0.1 * a})`}}>
              <Quet t={t} at={at} />
              <HuyHieu loai={loai} size={130} />
              <div style={{color: C.muc, fontSize: 40, fontWeight: 600, lineHeight: 1.32}}><Rich text={x} /></div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// ================= CANH 6: LICH TRINH + KET =================
const Ket: React.FC<{o: number}> = ({o}) => {
  const t = useSec() + o;
  const moc = [["9:00", "Khám bệnh, tư vấn sức khỏe, khám sàng lọc mắt", "TT Văn hóa - Thể thao xã An Thạnh Thủy", T.c6_04],
    ["9:30", "Trao tặng tủ sách và quà cho học sinh", "Trường Tiểu học An Thạnh Thủy (điểm chính)", T.c6_05],
    ["10:30", "Trao quà người có công, người khó khăn, học bổng", "TT Văn hóa - Thể thao Bình Phục Nhứt", T.c6_06]] as const;
  const giai2 = ease(t, T.c6_08 - 0.4, T.c6_08 + 0.2);
  const giai3 = ease(t, T.c6_12 - 0.4, T.c6_12 + 0.2);
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{opacity: 1 - giai2}}>
        <div style={{position: "absolute", left: 0, right: 0, top: 150, textAlign: "center", opacity: ease(t, o, o + 0.6)}}>
          <ChuVang size={60} t={t} tre={o}>LỊCH TRÌNH · THỨ BẢY, 07/11/2026</ChuVang>
          <HoaVan t={t} at={o + 0.4} rong={800} />
        </div>
        <div style={{position: "absolute", left: 190, top: 270, width: 6, height: 640 * ease(t, T.c6_04 - 0.6, T.c6_06 + 0.4), background: C.vang, borderRadius: 3}} />
        {moc.map(([gio, viec, noi, at], i) => {
          const a = ease(t, at - 0.2, at + 0.45);
          return (
            <div key={i} style={{position: "absolute", left: 140, top: 280 + i * 215, display: "flex", alignItems: "center", gap: 34, opacity: a, transform: `translateX(${(1 - a) * 50}px)`}}>
              <div style={{width: 106, height: 106, borderRadius: "50%", background: C.vang, display: "flex", alignItems: "center", justifyContent: "center",
                color: C.do, fontSize: 32, fontWeight: 900, boxShadow: "0 0 30px rgba(242,199,92,0.6)"}}>{gio}</div>
              <div style={{position: "relative", overflow: "hidden", width: 1400, padding: "18px 34px", borderRadius: 20, background: "rgba(255,246,226,0.96)"}}>
                <Quet t={t} at={at} />
                <div style={{color: C.do, fontSize: 46, fontWeight: 900}}>{viec}</div>
                <div style={{color: C.muc, fontSize: 34, fontWeight: 600, marginTop: 6, display: "flex", alignItems: "center", gap: 10}}><IconTron loai="ghim" size={40} />{noi}</div>
              </div>
            </div>
          );
        })}
      </AbsoluteFill>
      <AbsoluteFill style={{alignItems: "center", justifyContent: "center", flexDirection: "column", opacity: giai2 * (1 - giai3)}}>
        <div style={{display: "flex", gap: 36, opacity: ease(t, T.c6_08, T.c6_08 + 0.6)}}>
          {["qua", "sach", "yte", "nguoi"].map((l, i) => <HuyHieu key={l} loai={l} size={120} a={ease(t, T.c6_08 + i * 0.5, T.c6_08 + 0.5 + i * 0.5)} />)}
        </div>
        <ChuVang size={62} t={t} tre={T.c6_10} style={{marginTop: 50, width: 1600, opacity: ease(t, T.c6_11, T.c6_11 + 0.6)}}>
          ĐƯA HOẠT ĐỘNG AN SINH THIẾT THỰC ĐẾN ĐÚNG ĐỐI TƯỢNG
        </ChuVang>
        <HoaVan t={t} at={T.c6_11 + 0.6} rong={900} />
        <div style={{marginTop: 20, color: C.kem, fontSize: 44, fontWeight: 700, opacity: ease(t, T.c6_11 + 2, T.c6_11 + 2.6)}}>Góp phần chăm lo tốt hơn đời sống Nhân dân</div>
      </AbsoluteFill>
      <AbsoluteFill style={{alignItems: "center", justifyContent: "center", flexDirection: "column", opacity: giai3}}>
        <div style={{color: C.vang, fontSize: 36, fontWeight: 800, letterSpacing: 6}}>ỦY BAN NHÂN DÂN XÃ AN THẠNH THỦY</div>
        <ChuVang size={96} t={t} tre={T.c6_12} style={{marginTop: 16}}>TRÂN TRỌNG THÔNG BÁO</ChuVang>
        <HoaVan t={t} at={T.c6_12 + 0.5} rong={1000} />
        <div style={{marginTop: 30, display: "flex", gap: 40, color: C.kem, fontSize: 42, fontWeight: 700, opacity: ease(t, T.c6_13, T.c6_13 + 0.6)}}>
          <span>✓ Đúng thành phần</span><span>✓ Đúng thời gian</span><span>✓ Đúng địa điểm</span>
        </div>
        <div style={{marginTop: 40, color: C.vangNhat, fontSize: 40, fontWeight: 800, opacity: ease(t, T.c6_15, T.c6_15 + 0.6)}}>Chu đáo · An toàn · Ý nghĩa</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const DD: DiaDiem[] = [
  {gio: "9:00", anh: "dd1.jpg", anhChinh: "dd1_chinh.jpg", tieuDe: "KHÁM BỆNH · TƯ VẤN SỨC KHỎE\nKHÁM SÀNG LỌC MẮT", noi: "Trung tâm Văn hóa - Thể thao\nxã An Thạnh Thủy",
    muc: [{loai: "yte", at: T.c2_04, so: 200, dong: "người dân có hoàn cảnh khó khăn", phu: "được khám bệnh, tư vấn sức khỏe"},
      {loai: "nguoi", at: T.c2_05, dong: "Ưu tiên: **hộ nghèo, cận nghèo, người cao tuổi**"},
      {loai: "mat", at: T.c2_07, so: 50, dong: "trường hợp đục thủy tinh thể", phu: "dự kiến được hỗ trợ phẫu thuật"}],
    nhan: {at: T.c2_11, text: "Đăng ký khám mắt: liên hệ Trưởng ấp hoặc Trạm Y tế xã"}},
  {gio: "9:30", anh: "dd2.jpg", anhChinh: "dd2_chinh.jpg", tieuDe: "TRAO SÁCH, TẶNG QUÀ\nTIẾP SỨC HỌC SINH ĐẾN TRƯỜNG", noi: "Trường Tiểu học An Thạnh Thủy\n(điểm trường chính)",
    muc: [{loai: "sach", at: T.c3_04, so: 50, donVi: " triệu", dong: "**01 tủ sách** cùng sách", phu: "tổng trị giá khoảng 50 triệu đồng"},
      {loai: "qua", at: T.c3_05, so: 50, dong: "phần quà", phu: "cho học sinh có hoàn cảnh khó khăn"},
      {loai: "check", at: T.c3_06, dong: "Phong phú tài liệu, **khơi dậy niềm yêu thích đọc sách**"}]},
  {gio: "10:30", anh: "dd3.jpg", anhChinh: "dd3_chinh.jpg", tieuDe: "TRI ÂN NGƯỜI CÓ CÔNG\nCHĂM LO NGƯỜI KHÓ KHĂN", noi: "Trung tâm Văn hóa - Thể thao\nBình Phục Nhứt",
    muc: [{loai: "qua", at: T.c4_04, so: 20, dong: "phần quà người có công", phu: "4 Bà mẹ Việt Nam anh hùng · 16 thương binh, bệnh binh"},
      {loai: "nguoi", at: T.c4_08, so: 200, dong: "phần quà", phu: "cho người nghèo, người có hoàn cảnh khó khăn"},
      {loai: "sach", at: T.c4_09, so: 100, dong: "suất học bổng", phu: "cho học sinh hiếu học vượt khó"}],
    nhan: {at: T.c4_06, text: "“Uống nước nhớ nguồn” – tri ân những cống hiến, hy sinh"}},
];

export const AnSinh711: React.FC = () => {
  const {fps} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);
  const CANH = [
    {tu: 0, den: T.c2_01 - 0.5, nhan: "Lan tỏa sự sẻ chia"},
    {tu: T.c2_01 - 0.5, den: T.c3_01 - 0.5, nhan: "Chăm sóc sức khỏe – Mở thêm cơ hội tìm lại ánh sáng"},
    {tu: T.c3_01 - 0.5, den: T.c4_01 - 0.5, nhan: "Trao sách, tặng quà – Tiếp sức học sinh đến trường"},
    {tu: T.c4_01 - 0.5, den: T.c5_01 - 0.5, nhan: "Tri ân người có công – Chăm lo người khó khăn"},
    {tu: T.c5_01 - 0.5, den: T.c6_01 - 0.5, nhan: "Thông tin người dân cần lưu ý"},
    {tu: T.c6_01 - 0.5, den: DURATION_S, nhan: "Lịch trình chương trình"},
  ];
  return (
    <AbsoluteFill style={{fontFamily: FONT}}>
      <Nen />
      {CANH.map((c, i) => (
        <Sequence key={i} from={f(c.tu)} durationInFrames={f(c.den - c.tu)}>
          {i > 0 ? <Dau nhan={c.nhan} /> : null}
          {i === 0 ? <MoDau o={c.tu} /> : i <= 3 ? <CanhDiaDiem o={c.tu} d={DD[i - 1]} het={c.den} /> : i === 4 ? <LuuY o={c.tu} het={c.den} /> : <Ket o={c.tu} />}
        </Sequence>
      ))}
      <PhuDe />
      <Audio src={A("am_thanh.wav")} />
    </AbsoluteFill>
  );
};
