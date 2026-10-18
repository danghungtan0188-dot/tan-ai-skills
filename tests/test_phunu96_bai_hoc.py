"""Bai hoc tu video 96 nam Hoi LHPN Viet Nam (2026-10-18): may dang le bat duoc ma khong bat.

Bo chon ban TTS (san cung: it chu kho sai nhat truoc) chon trung ban LAP CHU s2d_5 — dai 4,9 s
trong khi cac ban khac 3,1 s — vi ban do sai it chu kho nhat. Gio loai ban dai > 1,3 x trung vi truoc.
"""

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "skills" / "bien-tap-video-thong-minh-song-ngu-tan" / "scripts"))

from chon_ban_tts import chon_ban  # noqa: E402


def ban(ten, cer, thieu, f0r, dur):
    return {"ten": ten, "cer": cer, "thieu": thieu, "f0r": f0r, "dur": dur}


class TestChonBanTTS(unittest.TestCase):
    def test_loai_ban_lap_chu_du_sai_it_chu_kho_nhat(self):
        # so lieu that cua cum s2d (6 ban)
        ds = [
            ban("s2d_1", 0.163, ["bền bỉ", "cống hiến", "vun đắp"], 18.7, 3.1),
            ban("s2d_2", 0.163, ["bền bỉ", "cống hiến", "vun đắp"], 9.1, 3.3),
            ban("s2d_3", 0.186, ["bền bỉ", "cống hiến", "vun đắp"], 9.2, 3.3),
            ban("s2d_4", 0.093, ["bền bỉ", "cống hiến", "vun đắp"], 14.7, 3.1),
            ban("s2d_5", 0.442, ["vun đắp"], 18.1, 4.9),  # doc lap "vun dap hanh phuc"
            ban("s2d_6", 0.186, ["bền bỉ", "vun đắp"], 17.8, 3.2),
        ]
        self.assertNotEqual(chon_ban(ds), "s2d_5")
        self.assertEqual(chon_ban(ds), "s2d_6")

    def test_phat_am_truoc_ngu_dieu(self):
        # ban ngu dieu dep hon nhung CER vuot san thi khong duoc chon
        ds = [ban("a", 0.00, [], 6.0, 2.0), ban("b", 0.05, [], 11.0, 2.0)]
        self.assertEqual(chon_ban(ds), "a")

    def test_dong_san_thi_xet_ngu_dieu(self):
        ds = [ban("a", 0.00, [], 6.0, 2.0), ban("b", 0.02, [], 11.0, 2.1)]
        self.assertEqual(chon_ban(ds), "b")


if __name__ == "__main__":
    unittest.main()
