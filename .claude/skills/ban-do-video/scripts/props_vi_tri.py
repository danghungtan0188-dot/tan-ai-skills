"""Dựng props cho mẫu Remotion `ViTriNha` từ duong_di.json + ảnh nền, kèm lời đọc nháp.

    python props_vi_tri.py duong_di.json nen.jpg.json --anh nen.jpg --ten "Nhà phố sát Quốc lộ 1A" --gia "3,2 tỷ" \
        --dong "5x20m" --dong "3 phòng ngủ" --lien-he "Anh Tân" --sdt 09xxxxxxxx --ra props.json

Giá, thông tin nhà, số điện thoại CHỈ lấy từ tham số người dùng đưa — thiếu thì bỏ thẻ, không tự điền.
Tốc độ lia theo ngưỡng trong SKILL.md: easing inOut(quad) có đỉnh gấp 2 lần tốc độ trung bình, từ đó tính ra thời gian lia.
"""
from __future__ import annotations

import argparse
import json
import math

from chuyen_toa_do import gian, px_ham

FPS, W, H = 30, 1080, 1920
LIA_TOI_DA = 12.8  # px màn hình / khung
ZOOM_TOI_DA = 1.6  # ảnh z16 phóng quá mức này sẽ vỡ
VUNG_NHAN = (40, 420, 1040, 1320)  # tránh tiêu đề trên và phụ đề dưới


def chu_km(km):
    """Dấu cách không ngắt để phụ đề không xuống dòng giữa số và đơn vị."""
    return f"{round(km * 1000 / 10) * 10} m" if km < 1 else f"{km:.1f}".replace(".", ",").removesuffix(",0") + " km"


def phu_kin(nen, cam):
    """Ảnh nền có phủ kín khung ở cảnh này không (thiếu là lộ dải đen)."""
    nx, ny = W / 2 / cam["zoom"], H / 2 / cam["zoom"]
    return cam["cx"] - nx >= 0 and cam["cy"] - ny >= 0 and cam["cx"] + nx <= nen["w"] and cam["cy"] + ny <= nen["h"]


def giay_lia(a, b, gioi=LIA_TOI_DA):
    """Thời gian máy quay đi từ cảnh a tới cảnh b sao cho đỉnh tốc độ không quá `gioi`; tối thiểu 1 giây."""
    d = math.dist((a["cx"], a["cy"]), (b["cx"], b["cy"])) * max(a["zoom"], b["zoom"])
    return round(max(1.0, 2 * d / (gioi * FPS)), 2)


def khung_vua(net, z_rong):
    """Cảnh máy quay ôm trọn một tuyến trong vùng giữa khung dọc."""
    xs, ys = [p[0] for p in net], [p[1] for p in net]
    rx, ry = max(max(xs) - min(xs), 1), max(max(ys) - min(ys), 1)
    z = min(W * 0.72 / rx, H * 0.42 / ry, ZOOM_TOI_DA)
    return {"cx": (min(xs) + max(xs)) / 2, "cy": (min(ys) + max(ys)) / 2, "zoom": round(max(z, z_rong), 3)}


def dat_nhan_duong(duong_lon, cam):
    """Đặt nhãn đường ở cảnh toàn: mỗi đường tìm điểm gần tâm nhất mà khung chữ không đụng nhãn trước; hết chỗ thì bỏ."""
    daDat, ra = [(W / 2 - 55, H / 2 - 120, W / 2 + 55, H / 2 + 10)], []  # chỗ của ghim nhà
    x0, y0, x1, y1 = VUNG_NHAN
    for d in duong_lon:
        rong, cao = len(d["ten"]) * 22 + 40, 56
        diem = sorted((p for n in d["net"] for p in n), key=lambda p: math.dist(p, (cam["cx"], cam["cy"])))
        for p in diem:
            x, y = (p[0] - cam["cx"]) * cam["zoom"] + W / 2, (p[1] - cam["cy"]) * cam["zoom"] + H / 2
            o = (x - rong / 2, y - cao / 2, x + rong / 2, y + cao / 2)
            if o[0] < x0 or o[2] > x1 or o[1] < y0 or o[3] > y1:
                continue
            if any(o[0] < k[2] and k[0] < o[2] and o[1] < k[3] and k[1] < o[3] for k in daDat):
                continue
            daDat.append(o)
            ra.append({"ten": d["ten"], "net": d["net"], "nhan": list(p)})
            break
    return ra


