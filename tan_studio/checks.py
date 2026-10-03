"""Kiểm tra tự động, giải thích được, ngưỡng cấu hình được (data/nguong.json, ghi đè bằng "kiem_tra" trong dự án).

Mỗi phát hiện: {id, ma, muc_do (loi|canh_bao|thong_tin), buoc, vi_tri, ly_do, goi_y, dau_van_tay}.
`dau_van_tay` giống nhau giữa các lần chạy cho cùng một vấn đề -> đếm được lỗi tái xuất hiện.
Chỉ BÁO, không tự sửa nội dung.

Cố ý KHÔNG có (chưa phát hiện đáng tin bằng công cụ hiện có): lỗi chính tả, chuyển cảnh bất thường,
cảnh lặp, chất lượng nghe nhìn. Các mục đó cần người xem — báo cáo ghi "nội dung: chưa đánh giá".
"""

from __future__ import annotations

import hashlib
import re
import subprocess
import wave
from pathlib import Path

from . import DATA, read_json

import check_subtitles  # noqa: E402
import video_qa  # noqa: E402

DEFAULTS = {k: v for k, v in (read_json(DATA / "nguong.json") or {}).items() if not k.startswith("_")}
SEVERITY = ("loi", "canh_bao", "thong_tin")


def thresholds(override: dict | None) -> dict:
    out = dict(DEFAULTS)
    for k, v in (override or {}).items():
        out[k] = {**out[k], **v} if isinstance(out.get(k), dict) and isinstance(v, dict) else v
    return out


def finding(ma: str, muc_do: str, buoc: str, ly_do: str, goi_y: str, key: str = "", **vi_tri) -> dict:
    vi_tri = {k: v for k, v in vi_tri.items() if v is not None}
    fp = f"tu:{vi_tri['tu']}" if "tu" in vi_tri else f"{ma}:{key}"  # không chứa số đo -> ổn định giữa các lần chạy
    fid = hashlib.sha1(f"{ma}|{key}|{sorted(vi_tri.items())}".encode()).hexdigest()[:8]
    return {"id": f"ph-{fid}", "ma": ma, "muc_do": muc_do, "buoc": buoc, "vi_tri": vi_tri,
            "ly_do": ly_do, "goi_y": goi_y, "dau_van_tay": fp}


def _key(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:8]


# ---------- script ----------

PLACEHOLDER = re.compile(r"\[[^\]]*\]|\{\{[^}]*\}\}|\bTODO\b|\bXXX\b|\?\?\?")


def check_script(norm: dict, t: dict) -> list[dict]:
    out = []
    for s in norm["segments"]:
        i = s["index"]
        if not s["normalized"].strip():
            out.append(finding("doan_rong", "loi", "chuan_hoa", "đoạn văn bản rỗng sau chuẩn hoá",
                               "xoá đoạn hoặc viết lại", key=str(i), doan=i))
        for m in PLACEHOLDER.finditer(s["original"]):
            out.append(finding("con_danh_dau", "loi", "chuan_hoa", f"còn chỗ đánh dấu chưa xử lý: {m.group(0)!r}",
                               "điền nội dung thật hoặc xoá đánh dấu", key=m.group(0), doan=i, doan_van=m.group(0)))
        for f in s["flags"]:
            sev = "canh_bao" if f["loai"] == "can_xem_lai" else "thong_tin"
            goi_y = ("viết lại bằng chữ, hoặc ghi lỗi phát âm để tạo quy tắc đề xuất"
                     if f["loai"] == "can_xem_lai" else "nghe lại đoạn này sau khi đọc")
            out.append(finding(f["loai"], sev, "chuan_hoa", f["ly_do"], goi_y, doan=i, tu=f["doan"]))
        for m in re.finditer(r"([,;:!?])\1+|\.{4,}", s["normalized"]):
            out.append(finding("lap_dau_cau", "canh_bao", "chuan_hoa", f"dấu câu lặp {m.group(0)!r}",
                               "giữ một dấu", key=f"{i}:{m.group(0)}", doan=i))
        for sent in re.split(r"[.!?;:,]", s["normalized"]):
            n = len(sent.split())
            if n > t["cau_toi_da_tu"]:
                out.append(finding("cau_qua_dai", "canh_bao", "chuan_hoa",
                                   f"{n} từ liền không dấu ngắt (> {t['cau_toi_da_tu']}) — giọng đọc hụt hơi, phụ đề dài",
                                   "thêm dấu phẩy/chấm ở chỗ ngắt nghĩa", key=_key(sent), doan=i,
                                   doan_van=" ".join(sent.split()[:8]) + "…"))
    return out


