#!/usr/bin/env python3
"""Tom tat nhat ky harness: hook nao chan/hoi/nhac bao nhieu lan, skill/agent/lenh nao duoc dung.

  python observability/xem.py            # 30 ngay gan nhat
  python observability/xem.py --ngay 7

Skill trong skills/ ma khong lan nao duoc goi -> liet ke rieng (ung vien gop/bo,
nhung chi ket luan khi nhat ky da du dai).
"""

import argparse
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from observability.nhat_ky import doc, thu_muc  # noqa: E402

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def tom_tat(dong: list[dict], ten_skill: list[str]) -> dict:
    hook = Counter((d.get("hook"), d.get("quyet_dinh"), d.get("ly_do")) for d in dong if d.get("loai") == "hook")
    dung = {loai: Counter(d.get("ten") for d in dong if d.get("loai") == loai) for loai in ("skill", "agent", "lenh")}
    return {"so_dong": len(dong), "hook": hook, "dung": dung,
            "skill_chua_dung": sorted(set(ten_skill) - set(dung["skill"]))}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ngay", type=int, default=30)
    args = ap.parse_args()
    ten_skill = [p.name for p in (REPO_ROOT / "skills").iterdir() if (p / "SKILL.md").is_file()]
    t = tom_tat(doc(args.ngay), ten_skill)
    print(f"Nhat ky {args.ngay} ngay: {t['so_dong']} dong ({thu_muc()})\n")
    print("HOOK (chan / hoi / nhac):")
    for (hook, qd, ly_do), n in t["hook"].most_common(20) or [(("-", "-", "chua co"), 0)]:
        print(f"  {n:>4}  {hook:<14} {qd:<5} {ly_do}")
    for loai in ("skill", "agent", "lenh"):
        print(f"\n{loai.upper()} duoc goi:")
        for ten, n in t["dung"][loai].most_common(15) or [("chua co", 0)]:
            print(f"  {n:>4}  {ten}")
    print(f"\nSkill trong repo chua lan nao duoc goi ({len(t['skill_chua_dung'])}/{len(ten_skill)}):")
    print("  " + ", ".join(t["skill_chua_dung"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
