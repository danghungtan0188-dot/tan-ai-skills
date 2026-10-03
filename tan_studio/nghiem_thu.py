"""Workflow mẫu + tiêu chí nghiệm thu. Mọi thay đổi liên quan tới tan_studio phải qua lệnh này.

Chạy trên BẢN SAO SẠCH của tan_studio/vi-du/ (không bị quy tắc/kết quả cũ ảnh hưởng), vào
outputs/nghiem-thu/<thời điểm>/. Tiêu chí ở vi-du/nghiem-thu.json. Chỉ kiểm được kỹ thuật và văn bản:
kết luận luôn ghi rõ nội dung nghe nhìn CHƯA được đánh giá.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from . import REPO_ROOT, read_json, stamp
from . import workflow

SAMPLE = Path(__file__).resolve().parent / "vi-du"


def run(engine: str = "thu-nghiem", out_root: Path | None = None, log=print) -> dict:
    spec = read_json(SAMPLE / "nghiem-thu.json")
    work = Path(out_root or REPO_ROOT / "outputs" / "nghiem-thu") / f"{stamp()}-{engine}"
    work.mkdir(parents=True)
    for name in spec["tep"]:
        shutil.copyfile(SAMPLE / name, work / name)
    project = work / spec["du_an"]
    report = workflow.run(project, log=log, override={"tts": {**read_json(project)["tts"], "engine": engine}})
    run_dir = Path(report["run_dir"])
    steps = {s["name"]: s for s in report["steps"]}
    norm = read_json(run_dir / "chuan-hoa.json") or {"normalized_text": "", "segments": []}
    found = read_json(run_dir / "phat-hien.json", {"phat_hien": []})["phat_hien"]
    timeline = steps["dung_video"].get("timeline") or {}
    results = []

    def crit(name, ok, detail=""):
        results.append({"tieu_chi": name, "dat": bool(ok), "chi_tiet": "" if ok else detail})

    bad = [n for n, s in steps.items() if s["status"] not in ("DONE", "SKIPPED")]
    crit("mọi bước chạy xong", not bad, f"chưa xong: {bad}" if bad else "")
    for text in spec["van_ban_chuan_hoa_phai_co"]:
        crit(f"chuẩn hoá có '{text}'", text in norm["normalized_text"])
    for text in spec["van_ban_chuan_hoa_khong_duoc_co"]:
        crit(f"chuẩn hoá không còn '{text}'", text not in norm["normalized_text"])
    fps = {f["dau_van_tay"] for f in found}
    for fp in spec["phat_hien_phai_co"]:
        crit(f"phát hiện '{fp}'", fp in fps, f"có: {sorted(fps)[:8]}")
    crit("kích thước khung đúng", timeline.get("khung") == spec["khung"], f"{timeline.get('khung')}")
    crit("QA kỹ thuật PASS", steps["kiem_tra"].get("qa_ky_thuat") == "PASS", steps["kiem_tra"].get("error", ""))
    srt = run_dir / "phu-de.srt"
    crit("phụ đề hiện chữ gốc", srt.exists() and spec["phu_de_phai_co"] in srt.read_text(encoding="utf-8"))
    crit("hồ sơ có phiên bản + mã cấu hình", bool(report.get("config_hash") and report["versions"].get("tan_studio")))
    ok = all(r["dat"] for r in results)
    return {"thu_muc": str(work), "run_id": report["run_id"], "engine": engine, "tieu_chi": results,
            "ket_luan_ky_thuat": "ĐẠT" if ok else "KHÔNG ĐẠT",
            "noi_dung": "CHƯA ĐÁNH GIÁ — cần người nghe/xem" + (" (audio giả)" if engine == "thu-nghiem" else "")}
