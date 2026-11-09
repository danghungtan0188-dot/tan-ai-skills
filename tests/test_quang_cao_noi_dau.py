"""Cong thuc video quang cao mo bang noi dau: du 5 nhip, giu luat khong bia, duoc noi tu skill video-marketing."""

import re
import unittest
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
CONG_THUC = GOC / "skills/video-marketing/references/quang-cao-noi-dau.md"


class TestQuangCaoNoiDau(unittest.TestCase):
    NOI_DUNG = CONG_THUC.read_text(encoding="utf-8")

    def test_du_5_nhip_theo_thu_tu(self):
        nhip = re.findall(r"^\| \*\*(\d)\. ", self.NOI_DUNG, re.M)
        self.assertEqual(nhip, ["1", "2", "3", "4", "5"])

    def test_giu_luat_khong_bia(self):
        self.assertIn("Con số phải thật", self.NOI_DUNG)
        self.assertIn("sản phẩm thật", self.NOI_DUNG)

    def test_duoc_noi_tu_skill(self):
        self.assertIn("quang-cao-noi-dau.md", (GOC / "skills/video-marketing/SKILL.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
