"""Chot chan: chu dam trong mau do hoa phai dung font du dau tieng Viet.

Bai hoc 16/11/2026: Arial dam 800/900 -> Arial Black thieu 92 chu co dau
("XA AN THANH THUY": chu A. va U? bi lay tu font khac). Xem scripts/kiem_font_viet.py.
"""
import sys
import tempfile
import unittest
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "scripts"))
import kiem_font_viet as k  # noqa: E402

CO_FONT = (k.THU_MUC_FONT / "ariblk.ttf").exists() and (k.THU_MUC_FONT / "arialbd.ttf").exists()


class TestChonDoDam(unittest.TestCase):
    def test_theo_luat_css(self):
        arial = [400, 700, 900]
        self.assertEqual(k.chon_do_dam(arial, 800), 900)  # day la duong vao Arial Black
        self.assertEqual(k.chon_do_dam(arial, 600), 700)
        self.assertEqual(k.chon_do_dam(arial, 500), 400)
        self.assertEqual(k.chon_do_dam(arial, 300), 400)


@unittest.skipUnless(CO_FONT, "can font Windows (Arial, Arial Black)")
class TestKiemFont(unittest.TestCase):
    def _quet(self, noi_dung: str):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "Mau.tsx"
            p.write_text(noi_dung, encoding="utf-8")
            return k.quet_file(p, {})

    def test_arial_black_thieu_dau(self):
        self.assertIn("Ạ", k.chu_thieu("ariblk.ttf"))
        self.assertEqual(k.chu_thieu("arialbd.ttf"), "")

    def test_bat_arial_900(self):
        loi = self._quet('const FONT = "Arial, sans-serif";\n<div style={{ fontFamily: FONT, fontWeight: 900 }} />')
        self.assertEqual(len(loi), 1)
        self.assertEqual(loi[0]["font"], "ariblk.ttf")

    def test_arial_700_dat(self):
        self.assertEqual(self._quet('<div style={{ fontFamily: "Arial", fontWeight: 700 }} />'), [])

    def test_segoe_ui_900_dat(self):
        self.assertEqual(self._quet("const F = \"'Segoe UI', 'Arial', sans-serif\";\n<b style={{ fontFamily: F, fontWeight: 900 }} />"), [])

    def test_ke_thua_tu_phan_tu_cha(self):
        loi = self._quet('<div style={{ fontFamily: "Arial" }}>\n  <span style={{ fontWeight: 800 }}>Ạ</span>\n</div>')
        self.assertEqual(len(loi), 1)

    def test_font_tu_tham_so_mac_dinh(self):
        loi = self._quet('font: z.string().default("Arial, sans-serif"),\n<p style={{ fontFamily: font, fontWeight: 900 }} />')
        self.assertEqual(len(loi), 1)

    def test_font_tu_nap_bo_qua(self):
        noi_dung = ('const FONT = "MontVN, Arial, sans-serif";\nnew FontFace("MontVN", "url(x.woff2)");\n'
                    '<h1 style={{ fontFamily: FONT, fontWeight: 900 }} />')
        self.assertEqual(self._quet(noi_dung), [])

    def test_mau_trong_repo_du_dau(self):
        loi = k.quet(k.MAC_DINH)
        self.assertEqual(loi, [], "Chu dam thieu dau tieng Viet:\n" + "\n".join(
            f"{x['file']}:{x['dong']} {x['ho']} {x['dam']}" for x in loi))


if __name__ == "__main__":
    unittest.main()