# ---------- audio ----------

def _read_pcm(path: Path):
    import numpy as np
    with wave.open(str(path), "rb") as w:
        if w.getsampwidth() != 2:
            return None, 0
        x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype("float32") / 32768.0
        if w.getnchannels() > 1:
            x = x.reshape(-1, w.getnchannels()).mean(axis=1)
        return x, w.getframerate()


def _analyse(x, sr: int, t: dict) -> dict:
    import numpy as np
    win = max(1, int(sr * 0.05))
    n = len(x) // win
    if n == 0:
        return {"voiced": 0.0, "rms_db": -120.0, "gaps": [], "clip": 0.0, "clip_at": None}
    frames = x[: n * win].reshape(n, win)
    db = 20 * np.log10(np.sqrt((frames ** 2).mean(axis=1)) + 1e-9)
    loud = np.where(db > t["nguong_lang_dbfs"])[0]
    clip_idx = np.where(np.abs(x) >= 0.999)[0]
    gaps, run_start = [], None
    if len(loud):
        first, last = loud[0], loud[-1]
        for k in range(first, last + 1):
            if db[k] <= t["nguong_lang_dbfs"]:
                run_start = k if run_start is None else run_start
            elif run_start is not None:
                if (k - run_start) * 0.05 >= t["lang_trong_doan_s"]:
                    gaps.append((run_start * 0.05, (k - run_start) * 0.05))
                run_start = None
        voiced = (last - first + 1) * 0.05
    else:
        voiced = 0.0
    total_db = float(20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9))
    return {"voiced": voiced, "rms_db": total_db, "gaps": gaps, "clip": len(clip_idx) / max(1, len(x)),
            "clip_at": clip_idx[0] / sr if len(clip_idx) else None}


