"""Đo một tuyến (sông/kênh/đường) so với ranh giới xã: bao nhiêu km TRONG xã, bao nhiêu km CHẠY DỌC ranh giới.

Bài học kênh Chợ Gạo (10/2026): đếm "trong xã" bằng điểm-trong-đa-giác ra 8,3 km nhưng thực ra kênh LÀ ranh giới
giữa hai xã — điểm giữa các đoạn rơi ngẫu nhiên hai bên đường ranh. Luôn tách hai con số này trước khi viết lời đọc.

    python do_ranh.py osm.json --xa-id 14736644 --way 1104010765 [--sat 0.15]
"""
from __future__ import annotations

import argparse
import json

from hinh_hoc import chia_mau, ghep_vong, km_toi_duong, trong


def do(tuyen, vong, sat_km=0.15, buoc_km=0.1):
    mau = chia_mau(tuyen, buoc_km)
    doc = [p for p in mau if km_toi_duong(p, vong) < sat_km]
    trong_xa = [p for p in mau if p not in doc and trong(p, vong)]
    return {"tong_km": round(len(mau) * buoc_km, 2), "doc_ranh_km": round(len(doc) * buoc_km, 2),
            "trong_xa_km": round(len(trong_xa) * buoc_km, 2)}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("osm"); ap.add_argument("--xa-id", type=int, required=True); ap.add_argument("--way", type=int, required=True)
    ap.add_argument("--sat", type=float, default=0.15, help="km: gần ranh hơn mức này coi là chạy dọc ranh")
    a = ap.parse_args()
    E = {(e["type"], e["id"]): e for e in json.load(open(a.osm, encoding="utf-8"))["elements"]}
    vong = ghep_vong(E[("relation", a.xa_id)])
    tuyen = [(p["lon"], p["lat"]) for p in E[("way", a.way)]["geometry"]]
    print(json.dumps(do(tuyen, vong, a.sat), ensure_ascii=False))
