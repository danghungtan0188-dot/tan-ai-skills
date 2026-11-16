"""Kiem chu dam trong mau do hoa (.tsx) co dung font du dau tieng Viet khong.

Loi da gap (16/11/2026): Arial o do dam 800/900 -> Chrome lay Arial Black, ma Arial Black
thieu 92 chu co dau (A., A?, E^'...) -> chu do bi lay tu font khac, lech net tren man hinh.

Cach kiem: voi moi `fontWeight` trong file .tsx, tim `fontFamily` cung khoi style
(khong co thi lay fontFamily dau tien trong file), chon file font Windows theo dung
luat chon do dam cua CSS, roi mo file font kiem du bo chu tieng Viet.
Font tu nap bang `new FontFace(...)` (Montserrat VN...) duoc coi la font Viet, bo qua.

  python scripts/kiem_font_viet.py                 # quet do-hoa/src, remotion-studio/src
  python scripts/kiem_font_viet.py duong/dan ...   # quet thu muc/file khac
Thoat 1 neu co cho thieu dau.
"""
from __future__ import annotations

import os
import re
import sys
from functools import lru_cache
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
MAC_DINH = [GOC / "do-hoa" / "src", GOC / "remotion-studio" / "src"]
THU_MUC_FONT = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"

_HOA = "ÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬĐÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴ"
CHU_VIET = _HOA + _HOA.lower()

# Ho font he thong -> {do dam: file}. Chi ghi cac ho repo dang/de dung.
FONT_HE_THONG = {
    "arial": {400: "arial.ttf", 700: "arialbd.ttf", 900: "ariblk.ttf"},
    "arial black": {900: "ariblk.ttf"},
    "segoe ui": {400: "segoeui.ttf", 600: "seguisb.ttf", 700: "segoeuib.ttf", 900: "seguibl.ttf"},
    "impact": {400: "impact.ttf"},
    "bahnschrift": {400: "bahnschrift.ttf"},
    "times new roman": {400: "times.ttf", 700: "timesbd.ttf"},
}
TU_KHOA_DAM = {"normal": 400, "bold": 700, "bolder": 900, "lighter": 300}


def chon_do_dam(co: list[int], muon: int) -> int:
    """Luat chon do dam cua CSS Fonts (muc 'font-weight' matching)."""
    if muon in co:
        return muon
    if 400 <= muon <= 500:
        tren = sorted(w for w in co if muon < w <= 500)
        if tren:
            return tren[0]
        duoi = sorted((w for w in co if w < muon), reverse=True)
        return duoi[0] if duoi else min(co)
    if muon > 500:
        tren = sorted(w for w in co if w > muon)
        return tren[0] if tren else max(co)
    duoi = sorted((w for w in co if w < muon), reverse=True)
    return duoi[0] if duoi else min(co)


@lru_cache(maxsize=None)
def chu_thieu(file_font: str) -> str:
    from fontTools.ttLib import TTFont

    cmap = TTFont(str(THU_MUC_FONT / file_font), fontNumber=0).getBestCmap()
    return "".join(c for c in CHU_VIET if ord(c) not in cmap)


def kiem_ho(ho: str, dam: int):
    """-> (file font, chu thieu) hoac None neu khong phai font he thong da biet."""
    bang = FONT_HE_THONG.get(ho.strip().strip("'\"").lower())
    if not bang:
        return None
    f = bang[chon_do_dam(sorted(bang), dam)]
    if not (THU_MUC_FONT / f).exists():
        return None
    return f, chu_thieu(f)


def _hang_so(text: str) -> dict[str, str]:
    hs = {m[1]: m[3] for m in re.finditer(r"(?:export\s+)?const\s+(\w+)\s*=\s*([\"'`])(.*?)\2", text)}
    # prop co gia tri mac dinh trong schema: font: z.string().default("Arial, ...")
    hs.update({m[1]: m[3] for m in re.finditer(r"(\w+)\s*:\s*z\.string\(\)\.default\(\s*([\"'`])(.*?)\2", text)})
    return hs


