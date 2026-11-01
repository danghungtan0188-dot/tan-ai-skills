#!/usr/bin/env python3
"""Hook ghi nhat ky su dung: skill / agent / lenh "/..." nao duoc goi. KHONG BAO GIO chan.

PreToolUse (Skill | Agent | Task) -> ghi ten skill hoac loai agent.
UserPromptSubmit                 -> loi nhan bat dau bang "/" thi ghi ten lenh (chi ten, khong ghi noi dung).
Du lieu: observability/nhat_ky.py (ngoai repo). Xem: python observability/xem.py
"""

import json
import sys

try:
    from pathlib import Path as _P
    sys.path.insert(0, str(_P(__file__).resolve().parents[2]))
    from observability.nhat_ky import ghi_su_dung
except Exception:  # nhat ky la phu: loi o day khong duoc lam hong phien
    def ghi_su_dung(*_a, **_k):
        pass


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    if not isinstance(payload, dict):
        return 0
    vao = payload.get("tool_input") or {}
    cong_cu = payload.get("tool_name")
    if cong_cu == "Skill" and vao.get("skill"):
        ghi_su_dung("skill", vao["skill"], payload)
    elif cong_cu in ("Agent", "Task"):
        ghi_su_dung("agent", vao.get("subagent_type") or "general-purpose", payload)
    elif isinstance(payload.get("prompt"), str) and payload["prompt"].lstrip().startswith("/"):
        ghi_su_dung("lenh", payload["prompt"].split()[0], payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
