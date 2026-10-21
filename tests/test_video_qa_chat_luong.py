"""video_qa --strict --audio: bat loi nhin/nghe thay duoc, khong chi dinh dang.

Truoc day file den 3,7 s giua video, giong qua nho -30 LUFS hay file qua nang van PASS.
Nguong do tren 6 video da giao (deu PASS); chuyen canh qua den ~0,4 s khong bi bat.
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

import video_qa  # noqa: E402

# tieng noi gia: tieng on hong dieu bien cham; do truoc: I ~ -17 LUFS, dinh ~ -3 dBFS (giong ban tin da chuan hoa)
GIONG = "anoisesrc=c=pink:r=48000:a=0.3,volume='0.5+0.5*(0.5+0.5*sin(2*PI*0.1*t))':eval=frame,volume=10dB"


@unittest.skipUnless(shutil.which("ffmpeg"), "can ffmpeg")
class TestChatLuong(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)

    def tao(self, ten, vf="", af=GIONG, crf="20", maxrate=None, dur=12):
        out = self.tmp / ten
        cmd = ["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"testsrc2=s=640x360:r=30:d={dur}",
               "-f", "lavfi", "-t", str(dur), "-i", af]
        if vf:
            cmd += ["-vf", vf]
        cmd += ["-c:v", "libx264", "-crf", crf, "-pix_fmt", "yuv420p"]
        if maxrate:
            cmd += ["-b:v", maxrate, "-maxrate", maxrate, "-bufsize", maxrate]
        cmd += ["-c:a", "aac", "-ar", "48000",
                "-movflags", "+faststart", "-shortest", str(out)]
        subprocess.run(cmd, check=True)
        return out

    def qa(self, f):
        r = video_qa.check(Namespace(artifact=str(f), strict=True, audio=True, source=None, cut_authorized=False))
        return r, {c["name"]: c["status"] for c in r["checks"]}

    def test_video_tot_pass(self):
        r, st = self.qa(self.tao("tot.mp4"))
        self.assertEqual(r["status"], "PASS", r["warnings"] + r["errors"])
        for k in ("black_frames", "bitrate", "loudness"):
            self.assertEqual(st[k], "PASS")

    def test_chuyen_canh_qua_den_ngan_khong_bi_bat(self):
        _, st = self.qa(self.tao("ngan.mp4", vf="drawbox=c=black:t=fill:enable='between(t,5.8,6.2)'"))
        self.assertEqual(st["black_frames"], "PASS")

    def test_den_dau_duoi_giua(self):
        vf = "drawbox=c=black:t=fill:enable='lt(t,1)+between(t,4,7.7)+gte(t,11.5)'"
        r, st = self.qa(self.tao("den.mp4", vf=vf))
        self.assertEqual(st["black_start"], "WARN")
        self.assertEqual(st["black_tail"], "WARN")
        self.assertEqual(st["black_middle"], "FAIL")  # 3,7 s >= 3 s
        self.assertEqual(r["status"], "FAIL")

    def test_giong_qua_nho(self):
        r, st = self.qa(self.tao("nho.mp4", af=GIONG + ",volume=-14dB"))
        self.assertEqual(st["loudness"], "WARN")

    def test_bitrate_qua_cao(self):
        _, st = self.qa(self.tao("nang.mp4", maxrate="12M", vf="noise=alls=60:allf=t"))
        self.assertEqual(st["bitrate"], "WARN")

    def test_nen_mot_mau_bitrate_thap_khong_bi_bat(self):
        # tan_studio dung nen mot mau: crf cho 0,1 Mbps ma hinh van net — khong phai loi
        _, st = self.qa(self.tao("phang_mau.mp4", vf="drawbox=c=navy:t=fill"))
        self.assertEqual(st["bitrate"], "PASS")


if __name__ == "__main__":
    unittest.main()
