# Tải ô ảnh vệ tinh Esri World Imagery (z = 15 cho nền, 17 cho cận cảnh) và ghép thành 1 ảnh; ghi khung ô ra <ra>.json.
# Lưu từng ô vào o/ — chạy lại bỏ qua ô đã có. Ghi nguồn "Ảnh vệ tinh: Esri, Maxar"; phát sóng thì kiểm điều khoản Esri.
# Dùng: python tai_ve_tinh.py <z> <lon0> <lat0> <lon1> <lat1> <ra.jpg>
import math, os, sys, json, time, urllib.request
from PIL import Image
def xy(lon, lat, z):
    n = 2 ** z; s = math.sin(math.radians(lat))
    return (lon + 180) / 360 * n, (0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)) * n
z = int(sys.argv[1]); lon0, lat0, lon1, lat1 = map(float, sys.argv[2:6]); ra = sys.argv[6]
x0, y0 = xy(lon0, lat1, z); x1, y1 = xy(lon1, lat0, z)
tx0, ty0, tx1, ty1 = int(x0), int(y0), int(x1), int(y1)
os.makedirs("o", exist_ok=True)
anh = Image.new("RGB", ((tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256))
for ty in range(ty0, ty1 + 1):
    for tx in range(tx0, tx1 + 1):
        f = f"o/{z}_{tx}_{ty}.jpg"
        if not os.path.exists(f):
            r = urllib.request.Request(f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{ty}/{tx}", headers={"User-Agent": "tan-ai-skills/1.0"})
            open(f, "wb").write(urllib.request.urlopen(r, timeout=60).read()); time.sleep(0.05)
        anh.paste(Image.open(f), ((tx - tx0) * 256, (ty - ty0) * 256))
anh.save(ra, quality=90)
json.dump({"z": z, "tx0": tx0, "ty0": ty0, "w": anh.width, "h": anh.height}, open(ra + ".json", "w"))
print(ra, anh.size, (tx1 - tx0 + 1) * (ty1 - ty0 + 1), "o")
