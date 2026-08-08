#!/usr/bin/env python3
"""Kiem tra moi truong truoc khi dung skill tan-giong-doc-ban-tin.

Chay: python check_env.py

In bang PASS/FAIL cho tung dieu kien can, kem lenh khac phuc cu the. Khong sua
gi ca — chi doc/kiem tra.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from typing import Callable, List, Tuple

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

CheckResult = Tuple[str, bool, str]


def check_python_version() -> CheckResult:
    major, minor = sys.version_info[:2]
    version_str = f"{major}.{minor}.{sys.version_info[2]}"
    if (major, minor) < (3, 10):
        return (
            f"Python {version_str}",
            False,
            "Cần Python ≥ 3.10. Cài Python 3.11/3.12 rồi tạo lại virtualenv.",
        )
    if (major, minor) >= (3, 13):
        return (
            f"Python {version_str}",
            True,
            "OK, nhưng Python "
            f"{major}.{minor} khá mới — nếu 'pip install vieneu' báo lỗi không "
            "tìm thấy wheel (onnxruntime/tokenizers), hãy dùng Python 3.11 hoặc "
            "3.12 thay vì bản mới nhất: uv venv --python 3.12",
        )
    return (f"Python {version_str}", True, "OK")


def check_module(module_name: str, install_hint: str) -> Callable[[], CheckResult]:
    def _check() -> CheckResult:
        try:
            mod = __import__(module_name)
        except ImportError:
            return (f"Thư viện '{module_name}'", False, f"Chưa cài. Chạy: {install_hint}")
        version = getattr(mod, "__version__", "?")
        return (f"Thư viện '{module_name}' ({version})", True, "OK")

    return _check


def check_vieneu() -> CheckResult:
    try:
        import vieneu  # noqa: F401
    except ImportError:
        return (
            "Thư viện 'vieneu'",
            False,
            "Chưa cài. Xem INSTALL.md — CPU: pip install vieneu | "
            "GPU: cài torch CUDA trước rồi pip install vieneu",
        )
    version = getattr(vieneu, "__version__", "?")
    return (f"Thư viện 'vieneu' ({version})", True, "OK")


def check_ffmpeg() -> CheckResult:
    path = shutil.which("ffmpeg")
    if not path:
        return (
            "ffmpeg (xuất MP3)",
            False,
            "Chưa có trong PATH. Cài bằng: winget install Gyan.FFmpeg  "
            "(hoặc choco install ffmpeg)",
        )
    try:
        result = subprocess.run([path, "-version"], capture_output=True, text=True, timeout=10)
        first_line = result.stdout.splitlines()[0] if result.stdout else path
    except Exception:
        first_line = path
    return (f"ffmpeg ({first_line})", True, "OK")


def check_torch_gpu() -> CheckResult:
    try:
        import torch
    except ImportError:
        return (
            "PyTorch/GPU (tuỳ chọn — chỉ cần cho nhân bản giọng)",
            True,
            "Chưa cài PyTorch — giọng dựng sẵn vẫn chạy bình thường trên CPU/ONNX. "
            "Chỉ cần cài nếu muốn nhân bản giọng của bạn và gặp lỗi thiếu torch "
            "(xem INSTALL.md, mục GPU).",
        )
    cuda_ok = torch.cuda.is_available()
    detail = "CUDA khả dụng" if cuda_ok else "đã cài nhưng KHÔNG thấy GPU CUDA (sẽ chạy chậm trên CPU qua PyTorch)"
    return (f"PyTorch {torch.__version__} ({detail})", True, "OK")


def main() -> int:
    checks: List[Callable[[], CheckResult]] = [
        check_python_version,
        check_vieneu,
        check_module("numpy", "pip install numpy"),
        check_module("soundfile", "pip install soundfile"),
        check_module("docx", "pip install python-docx"),
        check_ffmpeg,
        check_torch_gpu,
    ]

    print("=" * 70)
    print("KIỂM TRA MÔI TRƯỜNG — skill tan-giong-doc-ban-tin")
    print("=" * 70)

    all_required_ok = True
    for check in checks:
        name, ok, detail = check()
        icon = "✅" if ok else "❌"
        print(f"{icon} {name}")
        if detail and detail != "OK":
            print(f"    → {detail}")
        if not ok:
            all_required_ok = False

    print("=" * 70)
    if all_required_ok:
        print("✅ Sẵn sàng sử dụng. Chạy thử: python scripts/synthesize.py --help")
    else:
        print("❌ Còn thiếu điều kiện bắt buộc ở trên — khắc phục rồi chạy lại check_env.py.")
    print("=" * 70)
    return 0 if all_required_ok else 1


if __name__ == "__main__":
    sys.exit(main())
