"""Kiem nhat ky ban tin: moi bai hoc phai co cho neo CO THAT.

Chan thoi quen ghi kinh nghiem cho co. Khai test:TenClass ma class do khong ton tai,
hay script:/doc: tro vao file khong co, thi test do.
Cach ghi: skills/bien-tap-video-thong-minh-song-ngu-tan/references/rut-kinh-nghiem.md
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL = REPO_ROOT / "skills" / "bien-tap-video-thong-minh-song-ngu-tan"
NHAT_KY = SKILL / "references" / "nhat-ky-ban-tin.md"
DANG = ("test", "script", "doc")


def dong_bang(text: str) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        if not line.startswith("|") or set(line) <= set("|- "):
            continue
        o = [c.strip() for c in line.strip("|").split("|")]
        if len(o) == 5 and o[0] != "Ngày":
            rows.append(o)
    return rows


class TestNhatKyBanTin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = dong_bang(NHAT_KY.read_text(encoding="utf-8"))
        cls.tests_src = "\n".join(p.read_text(encoding="utf-8") for p in REPO_ROOT.glob("tests/*.py"))

    def test_co_dong_de_kiem(self):
        self.assertGreater(len(self.rows), 0, "nhat ky trong")

    def test_moi_bai_hoc_co_cho_neo_dung_dang(self):
        for r in self.rows:
            neo = re.findall(r"`([a-z]+):([^`]+)`", r[4])
            self.assertTrue(neo, f"dong '{r[1]}' chua co cho neo o cot Chot bang")
            for dang, _ in neo:
                self.assertIn(dang, DANG, f"dang neo '{dang}' phai la {DANG}")

    def test_cho_neo_co_that(self):
        for r in self.rows:
            for dang, ten in re.findall(r"`([a-z]+):([^`]+)`", r[4]):
                if dang == "test":
                    self.assertRegex(self.tests_src, rf"class {re.escape(ten)}\b",
                                     f"khai {dang}:{ten} nhung khong co class do trong tests/")
                elif dang == "script":
                    self.assertTrue((SKILL / "scripts" / ten).exists(),
                                    f"khai {dang}:{ten} nhung khong co file do")
                else:
                    self.assertTrue((SKILL / "references" / ten).exists(),
                                    f"khai {dang}:{ten} nhung khong co file do")

    def test_bai_hoc_co_noi_dung(self):
        for r in self.rows:
            self.assertGreaterEqual(len(r[3]), 20, f"bai hoc cua '{r[1]}' qua so sai de dung lai")

    def test_quy_trinh_duoc_lien_ket(self):
        self.assertIn("rut-kinh-nghiem.md", (SKILL / "SKILL.md").read_text(encoding="utf-8"),
                      "SKILL.md phai tro toi quy trinh rut kinh nghiem")


if __name__ == "__main__":
    unittest.main(verbosity=2)
