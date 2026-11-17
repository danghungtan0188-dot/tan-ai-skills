"""Hoi quy quy tac "moi canh chi xuat hien 1 lan" (17/11/2026): kiem_lap_canh.py phai bat canh lap tren video."""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills" / "bien-tap-video-thong-minh-song-ngu-tan" / "scripts"))
import kiem_lap_canh  # noqa: E402

try:
    import numpy  # noqa: F401
    CO_NUMPY = True
except ImportError:
    CO_NUMPY = False


def doan(d: Path, ten: str, nguon: str) -> Path:
    f = d / ten
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", nguon,
                    "-t", "4", "-pix_fmt", "yuv420p", "-c:v", "libx264", "-preset", "ultrafast", str(f)], check=True)
    return f


def noi(d: Path, ds: list, ra: str) -> Path:
    vao = []
    for f in ds:
        vao += ["-i", str(f)]
    loc = "".join(f"[{i}:v]" for i in range(len(ds))) + f"concat=n={len(ds)}:v=1:a=0[v]"
    f = d / ra
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *vao, "-filter_complex", loc, "-map", "[v]",
                    "-c:v", "libx264", "-preset", "ultrafast", str(f)], check=True)
    return f


@unittest.skipUnless(shutil.which("ffmpeg") and CO_NUMPY, "can ffmpeg + numpy")
class TestKiemLapCanh(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tam = tempfile.TemporaryDirectory()
        d = Path(cls.tam.name)
        cls.a = doan(d, "a.mp4", "testsrc2=s=640x360:r=25")
        cls.b = doan(d, "b.mp4", "mandelbrot=s=640x360:r=25")
        cls.c = doan(d, "c.mp4", "cellauto=s=640x360:r=25:rule=110")
        cls.d = d

    @classmethod
    def tearDownClass(cls):
        cls.tam.cleanup()

    def kiem(self, f: Path):
        return kiem_lap_canh.tim_lap(kiem_lap_canh.khung(f, 2), 2, 6, 0.95, [])

    def test_bat_canh_lap_cach_xa(self):
        f = noi(self.d, [self.a, self.b, self.c, self.a], "lap.mp4")  # a o 0 s va 12 s
        lap = self.kiem(f)
        self.assertTrue(lap, "phai bat duoc canh a xuat hien 2 lan")
        self.assertTrue(any(abs(x) < 4 and 10 <= y <= 16 for x, y, _ in lap))

    def test_moi_canh_mot_lan_thi_pass(self):
        f = noi(self.d, [self.a, self.b, self.c], "khong-lap.mp4")
        self.assertEqual(self.kiem(f), [])


if __name__ == "__main__":
    unittest.main()
