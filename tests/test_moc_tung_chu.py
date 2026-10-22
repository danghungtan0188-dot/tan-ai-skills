"""moc_tung_chu.canh_chu: phụ đề từng chữ phải lấy mốc thật, chữ whisper nghe sai thì nội suy (không chia đều cả câu)."""

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "skills" / "bien-tap-video-thong-minh-song-ngu-tan" / "scripts"))

from moc_tung_chu import canh_chu  # noqa: E402


class TestCanhChu(unittest.TestCase):
    def test_khop_het_lay_dung_moc_whisper(self):
        chu = "Cầu Bình Phan bắc qua kênh".split()
        nghe = [("Cầu", 1.0), ("Bình", 1.3), ("Phan", 1.5), ("bắc", 2.4), ("qua", 2.6), ("kênh", 2.8)]
        self.assertEqual(canh_chu(chu, nghe, 1.0, 3.2), [1.0, 1.3, 1.5, 2.4, 2.6, 2.8])

    def test_chu_nghe_sai_thi_noi_suy_giua_hai_chu_khop(self):
        # whisper nghe "Thạnh" thành "thanh" -> không khớp, phải nằm giữa "An" và "Thủy"
        chu = "xã An Thạnh Thủy".split()
        nghe = [("xã", 0.0), ("an", 0.4), ("thanh", 0.7), ("thủy", 1.0)]
        r = canh_chu(chu, nghe, 0.0, 1.4)
        self.assertEqual(r[1], 0.4)
        self.assertEqual(r[3], 1.0)
        self.assertAlmostEqual(r[2], 0.7, places=3)

    def test_nghe_khong_ra_gi_van_tang_dan_trong_bien(self):
        r = canh_chu("một hai ba bốn".split(), [], 2.0, 4.0)
        self.assertEqual(r, sorted(r))
        self.assertTrue(all(2.0 <= t <= 4.0 for t in r))

    def test_moc_lui_bi_kep_don_dieu(self):
        r = canh_chu("a b c".split(), [("a", 1.0), ("b", 0.8), ("c", 1.5)], 1.0, 2.0)
        self.assertEqual(r, sorted(r))


if __name__ == "__main__":
    unittest.main()
