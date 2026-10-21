// Số lăn như đồng hồ đo: "2025" thành "2026". Mỗi chữ số là một cột 0–9 trượt xuống, số mới rơi từ trên vào,
// cột đổi lần lượt từ phải sang trái. Chữ số không đổi đứng yên. Nền trong suốt để đắp lên video.
// Ý tưởng cột chữ số: iart-ai/tiktok-video-skills (digit-flip.md, MIT).
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FONT, FPS, MAU, vaoRa } from "../chung";

export const soLanSchema = coBan.extend({
  tu: z.string().min(1),
  den: z.string().min(1),
  tai: z.number().min(0).default(0.6),
  tieuDe: z.string().default(""),
});

const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const nayNhe = Easing.bezier(0.34, 1.4, 0.64, 1); // vượt nhẹ rồi khớp, như bánh xe đồng hồ
const MOI_COT = 0.7; // giây lăn một cột
const CACH_COT = 0.12; // cột bên trái bắt đầu trễ hơn cột bên phải

const laSo = (c: string) => c >= "0" && c <= "9";

export const SoLan: React.FC<z.infer<typeof soLanSchema>> = (p) => {
  const frame = useCurrentFrame();
  const { width, durationInFrames } = useVideoConfig();
  const doc = p.tiLe === "9:16";
  const s = width / (doc ? 1080 : 1920);
  const co = (doc ? 260 : 300) * s;
  const cao = co * 1.15;

  const dai = Math.max(p.tu.length, p.den.length);
  const cu = p.tu.padStart(dai, " ");
  const moi = p.den.padStart(dai, " ");
  // thứ tự lăn tính từ phải sang, chỉ đếm các cột có đổi
  let thuTu = 0;
  const lich = [...moi].map((_, i) => i).reverse().map((i) => (cu[i] !== moi[i] ? thuTu++ : -1)).reverse();

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        fontFamily: FONT,
        opacity: vaoRa(frame, durationInFrames, 0.3, 0.4),
      }}
    >
      {p.tieuDe ? (
        <div
          style={{
            color: "white",
            fontWeight: 700,
            fontSize: (doc ? 64 : 60) * s,
            marginBottom: 10 * s,
            textShadow: `0 ${4 * s}px ${18 * s}px rgba(0,0,0,.6)`,
          }}
        >
          {p.tieuDe}
        </div>
      ) : null}
      <div style={{ display: "flex", filter: `drop-shadow(0 ${6 * s}px ${20 * s}px rgba(0,0,0,.55))` }}>
        {[...moi].map((c, i) => {
          const o = { height: cao, lineHeight: `${cao}px`, textAlign: "center" as const };
          const kieu = {
            color: MAU.vang,
            fontWeight: 800,
            fontSize: co,
            fontVariantNumeric: "tabular-nums" as const,
            WebkitTextStroke: `${3 * s}px ${MAU.navyNews}`,
          };
          if (lich[i] < 0 || !laSo(c) || !laSo(cu[i])) {
            // không đổi, hoặc không phải chữ số: đứng yên (ký tự mới hiện mờ dần nếu khác)
            const bd = (p.tai + Math.max(lich[i], 0) * CACH_COT) * FPS;
            return (
              <div key={i} style={{ ...o, ...kieu, width: laSo(c) ? co * 0.62 : undefined, opacity: lich[i] < 0 ? 1 : interpolate(frame, [bd, bd + 8], [0, 1], kep) }}>
                {c === " " ? "" : c}
              </div>
            );
          }
          const a = Number(cu[i]);
          const buoc = (Number(c) - a + 10) % 10 || 10; // lăn tới, qua 9 thì về 0
          const bd = (p.tai + lich[i] * CACH_COT) * FPS;
          const t = interpolate(frame, [bd, bd + MOI_COT * FPS], [0, 1], { ...kep, easing: nayNhe });
          // cột xếp số lớn dần lên trên; kéo cột xuống thì số mới rơi từ trên vào
          const day = Array.from({ length: buoc + 1 }, (_, k) => (a + k) % 10);
          return (
            <div
              key={i}
              style={{
                ...o,
                overflow: "hidden",
                position: "relative",
                width: co * 0.62,
                // mờ mép trên dưới: chữ đang lăn tan dần thay vì bị cắt sắc
                maskImage: "linear-gradient(transparent, black 16%, black 84%, transparent)",
              }}
            >
              <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, translate: `0 ${t * buoc * cao}px` }}>
                {day
                  .slice()
                  .reverse()
                  .map((d, k) => (
                    <div key={k} style={{ ...o, ...kieu }}>
                      {d}
                    </div>
                  ))}
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
