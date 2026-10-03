"""Lồng tiếng theo phụ đề: mỗi cue .srt/.vtt đọc thành một câu, đặt đúng mốc, ghép thành một file audio.

Câu dài hơn chỗ trống của nó, xử lý theo thứ tự:
1. lấn sang khoảng lặng trước cue sau (không đổi gì);
2. đọc nhanh hơn, tối đa `max_speed` (mặc định 1.15 — kéo tempo nhiều làm giọng máy móc);
3. vẫn không vừa thì đẩy câu sau lùi lại, và xuất `phu-de-da-chinh.srt` cho khớp giọng.
Không bao giờ cắt chữ. Mỗi câu lưu thành WAV riêng; chạy lại thì bỏ qua câu đã có.
"""

from __future__ import annotations

import hashlib
import math
import subprocess
import wave
from pathlib import Path

from . import now, write_json
from .normalize import normalize_text
from .tts import EngineError, get_engine, wav_duration

import check_subtitles  # noqa: E402  (skills/bien-tap-video-thong-minh-song-ngu-tan/scripts)
import export_subtitles  # noqa: E402

GAP_S = 0.1  # khoảng hở tối thiểu giữa hai câu khi phải đẩy lùi


def read_cues(path: Path) -> list[dict]:
    kind = "vtt" if path.suffix.lower() == ".vtt" else "srt"
    cues = check_subtitles.parse(path.read_text(encoding="utf-8"), kind)
    return [{"so": c["so"], "start": c["start"], "end": c["end"], "text": " ".join(c["lines"])}
            for c in cues if c["start"] is not None and c["lines"]]


def place(cues: list[dict], durations: list[float], max_speed: float) -> list[dict]:
    """Tính mốc đặt từng câu (thuần số, không đụng audio). durations: độ dài câu ở tốc độ 1.0."""
    plan, cursor = [], 0.0
    for i, (c, dur) in enumerate(zip(cues, durations)):
        start = max(c["start"], cursor)
        limit = cues[i + 1]["start"] if i + 1 < len(cues) else math.inf
        slot = limit - start
        speed = 1.0
        if dur > slot:
            speed = max_speed if slot <= 0 else min(dur / slot, max_speed)
        end = start + dur / speed
        plan.append({"so": c["so"], "text": c["text"], "goc": [c["start"], c["end"]],
                     "start": round(start, 3), "end": round(end, 3), "toc_do": round(speed, 3),
                     "lui_s": round(start - c["start"], 3)})
        cursor = end + GAP_S if end > limit else 0.0
    return plan


def _atempo(src: Path, dst: Path, speed: float) -> None:
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-filter:a", f"atempo={speed:.4f}",
                        "-c:a", "pcm_s16le", str(dst)], capture_output=True, text=True)
    if r.returncode:
        raise EngineError(f"ffmpeg atempo lỗi: {r.stderr[-400:]}")


def _mix(parts: list[tuple[Path, float]], out: Path, total: float) -> None:
    """Đặt từng WAV (cùng thông số) vào đúng giây của một dải lặng dài `total`."""
    with wave.open(str(parts[0][0]), "rb") as w:
        params = w.getparams()
    step = params.sampwidth * params.nchannels
    buf = bytearray(int(math.ceil(total * params.framerate)) * step)
    for path, start in parts:
        with wave.open(str(path), "rb") as w:
            if (w.getnchannels(), w.getsampwidth(), w.getframerate()) != params[:3]:
                raise EngineError(f"{path.name} khác thông số âm thanh với câu đầu")
            frames = w.readframes(w.getnframes())
        off = int(round(start * params.framerate)) * step
        buf[off:off + len(frames)] = frames
    with wave.open(str(out), "wb") as w:
        w.setparams(params)
        w.writeframes(bytes(buf))


def dub(srt: Path, out_dir: Path, engine: str = "vieneu", voice: str = "nam", style: str = "tin_tuc",
        max_speed: float = 1.15, phat_am: list[dict] | None = None) -> dict:
    if not 1.0 <= max_speed <= 1.5:
        raise EngineError("max_speed phải trong khoảng 1.0–1.5")
    cues = read_cues(Path(srt))
    if not cues:
        raise EngineError(f"{srt}: không có câu phụ đề nào đọc được")
    eng = get_engine(engine)
    reason = eng.check()
    if reason:
        raise EngineError(reason)
    out_dir = Path(out_dir)
    parts_dir = out_dir / "cau"
    parts_dir.mkdir(parents=True, exist_ok=True)

    wavs, opened = [], False
    for c in cues:
        text = normalize_text(c["text"], phat_am=phat_am)["normalized"]
        key = hashlib.sha1(f"{engine}|{voice}|{style}|{text}".encode()).hexdigest()[:8]
        path = parts_dir / f"{c['so']:04d}_{key}.wav"
        if not path.exists():
            if not opened:
                eng.open(voice, style)
                opened = True
            tmp = path.with_suffix(".tmp.wav")
            eng.synth(text, tmp)
            tmp.replace(path)
        wavs.append(path)

    plan = place(cues, [wav_duration(p) for p in wavs], max_speed)
    parts = []
    for p, wav in zip(plan, wavs):
        if p["toc_do"] > 1.0:
            fast = wav.with_name(f"{wav.stem}_x{p['toc_do']:.3f}.wav")
            if not fast.exists():
                _atempo(wav, fast, p["toc_do"])
            wav = fast
            p["end"] = round(p["start"] + wav_duration(wav), 3)
        p["wav"] = str(wav)
        parts.append((wav, p["start"]))

    total = max(plan[-1]["end"], cues[-1]["end"] or 0.0)
    audio = out_dir / "long-tieng.wav"
    _mix(parts, audio, total)

    shifted = [p for p in plan if p["lui_s"] > 0]
    adjusted = None
    if shifted:
        adjusted = out_dir / "phu-de-da-chinh.srt"
        segs = []
        for i, p in enumerate(plan):
            end = max(p["end"], p["goc"][1])  # chữ hiện tới khi giọng đọc xong
            if i + 1 < len(plan):
                end = min(end, plan[i + 1]["start"])
            segs.append({"start": p["start"], "end": end, "vi": p["text"]})
        adjusted.write_text(export_subtitles.srt(segs, "vi"), encoding="utf-8")

    result = {"kind": "DubResult", "created_at": now(), **eng.info(), "voice": voice, "style": style,
              "nguon": str(srt), "max_speed": max_speed, "audio": str(audio), "duration": round(total, 3),
              "phu_de_da_chinh": str(adjusted) if adjusted else None,
              "so_cau_doc_nhanh": sum(p["toc_do"] > 1.0 for p in plan), "so_cau_bi_lui": len(shifted),
              "cau": plan}
    write_json(out_dir / "long-tieng.json", result)
    return result
