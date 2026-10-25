// Video "VNeID – một tài khoản, nhiều tiện ích": mở đầu + 5 ảnh tiện ích + lời kết, mốc theo giọng đọc (data.ts sinh từ moc.json).
// Cùng bảng màu xanh ngọc / cam san hô với bản "Kích hoạt Sổ sức khỏe điện tử" (so-suc-khoe) để hai video đi cùng bộ.
import React from "react";
import {AbsoluteFill, Audio, Easing, Img, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig} from "remotion";
import {AUDIO_FROM, INTRO_THUMBS, OUTRO_FROM, OUTRO_LOI, OUTRO_TAI, PAGES, type Page} from "./data";

const C = {deep: "#053f3c", teal: "#0f766e", mint: "#5eead4", coral: "#fb7a45", coralDeep: "#e4572e", ink: "#0b2b2a", white: "#ffffff"};
const FONT = "'Segoe UI', 'Arial', sans-serif";
const NHAN = ["Xác thực danh tính", "Thẻ BHYT", "Sổ sức khỏe", "An sinh xã hội", "Dịch vụ công"];

const useSec = () => useCurrentFrame() / useVideoConfig().fps;
const ease = (t: number, a: number, b: number) =>
  interpolate(t, [a, b], [0, 1], {extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic)});

// **chữ** -> tô màu nhấn
const Rich: React.FC<{text: string}> = ({text}) => (
  <>
    {text.split(/(\*\*[^*]+\*\*)/).map((p, i) =>
      p.startsWith("**") ? <span key={i} style={{color: C.coralDeep, fontWeight: 800}}>{p.slice(2, -2)}</span> : <span key={i}>{p}</span>,
    )}
  </>
);

const Background: React.FC = () => {
  const t = useSec();
  return (
    <AbsoluteFill style={{background: `linear-gradient(135deg, ${C.deep} 0%, ${C.teal} 58%, #0d5c56 100%)`}}>
      <div style={{position: "absolute", width: 900, height: 900, borderRadius: "50%", filter: "blur(40px)",
        background: "radial-gradient(circle, rgba(94,234,212,0.28), transparent 65%)", left: 1100 + 60 * Math.sin(t / 6), top: -260 + 40 * Math.cos(t / 7)}} />
      <div style={{position: "absolute", width: 700, height: 700, borderRadius: "50%", filter: "blur(50px)",
        background: "radial-gradient(circle, rgba(251,122,69,0.16), transparent 65%)", left: -220 + 50 * Math.cos(t / 8), top: 560 + 30 * Math.sin(t / 5)}} />
    </AbsoluteFill>
  );
};

const Header: React.FC = () => (
  <div style={{position: "absolute", left: 80, top: 40, right: 80, display: "flex", alignItems: "center", gap: 18}}>
    <Img src={staticFile("vneid-tien-ich/vneid_icon.png")} style={{height: 64}} />
    <div style={{display: "flex", flexDirection: "column"}}>
      <span style={{color: C.mint, fontSize: 22, fontWeight: 700, letterSpacing: 3}}>TIỆN ÍCH SỐ</span>
      <span style={{color: C.white, fontSize: 34, fontWeight: 800}}>VNeID – Một tài khoản, nhiều tiện ích</span>
    </div>
    <div style={{flex: 1}} />
    <Img src={staticFile("vneid-tien-ich/att_news.png")} style={{height: 58}} />
  </div>
);

