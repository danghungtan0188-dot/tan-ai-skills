"""Skill ban-do-video: hình học OSM và phép đo tuyến so với ranh giới xã.

Bài học kênh Chợ Gạo (10/2026): đếm "km trong xã" bằng điểm-trong-đa-giác cho 8,3 km, thật ra kênh là RANH GIỚI.
do_ranh.do() phải tách "dọc ranh giới" khỏi "trong xã".
"""

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "skills" / "ban-do-video" / "scripts"))

from do_ranh import do  # noqa: E402
from hinh_hoc import ghep_vong, km, trong  # noqa: E402

# hình vuông ~11 km cạnh quanh (106.5, 10.4)
VUONG = [(106.45, 10.35), (106.55, 10.35), (106.55, 10.45), (106.45, 10.45), (106.45, 10.35)]


def rel(*ways):
    return {"members": [{"type": "way", "role": "outer", "geometry": [{"lon": x, "lat": y} for x, y in w]} for w in ways]}


class TestHinhHoc(unittest.TestCase):
    def test_km_mot_do_kinh_o_vi_do_10(self):
        self.assertAlmostEqual(km((106.0, 10.0), (107.0, 10.0)), 109.5, delta=0.5)

    def test_trong_da_giac(self):
        self.assertTrue(trong((106.5, 10.4), VUONG))
        self.assertFalse(trong((106.6, 10.4), VUONG))

    def test_ghep_vong_tu_cac_way_dao_chieu(self):
        # ranh giới cắt thành 2 way, way thứ hai ngược chiều — phải ghép thành vòng kín
        v = ghep_vong(rel(VUONG[:3], VUONG[2:][::-1]))
        self.assertEqual(v[0], v[-1])
        self.assertEqual(len(v), 5)

    def test_thieu_members_bao_loi_ro(self):
        with self.assertRaises(ValueError):
            ghep_vong({"tags": {}})


class TestDoRanh(unittest.TestCase):
    def test_tuyen_chay_doc_ranh_khong_tinh_la_trong_xa(self):
        # kênh chạy sát cạnh trái (lệch 50 m ra ngoài) — giống kênh Chợ Gạo làm ranh giới
        kenh = [(106.4495, 10.36), (106.4495, 10.44)]
        r = do(kenh, VUONG)
        self.assertGreater(r["doc_ranh_km"], 8.0)
        self.assertEqual(r["trong_xa_km"], 0.0)

    def test_tuyen_cat_ngang_giua_xa(self):
        duong = [(106.47, 10.40), (106.53, 10.40)]
        r = do(duong, VUONG)
        self.assertGreater(r["trong_xa_km"], 5.5)
        self.assertEqual(r["doc_ranh_km"], 0.0)


if __name__ == "__main__":
    unittest.main()
