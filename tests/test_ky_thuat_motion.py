"""skills/motion-graphics-tan/assets/ky-thuat: 12 the hoc tu 86 video marketing + 3 the hoc tu prompt Opus 5.5.

Cung hop dong voi the phong cach (tests/test_motion_graphics.py), nhung thoi luong 3-8 s theo tung ky thuat (giai-thich-5-canh dai 8 s vi co 5 canh).
Khong render -- render that bang `python scripts/render_mau.py <ten>`.
"""

import json
import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL = REPO_ROOT / "skills" / "motion-graphics-tan"
sys.path.insert(0, str(SKILL / "scripts"))

import render_mau  # noqa: E402

KY_THUAT = sorted(p for p in (SKILL / "assets" / "ky-thuat").iterdir() if p.is_dir())
FONT = SKILL / "assets" / "fonts"
TEN = {"phu-de-to-tu", "tieu-de-mo-dau", "so-muc-to", "khung-dien-thoai", "o-hoi-lat", "chia-doi",
       "the-kien-thuc", "moc-gio", "khoanh-tay", "chu-ma-nen", "con-tro-gia", "so-dem-chay",
       "giai-thich-5-canh", "cong-thuc-tung-buoc", "hinh-bien-giao-dien", "o-binh-luan"}


class TestThuVienKyThuat(unittest.TestCase):
    def test_du_15_ky_thuat_va_co_trong_huong_dan(self):
        self.assertEqual({p.name for p in KY_THUAT}, TEN)
        huong_dan = (SKILL / "references" / "ky-thuat.md").read_text(encoding="utf-8")
        for ten in TEN:
            self.assertIn(f"`{ten}`", huong_dan)
        self.assertIn("references/ky-thuat.md", (SKILL / "SKILL.md").read_text(encoding="utf-8"))

    def test_render_mau_tim_duoc_ca_hai_nhom(self):
        self.assertEqual(render_mau.tim_the("swiss").parent.parent.name, "mau")
        self.assertEqual(render_mau.tim_the("so-dem-chay").parent.parent.name, "ky-thuat")
        with self.assertRaises(SystemExit):
            render_mau.tim_the("khong-co")


class TestTheKyThuat(unittest.TestCase):
    def test_hop_dong_hyperframes(self):
        for p in KY_THUAT:
            with self.subTest(p.name):
                html = (p / "index.html").read_text(encoding="utf-8")
                self.assertTrue(3.0 <= render_mau.thoi_luong_goc(html) <= 8.0)
                self.assertIn('window.__timelines["main"] = tl', html)
                self.assertNotRegex(html, r"repeat:\s*-1|Math\.random|Date\.now")
                self.assertEqual(html.count('class="clip"'), 1)
                self.assertNotIn("/*FONT:", html, "con dau cho font chua thay")

    def test_bien_noi_dung_khong_trung_bien_css(self):
        for p in KY_THUAT:
            with self.subTest(p.name):
                html = (p / "index.html").read_text(encoding="utf-8")
                bien = {b["id"] for b in json.loads(re.search(r"data-composition-variables='(.*?)'", html, re.S).group(1))}
                self.assertEqual(bien & set(re.findall(r"--([a-z0-9-]+)\s*:", html)), set())
                self.assertEqual(bien, set(re.findall(r'data-var-text="([^"]+)"', html)))

    def test_xuat_trong_suot_duoc(self):
        for p in KY_THUAT:
            with self.subTest(p.name):
                self.assertIn("--nen: transparent", render_mau.bo_nen((p / "index.html").read_text(encoding="utf-8")))

    def test_chi_dung_font_co_tieng_viet_cua_skill(self):
        for p in KY_THUAT:
            with self.subTest(p.name):
                html = (p / "index.html").read_text(encoding="utf-8")
                for bien in re.findall(r"--font[a-z-]*:\s*([^;]+);", html):
                    self.assertRegex(bien, r"^'(Montserrat|Inter|Playfair|Nunito|VT323|Patrick Hand|Tilt Neon) VN'", bien)
                for ho in re.findall(r"--font[a-z-]*:\s*'([^']+)'", html):
                    self.assertIn(f"font-family: '{ho}'", html)
                for tep in re.findall(r"url\('assets/fonts/([^']+)'\)", html):
                    self.assertTrue((FONT / tep).is_file(), tep)
                self.assertNotIn("background-clip", html)
                self.assertNotRegex(html, r"letterSpacing\s*:")

    def test_loi_that_khi_lam(self):
        """Loi that 06/11: chu ma to dac bi bao tuong phan 1,37:1; net SVG dau tron lo cham truoc khi ve."""
        ma = (SKILL / "assets" / "ky-thuat" / "chu-ma-nen" / "index.html").read_text(encoding="utf-8")
        self.assertIn("-webkit-text-stroke", ma)
        self.assertIn("data-layout-allow-overlap", ma)
        khoanh = (SKILL / "assets" / "ky-thuat" / "khoanh-tay" / "index.html").read_text(encoding="utf-8")
        self.assertRegex(khoanh, r"strokeDasharray: dv, opacity: 0")


if __name__ == "__main__":
    unittest.main()
