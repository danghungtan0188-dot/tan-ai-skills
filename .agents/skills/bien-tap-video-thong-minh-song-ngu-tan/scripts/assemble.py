#!/usr/bin/env python3
"""Ghép các đoạn trong edit-plan.json thành một bản dựng thô, một lượt ffmpeg.

    python assemble.py edit-plan.json --out rough.mp4 [--rushes rushes.json]
        [--voice vo.wav] [--nat-db -12] [--size 1920x1080] [--fps 30] [--preview]

Chuẩn hoá mọi clip về cùng khung/fps/âm thanh rồi nối hard cut — nhịp bản tin là hard cut,
không chèn dissolve ở đây; muốn dissolve thì làm ở bước đồ hoạ.

Âm thanh:
- `--rushes`: cân mức từng clip bằng MỘT mức gain cố định (đo sẵn ở survey_rushes.py) để clip
  này không to hơn clip kia. Gain tĩnh — không nén, không bóp dải động.
- `--voice`: lồng lời đọc lên trên, tiếng hiện trường hạ còn `--nat-db` (mặc định −12 dB).
  Hạ bằng gain cố định, KHÔNG ducking động — tiếng hiện trường là bằng chứng sự việc, phải nghe rõ.
- Không chuẩn hoá LUFS ở đây; việc đó để render_att.py làm một lần ở cuối.

Chỉ chạy sau khi người dùng đã duyệt bảng đoạn của build_edit_plan.py.
Bước sau: render_att.py (logo, banner, phụ đề, outro) rồi qa.py.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from khuon_mau import lay_hinh, loc_hinh, loc_tieng  # noqa: E402

LUFS_CHUAN, GAIN_TOI_DA = -20.0, 12.0


def co_tieng(path: str) -> bool:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
                        "stream=codec_type", "-of", "csv=p=0", path], text=True, capture_output=True)
    return "audio" in r.stdout


def gain_clip(rushes: Path | None) -> dict[str, float]:
    if not rushes:
        return {}
    d = json.loads(rushes.read_text(encoding="utf-8"))
    return {c["file"]: max(-GAIN_TOI_DA, min(GAIN_TOI_DA, LUFS_CHUAN - c["lufs"]))
            for c in d["clips"] if c.get("lufs") is not None}


def build_cmd(plan: dict, a, tieng: dict[str, bool], gain: dict[str, float],
              khuon: dict | None = None) -> list[str]:
    W, H = (int(v) for v in a.size.split("x"))
    inputs, fc, vlab, alab = [], [], [], []
    n_in = 0                        # chỉ số input thật: clip câm chèn thêm anullsrc nên không dùng k được

    def them(args: list[str]) -> int:
        nonlocal n_in
        inputs.extend(args)
        n_in += 1
        return n_in - 1

    for k, s in enumerate(plan["segments"]):
        kieu = lay_hinh(khuon, s["hinh"]) if (khuon and s.get("hinh")) else None
        toc = float(kieu.get("toc_do", 1.0)) if kieu else 1.0
        # tốc độ khác 1 thì phải lấy nhiều/ít vật liệu hơn ở nguồn để đoạn vẫn dài đúng kế hoạch
        lay = s["dur"] * toc
        i = them(["-ss", f"{s['in']:.3f}", "-t", f"{lay:.3f}", "-i", s["file"]])
        mo = f"{loc_hinh(kieu, s['dur'], W, H, a.fps)}," if kieu else ""
        fc.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=decrease,"
                  f"pad={W}:{H}:-1:-1:color=black,setsar=1,{mo}fps={a.fps},format=yuv420p[v{k}]")
        vlab.append(f"[v{k}]")
        if tieng[s["file"]]:
            g = gain.get(s["file"], 0.0)
            vol = f"volume={g:.2f}dB," if abs(g) > 0.05 else ""
            tempo = f"{loc_tieng(kieu)}," if kieu and loc_tieng(kieu) else ""
            fc.append(f"[{i}:a]{vol}aresample=48000,aformat=channel_layouts=stereo,{tempo}"
                      f"atrim=0:{s['dur']:.3f},asetpts=PTS-STARTPTS[a{k}]")
        else:                       # clip câm: chèn im lặng đúng độ dài, nếu không concat lệch tiếng
            j = them(["-f", "lavfi", "-t", f"{s['dur']:.3f}", "-i", "anullsrc=r=48000:cl=stereo"])
            fc.append(f"[{j}:a]aresample=48000[a{k}]")
        alab.append(f"[a{k}]")
    n = len(plan["segments"])
    fc.append("".join(x + y for x, y in zip(vlab, alab)) + f"concat=n={n}:v=1:a=1[vc][ac]")
    if a.voice:
        # lời đọc ngắn hơn phim thì apad bù im lặng, dài hơn thì atrim cắt — nếu không, amix
        # kết thúc theo lời đọc và phim mất tiếng ở đuôi hoặc dài ra ngoài kế hoạch
        tong = sum(s["dur"] for s in plan["segments"])
        i = them(["-i", str(a.voice)])
        fc.append(f"[ac]volume={a.nat_db}dB[nat];"
                  f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,apad,"
                  f"atrim=0:{tong:.3f},asetpts=PTS-STARTPTS[vo];"
                  "[vo][nat]amix=inputs=2:duration=first:normalize=0[ao]")
        amap = "[ao]"
    else:
        amap = "[ac]"
    enc = ["veryfast", "27"] if a.preview else ["faster", "20"]
    return ["ffmpeg", "-y", "-hide_banner", "-v", "error", "-stats", *inputs,
            "-filter_complex", ";".join(fc), "-map", "[vc]", "-map", amap,
            "-c:v", "libx264", "-preset", enc[0], "-crf", enc[1],
            "-c:a", "aac", "-ar", "48000", "-b:a", "192k", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", str(a.out)]


def kiem_dau_ra(out: Path, tong: float, W: int, H: int, fps: int) -> list[str]:
    """Render xong ≠ xong: probe lại file thật thay vì tin vào kế hoạch."""
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration:stream=codec_type,width,height,avg_frame_rate",
                        "-of", "json", str(out)], text=True, capture_output=True, check=True)
    d = json.loads(r.stdout)
    loi = []
    thuc = float(d["format"]["duration"])
    if abs(thuc - tong) > 0.3:
        loi.append(f"thời lượng thật {thuc:.2f}s ≠ kế hoạch {tong:.2f}s")
    v = next((s for s in d["streams"] if s.get("codec_type") == "video"), None)
    if v is None or not any(s.get("codec_type") == "audio" for s in d["streams"]):
        loi.append("thiếu luồng hình hoặc tiếng")
    elif (v["width"], v["height"]) != (W, H):
        loi.append(f"khung {v['width']}x{v['height']} ≠ {W}x{H}")
    if v:
        num, den = (v.get("avg_frame_rate") or "0/1").split("/")
        if den != "0" and abs(float(num) / float(den) - fps) > 0.1:
            loi.append(f"fps {num}/{den} ≠ {fps}")
    return loi


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("plan", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--rushes", type=Path, help="để cân mức tiếng giữa các clip")
    ap.add_argument("--khuon", type=Path, help="khuon.json — để dùng kiểu chuyển động ghi trong plan")
    ap.add_argument("--voice", type=Path, help="file lời đọc lồng lên trên")
    ap.add_argument("--nat-db", type=float, default=-12.0, help="mức tiếng hiện trường khi có lời đọc")
    ap.add_argument("--size", default="1920x1080")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--preview", action="store_true")
    a = ap.parse_args()
    plan = json.loads(a.plan.read_text(encoding="utf-8"))
    if plan.get("valid") is False:
        raise SystemExit("Kế hoạch còn lỗi (valid=false) — sửa chon-canh.json rồi chạy lại build_edit_plan.py")
    if not plan.get("segments"):
        raise SystemExit("Kế hoạch không có đoạn nào")
    for ten, p in (("--voice", a.voice), ("--rushes", a.rushes), ("--khuon", a.khuon)):
        if p and not p.exists():
            raise SystemExit(f"Không thấy file {ten}: {p}")
    if plan.get("cut_authorized") is not True:
        raise SystemExit("Kế hoạch chưa được cho phép cắt ghép (cut_authorized=false). "
                         "Hãy xin duyệt hoặc tạo lại plan với --approved khi người dùng đã yêu cầu tự động dựng.")
    files = {s["file"] for s in plan["segments"]}
    thieu = [f for f in files if not Path(f).exists()]
    if thieu:
        raise SystemExit("Không thấy clip: " + ", ".join(thieu))
    a.out.parent.mkdir(parents=True, exist_ok=True)
    khuon = json.loads(a.khuon.read_text(encoding="utf-8")) if a.khuon else None
    can_khuon = [s["n"] for s in plan["segments"] if s.get("hinh") and s["hinh"] != "tinh"]
    if can_khuon and not khuon:
        raise SystemExit(f"Đoạn {can_khuon} có kiểu hình nhưng thiếu --khuon")
    cmd = build_cmd(plan, a, {f: co_tieng(f) for f in files}, gain_clip(a.rushes), khuon)
    subprocess.run(cmd, check=True)
    W, H = (int(v) for v in a.size.split("x"))
    loi = kiem_dau_ra(a.out, sum(s["dur"] for s in plan["segments"]), W, H, a.fps)
    print(f"{a.out}  ({plan['tong']}s theo kế hoạch, yêu cầu {plan['target']}s)")
    for x in loi:
        print("LỖI      ", x)
    if loi:
        return 1
    print("Đo lại file thật: khớp kế hoạch. Còn phải xem tay điểm nối giữa các đoạn, rồi qa.py --plan.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
