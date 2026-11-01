#!/usr/bin/env python3
"""Dong bo toan bo skills/ (nguon chuan) sang .claude/skills/ va .agents/skills/.

Thay cho viec moi skill co mot sync_skill.py rieng — cac script cu van chay duoc,
script nay xu ly tat ca skill trong mot lan, ke ca skill moi chua co script rieng.

  python scripts/sync_skills.py --check    Kiem tra, khong ghi gi. Exit 1 neu lech.
  python scripts/sync_skills.py --force    Ghi de hai ban sao bang noi dung nguon.

Khong dung symlink de tranh rui ro tuong thich tren Windows.

--check con bao loi khi ~/.claude/skills/<ten> la BAN CHEP RIENG cua mot skill trong repo
(khong phai lien ket ve .claude/skills/<ten>): ban chep do se lech dan voi repo.
Sua bang junction: mklink /J "%USERPROFILE%\\.claude\\skills\\<ten>" "<repo>\\.claude\\skills\\<ten>"
"""

import argparse
import hashlib
import os
import shutil
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPO_ROOT / "skills"
TARGET_ROOTS = [REPO_ROOT / ".claude" / "skills", REPO_ROOT / ".agents" / "skills"]

IGNORE_NAMES = {".git", "__pycache__", "node_modules", ".venv"}
IGNORE_SUFFIXES = {".pyc", ".pyo"}


def relevant_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in IGNORE_NAMES for part in path.relative_to(root).parts):
            continue
        if path.suffix in IGNORE_SUFFIXES:
            continue
        yield path


def fingerprint(root: Path) -> str | None:
    """Hash toan bo cay thu muc: duong dan tuong doi + noi dung."""
    if not root.is_dir():
        return None
    digest = hashlib.sha256()
    for path in relevant_files(root):
        rel = path.relative_to(root).as_posix()
        digest.update(rel.encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def ignore_factory(_dir, names):
    return {n for n in names
            if n in IGNORE_NAMES or Path(n).suffix in IGNORE_SUFFIXES}


def skill_dirs() -> list[Path]:
    if not SOURCE_ROOT.is_dir():
        return []
    return sorted(p for p in SOURCE_ROOT.iterdir()
                  if p.is_dir() and (p / "SKILL.md").is_file())


def noi_dung_skill(root: Path) -> str:
    """Nhu fingerprint nhung bo file cai dat (uv.lock, *.egg-info) -- .venv da nam trong IGNORE_NAMES."""
    digest = hashlib.sha256()
    for path in relevant_files(root):
        rel = path.relative_to(root)
        if rel.as_posix() == "uv.lock" or any(p.endswith(".egg-info") for p in rel.parts):
            continue
        digest.update(rel.as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def ban_chep_rieng(skills: list[Path], home_skills: Path) -> list[str]:
    """Skill co ban chep rieng o home_skills (khong lien ket ve repo) va noi dung da lech repo.

    Ban chep con khop thi cho qua: vd. video-use giu ban cai rieng vi co .venv ben trong.
    """
    ket_qua = []
    for source in skills:
        o_home = home_skills / source.name
        if not o_home.exists():
            continue
        if Path(os.path.realpath(o_home)) == Path(os.path.realpath(TARGET_ROOTS[0] / source.name)):
            continue
        if noi_dung_skill(o_home) != noi_dung_skill(source):
            ket_qua.append(source.name)
    return ket_qua


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true",
                      help="Kiem tra trang thai dong bo, khong ghi gi")
    mode.add_argument("--force", action="store_true",
                      help="Ghi de hai ban sao bang noi dung nguon chuan")
    args = parser.parse_args()

    skills = skill_dirs()
    if not skills:
        print(f"Khong tim thay skill nao trong {SOURCE_ROOT}", file=sys.stderr)
        return 1

    out_of_sync, synced = [], 0
    for source in skills:
        source_hash = fingerprint(source)
        for target_root in TARGET_ROOTS:
            target = target_root / source.name
            label = f"{source.name} -> {target.relative_to(REPO_ROOT).as_posix()}"
            if fingerprint(target) == source_hash:
                synced += 1
                continue
            if args.check:
                state = "thieu" if not target.is_dir() else "lech noi dung"
                out_of_sync.append(f"{label}  [{state}]")
                continue
            if target.is_dir():
                shutil.rmtree(target)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source, target, ignore=ignore_factory)
            print(f"da dong bo  {label}")

    if args.check:
        print(f"Skill: {len(skills)}  |  ban sao khop: {synced}/{len(skills) * 2}")
        if out_of_sync:
            print("Chua dong bo:")
            for item in out_of_sync:
                print(f"  - {item}")
            print("Chay: python scripts/sync_skills.py --force")
            return 1
        rieng = ban_chep_rieng(skills, Path.home() / ".claude" / "skills")
        if rieng:
            print("Ban chep rieng o ~/.claude/skills da lech voi repo -- thay bang junction hoac cap nhat:")
            for ten in rieng:
                print(f"  - {ten}")
            return 1
        print("Tat ca da dong bo.")
        return 0

    print(f"Xong. {len(skills)} skill x {len(TARGET_ROOTS)} dich.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