def _font_tu_nap(text: str) -> set[str]:
    return {m.lower() for m in re.findall(r"new\s+FontFace\(\s*[\"'`]([^\"'`]+)", text)}


def _khoi_chua(text: str, vi_tri: int) -> str:
    """Doan van ban cua khoi { ... } gan nhat bao quanh vi_tri."""
    sau, i = 0, vi_tri
    while i > 0:
        i -= 1
        if text[i] == "}":
            sau += 1
        elif text[i] == "{":
            if sau == 0:
                break
            sau -= 1
    sau, j = 0, vi_tri
    while j < len(text):
        if text[j] == "{":
            sau += 1
        elif text[j] == "}":
            if sau == 0:
                break
            sau -= 1
        j += 1
    return text[i:j]


RE_HO = re.compile(r"fontFamily\s*:\s*(?:\"([^\"]+)\"|'([^']+)'|`([^`]+)`|(\w+))")
RE_DAM = re.compile(r"fontWeight\s*:\s*[\"'`]?(\d{3}|bold|bolder|normal|lighter)\b")


def quet_file(p: Path, hang_so_chung: dict[str, str]) -> list[dict]:
    text = p.read_text(encoding="utf-8", errors="replace")
    dung_chung = re.search(r"from\s+[\"'][./]*chung[\"']", text)
    hs = {**(hang_so_chung if dung_chung else {}), **_hang_so(text)}
    tu_nap = _font_tu_nap(text)

    def giai(m) -> str | None:
        return m[1] or m[2] or m[3] or hs.get(m[4])

    cac_ho = list(RE_HO.finditer(text))
    loi = []
    for m in RE_DAM.finditer(text):
        dam = TU_KHOA_DAM.get(m[1]) or int(m[1])
        k = RE_HO.search(_khoi_chua(text, m.start()))
        if not k:  # ke thua tu phan tu cha: lay fontFamily gan nhat phia truoc
            truoc = [h for h in cac_ho if h.start() < m.start()]
            k = truoc[-1] if truoc else None
        chuoi = giai(k) if k else None
        if not chuoi:
            continue
        for ho in chuoi.split(","):
            ho_sach = ho.strip().strip("'\"").lower()
            if ho_sach in tu_nap:
                break  # font Viet tu nap
            kq = kiem_ho(ho_sach, dam)
            if kq is None:
                continue  # khong biet / generic -> xet ho tiep theo
            f, thieu = kq
            if thieu:
                dong = text.count("\n", 0, m.start()) + 1
                loi.append({"file": p, "dong": dong, "ho": ho.strip(), "dam": dam, "font": f, "thieu": thieu})
            break
    return loi


def quet(duong: list[Path]) -> list[dict]:
    hang_so_chung = {}
    for chung in GOC.glob("do-hoa/src/chung.tsx"):
        hang_so_chung.update(_hang_so(chung.read_text(encoding="utf-8")))
    files = []
    for d in duong:
        files += [d] if d.is_file() else sorted(d.rglob("*.tsx"))
    loi = []
    for f in files:
        if "node_modules" not in f.parts:
            loi += quet_file(f, hang_so_chung)
    return loi


def main(argv: list[str]) -> int:
    duong = [Path(a) for a in argv] or MAC_DINH
    loi = quet(duong)
    for x in loi:
        rel = os.path.relpath(x["file"], GOC)
        print(f"{rel}:{x['dong']}  {x['ho']} dam {x['dam']} -> {x['font']} thieu {len(x['thieu'])} chu ({x['thieu'][:12]}...)")
    if loi:
        print(f"\nTHIEU DAU: {len(loi)} cho. Sua: ha do dam (Arial <= 700) hoac doi font du dau (Segoe UI, Montserrat VN).")
        return 1
    print("Font tieng Viet: dat.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
