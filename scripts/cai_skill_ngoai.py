#!/usr/bin/env python3
"""Kiem / cai lai cac skill harness can ma khong nam trong skills/ cua repo (scripts/skills-ngoai.json).

  python scripts/cai_skill_ngoai.py --kiem       # chi doc, bao thieu gi. Exit 1 neu thieu.
  python scripts/cai_skill_ngoai.py --cai        # cai phan thieu (npx skills, npm, junction)
  python scripts/cai_skill_ngoai.py --cap-nhat   # cap nhat skill qua CLI skills + cai lai Playwright CLI dung phien ban

--cai / --cap-nhat tai goi tu npm va GitHub: chi chay khi nguoi dung dong y (guard_app se hoi).
Dung cho may moi / cai lai Windows: clone repo, chay --cai, roi --kiem.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

REPO_ROOT = Path(__file__).resolve().parents[1]
DANH_SACH = Path(__file__).resolve().parent / "skills-ngoai.json"


def doc_danh_sach() -> dict:
    return json.loads(DANH_SACH.read_text(encoding="utf-8"))


def kiem(ds: dict, home: Path, repo: Path, co_lenh=shutil.which) -> list[dict]:
    """Moi muc: {loai, ten, dat, ghi_chu}. Khong ghi gi."""
    skills = home / ".claude" / "skills"
    ra = []

    def muc(loai, ten, dat, ghi_chu=""):
        ra.append({"loai": loai, "ten": ten, "dat": bool(dat), "ghi_chu": ghi_chu})

    for goi in ds["skills_cli"]["goi"]:
        for ten in goi["skill"]:
            muc("skills-cli", ten, (skills / ten / "SKILL.md").is_file(), goi["nguon"])
    for goi in ds["npm"]:
        muc("npm", goi["lenh"], co_lenh(goi["lenh"]), f"{goi['goi']}@{goi['phien_ban']}")
        for ten in goi["skill"]:
            muc("npm-skill", ten, (skills / ten / "SKILL.md").is_file(), goi["lenh"])
    dich_repo = repo / ".claude" / "skills"
    for ten in ds["lien_ket_repo"]["skill"]:
        p = skills / ten
        dung = p.exists() and Path(os.path.realpath(p)) == Path(os.path.realpath(dich_repo / ten))
        muc("lien-ket", ten, dung, "junction ve repo" if dung else ("ban chep rieng" if p.exists() else "thieu"))
    for ten in ds["ban_cai_rieng"]["skill"]:
        muc("cai-rieng", ten, (skills / ten / "SKILL.md").is_file(), "cai tay theo install.md")
    return ra


def _chay(cmd: list[str], cwd: Path) -> bool:
    print("  $", " ".join(cmd), flush=True)
    return subprocess.run(cmd, cwd=cwd, shell=os.name == "nt" and cmd[0] in ("npx", "npm")).returncode == 0


def cai(ds: dict, thieu: list[dict], cap_nhat: bool, home: Path, repo: Path) -> int:
    loi = 0
    cli = f"skills@{ds['skills_cli']['phien_ban']}"
    for goi in ds["skills_cli"]["goi"]:
        can = [m["ten"] for m in thieu if m["loai"] == "skills-cli" and m["ghi_chu"] == goi["nguon"]]
        for ten in can:
            loi += not _chay(["npx", "-y", cli, "add", goi["nguon"], "--skill", ten, "-g", "-y"], home)
    if cap_nhat:
        tat_ca = [t for g in ds["skills_cli"]["goi"] for t in g["skill"]]
        loi += not _chay(["npx", "-y", cli, "update", "-g", "-y", *tat_ca], home)
    for goi in ds["npm"]:
        if cap_nhat or any(m["ten"] == goi["lenh"] and m["loai"] == "npm" for m in thieu):
            loi += not _chay(["npm", "install", "-g", f"{goi['goi']}@{goi['phien_ban']}"], home)
        if cap_nhat or any(m["loai"] == "npm-skill" and m["ten"] in goi["skill"] for m in thieu):
            loi += not _chay(goi["sau_khi_cai"], home)
    for m in thieu:
        if m["loai"] == "lien-ket" and m["ghi_chu"] == "thieu" and os.name == "nt":
            dich = home / ".claude" / "skills" / m["ten"]
            loi += not _chay(["cmd", "/c", "mklink", "/J", str(dich), str(repo / ".claude" / "skills" / m["ten"])], home)
        elif m["loai"] in ("lien-ket", "cai-rieng"):
            print(f"  ! {m['ten']}: {m['ghi_chu']} — xu ly tay (xem memory project_skill_toan_cuc_junction).")
    return loi


def in_bang(ket_qua: list[dict]) -> None:
    for m in ket_qua:
        print(f"  {'DAT ' if m['dat'] else 'THIEU'}  {m['loai']:<11} {m['ten']:<26} {m['ghi_chu']}")
    thieu = [m for m in ket_qua if not m["dat"]]
    print(f"\n{len(ket_qua) - len(thieu)}/{len(ket_qua)} muc dat.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    che_do = ap.add_mutually_exclusive_group(required=True)
    che_do.add_argument("--kiem", action="store_true")
    che_do.add_argument("--cai", action="store_true")
    che_do.add_argument("--cap-nhat", action="store_true")
    args = ap.parse_args()
    ds, home = doc_danh_sach(), Path.home()

    ket_qua = kiem(ds, home, REPO_ROOT)
    in_bang(ket_qua)
    thieu = [m for m in ket_qua if not m["dat"]]
    if args.kiem:
        return 1 if thieu else 0
    if not thieu and not args.cap_nhat:
        print("Khong thieu gi.")
        return 0
    loi = cai(ds, thieu, args.cap_nhat, home, REPO_ROOT)
    print("\nKiem lai:")
    sau = kiem(ds, home, REPO_ROOT)
    in_bang(sau)
    return 1 if loi or any(not m["dat"] for m in sau) else 0


if __name__ == "__main__":
    raise SystemExit(main())
