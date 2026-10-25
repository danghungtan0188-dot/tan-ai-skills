import React from "react";
import {Easing, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from "remotion";

// Màn hình ứng dụng vẽ lại dạng minh hoạ (chữ to, rõ). Riêng biểu tượng VNeID lấy từ video nguồn của người dùng.
const RED = "#c8102e";
const INK = "#1f2933";
const CORAL = "#fb7a45";
const TEAL = "#0f766e";

export type Row = {label: string; sub?: string; tapAt?: number};
export type Scene =
  | {kind: "list"; at: number; header: string; rows: Row[]}
  | {kind: "store"; at: number; typeAt: number; tapAt: number; gpAt?: number; asAt?: number}
  | {kind: "cards"; at: number; header: string; cards: {label: string; at: number}[]}
  | {kind: "login"; at: number; fillAt: number; tapAt: number; okAt: number}
  | {kind: "form"; at: number; fillAt: number; numAt: number; checkAt: number; tapAt: number; okAt: number}
  | {kind: "passcode"; at: number; fillAt: number; okAt: number}
  | {kind: "done"; at: number; header: string; title: string; lines: string[]};

const clamp = {extrapolateLeft: "clamp", extrapolateRight: "clamp"} as const;
const ease = (t: number, a: number, b: number) => interpolate(t, [a, b], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});

// vòng chạm: hiện ~0.9 s quanh thời điểm bấm
const Tap: React.FC<{t: number; at: number}> = ({t, at}) => {
  const d = t - at;
  if (d < -0.5 || d > 0.9) return null;
  const a = d < 0 ? ease(t, at - 0.5, at) : 1 - ease(t, at + 0.4, at + 0.9);
  const r = 1 + Math.max(0, d) * 0.9;
  return (
    <div style={{position: "absolute", right: 34, top: "50%", width: 56, height: 56, marginTop: -28, borderRadius: 28,
      background: "rgba(251,122,69,0.35)", border: `4px solid ${CORAL}`, opacity: a, transform: `scale(${r})`}} />
  );
};

const Header: React.FC<{text: string}> = ({text}) => (
  <div style={{background: RED, color: "#fff", padding: "34px 28px 22px", fontSize: 30, fontWeight: 800}}>{text}</div>
);

const RowView: React.FC<{row: Row; t: number}> = ({row, t}) => {
  const hot = row.tapAt !== undefined && t >= row.tapAt - 0.5;
  return (
    <div style={{position: "relative", margin: "14px 18px", padding: "22px 22px", borderRadius: 18, background: hot ? "#fff3ec" : "#fff",
      border: `3px solid ${hot ? CORAL : "#e5e7eb"}`, boxShadow: "0 4px 10px rgba(0,0,0,0.06)"}}>
      <div style={{fontSize: 30, fontWeight: 800, color: hot ? RED : INK}}>{row.label}</div>
      {row.sub ? <div style={{fontSize: 22, color: "#6b7280", marginTop: 4}}>{row.sub}</div> : null}
      <div style={{position: "absolute", right: 22, top: "50%", marginTop: -16, fontSize: 30, color: "#9ca3af"}}>›</div>
      {row.tapAt !== undefined ? <Tap t={t} at={row.tapAt} /> : null}
    </div>
  );
};

const Field: React.FC<{label: string; value: string; on: boolean}> = ({label, value, on}) => (
  <div style={{margin: "16px 22px"}}>
    <div style={{fontSize: 22, color: "#6b7280", marginBottom: 6}}>{label}</div>
    <div style={{padding: "16px 18px", borderRadius: 14, border: `3px solid ${on ? TEAL : "#d1d5db"}`, fontSize: 30, fontWeight: 700,
      color: INK, minHeight: 40, letterSpacing: 2}}>{value}</div>
  </div>
);

