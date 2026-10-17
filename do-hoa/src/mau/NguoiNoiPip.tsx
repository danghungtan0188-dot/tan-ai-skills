// Người nói ↔ khung tròn góc: video người nói chạy suốt, tiếng không đổi. Trong mỗi đoạn `doHoa`, ảnh/video đồ họa
// phủ toàn khung và người nói thu mượt thành vòng tròn viền trắng ở góc dưới phải, hết đoạn thì phóng lại toàn khung.
// File đọc qua staticFile (--public-dir).
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FPS } from "../chung";

export const nguoiNoiPipSchema = coBan.extend({
  video: z.string(), // video người nói
  doHoa: z.array(z.object({ tu: z.number(), den: z.number(), file: z.string() })).default([]),
  coTron: z.number().default(220), // đường kính vòng tròn (px ở khung 1920 hoặc 1080 rộng)
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const CHUYEN = 0.45; // giây thu/phóng
const laVideo = (f: string) => /\.(mp4|mov|webm|m4v)$/i.test(f);

export const NguoiNoiPip: React.FC<z.infer<typeof nguoiNoiPipSchema>> = ({ video, doHoa, coTron }) => {
  const frame = useCurrentFrame();
  const { width: W, height: H } = useVideoConfig();
  const t = frame / FPS;
  const s = W / (W > H ? 1920 : 1080);

  // p = 0: toàn khung, 1: vòng tròn. Gộp các đoạn cách nhau dưới 2 lần thời gian chuyển, kẻo người nói
  // phóng ra rồi thu lại ngay ở chỗ nối hai đồ họa.
  const khoang: { tu: number; den: number }[] = [];
  for (const { tu, den } of [...doHoa].sort((a, b) => a.tu - b.tu)) {
    const cuoi = khoang[khoang.length - 1];
    if (cuoi && tu - cuoi.den < 2 * CHUYEN) cuoi.den = Math.max(cuoi.den, den);
    else khoang.push({ tu, den });
  }
  const p = Math.max(
    0,
    ...khoang.map(({ tu, den }) =>
      Math.min(
        interpolate(t, [tu, tu + CHUYEN], [0, 1], { ...kep, easing: Easing.inOut(Easing.cubic) }),
        interpolate(t, [den - CHUYEN, den], [1, 0], { ...kep, easing: Easing.inOut(Easing.cubic) }),
      ),
    ),
  );

  const d = coTron * s;
  const le = 40 * s;
  const vien = 6 * s;
  // Khung người nói: từ cả khung (W×H, góc vuông) về hình vuông d×d bo tròn hoàn toàn ở góc dưới phải.
  const rong = interpolate(p, [0, 1], [W, d]);
  const cao = interpolate(p, [0, 1], [H, d]);
  const trai = interpolate(p, [0, 1], [0, W - d - le]);
  const tren = interpolate(p, [0, 1], [0, H - d - le]);

  return (
    <AbsoluteFill style={{ background: "#000" }}>
      {doHoa.map(({ tu, den, file }, i) => (
        <Sequence key={i} from={Math.round(tu * FPS)} durationInFrames={Math.max(1, Math.round((den - tu) * FPS))}>
          <AbsoluteFill style={{ background: "#fff" }}>
            {laVideo(file) ? (
              <OffthreadVideo src={staticFile(file)} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
            ) : (
              <Img src={staticFile(file)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
            )}
          </AbsoluteFill>
        </Sequence>
      ))}
      <div
        style={{
          position: "absolute", left: trai, top: tren, width: rong, height: cao, overflow: "hidden",
          borderRadius: interpolate(p, [0, 1], [0, d / 2]),
          boxShadow: p > 0 ? `0 0 0 ${vien * p}px white, 0 ${10 * s}px ${30 * s}px rgba(0,0,0,${0.45 * p})` : "none",
        }}
      >
        <OffthreadVideo src={staticFile(video)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      </div>
    </AbsoluteFill>
  );
};