def len_lich(tuyen, cam0, the, ket):
    """Xếp thời gian: mở 5 giây → mỗi nơi (lia rồi vẽ tuyến) → về toàn cảnh → thẻ giá → thẻ liên hệ."""
    canh, diem, t = [{"tu": 0, "giay": 1, **cam0}], [], 5.0
    for x in tuyen:
        c = khung_vua(x["duong"], cam0["zoom"])
        g = giay_lia(canh[-1], c)
        canh.append({"tu": t, "giay": g, **c})
        den = round(t + max(g, 1.2) + 2.4, 2)
        diem.append({**x, "tu": t, "ve": round(t + max(g * 0.5, 0.5), 2), "den": den})
        t = den
    g = giay_lia(canh[-1], cam0)
    canh.append({"tu": t, "giay": g, **cam0})
    moc_the = round(t + g * 0.5, 2) if the else None
    t = moc_the + 4.0 if the else t + g
    moc_ket = round(t, 2) if ket else None
    t = t + 3.5 if ket else t + 1.0
    return canh, diem, moc_the, moc_ket, round(t, 2)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("duong_di"); ap.add_argument("nen"); ap.add_argument("--anh", default="nen.jpg")
    ap.add_argument("--ten", default=""); ap.add_argument("--gia", default=""); ap.add_argument("--dong", action="append", default=[])
    ap.add_argument("--lien-he", default=""); ap.add_argument("--sdt", default="")
    ap.add_argument("--tieu-de", default="Vị trí căn nhà"); ap.add_argument("--ra", default="props.json")
    a = ap.parse_args()
    du = json.load(open(a.duong_di, encoding="utf-8")); nen = json.load(open(a.nen))
    px = px_ham(nen)
    nha = px(du["nha"]["lon"], du["nha"]["lat"])
    mPx = 156543.03392 * math.cos(math.radians(du["nha"]["lat"])) / 2 ** nen["z"]
    r_px = du["ban_kinh_km"] * 1000 / mPx
    cam0 = {"cx": nha[0], "cy": nha[1], "zoom": round(W * 0.92 / (2 * r_px), 3)}
    if not phu_kin(nen, cam0):
        raise SystemExit("ảnh nền không phủ kín khung 9:16 ở cảnh toàn — tải lại đúng lệnh duong_di.py in ra")
    tuyen = [{"ten": t["ten"], "loai": t["loai"], "km": t["km"], "phut": t["phut"], "xy": px(t["lon"], t["lat"]),
              "duong": gian([px(*p) for p in t["duong"]], 3)} for t in du["tuyen"]]
    duong_lon = dat_nhan_duong([{"ten": d["ten"], "net": [gian([px(*p) for p in n], 6) for n in d["net"]]} for d in du["duong_lon"]], cam0)
    the = {"gia": a.gia, "ten": a.ten, "dong": a.dong} if a.gia else None
    ket = {"ten": a.lien_he, "sdt": a.sdt} if a.sdt else None
    canh, diem, moc_the, moc_ket, het = len_lich(tuyen, cam0, the, ket)
    cau = [{"chu": f'Cách {d["ten"]} {chu_km(d["km"])}, khoảng {d["phut"]} phút đi ô tô.', "batDau": d["tu"], "ketThuc": d["den"] - 0.1} for d in diem]
    props = {
        "tiLe": "9:16", "thoiLuong": het, "font": "", "nen": {"file": a.anh, "w": nen["w"], "h": nen["h"], "mPx": round(mPx, 3)},
        "nha": {"xy": nha}, "tieuDe": {"lon": a.tieu_de, "phu": f'Tiện ích trong bán kính {chu_km(du["ban_kinh_km"])}'},
        "banKinhPx": round(r_px), "duongLon": duong_lon,
        "diem": [{"ten": d["ten"], "loai": d["loai"], "doan": f'{chu_km(d["km"])} · khoảng {d["phut"]} phút', "xy": d["xy"], "duong": d["duong"],
                  "tu": d["tu"], "ve": d["ve"], "den": d["den"]} for d in diem],
        "the": {**the, "tu": moc_the} if the else None, "ket": {**ket, "tu": moc_ket} if ket else None,
        "canh": canh, "cau_doc": cau,
        "nguon": ["Ảnh vệ tinh: Esri, Maxar · Dữ liệu © OpenStreetMap · Đường đi: OSRM · Thời gian ước tính, chỉ tham khảo"],
    }
    json.dump(props, open(a.ra, "w", encoding="utf-8"), ensure_ascii=False)
    moc = {"mo": 3.6, **{f'diem_{i + 1}': round(d["den"] - 0.5, 2) for i, d in enumerate(diem)}, "the": moc_the and moc_the + 1, "ket": moc_ket and moc_ket + 1}
    print("đã ghi", a.ra, "| dài", het, "giây | nhãn đường", [d["ten"] for d in duong_lon])
    print("mốc soi khung tĩnh (giây):", {k: v for k, v in moc.items() if v is not None})
    print("lời đọc nháp:"); [print(" ", c["chu"]) for c in cau]
