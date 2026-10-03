"""Chạy workflow theo file dự án (JSON). Mỗi lần chạy có run_id + thư mục riêng, không ghi đè lần trước.

Bước: chuan_hoa -> giong_doc -> phu_de -> kiem_truoc -> dung_video -> kiem_tra.
run.json (hồ sơ) được ghi lại sau MỖI bước. `kiem_truoc` chặn dựng video khi có lỗi mức `loi`.
Trạng thái kỹ thuật (status) KHÁC đánh giá nội dung (noi_dung): máy chỉ kiểm được kỹ thuật;
nội dung nghe nhìn là "chua_danh_gia" cho tới khi người dùng chấp nhận/từ chối.
"""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import time
import traceback
from pathlib import Path

from . import REPO_ROOT, SKILL_DIRS, __version__, fingerprint_file, now, read_json, sha_text, stamp, write_json
from . import checks, do_hoa, normalize, rules, subtitles, tts, video

STEPS = ["chuan_hoa", "giong_doc", "phu_de", "kiem_truoc", "dung_video", "kiem_tra"]
DEFAULTS = {
    "ten": "du-an",
    "kich_ban": None,
    "audio": None,
    "phu_de": None,
    "media": [],
    "ti_le": "16:9",
    "thu_muc_ket_qua": "ket-qua",
    "tts": {"engine": "vieneu", "giong": "nam", "phong_cach": "tin_tuc", "toc_do": 1.0,
            "khoang_lang_ms": 450, "mp3": False},
    "chuan_hoa": {"tat_quy_tac": []},
    "kiem_tra": {},
    "ho_so": {"luu_van_ban": True},
    "do_hoa": {},
}
TRACKED_FILES = [  # phiên bản quy tắc/skill dùng trong lần chạy
    SKILL_DIRS["tts"] / "normalize_vi.py",
    SKILL_DIRS["tts"].parent / "references" / "abbreviations.json",
    SKILL_DIRS["video"] / "check_subtitles.py",
    SKILL_DIRS["video"] / "export_subtitles.py",
    SKILL_DIRS["video"] / "render.py",
    SKILL_DIRS["qa"] / "video_qa.py",
]


class ProjectError(ValueError):
    pass


class Blocked(RuntimeError):
    pass


def load_project(path: Path, override: dict | None = None) -> dict:
    path = Path(path).resolve()
    raw = read_json(path)
    if raw is None:
        raise ProjectError(f"không thấy file dự án: {path}")
    raw = {**raw, **(override or {})}
    cfg = {**DEFAULTS, **raw}
    for key in ("tts", "chuan_hoa", "ho_so"):
        cfg[key] = {**DEFAULTS[key], **raw.get(key, {})}
    base = path.parent

    def rel(p):
        return None if p in (None, "") else (base / p).resolve()

    cfg["_file"], cfg["_dir"] = str(path), base
    for key in ("kich_ban", "audio", "phu_de"):
        cfg[key] = rel(cfg[key])
    cfg["media"] = [rel(m) for m in cfg["media"]]
    errors = []
    if not cfg["kich_ban"] or not cfg["kich_ban"].exists():
        errors.append(f"thiếu kịch bản: {cfg['kich_ban']}")
    if cfg["audio"] and not cfg["audio"].exists():
        errors.append(f"không thấy audio: {cfg['audio']}")
    if cfg["phu_de"] and not cfg["phu_de"].exists():
        errors.append(f"không thấy phụ đề: {cfg['phu_de']}")
    errors += video.check_media(cfg["media"])
    errors += do_hoa.check_config(cfg["do_hoa"])
    if cfg["ti_le"] not in video.SIZES:
        errors.append(f"ti_le phải là một trong {sorted(video.SIZES)}")
    unknown = set(cfg["kiem_tra"]) - set(checks.DEFAULTS)
    if unknown:
        errors.append(f"kiem_tra có khoá lạ {sorted(unknown)} — xem tan_studio/data/nguong.json")
    if errors:
        raise ProjectError("; ".join(errors))
    return cfg


