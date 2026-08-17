#!/usr/bin/env python3
"""PreToolUse hook: chan ghi secret vao repo.

Doc JSON hook input tren stdin (Write / Edit / NotebookEdit), kiem tra
duong dan va noi dung sap ghi.

Exit 0 = cho phep.
Exit 2 = chan, stderr duoc tra ve cho Claude de tu sua.

Xem rules/security.md.
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

# Cac file cua chinh he thong bao ve nay: chung chua mau regex secret nen
# se tu chan chinh no neu khong mien tru. Danh sach nay phai giu that ngan.
SELF_REFERENTIAL = {
    "rules/security.md",
    ".claude/hooks/guard_secrets.py",
    ".claude/hooks/guard_bash.py",
    "tests/test_hooks.py",
}

# Ten file .env that su (khong phai ban mau).
ENV_FILE = re.compile(r"(^|[./\\])\.env(\.[A-Za-z0-9_-]+)?$")
ENV_TEMPLATE_SUFFIX = (".example", ".sample", ".template", ".dist")

# Gia tri ro rang la placeholder -> khong coi la secret that.
PLACEHOLDER = re.compile(
    r"^(x{3,}|\*{3,}|\.{3,}|<[^>]*>|\{\{.*\}\}|\$\{.*\}|"
    r"(your|my|the)[-_ ].*|.*(example|placeholder|changeme|dummy|sample|"
    r"fake|test|redacted|todo|abcdef|123456).*)$",
    re.IGNORECASE,
)

# Mau co do tin cay cao: chan ngay.
HIGH_CONFIDENCE = [
    (re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}"), "Anthropic API key"),
    (re.compile(r"\bsk-[A-Za-z0-9]{32,}"), "OpenAI-style API key"),
    (re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"), "Google API key"),
    (re.compile(r"\b(ghp|gho|ghs|ghu)_[A-Za-z0-9]{30,}"), "GitHub token"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{50,}"), "GitHub fine-grained PAT"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key id"),
    (re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}"), "Slack token"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "Private key"),
    (
        re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]*service_role", re.I),
        "Supabase service_role JWT",
    ),
]

# Mau chung: KEY = <gia tri du dai>. Bo qua neu gia tri la placeholder.
GENERIC = re.compile(
    r"(?P<key>[A-Za-z0-9_]*(API[_-]?KEY|SECRET|TOKEN|PASSWORD|PASSWD|"
    r"PRIVATE[_-]?KEY|ACCESS[_-]?KEY|SERVICE[_-]?ROLE)[A-Za-z0-9_]*)"
    r"\s*[:=]\s*[\"']?(?P<val>[^\s\"'`,;<>()]{12,})[\"']?",
    re.IGNORECASE,
)


def normalise(path: str) -> str:
    # Khong dung lstrip("./") — no an ca dau cham cua ".env".
    return str(PurePosixPath(path.replace("\\", "/"))).removeprefix("./")


def is_self_referential(path: str) -> bool:
    norm = normalise(path)
    return any(norm.endswith(allowed) for allowed in SELF_REFERENTIAL)


def check_path(path: str) -> list[str]:
    norm = normalise(path)
    if norm.endswith(ENV_TEMPLATE_SUFFIX):
        return []
    if ENV_FILE.search(norm):
        return [
            f"Khong ghi file moi truong that: {norm}. "
            "Neu can mau cau hinh, dat ten .env.example va chi ghi gia tri placeholder."
        ]
    return []


def check_content(content: str) -> list[str]:
    findings = []
    for pattern, label in HIGH_CONFIDENCE:
        if pattern.search(content):
            findings.append(f"Phat hien {label} trong noi dung sap ghi.")
    for match in GENERIC.finditer(content):
        value = match.group("val")
        if PLACEHOLDER.match(value):
            continue
        findings.append(
            f"Bien '{match.group('key')}' duoc gan gia tri that "
            "(khong phai placeholder)."
        )
    # Bao cao toi da 5 dong cho de doc.
    return findings[:5]


def extract(tool_input: dict) -> tuple[str, str]:
    path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    parts = [
        tool_input.get("content"),
        tool_input.get("new_string"),
        tool_input.get("new_source"),
    ]
    if isinstance(tool_input.get("edits"), list):
        for edit in tool_input["edits"]:
            if isinstance(edit, dict):
                parts.append(edit.get("new_string"))
    return path, "\n".join(p for p in parts if isinstance(p, str))


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # Khong hieu input thi khong chan.

    path, content = extract(payload.get("tool_input") or {})
    if not path and not content:
        return 0
    if path and is_self_referential(path):
        return 0

    findings = check_path(path) + check_content(content)
    if not findings:
        return 0

    print("CHAN BOI HOOK guard_secrets (rules/security.md):", file=sys.stderr)
    for item in findings:
        print(f"  - {item}", file=sys.stderr)
    print(
        "Cach xu ly: dua gia tri that ra bien moi truong ngoai repo, "
        "trong file chi giu placeholder hoac tham chieu os.environ / process.env.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
