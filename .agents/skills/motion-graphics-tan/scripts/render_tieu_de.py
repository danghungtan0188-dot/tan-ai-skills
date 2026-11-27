"""Tieu de kieu "title preset" (assets/tieu-de-preset): 12 kieu chu nhieu lop, dau tieng Viet day du.

Chi render TREN MAY (khong dung cloud render tra phi). Nhe may: 1 trinh duyet, khong GPU.

    python render_tieu_de.py --ds                                   # liet ke 12 kieu
    python render_tieu_de.py vang-kim --chinh "AN THẠNH THỦY" --nhan "Bản tin" --phu "27/11"   # .mov trong suot + tieng
    python render_tieu_de.py neon --png                              # chi anh tinh .png (lam thumbnail), nhanh
    python render_tieu_de.py vang-kim --doc --giay 5                 # kho doc 9:16, dai 5 giay
    python render_tieu_de.py --bang                                  # bang xem truoc 12 kieu (anh tinh, khong render video)

Ket qua mac dinh: <--ra, mac dinh thu muc tam>/tieu-de-<kieu>.{mov,png}, bang: tieu-de-bang.png
Exit 0 = check + xuat dat; 1 = loi.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HYPERFRAMES = "hyperframes@0.8.226"
GOC = Path(__file__).resolve().parents[1] / "assets" / "tieu-de-preset"
KIEU = ["vang-kim", "neon", "bang-do", "noi-khoi", "vien-doi", "sang-trong",
        "sale-nong", "xanh-tuoi", "bang-mau", "chu-rong", "go-chu", "toc-do"]
# Noi dung mau cho bang xem truoc (noi dung cua minh, khong lay tu mau nguoi khac)
MAU_CHU = {
    "vang-kim": ("Bản tin", "AN THẠNH THỦY", "Thứ Năm, 27/11/2026"),
    "neon": ("Đêm nay", "NHẠC HỘI", "Quảng trường xã · 19h30"),
    "bang-do": ("Tin nóng", "NƯỚC LŨ DÂNG", "Cập nhật lúc 6 giờ sáng"),
    "noi-khoi": ("Bí quyết", "TRỒNG LÚA", "năng suất cao"),
    "vien-doi": ("Kỹ năng", "LÀM VIDEO", "cho người mới"),
    "sang-trong": ("Lễ kỷ niệm", "50 NĂM", "thành lập xã"),
    "sale-nong": ("Giảm sốc", "50%", "chỉ hôm nay"),
    "xanh-tuoi": ("Nông sản", "XANH SẠCH", "từ ruộng đến bàn ăn"),
    "bang-mau": ("CHUYÊN ĐỀ", "AN SINH XÃ HỘI", "Kỳ 3"),
    "chu-rong": ("Hành trình", "ĐỔI MỚI", "quê hương"),
    "go-chu": ("Mẹo hay", "CHỐNG LỪA ĐẢO", "qua điện thoại"),
    "toc-do": ("Thể thao", "BÓNG CHUYỀN", "chung kết toàn xã"),
}
CAU_HINH = {"$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
            "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"}}


def _npx(*a: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(["npx", "-y", HYPERFRAMES, *a], cwd=cwd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", shell=sys.platform == "win32")


def dung_html(giay: float, doc: bool, trong_suot: bool) -> str:
    html = (GOC / "index.html").read_text(encoding="utf-8")
    html = html.replace("/*FONTS*/", (GOC / "fonts" / "font-face.css").read_text(encoding="utf-8"), 1)
    if trong_suot:
        html = html.replace("--nen: #8a8f96", "--nen: transparent", 1)
    if doc:
        html = html.replace('data-width="1920" data-height="1080"', 'data-width="1080" data-height="1920"')
        html = html.replace("width=1920, height=1080", "width=1080, height=1920").replace(
            'data-resolution="landscape"', 'data-resolution="portrait"')
    if giay < 2.5:
        raise SystemExit("--giay toi thieu 2.5 (vao ~1,2 s + doc + ra 0,45 s)")
    return re.sub(r'data-duration="[\d.]+"', f'data-duration="{giay:g}"', html)


def gan_mac_dinh(html: str, bien: dict) -> str:
    """Ghi gia tri bien vao default cua mau: lenh `snapshot` khong nhan --variables-file nhu `render`."""
    m = re.search(r"data-composition-variables='([^']*)'", html)
    khai = json.loads(m.group(1))
    for b in khai:
        if b["id"] in bien:
            b["default"] = bien[b["id"]]
    moi = json.dumps(khai, ensure_ascii=False).replace("'", "&#39;")
    return html[: m.start(1)] + moi + html[m.end(1):]


def du_an(tam: Path, html: str, bien: dict) -> None:
    html = gan_mac_dinh(html, bien)
    (tam / "index.html").write_text(html, encoding="utf-8")
    shutil.copytree(GOC / "fonts", tam / "assets" / "fonts", ignore=shutil.ignore_patterns("*.css", "*.md"))
    (tam / "hyperframes.json").write_text(json.dumps(CAU_HINH), encoding="utf-8")
    (tam / "bien.json").write_text(json.dumps(bien, ensure_ascii=False), encoding="utf-8")


def kiem(tam: Path, ten: str) -> None:
    r = _npx("check", "--json", cwd=tam)
    try:
        ket = json.loads(r.stdout)
    except ValueError:
        raise SystemExit(f"check khong chay duoc:\n{r.stdout[-600:]}\n{r.stderr[-600:]}")
    loi = [f for v in ket.values() if isinstance(v, dict) for f in v.get("findings", []) if f.get("severity") == "error"]
    print(f"[{ten}] check: {'ok' if not loi else 'LOI'}")
    for f in loi:
        print("  LOI", f.get("code"), f.get("message"), "| Fix:", f.get("fixHint"))
    if loi:
        raise SystemExit(1)


def anh_tinh(tam: Path, giay: float, ra: Path) -> Path:
    """Chup 1 khung luc chu da vao xong (giay 1,8) bang snapshot, khong render video."""
    o = tam / "snap"
    t = min(1.8, giay - 0.6)
    r = _npx("snapshot", "--range", f"{t:g},{t + 0.04:g}", "--frames", "1", "--output", str(o), cwd=tam)
    pngs = sorted(o.rglob("*.png"))
    if r.returncode or not pngs:
        raise SystemExit(f"snapshot loi:\n{r.stdout[-800:]}\n{r.stderr[-800:]}")
    shutil.copy2(pngs[0], ra)
    return ra


def tieng(giay: float, wav: Path) -> None:
    """Tieng dong tu tong hop (scripts/sfx, MIT): vut vao, pop luc chu chinh cham, blip chu nhan, vut ra."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from sfx.mix import Mix
    from sfx.synth import blip, pop, whoosh
    mix = Mix(giay, seed=7)
    mix.put(0.03, whoosh(0.45, 300, 2600, peak=0.55), 0.22, -0.3)
    mix.put(0.45, pop(880.0, 440.0), 0.18)
    mix.put(0.65, blip(1174.66, dur=0.3, tau=0.1), 0.08, -0.4)
    mix.put(max(0.0, giay - 0.5), whoosh(0.4, 2600, 300, peak=0.35), 0.14, 0.3)
    mix.master(target_lufs=-20.0)
    mix.write(str(wav))


