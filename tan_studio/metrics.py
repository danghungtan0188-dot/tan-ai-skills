"""Đo chất lượng qua thời gian, lịch sử một lỗi qua các lần chạy, so sánh hai lần chạy.

Mọi tỉ lệ đi kèm số mẫu (n) và cách tính; n < MIN_N thì ghi "chưa đủ dữ liệu" thay vì kết luận.
"""

from __future__ import annotations

import difflib
import subprocess
from datetime import datetime
from pathlib import Path

from . import read_json
from . import review, rules, workflow

MIN_N = 3


def _rate(num: int, den: int, how: str) -> dict:
    out = {"tu_so": num, "mau_so": den, "cach_tinh": how}
    out["gia_tri"] = round(num / den, 3) if den else None
    out["ket_luan"] = "chưa đủ dữ liệu" if den < MIN_N else f"{num}/{den} = {num / den:.0%}"
    return out


def _runs(cfg) -> list[dict]:
    return [r for r in (read_json(d / "run.json") for d in workflow.list_runs(cfg)) if r]


def _findings(run: dict) -> list[dict]:
    return read_json(Path(run["run_dir"]) / "phat-hien.json", {"phat_hien": []})["phat_hien"]


def project_metrics(project: Path, group_by: str | None = None) -> dict:
    """group_by: None | 'config_hash' | 'app_version'."""
    cfg = workflow.load_project(project)
    runs = _runs(cfg)
    if group_by:
        groups = {}
        for r in runs:
            groups.setdefault(r.get(group_by, "?"), []).append(r["run_id"])
        return {k: _metrics(cfg, set(ids)) for k, ids in groups.items()}
    return {"tat_ca": _metrics(cfg, {r["run_id"] for r in runs})}


def _metrics(cfg, run_ids: set[str]) -> dict:
    pdir = cfg["_dir"]
    runs = sorted((r for r in _runs(cfg) if r["run_id"] in run_ids), key=lambda r: r["created_at"])
    verdicts = [v for v in review.verdicts(pdir) if v["lan_chay"] in run_ids]
    obs = [o for o in review.observations(pdir) if o["lan_chay"] in run_ids]

    # "lượt sản phẩm": chuỗi lần chạy kết thúc ở một lần được chấp nhận.
    final = {}
    for v in verdicts:
        if v["kind"] == "Verdict":
            final[v["lan_chay"]] = v
    sequences, cur = [], []
    for r in runs:
        if r.get("xem_truoc"):
            continue
        cur.append(r)
        if final.get(r["run_id"], {}).get("ket_luan") == "chap_nhan":
            sequences.append(cur)
            cur = []
    accepted_first = sum(len(s) == 1 for s in sequences)
    edits = [len(s) - 1 for s in sequences]
    durations = []
    for s in sequences:
        t0 = datetime.fromisoformat(s[0]["created_at"])
        t1 = datetime.fromisoformat(final[s[-1]["run_id"]]["luc"])
        durations.append(round((t1 - t0).total_seconds() / 60, 1))

    by_type, by_step = {}, {}
    for o in obs:
        by_type[o["loai"]] = by_type.get(o["loai"], 0) + 1
        by_step[o["buoc"]] = by_step.get(o["buoc"], 0) + 1
    recurring = [o for o in obs if o.get("lap_lai_tu_lan_chay")]
    fv = [v for v in verdicts if v["kind"] == "FindingVerdict"]
    fstats = rules.proposal_stats(pdir)
    decided = fstats.get("da_duyet", 0) + fstats.get("tu_choi", 0)
    return {
        "so_lan_chay": len(runs),
        "so_lan_duoc_danh_gia": len(final),
        "chap_nhan_ngay_lan_dau": _rate(accepted_first, len(sequences),
                                        "lượt sản phẩm (chuỗi lần chạy kết thúc khi được chấp nhận) chỉ cần 1 lần chạy"),
        "so_lan_sua_truoc_khi_duyet": {"danh_sach": edits, "trung_binh": round(sum(edits) / len(edits), 2) if edits else None,
                                       "n": len(edits)},
        "phut_tu_script_den_duyet": {"danh_sach": durations, "n": len(durations)},
        "loi_theo_loai": by_type,
        "loi_theo_buoc": by_step,
        "loi_cu_tai_xuat_hien": _rate(len(recurring), len(obs),
                                      "quan sát có cùng dấu vân tay với quan sát ở lần chạy TRƯỚC"),
        "canh_bao_tu_dong_dung": _rate(sum(v["ket_luan"] == "dung" for v in fv), len(fv),
                                       "cảnh báo người dùng xác nhận đúng / đã xác nhận"),
        "quy_tac_de_xuat": {"theo_trang_thai": fstats,
                            "ty_le_duyet": _rate(fstats.get("da_duyet", 0), decided, "đã duyệt / (duyệt + từ chối)")},
    }


