"""Review của người dùng — lưu ở <thư mục dự án>/hoc/.

quan-sat.jsonl   QUAN SÁT: một lỗi/phản hồi của một lần chạy (tầng 1). Gộp trùng bằng `trung_voi`.
danh-gia.jsonl   chấp nhận / từ chối video; đúng / sai cho từng cảnh báo tự động.
Quan sát loại phat_am có `tu` + `doc_dung` -> tự sinh QUY TẮC ĐỀ XUẤT (tầng 2), chưa áp dụng.
"""

from __future__ import annotations

import secrets
from pathlib import Path

from . import check_sensitive, now, read_json, read_jsonl, stamp, write_jsonl
from . import rules

LOAI = {  # loại vấn đề -> bước workflow chịu trách nhiệm
    "script": "chuan_hoa", "phat_am": "giong_doc", "giong_doc": "giong_doc", "hinh_anh": "dung_video",
    "chon_canh": "dung_video", "nhip_dung": "dung_video", "phu_de": "phu_de", "am_thanh": "giong_doc",
    "thuong_hieu": "dung_video", "ky_thuat": "kiem_tra",
}
UU_TIEN = ("cao", "trung_binh", "thap")


class ReviewError(ValueError):
    pass


def hoc_dir(project_dir: Path) -> Path:
    return Path(project_dir) / "hoc"


def observations(project_dir: Path) -> list[dict]:
    return read_jsonl(hoc_dir(project_dir) / "quan-sat.jsonl")


def verdicts(project_dir: Path) -> list[dict]:
    return read_jsonl(hoc_dir(project_dir) / "danh-gia.jsonl")


def _append(path: Path, item: dict) -> None:
    write_jsonl(path, read_jsonl(path) + [item])


def _context(run_dir: Path | None, tu: str | None, doan: int | None) -> str | None:
    """Câu gốc chứa từ bị lỗi — làm ví dụ trước/sau và ca kiểm thử cho quy tắc."""
    norm = read_json(run_dir / "chuan-hoa.json") if run_dir else None
    if not norm:
        return None
    for s in norm["segments"]:
        orig = s.get("original")
        if not isinstance(orig, str):
            return None  # lần chạy đã tắt lưu văn bản
        if (doan is None or s["index"] == doan) and (tu is None or tu in orig):
            if tu:
                for sent in orig.replace("!", ".").replace("?", ".").split("."):
                    if tu in sent:
                        return sent.strip() + "."
            return orig
    return None


def add_observation(project_dir: Path, project: dict, run_dir: Path | None, loai: str, mo_ta: str,
                    tu: str | None = None, doc_dung: str | None = None, doan: int | None = None,
                    thoi_diem: float | None = None, canh: int | None = None, de_xuat: str = "",
                    uu_tien: str = "trung_binh", pham_vi: str = "du_an", nguon: str = "nguoi_dung",
                    phat_hien: str | None = None) -> dict:
    if loai not in LOAI:
        raise ReviewError(f"loại phải là một trong {sorted(LOAI)}")
    if uu_tien not in UU_TIEN:
        raise ReviewError(f"ưu tiên phải là {UU_TIEN}")
    if pham_vi not in ("du_an", "chung"):
        raise ReviewError("phạm vi đề nghị: du_an (chỉ dự án này) hoặc chung (đề xuất thành quy tắc dùng chung)")
    try:
        check_sensitive(mo_ta, de_xuat, tu or "", doc_dung or "")
    except ValueError as exc:
        raise ReviewError(str(exc)) from exc
    run_id = run_dir.name if run_dir else None
    vi_tri = {k: v for k, v in {"doan": doan, "tu": tu, "thoi_diem": thoi_diem, "canh": canh}.items() if v is not None}
    fp = f"tu:{tu}" if tu else f"{loai}:{mo_ta.strip().lower()[:60]}"
    previous = [o for o in observations(project_dir) if o["dau_van_tay"] == fp]
    obs = {"kind": "Observation", "id": f"qs-{stamp()}-{secrets.token_hex(2)}", "lan_chay": run_id,
           "luc": now(), "loai": loai, "buoc": LOAI[loai], "vi_tri": vi_tri, "mo_ta": mo_ta,
           "de_xuat": de_xuat or (f"đọc là: {doc_dung}" if doc_dung else ""), "uu_tien": uu_tien,
           "pham_vi_de_nghi": pham_vi, "nguon": nguon, "phat_hien": phat_hien, "dau_van_tay": fp,
           "trung_voi": previous[0]["id"] if previous else None,
           "lap_lai_tu_lan_chay": sorted({o["lan_chay"] for o in previous if o["lan_chay"] and o["lan_chay"] != run_id}),
           "quy_tac": None}
    if loai == "phat_am" and tu and doc_dung:
        ctx = _context(run_dir, tu, doan) or f"{tu}."
        rule = rules.propose(project_dir, project, tu, doc_dung, ctx, obs["id"], run_id,
                             "du_an" if pham_vi == "du_an" else "he_thong")
        obs["quy_tac"] = rule["id"]
    _append(hoc_dir(project_dir) / "quan-sat.jsonl", obs)
    return obs


def verdict(project_dir: Path, run_dir: Path, ket_luan: str, ghi_chu: str = "") -> dict:
    if ket_luan not in ("chap_nhan", "tu_choi"):
        raise ReviewError("kết luận: chap_nhan hoặc tu_choi")
    check_sensitive(ghi_chu)
    item = {"kind": "Verdict", "lan_chay": run_dir.name, "ket_luan": ket_luan, "ghi_chu": ghi_chu, "luc": now()}
    _append(hoc_dir(project_dir) / "danh-gia.jsonl", item)
    return item


def finding_verdict(project_dir: Path, project: dict, run_dir: Path, finding_id: str, dung: bool,
                    ghi_chu: str = "") -> dict:
    """Người dùng xác nhận cảnh báo tự động đúng/sai. Đúng -> thành quan sát; sai -> ghi nhận cảnh báo sai."""
    found = next((f for f in read_json(run_dir / "phat-hien.json", {"phat_hien": []})["phat_hien"]
                  if f["id"] == finding_id), None)
    if found is None:
        raise ReviewError(f"lần chạy {run_dir.name} không có phát hiện {finding_id}")
    item = {"kind": "FindingVerdict", "lan_chay": run_dir.name, "phat_hien": finding_id, "ma": found["ma"],
            "ket_luan": "dung" if dung else "sai", "ghi_chu": ghi_chu, "luc": now()}
    _append(hoc_dir(project_dir) / "danh-gia.jsonl", item)
    if dung:
        loai = {"chuan_hoa": "script", "giong_doc": "giong_doc", "phu_de": "phu_de"}.get(found["buoc"], "ky_thuat")
        add_observation(project_dir, project, run_dir, loai, f"[tự động] {found['ly_do']}",
                        tu=found["vi_tri"].get("tu"), doan=found["vi_tri"].get("doan"),
                        thoi_diem=found["vi_tri"].get("thoi_diem"), nguon="tu_dong", phat_hien=finding_id)
    return item
