"""sua_am_tr: VieNeu (sea-g2p) phiên âm "tr" và "ch" cùng thành tʃ → sửa chuỗi phiên âm sau khi tạo."""

import sys
import types
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "skills" / "tan-giong-doc-ban-tin" / "scripts"))

import sua_am_tr  # noqa: E402


class TestSua(unittest.TestCase):
    def test_doi_tr_giu_ch(self):
        r = sua_am_tr.sua("nguồn hỗ trợ cho trẻ em", "ŋˈuə2n hˈo5 tʃˈəː6 tʃˌɔ tʃˈɛ4 ˈɛm")
        self.assertEqual(r, "ŋˈuə2n hˈo5 tɹˈəː6 tʃˌɔ tɹˈɛ4 ˈɛm")

    def test_chu_hoa_va_dau_cau(self):
        self.assertEqual(sua_am_tr.sua("Trần, chăm", "tʃˈə2n, tʃˈam"), "tɹˈə2n, tʃˈam")

    def test_lech_so_tu_giu_nguyen(self):
        ph = "tʃˈəː6"
        with mock.patch("sys.stderr"):
            self.assertEqual(sua_am_tr.sua("hỗ trợ", ph), ph)

    def test_pho_thay_giu_dau_cau(self):
        self.assertEqual(sua_am_tr.sua("Văn,", "fˈan,", {"văn": "vˈan"}), "vˈan,")


class TestVaPhienAm(unittest.TestCase):
    """Vá đúng hàm engine gọi, kể cả module đã `from ... import` trước đó."""

    def setUp(self):
        sua_am_tr._goc.clear()
        sua_am_tr._moi.clear()
        self.pt = types.ModuleType("vieneu_utils.phonemize_text")
        self.pt.phonemize_batch = lambda texts: ["tʃˈəː6" for _ in texts]
        self.pt.phonemize_with_dict = lambda text: "tʃˈəː6"
        self.pt.phonemize_text_with_emotions = lambda text: " ".join("tʃˈəː6" for _ in text.split())
        self.engine = types.ModuleType("vieneu.v3_turbo")
        self.engine.phonemize_text_with_emotions = self.pt.phonemize_text_with_emotions
        pkg = types.ModuleType("vieneu_utils")
        pkg.phonemize_text = self.pt
        self.mods = mock.patch.dict(sys.modules, {"vieneu_utils": pkg, "vieneu_utils.phonemize_text": self.pt,
                                                  "vieneu.v3_turbo": self.engine})
        self.mods.start()

    def tearDown(self):
        self.mods.stop()
        sua_am_tr._goc.clear()
        sua_am_tr._moi.clear()

    def test_va_module_engine_va_kiem_duoc(self):
        sua_am_tr.va_phien_am()
        self.assertEqual(self.engine.phonemize_text_with_emotions("trợ"), "tɹˈəː6")
        self.assertEqual(self.pt.phonemize_batch(["trợ"]), ["tɹˈəː6"])
        Tts = type("Tts", (), {"__module__": "vieneu.v3_turbo"})
        self.assertIn("tɹ", sua_am_tr.kiem_engine(Tts()))

    def test_kiem_engine_bao_loi_khi_engine_chua_va(self):
        sua_am_tr.va_phien_am()
        self.engine.phonemize_text_with_emotions = lambda text: text
        Tts = type("Tts", (), {"__module__": "vieneu.v3_turbo"})
        with self.assertRaises(AssertionError):
            sua_am_tr.kiem_engine(Tts())


if __name__ == "__main__":
    unittest.main()