def check_audio(tts_result: dict | None, audio: Path, t: dict) -> list[dict]:
    """Theo từng đoạn nếu có tts.json (biết chữ + mốc), không thì cả file."""
    out = []
    try:
        import numpy  # noqa: F401
    except ImportError:
        return [finding("khong_phan_tich_audio", "thong_tin", "giong_doc", "chưa cài numpy", "pip install numpy")]
    segs = (tts_result or {}).get("segments") or []
    if not segs:
        if Path(audio).suffix.lower() != ".wav":
            return [finding("khong_phan_tich_audio", "thong_tin", "giong_doc",
                            f"chỉ phân tích được WAV PCM 16-bit, audio là {Path(audio).suffix}",
                            "chuyển sang WAV nếu muốn kiểm tra audio")]
        segs = [{"index": None, "wav": str(audio), "start": 0.0, "text": None}]
    total_words, total_dur = 0, 0.0
    for s in segs:
        x, sr = _read_pcm(Path(s["wav"]))
        if x is None:
            out.append(finding("khong_phan_tich_audio", "thong_tin", "giong_doc", "WAV không phải PCM 16-bit",
                               "bỏ qua", key=str(s["index"]), doan=s["index"]))
            continue
        a = _analyse(x, sr, t)
        dur = len(x) / sr
        key = _key(s["text"] or s["wav"])
        if a["rms_db"] < t["im_lang_dbfs"]:
            out.append(finding("im_lang", "loi", "giong_doc", f"đoạn gần như im lặng ({a['rms_db']:.0f} dBFS)",
                               "đọc lại đoạn này", key=key, doan=s["index"], thoi_diem=s["start"]))
            continue
        if a["clip"] > t["clipping_ty_le"]:
            out.append(finding("clipping", "canh_bao", "giong_doc", f"{a['clip'] * 100:.2f}% mẫu bị chạm trần (vỡ tiếng)",
                               "giảm gain trước khi xuất", key=key, doan=s["index"],
                               thoi_diem=round(s["start"] + a["clip_at"], 2)))
        for g_at, g_len in a["gaps"]:
            out.append(finding("lang_bat_thuong", "canh_bao", "giong_doc",
                               f"khoảng lặng {g_len:.1f}s giữa đoạn đọc (> {t['lang_trong_doan_s']}s)",
                               "nghe lại: có thể giọng bị ngắt hoặc nuốt chữ", key=f"{key}:{g_at:.1f}",
                               doan=s["index"], thoi_diem=round(s["start"] + g_at, 2)))
        if s["text"]:
            words = len(s["text"].split())
            total_words += words
            total_dur += a["voiced"]
            rate = words / a["voiced"] if a["voiced"] else 0
            lo, hi = t["toc_do_doc"]["min"], t["toc_do_doc"]["max"]
            if not lo <= rate <= hi:
                out.append(finding("toc_do_doc", "canh_bao", "giong_doc",
                                   f"{rate:.1f} từ/giây, ngoài khoảng {lo}–{hi} — "
                                   + ("có thể đọc lặp hoặc chèn âm lạ" if rate < lo else "có thể đọc thiếu/nuốt chữ"),
                                   "nghe lại đoạn này, đọc lại nếu sai", key=key, doan=s["index"],
                                   thoi_diem=s["start"]))
    if total_words and total_dur:
        expect = total_words / t["tu_moi_giay_du_kien"]
        ratio = total_dur / expect
        lo, hi = t["thoi_luong_ty_le"]["min"], t["thoi_luong_ty_le"]["max"]
        if not lo <= ratio <= hi:
            out.append(finding("thoi_luong_lech", "canh_bao", "giong_doc",
                               f"giọng dài {total_dur:.1f}s, dự kiến ~{expect:.1f}s theo số chữ (tỉ lệ {ratio:.2f})",
                               "nghe lại toàn bài", key="tong"))
    return out


# ---------- phụ đề ----------

def check_subs(srt: Path, audio_duration: float, line_max: int, t: dict) -> list[dict]:
    cues = check_subtitles.parse(Path(srt).read_text(encoding="utf-8"), "srt")
    if not cues:
        return [finding("phu_de_trong", "loi", "phu_de", "không có cue nào", "tạo lại phụ đề", key="")]
    errors, warnings = check_subtitles.check(cues, max_chars=line_max)
    out = []
    start_of = {c["so"]: c["start"] for c in cues}
    for msgs, sev in ((errors, "loi"), (warnings, "canh_bao")):
        for m in msgs:
            n = int(re.match(r"cue (\d+)", m).group(1)) if m.startswith("cue ") else None
            out.append(finding("phu_de", sev, "phu_de", m, "sửa phu-de.srt rồi chạy lại từ bước phu_de",
                               key=f"{n}:" + re.sub(r"[\d.,]+", "#", m.split(":", 1)[-1])[:40],
                               cue=n, thoi_diem=start_of.get(n)))
    ends = [c["end"] for c in cues if c["end"] is not None]
    starts = [c["start"] for c in cues if c["start"] is not None]
    if ends and audio_duration - max(ends) > t["phu_de_lech_s"]:
        out.append(finding("phu_de_ket_thuc_som", "canh_bao", "phu_de",
                           f"phụ đề hết ở {max(ends):.1f}s, giọng dài {audio_duration:.1f}s",
                           "kiểm tra đoạn cuối có thiếu phụ đề", key="cuoi", thoi_diem=max(ends)))
    if ends and max(ends) - audio_duration > t["phu_de_lech_s"]:
        out.append(finding("phu_de_qua_dai", "loi", "phu_de",
                           f"phụ đề kéo tới {max(ends):.1f}s, giọng chỉ dài {audio_duration:.1f}s",
                           "sửa mốc thời gian trong phu-de.srt", key="cuoi", thoi_diem=audio_duration))
    if starts and min(starts) > t["phu_de_lech_s"]:
        out.append(finding("phu_de_bat_dau_muon", "canh_bao", "phu_de", f"cue đầu bắt đầu ở {min(starts):.1f}s",
                           "kiểm tra mốc cue đầu", key="dau", thoi_diem=0.0))
    return out


