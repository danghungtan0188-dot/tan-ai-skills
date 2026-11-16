"""Chot chan: do hoa do-hoa lay so hinh/giay tu mot nguon (FPS trong chung.tsx, doi bang REMOTION_FPS).

Bai hoc 16/11/2026: do hoa render 30 hinh/giay roi doi sang 25 cho ban phat song -> bo 1/6 so hinh, chuyen dong giat.
Ban phat song chay `REMOTION_FPS=25 npx remotion render ...` de dung thang o 25.
"""
import re
import unittest
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
SRC = GOC / "do-hoa" / "src"


class TestFpsDoHoa(unittest.TestCase):
    def test_fps_doc_tu_bien_moi_truong(self):
        chung = (SRC / "chung.tsx").read_text(encoding="utf-8")
        self.assertRegex(chung, r"export const FPS = Number\(process\.env\.REMOTION_FPS\) \|\| 30;")

    def test_khong_mau_nao_ghi_cung_fps(self):
        cung = []
        for p in SRC.rglob("*.tsx"):
            for i, dong in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                if re.search(r"\bfps\s*[:=]\s*\{?\s*\d", dong):
                    cung.append(f"{p.relative_to(GOC)}:{i}")
        self.assertEqual(cung, [], "Dung FPS trong chung.tsx, khong ghi so cung")

    def test_tan_studio_cung_nguon_fps(self):
        s = (GOC / "tan_studio" / "do_hoa.py").read_text(encoding="utf-8")
        self.assertIn('os.environ.get("REMOTION_FPS")', s)
        self.assertNotRegex(s, r"\*\s*30\b")


if __name__ == "__main__":
    unittest.main()
