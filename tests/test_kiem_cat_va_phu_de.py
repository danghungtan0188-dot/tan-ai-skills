"""Test kiem diem cat theo song am, kiem phu de bang OCR va cac buoc hoc tu editonny trong /dung-video."""

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import wave
from pathlib import Path
from unittest import mock

import numpy as np

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC / "scripts"))

import kiem_diem_cat as dc  # noqa: E402
import kiem_phu_de_ocr as ocr  # noqa: E402


def rms_mau():
    """1 giay lang, 1 giay tieng, 1 giay lang (o 10 ms)."""
    return np.concatenate([np.full(100, 5.0), np.full(100, 3000.0), np.full(100, 5.0)])


class TestDiemCat(unittest.TestCase):
    def test_cat_o_khoang_lang_thi_dat(self):
        self.assertEqual(dc.kiem_doan(rms_mau(), [{"start": 0.5, "end": 2.5}]), [])

    def test_cat_giua_tieng_thi_bao_loi_va_goi_y_cho_lang(self):
        loi = dc.kiem_doan(rms_mau(), [{"start": 0.5, "end": 1.85}])
        self.assertEqual(len(loi), 1)
        self.assertEqual(loi[0]["bien"], "cuoi")
        self.assertEqual(loi[0]["goi_y"], 2.0)

    def test_giua_tieng_dai_khong_co_cho_lang_gan_thi_khong_goi_y(self):
        rms = np.concatenate([np.full(100, 5.0), np.full(200, 3000.0)])
        loi = dc.kiem_doan(rms, [{"start": 0.5, "end": 2.0}])
        self.assertIsNone(loi[0]["goi_y"])

    def test_dau_va_cuoi_file_khong_tinh_la_diem_cat(self):
        rms = np.full(300, 3000.0)
        self.assertEqual(dc.kiem_doan(rms, [{"start": 0, "end": 3.0}]), [])

    def test_doc_duoc_edit_plan_va_danh_sach(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "p.json"
            f.write_text(json.dumps({"segments": [{"start": 1, "end": 2, "purpose": "x"}]}), encoding="utf-8")
            self.assertEqual(dc.doc_doan(f)[0]["end"], 2)
            f.write_text(json.dumps([{"start": 3, "end": 1}]), encoding="utf-8")
            with self.assertRaises(ValueError):
                dc.doc_doan(f)

    @unittest.skipUnless(shutil.which("ffmpeg"), "can ffmpeg")
    def test_do_rms_tu_file_am_thanh_that(self):
        tin_hieu = np.concatenate([np.zeros(16000), 8000 * np.sin(np.linspace(0, 2000, 16000))]).astype(np.int16)
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "a.wav"
            with wave.open(str(f), "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(16000)
                w.writeframes(tin_hieu.tobytes())
            rms = dc.do_rms(f)
        self.assertLess(rms[10:90].max(), 10)
        self.assertGreater(rms[110:190].min(), 1000)
        self.assertEqual(dc.kiem_doan(rms, [{"start": 1.5, "end": 1.9}])[0]["doan"], 1)


class TestPhuDeOcr(unittest.TestCase):
    SRT = "1\n00:00:01,000 --> 00:00:03,000\n<b>Xin chào</b> các bạn\n\n2\n00:00:04,000 --> 00:00:05,000\nMặt trời\n"

    def test_doc_srt_lay_giua_cau_va_bo_the(self):
        self.assertEqual(ocr.doc_srt(self.SRT), [(2.0, "Xin chào các bạn"), (4.5, "Mặt trời")])

    def test_sai_dau_tieng_viet_thi_khong_khop(self):
        self.assertEqual(ocr.ty_le_khop("Mặt trời", "Mat troi"), 0.0)
        self.assertEqual(ocr.ty_le_khop("Mặt trời", "... MẶT TRỜI ..."), 1.0)

    def test_kiem_chi_bao_cau_doc_sai(self):
        cau = ocr.doc_srt(self.SRT)
        doc = {2.0: "Xin chào các bạn", 4.5: "Mat troi"}
        loi = ocr.kiem(cau, doc.__getitem__, 0.6)
        self.assertEqual([x[1] for x in loi], ["Mặt trời"])

    def test_chon_mau_trai_deu_va_khong_vuot_toi_da(self):
        cau = [(i, str(i)) for i in range(100)]
        mau = ocr.chon_mau(cau, 12)
        self.assertEqual(len(mau), 12)
        self.assertEqual(mau[0][0], 0)
        self.assertGreater(mau[-1][0], 90)

    def test_thieu_tesseract_la_not_run_khong_phai_pass(self):
        with mock.patch.object(ocr.shutil, "which", return_value=None), \
                mock.patch.object(ocr, "DUONG_TESSERACT_WINDOWS", Path("Z:/khong-co.exe")), \
                mock.patch.object(sys, "argv", ["x", "v.mp4", "p.srt"]):
            self.assertEqual(ocr.main(), 3)

    def test_tesseract_khong_co_tieng_viet_cung_la_not_run(self):
        kq = subprocess.CompletedProcess([], 0, stdout="List of available languages:\neng\n", stderr="")
        with mock.patch.object(ocr.shutil, "which", return_value="tesseract"), \
                mock.patch.object(ocr.subprocess, "run", return_value=kq):
            with self.assertRaises(ocr.ThieuTesseract):
                ocr.tim_tesseract()


class TestDungVideo(unittest.TestCase):
    NOI_DUNG = (GOC / ".claude/commands/dung-video.md").read_text(encoding="utf-8")

    def test_co_the_cai_dat_ghi_nguon_goc_tung_muc(self):
        for chu in ("Thẻ cài đặt", "_(yêu cầu)_", "_(đề xuất)_", "_(từ tư liệu)_"):
            self.assertIn(chu, self.NOI_DUNG)

    def test_mau_ngan_truoc_khi_render_ca_video(self):
        self.assertLess(self.NOI_DUNG.index("8–15 giây"), self.NOI_DUNG.index("video_qa.py"))

    def test_mac_dinh_tat_cac_thu_them_vao(self):
        self.assertIn("Mặc định tắt", self.NOI_DUNG)
        for chu in ("nhạc", "tiếng động", "lọc màu", "chuyển cảnh"):
            self.assertIn(chu, self.NOI_DUNG.split("Mặc định tắt")[1])

    def test_goi_dung_hai_script_kiem(self):
        self.assertIn("kiem_diem_cat.py", self.NOI_DUNG)
        self.assertIn("kiem_phu_de_ocr.py", self.NOI_DUNG)


class TestCanhTheoMucDich(unittest.TestCase):
    def test_moi_the_ton_tai_va_du_20_phong_cach(self):
        goc = GOC / "skills/motion-graphics-tan"
        noi_dung = (goc / "references/canh-theo-muc-dich.md").read_text(encoding="utf-8")
        the = set(re.findall(r"^\| [^|]+ \| `([a-z0-9-]+)` \|", noi_dung, re.M))
        co_that = {p.name for p in (goc / "assets/mau").iterdir() if p.is_dir()}
        self.assertEqual(the, co_that)
        self.assertIn("canh-theo-muc-dich.md", (goc / "SKILL.md").read_text(encoding="utf-8"))

    def test_bien_khai_bao_co_trong_the_mau(self):
        goc = GOC / "skills/motion-graphics-tan"
        noi_dung = (goc / "references/canh-theo-muc-dich.md").read_text(encoding="utf-8")
        for ten, cot_bien in re.findall(r"^\| [^|]+ \| `([a-z0-9-]+)` \| (.+) \|$", noi_dung, re.M):
            html = (goc / "assets/mau" / ten / "index.html").read_text(encoding="utf-8")
            for bien in re.findall(r"`([a-z0-9-]+)`", cot_bien):
                self.assertIn(bien, html, f"{ten}: thieu bien {bien}")


if __name__ == "__main__":
    unittest.main()
