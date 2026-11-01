#!/usr/bin/env python3
"""Stop hook (cong "xong"): luot nay da sua code thi phai chay du lenh kiem cua du an.

Doc transcript tu loi nhan gan nhat cua nguoi dung. Neu co Write/Edit vao
file code -> moi lenh kiem bat buoc phai chay THANH CONG sau lan sua cuoi;
thieu lenh nao (hoac lenh do loi) -> chan mot lan (decision=block) va liet ke
dung lenh con thieu, de Claude chay hoac ghi ro NOT RUN.

Lenh kiem bat buoc, theo thu tu uu tien:
  1. muc "## Lenh kiem tra" (co dau: "## Lệnh kiểm tra") trong CLAUDE.md / AGENTS.md
     cua du an: moi dong trong khoi code la mot lenh (bo dong rong, dong "#",
     dong co <placeholder>);
  2. package.json: cac script lint / typecheck / test / build dang co;
  3. khong co gi -> chi can mot lenh test/lint/build bat ky (LENH_KIEM).

Lan thu hai (stop_hook_active) va moi loi doc transcript -> cho qua.
Xem rules/global.md (NO TEST = NO PASS).

--toan-cuc: lenh trong ~/.claude/settings.json. Dang o trong chinh repo nay
thi bo qua, vi .claude/settings.json cua repo da chay hook nay roi.
"""

import json
import os
import re
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

DUOI_CODE = {".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".css", ".scss", ".html",
             ".vue", ".svelte", ".astro", ".sql", ".ps1", ".sh", ".dart", ".kt", ".kts",
             ".swift", ".go", ".rs", ".cs", ".java", ".rb", ".php"}
CONG_CU_SUA = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
CONG_CU_LENH = {"Bash", "PowerShell"}
LENH_KIEM = re.compile(
    r"\b(unittest|pytest|vitest|jest|playwright|tsc|video_qa\.py)\b"
    r"|\b(npm|pnpm|yarn)\s+(run\s+)?(test|lint|typecheck|build)"
    r"|\b(flutter|cargo|go|dotnet)\s+test\b")
SCRIPT_KIEM = ("lint", "typecheck", "test", "build")
MUC_LENH = re.compile(r"^#{2,3}\s*(Lệnh kiểm tra|Lenh kiem tra)\s*$", re.I | re.M)
REPO = Path(__file__).resolve().parents[2]


def gon(lenh: str) -> str:
    return " ".join(lenh.split())


def lenh_trong_claude_md(goc: Path) -> list[str]:
    """Lenh trong khoi code dau tien cua muc "## Lenh kiem tra" (tim tu goc len toi .git)."""
    for thu_muc in (goc, *goc.parents):
        for ten in ("CLAUDE.md", "AGENTS.md"):
            tep = thu_muc / ten
            if not tep.is_file():
                continue
            van_ban = tep.read_text(encoding="utf-8", errors="replace")
            muc = MUC_LENH.search(van_ban)
            if not muc:
                continue
            khoi = re.search(r"```[^\n]*\n(.*?)```", van_ban[muc.end():], re.S)
            if not khoi:
                continue
            return [gon(d.split(" #")[0]) for d in khoi.group(1).splitlines()
                    if d.strip() and not d.strip().startswith("#") and "<" not in d]
        if (thu_muc / ".git").exists():
            break
    return []


def script_package_json(goc: Path) -> list[str]:
    try:
        scripts = json.loads((goc / "package.json").read_text(encoding="utf-8")).get("scripts") or {}
    except (OSError, ValueError, AttributeError):
        return []
    return [ten for ten in SCRIPT_KIEM
            if isinstance(scripts.get(ten), str) and "no test specified" not in scripts[ten]]


def da_chay(bat_buoc: str, la_script: bool, lenh: str) -> bool:
    lenh = gon(lenh)
    if not la_script:
        return bat_buoc in lenh
    return re.search(rf"\b(npm|pnpm|yarn|bun)\s+(run\s+)?{re.escape(bat_buoc)}(?![\w:-])", lenh) is not None


def la_loi_nguoi_dung(entry: dict) -> bool:
    if entry.get("type") != "user" or entry.get("isMeta"):
        return False
    content = (entry.get("message") or {}).get("content")
    if isinstance(content, str):
        return True
    return isinstance(content, list) and not any(
        isinstance(b, dict) and b.get("type") == "tool_result" for b in content)


