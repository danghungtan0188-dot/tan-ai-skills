"""khung6535: bố cục 65/35 — tên không lẻ dòng, chữ thu cỡ cho vừa, mốc "cid+0.4"/"cid$" đổi ra giây."""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "skills" / "bien-tap-video-thong-minh-song-ngu-tan" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import khung6535 as k  # noqa: E402


class TestChu(unittest.TestCase):
    def test_can_dong_khong_de_chu_le_dong_cuoi(self):
        f = k.font(36, "b")
        text = "Lan tỏa tinh thần tương thân tương ái"
        rong = k._do.textlength("Lan tỏa tinh thần tương thân tương", font=f) + 2   # ngắt thường: "ái" lẻ
        self.assertEqual(len(k.ngat(text, f, rong)[-1].split()), 1)
        ds = k.can_dong(text, f, rong)
        self.assertEqual(" ".join(ds), text)
        self.assertGreater(len(ds[-1].split()), 1)
        self.assertTrue(all(k._do.textlength(l, font=f) <= rong for l in ds))

    def test_vua_dong_thu_co_chu(self):
        ten = "NGUYỄN THỊ QUYẾT TÂM"
        f = k.vua_dong(ten, 58, 400, "bl")
        self.assertLess(f.size, 58)
        self.assertLessEqual(k._do.textlength(ten, font=f), 400)
        self.assertEqual(k.vua_dong("AN", 58, 400, "bl").size, 58)


class TestMoc(unittest.TestCase):
    MOC = {"d2_01": [10.0, 14.5], "d2_02": [15.0, 18.0]}

    def test_doi_moc(self):
        self.assertEqual(k.doi_moc("d2_01", self.MOC), 10.0)
        self.assertAlmostEqual(k.doi_moc("d2_01+0.4", self.MOC), 10.4)
        self.assertAlmostEqual(k.doi_moc("d2_02-0.3", self.MOC), 14.7)
        self.assertEqual(k.doi_moc("d2_01$", self.MOC), 14.5)
        self.assertAlmostEqual(k.doi_moc("d2_02$+1.0", self.MOC), 19.0)
        self.assertEqual(k.doi_moc(3.5, self.MOC), 3.5)

    def test_giai_moc_ca_kich_ban(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "moc.json").write_text(json.dumps({"moc": self.MOC, "het": 20.0}), encoding="utf-8")
            KB = {"moc_file": "moc.json", "canh": [{"bd": 0, "kt": "d2_01$", "muc": [{"t": "d2_01+0.4"}]}]}
            KB = k.giai_moc(KB, tmp)
        self.assertEqual((KB["het"], KB["canh"][0]["kt"]), (20.0, 14.5))
        self.assertAlmostEqual(KB["canh"][0]["muc"][0]["t"], 10.4)


class TestMauKichBan(unittest.TestCase):
    """Kịch bản mẫu kèm script phải đọc được và vẽ được một khung (ảnh giả tạo tạm)."""

    def test_ve_mot_khung_tu_mau(self):
        with tempfile.TemporaryDirectory() as tmp:
            for ten in ("mau_tin_65_35.json", "mau_tin_65_35_moc.json"):
                shutil.copy(SCRIPTS / ten, tmp)
            (Path(tmp) / "anh").mkdir()
            for i in range(1, 5):
                k.Image.new("RGB", (800, 450), (40 * i, 90, 120)).save(Path(tmp) / "anh" / f"anh_0{i}.jpg")
            KB = k.doc_kich_ban(Path(tmp) / "mau_tin_65_35.json")
            self.assertEqual(KB["het"], 17.0)
            im = k.khung(KB, 7.5)
        self.assertEqual(im.size, (k.W, k.H))
        # khung ảnh bên phải (cảnh 2, "P") có viền vàng tại mép trái khung
        r, g, b = im.getpixel((k.W - 60 - k.BW - 4, k.BY + 300))
        self.assertGreater(r, 150)
        self.assertGreater(r, b)


if __name__ == "__main__":
    unittest.main()
