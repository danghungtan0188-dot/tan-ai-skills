"""Quy tắc học được: đề xuất -> (người dùng duyệt) -> đã duyệt. Có phiên bản, lịch sử, bật/tắt, hoàn tác.

Ba phạm vi, phạm vi hẹp thắng khi áp dụng:  du_an  >  ca_nhan  >  he_thong
- du_an:    <thư mục dự án>/hoc/quy-tac.json   (cũng là nơi giữ mọi quy tắc ĐỀ XUẤT)
- ca_nhan:  $TAN_STUDIO_HOME/quy-tac.json      (mặc định ~/.tan-studio/)
- he_thong: tan_studio/data/quy_tac_he_thong.json (trong repo, có test hồi quy)

Chỉ quy tắc `da_duyet` + `bat` mới được áp dụng. Hai quy tắc cùng từ mà cách đọc khác nhau là
MÂU THUẪN: không tự chọn; chỉ được duyệt ở phạm vi dự án (ghi đè cục bộ), hoặc người dùng tắt cái kia.
"""

from __future__ import annotations

import copy
import secrets
from pathlib import Path

from . import DATA, now, read_json, studio_home, write_json

SCOPES = ("du_an", "ca_nhan", "he_thong")
SYSTEM_FILE = DATA / "quy_tac_he_thong.json"


class RuleError(ValueError):
    pass


def scope_file(scope: str, project_dir: Path | None) -> Path | None:
    if scope == "du_an":
        return Path(project_dir) / "hoc" / "quy-tac.json" if project_dir else None
    if scope == "ca_nhan":
        return studio_home() / "quy-tac.json"
    if scope == "he_thong":
        return SYSTEM_FILE
    raise RuleError(f"phạm vi phải là {SCOPES}")


def _load(path: Path | None) -> dict:
    if path is None:
        return {"quy_tac": []}
    return read_json(path, {"quy_tac": []})


def all_rules(project_dir: Path | None) -> list[tuple[str, dict]]:
    out = []
    for scope in SCOPES:
        out += [(scope, r) for r in _load(scope_file(scope, project_dir))["quy_tac"]]
    return out


def active_pronunciations(project_dir: Path | None) -> list[dict]:
    """Thứ tự du_an -> ca_nhan -> he_thong: quy tắc hẹp chạy trước nên thắng."""
    return [{"tu": r["dieu_kien"]["tu"], "doc_thanh": r["bien_doi"]["doc_thanh"], "id": r["id"],
             "phien_ban": r["phien_ban"], "pham_vi": scope}
            for scope, r in all_rules(project_dir)
            if r["trang_thai"] == "da_duyet" and r["bat"]]


def _find(project_dir: Path | None, rule_id: str):
    for scope in SCOPES:
        path = scope_file(scope, project_dir)
        data = _load(path)
        for r in data["quy_tac"]:
            if r["id"] == rule_id:
                return path, data, r
    raise RuleError(f"không có quy tắc {rule_id}" + ("" if project_dir else " (thiếu file dự án?)"))


def _save(path: Path, data: dict) -> None:
    data.setdefault("_ghi_chu", "Quản lý bằng `python -m tan_studio quy-tac ...` — đừng sửa tay trạng thái/lịch sử.")
    write_json(path, data)


def _mutate(rule: dict, action: str, changes: dict, ghi_chu: str = "") -> None:
    snap = {k: copy.deepcopy(v) for k, v in rule.items() if k != "lich_su"}
    rule.update(changes)
    rule["phien_ban"] += 1
    rule["lich_su"].append({"luc": now(), "hanh_dong": action, "phien_ban": rule["phien_ban"],
                            "ghi_chu": ghi_chu, "truoc": snap})


