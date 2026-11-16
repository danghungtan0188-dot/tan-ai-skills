"""Tính đường đi thật từ nhà tới từng tiện ích (OSRM), lưu từng nơi — chạy lại bỏ qua nơi đã có.

    python duong_di.py tien_ich.json --ra duong_di.json

Máy chủ mặc định là bản thử công khai của OSRM: dùng ít, nghỉ 1 giây mỗi lượt; làm hàng loạt/bán dịch vụ thì tự dựng OSRM.
Số phút tính theo ô tô, chỉ là ước tính — trên video ghi "khoảng". In sẵn lệnh tai_ve_tinh.py phủ đủ mọi tuyến.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import time
import urllib.request

URL = "https://router.project-osrm.org/route/v1/driving"


def ghep_tuyen(nha, dich, hinh):
    """OSRM bắt đầu/kết thúc ở điểm gần nhất trên đường; nối thêm đoạn từ nhà và tới nơi để nét vẽ chạm đúng hai ghim."""
    return [list(nha)] + [list(p) for p in hinh] + [list(dich)]


def hoi_duong(nha, dich):
    u = f"{URL}/{nha[0]},{nha[1]};{dich[0]},{dich[1]}?overview=full&geometries=geojson"
    r = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "tan-ai-skills/ban-do-video"}), timeout=60))
    if r.get("code") != "Ok" or not r.get("routes"):
        raise ValueError(f'OSRM trả {r.get("code")}')
    return r["routes"][0]


def khung(du, le=0.01):
    xs, ys = [du["nha"]["lon"]], [du["nha"]["lat"]]
    for t in du["tuyen"]:
        xs += [p[0] for p in t["duong"]]; ys += [p[1] for p in t["duong"]]
    d_lat = du["ban_kinh_km"] / 110.57 * (16 / 9) / 0.92  # cảnh toàn: vòng bán kính rộng 92 % khung dọc, ảnh phải cao đủ phủ kín 9:16
    d_lon = du["ban_kinh_km"] / (111.32 * math.cos(math.radians(du["nha"]["lat"])))
    return (min(*xs, du["nha"]["lon"] - d_lon) - le, min(*ys, du["nha"]["lat"] - d_lat) - le,
            max(*xs, du["nha"]["lon"] + d_lon) + le, max(*ys, du["nha"]["lat"] + d_lat) + le)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("tien_ich"); ap.add_argument("--ra", default="duong_di.json")
    a = ap.parse_args()
    du = json.load(open(a.tien_ich, encoding="utf-8"))
    cu = {t["ten"]: t for t in json.load(open(a.ra, encoding="utf-8"))["tuyen"]} if os.path.exists(a.ra) else {}
    nha = (du["nha"]["lon"], du["nha"]["lat"])
    du["tuyen"] = []
    for t in du["tien_ich"]:
        if t["ten"] in cu:
            du["tuyen"].append(cu[t["ten"]]); continue
        dich = (t["lon"], t["lat"])
        try:
            r = hoi_duong(nha, dich)
        except (OSError, ValueError) as e:  # một nơi lỗi không làm mất các nơi đã có; chạy lại sẽ thử tiếp
            print("BỎ QUA", t["ten"], "—", e); continue
        du["tuyen"].append({**t, "km": round(r["distance"] / 1000, 2), "phut": max(1, round(r["duration"] / 60)),
                            "duong": ghep_tuyen(nha, dich, r["geometry"]["coordinates"])})
        json.dump(du, open(a.ra, "w", encoding="utf-8"), ensure_ascii=False)
        print(t["ten"], du["tuyen"][-1]["km"], "km", du["tuyen"][-1]["phut"], "phút")
        time.sleep(1)
    json.dump(du, open(a.ra, "w", encoding="utf-8"), ensure_ascii=False)
    if not du["tuyen"]:
        raise SystemExit("không có tuyến nào — kiểm tra mạng rồi chạy lại")
    b = khung(du)
    print(f"đã ghi {a.ra}: {len(du['tuyen'])}/{len(du['tien_ich'])} nơi")
    z = 16 if du["ban_kinh_km"] <= 3 else 15  # bán kính lớn mà z16 thì ảnh quá nặng cho máy khi render
    print(f"ảnh nền: python tai_ve_tinh.py {z} {b[0]:.4f} {b[1]:.4f} {b[2]:.4f} {b[3]:.4f} nen.jpg")
