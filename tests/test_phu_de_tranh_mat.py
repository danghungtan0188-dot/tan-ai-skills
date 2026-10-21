"""Phu de tranh mat (phu_de_tranh_mat.py): cue de len mat thi doi duoi cam / tren dau.

Hop mat duoc dua thang vao (khong can video that) de kiem phan chon cho. Mot test dung
YuNet that tren khung trong de chac model nap duoc va khong bao mat gia.
"""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "skills" / "bien-tap-video-thong-minh-song-ngu-tan" / "scripts"))

import make_bilingual_ass  # noqa: E402
import phu_de_tranh_mat as tm  # noqa: E402

SEG = [{"start": 0.0, "end": 2.0, "en": "Every day one small step", "vi": "Mỗi ngày một bước nhỏ"}]


def mat(x0, y0, x1, y1):
    """Hop mat chuan hoa giu nguyen suot cue (moi 0,2 s)."""
    return [(t / 5, [(x0, y0, x1, y1)]) for t in range(11)]


class TestTranhMat(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)

    def chay(self, faces, aspect="16:9", ass_text=None):
        src = self.tmp / "cap.ass"
        src.write_text(ass_text or make_bilingual_ass.build_ass(SEG, aspect), encoding="utf-8")
        out = self.tmp / "ra.ass"
        bc = tm.tranh_mat("khong-can.mp4", src, out, faces)
        return bc, out.read_text(encoding="utf-8")

    def test_khong_de_mat_thi_giu_nguyen(self):
        bc, text = self.chay(mat(0.40, 0.10, 0.60, 0.55))
        self.assertEqual(bc[0]["quyet_dinh"], "giu")
        self.assertEqual(text, make_bilingual_ass.build_ass(SEG, "16:9"))

    def test_mat_thap_thi_dua_len_tren_dau(self):
        bc, _ = self.chay(mat(0.40, 0.45, 0.60, 0.95))
        self.assertEqual(bc[0]["quyet_dinh"], "tren_dau")
        self.assertLess(bc[0]["doi_px"], 0)

    def test_cam_cham_dong_chu_thi_ha_xuong_duoi_cam(self):
        bc, text = self.chay(mat(0.40, 0.20, 0.60, 0.80))
        self.assertEqual(bc[0]["quyet_dinh"], "duoi_cam")
        self.assertGreater(bc[0]["doi_px"], 0)
        # EN va VI doi cung nhau: van cach nhau 58 px nhu ban goc
        mv = [int(ln.split(",")[7]) for ln in text.splitlines() if ln.startswith("Dialogue:")]
        self.assertEqual(mv[0] - mv[1], 58)

    def test_mat_kin_khung_thi_bao_van_che_va_giu_co_chu(self):
        bc, text = self.chay(mat(0.05, 0.10, 0.95, 0.97), aspect="9:16")
        self.assertEqual(bc[0]["quyet_dinh"], "van_che")
        self.assertEqual(bc[0]["co_chu"], 1.0)
        self.assertNotIn("\\fscx", text)

    def test_mat_lech_sang_ben_khong_tinh_la_de(self):
        bc, _ = self.chay(mat(0.0, 0.45, 0.06, 0.95))  # mat sat mep trai, chu nam giua
        self.assertEqual(bc[0]["quyet_dinh"], "giu")

    def test_chu_dat_tay_va_lower_third_giu_nguyen(self):
        ass = make_bilingual_ass.build_ass(SEG, "16:9").replace(
            "VI,,0,0,0,,", "VI,,0,0,0,,{\\pos(960,900)}")
        bc, text = self.chay(mat(0.40, 0.45, 0.60, 0.95), ass_text=ass)
        self.assertIn("{\\pos(960,900)}Mỗi ngày", text)
        vi = [ln for ln in text.splitlines() if ln.startswith("Dialogue: 1")][0]
        self.assertEqual(vi.split(",")[7], "0")  # dong VI khong bi dong vao


@unittest.skipUnless(shutil.which("ffmpeg"), "can ffmpeg")
class TestYuNetThat(unittest.TestCase):
    def test_khung_trong_khong_co_mat(self):
        with tempfile.TemporaryDirectory() as d:
            v = Path(d) / "trong.mp4"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=gray:s=640x360:d=1",
                            "-pix_fmt", "yuv420p", str(v)], check=True)
            ds = tm.quet_mat(str(v))
            self.assertGreaterEqual(len(ds), 4)
            self.assertTrue(all(not hop for _, hop in ds))


if __name__ == "__main__":
    unittest.main()
