#!/usr/bin/env python3
"""Đề xuất bỏ khoảng lặng dài và từ đệm — ĐỀ XUẤT, không tự cắt.

    # 1. xem máy đề xuất cắt chỗ nào
    python cut_silence.py VIDEO --words asr_words.json --out edit/de-xuat-cat.json

    # 2. người dùng duyệt rồi mới cắt
    python cut_silence.py VIDEO --de-xuat edit/de-xuat-cat.json --ap edit/goncut.mp4 --approved

    # 3. cắt xong PHẢI dời mốc phụ đề, nếu không phụ đề lệch hẳn
    python cut_silence.py --doi-moc edit/bilingual.json edit/anh-xa.json --out edit/bilingual2.json

Bỏ khoảng lặng không phải lúc nào cũng hay: người nói cần nhịp thở, bản tin cần khoảng ngắt
giữa hai ý. Mặc định chỉ đề xuất khoảng lặng **dài hơn `--toi-thieu`** và vẫn **giữ lại `--giu`
giây** ở mỗi chỗ. Đừng cắt sạch mọi khoảng lặng.

Từ đệm: chỉ cắt đúng từ đệm đứng riêng (`ờ`, `à`, `ừm`…). Không cắt từ nằm trong câu có nghĩa.
Máy không hiểu nghĩa — đọc bảng đề xuất rồi bỏ bớt dòng nào không nên cắt.
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
from pathlib import Path

TU_DEM = ("ờ", "à", "ừ", "ừm", "ờm", "ơ", "ể", "ìa")
DEM_TOI_DA = 1.2          # từ đệm dài hơn ngần này thường là từ có nghĩa bị nghe nhầm


def do_lang(video: str, nguong: float, toi_thieu: float) -> list[tuple[float, float]]:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", video, "-af",
                        f"silencedetect=n={nguong}dB:d={toi_thieu}", "-f", "null", "-"],
                       text=True, capture_output=True, encoding="utf-8", errors="replace")
    bd = [float(x) for x in re.findall(r"silence_start:\s*(-?[0-9.]+)", r.stderr)]
    kt = [float(x) for x in re.findall(r"silence_end:\s*([0-9.]+)", r.stderr)]
    return [(a, b) for a, b in zip(bd, kt) if b > a]


def de_xuat(lang: list[tuple[float, float]], words: list[dict], giu: float,
            tu_dem: tuple[str, ...]) -> list[dict]:
    ra = []
    for a, b in lang:
        if b - a <= giu:
            continue
        ra.append({"start": round(a + giu / 2, 2), "end": round(b - giu / 2, 2),
                   "ly_do": f"khoảng lặng {b - a:.2f}s, giữ lại {giu}s"})
    for w in words:
        t = w["w"].strip().lower().strip(".,!?")
        if t in tu_dem and w["e"] - w["s"] <= DEM_TOI_DA:
            ra.append({"start": round(w["s"] - 0.03, 2), "end": round(w["e"] + 0.03, 2),
                       "ly_do": f"từ đệm '{w['w']}'"})
    return gop(ra)


def gop(cat: list[dict]) -> list[dict]:
    """Gộp các đoạn cắt chồng nhau, nếu không ffmpeg sẽ cắt trùng."""
    ra = []
    for c in sorted(cat, key=lambda x: x["start"]):
        if ra and c["start"] <= ra[-1]["end"]:
            ra[-1]["end"] = max(ra[-1]["end"], c["end"])
            if c["ly_do"] not in ra[-1]["ly_do"]:
                ra[-1]["ly_do"] += " + " + c["ly_do"]
        else:
            ra.append(dict(c))
    return [c for c in ra if c["end"] > c["start"]]


def doan_giu(cat: list[dict], dur: float) -> list[tuple[float, float]]:
    ra, t = [], 0.0
    for c in cat:
        if c["start"] > t:
            ra.append((round(t, 3), round(min(c["start"], dur), 3)))
        t = max(t, c["end"])
    if t < dur:
        ra.append((round(t, 3), round(dur, 3)))
    return [(a, b) for a, b in ra if b - a > 0.04]


def anh_xa(giu: list[tuple[float, float]]) -> list[dict]:
    ra, moi = [], 0.0
    for a, b in giu:
        ra.append({"cu_tu": a, "cu_den": b, "moi_tu": round(moi, 3)})
        moi += b - a
    return ra


def doi_moc(t: float, ax: list[dict]) -> float:
    """Mốc cũ -> mốc mới. Mốc rơi vào đoạn bị cắt thì dồn về mép gần nhất."""
    for m in ax:
        if t < m["cu_tu"]:
            return round(m["moi_tu"], 2)
        if t <= m["cu_den"]:
            return round(m["moi_tu"] + (t - m["cu_tu"]), 2)
    cuoi = ax[-1]
    return round(cuoi["moi_tu"] + (cuoi["cu_den"] - cuoi["cu_tu"]), 2)


def cat_video(video: str, giu: list[tuple[float, float]], out: Path, preview: bool) -> list[str]:
    inputs, fc, lab = [], [], []
    for k, (a, b) in enumerate(giu):
        inputs += ["-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", video]
        fc.append(f"[{k}:v]setpts=PTS-STARTPTS[v{k}];[{k}:a]asetpts=PTS-STARTPTS[a{k}]")
        lab.append(f"[v{k}][a{k}]")
    fc.append("".join(lab) + f"concat=n={len(giu)}:v=1:a=1[vo][ao]")
    enc = ["veryfast", "27"] if preview else ["faster", "20"]
    return ["ffmpeg", "-y", "-hide_banner", "-v", "error", "-stats", *inputs,
            "-filter_complex", ";".join(fc), "-map", "[vo]", "-map", "[ao]",
            "-c:v", "libx264", "-preset", enc[0], "-crf", enc[1],
            "-c:a", "aac", "-ar", "48000", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]


def thoi_luong(p: str) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", p], text=True, capture_output=True)
    if r.returncode or not r.stdout.strip():
        raise SystemExit(f"ffprobe không đọc được {p}")
    return float(r.stdout.strip())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("video", nargs="?")
    ap.add_argument("--doi-moc", nargs=2, type=Path, metavar=("CUES", "ANH_XA"),
                    help="dời mốc phụ đề sau khi cắt, ghi ra --out")
    ap.add_argument("--words", type=Path, help="asr_words.json — để tìm từ đệm")
    ap.add_argument("--de-xuat", type=Path, help="dùng lại file đề xuất đã duyệt thay vì dò lại")
    ap.add_argument("--out", type=Path, default=Path("de-xuat-cat.json"))
    ap.add_argument("--nguong", type=float, default=-35.0, help="dBFS coi là im lặng")
    ap.add_argument("--toi-thieu", type=float, default=1.0, help="chỉ xét khoảng lặng dài hơn")
    ap.add_argument("--giu", type=float, default=0.35, help="giữ lại ngần này giây ở mỗi khoảng lặng")
    ap.add_argument("--ap", type=Path, help="cắt thật — cần --approved")
    ap.add_argument("--approved", action="store_true", help="người dùng đã duyệt bảng đề xuất")
    ap.add_argument("--preview", action="store_true")
    a = ap.parse_args()

    if a.doi_moc:
        cues_p, ax_p = a.doi_moc
        ax = json.loads(ax_p.read_text(encoding="utf-8"))
        data = json.loads(cues_p.read_text(encoding="utf-8"))
        for s in data.get("segments", []):
            s["start"], s["end"] = doi_moc(s["start"], ax), doi_moc(s["end"], ax)
        data.setdefault("meta", {})["needs_review"] = True
        a.out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{len(data.get('segments', []))} cue đã dời mốc -> {a.out}. Xem lại đồng bộ bằng mắt.")
        return 0
    if not a.video:
        raise SystemExit("Cần đường dẫn video")
    if not Path(a.video).exists():
        raise SystemExit(f"Không thấy video: {a.video}")
    if a.ap and not a.approved:     # chặn ngay, trước khi tốn công đo
        raise SystemExit("Chưa có --approved: không tự cắt lời người nói khi người dùng chưa duyệt")

    if a.de_xuat:
        cat = gop(json.loads(a.de_xuat.read_text(encoding="utf-8"))["cat"])
    else:
        words = json.loads(a.words.read_text(encoding="utf-8")) if a.words else []
        cat = de_xuat(do_lang(a.video, a.nguong, a.toi_thieu), words, a.giu, TU_DEM)
    dur = thoi_luong(a.video)
    bo = sum(c["end"] - c["start"] for c in cat)
    for c in cat:
        print(f"  {c['start']:8.2f} → {c['end']:8.2f}  ({c['end'] - c['start']:5.2f}s)  {c['ly_do']}")
    print(f"  {len(cat)} đoạn, bỏ {bo:.2f}s / {dur:.2f}s → còn {dur - bo:.2f}s")

    if not a.de_xuat:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(json.dumps({"video": a.video, "duration": dur, "cat": cat},
                                    ensure_ascii=False, indent=1), encoding="utf-8")
        print("->", a.out)
    if not a.ap:
        print("ĐỀ XUẤT. Bỏ bớt dòng không nên cắt, đưa người dùng duyệt, rồi chạy lại với --ap --approved.")
        return 0
    giu = doan_giu(cat, dur)
    if not giu:
        raise SystemExit("Cắt hết thì không còn gì — xem lại ngưỡng")
    a.ap.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(cat_video(a.video, giu, a.ap, a.preview), check=True)
    ax = a.ap.with_name("anh-xa.json")
    ax.write_text(json.dumps(anh_xa(giu), ensure_ascii=False, indent=1), encoding="utf-8")
    thuc = thoi_luong(str(a.ap))
    print(f"{a.ap}  {thuc:.2f}s (dự tính {dur - bo:.2f}s)  + {ax}")
    if abs(thuc - (dur - bo)) > 0.3:
        print("LỖI       thời lượng thật lệch dự tính — kiểm lại")
        return 1
    print("Phụ đề cũ giờ đã lệch: chạy `cut_silence.py --doi-moc` trước khi render.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
