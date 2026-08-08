#!/usr/bin/env python3
"""Nhan ban va luu giong noi cua ban tu file WAV de dung lai trong synthesize.py.

Vi du:
    python clone_voice.py enroll --name "Giọng của tôi" --wav giong_toi.wav
    python clone_voice.py list
    python clone_voice.py remove --name "Giọng của tôi"

Giong duoc luu tai thu muc rieng cua skill (xem voices_store.CUSTOM_VOICES_FILE),
KHONG ghi vao thu muc cai dat cua goi vieneu.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
import voices_store  # noqa: E402


def _friendly_import_error() -> str:
    return (
        "Chua cai duoc thu vien 'vieneu'. Chay: pip install vieneu\n"
        "(xem INSTALL.md trong skill nay de biet lua chon CPU hay GPU)."
    )


def cmd_enroll(args: argparse.Namespace) -> int:
    wav_path = Path(args.wav)
    if not wav_path.exists():
        print(f"LOI: khong tim thay file WAV: {wav_path}", file=sys.stderr)
        return 2
    if wav_path.suffix.lower() != ".wav":
        print(
            f"CANH BAO: file '{wav_path.name}' khong co duoi .wav — VieNeu-TTS mong doi WAV, "
            "ket qua co the khong chinh xac.",
            file=sys.stderr,
        )

    try:
        from vieneu import Vieneu
    except ImportError:
        print(f"LOI: {_friendly_import_error()}", file=sys.stderr)
        return 2

    print("Đang khởi tạo VieNeu-TTS (lần đầu sẽ tải model, có thể mất vài phút)...")
    vieneu = Vieneu()
    backend = getattr(vieneu, "backend", "?")
    print(f"Backend đang chạy: {backend}")

    voices_store.load_custom_voices(vieneu)

    print(f"Đang nhân bản giọng từ: {wav_path} (denoise={not args.no_denoise})")
    try:
        vieneu.add_voice(
            args.name,
            str(wav_path),
            denoise=not args.no_denoise,
            description=args.description or f"Giọng tự nhân bản · {args.gender or '?'} · {args.region or '?'}",
            gender=args.gender or "",
            style=args.style,
            save=False,
        )
    except Exception as exc:  # thư viện có thể ném nhiều loại lỗi khác nhau tuỳ backend
        msg = str(exc)
        if "torch" in msg.lower() or "cuda" in msg.lower():
            print(
                "LOI khi nhân bản giọng — có vẻ backend hiện tại (ONNX/CPU) chưa hỗ trợ "
                "clone trên máy này. Hãy cài thêm nhóm GPU/PyTorch rồi thử lại:\n"
                "  uv sync --group gpu          (nếu clone repo)\n"
                "  hoặc: pip install torch==2.8.0 torchaudio==2.8.0 --index-url "
                "https://download.pytorch.org/whl/cu128 && pip install \"transformers==4.57.6\"\n"
                f"Chi tiết lỗi gốc: {msg}",
                file=sys.stderr,
            )
        else:
            print(f"LOI khi nhân bản giọng: {msg}", file=sys.stderr)
        return 1

    saved_path = voices_store.save_enrolled_voice(vieneu)
    print(f"✅ Đã lưu giọng '{args.name}' vào: {saved_path}")
    print(f'Dùng lại bằng: python synthesize.py --input <kịch_bản> --voice "{args.name}"')
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    voices_store.ensure_data_dirs()
    if not voices_store.CUSTOM_VOICES_FILE.exists():
        print("Chưa có giọng nào được nhân bản.")
        print(f"(sẽ được lưu tại: {voices_store.CUSTOM_VOICES_FILE})")
        return 0

    import json

    data = json.loads(voices_store.CUSTOM_VOICES_FILE.read_text(encoding="utf-8"))
    presets = data.get("presets", {})
    if not presets:
        print("Chưa có giọng nào được nhân bản.")
        return 0

    print(f"Các giọng đã nhân bản ({len(presets)}) — lưu tại {voices_store.CUSTOM_VOICES_FILE}:")
    for name, v in presets.items():
        print(f"  - {name}: {v.get('description', '')}")
    return 0


def cmd_remove(args: argparse.Namespace) -> int:
    if not voices_store.CUSTOM_VOICES_FILE.exists():
        print("Chưa có giọng nào được nhân bản — không có gì để xoá.", file=sys.stderr)
        return 1

    import json

    data = json.loads(voices_store.CUSTOM_VOICES_FILE.read_text(encoding="utf-8"))
    presets = data.get("presets", {})
    if args.name not in presets:
        print(f"LOI: không tìm thấy giọng '{args.name}'. Có: {list(presets)}", file=sys.stderr)
        return 2

    del presets[args.name]
    data["presets"] = presets
    voices_store.CUSTOM_VOICES_FILE.write_text(
        json.dumps(data, ensure_ascii=False), encoding="utf-8"
    )
    print(f"✅ Đã xoá giọng '{args.name}'.")
    return 0


def _main() -> int:
    parser = argparse.ArgumentParser(description="Nhân bản / quản lý giọng nói của bạn cho VieNeu-TTS.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_enroll = sub.add_parser("enroll", help="Nhân bản một giọng mới từ file WAV và lưu lại")
    p_enroll.add_argument("--name", required=True, help='Tên giọng, ví dụ "Giọng của tôi"')
    p_enroll.add_argument("--wav", required=True, help="Đường dẫn file WAV mẫu (khuyến nghị 3-8 giây, giọng sạch)")
    p_enroll.add_argument("--gender", choices=["nam", "nữ"], default=None, help="Giới tính (chỉ để ghi chú)")
    p_enroll.add_argument("--region", default=None, help='Vùng miền (chỉ để ghi chú), ví dụ "Nam"')
    p_enroll.add_argument(
        "--style",
        choices=["tu_nhien", "tin_tuc", "doc_truyen"],
        default="tin_tuc",
        help="Phong cách đọc mặc định khi dùng giọng này (mặc định: tin_tuc)",
    )
    p_enroll.add_argument("--description", default=None, help="Ghi chú mô tả tuỳ chọn")
    p_enroll.add_argument(
        "--no-denoise",
        action="store_true",
        help="Bỏ qua khử nhiễu (chỉ dùng nếu file WAV đã sạch sẵn)",
    )
    p_enroll.set_defaults(func=cmd_enroll)

    p_list = sub.add_parser("list", help="Liệt kê các giọng đã nhân bản")
    p_list.set_defaults(func=cmd_list)

    p_remove = sub.add_parser("remove", help="Xoá một giọng đã nhân bản")
    p_remove.add_argument("--name", required=True)
    p_remove.set_defaults(func=cmd_remove)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(_main())