const Progress: React.FC<{n: number; t: number}> = ({n, t}) => {
  const x0 = 260, x1 = 1660, y = 1000;
  return (
    <div style={{position: "absolute", left: 0, top: 0, width: 1920, height: 1080}}>
      <div style={{position: "absolute", left: x0, top: y - 3, width: x1 - x0, height: 6, borderRadius: 3, background: "rgba(255,255,255,0.18)"}} />
      <div style={{position: "absolute", left: x0, top: y - 3, width: ((x1 - x0) * (n - 1)) / 4, height: 6, borderRadius: 3, background: C.mint}} />
      {NHAN.map((lb, i) => {
        const k = i + 1, cur = k === n, done = k < n;
        const cx = x0 + ((x1 - x0) * i) / 4;
        return (
          <div key={lb} style={{position: "absolute", left: cx - 110, top: y - 24, width: 220, textAlign: "center"}}>
            <div style={{margin: "0 auto", width: 48, height: 48, borderRadius: 24, transform: `scale(${cur ? 1 + 0.08 * Math.sin(t * 5) : 1})`,
              display: "flex", alignItems: "center", justifyContent: "center", fontWeight: 800, fontSize: 22,
              background: cur ? C.coral : done ? C.mint : "rgba(255,255,255,0.15)", color: cur ? C.white : done ? C.ink : "rgba(255,255,255,0.75)",
              border: `3px solid ${cur ? C.white : "transparent"}`, boxShadow: cur ? "0 0 24px rgba(251,122,69,0.7)" : "none"}}>
              {done ? "✓" : k}
            </div>
            <div style={{marginTop: 6, fontSize: 18, fontWeight: cur ? 800 : 600, color: cur ? C.white : "rgba(255,255,255,0.7)"}}>{lb}</div>
          </div>
        );
      })}
    </div>
  );
};

// Ảnh tiện ích: thẻ bo góc, vào bằng lò xo, đẩy chậm 1,0 -> 1,05 suốt trang
const AnhTienIch: React.FC<{page: Page; t: number}> = ({page, t}) => {
  const {fps} = useVideoConfig();
  const frame = useCurrentFrame();
  const vao = spring({frame, fps, config: {damping: 15}});
  const dai = page.to - page.from;
  const rong = page.ngang ? 1080 : 740;   // anh doc 740 px: day the cach thanh buoc o duoi (y 976)
  const cao = page.ngang ? Math.round((1080 * 482) / 777) : Math.round((740 * 523) / 507);
  return (
    <div style={{position: "absolute", left: 90, top: page.ngang ? 230 : 150, width: rong, height: cao, borderRadius: 30, overflow: "hidden",
      boxShadow: "0 30px 60px rgba(0,0,0,0.35)", border: "6px solid rgba(255,255,255,0.95)",
      transform: `translateX(${(1 - vao) * -80}px) rotate(${(1 - vao) * -3}deg)`, opacity: vao}}>
      <Img src={staticFile(`vneid-tien-ich/${page.anh}`)}
        style={{width: "100%", height: "100%", objectFit: "cover", transform: `scale(${1 + 0.05 * Math.min(1, t / dai)})`}} />
    </div>
  );
};

const TrangTienIch: React.FC<{page: Page}> = ({page}) => {
  const t = useSec();
  const ra = ease(t, page.to - page.from - 0.35, page.to - page.from);
  const trai = page.ngang ? 1220 : 950;
  return (
    <AbsoluteFill style={{opacity: 1 - ra}}>
      <AnhTienIch page={page} t={t} />
      <div style={{position: "absolute", left: trai, top: 190, width: 1840 - trai}}>
        <div style={{display: "flex", alignItems: "center", gap: 22, opacity: ease(t, 0.15, 0.6)}}>
          <div style={{flex: "none", width: 100, height: 100, borderRadius: 26, background: C.coral, color: C.white, display: "flex",
            flexDirection: "column", alignItems: "center", justifyContent: "center", boxShadow: "0 14px 30px rgba(228,87,46,0.45)"}}>
            <span style={{fontSize: 17, fontWeight: 700, letterSpacing: 2}}>TIỆN ÍCH</span>
            <span style={{fontSize: 54, fontWeight: 900, lineHeight: 1}}>{page.n}</span>
          </div>
          <div style={{color: C.white, fontSize: page.ngang ? 38 : 44, fontWeight: 800, lineHeight: 1.15}}>{page.title}</div>
        </div>
        <div style={{marginTop: 34, background: "rgba(255,255,255,0.96)", borderRadius: 26, padding: "30px 34px",
          boxShadow: "0 24px 50px rgba(0,0,0,0.25)", borderLeft: `10px solid ${C.mint}`,
          opacity: ease(t, page.items[0][1] - page.from - 0.3, page.items[0][1] - page.from + 0.1)}}>
          {page.items.map(([text, at], i) => {
            const a = ease(t, at - page.from - 0.1, at - page.from + 0.35);
            return (
              <div key={i} style={{display: "flex", gap: 16, alignItems: "flex-start", marginBottom: i < page.items.length - 1 ? 22 : 0,
                opacity: a, transform: `translateY(${(1 - a) * 22}px)`}}>
                <div style={{flex: "none", marginTop: 4, width: 36, height: 36, borderRadius: 18, background: C.teal, color: C.white,
                  display: "flex", alignItems: "center", justifyContent: "center", fontSize: 20, fontWeight: 900}}>✓</div>
                <div style={{fontSize: page.ngang ? 30 : 34, lineHeight: 1.32, color: C.ink, fontWeight: 600}}><Rich text={text} /></div>
              </div>
            );
          })}
        </div>
      </div>
      <Progress n={page.n} t={t} />
    </AbsoluteFill>
  );
};

