"""Bai hoc tu video tranh giay 20/10 (2026-10-18): may dang le bat duoc ma khong bat.

Nhac tu soan co tieng gay nhon: dinh -1,9 dBTP truoc AAC thanh +0,8 dBTP sau AAC,
video_qa --strict --audio van PASS ca 8 muc vi chi do mean_volume.
"""

import shutil
import subprocess
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))


@unittest.skipUnless(shutil.which("ffmpeg"), "can ffmpeg")
class TestVideoQaDinhTiengSauAAC(unittest.TestCase):
    def tao(self, bien_do: float) -> Path:
        out = Path(tempfile.mkdtemp()) / "thu.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=gray:s=320x180:r=25:d=2",
                        "-f", "lavfi", "-i", f"aevalsrc={bien_do}*sin(2*PI*440*t):s=48000:d=2",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart",
                        "-shortest", str(out)], check=True)
        return out

    def chay(self, f: Path) -> dict:
        import video_qa
        r = video_qa.check(Namespace(artifact=str(f), strict=True, audio=True, source=None, cut_authorized=False))
        return {c["name"]: c["status"] for c in r["checks"]}

    def test_dinh_sat_0_dB_sau_aac_la_fail(self):
        self.assertEqual(self.chay(self.tao(0.99)).get("true_peak"), "FAIL")

    def test_dinh_thap_la_pass(self):
        self.assertEqual(self.chay(self.tao(0.3)).get("true_peak"), "PASS")


if __name__ == "__main__":
    unittest.main()