def _conflicts(project_dir, rule) -> list[str]:
    return [r["id"] for _, r in all_rules(project_dir)
            if r["id"] != rule["id"] and r["dieu_kien"]["tu"] == rule["dieu_kien"]["tu"]
            and r["bien_doi"]["doc_thanh"] != rule["bien_doi"]["doc_thanh"]
            and (r["trang_thai"] in ("de_xuat", "mau_thuan") or (r["trang_thai"] == "da_duyet" and r["bat"]))]


def _normalized_with(text: str, entries: list[dict]) -> str:
    from .normalize import normalize_text
    return normalize_text(text, phat_am=entries)["normalized"]


def propose(project_dir: Path, project: dict, tu: str, doc_thanh: str, ngu_canh: str,
            quan_sat_id: str, run_id: str | None, pham_vi_de_nghi: str = "du_an") -> dict:
    """Tạo quy tắc ĐỀ XUẤT từ một quan sát. Trùng (cùng từ, cùng cách đọc) thì chỉ liên kết thêm quan sát."""
    path = scope_file("du_an", project_dir)
    data = _load(path)
    for scope, r in all_rules(project_dir):
        if r["dieu_kien"]["tu"] == tu and r["bien_doi"]["doc_thanh"] == doc_thanh and r["trang_thai"] != "tu_choi":
            if scope == "du_an":
                r2 = next(x for x in data["quy_tac"] if x["id"] == r["id"])
                if quan_sat_id not in r2["nguon"]["quan_sat"]:
                    r2["nguon"]["quan_sat"].append(quan_sat_id)
                    _save(path, data)
                return r2
            return r
    entry = {"tu": tu, "doc_thanh": doc_thanh, "id": "de-xuat", "phien_ban": 0}
    rule = {
        "kind": "Rule", "id": f"qt-{secrets.token_hex(3)}", "loai": "phat_am",
        "trang_thai": "de_xuat", "bat": False, "pham_vi": "du_an", "pham_vi_de_nghi": pham_vi_de_nghi,
        "dieu_kien": {"tu": tu, "khop": "nguyên từ, phân biệt hoa thường"},
        "bien_doi": {"doc_thanh": doc_thanh},
        "vi_du": {"truoc": ngu_canh, "sau": _normalized_with(ngu_canh, [entry])},
        "kiem_thu": [], "xac_nhan": None, "mau_thuan_voi": [],
        "nguon": {"quan_sat": [quan_sat_id], "lan_chay": run_id, "du_an": project.get("ten"),
                  "du_an_file": project.get("_file")},
        "tao_luc": now(), "phien_ban": 1,
        "lich_su": [{"luc": now(), "hanh_dong": "de_xuat", "phien_ban": 1, "ghi_chu": f"từ quan sát {quan_sat_id}"}],
    }
    rule["mau_thuan_voi"] = _conflicts(project_dir, rule)
    if rule["mau_thuan_voi"]:
        rule["trang_thai"] = "mau_thuan"
        for other in data["quy_tac"]:  # đánh dấu cả phía bên kia nếu nó còn là đề xuất trong dự án
            if other["id"] in rule["mau_thuan_voi"] and other["trang_thai"] in ("de_xuat", "mau_thuan"):
                _mutate(other, "phat_hien_mau_thuan", {"trang_thai": "mau_thuan",
                                                       "mau_thuan_voi": other["mau_thuan_voi"] + [rule["id"]]})
    data["quy_tac"].append(rule)
    _save(path, data)
    return rule


