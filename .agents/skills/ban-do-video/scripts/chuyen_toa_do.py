"""Đổi dữ liệu OSM (từ lay_osm.py) sang toạ độ pixel của ảnh nền (từ tai_ve_tinh.py) cho mẫu Remotion
`BanDoVeTinh` / `BanDoNoi`. Ảnh cận (z cao hơn) đặt chồng theo cùng hệ toạ độ.

    python chuyen_toa_do.py osm.json nen15.jpg.json --song "Kênh Chợ Gạo" --duong "QL.50,ĐT.877" \
        [--can cau17.jpg.json] --ra ban_do.json

Sau khi chạy: VẼ CHỒNG ban_do.json lên ảnh nền và nhìn (xem SKILL.md) trước khi viết lời đọc có số liệu.
"""
from __future__ import annotations

import argparse
import json
import math

from hinh_hoc import ghep_vong, km_toi_duong


def px_ham(nen):
    def px(lon, lat):
        n = 2 ** nen["z"]; s = math.sin(math.radians(lat))
        x = (lon + 180) / 360 * n; y = (0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)) * n
        return [round((x - nen["tx0"]) * 256, 1), round((y - nen["ty0"]) * 256, 1)]
    return px


def gian(pts, buoc=4.0):
    ra = [pts[0]]
    for p in pts[1:]:
        if math.dist(p, ra[-1]) >= buoc:
            ra.append(p)
    return ra


def bac_truoc(d):  # vẽ từ đầu phía bắc (y nhỏ) cho thống nhất hướng "đầu bút"
    return d[::-1] if d[0][1] > d[-1][1] else d


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("osm"); ap.add_argument("nen")
    ap.add_argument("--song", default="", help="tên sông/kênh, cách nhau dấu phẩy")
    ap.add_argument("--duong", default="", help="số hiệu đường (ref), cách nhau dấu phẩy")
    ap.add_argument("--can", help="file .json của ảnh cận (z cao hơn)")
    ap.add_argument("--ra", default="ban_do.json")
    a = ap.parse_args()
    j = json.load(open(a.osm, encoding="utf-8")); nen = json.load(open(a.nen))
    E = {(e["type"], e["id"]): e for e in j["elements"]}
    px = px_ham(nen)
    ll = lambda e: [(q["lon"], q["lat"]) for q in e["geometry"]]
    xa_rel = E[("relation", j["muc_tieu"])]; xa = ghep_vong(xa_rel)
    songs = [s.strip() for s in a.song.split(",") if s.strip()]
    refs = [s.strip() for s in a.duong.split(",") if s.strip()]
    song = [e for e in j["elements"] if e["type"] == "way" and e.get("tags", {}).get("waterway") and e["tags"].get("name") in songs]
    lang = []
    for (t, i), e in E.items():
        tg = e.get("tags", {})
        if t == "relation" and tg.get("boundary") == "administrative" and i != j["muc_tieu"] and e.get("members"):
            try:
                v = ghep_vong(e)
            except ValueError:
                continue
            lang.append({"ten": tg.get("name", "").upper(), "xy": px(sum(p[0] for p in v) / len(v), sum(p[1] for p in v) / len(v)),
                         "vong": gian([px(*p) for p in v[::2]], 6)})
    cau = []
    for e in j["elements"]:
        tg = e.get("tags", {})
        if e["type"] == "way" and tg.get("bridge") == "yes" and tg.get("name", "").lower().startswith("cầu") and song:  # way cầu hay mang tên đường
            g = ll(e); c = g[len(g) // 2]
            if min(km_toi_duong(c, ll(s)) for s in song) < 0.15:
                cau.append({"ten": tg["name"].upper(), "phu": tg.get("ref", ""), "xy": px(*c)})
    du = {
        "nen": {"w": nen["w"], "h": nen["h"], "mPx": round(156543.03392 * math.cos(math.radians(xa[0][1])) / 2 ** nen["z"], 3)},
        "xa": {"ten": xa_rel["tags"].get("name", "").upper(), "vong": gian([px(*p) for p in xa], 3)},
        "song": [{"ten": e["tags"]["name"].upper(), "duong": bac_truoc(gian([px(*p) for p in ll(e)], 3))} for e in song],
        "duong": {r: [gian([px(*p) for p in ll(e)]) for e in j["elements"] if e["type"] == "way" and r in e.get("tags", {}).get("ref", "").split(";")] for r in refs},
        "cau": cau, "langGieng": lang,
    }
    if a.can:
        c = json.load(open(a.can)); f = 2 ** (c["z"] - nen["z"])
        du["can"] = {"x": c["tx0"] * 256 / f - nen["tx0"] * 256, "y": c["ty0"] * 256 / f - nen["ty0"] * 256, "w": c["w"] / f, "h": c["h"] / f}
    json.dump(du, open(a.ra, "w", encoding="utf-8"), ensure_ascii=False)
    print("đã ghi", a.ra, "| sông", len(du["song"]), "| đường", {k: len(v) for k, v in du["duong"].items()}, "| cầu", [x["ten"] for x in cau], "| lân cận", len(lang))
