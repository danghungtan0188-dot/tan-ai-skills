"""Đánh giá TTS lặp lại được trên bộ câu mẫu (data/tts_cases.json).

Mỗi lần chạy một thư mục riêng (không ghi đè). Chấm tự động bằng ASR là TUỲ CHỌN và chỉ là
tín hiệu tham khảo: whisper small nghe sai tiếng Việt khá nhiều (đặc biệt tên riêng), nên
nghe nhiều lượt lấy đa số, và có chấm tay (`cham`) để ghi kết luận của người nghe.
"""

from __future__ import annotations

import csv
import importlib.util
import re
import unicodedata
from pathlib import Path

from . import DATA, now, read_json, stamp, write_json
from . import normalize, rules, tts

import normalize_vi  # noqa: E402

CASES_FILE = DATA / "tts_cases.json"
TEMPERATURES = [0.0, 0.4, 0.6, 0.8, 1.0]


# Bỏ dấu kiểu cũ/mới ("uỷ"/"ủy", "hoà"/"hòa") — whisper và người viết dùng lẫn lộn.
_OLD_TONE = {"oà": "òa", "oá": "óa", "oả": "ỏa", "oã": "õa", "oạ": "ọa",
             "uỳ": "ùy", "uý": "úy", "uỷ": "ủy", "uỹ": "ũy", "uỵ": "ụy"}


def _clean(text: str) -> str:
    """Chuẩn hoá transcript/từ khoá để so: số về chữ, chữ thường, bỏ dấu câu, thống nhất bỏ dấu."""
    text = unicodedata.normalize("NFC", normalize_vi.normalize_numbers(text)).lower()
    for old, new in _OLD_TONE.items():
        text = text.replace(old, new)
    text = " ".join(re.sub(r"[^\w\s]", " ", text).split())
    return text.replace("tháng bốn", "tháng tư")  # whisper ghi "tháng 4"


def transcribe(wavs: dict[str, Path], passes: int) -> dict[str, list[str]]:
    from faster_whisper import WhisperModel

    model = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4, num_workers=1)
    out = {}
    for case_id, wav in wavs.items():
        out[case_id] = []
        for temp in TEMPERATURES[:passes]:
            segs, _ = model.transcribe(str(wav), language="vi", beam_size=1, temperature=temp,
                                       condition_on_previous_text=False)
            out[case_id].append(" ".join(s.text.strip() for s in segs))
    return out


def run_eval(out_root: Path, engine: str = "vieneu", voice: str = "nam", style: str = "tin_tuc",
             asr: bool = False, passes: int = 3, cases_file: Path = CASES_FILE, log=print) -> Path:
    cases_doc = read_json(cases_file)
    eng = tts.get_engine(engine)
    reason = eng.check()
    if reason:
        raise tts.EngineError(reason)
    run_dir = Path(out_root) / f"{stamp()}-{engine}-{re.sub(r'[^0-9A-Za-z]+', '-', voice).strip('-') or 'giong'}"
    run_dir.mkdir(parents=True, exist_ok=False)

    cases = []
    active = rules.active_pronunciations(None)  # quy tắc cá nhân + hệ thống đã duyệt
    for c in cases_doc["cau"]:
        norm = normalize.normalize_text(c["van_ban"], phat_am=active)
        cases.append({**c, "chuan_hoa": norm["normalized"], "co": norm["flags"], "wav": None,
                      "loi": None, "asr": [], "trung": {}, "tu_dong": "CHUA_CHAM"})

    eng.open(voice, style)
    for c in cases:
        wav = run_dir / f"{c['id']}.wav"
        log(f"[đọc] {c['id']}")
        try:
            eng.synth(c["chuan_hoa"], wav)
            c["wav"] = str(wav)
        except Exception as exc:
            c["loi"] = str(exc)
            c["tu_dong"] = "LOI"

    asr_status = "NOT_RUN"
    asr_reason = "không bật --asr"
    if asr:
        if importlib.util.find_spec("faster_whisper") is None:
            asr_reason = "chưa cài faster-whisper"
        elif eng.placeholder:
            asr_reason = "audio giả, không có gì để nghe"
        else:
            log(f"[asr] whisper small, {passes} lượt/câu, 4 luồng")
            heard = transcribe({c["id"]: Path(c["wav"]) for c in cases if c["wav"]}, passes)
            for c in cases:
                if c["id"] not in heard:
                    continue
                c["asr"] = heard[c["id"]]
                cleaned = [_clean(t) for t in c["asr"]]
                c["trung"] = {k: sum(_clean(k) in t for t in cleaned) for k in c["tu_khoa"]}
                c["tu_dong"] = "DAT" if all(v * 2 > passes for v in c["trung"].values()) else "CHUA_DAT"
            asr_status, asr_reason = "DONE", f"whisper small, {passes} lượt, đạt khi đa số lượt nghe đúng từ khoá"

    result = {"kind": "TtsEvalRun", "run_id": run_dir.name, "created_at": now(),
              **eng.info(), "voice": voice, "style": style,
              "quy_tac_ap_dung": [f"{e['id']} v{e['phien_ban']}" for e in active],
              "cases_file": str(cases_file), "cases_version": cases_doc.get("phien_ban"),
              "asr": {"status": asr_status, "ghi_chu": asr_reason}, "cases": cases}
    write_json(run_dir / "ket-qua.json", result)
    write_reports(run_dir)
    return run_dir


