import React from "react";
import {
  AbsoluteFill,
  Audio,
  Easing,
  Img,
  interpolate,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import {OUTRO_FROM, PAGES, STEP_LABELS, type Page} from "./data";
import {PhoneMock} from "./PhoneMock";

// Bảng màu: xanh ngọc y tế + cam san hô (khác hẳn bản xanh dương cũ)
const C = {
  deep: "#053f3c",
  teal: "#0f766e",
  mint: "#5eead4",
  coral: "#fb7a45",
  coralDeep: "#e4572e",
  ink: "#0b2b2a",
  white: "#ffffff",
};
const FONT = "'Segoe UI', 'Arial', sans-serif";

const useSec = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return frame / fps;
};

const ease = (t: number, a: number, b: number) =>
  interpolate(t, [a, b], [0, 1], {extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic)});

// **chữ** -> tô màu nhấn
const Rich: React.FC<{text: string}> = ({text}) => (
  <>
    {text.split(/(\*\*[^*]+\*\*)/).map((p, i) =>
      p.startsWith("**") ? (
        <span key={i} style={{color: C.coralDeep, fontWeight: 800}}>
          {p.slice(2, -2)}
        </span>
      ) : (
        <span key={i}>{p}</span>
      ),
    )}
  </>
);

const Background: React.FC = () => {
  const t = useSec();
  return (
    <AbsoluteFill style={{background: `linear-gradient(135deg, ${C.deep} 0%, ${C.teal} 58%, #0d5c56 100%)`}}>
      <div
        style={{
          position: "absolute", width: 900, height: 900, borderRadius: "50%", filter: "blur(40px)",
          background: "radial-gradient(circle, rgba(94,234,212,0.28), transparent 65%)",
          left: 1100 + 60 * Math.sin(t / 6), top: -260 + 40 * Math.cos(t / 7),
        }}
      />
      <div
        style={{
          position: "absolute", width: 700, height: 700, borderRadius: "50%", filter: "blur(50px)",
          background: "radial-gradient(circle, rgba(251,122,69,0.16), transparent 65%)",
          left: -220 + 50 * Math.cos(t / 8), top: 560 + 30 * Math.sin(t / 5),
        }}
      />
      <svg width="1920" height="1080" style={{position: "absolute", opacity: 0.07}}>
        <defs>
          <pattern id="plus" width="80" height="80" patternUnits="userSpaceOnUse" patternTransform={`translate(${(t * 6) % 80} 0)`}>
            <path d="M40 30 v20 M30 40 h20" stroke="#fff" strokeWidth="3" strokeLinecap="round" />
          </pattern>
        </defs>
        <rect width="1920" height="1080" fill="url(#plus)" />
      </svg>
    </AbsoluteFill>
  );
};

const ShieldIcon: React.FC<{size: number; draw: number}> = ({size, draw}) => (
  <svg width={size} height={size} viewBox="0 0 120 120">
    <path d="M60 8 L104 24 V58 C104 86 84 104 60 112 C36 104 16 86 16 58 V24 Z" fill={C.white} stroke={C.coral} strokeWidth="6" />
    <path d="M52 34 h16 v16 h16 v16 h-16 v16 h-16 v-16 h-16 v-16 h16 z" fill={C.coralDeep} />
    <path
      d="M10 92 h28 l8 -12 l10 20 l8 -14 h46"
      fill="none" stroke={C.teal} strokeWidth="5" strokeLinecap="round" strokeLinejoin="round"
      strokeDasharray="140" strokeDashoffset={140 * (1 - draw)}
    />
  </svg>
);

const Header: React.FC = () => (
  <div style={{position: "absolute", left: 80, top: 46, right: 80, display: "flex", alignItems: "center", gap: 20}}>
    <ShieldIcon size={62} draw={1} />
    <div style={{display: "flex", flexDirection: "column"}}>
      <span style={{color: C.mint, fontSize: 22, fontWeight: 700, letterSpacing: 3}}>HƯỚNG DẪN NHANH</span>
      <span style={{color: C.white, fontSize: 34, fontWeight: 800}}>Kích hoạt Sổ sức khỏe điện tử trên VNeID</span>
    </div>
    <div style={{flex: 1}} />
    <Img src={staticFile("so-suc-khoe/att_news.png")} style={{height: 58}} />
  </div>
);

