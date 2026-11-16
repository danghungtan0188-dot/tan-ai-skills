"""Chot chan: moi mau do-hoa phai co trong danh muc (nhom + dung khi nao).

Mau moi them vao src/Root.tsx ma quen ghi danh muc -> AI va nguoi dung khong biet co mau do.
Bai hoc 16/11/2026: MoDauBanTin.tsx co file nhung chua dang ky Root.tsx nen khong ai dung duoc.
"""
import json
import re
import unittest
from pathlib import Path

DO_HOA = Path(__file__).resolve().parent.parent / "do-hoa"


def _ids_root() -> set[str]:
    return set(re.findall(r'id="(\w+)"', (DO_HOA / "src" / "Root.tsx").read_text(encoding="utf-8")))


class TestDanhMucDoHoa(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dm = json.loads((DO_HOA / "danh-muc.json").read_text(encoding="utf-8"))
        cls.ids = _ids_root()

    def test_moi_mau_deu_co_trong_danh_muc(self):
        thieu = sorted(self.ids - set(self.dm["mau"]))
        self.assertEqual(thieu, [], f"Them vao do-hoa/danh-muc.json: {thieu}")

    def test_danh_muc_khong_con_mau_da_xoa(self):
        thua = sorted(set(self.dm["mau"]) - self.ids)
        self.assertEqual(thua, [], f"Mau khong con trong Root.tsx: {thua}")

    def test_moi_muc_co_nhom_va_dung_khi(self):
        for ten, m in self.dm["mau"].items():
            with self.subTest(ten):
                self.assertIn(m.get("nhom"), self.dm["nhom"])
                self.assertGreaterEqual(len(m.get("dungKhi", "").strip()), 20, "cau 'dung khi' qua ngan")

    def test_file_mau_deu_duoc_dang_ky(self):
        chua = sorted(p.stem for p in (DO_HOA / "src" / "mau").glob("*.tsx") if p.stem not in self.ids)
        self.assertEqual(chua, [], f"File mau chua dang ky trong src/Root.tsx: {chua}")


if __name__ == "__main__":
    unittest.main()
