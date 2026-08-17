#!/usr/bin/env python3
"""Dong bo skills/video-san-pham (nguon chuan) sang
.agents/skills/video-san-pham va .claude/skills/video-san-pham
(ban sao cho Codex/Claude Code).

Che do:
  --check   Kiem tra ba ban co dong bo hay khong, khong ghi gi ca.
  --force   Thuc hien dong bo (ghi de ban sao bang noi dung nguon chuan).

Khong dung symlink de tranh rui ro tuong thich tren Windows.
"""

import argparse
import hashlib
import shutil
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

IGNORE_NAMES = {".git", "__pycache__"}
IGNORE_SUFFIXES = {".pyc"}

SCRIPT_DIR = Path(__file__).resolve().parent
SOURCE_DIR = SCRIPT_DIR.parent  # skills/video-san-pham
REPO_ROOT = SOURCE_DIR.parent.parent  # thu muc goc repo

SKILL_NAME = "video-san-pham"

TARGETS = [
    REPO_ROOT / ".agents" / "skills" / SKILL_NAME,
    REPO_ROOT / ".claude" / "skills" / SKILL_NAME,
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sync_skill.py",
        description=(
            f"Dong bo skills/{SKILL_NAME} (nguon chuan duy nhat) sang "
            f".agents/skills/{SKILL_NAME} va .claude/skills/{SKILL_NAME}."
        ),
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check",
        action="store_true",
        help="Kiểm tra xem ba bản đã đồng bộ chưa, không ghi gì.",
    )
    mode.add_argument(
        "--force",
        action="store_true",
        help="Thực hiện đồng bộ, ghi đè bản sao đích bằng nội dung nguồn chuẩn.",
    )
    return parser


def should_ignore(path: Path) -> bool:
    if any(part in IGNORE_NAMES for part in path.parts):
        return True
    if path.suffix in IGNORE_SUFFIXES:
        return True
    return False


def build_manifest(root: Path) -> dict:
    manifest = {}
    if not root.exists():
        return manifest
    for path in root.rglob("*"):
        if should_ignore(path.relative_to(root)):
            continue
        if path.is_file():
            rel = path.relative_to(root).as_posix()
            manifest[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return manifest


def diff_manifests(source: dict, target: dict):
    source_files = set(source)
    target_files = set(target)
    missing = sorted(source_files - target_files)
    extra = sorted(target_files - source_files)
    changed = sorted(
        f for f in source_files & target_files if source[f] != target[f]
    )
    return missing, extra, changed


def print_diff(target_label: str, target_path: Path, missing, extra, changed) -> bool:
    if not target_path.exists():
        print(f"[{target_label}] CHƯA ĐỒNG BỘ — thư mục chưa tồn tại: {target_path}")
        return False
    if not missing and not extra and not changed:
        print(f"[{target_label}] ĐÃ ĐỒNG BỘ — {target_path}")
        return True

    print(f"[{target_label}] CHƯA ĐỒNG BỘ — {target_path}")
    if missing:
        print("  Thiếu file (có ở nguồn, chưa có ở bản sao):")
        for f in missing:
            print(f"    - {f}")
    if extra:
        print("  File thừa (không có ở nguồn):")
        for f in extra:
            print(f"    - {f}")
    if changed:
        print("  File khác nội dung so với nguồn:")
        for f in changed:
            print(f"    - {f}")
    return False


def safe_target_check(target: Path) -> None:
    expected_suffix = Path("skills") / SKILL_NAME
    parts = target.parts[-2:]
    if Path(*parts) != expected_suffix:
        raise RuntimeError(
            f"Đường dẫn đích không hợp lệ, từ chối thao tác để tránh xóa nhầm: {target}"
        )


def do_check() -> int:
    source_manifest = build_manifest(SOURCE_DIR)
    if not source_manifest:
        print(f"Lỗi: không đọc được nguồn chuẩn tại {SOURCE_DIR}.", file=sys.stderr)
        return 2

    all_synced = True
    labels = [f".agents/skills/{SKILL_NAME}", f".claude/skills/{SKILL_NAME}"]
    for label, target in zip(labels, TARGETS):
        target_manifest = build_manifest(target)
        missing, extra, changed = diff_manifests(source_manifest, target_manifest)
        synced = print_diff(label, target, missing, extra, changed)
        all_synced = all_synced and synced

    return 0 if all_synced else 1


def do_force() -> int:
    if not SOURCE_DIR.exists():
        print(f"Lỗi: không tìm thấy nguồn chuẩn tại {SOURCE_DIR}.", file=sys.stderr)
        return 2

    for target in TARGETS:
        safe_target_check(target)
        if target.exists():
            shutil.rmtree(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(
            SOURCE_DIR,
            target,
            ignore=shutil.ignore_patterns(*IGNORE_NAMES, "*.pyc"),
        )
        print(f"Đã đồng bộ: {target}")

    print()
    return do_check()


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.check and not args.force:
        parser.error("Cần chỉ định --check hoặc --force.")

    if args.check:
        return do_check()

    return do_force()


if __name__ == "__main__":
    sys.exit(main())
