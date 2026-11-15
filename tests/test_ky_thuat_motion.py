"""skills/motion-graphics-tan/assets/ky-thuat: 12 the hoc tu 86 video marketing + 3 the hoc tu prompt Opus 5.5
+ 20 the do hoa dai khung ngang (dai-*, hoc tu Truyen hinh Dong Thap, vung an toan EBU R95).

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
       "giai-thich-5-canh", "cong-thuc-tung-buoc", "hinh-bien-giao-dien", "o-binh-luan",
       "dai-lower-third", "dai-chu-chay", "dai-logo-goc", "dai-gio-phat-song", "dai-ident", "dai-tai-tro",
       "dai-diem-tin", "dai-chuyen-muc", "dai-dinh-vi", "dai-trich-dan", "dai-e-kip", "dai-tiep-theo",
       "dai-gia-nong-san", "dai-dem-nguoc", "dai-tin-nong", "dai-hai-khung", "dai-dien-thoai", "dai-thoi-tiet",
       "dai-nhan-nguon", "dai-truc-tiep"}


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

    def test_the_dai_khung_ngang(self):
        """The dai 1920x1080: render_mau doi anh soi sang khung ngang; the khac van khung doc."""
        for p in KY_THUAT:
            with self.subTest(p.name):
                html = (p / "index.html").read_text(encoding="utf-8")
                ngang = p.name.startswith("dai-")
                self.assertEqual(render_mau.la_khung_ngang(html), ngang)
                self.assertIn('data-width="1920" data-height="1080"' if ngang else 'data-width="1080"', html)
        cmd = render_mau.lenh_soi(Path("a.mp4"), Path("a.png"), 30, 3.0, ngang=True)
        self.assertIn("scale=480:270", cmd[cmd.index("-vf") + 1])

    def test_the_dai_trong_vung_an_toan(self):
        """EBU R95: chu/logo cach mep trai-phai >= 96 px, tren-duoi >= 54 px (khung 1920x1080).
        Loi that 15/11: logo goc cach mep phai 70 px, dinh vi 70 px, bang chu chay day 1046 px, hai khung 80 px."""
        doc = lambda ten: (SKILL / "assets" / "ky-thuat" / ten / "index.html").read_text(encoding="utf-8")
        self.assertIn("#lg { position: absolute; right: 100px; top: 60px;", doc("dai-logo-goc"))
        self.assertIn("#dv { position: absolute; left: 100px; top: 60px;", doc("dai-dinh-vi"))
        self.assertIn("#hk-1 { left: 100px; } #hk-2 { left: 970px; }", doc("dai-hai-khung"))
        cc = doc("dai-chu-chay")
        top, cao = map(int, re.search(r"#cc \{ position: absolute; left: 0; right: 0; top: (\d+)px; height: (\d+)px", cc).groups())
        self.assertLessEqual(top + cao, 1080 - 54)
        self.assertIn("padding-left: 100px", cc)

    def test_loi_that_khi_lam(self):
        """Loi that 06/11: chu ma to dac bi bao tuong phan 1,37:1; net SVG dau tron lo cham truoc khi ve."""
        ma = (SKILL / "assets" / "ky-thuat" / "chu-ma-nen" / "index.html").read_text(encoding="utf-8")
        self.assertIn("-webkit-text-stroke", ma)
        self.assertIn("data-layout-allow-overlap", ma)
        khoanh = (SKILL / "assets" / "ky-thuat" / "khoanh-tay" / "index.html").read_text(encoding="utf-8")
        self.assertRegex(khoanh, r"strokeDasharray: dv, opacity: 0")
        # Loi that 15/11: chu NEWS 104 px tran o 290 px -> text_occluded. Giu co chu 86 px trong o 340 px.
        ident = (SKILL / "assets" / "ky-thuat" / "dai-ident" / "index.html").read_text(encoding="utf-8")
        self.assertRegex(ident, r"#id-news \{ width: 340px;[^}]*font-size: 86px")


if __name__ == "__main__":
    unittest.main()
