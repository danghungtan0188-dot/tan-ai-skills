// Ảnh bay vào xếp chồng rồi phóng to (kiểu video tổng kết): nền là ảnh chính khử màu + làm mờ, các ảnh viền trắng
// lần lượt bay vào từ ngoài khung, nghiêng nhẹ, chồng lên nhau. Ảnh cuối danh sách đáp giữa khung rồi phóng to
// phủ kín, nền trở lại màu. Toàn khung. Ảnh đọc qua staticFile (--public-dir).
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FONT, FPS } from "../chung";

export const anhBayVaoSchema = coBan.extend({
  anh: z.array(z.string()).min(2).max(8), // ảnh cuối = ảnh chính, phóng to toàn khung
  cachNhau: z.number().default(0.45), // giây giữa hai ảnh bay vào
  tieuDe: z.string().default(""),
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

// Chỗ đáp (tâm, theo % khung) và góc nghiêng — rải quanh tâm để ảnh chính đè lên giữa.
const CHO = [
  [30, 32, -9], [72, 30, 7], [28, 70, 6], [70, 72, -6], [50, 24, 3], [48, 76, -4], [22, 50, 11],
] as const;

export const AnhBayVao: React.FC<z.infer<typeof anhBayVaoSchema>> = ({ anh, cachNhau, tieuDe }) => {
  const frame = useCurrentFrame();
  const { width: W, height: H, durationInFrames } = useVideoConfig();
  const t = frame / FPS;
  const het = durationInFrames / FPS;
  const s = Math.min(W / 1920, H / 1080);
  const chinh = anh[anh.length - 1];
  const phu = anh.slice(0, -1);
  const tPhong = het - 2; // bắt đầu phóng to
  const phong = interpolate(t, [tPhong, tPhong + 1.2], [0, 1], { ...kep, easing: Easing.inOut(Easing.cubic) });
  const vien = 14 * s;
  const rong0 = W * 0.42;

  const the = (i: number, cx: number, cy: number, goc: number, vao: number) => {
    const p = spring({ frame: frame - vao * FPS, fps: FPS, config: { damping: 16, mass: 0.9 } });
    const huong = (i * 137) % 360; // mỗi ảnh bay từ một hướng khác
    const xa = Math.max(W, H) * 0.9;
    const x = cx + Math.cos((huong * Math.PI) / 180) * xa * (1 - p);
    const y = cy + Math.sin((huong * Math.PI) / 180) * xa * (1 - p);
    return { p, x, y, goc: goc + (1 - p) * 25 * (i % 2 ? 1 : -1) };
  };

  const khung = (src: string, key: React.Key, x: number, y: number, rong: number, goc: number, v: number, op = 1) => (
    <div
      key={key}
      style={{
        position: "absolute", left: x - rong / 2 - v, top: y - (rong * H) / W / 2 - v,
        width: rong, height: (rong * H) / W, border: `${v}px solid white`, rotate: `${goc}deg`, opacity: op,
        boxShadow: `0 ${12 * s}px ${30 * s}px rgba(0,0,0,0.5)`, overflow: "hidden", background: "#222",
      }}
    >
      <Img src={staticFile(src)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
    </div>
  );

  const vaoChinh = 0.3 + phu.length * cachNhau;
  const c = the(phu.length, W / 2, H / 2, -2, vaoChinh);

  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <AbsoluteFill style={{ scale: 1.1 }}>
        <Img
          src={staticFile(chinh)}
          style={{
            width: "100%", height: "100%", objectFit: "cover",
            filter: `grayscale(${1 - phong}) blur(${(1 - phong) * 14 * s}px) brightness(${0.65 + 0.35 * phong})`,
          }}
        />
      </AbsoluteFill>
      {phu.map((src, i) => {
        const [px, py, goc] = CHO[i % CHO.length];
        const a = the(i, (px / 100) * W, (py / 100) * H, goc, 0.3 + i * cachNhau);
        return a.p > 0.001 ? khung(src, i, a.x, a.y, rong0 * 0.85, a.goc, vien, 1 - phong) : null;
      })}
      {c.p > 0.001
        ? khung(chinh, "chinh", interpolate(phong, [0, 1], [c.x, W / 2]), interpolate(phong, [0, 1], [c.y, H / 2]),
            interpolate(phong, [0, 1], [rong0, W]), c.goc * (1 - phong), vien * (1 - phong))
        : null}
      {tieuDe ? (
        <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 90 * s }}>
          <div
            style={{
              fontFamily: FONT, fontWeight: 800, fontSize: 64 * s, color: "white", textAlign: "center",
              textShadow: `0 ${4 * s}px ${14 * s}px rgba(0,0,0,0.8)`,
              opacity: interpolate(t, [tPhong + 1, tPhong + 1.6], [0, 1], kep),
              translate: `0px ${interpolate(t, [tPhong + 1, tPhong + 1.6], [30, 0], kep) * s}px`,
            }}
          >
            {tieuDe}
          </div>
        </AbsoluteFill>
      ) : null}
    </AbsoluteFill>
  );
};
