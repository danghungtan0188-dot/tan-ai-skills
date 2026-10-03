"""Tân Studio: script tiếng Việt -> chuẩn hoá -> giọng đọc -> phụ đề -> MP4 -> QA -> học có kiểm soát.

Không viết lại skill: nạp thẳng script trong skills/ và scripts/ của repo.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

__version__ = "0.2.0"

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA = Path(__file__).resolve().parent / "data"
SKILL_DIRS = {
    "tts": REPO_ROOT / "skills" / "tan-giong-doc-ban-tin" / "scripts",
    "video": REPO_ROOT / "skills" / "bien-tap-video-thong-minh-song-ngu-tan" / "scripts",
    "qa": REPO_ROOT / "scripts",
}
for _p in SKILL_DIRS.values():
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

PARTIAL_HASH_OVER = 50 * 1024 * 1024  # media lớn: băm đầu + cuối file cho nhẹ máy

SENSITIVE = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "email"),
    (re.compile(r"(?<!\d)0\d{9,10}(?!\d)"), "số điện thoại"),
    (re.compile(r"(?<!\d)\d{12}(?!\d)"), "số CCCD"),
]


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def studio_home() -> Path:
    """Nơi lưu quy tắc phạm vi cá nhân. Đổi bằng biến môi trường TAN_STUDIO_HOME."""
    return Path(os.environ.get("TAN_STUDIO_HOME") or Path.home() / ".tan-studio")


def read_json(path: Path, default=None):
    path = Path(path)
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)
    return path


def read_jsonl(path: Path) -> list[dict]:
    path = Path(path)
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, items: list[dict]) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("".join(json.dumps(i, ensure_ascii=False) + "\n" for i in items), encoding="utf-8")


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fingerprint_file(path: Path) -> dict:
    """Nhận diện tệp mà không sao chép: kích thước, thời điểm sửa, sha256 (một phần nếu tệp lớn)."""
    path = Path(path)
    st = path.stat()
    h = hashlib.sha256()
    partial = st.st_size > PARTIAL_HASH_OVER
    with path.open("rb") as f:
        if partial:
            h.update(f.read(4 * 1024 * 1024))
            f.seek(-4 * 1024 * 1024, 2)
            h.update(f.read())
        else:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
    return {"path": str(path), "size": st.st_size,
            "mtime": datetime.fromtimestamp(st.st_mtime).astimezone().isoformat(timespec="seconds"),
            "sha256": h.hexdigest(), "sha256_mot_phan": partial}


def check_sensitive(*texts: str) -> None:
    for t in texts:
        for rx, label in SENSITIVE:
            if t and rx.search(t):
                raise ValueError(f"nội dung có vẻ chứa {label} — không lưu thông tin cá nhân")