def config_snapshot(cfg: dict) -> dict:
    """Cấu hình đầy đủ để chạy lại (đường dẫn tuyệt đối), không có khoá nội bộ."""
    snap = {k: copy.deepcopy(v) for k, v in cfg.items() if not k.startswith("_")}
    for key in ("kich_ban", "audio", "phu_de"):
        snap[key] = str(snap[key]) if snap[key] else None
    snap["media"] = [str(m) for m in snap["media"]]
    return snap


def config_hash(snap: dict) -> str:
    """Mã cấu hình: bỏ đường dẫn tệp và tên, chỉ còn lựa chọn xử lý — so sánh được giữa dự án."""
    keyed = {k: v for k, v in snap.items()
             if k not in ("ten", "kich_ban", "audio", "phu_de", "media", "thu_muc_ket_qua")}
    return sha_text(json.dumps(keyed, sort_keys=True, ensure_ascii=False))[:12]


def versions(project_dir: Path) -> dict:
    def git(*args):
        try:
            r = subprocess.run(["git", "-C", str(REPO_ROOT), *args], capture_output=True, text=True, timeout=10)
            return r.stdout.strip() if r.returncode == 0 else None
        except (OSError, subprocess.TimeoutExpired):
            return None
    code = hashlib.sha256()
    for f in sorted(Path(__file__).parent.glob("*.py")) + sorted(Path(__file__).parent.glob("data/*.json")):
        code.update(f.read_bytes())
    return {
        "tan_studio": __version__,
        "tan_studio_ma_nguon": code.hexdigest()[:12],
        "git_commit": git("rev-parse", "--short", "HEAD"),
        "git_co_thay_doi_chua_commit": bool(git("status", "--porcelain")),
        "tep_skill": {f.name: sha_text(f.read_text(encoding="utf-8"))[:12] for f in TRACKED_FILES if f.exists()},
        "quy_tac_ap_dung": [{k: e[k] for k in ("id", "phien_ban", "pham_vi")}
                            for e in rules.active_pronunciations(project_dir)],
    }


# ---------- các bước ----------

def step_chuan_hoa(cfg, run_dir, report):
    data = normalize.normalize_script(cfg["kich_ban"], cfg["chuan_hoa"]["tat_quy_tac"],
                                      rules.active_pronunciations(cfg["_dir"]))
    write_json(run_dir / "chuan-hoa.json", data)
    (run_dir / "chuan-hoa.txt").write_text(data["normalized_text"] + "\n", encoding="utf-8")
    counts = {}
    for s in data["segments"]:
        for c in s["changes"]:
            counts[c["quy_tac"]] = counts.get(c["quy_tac"], 0) + 1
    return {"outputs": {"chuan_hoa": str(run_dir / "chuan-hoa.json"), "van_ban": str(run_dir / "chuan-hoa.txt")},
            "tom_tat": {"so_doan": len(data["segments"]), "thay_doi_theo_quy_tac": counts,
                        "so_cho_can_xem_lai": sum(len(s["flags"]) for s in data["segments"])}}


def step_giong_doc(cfg, run_dir, report):
    if cfg["audio"]:
        return {"status": "SKIPPED", "reason": f"dùng audio có sẵn: {cfg['audio']}"}
    data = read_json(run_dir / "chuan-hoa.json")
    t = cfg["tts"]
    res = tts.synthesize(data, run_dir / "giong-doc", t["engine"], t["giong"], t["phong_cach"],
                         t["toc_do"], t["khoang_lang_ms"], t["mp3"])
    warnings = []
    if res["placeholder"]:
        warnings.append(f"engine '{res['engine']}' tạo audio GIẢ (tiếng bíp) — không phải giọng đọc")
    if res["failures"]:
        raise tts.EngineError(f"{len(res['failures'])} đoạn đọc lỗi: {res['failures']}")
    return {"outputs": {"audio": res["audio"], "tts": str(run_dir / "giong-doc" / "tts.json")},
            "warnings": warnings,
            "engine": {k: res.get(k) for k in ("engine", "version", "voice", "style", "speed", "gap_ms",
                                               "placeholder", "sample_rate", "duration", "format")}}


def _audio_path(cfg, run_dir) -> Path:
    if cfg["audio"]:
        return cfg["audio"]
    res = read_json(run_dir / "giong-doc" / "tts.json")
    if not res or not res.get("audio"):
        raise tts.EngineError("chưa có audio — chạy bước giong_doc trước")
    return Path(res["audio"])


