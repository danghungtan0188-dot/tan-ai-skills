"""Test cho scripts/check_citations.py — bat duoc trich dan bia."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import check_citations  # noqa: E402


class TestCheckCitations(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "src").mkdir()
        (self.root / "src" / "app.ts").write_text(
            "import x from 'y'\n\nexport function login() {}\n", encoding="utf-8")
        self.doc = self.root / "ARCHITECTURE.md"

    def tearDown(self):
        self.tmp.cleanup()

    def run_check(self, body):
        self.doc.write_text(body, encoding="utf-8")
        return check_citations.check(self.doc, self.root)

    def test_trich_dan_dung(self):
        total, errors = self.run_check("Đăng nhập ở `src/app.ts:3`, import `src/app.ts:1-3`.")
        self.assertEqual(total, 2)
        self.assertEqual(errors, [])

    def test_file_khong_ton_tai(self):
        _, errors = self.run_check("`src/khong-co.ts:1`")
        self.assertIn("không có file", errors[0])

    def test_dong_vuot_qua_file(self):
        _, errors = self.run_check("`src/app.ts:99`")
        self.assertIn("chỉ có 3 dòng", errors[0])

    def test_dong_trong(self):
        _, errors = self.run_check("`src/app.ts:2`")
        self.assertIn("dòng trống", errors[0])

    def test_exit_code(self):
        script = REPO_ROOT / "scripts" / "check_citations.py"
        run = lambda: subprocess.run([sys.executable, str(script), str(self.doc),
                                      "--root", str(self.root)], capture_output=True)
        self.doc.write_text("`src/app.ts:3`", encoding="utf-8")
        self.assertEqual(run().returncode, 0)
        self.doc.write_text("`src/app.ts:99`", encoding="utf-8")
        self.assertEqual(run().returncode, 1)
        self.doc.write_text("không dẫn nguồn", encoding="utf-8")
        self.assertEqual(run().returncode, 2)


if __name__ == "__main__":
    unittest.main()
