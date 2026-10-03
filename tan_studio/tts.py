"""Giao diện TTS chung. Thêm engine = thêm một lớp có check/info/open/synth rồi đăng ký vào ENGINES.

Mỗi đoạn được tổng hợp thành một file WAV riêng (lưu ngay, chạy lại thì bỏ qua đoạn đã có),
rồi ghép bằng khoảng lặng. Nhờ vậy biết chính xác mốc bắt đầu/kết thúc từng đoạn cho phụ đề.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import importlib.util
import math
import shutil
import struct
import subprocess
import wave
from pathlib import Path

from . import now, write_json


class EngineError(RuntimeError):
    pass


class VieneuEngine:
    """VieNeu-TTS qua thư viện `vieneu` + kho giọng của skill tan-giong-doc-ban-tin."""

    name = "vieneu"
    placeholder = False

    def check(self) -> str | None:
        for mod in ("vieneu", "soundfile", "numpy"):
            if importlib.util.find_spec(mod) is None:
                return (f"chưa cài '{mod}' — pip install vieneu soundfile "
                        "(xem skills/tan-giong-doc-ban-tin/INSTALL.md)")
        return None

    def info(self) -> dict:
        try:
            version = importlib.metadata.version("vieneu")
        except importlib.metadata.PackageNotFoundError:
            version = None
        return {"engine": self.name, "version": version, "placeholder": False}

    def open(self, voice: str, style: str) -> None:
        reason = self.check()
        if reason:
            raise EngineError(reason)
        from vieneu import Vieneu
        import voices_store

        self._tts = Vieneu()
        voices_store.load_custom_voices(self._tts)
        self.voice = voices_store.resolve_voice_name(voice)
        names = {n for _, n in voices_store.list_all_voice_names(self._tts)}
        if self.voice not in names:
            raise EngineError(f"không có giọng '{self.voice}'. Giọng hiện có: {sorted(names)}")
        self.style = style
        self.sample_rate = getattr(self._tts, "sample_rate", 48000)

    def synth(self, text: str, path: Path) -> None:
        import numpy as np
        import soundfile as sf

        audio = self._tts.infer(text, voice=self.voice, style=self.style)
        sf.write(str(path), np.asarray(audio, dtype=np.float32), self.sample_rate, subtype="PCM_16")


class ToneEngine:
    """Audio GIẢ (tiếng bíp nhỏ) dài bằng thời lượng đọc ước tính — chỉ để thử luồng video/CI.

    Không phải giọng đọc. Báo cáo luôn gắn cờ placeholder.
    """

    name = "thu-nghiem"
    placeholder = True
    sample_rate = 24000
    words_per_second = 4.8  # tốc độ đo được của giọng Minh Triết

    def check(self) -> str | None:
        return None

    def info(self) -> dict:
        return {"engine": self.name, "version": "tone-440hz", "placeholder": True}

    def open(self, voice: str, style: str) -> None:
        pass

    def synth(self, text: str, path: Path) -> None:
        seconds = max(0.8, len(text.split()) / self.words_per_second)
        n = int(seconds * self.sample_rate)
        amp = int(32767 * 0.05)
        frames = b"".join(struct.pack("<h", int(amp * math.sin(2 * math.pi * 440 * i / self.sample_rate)))
                          for i in range(n))
        with wave.open(str(path), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(self.sample_rate)
            w.writeframes(frames)


ENGINES = {"vieneu": VieneuEngine, "thu-nghiem": ToneEngine}


def get_engine(name: str):
    if name not in ENGINES:
        raise EngineError(f"không có engine '{name}'. Có: {sorted(ENGINES)}")
    return ENGINES[name]()


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as w:
        return w.getnframes() / w.getframerate()


def concat_wavs(parts: list[Path], out: Path, gap_ms: int, gaps: list[int | None] | None = None) -> list[tuple[float, float]]:
    """Ghép các WAV (cùng thông số) với khoảng lặng; trả (start, end) của từng phần.

    gaps[i] (nếu có, khác None) thay gap_ms cho khoảng lặng trước phần i (thẻ `[nghỉ ...]`)."""
    timings, cursor, params = [], 0.0, None
    with wave.open(str(out), "wb") as dst:
        for i, part in enumerate(parts):
            with wave.open(str(part), "rb") as src:
                p = src.getparams()
                if params is None:
                    params = p
                    dst.setparams(p)
                elif (p.nchannels, p.sampwidth, p.framerate) != (params.nchannels, params.sampwidth, params.framerate):
                    raise EngineError(f"{part.name} khác thông số âm thanh với đoạn đầu")
                frames = src.readframes(p.nframes)
            if i:
                ms = gaps[i] if gaps and gaps[i] is not None else gap_ms
                gap = int(params.framerate * ms / 1000)
                dst.writeframes(b"\x00" * gap * params.sampwidth * params.nchannels)
                cursor += gap / params.framerate
            dur = p.nframes / p.framerate
            timings.append((round(cursor, 3), round(cursor + dur, 3)))
            dst.writeframes(frames)
            cursor += dur
    return timings


def to_mp3(wav: Path) -> Path | None:
    if not shutil.which("ffmpeg"):
        return None
    mp3 = wav.with_suffix(".mp3")
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-c:a", "libmp3lame",
                        "-b:a", "192k", str(mp3)], capture_output=True, text=True)
    return mp3 if r.returncode == 0 else None


def synthesize(normalized: dict, out_dir: Path, engine: str = "vieneu", voice: str = "nam",
               style: str = "tin_tuc", speed: float = 1.0, gap_ms: int = 450, mp3: bool = False) -> dict:
    """Đọc mọi đoạn của NormalizedScript, ghi giong-doc.wav + tts.json vào out_dir."""
    if speed != 1.0:
        raise EngineError("chưa hỗ trợ đổi tốc độ: kéo giãn tempo làm giọng nghe máy móc — "
                          "muốn dài hơn thì tăng gap_ms")
    eng = get_engine(engine)
    reason = eng.check()
    if reason:
        raise EngineError(reason)
    out_dir = Path(out_dir)
    parts_dir = out_dir / "doan"
    parts_dir.mkdir(parents=True, exist_ok=True)

    todo = [s for s in normalized["segments"] if s["normalized"].strip()]
    jobs = []
    for seg in todo:
        key = hashlib.sha1(f"{engine}|{voice}|{style}|{seg['normalized']}".encode()).hexdigest()[:8]
        jobs.append((seg, parts_dir / f"{seg['index']:03d}_{key}.wav"))

    failures, opened = [], False
    for seg, path in jobs:
        if path.exists():
            continue
        if not opened:
            eng.open(voice, style)
            opened = True
        tmp = path.with_suffix(".tmp.wav")
        try:
            eng.synth(seg["normalized"], tmp)
            tmp.replace(path)
        except Exception as exc:  # đoạn lỗi không làm mất các đoạn khác
            failures.append({"index": seg["index"], "loi": str(exc)})
            tmp.unlink(missing_ok=True)

    done = [(seg, path) for seg, path in jobs if path.exists()]
    result = {
        "kind": "TtsResult",
        "created_at": now(),
        **eng.info(),
        "voice": voice, "style": style, "speed": speed, "gap_ms": gap_ms,
        "failures": failures,
        "segments": [],
        "audio": None,
    }
    if done:
        wav = out_dir / "giong-doc.wav"
        timings = concat_wavs([p for _, p in done], wav, gap_ms, [s.get("nghi_truoc_ms") for s, _ in done])
        with wave.open(str(wav), "rb") as w:
            result["sample_rate"] = w.getframerate()
            result["duration"] = round(w.getnframes() / w.getframerate(), 3)
        result["audio"] = str(wav)
        result["format"] = "wav"
        if mp3:
            m = to_mp3(wav)
            result["mp3"] = str(m) if m else None
        for (seg, path), (start, end) in zip(done, timings):
            result["segments"].append({"index": seg["index"], "text": seg["normalized"],
                                       "wav": str(path), "start": start, "end": end})
    write_json(out_dir / "tts.json", result)
    return result