def step_phu_de(cfg, run_dir, report):
    out = run_dir / "phu-de.srt"
    if cfg["phu_de"]:
        shutil.copyfile(cfg["phu_de"], out)
        method = "file_co_san"
    else:
        data = read_json(run_dir / "chuan-hoa.json")
        if cfg["audio"]:
            cues = subtitles.cues_from_duration(data["segments"], video.video_qa.duration_of(cfg["audio"]),
                                                cfg["ti_le"])
            method = "ti_le_so_chu"
        else:
            cues = subtitles.cues_from_tts(data["segments"],
                                           read_json(run_dir / "giong-doc" / "tts.json")["segments"], cfg["ti_le"])
            method = "moc_doan_tts"
        subtitles.write_srt(cues, out, cfg["ti_le"])
    note = {"moc_doan_tts": "mốc đoạn chính xác, trong đoạn chia theo số ký tự (ước lượng)",
            "ti_le_so_chu": "chia cả bài theo số ký tự — ước lượng, nên xem lại",
            "file_co_san": "dùng file phụ đề của người dùng"}[method]
    return {"outputs": {"srt": str(out)}, "phuong_phap": method, "ghi_chu": note,
            "so_cue": len(subtitles.read_srt(out))}


def _save_findings(run_dir: Path, findings: list[dict], replace_steps: set[str]) -> list[dict]:
    old = read_json(run_dir / "phat-hien.json", {"phat_hien": []})["phat_hien"]
    merged = [f for f in old if f["buoc"] not in replace_steps] + findings
    write_json(run_dir / "phat-hien.json", {"kind": "Findings", "luc": now(), "phat_hien": merged})
    return merged


def step_kiem_truoc(cfg, run_dir, report):
    t = checks.thresholds(cfg["kiem_tra"])
    norm = read_json(run_dir / "chuan-hoa.json")
    audio = _audio_path(cfg, run_dir)
    found = checks.check_script(norm, t)
    found += checks.check_audio(read_json(run_dir / "giong-doc" / "tts.json"), audio, t)
    found += checks.check_subs(run_dir / "phu-de.srt", video.video_qa.duration_of(audio),
                               subtitles.LINE[cfg["ti_le"]], t)
    _save_findings(run_dir, found, {"chuan_hoa", "giong_doc", "phu_de"})
    result = {"outputs": {"phat_hien": str(run_dir / "phat-hien.json")}, "phat_hien": checks.summary(found),
              "warnings": [checks.describe(f) for f in found if f["muc_do"] != "thong_tin"]}
    errors = [f for f in found if f["muc_do"] == "loi"]
    if errors and t["chan_khi_loi"]:
        raise Blocked(f"{len(errors)} lỗi chặn xuất video: " + "; ".join(checks.describe(f) for f in errors[:5]))
    return result


def step_dung_video(cfg, run_dir, report):
    srt = run_dir / "phu-de.srt"
    if not srt.exists():
        raise ProjectError("chưa có phu-de.srt — chạy bước phu_de trước")
    preview = report.get("xem_truoc", False)
    name = f"{cfg['ten']}.xem-truoc.mp4" if preview else f"{cfg['ten']}.mp4"
    audio = _audio_path(cfg, run_dir)
    overlays = (do_hoa.overlays(cfg["do_hoa"], cfg["ti_le"], run_dir / "do-hoa", video.video_qa.duration_of(audio))
                if cfg["do_hoa"] else None)
    res = video.render_video(audio, subtitles.read_srt(srt), cfg["media"],
                             run_dir / name, cfg["ti_le"], preview=preview, overlays=overlays)
    return {"outputs": {"video": res["video"], "ass": res["ass"]}, "timeline": res["timeline"],
            "command": res["command"]}


