"""Xem, xuất, xoá, dọn dữ liệu của dự án/lần chạy. Mọi lệnh xoá cần --chac-chan; không có thì chỉ in kế hoạch.

Không bao giờ đụng tới tư liệu gốc (kịch bản, audio, media người dùng đưa vào) — chỉ xoá trong
<dự án>/ket-qua/ và <dự án>/hoc/. Media không được sao chép vào lần chạy (chỉ lưu dấu vân tay).
"""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

from . import read_json, read_jsonl, write_jsonl
from . import review, workflow

HEAVY = {".wav", ".mp4", ".mp3", ".ass"}


def _size(p: Path) -> int:
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file()) if p.exists() else 0


def overview(project: Path) -> dict:
    cfg = workflow.load_project(project)
    runs = []
    for d in workflow.list_runs(cfg):
        r = read_json(d / "run.json")
        runs.append({"run_id": d.name, "trang_thai": r.get("status"), "noi_dung": r.get("noi_dung"),
                     "xem_truoc": r.get("xem_truoc"), "dung_luong_mb": round(_size(d) / 1e6, 2),
                     "da_don_media": r.get("ho_so", {}).get("da_don_media", False)})
    hoc = review.hoc_dir(cfg["_dir"])
    return {"du_an": cfg["ten"], "lan_chay": runs, "hoc": {
        "quan_sat": len(review.observations(cfg["_dir"])), "danh_gia": len(review.verdicts(cfg["_dir"])),
        "quy_tac": len((read_json(hoc / "quy-tac.json") or {"quy_tac": []})["quy_tac"])},
        "tong_dung_luong_mb": round((_size(workflow.runs_root(cfg)) + _size(hoc)) / 1e6, 2)}


def export(project: Path, out_zip: Path, run_id: str | None = None, with_media: bool = False) -> Path:
    cfg = workflow.load_project(project)
    roots = [workflow.resolve_run(cfg, run_id)] if run_id else [workflow.runs_root(cfg), review.hoc_dir(cfg["_dir"])]
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for root in roots:
            for f in (root.rglob("*") if root.exists() else []):
                if f.is_file() and (with_media or f.suffix.lower() not in HEAVY):
                    z.write(f, f.relative_to(cfg["_dir"]))
    return out_zip


def delete_run(project: Path, run_id: str, sure: bool) -> dict:
    """Xoá thư mục lần chạy + quan sát/đánh giá gắn với nó. Quy tắc đã duyệt giữ nguyên (chỉ còn nguồn tham chiếu)."""
    cfg = workflow.load_project(project)
    d = workflow.resolve_run(cfg, run_id)
    hoc = review.hoc_dir(cfg["_dir"])
    obs = [o for o in review.observations(cfg["_dir"]) if o["lan_chay"] == run_id]
    ver = [v for v in review.verdicts(cfg["_dir"]) if v["lan_chay"] == run_id]
    plan = {"xoa_thu_muc": str(d), "dung_luong_mb": round(_size(d) / 1e6, 2), "xoa_quan_sat": len(obs),
            "xoa_danh_gia": len(ver), "da_xoa": False}
    if sure:
        shutil.rmtree(d)
        write_jsonl(hoc / "quan-sat.jsonl", [o for o in read_jsonl(hoc / "quan-sat.jsonl") if o["lan_chay"] != run_id])
        write_jsonl(hoc / "danh-gia.jsonl", [v for v in read_jsonl(hoc / "danh-gia.jsonl") if v["lan_chay"] != run_id])
        plan["da_xoa"] = True
    return plan


def cleanup(project: Path, keep: int, sure: bool) -> dict:
    """Giữ media của `keep` lần chạy mới nhất + mọi lần đã được chấp nhận; lần cũ hơn chỉ giữ JSON/MD/SRT."""
    cfg = workflow.load_project(project)
    runs = workflow.list_runs(cfg)
    accepted = {v["lan_chay"] for v in review.verdicts(cfg["_dir"])
                if v["kind"] == "Verdict" and v["ket_luan"] == "chap_nhan"}
    victims = [d for d in runs[: max(0, len(runs) - keep)] if d.name not in accepted]
    files = [f for d in victims for f in d.rglob("*") if f.is_file() and f.suffix.lower() in HEAVY]
    plan = {"lan_chay": [d.name for d in victims], "so_tep": len(files),
            "giai_phong_mb": round(sum(f.stat().st_size for f in files) / 1e6, 2), "da_xoa": False}
    if sure:
        for f in files:
            f.unlink()
        for d in victims:
            r = read_json(d / "run.json")
            r.setdefault("ho_so", {})["da_don_media"] = True
            workflow.save(r, d)
        plan["da_xoa"] = True
    return plan


def delete_project_data(project: Path, sure: bool) -> dict:
    cfg = workflow.load_project(project)
    targets = [workflow.runs_root(cfg), review.hoc_dir(cfg["_dir"])]
    plan = {"xoa": [str(t) for t in targets if t.exists()],
            "dung_luong_mb": round(sum(_size(t) for t in targets) / 1e6, 2), "da_xoa": False,
            "khong_dung_toi": "kịch bản, audio, media gốc và file dự án"}
    if sure:
        for t in targets:
            if t.exists():
                shutil.rmtree(t)
        plan["da_xoa"] = True
    return plan
