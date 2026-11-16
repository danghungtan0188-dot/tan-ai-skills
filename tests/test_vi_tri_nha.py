"""Video vị trí nhà (skill ban-do-video): chọn tiện ích, nối tuyến, nhịp máy quay, không tự điền giá.

Các lỗi dưới đây đều lộ ra khi chạy thử toạ độ thật ở Mỹ Tho (11/2026): "Street market" lọt vào danh sách,
"Ấp Bắc" / "Đường Ấp Bắc" thành hai đường, way mang tên "Ngã tư ..." bị coi là trục đường.
"""

import math
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "skills" / "ban-do-video" / "scripts"))

from duong_di import ghep_tuyen  # noqa: E402
from props_vi_tri import LIA_TOI_DA, chu_km, dat_nhan_duong, giay_lia, len_lich, phu_kin  # noqa: E402
from quet_tien_ich import chon_duong_lon, chon_tien_ich, doc_toa_do  # noqa: E402

NHA = (106.36, 10.36)


def noi(ten, lon, tag=("amenity", "school")):
    return {"lon": lon, "lat": 10.36, "tags": {"name": ten, tag[0]: tag[1]}}


def way(ten=None, ref=None, lon=106.361):
    tg = {k: v for k, v in (("name", ten), ("ref", ref)) if v}
    return {"tags": tg, "geometry": [{"lon": lon, "lat": 10.36}, {"lon": lon, "lat": 10.37}]}


class TestToaDo(unittest.TestCase):
    def test_lat_lon_doi_thanh_lon_lat(self):
        self.assertEqual(doc_toa_do("10.36, 106.37"), (106.37, 10.36))

    def test_link_maps_uu_tien_toa_do_dia_diem_khong_phai_tam_khung_nhin(self):
        u = "https://www.google.com/maps/place/X/@10.1,106.1,17z/data=!3m1!4b1!3d10.36!4d106.37"
        self.assertEqual(doc_toa_do(u), (106.37, 10.36))

    def test_khong_doc_duoc_thi_bao_loi(self):
        with self.assertRaises(ValueError):
            doc_toa_do("nhà anh Tân")


class TestChonTienIch(unittest.TestCase):
    def test_moi_loai_mot_noi_truoc_khi_lay_noi_thu_hai(self):
        el = [noi("Trường A", 106.361), noi("Trường B", 106.362), noi("Chợ C", 106.37, ("amenity", "marketplace"))]
        self.assertEqual([x["ten"] for x in chon_tien_ich(el, NHA, 2)], ["Trường A", "Chợ C"])

    def test_bo_noi_khong_ten_va_ten_chung_chung(self):
        el = [noi("Street market", 106.361, ("shop", "supermarket")), noi("", 106.361), noi("Trường A", 106.37)]
        self.assertEqual([x["ten"] for x in chon_tien_ich(el, NHA)], ["Trường A"])

    def test_ten_trung_chi_lay_mot(self):
        self.assertEqual(len(chon_tien_ich([noi("Trường A", 106.361), noi("trường a", 106.362)], NHA)), 1)


class TestDuongLon(unittest.TestCase):
    def test_gop_ten_co_va_khong_co_chu_duong(self):
        r = chon_duong_lon([way("Ấp Bắc"), way("Đường Ấp Bắc", lon=106.363)], NHA)
        self.assertEqual([d["ten"] for d in r], ["Ấp Bắc"])
        self.assertEqual(len(r[0]["net"]), 2)

    def test_bo_way_mang_ten_nut_giao(self):
        self.assertEqual(chon_duong_lon([way("Ngã tư Nam Kỳ–Nguyễn Trãi")], NHA), [])

    def test_uu_tien_so_hieu(self):
        self.assertEqual(chon_duong_lon([way("Đường Lý Thường Kiệt", "QL.1A")], NHA)[0]["ten"], "QL.1A")