def doc_luot(transcript: Path) -> tuple[list[str], list[str]]:
    """(file code da sua trong luot nay, cac lenh chay THANH CONG sau lan sua cuoi)."""
    da_sua: list[str] = []
    lenh_dat: list[str] = []
    cho_ket_qua: dict[str, str] = {}
    for dong in transcript.read_text(encoding="utf-8").splitlines():
        if not dong.strip():
            continue
        entry = json.loads(dong)
        if entry.get("isSidechain"):
            continue
        if la_loi_nguoi_dung(entry):
            da_sua, lenh_dat, cho_ket_qua = [], [], {}
            continue
        content = (entry.get("message") or {}).get("content") or []
        if entry.get("type") == "user" and isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_result":
                    lenh = cho_ket_qua.pop(str(block.get("tool_use_id")), None)
                    if lenh is not None and not block.get("is_error"):
                        lenh_dat.append(lenh)
            continue
        if entry.get("type") != "assistant":
            continue
        for block in content:
            if not isinstance(block, dict) or block.get("type") != "tool_use":
                continue
            ten, vao = block.get("name"), block.get("input") or {}
            if ten in CONG_CU_SUA:
                duong_dan = str(vao.get("file_path") or vao.get("notebook_path") or "")
                if Path(duong_dan).suffix.lower() in DUOI_CODE:
                    if duong_dan not in da_sua:
                        da_sua.append(duong_dan)
                    lenh_dat, cho_ket_qua = [], {}
            elif ten in CONG_CU_LENH:
                cho_ket_qua[str(block.get("id"))] = str(vao.get("command") or "")
    # Lenh chua co ket qua (vd. ket qua nam sau dong cuoi) van tinh la da chay.
    return da_sua, lenh_dat + list(cho_ket_qua.values())


def lenh_con_thieu(goc: Path, lenh_dat: list[str]) -> tuple[list[str], str]:
    """(lenh bat buoc chua chay thanh cong, nguon cua danh sach lenh)."""
    khai_bao = lenh_trong_claude_md(goc)
    if khai_bao:
        return [b for b in khai_bao if not any(da_chay(b, False, l) for l in lenh_dat)], \
            "muc 'Lenh kiem tra' trong CLAUDE.md"
    scripts = script_package_json(goc)
    if scripts:
        return [f"npm run {s}" for s in scripts
                if not any(da_chay(s, True, l) for l in lenh_dat)], "script trong package.json"
    if any(LENH_KIEM.search(l) for l in lenh_dat):
        return [], ""
    return ["lenh test/lint/build cua du an"], ""


try:
    from pathlib import Path as _P
    sys.path.insert(0, str(_P(__file__).resolve().parents[2]))
    from observability.nhat_ky import ghi_hook
except Exception:  # nhat ky la phu: loi o day khong duoc lam hong hook
    def ghi_hook(*_a, **_k):
        pass


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    if payload.get("stop_hook_active"):
        return 0
    goc = Path(payload.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
    if "--toan-cuc" in sys.argv and goc.resolve().is_relative_to(REPO):
        return 0

    try:
        da_sua, lenh_dat = doc_luot(Path(payload.get("transcript_path") or ""))
    except (OSError, ValueError, AttributeError, TypeError):
        return 0
    if not da_sua:
        return 0
    thieu, nguon = lenh_con_thieu(goc, lenh_dat)
    if not thieu:
        return 0

    ghi_hook("nhac_test", "nhac", f"thieu {len(thieu)} lenh kiem" + (f" ({nguon})" if nguon else ""), payload)
    ds = ", ".join(Path(p).name for p in da_sua[:5])
    if len(da_sua) > 5:
        ds += f" (+{len(da_sua) - 5} file)"
    theo = f" (theo {nguon})" if nguon else ""
    print(json.dumps({
        "decision": "block",
        "reason": (
            f"Luot nay da sua code ({ds}) nhung sau lan sua cuoi chua chay thanh cong: "
            f"{'; '.join(thieu)}{theo}. "
            "Hay chay du cac lenh do roi bao PASS/FAIL tung lenh; lenh nao khong chay duoc thi "
            "ghi ro NOT RUN va ly do (rules/global.md: NO TEST = NO PASS)."
        ),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
