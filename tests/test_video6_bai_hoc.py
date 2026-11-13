"""Bai hoc tu video6 (Anh hung LLVT, 2026-10-10): hai loi may dang le bat duoc ma khong bat.

1. Ban doc TTS co "tieng la" sau quang lang cuoi cau — nguoi xem nghe ra, QA khong do.
2. Hinh ngan hon tieng 26 s (xfade lang le bo canh) — video_qa van PASS.
"""

import shutil
import subprocess
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "skills" / "bien-tap-video-thong-minh-song-ngu-tan" / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from cat_gon_tts import cat_gon  # noqa: E402

SR = 16000


def tieng(giay: float, bien_do: float = 0.3) -> np.ndarray:
    t = np.arange(int(giay * SR)) / SR
    return (bien_do * np.sin(2 * np.pi * 220 * t)).astype(np.float32)


def lang(giay: float) -> np.ndarray:
    return np.zeros(int(giay * SR), np.float32)


class TestCatGonTTS(unittest.TestCase):
    def test_bo_tieng_la_sau_quang_lang(self):
        a = np.concatenate([lang(0.2), tieng(3.0), lang(0.8), tieng(0.2), lang(0.1)])
        x, bo = cat_gon(a, SR)
        self.assertGreater(bo, 0.5)
        self.assertLess(len(x) / SR, 3.3)

    def test_khong_dong_cau_binh_thuong(self):
        # nghi ngan giua cau (0,2 s) va tu cuoi dai — khong phai tieng la
        a = np.concatenate([lang(0.2), tieng(1.5), lang(0.2), tieng(1.0), lang(0.3)])
        x, bo = cat_gon(a, SR)
        self.assertEqual(bo, 0.0)
        self.assertGreater(len(x) / SR, 2.7)


class TestCatGonGiuAmDauNho(unittest.TestCase):
    """Bai hoc 13/11/2026: cat lang dau cau lem mat am "Th" (nho hon nguong 0,01) -> "Tham du" nghe thanh "am du"."""

    def test_giu_am_hoi_gio_truoc_tieng_to(self):
        hoi = tieng(0.10, bien_do=0.006)   # "Th": hoi gio, bien do < 0,01
        a = np.concatenate([lang(0.3), hoi, tieng(1.0), lang(0.3)])
        x, _ = cat_gon(a, SR)
        self.assertGreaterEqual(len(x) / SR, 1.0 + 0.10, "phai giu lai 0,10 s am nho o dau cau")

    def test_khong_nuot_tieng_bat_ngay_dau_file(self):
        # ban doc bat dau bang tieng bat "T" o mau dau tien: lam mem 10 ms nuot mat no ("Tham du" -> "am du")
        bat = tieng(0.006, bien_do=0.5)
        a = np.concatenate([bat, tieng(1.0, bien_do=0.1), lang(0.2)])
        x, _ = cat_gon(a, SR)
        n = len(bat)
        self.assertGreater(np.sum(x[:n] ** 2) / np.sum(a[:n] ** 2), 0.6, "tieng bat dau cau bi lam mem mat")


@unittest.skipUnless(shutil.which("ffmpeg"), "can ffmpeg")
class TestVideoQaHinhLechTieng(unittest.TestCase):
    def tao(self, hinh: float, tieng_: float) -> Path:
        out = Path(tempfile.mkdtemp()) / "thu.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=gray:s=320x180:r=25:d={hinh}",
                        "-f", "lavfi", "-i", f"sine=f=440:d={tieng_}", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-movflags", "+faststart", str(out)], check=True)
        return out

    def chay(self, f: Path) -> dict:
        import video_qa
        r = video_qa.check(Namespace(artifact=str(f), strict=True, audio=False, source=None, cut_authorized=False))
        return {c["name"]: c["status"] for c in r["checks"]}

    def test_hinh_ngan_hon_tieng_la_fail(self):
        self.assertEqual(self.chay(self.tao(1.0, 3.0)).get("av_length"), "FAIL")

    def test_hinh_bang_tieng_la_pass(self):
        self.assertEqual(self.chay(self.tao(2.0, 2.0)).get("av_length"), "PASS")


if __name__ == "__main__":
    unittest.main()