def step_kiem_tra(cfg, run_dir, report):
    vid = next((s for s in report["steps"] if s["name"] == "dung_video"), {}).get("outputs", {}).get("video")
    if not vid or not Path(vid).exists():
        raise ProjectError("chưa có video — chạy bước dung_video trước")
    audio = _audio_path(cfg, run_dir)
    t = checks.thresholds(cfg["kiem_tra"])
    w, h = video.frame_size(cfg["ti_le"], report.get("xem_truoc", False))
    found = checks.check_video(Path(vid), w, h, video.video_qa.duration_of(audio), t)
    qa = video.qa(Path(vid), audio)
    write_json(run_dir / "qa.json", qa)
    _save_findings(run_dir, found, {"dung_video"})
    result = {"outputs": {"qa": str(run_dir / "qa.json"), "phat_hien": str(run_dir / "phat-hien.json")},
              "qa_ky_thuat": qa["status"], "phat_hien": checks.summary(found),
              "warnings": [checks.describe(f) for f in found if f["muc_do"] != "thong_tin"] + qa["warnings"]}
    errors = [f for f in found if f["muc_do"] == "loi"]
    if qa["status"] == "FAIL" or errors:
        raise Blocked("QA kỹ thuật FAIL: " + "; ".join(qa["errors"] + [checks.describe(f) for f in errors]))
    return result


STEP_FN = {"chuan_hoa": step_chuan_hoa, "giong_doc": step_giong_doc, "phu_de": step_phu_de,
           "kiem_truoc": step_kiem_truoc, "dung_video": step_dung_video, "kiem_tra": step_kiem_tra}


# ---------- điều phối ----------

def runs_root(cfg) -> Path:
    return cfg["_dir"] / cfg["thu_muc_ket_qua"]


def _new_run_dir(cfg) -> Path:
    base = stamp()
    for n in range(1, 100):
        d = runs_root(cfg) / (base if n == 1 else f"{base}-{n}")
        try:
            d.mkdir(parents=True)
            return d
        except FileExistsError:
            continue
    raise ProjectError("không tạo được thư mục lần chạy mới")


def overall(steps: list[dict]) -> str:
    if any(s["status"] == "FAILED" for s in steps):
        return "FAILED"
    if any(s["status"] == "NOT_RUN" for s in steps):
        return "INCOMPLETE"
    if any(s.get("warnings") for s in steps):
        return "DONE_WITH_WARNINGS"
    return "DONE"


def _inputs(cfg) -> dict:
    return {"kich_ban": fingerprint_file(cfg["kich_ban"]),
            "audio": fingerprint_file(cfg["audio"]) if cfg["audio"] else None,
            "phu_de": fingerprint_file(cfg["phu_de"]) if cfg["phu_de"] else None,
            "media": [fingerprint_file(m) for m in cfg["media"]]}


def run(project: Path, steps: list[str] | None = None, run_id: str | None = None, log=print,
        xem_truoc: bool = False, override: dict | None = None, chay_lai_tu: str | None = None) -> dict:
    cfg = load_project(project, override)
    steps = steps or STEPS
    bad = set(steps) - set(STEPS)
    if bad:
        raise ProjectError(f"không có bước {sorted(bad)}; các bước: {STEPS}")
    if run_id:
        run_dir = runs_root(cfg) / run_id
        report = read_json(run_dir / "run.json")
        if report is None:
            raise ProjectError(f"không thấy lần chạy {run_id}")
        if report["ho_so"].get("da_xoa_van_ban"):
            raise ProjectError("lần chạy này đã xoá văn bản (luu_van_ban=false) — không chạy tiếp được, dùng chay-lai")
    else:
        run_dir = _new_run_dir(cfg)
        snap = config_snapshot(cfg)
        report = {
            "kind": "RunReport", "run_id": run_dir.name, "run_dir": str(run_dir), "project": cfg["ten"],
            "project_file": cfg["_file"], "created_at": now(), "app_version": f"tan_studio {__version__}",
            "config_hash": config_hash(snap), "config": snap, "versions": versions(cfg["_dir"]),
            "inputs": _inputs(cfg), "ho_so": dict(cfg["ho_so"]), "xem_truoc": xem_truoc,
            "chay_lai_tu": chay_lai_tu, "noi_dung": "chua_danh_gia",
            "steps": [{"name": s, "status": "NOT_RUN", "reason": "chưa chạy"} for s in STEPS],
        }
    by_name = {s["name"]: s for s in report["steps"]}
    failed = False
    for name in STEPS:
        if name not in steps:
            continue
        entry = by_name[name]
        if failed:
            entry.clear()
            entry.update(name=name, status="NOT_RUN", reason="bước trước bị lỗi hoặc bị chặn")
            continue
        log(f"[{name}] đang chạy...")
        entry.clear()
        entry.update(name=name, started_at=now())
        t0 = time.perf_counter()
        try:
            result = STEP_FN[name](cfg, run_dir, report) or {}
            entry["status"] = result.pop("status", "DONE")
            entry.update(result)
        except Exception as exc:
            entry.update(status="FAILED", error=f"{type(exc).__name__}: {exc}")
            if not isinstance(exc, (Blocked, ProjectError, tts.EngineError, video.VideoError, do_hoa.DoHoaError)):
                entry["trace"] = traceback.format_exc(limit=3)
            failed = True
        entry["ended_at"] = now()
        entry["duration_s"] = round(time.perf_counter() - t0, 2)
        log(f"[{name}] {entry['status']} ({entry['duration_s']}s)"
            + (f" — {entry.get('error') or entry.get('reason')}" if entry["status"] in ("FAILED", "SKIPPED") else ""))
        report["status"] = overall(report["steps"])
        report["updated_at"] = now()
        save(report, run_dir)
    report["status"] = overall(report["steps"])
    if not report["ho_so"].get("luu_van_ban", True):
        scrub_text(run_dir)
        report["ho_so"]["da_xoa_van_ban"] = True
    save(report, run_dir)
    return report