def error_history(project: Path, key: str | None = None) -> dict:
    """Bảng dấu vân tay × lần chạy: X = có (máy phát hiện hoặc người dùng ghi), . = không."""
    cfg = workflow.load_project(project)
    runs = sorted(_runs(cfg), key=lambda r: r["created_at"])
    obs = review.observations(cfg["_dir"])
    table = {}
    for r in runs:
        present = {f["dau_van_tay"] for f in _findings(r)} | {o["dau_van_tay"] for o in obs if o["lan_chay"] == r["run_id"]}
        for fp in present:
            table.setdefault(fp, {})[r["run_id"]] = True
    if key:
        table = {fp: v for fp, v in table.items() if key.lower() in fp.lower()}
    rows = []
    for fp, seen in sorted(table.items()):
        marks = ["X" if seen.get(r["run_id"]) else "." for r in runs]
        first = marks.index("X")
        rows.append({"dau_van_tay": fp, "lan_chay": marks, "lan_dau": runs[first]["run_id"],
                     "lan_gan_nhat_co": runs[len(marks) - 1 - marks[::-1].index("X")]["run_id"],
                     "con_o_lan_moi_nhat": marks[-1] == "X"})
    return {"lan_chay": [r["run_id"] for r in runs], "quy_tac_dang_bat": [
        f"{e['id']} v{e['phien_ban']}" for e in rules.active_pronunciations(cfg["_dir"])], "dong": rows}


def compare(project: Path, run_a: str, run_b: str, video_out: Path | None = None) -> dict:
    cfg = workflow.load_project(project)
    a = read_json(workflow.resolve_run(cfg, run_a) / "run.json")
    b = read_json(workflow.resolve_run(cfg, run_b) / "run.json")

    def flat(d, prefix=""):
        out = {}
        for k, v in (d or {}).items():
            if isinstance(v, dict):
                out.update(flat(v, f"{prefix}{k}."))
            else:
                out[f"{prefix}{k}"] = v
        return out

    ca, cb = flat(a["config"]), flat(b["config"])
    va, vb = flat(a["versions"]), flat(b["versions"])
    fa = {f["dau_van_tay"]: f for f in _findings(a)}
    fb = {f["dau_van_tay"]: f for f in _findings(b)}
    na = read_json(Path(a["run_dir"]) / "chuan-hoa.json") or {}
    nb = read_json(Path(b["run_dir"]) / "chuan-hoa.json") or {}
    text_a, text_b = na.get("normalized_text", ""), nb.get("normalized_text", "")
    steps = {s["name"]: s for s in a["steps"]}, {s["name"]: s for s in b["steps"]}
    out = {
        "a": run_a, "b": run_b,
        "cau_hinh_khac": {k: [ca.get(k), cb.get(k)] for k in sorted(set(ca) | set(cb)) if ca.get(k) != cb.get(k)},
        "phien_ban_khac": {k: [va.get(k), vb.get(k)] for k in sorted(set(va) | set(vb)) if va.get(k) != vb.get(k)},
        "van_ban_chuan_hoa_khac": list(difflib.unified_diff(text_a.splitlines(), text_b.splitlines(),
                                                            run_a, run_b, lineterm="", n=0)),
        "phat_hien_da_het": sorted(set(fa) - set(fb)),
        "phat_hien_moi": sorted(set(fb) - set(fa)),
        "phat_hien_con": sorted(set(fa) & set(fb)),
        "trang_thai": [a.get("status"), b.get("status")],
        "noi_dung": [a.get("noi_dung"), b.get("noi_dung")],
        "thoi_gian_buoc": {n: [steps[0].get(n, {}).get("duration_s"), steps[1].get(n, {}).get("duration_s")]
                           for n in workflow.STEPS},
    }
    if video_out:
        out["video_so_sanh"] = str(side_by_side(_video(a), _video(b), video_out))
    return out


def _video(run: dict) -> Path:
    v = next((s for s in run["steps"] if s["name"] == "dung_video"), {}).get("outputs", {}).get("video")
    if not v or not Path(v).exists():
        raise workflow.ProjectError(f"lần chạy {run['run_id']} không có video")
    return Path(v)


def side_by_side(a: Path, b: Path, out: Path) -> Path:
    """Hai video cạnh nhau (trái = trước, phải = sau), cao 540px, mã hoá nhanh — nhẹ máy."""
    out.parent.mkdir(parents=True, exist_ok=True)
    flt = ("[0:v]scale=-2:540,setsar=1[l];[1:v]scale=-2:540,setsar=1[r];[l][r]hstack=inputs=2:shortest=1[v];"
           "[0:a][1:a]amerge=inputs=2,pan=stereo|c0=c0|c1=c2[a]")
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(a), "-i", str(b),
           "-filter_complex", flt, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "ultrafast",
           "-crf", "28", "-threads", "4", "-c:a", "aac", "-shortest", "-movflags", "+faststart", str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise workflow.ProjectError(f"ffmpeg so sánh lỗi: {r.stderr[-500:]}")
    return out