const MoDau: React.FC<{het: number}> = ({het}) => {
  const t = useSec();
  const {fps} = useVideoConfig();
  const frame = useCurrentFrame();
  const icon = spring({frame, fps, config: {damping: 12}});
  const chu = ["MỘT", "TÀI", "KHOẢN", "–", "NHIỀU", "TIỆN", "ÍCH"];
  return (
    <AbsoluteFill style={{alignItems: "center", flexDirection: "column", opacity: 1 - ease(t, het - 0.4, het)}}>
      <Img src={staticFile("vneid-tien-ich/vneid_icon.png")} style={{marginTop: 120, height: 190, transform: `scale(${icon})`}} />
      <div style={{marginTop: 20, padding: "10px 34px", borderRadius: 40, background: C.coral, color: C.white, fontSize: 30, fontWeight: 800,
        letterSpacing: 5, opacity: ease(t, 0.5, 0.9)}}>ỨNG DỤNG VNeID</div>
      <div style={{marginTop: 22, fontSize: 88, fontWeight: 900, color: C.white}}>
        {chu.map((w, i) => {
          const a = ease(t, 0.8 + i * 0.12, 1.2 + i * 0.12);
          return <span key={i} style={{display: "inline-block", margin: "0 12px", opacity: a, transform: `translateY(${(1 - a) * 40}px)`,
            color: i >= 4 ? C.mint : C.white}}>{w}</span>;
        })}
      </div>
      <div style={{marginTop: 40, display: "flex", gap: 26}}>
        {INTRO_THUMBS.map((at, i) => {
          const a = spring({frame: frame - Math.round(at * fps), fps, config: {damping: 11}});
          return (
            <div key={i} style={{width: 250, height: 190, borderRadius: 18, overflow: "hidden", border: "4px solid #fff",
              boxShadow: "0 16px 30px rgba(0,0,0,0.3)", transform: `scale(${a}) translateY(${(1 - a) * 30}px)`, opacity: a}}>
              <Img src={staticFile(`vneid-tien-ich/anh${i + 1}.png`)} style={{width: "100%", height: "100%", objectFit: "cover", objectPosition: "top"}} />
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const LoiKet: React.FC<{tai: number[]; loi: number[]}> = ({tai, loi}) => {
  const t = useSec();
  const {fps} = useVideoConfig();
  const frame = useCurrentFrame();
  const vao = spring({frame, fps, config: {damping: 13}});
  return (
    <AbsoluteFill style={{alignItems: "center", flexDirection: "column", opacity: ease(t, 0, 0.4)}}>
      <div style={{marginTop: 150, display: "flex", gap: 20}}>
        {[1, 2, 3, 4, 5].map((k, i) => {
          const a = spring({frame: frame - Math.round((0.2 + i * 0.15) * fps), fps, config: {damping: 12}});
          return (
            <div key={k} style={{width: 200, height: 150, borderRadius: 14, overflow: "hidden", border: "3px solid #fff", transform: `scale(${a})`}}>
              <Img src={staticFile(`vneid-tien-ich/anh${k}.png`)} style={{width: "100%", height: "100%", objectFit: "cover", objectPosition: "top"}} />
            </div>
          );
        })}
      </div>
      <div style={{position: "relative", width: 1500, height: 300, marginTop: 40}}>
        {/* truoc khau hieu: loi ket + khung khuyen khich (man hinh khong con trong khi doc k1-k3) */}
        <div style={{position: "absolute", inset: 0, display: "flex", flexDirection: "column", alignItems: "center",
          opacity: 1 - ease(t, tai[0] - 0.4, tai[0])}}>
          <div style={{color: C.mint, fontSize: 38, fontWeight: 800, textAlign: "center", whiteSpace: "nowrap", opacity: ease(t, loi[0], loi[0] + 0.5)}}>
            Mỗi tiện ích trên VNeID – thêm một bước thuận lợi trong cuộc sống số
          </div>
          <div style={{marginTop: 26, background: "rgba(255,255,255,0.96)", borderRadius: 24, padding: "22px 40px", borderLeft: `10px solid ${C.coral}`,
            boxShadow: "0 20px 40px rgba(0,0,0,0.25)", opacity: ease(t, loi[1] - 0.2, loi[1] + 0.3)}}>
            <div style={{fontSize: 34, fontWeight: 800, color: C.teal}}>UBND xã An Thạnh Thủy khuyến khích người dân:</div>
            {[["Chủ động **kích hoạt tài khoản định danh điện tử mức độ 2**", loi[2]], ["**Tích hợp giấy tờ, tiện ích** cần thiết để sử dụng khi có nhu cầu", loi[3]]].map(([x, at], i) => {
              const a = ease(t, (at as number) - 0.1, (at as number) + 0.35);
              return (
                <div key={i} style={{marginTop: 12, display: "flex", gap: 14, alignItems: "center", opacity: a, transform: `translateY(${(1 - a) * 18}px)`}}>
                  <div style={{flex: "none", width: 34, height: 34, borderRadius: 17, background: C.teal, color: C.white, display: "flex",
                    alignItems: "center", justifyContent: "center", fontSize: 20, fontWeight: 900}}>✓</div>
                  <div style={{fontSize: 32, color: C.ink, fontWeight: 600}}><Rich text={x as string} /></div>
                </div>
              );
            })}
          </div>
        </div>
        <div style={{position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", gap: 26,
          opacity: ease(t, tai[0], tai[0] + 0.5)}}>
          <Img src={staticFile("vneid-tien-ich/vneid_icon.png")} style={{height: 130, transform: `scale(${vao})`}} />
          <div style={{color: C.white, fontSize: 84, fontWeight: 900, lineHeight: 1.05}}>
            VNeID<br /><span style={{color: C.mint, fontSize: 56}}>Một tài khoản – Nhiều tiện ích</span>
          </div>
        </div>
      </div>
      <div style={{marginTop: 44, padding: "16px 44px", borderRadius: 16, background: C.coral, color: C.white, fontSize: 36, fontWeight: 800,
        textAlign: "center", opacity: ease(t, tai[1], tai[1] + 0.5), transform: `translateY(${(1 - ease(t, tai[1], tai[1] + 0.5)) * 20}px)`}}>
        Vì nền hành chính hiện đại, minh bạch,<br />phục vụ Nhân dân ngày càng tốt hơn!
      </div>
      <div style={{marginTop: 34, color: "rgba(255,255,255,0.85)", fontSize: 28, fontWeight: 700, letterSpacing: 2, opacity: ease(t, tai[1] + 0.6, tai[1] + 1.2)}}>
        ỦY BAN NHÂN DÂN XÃ AN THẠNH THỦY
      </div>
    </AbsoluteFill>
  );
};

export const VneidTienIch: React.FC = () => {
  const {fps} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);
  return (
    <AbsoluteFill style={{fontFamily: FONT}}>
      <Background />
      <Sequence durationInFrames={f(PAGES[0].from)}>
        <MoDau het={PAGES[0].from} />
      </Sequence>
      {PAGES.map((p) => (
        <Sequence key={p.n} from={f(p.from)} durationInFrames={f(p.to - p.from)}>
          <Header />
          <TrangTienIch page={p} />
        </Sequence>
      ))}
      <Sequence from={f(OUTRO_FROM)}>
        <LoiKet tai={[OUTRO_TAI[0] - OUTRO_FROM, OUTRO_TAI[1] - OUTRO_FROM]} loi={OUTRO_LOI.map((x) => x - OUTRO_FROM)} />
      </Sequence>
      <Sequence from={f(AUDIO_FROM)}>
        <Audio src={staticFile("vneid-tien-ich/giong.wav")} />
      </Sequence>
    </AbsoluteFill>
  );
};