const Button: React.FC<{label: string; t: number; tapAt: number}> = ({label, t, tapAt}) => {
  const press = t >= tapAt && t < tapAt + 0.3 ? 0.95 : 1;
  return (
    <div style={{position: "relative", margin: "22px", padding: "20px", borderRadius: 16, background: RED, color: "#fff", textAlign: "center",
      fontSize: 30, fontWeight: 800, transform: `scale(${press})`}}>
      {label}
      <Tap t={t} at={tapAt} />
    </div>
  );
};

const Toast: React.FC<{t: number; at: number; text: string}> = ({t, at, text}) => {
  const a = ease(t, at, at + 0.35);
  return (
    <div style={{position: "absolute", left: 22, right: 22, bottom: 40, padding: "18px 20px", borderRadius: 16, background: TEAL, color: "#fff",
      fontSize: 26, fontWeight: 800, textAlign: "center", opacity: a, transform: `translateY(${(1 - a) * 30}px)`}}>
      ✓ {text}
    </div>
  );
};

const typed = (s: string, t: number, at: number, cps = 14) => s.slice(0, Math.max(0, Math.floor((t - at) * cps)));

const SceneView: React.FC<{s: Scene; t: number}> = ({s, t}) => {
  switch (s.kind) {
    case "list":
      return (
        <>
          <Header text={s.header} />
          {s.rows.map((r, i) => <RowView key={i} row={r} t={t} />)}
        </>
      );
    case "store": {
      // biểu tượng lấy từ chính video nguồn của người dùng (public/so-suc-khoe/vneid_icon.png), không vẽ lại
      const icon = staticFile("so-suc-khoe/vneid_icon.png");
      const q = typed("VNeID", t, s.typeAt, 6);
      const searching = t >= s.typeAt;
      const show = ease(t, s.typeAt + 0.9, s.typeAt + 1.3);
      const prog = interpolate(t, [s.tapAt + 0.2, s.tapAt + 1.8], [0, 1], clamp);
      const tab = (name: string, at?: number) => {
        const on = at !== undefined && t >= at;
        return (
          <div key={name} style={{flex: 1, padding: "12px 0", textAlign: "center", borderRadius: 30, fontSize: 22, fontWeight: 800,
            background: on ? CORAL : "#111827", color: "#fff", transform: `scale(${on ? 1.04 : 1})`,
            boxShadow: on ? "0 6px 16px rgba(251,122,69,0.45)" : "none"}}>{name}</div>
        );
      };
      const active = s.asAt !== undefined && t >= s.asAt ? "as" : s.gpAt !== undefined && t >= s.gpAt ? "gp" : "";
      return (
        <>
          <Header text="Cửa hàng ứng dụng" />
          <div style={{display: "flex", gap: 12, margin: "18px 22px"}}>
            {tab("Google Play", active === "gp" ? s.gpAt : undefined)}
            {tab("App Store", active === "as" ? s.asAt : undefined)}
          </div>
          <Field label="Tìm kiếm" value={q ? `🔍 ${q}` : "🔍"} on={searching} />
          {!searching ? (
            <div style={{margin: "8px 22px", padding: "22px 20px", borderRadius: 24, textAlign: "center",
              background: "linear-gradient(160deg,#ecfdf5,#ffffff)", border: "3px solid #d1fae5", opacity: ease(t, s.at + 0.3, s.at + 0.8)}}>
              <div style={{fontSize: 20, fontWeight: 800, color: TEAL, letterSpacing: 1}}>ỨNG DỤNG NỔI BẬT</div>
              <Img src={icon} style={{width: 150, height: 150, margin: "16px auto 10px", display: "block",
                filter: "drop-shadow(0 10px 18px rgba(0,0,0,0.25))", transform: `scale(${1 + 0.03 * Math.sin(t * 2.2)})`}} />
              <div style={{fontSize: 34, fontWeight: 900, color: INK}}>VNeID</div>
              <div style={{fontSize: 22, color: "#6b7280", marginTop: 4}}>Bộ Công an</div>
              <div style={{fontSize: 20, color: TEAL, marginTop: 10, fontWeight: 700}}>Định danh điện tử</div>
            </div>
          ) : (
            <>
              <div style={{opacity: show, margin: "14px 22px", padding: 18, borderRadius: 20, border: "3px solid #e5e7eb", background: "#fff",
                display: "flex", gap: 16, alignItems: "center", transform: `translateY(${(1 - show) * 20}px)`}}>
                <Img src={icon} style={{width: 96, height: 96, filter: "drop-shadow(0 6px 10px rgba(0,0,0,0.2))"}} />
                <div style={{flex: 1}}>
                  <div style={{fontSize: 30, fontWeight: 900, color: INK}}>VNeID</div>
                  <div style={{fontSize: 22, color: "#6b7280"}}>Bộ Công an</div>
                </div>
              </div>
              <div style={{opacity: show}}>
                {prog <= 0 ? (
                  <Button label="Cài đặt / Cập nhật" t={t} tapAt={s.tapAt} />
                ) : prog < 1 ? (
                  <div style={{margin: 22}}>
                    <div style={{fontSize: 24, fontWeight: 700, color: INK, marginBottom: 10}}>Đang tải… {Math.round(prog * 100)}%</div>
                    <div style={{height: 16, borderRadius: 8, background: "#e5e7eb", overflow: "hidden"}}>
                      <div style={{width: `${prog * 100}%`, height: "100%", background: TEAL}} />
                    </div>
                  </div>
                ) : (
                  <div style={{margin: 22, padding: 20, borderRadius: 16, background: TEAL, color: "#fff", textAlign: "center", fontSize: 30, fontWeight: 800}}>
                    ✓ Mở
                  </div>
                )}
              </div>
            </>
          )}
        </>
      );
    }
    case "cards":
      return (
        <>
          <Header text={s.header} />
          {s.cards.map((c, i) => {
            const a = ease(t, c.at, c.at + 0.4);
            return (
              <div key={i} style={{margin: "22px", padding: "28px 24px", borderRadius: 20, background: "#fff", border: `3px solid ${TEAL}`,
                opacity: a, transform: `translateX(${(1 - a) * 60}px)`, display: "flex", gap: 18, alignItems: "center"}}>
                <div style={{width: 54, height: 54, borderRadius: 27, background: TEAL, color: "#fff", fontSize: 30, fontWeight: 900,
                  display: "flex", alignItems: "center", justifyContent: "center"}}>✓</div>
                <div style={{fontSize: 30, fontWeight: 800, color: INK, flex: 1}}>{c.label}</div>
              </div>
            );
          })}
        </>
      );
    case "login":
      return (
        <>
          <Header text="Đăng nhập VNeID" />
          <Field label="Số định danh cá nhân" value={typed("0xxxxxxxxxxx", t, s.fillAt)} on={t >= s.fillAt} />
          <Field label="Mật khẩu" value={"●".repeat(Math.min(8, Math.max(0, Math.floor((t - s.fillAt - 1) * 10))))} on={t >= s.fillAt + 1} />
          <Button label="Đăng nhập" t={t} tapAt={s.tapAt} />
          {t >= s.okAt ? <Toast t={t} at={s.okAt} text="Xác thực đăng nhập thành công" /> : null}
        </>
      );
    case "form":
      return (
        <>
          <Header text="Tạo mới yêu cầu" />
          <Field label="Loại thông tin" value="Thẻ BHYT" on={false} />
          <Field label="Đơn vị cấp thẻ" value={typed("Bảo hiểm xã hội Việt Nam", t, s.fillAt, 18)} on={t >= s.fillAt} />
          <Field label="Số thẻ BHYT" value={typed("••••••••••", t, s.numAt, 8)} on={t >= s.numAt} />
          <div style={{margin: "18px 22px", display: "flex", gap: 14, alignItems: "center", fontSize: 24, color: INK, fontWeight: 600}}>
            <div style={{width: 36, height: 36, borderRadius: 8, border: `3px solid ${TEAL}`, background: t >= s.checkAt ? TEAL : "#fff",
              color: "#fff", fontSize: 26, fontWeight: 900, display: "flex", alignItems: "center", justifyContent: "center"}}>{t >= s.checkAt ? "✓" : ""}</div>
            Tôi xác nhận thông tin là đúng
          </div>
          <Button label="Gửi yêu cầu" t={t} tapAt={s.tapAt} />
          {t >= s.okAt ? <Toast t={t} at={s.okAt} text="Đã gửi yêu cầu, chờ xét duyệt" /> : null}
        </>
      );
    case "passcode": {
      const n = Math.min(6, Math.max(0, Math.floor((t - s.fillAt) * 4)));
      return (
        <>
          <Header text="Nhập passcode" />
          <div style={{display: "flex", justifyContent: "center", gap: 18, margin: "60px 0 40px"}}>
            {[0, 1, 2, 3, 4, 5].map((i) => (
              <div key={i} style={{width: 34, height: 34, borderRadius: 17, border: `3px solid ${RED}`, background: i < n ? RED : "#fff"}} />
            ))}
          </div>
          <div style={{display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 14, margin: "0 40px"}}>
            {["1", "2", "3", "4", "5", "6", "7", "8", "9", "", "0", "⌫"].map((k, i) => (
              <div key={i} style={{height: 74, borderRadius: 16, background: k ? "#f3f4f6" : "transparent", fontSize: 32, fontWeight: 700,
                color: INK, display: "flex", alignItems: "center", justifyContent: "center"}}>{k}</div>
            ))}
          </div>
          {t >= s.okAt ? <Toast t={t} at={s.okAt} text="Mở Sổ sức khỏe điện tử" /> : null}
        </>
      );
    }
    case "done":
      return (
        <>
          <Header text={s.header} />
          <div style={{margin: "26px 22px", padding: 26, borderRadius: 20, background: "linear-gradient(135deg,#0f766e,#14b8a6)", color: "#fff"}}>
            <div style={{fontSize: 34, fontWeight: 900}}>{s.title}</div>
            {s.lines.map((l, i) => (
              <div key={i} style={{fontSize: 24, marginTop: 10, opacity: ease(t, s.at + 0.3 + i * 0.3, s.at + 0.6 + i * 0.3)}}>✓ {l}</div>
            ))}
          </div>
        </>
      );
  }
};

