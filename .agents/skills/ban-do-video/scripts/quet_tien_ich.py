"""Quét tiện ích và đường lớn quanh một căn nhà qua Overpass (bước đầu của video vị trí nhà, mẫu `ViTriNha`).

    python quet_tien_ich.py "10.3600,106.3600" --ban-kinh 5 --toi-da 5 --ra tien_ich.json
    python quet_tien_ich.py "https://www.google.com/maps/place/...!3d10.36!4d106.36" --ra tien_ich.json

Chỉ giữ chỗ có tên trên OSM; lấy lần lượt mỗi loại một nơi gần nhất để video không toàn trường học.
Khoảng cách ở đây là đường chim bay, chỉ để chọn — số km đọc trong video phải lấy từ duong_di.py.
"""
from __future__ import annotations

import argparse
import json
import re
import time

from hinh_hoc import km
from lay_osm import hoi

LOAI = {  # thứ tự = thứ tự ưu tiên khi chọn
    ("amenity", "school"): "trường",
    ("amenity", "marketplace"): "chợ",
    ("amenity", "hospital"): "bệnh viện",
    ("shop", "supermarket"): "siêu thị",
    ("shop", "mall"): "siêu thị",
    ("amenity", "university"): "đại học",
    ("amenity", "college"): "đại học",
}
THU_TU = ["trường", "chợ", "bệnh viện", "siêu thị", "đại học"]
# Người vẽ OSM hay gõ loại địa điểm vào ô tên, đọc lên video nghe vô nghĩa
TEN_CHUNG = {"street market", "market", "school", "hospital", "supermarket", "chợ", "trường học", "bệnh viện", "siêu thị"}
# Way mang tên nút giao/cầu không phải tên một trục đường
KHONG_PHAI_DUONG = ("ngã ba", "ngã tư", "ngã năm", "ngã sáu", "vòng xoay", "bùng binh", "cầu ")


def ten_duong(tags):
    """Tên hiển thị của đường; "Đường Ấp Bắc" và "Ấp Bắc" là một. Bỏ qua way mang tên nút giao/cầu."""
    ten = (tags.get("ref", "").split(";")[0] or tags.get("name", "")).strip()
    if ten.lower().startswith(KHONG_PHAI_DUONG):
        return ""
    return ten[6:].strip() if ten.lower().startswith("đường ") else ten


def hoi_lai(q, lan=4):
    """Overpass công khai hay trả 502/504 khi quá tải: chờ tăng dần rồi thử lại."""
    for i in range(lan):
        try:
            return hoi(q)
        except OSError as e:
            if i == lan - 1:
                raise
            print(f"Overpass lỗi ({e}), thử lại sau {15 * (i + 1)} giây")
            time.sleep(15 * (i + 1))


def doc_toa_do(chu):
    """Nhận "lat,lon" hoặc link Google Maps; trả (lon, lat). Link có !3d!4d là toạ độ địa điểm, chính xác hơn @ (tâm khung nhìn)."""
    m = re.search(r"!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)", chu) or re.search(r"(-?\d{1,2}\.\d+)\s*,\s*(-?\d{1,3}\.\d+)", chu)
    if not m:
        raise ValueError(f"không đọc được toạ độ từ: {chu!r}")
    lat, lon = float(m.group(1)), float(m.group(2))
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        raise ValueError(f"toạ độ ngoài phạm vi: {lat}, {lon}")
    return lon, lat


def loai_cua(tags):
    return next((v for (k, g), v in LOAI.items() if tags.get(k) == g), None)


def chon_tien_ich(elements, nha, toi_da=5):
    """Lần lượt mỗi loại một nơi gần nhất tới khi đủ `toi_da`; bỏ chỗ không tên và tên trùng."""
    theo_loai = {l: [] for l in THU_TU}
    da_thay = set()
    for e in sorted(elements, key=lambda e: km(nha, _xy(e)) if _xy(e) else 1e9):
        tg, xy = e.get("tags", {}), _xy(e)
        ten, loai = tg.get("name", "").strip(), loai_cua(tg)
        if not (ten and loai and xy) or ten.lower() in da_thay or ten.lower() in TEN_CHUNG:
            continue
        da_thay.add(ten.lower())
        theo_loai[loai].append({"ten": ten, "loai": loai, "lon": xy[0], "lat": xy[1], "chim_bay_km": round(km(nha, xy), 2)})
    ra = []
    while len(ra) < toi_da and any(theo_loai.values()):
        for l in THU_TU:
            if theo_loai[l] and len(ra) < toi_da:
                ra.append(theo_loai[l].pop(0))
    return ra


def _xy(e):
    if "lon" in e:
        return e["lon"], e["lat"]
    c = e.get("center")
    return (c["lon"], c["lat"]) if c else None


def chon_duong_lon(ways, nha, toi_da=4):
    """Gom các đoạn cùng số hiệu/tên thành một đường, lấy các đường gần nhà nhất."""
    gom = {}
    for w in ways:
        ten = ten_duong(w.get("tags", {}))
        if not ten or not w.get("geometry"):
            continue
        net = [(p["lon"], p["lat"]) for p in w["geometry"]]
        d = gom.setdefault(ten, {"ten": ten, "net": [], "gan_km": 1e9})
        d["net"].append(net)
        d["gan_km"] = round(min(d["gan_km"], *(km(nha, p) for p in net)), 2)
    return sorted(gom.values(), key=lambda d: d["gan_km"])[:toi_da]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("toa_do"); ap.add_argument("--ban-kinh", type=float, default=5, help="km")
    ap.add_argument("--toi-da", type=int, default=5); ap.add_argument("--ra", default="tien_ich.json")
    a = ap.parse_args()
    nha = doc_toa_do(a.toa_do)
    vong = f"(around:{int(a.ban_kinh * 1000)},{nha[1]},{nha[0]})"
    j = hoi_lai(f'''[out:json][timeout:120];
(nwr["amenity"~"^(school|marketplace|hospital|university|college)$"]{vong};
 nwr["shop"~"^(supermarket|mall)$"]{vong};);out center tags;''')
    d = hoi_lai(f'[out:json][timeout:120];way["highway"~"^(motorway|trunk|primary|secondary)$"]{vong};out geom tags;')
    ti, dl = chon_tien_ich(j["elements"], nha, a.toi_da), chon_duong_lon(d["elements"], nha)
    json.dump({"nha": {"lon": nha[0], "lat": nha[1]}, "ban_kinh_km": a.ban_kinh, "tien_ich": ti, "duong_lon": dl},
              open(a.ra, "w", encoding="utf-8"), ensure_ascii=False)
    for t in ti:
        print(f'{t["loai"]:10} {t["ten"]}  (chim bay {t["chim_bay_km"]} km)')
    print("đường lớn:", [(x["ten"], x["gan_km"]) for x in dl])
    print("đã ghi", a.ra, "— mở bản đồ đối chiếu tên trước khi đọc lên video")