const Progress: React.FC<{step: number; local: number}> = ({step, local}) => {
  const x0 = 260, x1 = 1660, y = 990;
  const fill = (step - 1) / 4;
  return (
    <div style={{position: "absolute", left: 0, top: 0, width: 1920, height: 1080}}>
      <div style={{position: "absolute", left: x0, top: y - 3, width: x1 - x0, height: 6, borderRadius: 3, background: "rgba(255,255,255,0.18)"}} />
      <div style={{position: "absolute", left: x0, top: y - 3, width: (x1 - x0) * fill, height: 6, borderRadius: 3, background: C.mint}} />
      {STEP_LABELS.map((lb, i) => {
        const n = i + 1;
        const done = n < step;
        const cur = n === step;
        const cx = x0 + ((x1 - x0) * i) / 4;
        const pulse = cur ? 1 + 0.08 * Math.sin(local * 5) : 1;
        return (
          <div key={lb} style={{position: "absolute", left: cx - 110, top: y - 26, width: 220, textAlign: "center"}}>
            <div
              style={{
                margin: "0 auto", width: 52, height: 52, borderRadius: 26, transform: `scale(${pulse})`,
                display: "flex", alignItems: "center", justifyContent: "center", fontWeight: 800, fontSize: 24,
                background: cur ? C.coral : done ? C.mint : "rgba(255,255,255,0.15)",
                color: cur ? C.white : done ? C.ink : "rgba(255,255,255,0.75)",
                border: `3px solid ${cur ? C.white : "transparent"}`,
                boxShadow: cur ? "0 0 24px rgba(251,122,69,0.7)" : "none",
              }}
            >
              {done ? "✓" : n}
            </div>
            <div style={{marginTop: 8, fontSize: 19, fontWeight: cur ? 800 : 600, color: cur ? C.white : "rgba(255,255,255,0.7)"}}>{lb}</div>
          </div>
        );
      })}
    </div>
  );
};

const StepPage: React.FC<{page: Page}> = ({page}) => {
  const t = useSec(); // giây tính từ đầu trang
  const {fps} = useVideoConfig();
  const frame = useCurrentFrame();
  const inA = spring({frame, fps, config: {damping: 16}});
  const outA = ease(t, page.to - page.from - 0.35, page.to - page.from);
  return (
    <AbsoluteFill style={{opacity: 1 - outA}}>
      <div style={{position: "absolute", left: 80, top: 190, width: 980, transform: `translateX(${(1 - inA) * -60}px)`, opacity: inA}}>
        <div style={{display: "flex", alignItems: "center", gap: 26}}>
          <div
            style={{
              width: 116, height: 116, borderRadius: 30, background: C.coral, color: C.white,
              display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
              boxShadow: "0 14px 30px rgba(228,87,46,0.45)", transform: `rotate(${(1 - inA) * -12}deg)`,
            }}
          >
            <span style={{fontSize: 20, fontWeight: 700, letterSpacing: 2}}>BƯỚC</span>
            <span style={{fontSize: 62, fontWeight: 900, lineHeight: 1}}>{page.step}</span>
          </div>
          <div style={{color: C.white, fontSize: 48, fontWeight: 800, lineHeight: 1.15, flex: 1}}>{page.title}</div>
        </div>
        <div
          style={{
            marginTop: 40, background: "rgba(255,255,255,0.96)", borderRadius: 28, padding: "34px 40px",
            boxShadow: "0 24px 50px rgba(0,0,0,0.25)", borderLeft: `10px solid ${C.mint}`, minHeight: 300,
          }}
        >
          {page.items.map(([text, at], i) => {
            const a = ease(t, at - page.from - 0.1, at - page.from + 0.35);
            return (
              <div
                key={i}
                style={{
                  display: "flex", gap: 18, alignItems: "flex-start", marginBottom: i < page.items.length - 1 ? 24 : 0,
                  opacity: a, transform: `translateY(${(1 - a) * 22}px)`,
                }}
              >
                <div
                  style={{
                    flex: "none", marginTop: 4, width: 38, height: 38, borderRadius: 19, background: C.teal, color: C.white,
                    display: "flex", alignItems: "center", justifyContent: "center", fontSize: 22, fontWeight: 900,
                  }}
                >
                  ✓
                </div>
                <div style={{fontSize: 36, lineHeight: 1.35, color: C.ink, fontWeight: 600}}>
                  <Rich text={text} />
                </div>
              </div>
            );
          })}
        </div>
      </div>
      <PhoneMock scenes={page.scenes} t={page.from + t} />
    </AbsoluteFill>
  );
};

