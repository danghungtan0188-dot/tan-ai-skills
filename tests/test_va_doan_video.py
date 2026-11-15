"""va_doan_video: cắt tại khung chìa khóa, đoạn giữa dựng lại, phần còn lại -c copy, số khung bằng bản gốc."""

import io
import shutil
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from contextlib import redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import va_doan_video as v  # noqa: E402

CO_FFMPEG = shutil.which("ffmpeg") and shutil.which("ffprobe")


class TestChonCat(unittest.TestCase):
    KHOA = [0.0, 2.0, 4.0, 6.0]

    def test_chon_khung_khoa_bao_ngoai(self):
        self.assertEqual(v.chon_cat(self.KHOA, 2.3, 3.6), (2.0, 4.0))
        self.assertEqual(v.chon_cat(self.KHOA, 2.0, 4.0), (2.0, 4.0))

    def test_toi_het_video(self):
        self.assertEqual(v.chon_cat(self.KHOA, 6.5, 7.0), (6.0, None))

    def test_den_truoc_tu_la_loi(self):
        with self.assertRaises(ValueError):
            v.chon_cat(self.KHOA, 3.0, 2.0)


def _ff(*a):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-threads", "1", *map(str, a)], check=True)


def _mau_giua(p, t):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(p), "-frames:v", "1", "-vf", "crop=64:64:288:208,scale=1:1",
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True)
    return tuple(r.stdout[:3])


@unittest.skipUnless(CO_FFMPEG, "cần ffmpeg")
class TestVaThat(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        d = Path(cls.tmp.name)
        cls.goc, cls.giua, cls.ra = d / "goc.mp4", d / "giua.mp4", d / "ra.mp4"
        # 6 s, 30 fps, khung chìa khóa mỗi 1 s, nền xanh dương; đoạn giữa nền đỏ
        _ff("-f", "lavfi", "-i", "color=c=blue:s=640x480:r=30:d=6", "-f", "lavfi", "-i", "sine=f=440:d=6",
            "-c:v", "libx264", "-preset", "faster", "-x264-params", "keyint=30:min-keyint=30:scenecut=0:threads=1",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", cls.goc)
        _ff("-f", "lavfi", "-i", "color=c=red:s=640x480:r=30:d=2", "-c:v", "libx264", "-preset", "faster",
            "-pix_fmt", "yuv420p", cls.giua)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_chi_tim(self):
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(v.main([str(self.goc), "--tu", "2.3", "--den", "3.6", "--chi-tim"]), 0)
        self.assertIn("đoạn giữa 60 khung", out.getvalue())

    def test_va_giu_so_khung_va_thay_dung_doan(self):
        with redirect_stdout(io.StringIO()):
            ma = v.main([str(self.goc), "--tu", "2.3", "--den", "3.6", "--doan-giua", str(self.giua), "--ra", str(self.ra)])
        self.assertEqual(ma, 0)
        self.assertEqual(v.dem_khung(self.ra), 180)
        r, g, b = _mau_giua(self.ra, 3.0)
        self.assertGreater(r, 150)
        self.assertLess(b, 100)
        for t in (1.0, 5.0):
            r, g, b = _mau_giua(self.ra, t)
            self.assertGreater(b, 150, f"giây {t} phải giữ nguyên bản gốc")
        a = v._probe("-select_streams", "a", "-show_entries", "stream=codec_name", self.ra)["streams"]
        self.assertEqual(len(a), 1, "phải giữ dải tiếng")

    def test_khong_ghi_de_ban_goc(self):
        with redirect_stdout(io.StringIO()), unittest.mock.patch("sys.stderr", io.StringIO()):
            ma = v.main([str(self.goc), "--tu", "2.3", "--den", "3.6", "--doan-giua", str(self.giua), "--ra", str(self.goc)])
        self.assertEqual(ma, 2)


if __name__ == "__main__":
    unittest.main()
