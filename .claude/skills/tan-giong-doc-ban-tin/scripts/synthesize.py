#!/usr/bin/env python3
"""Doc ban tin tieng Viet (TXT/DOCX) thanh giong noi, xuat WAV 48kHz + MP3.

Vi du:
    python synthesize.py --input ban_tin.docx --voice nam
    python synthesize.py --input ban_tin.txt --voice "Giọng của tôi" --style tin_tuc
    python synthesize.py --input ban_tin.txt --voice nu --out-dir outputs --out-name toi_20260804

Quy trinh moi doan: mo rong viet tat (normalize_vi) -> vieneu.infer() [thu vien
tu dong chuan hoa so/ngay + tu dong chia nho doan dai o tang phoneme] -> ghep
cac doan bang khoang lang -> luu WAV 48kHz -> chuyen MP3 bang ffmpeg.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import List

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
import normalize_vi  # noqa: E402
import read_script  # noqa: E402
import voices_store  # noqa: E402


def _die(message: str, code: int = 2) -> "int":
    print(f"LOI: {message}", file=sys.stderr)
    return code


def _build_output_paths(args: argparse.Namespace) -> tuple[Path, Path]:
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = args.out_name or Path(args.input).stem
    wav_path = out_dir / f"{stem}.wav"
    mp3_path = out_dir / f"{stem}.mp3"
    return wav_path, mp3_path


def _convert_to_mp3(wav_path: Path, mp3_path: Path, bitrate: str) -> bool:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        print(
            "CANH BAO: không tìm thấy 'ffmpeg' trong PATH — bỏ qua bước xuất MP3. "
            "Chỉ có file WAV. Xem INSTALL.md để cài ffmpeg.",
            file=sys.stderr,
        )
        return False
    result = subprocess.run(
        [
            ffmpeg,
            "-y",
            "-loglevel",
            "error",
            "-i",
            str(wav_path),
            "-codec:a",
            "libmp3lame",
            "-b:a",
            bitrate,
            str(mp3_path),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"CANH BAO: ffmpeg chuyển MP3 thất bại:\n{result.stderr}", file=sys.stderr)
        return False
    return True


def _main() -> int:
    parser = argparse.ArgumentParser(
        description="Tổng hợp giọng đọc bản tin tiếng Việt từ file TXT/DOCX bằng VieNeu-TTS."
    )
    parser.add_argument("--input", required=True, help="File kịch bản .txt hoặc .docx")
    parser.add_argument(
        "--voice",
        default="nam",
        help='Tên giọng: "nam"/"nu" (giọng miền Nam, phong cách tin tức, mặc định), '
        "tên một giọng dựng sẵn bất kỳ (xem references/voices.md), "
        "hoặc tên giọng bạn đã nhân bản bằng clone_voice.py",
    )
    parser.add_argument(
        "--style",
        default="tin_tuc",
        choices=["tu_nhien", "tin_tuc", "doc_truyen"],
        help="Phong cách đọc (mặc định: tin_tuc — phù hợp bản tin)",
    )
    parser.add_argument("--out-dir", default=str(voices_store.DEFAULT_OUTPUT_DIR), help="Thư mục xuất file")
    parser.add_argument("--out-name", default=None, help="Tên file xuất (không có đuôi). Mặc định: theo tên file input")
    parser.add_argument("--gap-ms", type=int, default=450, help="Khoảng lặng giữa các đoạn (mili-giây)")
    parser.add_argument("--mp3-bitrate", default="192k", help="Bitrate MP3 xuất ra")
    parser.add_argument("--no-mp3", action="store_true", help="Chỉ xuất WAV, bỏ qua bước tạo MP3")
    parser.add_argument(
        "--abbrev-dict",
        default=None,
        help="Đường dẫn tự điển viết tắt tuỳ chỉnh (mặc định: references/abbreviations.json)",
    )
    parser.add_argument(
        "--no-abbrev",
        action="store_true",
        help="Bỏ qua bước mở rộng chữ viết tắt (chỉ dùng chuẩn hoá số/ngày có sẵn của VieNeu-TTS)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)

    try:
        paragraphs = read_script.read_script(input_path)
    except read_script.ScriptReadError as exc:
        return _die(str(exc))

    print(f"Đọc kịch bản thành công: {len(paragraphs)} đoạn từ {input_path.name}")

    if not args.no_abbrev:
        try:
            rules = normalize_vi.load_rules(Path(args.abbrev_dict) if args.abbrev_dict else None)
        except normalize_vi.NormalizeError as exc:
            return _die(str(exc))
        paragraphs = [normalize_vi.expand_abbreviations(p, rules) for p in paragraphs]
        print("Đã mở rộng chữ viết tắt theo tự điển.")

    try:
        from vieneu import Vieneu
    except ImportError:
        return _die(
            "Chưa cài được thư viện 'vieneu'. Chạy: pip install vieneu\n"
            "(xem INSTALL.md trong skill này để biết lựa chọn CPU hay GPU)."
        )

    print("Đang khởi tạo VieNeu-TTS (lần đầu sẽ tải model, có thể mất vài phút)...")
    t_init = time.time()
    vieneu = Vieneu()
    print(f"Sẵn sàng sau {time.time() - t_init:.1f}s — backend: {getattr(vieneu, 'backend', '?')}")

    voices_store.load_custom_voices(vieneu)

    voice_name = voices_store.resolve_voice_name(args.voice)
    available = {name for _, name in voices_store.list_all_voice_names(vieneu)}
    if voice_name not in available:
        print(
            f"LOI: không tìm thấy giọng '{voice_name}'.\n"
            f"Các giọng hiện có: {sorted(available)}\n"
            "Xem references/voices.md để biết danh sách giọng dựng sẵn, "
            "hoặc dùng clone_voice.py để nhân bản giọng của bạn trước.",
            file=sys.stderr,
        )
        return 2

    print(f'Dùng giọng: "{voice_name}" — phong cách: {args.style}')

    sample_rate = getattr(vieneu, "sample_rate", 48000)
    import numpy as np

    gap_samples = int(sample_rate * args.gap_ms / 1000)
    silence = np.zeros(gap_samples, dtype=np.float32)

    audio_segments: List["np.ndarray"] = []
    failures: List[str] = []
    t_synth = time.time()
    for i, paragraph in enumerate(paragraphs, 1):
        preview = paragraph if len(paragraph) <= 60 else paragraph[:57] + "..."
        print(f"[{i}/{len(paragraphs)}] Đang tổng hợp: {preview}")
        try:
            audio = vieneu.infer(paragraph, voice=voice_name, style=args.style)
        except Exception as exc:  # tiếp tục các đoạn còn lại thay vì huỷ toàn bộ
            failures.append(f"Đoạn {i}: {exc}")
            print(f"  LOI ở đoạn {i}, bỏ qua và tiếp tục: {exc}", file=sys.stderr)
            continue
        audio_segments.append(np.asarray(audio, dtype=np.float32))
        if i < len(paragraphs):
            audio_segments.append(silence)

    if not audio_segments:
        return _die("Không tổng hợp được đoạn nào — xem lỗi phía trên.", code=1)

    combined = np.concatenate(audio_segments)
    synth_seconds = time.time() - t_synth
    audio_seconds = len(combined) / sample_rate
    print(
        f"Đã tổng hợp {len(paragraphs) - len(failures)}/{len(paragraphs)} đoạn "
        f"trong {synth_seconds:.1f}s (audio dài {audio_seconds:.1f}s, "
        f"RTF={synth_seconds / audio_seconds:.2f})"
    )

    wav_path, mp3_path = _build_output_paths(args)
    vieneu.save(combined, str(wav_path))
    print(f"✅ Đã lưu WAV {sample_rate} Hz: {wav_path}")

    if not args.no_mp3:
        if _convert_to_mp3(wav_path, mp3_path, args.mp3_bitrate):
            print(f"✅ Đã lưu MP3 ({args.mp3_bitrate}): {mp3_path}")

    if failures:
        print(f"\n⚠️  {len(failures)} đoạn bị lỗi và đã bị bỏ qua:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(_main())
