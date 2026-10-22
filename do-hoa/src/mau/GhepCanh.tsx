// Ghép ảnh/clip thành một đoạn liền, nối bằng chuyển cảnh chính thức của Remotion (@remotion/transitions),
// tuỳ chọn vệt sáng (@remotion/light-leaks) đè lên mỗi chỗ nối. Toàn khung. Media đọc qua staticFile (--public-dir).
// Chỉ dùng các kiểu chạy bằng CSS; kiểu shader (zoom-blur, film-burn…) còn thử nghiệm nên chưa đưa vào.
import React from "react";
import { AbsoluteFill, CalculateMetadataFunction, Img, Sequence, staticFile, useVideoConfig } from "remotion";
// Video của @remotion/media giải mã bằng WebCodecs trong trình duyệt. OffthreadVideo cần remotion.exe
// (compositor), máy này bị Windows chặn chạy file đó ("spawn UNKNOWN").
import { Video } from "@remotion/media";
import { linearTiming, TransitionPresentation, TransitionSeries } from "@remotion/transitions";
import { clockWipe } from "@remotion/transitions/clock-wipe";
import { fade } from "@remotion/transitions/fade";
import { flip } from "@remotion/transitions/flip";
import { iris } from "@remotion/transitions/iris";
import { pushCut } from "@remotion/transitions/push-cut";
import { slide } from "@remotion/transitions/slide";
import { wipe } from "@remotion/transitions/wipe";
import { LightLeak } from "@remotion/light-leaks";
import { z } from "zod";
import { coBan, FPS, metadata } from "../chung";

const KIEU = ["fade", "slide", "wipe", "flip", "clockWipe", "iris", "pushCut"] as const;

export const ghepCanhSchema = coBan.extend({
  canh: z.array(z.object({ file: z.string(), giay: z.number().min(0.5) })).min(2),
  chuyen: z.array(z.enum(KIEU)).default(["fade"]), // ít hơn số chỗ nối thì lặp lại từ đầu
  chuyenGiay: z.number().min(0.1).default(0.5),
  vetSang: z.boolean().default(false),
});
type Props = z.infer<typeof ghepCanhSchema>;

// thoiLuong tự tính: tổng giây các cảnh trừ phần chồng nhau ở mỗi chỗ nối
export const ghepCanhMetadata: CalculateMetadataFunction<Props> = (opts) => {
  const p = opts.props;
  const giay = p.canh.reduce((s, c) => s + c.giay, 0) - (p.canh.length - 1) * p.chuyenGiay;
  return metadata<Props>(false)({ ...opts, props: { ...p, thoiLuong: giay } });
};

const LA_VIDEO = /\.(mp4|mov|webm|mkv|m4v)$/i;

export const GhepCanh: React.FC<Props> = ({ canh, chuyen, chuyenGiay, vetSang }) => {
  const { width, height } = useVideoConfig();
  const dai = Math.round(chuyenGiay * FPS);
  const kieu = (k: (typeof KIEU)[number]) =>
    ({
      fade: fade(),
      slide: slide({ direction: "from-right" }),
      wipe: wipe({ direction: "from-left" }),
      flip: flip(),
      clockWipe: clockWipe({ width, height }),
      iris: iris({ width, height }),
      pushCut: pushCut(),
    })[k] as TransitionPresentation<Record<string, unknown>>;

  const daySo: React.ReactNode[] = [];
  let noi = Math.round(canh[0].giay * FPS) - dai; // khung bắt đầu chỗ nối đầu tiên
  const choNoi: number[] = [];
  canh.forEach((c, i) => {
    const so = Math.round(c.giay * FPS);
    daySo.push(
      <TransitionSeries.Sequence key={`c${i}`} durationInFrames={so}>
        <AbsoluteFill style={{ background: "black" }}>
          {LA_VIDEO.test(c.file) ? (
            <Video src={staticFile(c.file)} muted objectFit="cover" style={{ width: "100%", height: "100%" }} />
          ) : (
            <Img src={staticFile(c.file)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
          )}
        </AbsoluteFill>
      </TransitionSeries.Sequence>,
    );
    if (i < canh.length - 1) {
      daySo.push(
        <TransitionSeries.Transition key={`t${i}`} presentation={kieu(chuyen[i % chuyen.length])}
          timing={linearTiming({ durationInFrames: dai })} />,
      );
      choNoi.push(noi);
      noi += Math.round(canh[i + 1].giay * FPS) - dai;
    }
  });

  return (
    <AbsoluteFill style={{ background: "black" }}>
      <TransitionSeries>{daySo}</TransitionSeries>
      {vetSang &&
        choNoi.map((f, i) => (
          <Sequence key={i} from={Math.max(0, f - dai / 2)} durationInFrames={dai * 2}>
            {/* để nguyên thì vệt sáng phủ kín khung; trộn screen cho cảnh vẫn lộ qua */}
            <AbsoluteFill style={{ mixBlendMode: "screen", opacity: 0.7 }}>
              <LightLeak seed={i} />
            </AbsoluteFill>
          </Sequence>
        ))}
    </AbsoluteFill>
  );
};