const Intro: React.FC = () => {
  const t = useSec();
  const {fps} = useVideoConfig();
  const frame = useCurrentFrame();
  const icon = spring({frame, fps, config: {damping: 12}});
  const lines = [["KÍCH", "HOẠT", "SỔ", "SỨC", "KHỎE"], ["ĐIỆN", "TỬ", "TRÊN", "VNeID"]];
  const out = ease(t, 5.55, 5.95);
  return (
    <AbsoluteFill style={{alignItems: "center", justifyContent: "center", flexDirection: "column", opacity: 1 - out}}>
      <div style={{transform: `scale(${icon})`}}>
        <ShieldIcon size={170} draw={ease(t, 0.4, 1.4)} />
      </div>
      <div
        style={{
          marginTop: 26, padding: "10px 34px", borderRadius: 40, background: C.coral, color: C.white,
          fontSize: 30, fontWeight: 800, letterSpacing: 5, opacity: ease(t, 0.5, 0.9),
        }}
      >
        HƯỚNG DẪN NHANH
      </div>
      <div style={{marginTop: 26, width: 1500, textAlign: "center", fontSize: 92, fontWeight: 900, lineHeight: 1.12, color: C.white}}>
        {lines.map((line, li) => (
          <div key={li}>
            {line.map((w, j) => {
              const i = li * 5 + j;
              const a = ease(t, 0.8 + i * 0.12, 1.2 + i * 0.12);
              return (
                <span key={j} style={{display: "inline-block", margin: "0 13px", opacity: a, transform: `translateY(${(1 - a) * 40}px)`,
                  color: w === "VNeID" ? C.mint : C.white}}>
                  {w}
                </span>
              );
            })}
          </div>
        ))}
      </div>
      <div style={{marginTop: 34, display: "flex", gap: 18, alignItems: "center"}}>
        <span style={{color: C.white, fontSize: 32, fontWeight: 700, opacity: ease(t, 2.4, 2.8)}}>5 BƯỚC ĐƠN GIẢN</span>
        {[1, 2, 3, 4, 5].map((n) => {
          const a = spring({frame: frame - Math.round((2.7 + n * 0.25) * fps), fps, config: {damping: 10}});
          return (
            <div key={n} style={{width: 56, height: 56, borderRadius: 28, background: C.mint, color: C.ink, fontSize: 28, fontWeight: 900,
              display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${a})`}}>
              {n}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const Outro: React.FC = () => {
  const t = useSec();
  const {fps} = useVideoConfig();
  const frame = useCurrentFrame();
  const ring = ease(t, 0.1, 0.9);
  const tick = ease(t, 0.7, 1.2);
  return (
    <AbsoluteFill style={{alignItems: "center", justifyContent: "center", flexDirection: "column", opacity: ease(t, 0, 0.3)}}>
      <svg width="190" height="190" viewBox="0 0 190 190">
        <circle cx="95" cy="95" r="82" fill="none" stroke={C.mint} strokeWidth="12" strokeDasharray="516" strokeDashoffset={516 * (1 - ring)}
          transform="rotate(-90 95 95)" strokeLinecap="round" />
        <path d="M55 98 l28 28 l52 -58" fill="none" stroke={C.white} strokeWidth="16" strokeLinecap="round" strokeLinejoin="round"
          strokeDasharray="130" strokeDashoffset={130 * (1 - tick)} />
      </svg>
      <div style={{marginTop: 24, color: C.white, fontSize: 96, fontWeight: 900, opacity: ease(t, 0.8, 1.2)}}>HOÀN TẤT KÍCH HOẠT</div>
      <div style={{marginTop: 6, color: C.mint, fontSize: 38, fontWeight: 700, opacity: ease(t, 1.0, 1.4)}}>
        Sổ sức khỏe điện tử đã sẵn sàng trên VNeID
      </div>
      <div style={{marginTop: 40, display: "flex", gap: 16}}>
        {STEP_LABELS.map((lb, i) => {
          const a = spring({frame: frame - Math.round((1.3 + i * 0.18) * fps), fps, config: {damping: 12}});
          return (
            <div key={lb} style={{padding: "12px 24px", borderRadius: 30, background: "rgba(255,255,255,0.95)", color: C.ink,
              fontSize: 24, fontWeight: 700, transform: `scale(${a})`}}>
              <span style={{color: C.teal, fontWeight: 900}}>✓ </span>{lb}
            </div>
          );
        })}
      </div>
      <div style={{marginTop: 40, padding: "14px 40px", borderRadius: 14, background: C.coral, color: C.white, fontSize: 32, fontWeight: 800,
        opacity: ease(t, 2.4, 2.8)}}>
        Chủ động tích hợp – Sử dụng thuận tiện – Khai thác hiệu quả
      </div>
    </AbsoluteFill>
  );
};

const PageFrame: React.FC<{page: Page}> = ({page}) => {
  const t = useSec();
  return (
    <>
      <Header />
      <StepPage page={page} />
      <Progress step={page.step} local={t} />
    </>
  );
};

export const SoSucKhoe: React.FC = () => {
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{fontFamily: FONT}}>
      <Background />
      <Sequence durationInFrames={Math.round(PAGES[0].from * fps)}>
        <Intro />
      </Sequence>
      {PAGES.map((p, i) => (
        <Sequence key={i} from={Math.round(p.from * fps)} durationInFrames={Math.round((p.to - p.from) * fps)}>
          <PageFrame page={p} />
        </Sequence>
      ))}
      <Sequence from={Math.round(OUTRO_FROM * fps)}>
        <Outro />
      </Sequence>
      <Audio src={staticFile("so-suc-khoe/giong.wav")} />
    </AbsoluteFill>
  );
};
