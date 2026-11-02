"""skills/motion-graphics-tan: moi phong cach du the mau + cong thuc; the mau dung hop dong HyperFrames.

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

MAU = sorted(p for p in (SKILL / "assets" / "mau").iterdir() if p.is_dir())
MUC_CONG_THUC = ("Trông thế nào", "Dùng khi", "Màu", "Font", "Chữ ký chuyển động", "Thẻ mẫu", "Biến", "Câu lệnh mẫu", "Kiểm")


class TestThuVien(unittest.TestCase):
    def test_du_5_phong_cach_dot_1(self):
        self.assertEqual({p.name for p in MAU}, {"swiss", "kinetic-type", "pop-art", "glassmorphism", "editorial"})

    def test_moi_mau_co_cong_thuc_du_muc_va_duoc_skill_nhac(self):
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for p in MAU:
            with self.subTest(p.name):
                ct = (SKILL / "references" / "phong-cach" / f"{p.name}.md").read_text(encoding="utf-8")
                for muc in MUC_CONG_THUC:
                    self.assertIn(muc, ct)
                self.assertIn(f"references/phong-cach/{p.name}.md", skill)
                self.assertIn(f"assets/mau/{p.name}/index.html", ct)


class TestTheMau(unittest.TestCase):
    def test_hop_dong_hyperframes(self):
        for p in MAU:
            with self.subTest(p.name):
                html = (p / "index.html").read_text(encoding="utf-8")
                self.assertEqual(render_mau.thoi_luong_goc(html), 3.0)
                self.assertIn('window.__timelines["main"] = tl', html)
                self.assertNotRegex(html, r"repeat:\s*-1|Math\.random|Date\.now")
                self.assertEqual(html.count('class="clip"'), 1)

    def test_bien_noi_dung_khong_trung_bien_css(self):
        """Loi that o the Editorial: bien 'nhan' de len --nhan lam mat mau nhung render van chay."""
        for p in MAU:
            with self.subTest(p.name):
                html = (p / "index.html").read_text(encoding="utf-8")
                bien = {b["id"] for b in json.loads(re.search(r"data-composition-variables='(.*?)'", html, re.S).group(1))}
                css = set(re.findall(r"--([a-z0-9-]+)\s*:", html))
                self.assertEqual(bien & css, set())
                dung = set(re.findall(r'data-var-text="([^"]+)"', html))
                self.assertEqual(bien, dung, "bien khai bao phai duoc dung, va nguoc lai")

    def test_xuat_trong_suot_bo_nen_xam(self):
        for p in MAU:
            with self.subTest(p.name):
                html = render_mau.bo_nen((p / "index.html").read_text(encoding="utf-8"))
                self.assertIn("--nen: transparent", html)
                self.assertNotIn("#8a8f96", html)

    def test_font_co_tieng_viet(self):
        """Archivo Black khong co bo chu tieng Viet: dau hien bang font khac, nhin lech."""
        for p in MAU:
            with self.subTest(p.name):
                self.assertNotIn("Archivo Black", (p / "index.html").read_text(encoding="utf-8"))


class TestAnhBonKhung(unittest.TestCase):
    def test_lay_dung_4_moc(self):
        cmd = render_mau.lenh_soi(Path("a.mp4"), Path("a.png"), 30, 3.0)
        loc = cmd[cmd.index("-vf") + 1]
        for n in (9, 27, 54, 84):
            self.assertIn(f"eq(n\\,{n})", loc)


if __name__ == "__main__":
    unittest.main()
