// Số liệu đè thẳng lên flycam (học từ phóng sự "Lương Hòa đồng hành cùng doanh nghiệp", 10/2026): không hộp nền,
// số in nghiêng đậm màu xanh có viền trắng + chữ đơn vị trắng nghiêng có viền tối, góc dưới phải. Mỗi mục trượt vào
// từ phải có nhòe chuyển động (giãn ngang + mờ) rồi đứng yên đúng lúc lời đọc nhắc tới số; ra thì nhòe sang trái.
// Nền trong suốt — đắp lên video bằng ProRes 4444.
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FPS } from "../chung";

export const soDeFlycamSchema = coBan.extend({
  font: z.string().default("Arial, 'Segoe UI', sans-serif"),
  mauSo: z.string().default("#1E3CFF"),
  muc: z.array(z.object({
    tu: z.number(), den: z.number(), // giây hiện / tắt
    truoc: z.string().default(""), // chữ trước số, ví dụ "tổng vốn đăng ký hơn"
    so: z.string(), // "57", "26.600", "30.941"
    sau: z.string().default(""), // "doanh nghiệp", "tỉ đồng"
  })),
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

export const SoDeFlycam: React.FC<z.infer<typeof soDeFlycamSchema>> = ({ font, mauSo, muc }) => {
  const frame = useCurrentFrame();
  const { width: W, height: H } = useVideoConfig();
  const t = frame / FPS;
  const s = H / 1080;
  const m = muc.find((x) => t >= x.tu && t < x.den);
  if (!m) return null;
  const vao = interpolate(t, [m.tu, m.tu + 0.35], [0, 1], { ...kep, easing: Easing.out(Easing.cubic) });
  const ra = interpolate(t, [m.den - 0.3, m.den], [0, 1], { ...kep, easing: Easing.in(Easing.cubic) });
  const lech = (1 - vao) * 260 * s - ra * 200 * s; // vào từ phải, ra sang trái
  const nhoe = (1 - vao) * 14 + ra * 12; // px mờ
  const gian = 1 + (1 - vao) * 0.6 + ra * 0.4; // giãn ngang giả nhòe chuyển động
  const vien = (mau: string, d: number) => `${d}px ${mau}`;
  const chu = {
    fontFamily: font, fontStyle: "italic" as const, fontWeight: 900, lineHeight: 1,
    paintOrder: "stroke fill" as const, filter: `blur(${nhoe * s}px) drop-shadow(0 ${4 * s}px ${8 * s}px rgba(0,0,0,0.55))`,
  };
  return (
    <AbsoluteFill>
      <div style={{
        position: "absolute", right: W * 0.045, bottom: H * 0.1, display: "flex", alignItems: "baseline", gap: 12 * s,
        translate: `${lech}px 0px`, scale: `${gian} 1`, transformOrigin: "right center", opacity: 1 - ra,
      }}>
        {m.truoc ? <span style={{ ...chu, fontSize: 40 * s, color: "#FFFFFF", WebkitTextStroke: vien("#0A1A6B", 5 * s) }}>{m.truoc}</span> : null}
        <span style={{ ...chu, fontSize: 92 * s, color: mauSo, WebkitTextStroke: vien("#FFFFFF", 7 * s) }}>{m.so}</span>
        {m.sau ? <span style={{ ...chu, fontSize: 46 * s, color: "#FFFFFF", WebkitTextStroke: vien("#0A1A6B", 5 * s) }}>{m.sau}</span> : null}
      </div>
    </AbsoluteFill>
  );
};
