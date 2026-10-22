"""Lấy dữ liệu OSM quanh một xã qua Overpass: ranh giới xã + xã lân cận, sông/kênh, đường cấp tỉnh trở lên, cầu, tên ấp.

    python lay_osm.py "An Thạnh Thủy" --ra osm.json          # in các relation khớp tên, lấy cái đầu
    python lay_osm.py "An Thạnh Thủy" --id 14736644 --le 0.03 --ra osm.json

Ghi chú: ranh giới xã sau sáp nhập 2025 trên OSM có thể chưa đúng/đủ — đối chiếu bản đồ chính thức trước khi đăng.
Nominatim có thể bị chặn DNS trên máy này; Overpass (overpass-api.de) dùng được.
"""
from __future__ import annotations

import argparse
import json
import urllib.parse
import urllib.request

URL = "https://overpass-api.de/api/interpreter"


def hoi(q):
    d = urllib.parse.urlencode({"data": q}).encode()
    r = urllib.request.Request(URL, d, headers={"User-Agent": "tan-ai-skills/ban-do-video"})
    return json.load(urllib.request.urlopen(r, timeout=240))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ten"); ap.add_argument("--id", type=int); ap.add_argument("--le", type=float, default=0.03, help="độ nới bbox")
    ap.add_argument("--ra", default="osm.json")
    a = ap.parse_args()
    ung = hoi(f'[out:json][timeout:120];rel["boundary"="administrative"]["name"~"{a.ten}"];out tags bb;')["elements"]
    for e in ung:
        print("ứng viên:", e["id"], e["tags"].get("name"), "admin_level", e["tags"].get("admin_level"), e.get("bounds"))
    xa = next((e for e in ung if e["id"] == a.id), ung[0] if ung else None)
    if not xa:
        raise SystemExit("không tìm thấy relation hành chính khớp tên")
    b = xa["bounds"]
    bb = f'{b["minlat"]-a.le},{b["minlon"]-a.le},{b["maxlat"]+a.le},{b["maxlon"]+a.le}'
    j = hoi(f'''[out:json][timeout:200];
(rel({xa["id"]});
 way["waterway"~"river|canal"]({bb});
 way["highway"~"trunk|primary|secondary|tertiary"]({bb});
 way["bridge"="yes"]["highway"]({bb});
 node["place"~"village|hamlet|town|suburb|quarter|neighbourhood"]({bb});
 rel["boundary"="administrative"]["admin_level"="{xa["tags"].get("admin_level", "6")}"]({bb});
);out geom;''')
    j["muc_tieu"] = xa["id"]; j["bbox"] = bb
    json.dump(j, open(a.ra, "w", encoding="utf-8"), ensure_ascii=False)
    print("đã ghi", a.ra, len(j["elements"]), "phần tử; xã", xa["id"], "bbox", bb)