def approve(project_dir: Path, rule_id: str, scope: str = "du_an", ghi_chu: str = "") -> dict:
    if scope not in SCOPES:
        raise RuleError(f"phạm vi phải là {SCOPES}")
    path, data, rule = _find(project_dir, rule_id)
    if rule["trang_thai"] not in ("de_xuat", "mau_thuan"):
        raise RuleError(f"{rule_id} đang ở trạng thái {rule['trang_thai']}, không duyệt được")
    conflicts = _conflicts(project_dir, rule)
    if conflicts:
        same_scope = [r["id"] for s, r in all_rules(project_dir) if r["id"] in conflicts and s == scope
                      and r["trang_thai"] == "da_duyet"]
        if scope != "du_an" or same_scope:
            raise RuleError(f"mâu thuẫn với {conflicts}: chỉ duyệt được ở phạm vi du_an khi trong dự án chưa có "
                            "quy tắc đã duyệt khác cho cùng từ — hoặc tắt/hoàn tác quy tắc kia trước")
    tu, doc = rule["dieu_kien"]["tu"], rule["bien_doi"]["doc_thanh"]
    cases = [{"dau_vao": rule["vi_du"]["truoc"], "ky_vong": doc}]
    entry = {"tu": tu, "doc_thanh": doc, "id": rule_id, "phien_ban": rule["phien_ban"]}
    for c in cases:
        if c["ky_vong"] not in _normalized_with(c["dau_vao"], [entry]):
            raise RuleError(f"ca kiểm thử không qua: {c['dau_vao']!r} không ra {doc!r}")
    _mutate(rule, "duyet", {"trang_thai": "da_duyet", "bat": True, "pham_vi": scope, "kiem_thu": cases,
                            "mau_thuan_voi": conflicts,
                            "xac_nhan": {"boi": "nguoi-dung", "luc": now(), "ghi_chu": ghi_chu}}, ghi_chu)
    _relocate(project_dir, path, data, rule)
    return rule


def _relocate(project_dir, path, data, rule) -> None:
    """Ghi rule vào file đúng phạm vi hiện tại của nó (chuyển file nếu phạm vi đổi)."""
    target = scope_file(rule["pham_vi"], project_dir)
    if Path(target) == Path(path):
        _save(path, data)
        return
    data["quy_tac"] = [r for r in data["quy_tac"] if r["id"] != rule["id"]]
    _save(path, data)
    tdata = _load(target)
    tdata["quy_tac"] = [r for r in tdata["quy_tac"] if r["id"] != rule["id"]] + [rule]
    _save(target, tdata)


def reject(project_dir: Path, rule_id: str, ly_do: str = "") -> dict:
    path, data, rule = _find(project_dir, rule_id)
    if rule["trang_thai"] not in ("de_xuat", "mau_thuan"):
        raise RuleError(f"{rule_id} không còn là đề xuất — dùng `tat` hoặc `hoan-tac`")
    _mutate(rule, "tu_choi", {"trang_thai": "tu_choi"}, ly_do)
    _save(path, data)
    return rule


def set_enabled(project_dir: Path, rule_id: str, bat: bool, ghi_chu: str = "") -> dict:
    path, data, rule = _find(project_dir, rule_id)
    if rule["trang_thai"] != "da_duyet":
        raise RuleError("chỉ bật/tắt được quy tắc đã duyệt")
    if rule["bat"] == bat:
        return rule
    _mutate(rule, "bat" if bat else "tat", {"bat": bat}, ghi_chu)
    _save(path, data)
    return rule


def undo(project_dir: Path, rule_id: str) -> dict:
    """Quay về trạng thái trước thao tác gần nhất. Bản thân việc hoàn tác cũng ghi lịch sử (hoàn tác tiếp = làm lại)."""
    path, data, rule = _find(project_dir, rule_id)
    last = next((h for h in reversed(rule["lich_su"]) if "truoc" in h), None)
    if last is None:
        raise RuleError("không còn thao tác nào để hoàn tác")
    restore = {k: v for k, v in last["truoc"].items() if k != "phien_ban"}
    _mutate(rule, f"hoan_tac:{last['hanh_dong']}", restore)
    _relocate(project_dir, path, data, rule)
    return rule