def xuat(kieu: str, bien: dict, giay: float, doc: bool, png: bool, ra_dir: Path, co_tieng: bool) -> Path:
    ra_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="tieu-de-", ignore_cleanup_errors=True) as t:
        tam = Path(t).resolve()
        du_an(tam, dung_html(giay, doc, trong_suot=True), {"kieu": kieu, **bien})
        kiem(tam, kieu)
        if png:
            return anh_tinh(tam, giay, (ra_dir / f"tieu-de-{kieu}.png").resolve())
        mov = (ra_dir / f"tieu-de-{kieu}{'-doc' if doc else ''}.mov").resolve()
        r = _npx("render", "--workers", "1", "--no-browser-gpu", "--format", "mov", "--quality", "delivery",
                 "--variables-file", "bien.json", "-o", str(mov), cwd=tam)
        if r.returncode or not mov.exists():
            raise SystemExit(f"render loi:\n{r.stdout[-1200:]}\n{r.stderr[-1200:]}")
    if co_tieng:
        wav = mov.with_suffix(".wav")
        tieng(giay, wav)
        tmp = mov.with_name(mov.stem + ".tam.mov")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-threads", "2", "-i", str(mov), "-i", str(wav), "-map", "0:v",
                        "-map", "1:a", "-c:v", "copy", "-c:a", "pcm_s16le", "-t", f"{giay:g}", str(tmp)], check=True)
        tmp.replace(mov)
    print(f"[{kieu}] -> {mov}")
    return mov


