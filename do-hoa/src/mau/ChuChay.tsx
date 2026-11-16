// Băng chữ chạy bản tin (ticker), nền trong suốt để đắp lên video: nhãn cố định bên trái (TIN VẮN / ĐIỂM TIN)
// + giờ tuỳ chọn, danh sách tin nối nhau bằng chấm vàng, chạy đều liên tục hết thời lượng video.
// Tốc độ tính theo khung hình nên không giật; mặc định 160 px/giây (khoảng 6–7 chữ/giây) cho người lớn tuổi kịp đọc.
// kieu "nong": băng đỏ cho tin khẩn / thông báo quan trọng. Font Segoe UI (đủ dấu tiếng Việt ở mọi độ đậm).
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { coBan, FPS, MAU } from "../chung";

export const chuChaySchema = coBan.extend({
  thoiLuong: z.number().min(3).max(1800), // chạy suốt bản tin, có thể vài phút
  nhan: z.string().default("TIN VẮN"),
  gio: z.string().default(""), // vd. "10:30"; rỗng thì không hiện
  tin: z.array(z.string().min(1)).min(1),
  kieu: z.enum(["thuong", "nong"]).default("thuong"),
  tocDo: z.number().min(60).max(400).default(160), // px/giây ở khung 1920 rộng
});

const FONT_CHAY = "'Segoe UI', Arial, sans-serif";
const kep = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const muot = Easing.bezier(0.16, 1, 0.3, 1);

const KIEU = {
  thuong: { bang: "rgba(0, 28, 100, 0.94)", nhanNen: MAU.vang, nhanChu: MAU.navyNews, vien: MAU.vang },
  nong: { bang: "rgba(150, 12, 18, 0.95)", nhanNen: "#FFFFFF", nhanChu: "#B3121B", vien: "#FFFFFF" },
} as const;

export const ChuChay: React.FC<z.infer<typeof chuChaySchema>> = ({ nhan, gio, tin, kieu, tocDo, tiLe }) => {
  const frame = useCurrentFrame();
  const { width, height, durationInFrames: het } = useVideoConfig();
  const doc = tiLe === "9:16";
  const s = width / (doc ? 1080 : 1920);
  const k = KIEU[kieu];

  const cao = 66 * s;
  const coChu = 36 * s;
  // cách mép dưới: ngang 5% (vùng an toàn truyền hình); dọc 14% (~270 px) để không bị UI TikTok/Facebook che
  // (luật chừa ~250 px đáy: skills/video-san-pham/references/dinh-dang-xuat-tiktok-facebook.md)
  const day = height * (doc ? 0.14 : 0.05);
  const vao = interpolate(frame, [0, 0.5 * FPS, het - 0.5 * FPS, het], [0, 1, 1, 0], { ...kep, easing: muot });

  // Chuỗi tin lặp đủ dài cho cả thời lượng: ước bề rộng tối thiểu 0,45 cỡ chữ mỗi ký tự (ước thấp → lặp dư, không bao giờ hụt).
  const quangDuong = tocDo * s * (het / FPS) + width;
  const soKyTu = tin.reduce((n, t) => n + t.length + 4, 0);
  const lap = Math.max(1, Math.ceil(quangDuong / (soKyTu * 0.45 * coChu)) + 1);
  const x = width * 0.6 - tocDo * s * (frame / FPS); // tin đầu vào từ giữa phải, không bắt người xem chờ

  return (
    <AbsoluteFill>
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          bottom: day,
          height: cao,
          display: "flex",
          fontFamily: FONT_CHAY,
          translate: `0px ${(1 - vao) * (cao + day)}px`,
          borderTop: `${3 * s}px solid ${k.vien}`,
          background: k.bang,
        }}
      >
        <div
          style={{
            flex: "none",
            display: "flex",
            alignItems: "center",
            gap: 14 * s,
            padding: `0 ${24 * s}px 0 ${(doc ? 30 : 46) * s}px`,
            background: k.nhanNen,
            color: k.nhanChu,
            fontWeight: 700,
            fontSize: coChu * 0.95,
            letterSpacing: 1 * s,
            zIndex: 1,
            boxShadow: `${8 * s}px 0 ${14 * s}px rgba(0,0,0,0.35)`,
          }}
        >
          {nhan}
          {gio ? (
            <span style={{ fontWeight: 600, fontSize: coChu * 0.8, opacity: 0.85, fontVariantNumeric: "tabular-nums" }}>{gio}</span>
          ) : null}
        </div>
        <div
          style={{
            position: "relative",
            flex: 1,
            overflow: "hidden",
            maskImage: `linear-gradient(90deg, transparent 0, #000 ${40 * s}px, #000 calc(100% - ${40 * s}px), transparent 100%)`,
          }}
        >
          <div
            style={{
              position: "absolute",
              top: 0,
              bottom: 0,
              left: 0,
              display: "flex",
              alignItems: "center",
              whiteSpace: "nowrap",
              translate: `${x}px 0px`,
              color: "white",
              fontWeight: 600,
              fontSize: coChu,
            }}
          >
            {Array.from({ length: lap }).flatMap((_, i) =>
              tin.map((t, j) => (
                <span key={`${i}-${j}`} style={{ display: "inline-flex", alignItems: "center" }}>
                  {t}
                  <span
                    style={{
                      width: 12 * s,
                      height: 12 * s,
                      margin: `0 ${30 * s}px`,
                      borderRadius: "50%",
                      background: kieu === "nong" ? "#FFFFFF" : MAU.vang,
                    }}
                  />
                </span>
              )),
            )}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
