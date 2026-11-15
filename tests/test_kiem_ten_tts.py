"""kiem_ten_tts: cụm bắt buộc đạt khi ≥ 2/3 lần nghe ra đủ (giả lập kết quả whisper, không cần model thật)."""

import io
import json
import sys
import tempfile
import types
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import kiem_ten_tts as k  # noqa: E402


class TestCham(unittest.TestCase):
    def test_hai_tren_ba_la_dat(self):
        nghe = ["Ông Đỗ Văn Chẩn nhận nhà", "ông đỗ văn chẩn", "ông Đỗ Văn Trẩn"]
        self.assertEqual(k.cham(nghe, ["đỗ văn chẩn"]), [("đỗ văn chẩn", 2, True)])

    def test_mot_tren_ba_la_can_xem(self):
        nghe = ["Đặng Thị Ngọc Thịnh", "Đặng Thiện Ngọc Thịnh", "Đặng Thiện Ngọc Thịnh"]
        self.assertEqual(k.cham(nghe, ["Đặng Thị Ngọc Thịnh"]), [("Đặng Thị Ngọc Thịnh", 1, False)])

    def test_khong_khop_nua_chu(self):
        # "văn út" không được tính là có trong "văn útt"
        self.assertFalse(k.cham(["nguyễn văn útt"] * 3, ["nguyễn văn út"])[0][2])

    def test_chuan_dau_cau_va_uy(self):
        self.assertTrue(k.cham(["Uỷ ban, Mặt trận."] * 2 + ["x"], ["ủy ban mặt trận"])[0][2])


class TestMain(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.goc = Path(self.tmp.name)
        (self.goc / "a.wav").write_bytes(b"0")
        (self.goc / "b.wav").write_bytes(b"0")
        self.cau = self.goc / "cau.json"
        self.cau.write_text(json.dumps([{"id": "a", "file": "a.wav", "can": ["trần văn sang"]},
                                        {"id": "b", "file": "b.wav", "can": ["nguyễn công thành"]}],
                                       ensure_ascii=False), encoding="utf-8")
        self.fw = mock.patch.dict(sys.modules, {"faster_whisper": types.SimpleNamespace(WhisperModel=mock.Mock())})
        self.fw.start()

    def tearDown(self):
        self.fw.stop()
        self.tmp.cleanup()

    def _chay(self, nghe):
        with mock.patch.object(k, "_nghe_file", side_effect=nghe) as m, mock.patch.object(k, "_ha_uu_tien"), \
                redirect_stdout(io.StringIO()):
            ma = k.main([str(self.cau)])
        return ma, m.call_count

    def test_bao_can_xem_va_luu_ket_qua(self):
        ma, goi = self._chay([["trần văn sang"] * 3, ["nguyễn công thanh"] * 3])
        self.assertEqual((ma, goi), (1, 2))
        kq = json.loads((self.goc / "cau_ket_qua.json").read_text(encoding="utf-8"))
        self.assertEqual(kq["_can_xem"], {"b": ["nguyễn công thành"]})

    def test_chay_lai_khong_nghe_lai_file_cu(self):
        self._chay([["trần văn sang"] * 3, ["nguyễn công thành"] * 3])
        ma, goi = self._chay([])
        self.assertEqual((ma, goi), (0, 0))

    def test_thieu_file_wav_la_loi_dau_vao(self):
        (self.goc / "b.wav").unlink()
        with mock.patch("sys.stderr", io.StringIO()):
            ma, _ = self._chay([["trần văn sang"] * 3])
        self.assertEqual(ma, 2)


if __name__ == "__main__":
    unittest.main()