# ---------- video ----------

def check_video(mp4: Path, expect_w: int, expect_h: int, audio_duration: float, t: dict) -> list[dict]:
    out = []
    try:
        summary = video_qa.summarise_probe(video_qa.probe(Path(mp4)))
    except Exception as exc:
        return [finding("video_khong_mo_duoc", "loi", "dung_video", f"ffprobe không đọc được: {exc}",
                        "render lại", key="probe")]
    v, a = summary.get("video"), summary.get("audio")
    if not v:
        out.append(finding("thieu_hinh", "loi", "dung_video", "không có luồng hình", "render lại", key="v"))
    elif (v["width"], v["height"]) != (expect_w, expect_h):
        out.append(finding("sai_kich_thuoc", "loi", "dung_video",
                           f"{v['width']}x{v['height']}, cấu hình yêu cầu {expect_w}x{expect_h}",
                           "kiểm tra ti_le trong file dự án", key="kt"))
    if not a:
        out.append(finding("thieu_tieng", "loi", "dung_video", "không có luồng tiếng", "render lại", key="a"))
    drift = summary["duration"] - audio_duration
    if abs(drift) > t["video_lech_s"]:
        out.append(finding("lech_thoi_luong", "loi", "dung_video",
                           f"video {summary['duration']:.2f}s, giọng {audio_duration:.2f}s (lệch {drift:+.2f}s)",
                           "render lại", key="tl"))
    cmd = ["ffmpeg", "-hide_banner", "-nostats", "-threads", "4", "-i", str(mp4),
           "-vf", f"blackdetect=d={t['den_toi_thieu_s']}:pix_th={t['den_nguong_diem_anh']}",
           "-af", f"silencedetect=n={t['lang_video_db']}dB:d={t['lang_video_s']}", "-f", "null", "-"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    for m in re.finditer(r"black_start:([\d.]+) black_end:([\d.]+)", r.stderr):
        s, e = float(m.group(1)), float(m.group(2))
        out.append(finding("khung_den", "canh_bao", "dung_video", f"màn hình đen {e - s:.1f}s",
                           "kiểm tra tư liệu ở đoạn này", key=f"{s:.1f}", thoi_diem=round(s, 2)))
    for m in re.finditer(r"silence_start: ([\d.]+)[\s\S]*?silence_end: ([\d.]+)", r.stderr):
        s, e = float(m.group(1)), float(m.group(2))
        out.append(finding("lang_trong_video", "canh_bao", "dung_video", f"khoảng lặng {e - s:.1f}s",
                           "nghe lại đoạn này", key=f"{s:.1f}", thoi_diem=round(s, 2)))
    return out


def summary(findings: list[dict]) -> dict:
    return {sev: sum(f["muc_do"] == sev for f in findings) for sev in SEVERITY}


def describe(f: dict) -> str:
    # không chép đoạn trích văn bản (doan_van) vào báo cáo — để tắt lưu văn bản thì hồ sơ không còn script
    where = ", ".join(f"{k} {v}" for k, v in f["vi_tri"].items() if k != "doan_van")
    return f"[{f['muc_do']}] {f['ma']} ({where or 'toàn bài'}): {f['ly_do']} → {f['goi_y']}  #{f['id']}"
