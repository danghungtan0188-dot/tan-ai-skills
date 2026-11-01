#!/usr/bin/env python3
"""PreToolUse hook: chot chan rieng cho du an phan mem (web, webapp, mobile, desktop).

Bash / PowerShell -> HOI (permissionDecision=ask) khi:
  - cai thu vien MOI (npm i <goi>, pnpm/yarn/bun add, pip install <goi>, uv add, ...);
    cai lai theo lockfile (npm install, npm ci, pip install -r ...) thi cho qua,
  - chay migration / day schema (prisma migrate, drizzle-kit push, alembic upgrade, ...),
  - SQL xoa cau truc: DROP TABLE, DROP COLUMN, TRUNCATE.
Write / Edit -> CHAN (exit 2) khi:
  - dat secret vao bien moi truong cong khai (NEXT_PUBLIC_*SECRET*, VITE_*SERVICE_ROLE*, ...):
    bien co tien to nay bi dong goi vao code chay o trinh duyet / dien thoai,
  - ghi Stripe secret key that (sk_live_ / rk_live_).
guard_bash da chan supabase db reset, DROP DATABASE, DELETE khong WHERE; hook nay khong lap lai.
Xem rules/security.md va docs/bai-hoc-va-chot-chan.md.
"""

import json
import re
import sys
from pathlib import PurePosixPath

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

# File cua chinh he thong nay chua mau can bat -> mien tru de khong tu chan.
SELF_REFERENTIAL = (".claude/hooks/guard_app.py", "tests/test_hooks.py")

# Trinh quan ly goi: (cac token mo dau, cac lenh con them goi moi).
_QUAN_LY_GOI = [
    (("npm",), {"install", "i", "in", "add", "isntall"}),
    (("pnpm",), {"add", "install", "i"}),
    (("yarn",), {"add"}),
    (("bun",), {"add", "install", "i"}),
    (("pip",), {"install"}),
    (("pip3",), {"install"}),
    (("-m", "pip"), {"install"}),
    (("uv", "pip"), {"install"}),
    (("uv",), {"add"}),
    (("poetry",), {"add"}),
    (("pipx",), {"install"}),
    (("expo",), {"install"}),
    (("cargo",), {"add", "install"}),
    (("go",), {"get"}),
    (("dotnet", "add"), {"package"}),
    (("flutter", "pub"), {"add"}),
    (("dart", "pub"), {"add"}),
    (("composer",), {"require"}),
    (("gem",), {"install"}),
]
# Tham so an luon gia tri di sau (khong phai ten goi).
_THAM_SO_CO_GIA_TRI = {"-r", "--requirement", "-c", "--constraint", "-e", "--editable",
                       "--index-url", "-i", "--extra-index-url", "--prefix", "--target", "-t"}
_KHONG_PHAI_GOI = {".", "pip", "setuptools", "wheel"}

MIGRATION = re.compile(
    r"\bprisma\s+(migrate\s+(dev|reset|deploy|resolve)|db\s+(push|execute))\b"
    r"|\bdrizzle-kit\s+(push|migrate|drop)\b"
    r"|\balembic\s+(upgrade|downgrade|stamp)\b"
    r"|\bmanage\.py\s+(migrate|flush)\b"
    r"|\b(rails|rake)\s+db:\w+"
    r"|\bknex\s+migrate:\w+"
    r"|\bsequelize(-cli)?\s+db:\w+"
    r"|\btypeorm\s+migration:(run|revert)\b"
    r"|\bsupabase\s+migration\s+(up|repair)\b",
    re.I,
)
SQL_XOA_CAU_TRUC = re.compile(r"\bDROP\s+(TABLE|COLUMN)\b|\bTRUNCATE\s+\w", re.I)

