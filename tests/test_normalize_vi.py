"""Doi so/ngay thanh chu truoc khi dua vao VieNeu-TTS.

Moi ca o day la mot loi phat am da gap that. Gap loi moi -> them mot dong.
"""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "skills" / "tan-giong-doc-ban-tin" / "scripts"))

import normalize_vi  # noqa: E402


class TestSoThanhChu(unittest.TestCase):
    def test_so_nguyen(self):
        cases = {
            0: "không",
            5: "năm",
            10: "mười",
            15: "mười lăm",
            21: "hai mươi mốt",
            24: "hai mươi tư",
            105: "một trăm lẻ năm",
            1402: "một nghìn bốn trăm lẻ hai",
            2003: "hai nghìn không trăm lẻ ba",
            1_500_000: "một triệu năm trăm nghìn",
            2_000_000_000: "hai tỷ",
        }
        for n, expected in cases.items():
            self.assertEqual(normalize_vi.number_to_words(n), expected, n)


class TestNormalizeNumbers(unittest.TestCase):
    def check(self, src, expected):
        self.assertEqual(normalize_vi.normalize_numbers(src), expected)

    def test_ngay_gach_ngang(self):
        # Loi that: thu vien doc "22 tháng 5203"
        self.check("sinh ngày 22-5-2003", "sinh ngày hai mươi hai tháng năm năm hai nghìn không trăm lẻ ba")

    def test_ngay_gach_cheo_khong_co_chu_ngay(self):
        self.check("Hạn chót 01/10/2026.", "Hạn chót ngày một tháng mười năm hai nghìn không trăm hai mươi sáu.")

    def test_ngay_thang_ngan(self):
        self.check("ngày 26/9", "ngày hai mươi sáu tháng chín")

    def test_thang_tu(self):
        self.check("tháng 4/2026", "tháng tư năm hai nghìn không trăm hai mươi sáu")

    def test_hai_so_lien_nhau_khong_dinh(self):
        # Loi that: "1402 ngày 26" bi doc dinh thanh "1.400 lẻ 2026"
        self.check(
            "Quyết định số 1402 ngày 26",
            "Quyết định số một nghìn bốn trăm lẻ hai ngày hai mươi sáu",
        )

    def test_dau_cham_hang_nghin(self):
        self.check("1.500.000 đồng", "một triệu năm trăm nghìn đồng")

    def test_so_thap_phan(self):
        self.check("tăng 3,5 lần", "tăng ba phẩy năm lần")

    def test_phan_tram(self):
        self.check("đạt 98%", "đạt chín mươi tám phần trăm")

    def test_so_bat_dau_bang_0_doc_tung_chu_so(self):
        self.check("gọi 0909", "gọi không chín không chín")

    def test_khong_dung_vao_chu(self):
        self.check("Ủy ban nhân dân xã", "Ủy ban nhân dân xã")


class TestNormalizeText(unittest.TestCase):
    def test_viet_tat_roi_toi_so(self):
        out = normalize_vi.normalize_text("UBND Q.5 họp ngày 2/9/2026", normalize_vi.load_rules())
        self.assertEqual(out, "Ủy ban nhân dân Quận năm họp ngày hai tháng chín năm hai nghìn không trăm hai mươi sáu")


if __name__ == "__main__":
    unittest.main()
