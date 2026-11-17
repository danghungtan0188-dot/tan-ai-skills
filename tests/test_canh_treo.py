"""Chó canh lệnh treo (scripts/canh_treo.py) — bài học 13/11: ghép bản tin treo 3 giờ không ai biết."""

import contextlib
import io
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import canh_treo  # noqa: E402

PY = sys.executable
NHANH = {"nguong_giay": 0.8, "moi_giay": 0.2}


class TestCanhTreo(unittest.TestCase):
    def test_tien_trinh_ngu_bi_dung_va_bao_treo(self):
        bat_dau = time.monotonic()
        ma, treo = canh_treo.canh([PY, "-c", "import time; time.sleep(60)"], **NHANH)
        self.assertTrue(treo)
        self.assertEqual(ma, canh_treo.MA_TREO)
        self.assertLess(time.monotonic() - bat_dau, 20)

    def test_lenh_xong_binh_thuong_giu_ma_thoat(self):
        self.assertEqual(canh_treo.canh([PY, "-c", "import sys; sys.exit(7)"], **NHANH), (7, False))

    def test_cpu_dang_chay_khong_bi_coi_la_treo(self):
        lenh = [PY, "-c", "import time\nt=time.time()\nwhile time.time()-t<2: pass"]
        self.assertEqual(canh_treo.canh(lenh, **NHANH), (0, False))

    def test_file_dau_ra_dang_lon_khong_bi_coi_la_treo(self):
        with tempfile.TemporaryDirectory() as tmp:
            ra = Path(tmp) / "ra.bin"
            lenh = [PY, "-c", f"import time\nfor _ in range(20):\n open(r'{ra}','ab').write(b'x'); time.sleep(0.1)"]
            self.assertEqual(canh_treo.canh(lenh, str(ra), **NHANH), (0, False))

    def test_cli_in_chu_treo(self):
        loi = io.StringIO()
        with contextlib.redirect_stderr(loi):
            ma = canh_treo.main(["--phut", "0.01", "--moi", "0.2", "--", PY, "-c", "import time; time.sleep(60)"])
        self.assertEqual(ma, canh_treo.MA_TREO)
        self.assertIn("TREO", loi.getvalue())

    def test_cli_thieu_lenh_bao_loi(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(canh_treo.main(["--phut", "1"]), 2)


if __name__ == "__main__":
    unittest.main()