def rerun(project: Path, run_id: str, log=print) -> dict:
    """Chạy lại một lần chạy cũ với ĐÚNG cấu hình đã lưu, ra lần chạy mới (để so-sanh)."""
    cfg = load_project(project)
    old = read_json(runs_root(cfg) / run_id / "run.json")
    if old is None:
        raise ProjectError(f"không thấy lần chạy {run_id}")
    report = run(project, None, None, log, old.get("xem_truoc", False), override=old["config"],
                 chay_lai_tu=run_id)
    notes = []
    changed = [k for k in ("kich_ban", "audio", "phu_de")
               if (old["inputs"].get(k) or {}).get("sha256") != (report["inputs"].get(k) or {}).get("sha256")]
    if changed:
        notes.append(f"đầu vào đã đổi so với lần gốc: {changed}")
    if old["versions"].get("tan_studio_ma_nguon") != report["versions"]["tan_studio_ma_nguon"]:
        notes.append("mã nguồn tan_studio đã đổi so với lần gốc")
    if old["versions"].get("quy_tac_ap_dung") != report["versions"]["quy_tac_ap_dung"]:
        notes.append("bộ quy tắc học được đã đổi so với lần gốc")
    if notes:
        report["canh_bao_chay_lai"] = notes
        save(report, Path(report["run_dir"]))
    return report


def scrub_text(run_dir: Path) -> None:
    """ho_so.luu_van_ban = false: bỏ văn bản script khỏi hồ sơ, chỉ giữ băm + độ dài + id quy tắc."""
    norm = read_json(run_dir / "chuan-hoa.json")
    if norm:
        for s in norm["segments"]:
            for key in ("original", "normalized"):
                if isinstance(s[key], str):
                    s[key] = {"sha256": sha_text(s[key]), "so_ky_tu": len(s[key])}
            s["changes"] = [{"quy_tac": c["quy_tac"], "ly_do": c["ly_do"]} for c in s["changes"]]
            s["flags"] = [{"loai": f["loai"], "ly_do": f["ly_do"]} for f in s["flags"]]
        norm["original_text"] = norm["normalized_text"] = "(đã xoá theo ho_so.luu_van_ban=false)"
        write_json(run_dir / "chuan-hoa.json", norm)
    (run_dir / "chuan-hoa.txt").unlink(missing_ok=True)
    t = read_json(run_dir / "giong-doc" / "tts.json")
    if t:
        for s in t["segments"]:
            s["text"] = None
        write_json(run_dir / "giong-doc" / "tts.json", t)
    found = read_json(run_dir / "phat-hien.json")
    if found:
        for f in found["phat_hien"]:
            f["vi_tri"].pop("doan_van", None)
        write_json(run_dir / "phat-hien.json", found)