PUBLIC_SECRET = re.compile(
    r"\b(NEXT_PUBLIC|NUXT_PUBLIC|EXPO_PUBLIC|REACT_APP|VITE|GATSBY|PUBLIC)_[A-Z0-9_]*"
    r"(SECRET|SERVICE_ROLE|SERVICE_KEY|PRIVATE|PASSWORD)[A-Z0-9_]*"
)
STRIPE_LIVE = re.compile(r"\b(sk|rk)_live_[0-9A-Za-z]{20,}")


def goi_moi(command: str) -> list[str]:
    """Ten cac goi moi trong lenh cai dat (rong neu chi cai lai theo lockfile)."""
    ket_qua = []
    for doan in re.split(r"&&|\|\||[;|\n]", command):
        tokens = [t.strip("\"'`()") for t in doan.split()]
        tokens = [t for t in tokens if t]
        for dau, lenh_con in _QUAN_LY_GOI:
            n = len(dau)
            for i in range(len(tokens) - n):
                if tuple(t.lower() for t in tokens[i:i + n]) != dau:
                    continue
                if tokens[i + n].lower() not in lenh_con:
                    continue
                bo_qua = False
                for tok in tokens[i + n + 1:]:
                    if bo_qua:
                        bo_qua = False
                    elif tok in _THAM_SO_CO_GIA_TRI:
                        bo_qua = True
                    elif not tok.startswith("-") and tok.lower() not in _KHONG_PHAI_GOI:
                        ket_qua.append(tok)
    return ket_qua


def ly_do_hoi(command: str) -> str | None:
    goi = goi_moi(command)
    if goi:
        return (f"cai thu vien moi ({', '.join(dict.fromkeys(goi))}). Kiem dung ten goi "
                "(khong phai ten nhai), con duoc bao tri, va nguoi dung dong y")
    if MIGRATION.search(command):
        return "chay migration / doi schema database. Phai cho nguoi dung xem file migration truoc"
    if SQL_XOA_CAU_TRUC.search(command):
        return "SQL xoa bang / cot / du lieu (DROP TABLE, DROP COLUMN, TRUNCATE)"
    return None


def loi_ghi(path: str, content: str) -> list[str]:
    norm = str(PurePosixPath(path.replace("\\", "/")))
    if norm.endswith(SELF_REFERENTIAL):
        return []
    loi = []
    # Tai lieu .md duoc nhac ten bien de canh bao; chi xet code va file cau hinh.
    if not norm.lower().endswith(".md"):
        for ten in dict.fromkeys(m.group(0) for m in PUBLIC_SECRET.finditer(content)):
            loi.append(f"Bien {ten}: tien to cong khai se dong goi secret vao code phia trinh "
                       "duyet / dien thoai. Doi ten bo tien to va chi dung o server.")
    if STRIPE_LIVE.search(content):
        loi.append("Phat hien Stripe secret key that (sk_live_/rk_live_).")
    return loi


def noi_dung_ghi(tool_input: dict) -> tuple[str, str]:
    path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    parts = [tool_input.get("content"), tool_input.get("new_string"), tool_input.get("new_source")]
    for edit in tool_input.get("edits") or []:
        if isinstance(edit, dict):
            parts.append(edit.get("new_string"))
    return path, "\n".join(p for p in parts if isinstance(p, str))


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
    tool_name = str(payload.get("tool_name") or "")
    tool_input = payload.get("tool_input") or {}

    if tool_name in ("Bash", "PowerShell"):
        command = tool_input.get("command")
        ly_do = ly_do_hoi(command) if isinstance(command, str) else None
        if ly_do:
            ghi_hook("guard_app", "hoi", ly_do.split(" (")[0].split(".")[0], payload)
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "ask",
                    "permissionDecisionReason": f"guard_app: {ly_do}.",
                }
            }, ensure_ascii=False))
        return 0

    loi = loi_ghi(*noi_dung_ghi(tool_input))
    if loi:
        ghi_hook("guard_app", "chan", "secret phia client", payload)
        print("CHAN BOI HOOK guard_app (rules/security.md):", file=sys.stderr)
        for item in loi:
            print(f"  - {item}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