class TestTuyen(unittest.TestCase):
    def test_net_ve_cham_ca_hai_ghim(self):
        r = ghep_tuyen((1, 1), (9, 9), [[2, 2], [8, 8]])
        self.assertEqual((r[0], r[-1]), ([1, 1], [9, 9]))


class TestHienThi(unittest.TestCase):
    def test_so_va_don_vi_khong_tach_dong(self):
        self.assertEqual(chu_km(0.13), "130 m")
        self.assertEqual(chu_km(1.32), "1,3 km")

    def test_bo_phan_le_khong(self):
        self.assertEqual(chu_km(3), "3 km")

    def test_anh_thieu_chieu_cao_thi_bi_phat_hien(self):
        # bản đầu: ảnh vuông 3840 ở zoom 0,39 lộ dải đen trên dưới
        cam = {"cx": 1920, "cy": 1920, "zoom": 0.39}
        self.assertFalse(phu_kin({"w": 3840, "h": 3840}, cam))
        self.assertTrue(phu_kin({"w": 3840, "h": 7400}, {**cam, "cy": 3700}))


class TestNhipMayQuay(unittest.TestCase):
    A = {"cx": 0, "cy": 0, "zoom": 1.0}
    B = {"cx": 3000, "cy": 0, "zoom": 1.5}

    def test_doan_dai_khong_vuot_nguong_lia(self):
        g = giay_lia(self.A, self.B)
        dinh = 2 * 3000 * 1.5 / (g * 30)  # đỉnh inOut(quad) gấp đôi tốc độ trung bình
        self.assertLessEqual(dinh, LIA_TOI_DA + 0.05)

    def test_doan_ngan_toi_thieu_mot_giay(self):
        self.assertEqual(giay_lia(self.A, {"cx": 1, "cy": 0, "zoom": 1.0}), 1.0)

    def test_moc_tang_dan_va_khong_co_gia_thi_khong_co_the(self):
        tuyen = [{"duong": [[0, 0], [100, 100]]}, {"duong": [[0, 0], [-400, 300]]}]
        canh, diem, moc_the, moc_ket, het = len_lich(tuyen, {"cx": 0, "cy": 0, "zoom": 0.3}, None, None)
        self.assertIsNone(moc_the)
        self.assertIsNone(moc_ket)
        tu = [c["tu"] for c in canh]
        self.assertEqual(tu, sorted(tu))
        self.assertGreater(het, diem[-1]["den"])


class TestNhanDuong(unittest.TestCase):
    def test_khong_de_nhau_va_nam_trong_vung_an_toan(self):
        cam = {"cx": 0, "cy": 0, "zoom": 1.0}
        net = [[[-300 + i * 10, 150] for i in range(60)]]
        r = dat_nhan_duong([{"ten": "Quốc lộ 1A", "net": net}, {"ten": "Quốc lộ 50", "net": net}], cam)
        self.assertEqual(len(r), 2)
        self.assertGreaterEqual(math.dist(r[0]["nhan"], r[1]["nhan"]), 200)

    def test_nhan_khong_nam_duoi_ghim_nha(self):
        # bản đầu: nhãn "Ấp Bắc" bị ghim che mất nửa vì chỉ xét khoảng cách từ tâm nhãn
        cam = {"cx": 0, "cy": 0, "zoom": 1.0}
        net = [[[-300 + i * 10, -50] for i in range(60)]]
        x = dat_nhan_duong([{"ten": "Ấp Bắc", "net": net}], cam)[0]["nhan"][0]
        self.assertGreater(abs(x), 55 + len("Ấp Bắc") * 11)

    def test_het_cho_thi_bo_khong_cat_mep(self):
        cam = {"cx": 0, "cy": 0, "zoom": 1.0}
        self.assertEqual(dat_nhan_duong([{"ten": "QL.1", "net": [[[5000, 5000]]]}], cam), [])


if __name__ == "__main__":
    unittest.main()
