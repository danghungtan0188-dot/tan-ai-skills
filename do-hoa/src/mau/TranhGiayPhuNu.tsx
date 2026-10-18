// Tranh giấy mừng ngày Phụ nữ (20/10): bình minh hồng – vàng, mặt trời giấy, đồi lượn và đầm sen cắt giấy
// đổ bóng chồng lớp. Các lớp bật lên như sách pop-up, sen nở, cánh hoa rơi; dải băng đỏ chữ vàng mở ra
// mang tiêu đề, sau đó đổi sang lời chúc. Hình vẽ toàn bằng SVG tự dựng, không dùng ảnh ngoài.
import React from "react";
import { AbsoluteFill, Easing, interpolate, random, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FONT, FPS } from "../chung";

export const tranhGiayPhuNuSchema = coBan.extend({
  tieuDe: z.string(),
  dongTen: z.string().default(""),
  dongNgay: z.string().default(""),
  loiChuc1: z.string().default(""),
  loiChuc2: z.string().default(""),
  dongKy: z.string().default(""), // đơn vị gửi lời chúc; trống thì không hiện
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const muot = Easing.bezier(0.16, 1, 0.3, 1);
const bat = Easing.out(Easing.back(1.5)); // bật lên có nảy nhẹ, như trang sách pop-up

const BONG = "drop-shadow(0 12px 14px rgba(60,10,30,0.45))";
const VIEN = "#FFF1DC"; // viền giấy kem

// Sóng nước: lượn đều + vòng xoắn ở đỉnh, như giấy cắt.
const Song: React.FC<{ W: number; H: number; y: number; bien: number; buoc: number; mau: string; lech: number }> = ({
  W, H, y, bien, buoc, mau, lech,
}) => {
  let d = `M ${-buoc * 2 + lech} ${y}`;
  for (let x = -buoc * 2; x < W + buoc * 2; x += buoc) d += ` q ${buoc / 4} ${-bien} ${buoc / 2} 0 t ${buoc / 2} 0`;
  d += ` L ${W + buoc * 2} ${H + 60} L ${-buoc * 2} ${H + 60} Z`;
  const xoan = [];
  for (let x = -buoc * 2 + buoc / 4; x < W + buoc * 2; x += buoc)
    xoan.push(<circle key={x} cx={x + lech} cy={y - bien * 0.35} r={bien * 0.3} fill="none" stroke={VIEN} strokeWidth={bien * 0.09} />);
  return (
    <g>
      <path d={d} fill={mau} stroke={VIEN} strokeWidth={bien * 0.11} />
      {xoan}
    </g>
  );
};

// Đồi lượn mềm (đường cong bậc hai qua các đỉnh).
const Doi: React.FC<{ W: number; H: number; dinh: [number, number][]; mau: string }> = ({ W, H, dinh, mau }) => {
  let d = `M 0 ${H * dinh[0][1]}`;
  for (let i = 1; i < dinh.length; i++) {
    const [x0, y0] = dinh[i - 1];
    const [x1, y1] = dinh[i];
    d += ` Q ${W * (x0 + x1) / 2} ${H * Math.min(y0, y1) - H * 0.06} ${W * x1} ${H * y1}`;
  }
  d += ` L ${W} ${H} L 0 ${H} Z`;
  return <path d={d} fill={mau} stroke="#F7C873" strokeWidth={H * 0.004} />;
};

// Mây giấy: cụm tròn trên đế bo tròn.
const May: React.FC<{ x: number; y: number; r: number }> = ({ x, y, r }) => (
  <g>
    {[[-1.4, 0.2], [-0.6, -0.5], [0.4, -0.7], [1.3, 0], [0, 0.1]].map(([dx, dy], i) => (
      <circle key={i} cx={x + dx * r} cy={y + dy * r} r={r * (i === 4 ? 1.1 : 0.85)} fill="#FFF3E6" stroke="#E98AA6" strokeWidth={r * 0.08} />
    ))}
    <rect x={x - 2.4 * r} y={y + 0.3 * r} width={4.8 * r} height={0.9 * r} rx={0.45 * r} fill="#FFF3E6" stroke="#E98AA6" strokeWidth={r * 0.08} />
  </g>
);

// Lá sen: đĩa tròn khuyết một khe hẹp (hai mép khe nằm đúng trên đường tròn), có gân.
const LaSen: React.FC<{ x: number; y: number; r: number; xoay: number }> = ({ x, y, r, xoay }) => {
  const khe = (12 * Math.PI) / 180;
  const [cx, sy] = [r * Math.cos(khe), r * Math.sin(khe)];
  return (
    <g transform={`translate(${x} ${y}) rotate(${xoay}) scale(1 0.42)`}>
      <path d={`M 0 0 L ${cx} ${-sy} A ${r} ${r} 0 1 0 ${cx} ${sy} Z`} fill="#3E9B5F" stroke="#D9F2C2" strokeWidth={r * 0.05} />
      {[45, 100, 155, 205, 260, 315].map((g) => (
        <line key={g} x1={0} y1={0} x2={r * 0.8 * Math.cos((g * Math.PI) / 180)} y2={r * 0.8 * Math.sin((g * Math.PI) / 180)} stroke="#2C7A48" strokeWidth={r * 0.035} />
      ))}
    </g>
  );
};

// Hoa sen: cánh hình giọt nước xoè ra theo `no` (0 = búp, 1 = nở hết).
const HoaSen: React.FC<{ x: number; y: number; r: number; no: number }> = ({ x, y, r, no }) => {
  const canh = (goc: number, dai: number, mau: string, key: string) => (
    <path
      key={key}
      d={`M 0 0 C ${-dai * 0.42} ${-dai * 0.3} ${-dai * 0.3} ${-dai * 0.85} 0 ${-dai} C ${dai * 0.3} ${-dai * 0.85} ${dai * 0.42} ${-dai * 0.3} 0 0 Z`}
      transform={`rotate(${goc * no})`}
      fill={mau}
      stroke="#FFF0F5"
      strokeWidth={r * 0.035}
    />
  );
  return (
    <g transform={`translate(${x} ${y}) scale(${0.35 + 0.65 * Math.min(1, no * 1.4)})`}>
      <path d={`M 0 0 L 0 ${r * 1.6}`} stroke="#2F7A4A" strokeWidth={r * 0.09} />
      {[-78, 78, -52, 52].map((g, i) => canh(g, r * 1.05, i < 2 ? "#F48FB1" : "#F7A8C4", `n${i}`))}
      {[-26, 26, 0].map((g, i) => canh(g, r * 1.15, i < 2 ? "#F06A93" : "#E8507F", `t${i}`))}
      <ellipse cx={0} cy={-r * 0.1} rx={r * 0.22} ry={r * 0.12} fill="#FFD25A" opacity={no} />
    </g>
  );
};

// Cánh hoa nhỏ rơi.
const CanhRoi: React.FC<{ x: number; y: number; r: number; xoay: number }> = ({ x, y, r, xoay }) => (
  <path
    d={`M 0 0 C ${-r * 0.6} ${-r * 0.4} ${-r * 0.4} ${-r * 1.2} 0 ${-r * 1.4} C ${r * 0.4} ${-r * 1.2} ${r * 0.6} ${-r * 0.4} 0 0 Z`}
    transform={`translate(${x} ${y}) rotate(${xoay})`}
    fill="#F7A3C0"
    stroke="#FFF0F5"
    strokeWidth={r * 0.12}
  />
);

// Dải băng đỏ có đuôi gấp, đường chỉ vàng, mở dần từ giữa ra.
const DaiBang: React.FC<{ W: number; H: number; s: number; mo: number; chu: string; doMo: number }> = ({ W, H, s, mo, chu, doMo }) => {
  const rong = W * 0.6;
  const cao = 150 * s;
  const duoi = cao * 0.75;
  const x0 = (W - rong) / 2;
  return (
    <div style={{ position: "absolute", left: 0, top: H * 0.08, width: W, height: cao * 1.4, opacity: doMo, filter: BONG }}>
      <svg width={W} height={cao * 1.4} style={{ position: "absolute", scale: `${Math.max(mo, 0.001)} 1`, transformOrigin: "50% 50%" }}>
        {/* đuôi gấp hai bên, đặt thấp hơn và tối hơn */}
        <path d={`M ${x0 - duoi} ${cao * 0.35} L ${x0 + duoi * 0.5} ${cao * 0.35} L ${x0 + duoi * 0.5} ${cao * 1.35} L ${x0 - duoi} ${cao * 1.35} L ${x0 - duoi * 0.55} ${cao * 0.85} Z`} fill="#8E0F24" />
        <path d={`M ${x0 + rong + duoi} ${cao * 0.35} L ${x0 + rong - duoi * 0.5} ${cao * 0.35} L ${x0 + rong - duoi * 0.5} ${cao * 1.35} L ${x0 + rong + duoi} ${cao * 1.35} L ${x0 + rong + duoi * 0.55} ${cao * 0.85} Z`} fill="#8E0F24" />
        <rect x={x0} y={cao * 0.1} width={rong} height={cao} fill="#C8102E" stroke="#F7C873" strokeWidth={4 * s} />
        <rect x={x0 + 14 * s} y={cao * 0.1 + 14 * s} width={rong - 28 * s} height={cao - 28 * s} fill="none" stroke="#FFD86B" strokeWidth={2.5 * s} strokeDasharray={`${12 * s} ${8 * s}`} />
      </svg>
      <div
        style={{
          position: "absolute", left: 0, top: cao * 0.1, width: W, height: cao, display: "flex", alignItems: "center", justifyContent: "center",
          fontFamily: FONT, fontWeight: 900, fontSize: 92 * s, letterSpacing: 4 * s, color: "#FFD86B",
          WebkitTextStroke: `${5 * s}px #5A0712`, paintOrder: "stroke fill", textShadow: `0 ${4 * s}px ${10 * s}px rgba(0,0,0,0.45)`,
          opacity: interpolate(mo, [0.6, 1], [0, 1], kep),
        }}
      >
        {chu}
      </div>
    </div>
  );
};

export const TranhGiayPhuNu: React.FC<z.infer<typeof tranhGiayPhuNuSchema>> = ({ tieuDe, dongTen, dongNgay, loiChuc1, loiChuc2, dongKy }) => {
  const frame = useCurrentFrame();
  const { width: W, height: H, durationInFrames } = useVideoConfig();
  const t = frame / FPS;
  const het = durationInFrames / FPS;
  const s = Math.min(W / 1920, H / 1080);

  // Mốc: lời chúc thay tiêu đề ở khoảng giữa clip; mờ ra đen ở 0,8 giây cuối.
  const doiChu = Math.max(4.5, het * 0.52);
  const tien = interpolate(frame, [0, durationInFrames], [0, 1], { ...kep, easing: Easing.inOut(Easing.quad) });
  const mat = interpolate(t, [0.4, 2.8], [0, 1], { ...kep, easing: muot });
  const ketThuc = interpolate(t, [het - 0.8, het], [1, 0], kep);

  // Lớp bật lên theo thứ tự từ xa tới gần; càng gần càng trôi/phóng nhiều khi máy đẩy tới.
  const lop = (thuTu: number, sau: number): React.CSSProperties => {
    const vao = interpolate(t, [0.15 + thuTu * 0.16, 0.15 + thuTu * 0.16 + 0.9], [1, 0], { ...kep, easing: bat });
    return {
      position: "absolute",
      filter: BONG,
      scale: 1 + sau * 0.12 * tien,
      translate: `0px ${vao * H * 0.45 + sau * 40 * tien * s}px`,
    };
  };

  const noSen = (tre: number) => interpolate(t, [2.2 + tre, 4.2 + tre], [0, 1], { ...kep, easing: muot });
  const songLech = (toc: number) => Math.sin(t * 0.9 + toc) * W * 0.012;

  const chu = (vao: number, ra: number, co: number, mau: string): React.CSSProperties => ({
    fontFamily: FONT, fontWeight: 900, fontSize: co * s, color: mau, textAlign: "center", lineHeight: 1.2, maxWidth: W * 0.94,
    opacity: interpolate(t, [vao, vao + 0.6, ra, ra + 0.5], [0, 1, 1, 0], kep),
    filter: `blur(${interpolate(t, [vao, vao + 0.7], [14, 0], kep) * s}px)`,
    translate: `0px ${interpolate(t, [vao, vao + 0.8, ra, ra + 0.5], [30, 0, 0, -30], { ...kep, easing: muot }) * s}px`,
    WebkitTextStroke: `${4 * s}px #4A0A1C`, paintOrder: "stroke fill",
    textShadow: `0 ${3 * s}px ${10 * s}px rgba(40,0,15,0.55)`,
  });

  const moBang = interpolate(t, [1.1, 2.0], [0, 1], { ...kep, easing: muot });
  const tatBang = interpolate(t, [doiChu, doiChu + 0.5], [1, 0], kep);

  // Cánh hoa rơi, vị trí cố định theo seed để render lại y hệt.
  const canh = Array.from({ length: 26 }, (_, i) => {
    const batDau = 2.5 + random(`b${i}`) * (het - 3);
    const tuoi = t - batDau;
    if (tuoi < 0) return null;
    const x = random(`x${i}`) * W + Math.sin(tuoi * 1.6 + i) * 40 * s;
    const y = -40 * s + tuoi * (110 + random(`v${i}`) * 90) * s;
    return <CanhRoi key={i} x={x} y={y} r={(14 + random(`r${i}`) * 12) * s} xoay={tuoi * 70 + i * 40} />;
  });

  const trongVung = H * 0.42; // vùng chữ: phần trời phía trên đồi

  return (
    <AbsoluteFill style={{ opacity: ketThuc, backgroundColor: "#000" }}>
      <AbsoluteFill style={{ background: "linear-gradient(180deg, #5B1A4A 0%, #B23A6B 30%, #F07C6B 55%, #FFC98A 76%, #FFE7C2 100%)" }} />

      {/* mặt trời giấy: đĩa + vành tia xoay chậm */}
      <svg width={W} height={H} style={{ position: "absolute", translate: `0px ${interpolate(mat, [0, 1], [H * 0.45, 0])}px`, filter: BONG }}>
        <g transform={`translate(${W / 2} ${H * 0.36}) rotate(${t * 6})`}>
          {Array.from({ length: 18 }, (_, i) => (
            <path key={i} d={`M ${-H * 0.025} ${-H * 0.2} L 0 ${-H * 0.29} L ${H * 0.025} ${-H * 0.2} Z`} transform={`rotate(${i * 20})`} fill="#FFD27A" stroke="#F49A6B" strokeWidth={2 * s} />
          ))}
        </g>
        <circle cx={W / 2} cy={H * 0.36} r={H * 0.18} fill="#FFE29A" stroke="#F49A6B" strokeWidth={5 * s} />
        <circle cx={W / 2} cy={H * 0.36} r={H * 0.14} fill="#FFC85A" />
      </svg>

      <svg width={W} height={H} style={lop(0, 0.15)}>
        <g transform={`translate(${interpolate(t, [0, het], [0, -W * 0.05])} 0)`}>
          <May x={W * 0.14} y={H * 0.2} r={H * 0.042} />
          <May x={W * 0.86} y={H * 0.15} r={H * 0.05} />
        </g>
      </svg>
      <svg width={W} height={H} style={lop(1, 0.3)}>
        <Doi W={W} H={H} dinh={[[0, 0.58], [0.22, 0.5], [0.45, 0.6], [0.7, 0.48], [1, 0.57]]} mau="#C2457A" />
      </svg>
      <svg width={W} height={H} style={lop(2, 0.45)}>
        <Doi W={W} H={H} dinh={[[0, 0.66], [0.3, 0.58], [0.58, 0.68], [0.82, 0.6], [1, 0.66]]} mau="#9C2C5E" />
      </svg>
      <svg width={W} height={H} style={lop(3, 0.6)}>
        <Song W={W} H={H} y={H * 0.74} bien={H * 0.05} buoc={W * 0.11} mau="#2E8C7E" lech={songLech(0)} />
        <LaSen x={W * 0.12} y={H * 0.8} r={H * 0.07} xoay={-8} />
        <LaSen x={W * 0.9} y={H * 0.79} r={H * 0.06} xoay={10} />
        <HoaSen x={W * 0.2} y={H * 0.76} r={H * 0.07} no={noSen(0.5)} />
        <HoaSen x={W * 0.82} y={H * 0.75} r={H * 0.065} no={noSen(0.8)} />
      </svg>
      <svg width={W} height={H} style={lop(4, 0.8)}>
        <Song W={W} H={H} y={H * 0.84} bien={H * 0.065} buoc={W * 0.15} mau="#1F6B63" lech={songLech(1.5)} />
        <LaSen x={W * 0.32} y={H * 0.9} r={H * 0.09} xoay={6} />
        <LaSen x={W * 0.7} y={H * 0.92} r={H * 0.08} xoay={-12} />
        <HoaSen x={W * 0.5} y={H * 0.84} r={H * 0.11} no={noSen(0)} />
      </svg>
      <svg width={W} height={H} style={lop(5, 1)}>
        <Song W={W} H={H} y={H * 0.95} bien={H * 0.08} buoc={W * 0.2} mau="#134C47" lech={songLech(3)} />
      </svg>

      <svg width={W} height={H} style={{ position: "absolute", filter: "drop-shadow(0 4px 4px rgba(60,10,30,0.35))" }}>
        {canh}
      </svg>

      {/* nhịp 1: dải băng tiêu đề + tên + ngày */}
      <DaiBang W={W} H={H} s={s} mo={moBang} chu={tieuDe} doMo={tatBang} />
      <AbsoluteFill style={{ alignItems: "center", paddingTop: H * 0.08 + 230 * s, gap: 14 * s }}>
        {dongTen ? <div style={chu(2.0, doiChu, 62, "#FFF4E6")}>{dongTen}</div> : null}
        {dongNgay ? <div style={chu(2.6, doiChu, 54, "#FFD86B")}>{dongNgay}</div> : null}
      </AbsoluteFill>

      {/* nhịp 2: lời chúc */}
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", height: trongVung, top: H * 0.06, gap: 18 * s }}>
        {loiChuc1 ? <div style={chu(doiChu + 0.4, het + 5, 64, "#FFF4E6")}>{loiChuc1}</div> : null}
        {loiChuc2 ? <div style={chu(doiChu + 1.1, het + 5, 64, "#FFD86B")}>{loiChuc2}</div> : null}
        {dongKy ? <div style={chu(doiChu + 1.8, het + 5, 44, "#FFF4E6")}>{dongKy}</div> : null}
      </AbsoluteFill>

      {/* vân giấy mờ phủ toàn khung */}
      <svg width={W} height={H} style={{ position: "absolute", opacity: 0.07, mixBlendMode: "multiply" }}>
        <filter id="vanGiay">
          <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={7} />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width={W} height={H} filter="url(#vanGiay)" />
      </svg>
    </AbsoluteFill>
  );
};
