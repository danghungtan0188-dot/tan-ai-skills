#!/usr/bin/env python3
"""Bai thi video chuan: dau vao tu sinh -> tan_studio chay het -> phieu diem -> so voi moc chuan.

Dau vao sinh bang ffmpeg (2 clip mau, 3 anh mau) + kich ban mau cua tan_studio, giong
`thu-nghiem` (tieng bip, khong can mo hinh) -> chay nhanh, may khong nong, khong ban quyen.
Phieu diem chi kiem KY THUAT; noi dung nghe nhin van can nguoi xem.

  python evaluations/bai_thi.py                 # chay, cham, so voi evaluations/moc-chuan.json
  python evaluations/bai_thi.py --luu-moc       # chay roi ghi ket qua lam moc chuan moi (nguoi quyet)
  python evaluations/bai_thi.py --hong khung    # co tinh lam hong de kiem phieu diem bat duoc

Ket qua o outputs/bai-thi/<thoi diem>/ (da gitignore). Exit 0 = DAT va khong hoi quy, 1 = co loi.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tan_studio import read_json, stamp, workflow  # noqa: E402
from tan_studio import video as tvideo  # noqa: E402

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

MAU = REPO_ROOT / "tan_studio" / "vi-du"
MOC = Path(__file__).resolve().parent / "moc-chuan.json"
TI_LE, KHUNG = "9:16", "1080x1920"
LUFS_DICH, LUFS_SAI = -16.0, 1.5
LECH_TOI_DA = 0.3  # giay, video so voi giong doc
CACH_HONG = {
    "khung": "dung khung 16:9 trong khi bai thi doi 9:16",
    "thieu-media": "xoa mot file media sau khi khai bao",
    "chuan-hoa": "tat quy tac viet_tat (UBND, BHYT... khong duoc doc thanh chu)",
}

# (ten file, nguon lavfi, la clip?)
MEDIA = [
    ("canh-1.mp4", "testsrc2=s=1280x720:r=25:d=2", True),
    ("anh-1.png", "smptebars=s=1280x720", False),
    ("canh-2.mp4", "mandelbrot=s=720x1280:r=25", True),
    ("anh-2.png", "color=c=0x0b3a5c:s=1080x1080", False),
    ("anh-3.png", "rgbtestsrc=s=1280x720", False),
]


def sinh_dau_vao(thu_muc: Path) -> list[Path]:
    thu_muc.mkdir(parents=True, exist_ok=True)
    ra = []
    for ten, nguon, la_clip in MEDIA:
        tep = thu_muc / ten
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", nguon]
        cmd += (["-t", "2", "-c:v", "libx264", "-preset", "faster", "-pix_fmt", "yuv420p"] if la_clip
                else ["-frames:v", "1"])
        subprocess.run(cmd + [str(tep)], check=True, timeout=120)
        ra.append(tep)
    shutil.copyfile(MAU / "kich-ban.txt", thu_muc / "kich-ban.txt")
    return ra


def tao_du_an(thu_muc: Path, media: list[Path], hong: str | None) -> Path:
    du_an = {"ten": "bai-thi", "kich_ban": "kich-ban.txt", "media": [m.name for m in media],
             "ti_le": "16:9" if hong == "khung" else TI_LE, "tts": {"engine": "thu-nghiem"}}
    if hong == "chuan-hoa":
        du_an["chuan_hoa"] = {"tat_quy_tac": ["viet_tat"]}
    tep = thu_muc / "du-an.json"
    tep.write_text(json.dumps(du_an, ensure_ascii=False, indent=2), encoding="utf-8")
    if hong == "thieu-media":
        media[0].unlink()
    return tep


def do_lufs(video: Path) -> float | None:
    """Do loudness tich hop (I, LUFS) bang ebur128. video_qa chi ghi mean_volume (dB), khong phai LUFS."""
    ra = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(video), "-map", "0:a:0",
                         "-af", "ebur128=framelog=quiet", "-f", "null", "-"],
                        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    m = re.findall(r"^\s*I:\s*(-?\d+(?:\.\d+)?)\s*LUFS", ra.stderr, re.M)
    return float(m[-1]) if m else None


def cham(report: dict, spec: dict) -> dict:
    """Phieu diem tu ho so chay (run.json) va cac file trong thu muc chay."""
    run_dir = Path(report["run_dir"])
    steps = {s["name"]: s for s in report["steps"]}
    norm = (read_json(run_dir / "chuan-hoa.json") or {}).get("normalized_text", "")
    found = (read_json(run_dir / "phat-hien.json") or {}).get("phat_hien", [])
    timeline = steps.get("dung_video", {}).get("timeline") or {}
    audio_s = steps.get("dung_video", {}).get("timeline", {}).get("thoi_luong")
    vid = steps.get("dung_video", {}).get("outputs", {}).get("video")
    video_s = tvideo.video_qa.duration_of(Path(vid)) if vid and Path(vid).exists() else None
    lufs = do_lufs(Path(vid)) if video_s is not None else None
    srt = run_dir / "phu-de.srt"
    cues = _cues(srt) if srt.exists() else []

    tieu_chi = []

    def tc(ma, dat, do_duoc):
        tieu_chi.append({"ma": ma, "dat": bool(dat), "do_duoc": do_duoc})

    chua_xong = [n for n, s in steps.items() if s["status"] not in ("DONE", "SKIPPED")]
    tc("moi_buoc_xong", not chua_xong, chua_xong or "tat ca DONE")
    tc("qa_ky_thuat_pass", steps.get("kiem_tra", {}).get("qa_ky_thuat") == "PASS",
       steps.get("kiem_tra", {}).get("qa_ky_thuat") or steps.get("kiem_tra", {}).get("error"))
    loi = [f.get("ma") for f in found if f.get("muc_do") == "loi"]
    tc("khong_co_phat_hien_loi", not loi, loi or 0)
    tc("khung_dung", timeline.get("khung") == KHUNG, timeline.get("khung"))
    so_nen = len(timeline.get("nen") or [])
    tc("du_media", so_nen == len(MEDIA), f"{so_nen}/{len(MEDIA)}")
    lech = abs(video_s - audio_s) if video_s is not None and audio_s else None
    tc("thoi_luong_khop_giong", lech is not None and lech <= LECH_TOI_DA,
       None if lech is None else round(lech, 3))
    tc("am_luong_dung_dich", lufs is not None and abs(lufs - LUFS_DICH) <= LUFS_SAI, lufs)
    het = max((c[1] for c in cues), default=None)
    tc("phu_de_trong_thoi_luong", bool(cues) and audio_s is not None and het <= audio_s + 0.1,
       {"so_cue": len(cues), "ket_thuc": het})
    thieu = [t for t in spec["van_ban_chuan_hoa_phai_co"] if t not in norm]
    tc("chuan_hoa_doc_thanh_chu", not thieu, thieu or "du")
    con = [t for t in spec["van_ban_chuan_hoa_khong_duoc_co"] if t in norm]
    tc("chuan_hoa_khong_con_viet_tat", not con, con or "khong con")

    dat = sum(t["dat"] for t in tieu_chi)
    return {"kind": "PhieuDiem", "run_dir": str(run_dir), "diem": f"{dat}/{len(tieu_chi)}",
            "ket_luan": "DAT" if dat == len(tieu_chi) else "KHONG_DAT", "tieu_chi": tieu_chi,
            "so_do": {"lufs": lufs, "lech_thoi_luong_s": None if lech is None else round(lech, 3),
                      "so_canh_bao": sum(f.get("muc_do") == "canh_bao" for f in found),
                      "thoi_gian_chay_s": round(sum(s.get("duration_s", 0) for s in report["steps"]), 1)},
            "noi_dung": "CHUA DANH GIA — phieu nay chi kiem ky thuat, audio la tieng bip"}


def phieu_tu_choi(thu_muc: Path, ly_do: str) -> dict:
    """Du an bi tu choi ngay tu dau: moi tieu chi deu truot, ghi ly do vao tieu chi dau."""
    ma = ["moi_buoc_xong", "qa_ky_thuat_pass", "khong_co_phat_hien_loi", "khung_dung", "du_media",
          "thoi_luong_khop_giong", "am_luong_dung_dich", "phu_de_trong_thoi_luong",
          "chuan_hoa_doc_thanh_chu", "chuan_hoa_khong_con_viet_tat"]
    tieu_chi = [{"ma": m, "dat": False, "do_duoc": f"du an bi tu choi: {ly_do}" if i == 0 else "khong chay"}
                for i, m in enumerate(ma)]
    return {"kind": "PhieuDiem", "run_dir": str(thu_muc), "diem": f"0/{len(ma)}", "ket_luan": "KHONG_DAT",
            "tieu_chi": tieu_chi, "so_do": {"lufs": None, "lech_thoi_luong_s": None, "so_canh_bao": None,
                                            "thoi_gian_chay_s": 0},
            "noi_dung": "CHUA DANH GIA"}


def _cues(srt: Path) -> list[tuple[float, float]]:
    def giay(t):
        h, m, s = t.replace(",", ".").split(":")
        return int(h) * 3600 + int(m) * 60 + float(s)
    ra = []
    for dong in srt.read_text(encoding="utf-8").splitlines():
        if "-->" in dong:
            a, b = (x.strip() for x in dong.split("-->"))
            ra.append((giay(a), giay(b)))
    return ra


def so_moc(phieu: dict, moc: dict | None) -> list[str]:
    """Hoi quy: tieu chi moc chuan dat ma nay truot, hoac so do xau di qua nguong."""
    if not moc:
        return []
    truoc = {t["ma"]: t["dat"] for t in moc["tieu_chi"]}
    ra = [f"HOI QUY {t['ma']}: moc DAT, nay KHONG DAT ({t['do_duoc']})"
          for t in phieu["tieu_chi"] if truoc.get(t["ma"]) and not t["dat"]]
    a, b = moc["so_do"], phieu["so_do"]
    if a.get("so_canh_bao") is not None and (b["so_canh_bao"] or 0) > a["so_canh_bao"]:
        ra.append(f"CANH BAO tang: {a['so_canh_bao']} -> {b['so_canh_bao']}")
    return ra


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--hong", choices=sorted(CACH_HONG), help="co tinh lam hong de kiem phieu diem")
    ap.add_argument("--luu-moc", action="store_true", help="ghi phieu nay lam moc chuan (chi khi DAT)")
    args = ap.parse_args()

    thu_muc = REPO_ROOT / "outputs" / "bai-thi" / (stamp() + (f"-hong-{args.hong}" if args.hong else ""))
    t0 = time.perf_counter()
    media = sinh_dau_vao(thu_muc)
    du_an = tao_du_an(thu_muc, media, args.hong)
    try:
        report = workflow.run(du_an, log=lambda *_: None)
        phieu = cham(report, read_json(MAU / "nghiem-thu.json"))
    except workflow.ProjectError as exc:  # tan_studio tu choi du an truoc khi chay buoc nao
        phieu = phieu_tu_choi(thu_muc, str(exc))
    phieu["hong"] = args.hong
    phieu["tong_thoi_gian_s"] = round(time.perf_counter() - t0, 1)
    hoi_quy = so_moc(phieu, read_json(MOC) if MOC.exists() else None)
    phieu["hoi_quy"] = hoi_quy
    (thu_muc / "phieu-diem.json").write_text(json.dumps(phieu, ensure_ascii=False, indent=2), encoding="utf-8")

    for t in phieu["tieu_chi"]:
        print(f"{'DAT ' if t['dat'] else 'TRUOT'}  {t['ma']:<30} {t['do_duoc']}")
    print(f"\nDiem: {phieu['diem']}  ->  {phieu['ket_luan']}   ({phieu['tong_thoi_gian_s']}s)")
    print(f"So do: {phieu['so_do']}")
    for dong in hoi_quy:
        print(dong)
    if not MOC.exists():
        print("Chua co moc chuan. Chay lai voi --luu-moc khi phieu DAT.")
    print(f"Phieu diem: {thu_muc / 'phieu-diem.json'}")

    if args.luu_moc:
        if args.hong or phieu["ket_luan"] != "DAT":
            print("Khong luu moc: chi luu phieu DAT va khong co --hong.", file=sys.stderr)
            return 1
        moc = {k: phieu[k] for k in ("diem", "tieu_chi", "so_do")}
        MOC.write_text(json.dumps(moc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Da luu moc chuan: {MOC}")
    return 0 if phieu["ket_luan"] == "DAT" and not hoi_quy else 1


if __name__ == "__main__":
    raise SystemExit(main())
