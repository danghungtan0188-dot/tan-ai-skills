"""Dựng MP4 một lượt ffmpeg: nền (ảnh/clip/màu) + giọng đọc + phụ đề đốt vào hình.

Dùng lại render.loudnorm_linear (loudnorm 2 lượt, không bóp dải động) và render.q (escape
đường dẫn cho filter). Không bao giờ ghi đè file đầu vào; không tải media bên ngoài.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from types import SimpleNamespace

import make_bilingual_ass  # noqa: E402  (skills/bien-tap-video-thong-minh-song-ngu-tan/scripts)
import render  # noqa: E402
import video_qa  # noqa: E402  (scripts/)

SIZES = {"16:9": (1920, 1080), "9:16": (1080, 1920)}
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
VIDEO_EXT = {".mp4", ".mov", ".mkv", ".m4v", ".avi"}
FPS = 30


class VideoError(RuntimeError):
    pass


def frame_size(aspect: str, preview: bool = False) -> tuple[int, int]:
    w, h = SIZES[aspect]
    return (w // 2, h // 2) if preview else (w, h)


def write_ass(cues: list[dict], path: Path, aspect: str, font: str = "Arial") -> Path:
    """ASS một ngôn ngữ, PlayRes khớp khung hình để cỡ chữ không bị co giãn."""
    w, h = SIZES[aspect]
    size, margin = (54, 70) if aspect == "16:9" else (52, 260)
    head = (f"[Script Info]\nScriptType: v4.00+\nPlayResX: {w}\nPlayResY: {h}\nWrapStyle: 0\n"
            "ScaledBorderAndShadow: yes\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
            "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, "
            "Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            f"Style: VI,{font},{size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,"
            f"1,3,1,2,120,120,{margin},1\n\n[Events]\n"
            "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    rows = [f"Dialogue: 0,{make_bilingual_ass.ts(c['start'])},{make_bilingual_ass.ts(c['end'])},VI,,0,0,0,,"
            f"{make_bilingual_ass.esc(c['vi'])}" for c in cues]
    Path(path).write_text(head + "\n".join(rows) + "\n", encoding="utf-8")
    return Path(path)


def check_media(media: list[Path]) -> list[str]:
    errors = []
    for m in media:
        if not m.exists():
            errors.append(f"không thấy file media: {m}")
        elif m.suffix.lower() not in IMAGE_EXT | VIDEO_EXT:
            errors.append(f"định dạng chưa hỗ trợ: {m.name} (ảnh {sorted(IMAGE_EXT)}, clip {sorted(VIDEO_EXT)})")
    return errors


def build_cmd(audio: Path, ass: Path, media: list[Path], out: Path, aspect: str,
              duration: float, audio_filter: str, preset: str = "faster", preview: bool = False,
              overlays: list[dict] | None = None) -> list[str]:
    """overlays: clip đồ hoạ có alpha (do_hoa.overlays) đắp từ giây `tai`, nằm dưới phụ đề."""
    w, h = frame_size(aspect, preview)
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    chains = []
    if media:
        slot = f"{duration / len(media):.3f}"
        for i, m in enumerate(media):
            cmd += (["-loop", "1"] if m.suffix.lower() in IMAGE_EXT else ["-stream_loop", "-1"])
            cmd += ["-t", slot, "-i", str(m)]
            chains.append(f"[{i}:v]scale={w}:{h}:force_original_aspect_ratio=decrease,"
                          f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,fps={FPS},"
                          f"trim=duration={slot},setpts=PTS-STARTPTS[v{i}]")
        chains.append("".join(f"[v{i}]" for i in range(len(media))) + f"concat=n={len(media)}:v=1:a=0[bg]")
    else:
        cmd += ["-f", "lavfi", "-t", f"{duration:.3f}", "-i", f"color=c=0x0b1f3a:s={w}x{h}:r={FPS}"]
        chains.append("[0:v]null[bg]")
    n_audio = max(len(media), 1)
    cmd += ["-i", str(audio)]
    cur = "bg"
    for k, o in enumerate(overlays or []):
        cmd += ["-i", o["tep"]]
        a, b = o["tai"], o["tai"] + o["thoi_luong"]
        chains.append(f"[{n_audio + 1 + k}:v]scale={w}:{h},setpts=PTS-STARTPTS+{a:.3f}/TB[o{k}]")
        chains.append(f"[{cur}][o{k}]overlay=eof_action=pass:enable='between(t,{a:.3f},{b:.3f})'[c{k}]")
        cur = f"c{k}"
    chains.append(f"[{cur}]ass='{render.q(ass.resolve().as_posix())}',format=yuv420p[vout]")
    cmd += ["-filter_complex", ";".join(chains), "-map", "[vout]", "-map", f"{n_audio}:a",
            "-af", f"{audio_filter},aresample=48000", "-t", f"{duration:.3f}",
            "-c:v", "libx264", "-preset", "ultrafast" if preview else preset, "-crf", "30" if preview else "21",
            "-threads", "4",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-movflags", "+faststart", str(out)]
    return cmd


def render_video(audio: Path, cues: list[dict], media: list[Path], out: Path, aspect: str = "16:9",
                 preset: str = "faster", preview: bool = False, overlays: list[dict] | None = None) -> dict:
    """preview=True: nửa độ phân giải, mã hoá nhanh — để xem trước khi render bản đầy đủ."""
    if aspect not in SIZES:
        raise VideoError(f"tỉ lệ khung '{aspect}' chưa hỗ trợ, chọn {sorted(SIZES)}")
    errors = check_media(media)
    if not Path(audio).exists():
        errors.append(f"không thấy audio: {audio}")
    if errors:
        raise VideoError("; ".join(errors))
    out = Path(out)
    if out.resolve() in {Path(p).resolve() for p in [audio, *media]}:
        raise VideoError("file đầu ra trùng file đầu vào — không ghi đè tư liệu gốc")
    duration = video_qa.duration_of(Path(audio))
    ass = write_ass(cues, out.with_suffix(".ass"), aspect)
    af = render.loudnorm_linear(str(audio))
    cmd = build_cmd(Path(audio), ass, media, out, aspect, duration, af, preset, preview, overlays)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise VideoError(f"ffmpeg lỗi (exit {r.returncode}): {r.stderr.strip()[-800:]}")
    w, h = frame_size(aspect, preview)
    slot = duration / len(media) if media else duration
    timeline = {
        "khung": f"{w}x{h}", "fps": FPS, "ti_le": aspect, "xem_truoc": preview, "thoi_luong": round(duration, 3),
        "nen": [{"tep": Path(m).name, "loai": "anh" if Path(m).suffix.lower() in IMAGE_EXT else "clip",
                 "bat_dau": round(i * slot, 3), "ket_thuc": round((i + 1) * slot, 3),
                 "cach_dat": "giữ tỉ lệ, viền đen (không cắt)"} for i, m in enumerate(media)]
                or [{"loai": "mau", "mau": "#0b1f3a", "bat_dau": 0.0, "ket_thuc": round(duration, 3)}],
        "phu_de": {"so_cue": len(cues), "kieu": "ASS đốt vào hình, Arial, viền đen"},
        "do_hoa": [{"mau": o["mau"], "tep": Path(o["tep"]).name, "bat_dau": o["tai"],
                    "ket_thuc": round(o["tai"] + o["thoi_luong"], 3)} for o in overlays or []],
        "nhac_nen": None,
        "chuyen_canh": "cắt thẳng",
        "am_thanh": {"loudnorm": "2 lượt linear, -16 LUFS, TP -1.5", "sample_rate": 48000},
        "ma_hoa": {"video": "h264 yuv420p", "preset": "ultrafast" if preview else preset,
                   "crf": 30 if preview else 21, "audio": "aac 192k"},
    }
    return {"video": str(out), "ass": str(ass), "duration_audio": round(duration, 3), "command": cmd,
            "timeline": timeline}


def qa(video: Path, audio: Path) -> dict:
    """QA kỹ thuật dùng chung của repo (--strict --audio) + đối chiếu thời lượng với audio.
    Chỉ kiểm metadata/luồng/mức âm — KHÔNG đánh giá nội dung nghe nhìn."""
    return video_qa.check(SimpleNamespace(artifact=str(video), source=str(audio), cut_authorized=False,
                                          strict=True, audio=True))
