"""Hình học tối thiểu cho dữ liệu OSM (không cần shapely): ghép vòng ranh giới, điểm trong đa giác,
độ dài haversine, khoảng cách điểm tới đường gấp khúc. Toạ độ dạng (lon, lat)."""
from __future__ import annotations

import math


def km(a, b):
    """Khoảng cách haversine (km) giữa hai điểm (lon, lat)."""
    la1, lo1, la2, lo2 = map(math.radians, (a[1], a[0], b[1], b[0]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(h))


def dai(pts):
    return sum(km(pts[i], pts[i + 1]) for i in range(len(pts) - 1))


def ghep_vong(rel):
    """Ghép các way outer của relation (Overpass `out geom;`) thành vòng kín dài nhất."""
    ws = [[(p["lon"], p["lat"]) for p in m["geometry"]] for m in rel.get("members", [])
          if m["type"] == "way" and m.get("role") in ("outer", "") and m.get("geometry")]
    if not ws:
        raise ValueError("relation không có members/geometry — truy vấn phải là `out geom;`, không phải `out geom tags;`")
    vong = []
    while ws:
        r = ws.pop(0)
        while r[0] != r[-1] and ws:
            for i, w in enumerate(ws):
                if w[0] == r[-1]:
                    r += w[1:]; ws.pop(i); break
                if w[-1] == r[-1]:
                    r += w[::-1][1:]; ws.pop(i); break
            else:
                break
        vong.append(r)
    return max(vong, key=len)


def trong(p, vong):
    """Điểm (lon, lat) có nằm trong vòng không (ray casting)."""
    x, y = p
    c = False
    for i in range(len(vong) - 1):
        (x1, y1), (x2, y2) = vong[i], vong[i + 1]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def km_toi_doan(p, a, b):
    kx, ky = 111.32 * math.cos(math.radians(p[1])), 110.57
    ax, ay, bx, by, px, py = a[0] * kx, a[1] * ky, b[0] * kx, b[1] * ky, p[0] * kx, p[1] * ky
    dx, dy = bx - ax, by - ay
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / ((dx * dx + dy * dy) or 1)))
    return math.hypot(px - ax - t * dx, py - ay - t * dy)


def km_toi_duong(p, line):
    return min(km_toi_doan(p, line[i], line[i + 1]) for i in range(len(line) - 1))


def chia_mau(line, buoc_km=0.1):
    """Chia đường gấp khúc thành các điểm cách nhau ~buoc_km (để đo trong/dọc ranh giới)."""
    mau = []
    for i in range(len(line) - 1):
        n = max(1, int(km(line[i], line[i + 1]) / buoc_km))
        for j in range(n):
            t = (j + 0.5) / n
            mau.append((line[i][0] + (line[i + 1][0] - line[i][0]) * t, line[i][1] + (line[i + 1][1] - line[i][1]) * t))
    return mau