def grade(run_dir: Path, case_id: str, verdict: str, note: str = "") -> dict:
    if verdict not in ("dat", "loi"):
        raise ValueError("kết luận phải là dat hoặc loi")
    result = read_json(Path(run_dir) / "ket-qua.json")
    if result is None or case_id not in {c["id"] for c in result["cases"]}:
        raise ValueError(f"không có câu {case_id} trong {run_dir}")
    manual = read_json(Path(run_dir) / "cham-tay.json", {})
    manual[case_id] = {"ket_luan": verdict, "ghi_chu": note, "luc": now()}
    write_json(Path(run_dir) / "cham-tay.json", manual)
    write_reports(run_dir)
    return manual[case_id]


def write_reports(run_dir: Path) -> None:
    run_dir = Path(run_dir)
    r = read_json(run_dir / "ket-qua.json")
    manual = read_json(run_dir / "cham-tay.json", {})
    with (run_dir / "ket-qua.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["id", "nhom", "van_ban", "chuan_hoa", "tu_dong", "cham_tay", "ghi_chu_tay", "asr_luot_1", "loi"])
        for c in r["cases"]:
            m = manual.get(c["id"], {})
            w.writerow([c["id"], c["nhom"], c["van_ban"], c["chuan_hoa"], c["tu_dong"], m.get("ket_luan", ""),
                        m.get("ghi_chu", ""), (c["asr"] or [""])[0], c["loi"] or ""])
    counts = {}
    for c in r["cases"]:
        counts[c["tu_dong"]] = counts.get(c["tu_dong"], 0) + 1
    lines = [f"# Đánh giá TTS {r['run_id']}", "",
             f"Engine: {r['engine']} {r['version']} — giọng {r['voice']} — phong cách {r['style']}  ",
             f"Bộ câu: {Path(r['cases_file']).name} (phiên bản {r['cases_version']})  ",
             f"ASR: {r['asr']['status']} — {r['asr']['ghi_chu']}  ",
             f"Tự động: {counts} — chấm tay: {len(manual)}/{len(r['cases'])} câu", ""]
    if r.get("placeholder"):
        lines += ["> Audio GIẢ (engine thử nghiệm) — kết quả không nói gì về chất lượng giọng.", ""]
    lines += ["> Điểm ASR chỉ là tín hiệu tham khảo, không phải đánh giá chất lượng tuyệt đối.", "",
              "| Câu | Nhóm | Tự động | Chấm tay | Trúng từ khoá |", "|---|---|---|---|---|"]
    for c in r["cases"]:
        hits = ", ".join(f"{k}: {v}" for k, v in c["trung"].items()) or "—"
        lines.append(f"| {c['id']} | {c['nhom']} | {c['tu_dong']} | {manual.get(c['id'], {}).get('ket_luan', '—')} | {hits} |")
    (run_dir / "bao-cao.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
