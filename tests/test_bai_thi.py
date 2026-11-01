"""Test offline cho evaluations/bai_thi.py: cham diem, phieu tu choi, so voi moc chuan.

Khong render video -- chay that bang `python evaluations/bai_thi.py`.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "evaluations"))

import bai_thi  # noqa: E402

SPEC = json.loads((REPO_ROOT / "tan_studio" / "vi-du" / "nghiem-thu.json").read_text(encoding="utf-8"))


class TestBaiThi(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.run_dir = Path(tmp.name)

    def report(self, van_ban, khung="1080x1920"):
        (self.run_dir / "chuan-hoa.json").write_text(
            json.dumps({"normalized_text": van_ban}, ensure_ascii=False), encoding="utf-8")
        (self.run_dir / "phu-de.srt").write_text(
            "1\n00:00:00,000 --> 00:00:02,500\nxin chao\n", encoding="utf-8")
        timeline = {"khung": khung, "thoi_luong": 3.0, "nen": [{}] * len(bai_thi.MEDIA)}
        return {"run_dir": str(self.run_dir), "steps": [
            {"name": "dung_video", "status": "DONE", "timeline": timeline, "outputs": {}},
            {"name": "kiem_tra", "status": "DONE", "qa_ky_thuat": "PASS"}]}

    def dat(self, phieu):
        return {t["ma"]: t["dat"] for t in phieu["tieu_chi"]}

    def test_cham_bat_khung_sai_va_viet_tat_con_sot(self):
        dung = " ".join(SPEC["van_ban_chuan_hoa_phai_co"])
        self.assertTrue(self.dat(bai_thi.cham(self.report(dung), SPEC))["khung_dung"])
        sai = self.dat(bai_thi.cham(self.report(dung + " UBND", khung="1920x1080"), SPEC))
        self.assertFalse(sai["khung_dung"])
        self.assertFalse(sai["chuan_hoa_khong_con_viet_tat"])
        self.assertTrue(sai["phu_de_trong_thoi_luong"])

    def test_khong_co_video_thi_khong_bao_dat_thoi_luong_va_am_luong(self):
        d = self.dat(bai_thi.cham(self.report(""), SPEC))
        self.assertFalse(d["thoi_luong_khop_giong"])
        self.assertFalse(d["am_luong_dung_dich"])

    def test_phieu_tu_choi_cung_bo_tieu_chi_voi_phieu_thuong(self):
        thuong = [t["ma"] for t in bai_thi.cham(self.report(""), SPEC)["tieu_chi"]]
        tu_choi = bai_thi.phieu_tu_choi(self.run_dir, "thieu media")
        self.assertEqual([t["ma"] for t in tu_choi["tieu_chi"]], thuong)
        self.assertFalse(any(t["dat"] for t in tu_choi["tieu_chi"]))

    def test_so_moc_bao_hoi_quy_va_canh_bao_tang(self):
        moc = {"tieu_chi": [{"ma": "khung_dung", "dat": True}, {"ma": "du_media", "dat": False}],
               "so_do": {"so_canh_bao": 4}}
        nay = {"tieu_chi": [{"ma": "khung_dung", "dat": False, "do_duoc": "1920x1080"},
                            {"ma": "du_media", "dat": False, "do_duoc": "4/5"}],
               "so_do": {"so_canh_bao": 6}}
        ket_qua = bai_thi.so_moc(nay, moc)
        self.assertEqual(len(ket_qua), 2)
        self.assertIn("HOI QUY khung_dung", ket_qua[0])
        self.assertIn("4 -> 6", ket_qua[1])
        self.assertEqual(bai_thi.so_moc(nay, None), [])

    def test_moc_chuan_trong_repo_la_phieu_dat(self):
        moc = json.loads(bai_thi.MOC.read_text(encoding="utf-8"))
        self.assertTrue(all(t["dat"] for t in moc["tieu_chi"]), "moc chuan chi duoc luu tu phieu DAT")


if __name__ == "__main__":
    unittest.main()