export const PhoneMock: React.FC<{scenes: Scene[]; t: number}> = ({scenes, t}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const pop = spring({frame: frame - 6, fps, config: {damping: 14, mass: 0.8}});
  const float = Math.sin(frame / fps / 1.6) * 6;
  let idx = 0;
  scenes.forEach((s, i) => {
    if (t >= s.at) idx = i;
  });
  const cur = scenes[idx];
  const slide = idx > 0 ? ease(t, cur.at, cur.at + 0.35) : 1;
  const W = 410, H = 780; // nằm gọn giữa logo (đáy y≈104) và thanh tiến trình (đỉnh y≈964)
  return (
    <div style={{position: "absolute", left: 1490 - W / 2, top: 545 - H / 2 + float, width: W, height: H, borderRadius: 60, background: "#0b0f14",
      padding: 16, boxShadow: "0 30px 60px rgba(0,0,0,0.4)", transform: `scale(${0.85 + 0.15 * pop})`, opacity: pop}}>
      <div style={{position: "relative", width: "100%", height: "100%", borderRadius: 46, overflow: "hidden", background: "#f8fafc"}}>
        <div style={{position: "absolute", top: 12, left: "50%", width: 120, height: 28, marginLeft: -60, borderRadius: 14, background: "#0b0f14", zIndex: 2}} />
        <div style={{position: "absolute", inset: 0, transform: `translateX(${(1 - slide) * 100}%)`}}>
          <SceneView s={cur} t={t} />
        </div>
      </div>
    </div>
  );
};