def regression(project_dir: Path | None) -> list[dict]:
    """Chạy lại ca kiểm thử của mọi quy tắc đã duyệt, với toàn bộ quy tắc đang bật (như lúc chạy thật)."""
    active = active_pronunciations(project_dir)
    results = []
    for scope, r in all_rules(project_dir):
        if r["trang_thai"] != "da_duyet":
            continue
        for c in r["kiem_thu"]:
            out = _normalized_with(c["dau_vao"], active if r["bat"] else
                                   [{"tu": r["dieu_kien"]["tu"], "doc_thanh": r["bien_doi"]["doc_thanh"],
                                     "id": r["id"], "phien_ban": r["phien_ban"]}] + active)
            results.append({"id": r["id"], "pham_vi": scope, "bat": r["bat"], "ok": c["ky_vong"] in out,
                            "dau_vao": c["dau_vao"], "ky_vong": c["ky_vong"], "thuc_te": out})
    return results


def trial(project_dir: Path, rule_id: str, samples: list[tuple[str, str]]) -> dict:
    """Thử một quy tắc (thường là đề xuất) trên bộ mẫu, so với cấu hình hiện tại. Không lưu, không áp dụng.

    samples: [(nguồn, câu)] — ví dụ từ bộ câu TTS và các lần chạy cũ của dự án.
    """
    _, _, rule = _find(project_dir, rule_id)
    base = [e for e in active_pronunciations(project_dir) if e["id"] != rule_id]
    cand = [{"tu": rule["dieu_kien"]["tu"], "doc_thanh": rule["bien_doi"]["doc_thanh"], "id": rule_id,
             "phien_ban": rule["phien_ban"]}] + base
    report = {"quy_tac": rule_id, "luc": now(), "tot_len": [], "xau_di": [], "doi_khac": [], "khong_doi": 0}
    for scope, r in all_rules(project_dir):
        if r["trang_thai"] != "da_duyet" or not r["bat"] or r["id"] == rule_id:
            continue
        for c in r["kiem_thu"]:
            before = c["ky_vong"] in _normalized_with(c["dau_vao"], base)
            after = c["ky_vong"] in _normalized_with(c["dau_vao"], cand)
            if before and not after:
                report["xau_di"].append({"kiem_thu_cua": r["id"], "dau_vao": c["dau_vao"]})
    own = rule["vi_du"]["truoc"]
    if rule["bien_doi"]["doc_thanh"] in _normalized_with(own, cand) and \
            rule["bien_doi"]["doc_thanh"] not in _normalized_with(own, base):
        report["tot_len"].append({"vi_du": own})
    for src, text in samples:
        a, b = _normalized_with(text, base), _normalized_with(text, cand)
        if a != b:
            report["doi_khac"].append({"nguon": src, "truoc": a, "sau": b})
        else:
            report["khong_doi"] += 1
    report["so_mau"] = len(samples)
    report["ket_luan"] = ("XẤU ĐI — làm hỏng kiểm thử của quy tắc khác" if report["xau_di"] else
                          "TỐT LÊN ở ví dụ của chính nó; xem các câu đổi khác trước khi duyệt" if report["tot_len"] else
                          "CHƯA ĐỦ DỮ LIỆU — quy tắc không làm đổi ví dụ của chính nó")
    return report


def history_samples(project_dir: Path) -> list[tuple[str, str]]:
    """Câu gốc từ các lần chạy cũ (nếu còn lưu văn bản) + bộ câu đánh giá TTS."""
    out = []
    for f in sorted(Path(project_dir).glob("*/*/chuan-hoa.json")):
        for s in (read_json(f) or {}).get("segments", []):
            if isinstance(s.get("original"), str):
                out.append((f"{f.parent.name}#{s['index']}", s["original"]))
    for c in (read_json(DATA / "tts_cases.json") or {}).get("cau", []):
        out.append((f"tts:{c['id']}", c["van_ban"]))
    return out


def proposal_stats(project_dir: Path) -> dict:
    counts = {}
    for _, r in all_rules(project_dir):
        if r["nguon"].get("du_an_file") and project_dir and \
                Path(r["nguon"]["du_an_file"]).parent != Path(project_dir):
            continue
        counts[r["trang_thai"]] = counts.get(r["trang_thai"], 0) + 1
    return counts