def save(report: dict, run_dir: Path) -> None:
    write_json(run_dir / "run.json", report)
    (run_dir / "bao-cao.md").write_text(render_report(report), encoding="utf-8")


NOI_DUNG = {"chua_danh_gia": "CHƯA ĐÁNH GIÁ — máy chỉ kiểm kỹ thuật; cần người xem/nghe rồi `xem-lai chap-nhan|tu-choi`",
            "chap_nhan": "người dùng CHẤP NHẬN", "tu_choi": "người dùng TỪ CHỐI"}


def render_report(r: dict) -> str:
    v = r.get("versions") or {}
    lines = [f"# Báo cáo lần chạy {r['run_id']} — {r['project']}", "",
             f"Kỹ thuật: **{r.get('status', '?')}**"
             + (" (XEM TRƯỚC, độ phân giải thấp)" if r.get("xem_truoc") else "") + "  ",
             f"Nội dung: **{NOI_DUNG.get(r.get('noi_dung', 'chua_danh_gia'))}**  ",
             f"Bắt đầu: {r['created_at']} — cập nhật: {r.get('updated_at', '')}  ",
             f"Phiên bản: {r.get('app_version')} · mã cấu hình `{r.get('config_hash')}` · git {v.get('git_commit')}"
             + (" (có thay đổi chưa commit)" if v.get("git_co_thay_doi_chua_commit") else "") + "  "]
    if r.get("chay_lai_tu"):
        lines.append(f"Chạy lại từ: {r['chay_lai_tu']}  ")
    for w in r.get("canh_bao_chay_lai", []):
        lines.append(f"⚠ {w}  ")
    lines += ["", "## Đầu vào", ""]
    for k, val in r["inputs"].items():
        for fp in (val if isinstance(val, list) else [val] if val else []):
            lines.append(f"- {k}: {Path(fp['path']).name} ({fp['size']} byte, sha256 {fp['sha256'][:12]})")
    used = v.get("quy_tac_ap_dung") or []
    if used:
        lines.append("- quy tắc học được đang bật: " + ", ".join(f"{x['id']} v{x['phien_ban']} ({x['pham_vi']})"
                                                               for x in used))
    lines += ["", "## Các bước", "", "| Bước | Trạng thái | Thời gian | Ghi chú |", "|---|---|---|---|"]
    for s in r["steps"]:
        note = s.get("error") or s.get("reason") or s.get("ghi_chu") or ""
        if s.get("phat_hien"):
            note = f"phát hiện {s['phat_hien']} {note}"
        dur = f"{s['duration_s']}s" if "duration_s" in s else ""
        lines.append(f"| {s['name']} | {s['status']} | {dur} | {str(note).replace('|', '/')[:220]} |")
    warns = [(s["name"], w) for s in r["steps"] for w in s.get("warnings", [])]
    if warns:
        lines += ["", "## Cảnh báo (vị trí: lý do → gợi ý  #id để `xem-lai canh-bao`)", ""]
        lines += [f"- [{n}] {w}" for n, w in warns[:40]]
        if len(warns) > 40:
            lines.append(f"- … còn {len(warns) - 40} cảnh báo trong phat-hien.json")
    outs = [(s["name"], k, val) for s in r["steps"] for k, val in s.get("outputs", {}).items()]
    if outs:
        lines += ["", "## File đầu ra", ""] + [f"- [{n}] {k}: {val}" for n, k, val in outs]
    return "\n".join(lines) + "\n"


def list_runs(cfg) -> list[Path]:
    root = runs_root(cfg)
    return sorted(p.parent for p in root.glob("*/run.json")) if root.exists() else []


def resolve_run(cfg, run_id: str | None) -> Path:
    if run_id:
        d = runs_root(cfg) / run_id
        if not (d / "run.json").exists():
            raise ProjectError(f"không thấy lần chạy {run_id}")
        return d
    runs = list_runs(cfg)
    if not runs:
        raise ProjectError("dự án chưa có lần chạy nào")
    return runs[-1]


def set_content_verdict(run_dir: Path, ket_luan: str) -> None:
    report = read_json(run_dir / "run.json")
    report["noi_dung"] = ket_luan
    report["updated_at"] = now()
    save(report, run_dir)