def bang(ra_dir: Path) -> Path:
    """12 anh tinh tren nen xam, ghep 4x3 (moi kieu 1 lan snapshot, khong render video)."""
    anh, hong = [], []
    for k in KIEU:
        n, c, p = MAU_CHU[k]
        with tempfile.TemporaryDirectory(prefix="tieu-de-", ignore_cleanup_errors=True) as t:
            tam = Path(t).resolve()
            du_an(tam, dung_html(4, False, trong_suot=False), {"kieu": k, "nhan": n, "chinh": c, "phu": p})
            try:
                kiem(tam, k)  # bao loi tung kieu nhung chay tiep, cuoi cung moi dung
            except SystemExit:
                hong.append(k)
                continue
            anh.append(anh_tinh(tam, 4, (ra_dir / f"bang-{k}.png").resolve()))
    if hong:
        raise SystemExit(f"{len(hong)} kieu khong qua check: {', '.join(hong)}")
    out = (ra_dir / "tieu-de-bang.png").resolve()
    vao = sum((["-i", str(a)] for a in anh), [])
    loc = "".join(f"[{i}]scale=640:360[s{i}];" for i in range(len(anh))) + "".join(f"[s{i}]" for i in range(len(anh))) + \
        f"xstack=inputs={len(anh)}:layout=" + "|".join(f"{(i % 4) * 640}_{(i // 4) * 360}" for i in range(len(anh)))
    subprocess.run(["ffmpeg", "-v", "error", "-y", *vao, "-filter_complex", loc, "-frames:v", "1", str(out)], check=True)
    for a in anh:
        a.unlink(missing_ok=True)
    print("bang ->", out)
    return out


def main() -> int:
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kieu", nargs="?", choices=KIEU)
    ap.add_argument("--nhan"), ap.add_argument("--chinh"), ap.add_argument("--phu")
    ap.add_argument("--giay", type=float, default=4.0)
    ap.add_argument("--doc", action="store_true", help="kho doc 1080x1920")
    ap.add_argument("--png", action="store_true", help="chi anh tinh trong suot (thumbnail)")
    ap.add_argument("--bang", action="store_true", help="bang xem truoc 12 kieu")
    ap.add_argument("--ds", action="store_true", help="liet ke kieu")
    ap.add_argument("--khong-tieng", action="store_true")
    ap.add_argument("--ra", type=Path, default=Path(tempfile.gettempdir()) / "tieu-de-preset")
    a = ap.parse_args()
    try:
        if a.ds:
            for k in KIEU:
                print(f"{k:<11} vd: {' / '.join(MAU_CHU[k])}")
        elif a.bang:
            a.ra.mkdir(parents=True, exist_ok=True)
            bang(a.ra)
        elif a.kieu:
            n, c, p = MAU_CHU[a.kieu]
            bien = {"nhan": a.nhan if a.nhan is not None else n, "chinh": a.chinh or c, "phu": a.phu if a.phu is not None else p}
            xuat(a.kieu, bien, a.giay, a.doc, a.png, a.ra, not a.khong_tieng)
        else:
            ap.error("chon kieu, hoac --bang / --ds")
    except SystemExit as e:
        if e.code not in (0, None):
            if not isinstance(e.code, int):
                print("LOI:", e.code)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
