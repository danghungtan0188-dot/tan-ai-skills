"""Hoi quy bai hoc 17/11/2026: tieng cam tu giua video den het phai bi bat (scripts/kiem_tieng_cam.py)."""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills" / "bien-tap-video-thong-minh-song-ngu-tan" / "scripts"))
import kiem_tieng_cam  # noqa: E402


@unittest.skipUnless(shutil.which("ffmpeg"), "can ffmpeg")
class TestKiemTiengCam(unittest.TestCase):
    def tao(self, d: Path, ten: str, loc: str) -> Path:
        f = d / ten
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", loc, "-t", "20", str(f)],
                       check=True)
        return f

    def test_bat_tieng_cam_tu_giua_den_het(self):
        with tempfile.TemporaryDirectory() as d:
            # 8 s co tieng roi cam den het (dung kieu loi da gap)
            f = self.tao(Path(d), "cam.wav", "sine=f=440:d=20,volume='if(lt(t,8),0.3,0)':eval=frame")
            cam = kiem_tieng_cam.doan_cam(f, doan=5)
            self.assertTrue(cam, "phai bat duoc doan cam")
            self.assertGreaterEqual(min(cam), 5.0)

    def test_tieng_du_khong_bao_cam(self):
        with tempfile.TemporaryDirectory() as d:
            f = self.tao(Path(d), "du.wav", "sine=f=440:d=20,volume=0.3")
            self.assertEqual(kiem_tieng_cam.doan_cam(f, doan=5), [])


if __name__ == "__main__":
    unittest.main()
