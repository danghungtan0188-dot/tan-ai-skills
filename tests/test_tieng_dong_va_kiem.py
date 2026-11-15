"""motion-graphics-tan: bo tieng dong sfx (claude-motion, MIT) va look.py (motionmaxxing, Apache 2.0).

Kiem: giu giay phep goc, sfx tao WAV dung luat (chay that, ~1 s, khong can ffmpeg), look.py chi them -threads 2.
"""

import importlib
import json
import re
import struct
import subprocess
import sys
import tempfile
import unittest
import wave
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "skills" / "motion-graphics-tan" / "scripts"


class TestGiayPhep(unittest.TestCase):
    def test_giu_giay_phep_va_ghi_nguon(self):
        self.assertIn("MIT License", (SCRIPTS / "sfx" / "LICENSE").read_text(encoding="utf-8"))
        self.assertIn("Apache License", (SCRIPTS / "giay-phep" / "motionmaxxing-LICENSE.txt").read_text(encoding="utf-8"))
        self.assertTrue((SCRIPTS / "giay-phep" / "motionmaxxing-NOTICE.txt").is_file())
        ref = SCRIPTS.parent / "references"
        self.assertIn("whaleyxbt/claude-motion", (ref / "tieng-dong.md").read_text(encoding="utf-8"))
        self.assertIn("Tejashmakwana/motionmaxxing", (ref / "kiem-re-tien.md").read_text(encoding="utf-8"))
        self.assertIn("MIT License", (SCRIPTS / "giay-phep" / "motion-prompt-LICENSE.txt").read_text(encoding="utf-8"))
        tu_dien = (ref / "tu-dien-chuyen-dong.md").read_text(encoding="utf-8")
        self.assertIn("showheyohtaki/motion-prompt", tu_dien)
        # Du 48 ten (#001-#048); the "san co" ghi trong tu dien phai ton tai that.
        self.assertEqual(len(re.findall(r"^\| 0\d\d \|", tu_dien, re.M)), 48)
        co = {p.name for p in (SCRIPTS.parent / "assets" / "ky-thuat").iterdir()} | {p.name for p in (SCRIPTS.parent / "assets" / "mau").iterdir()}
        dong = re.findall(r"^\| 0\d\d \|.*", tu_dien, re.M)
        for d in dong:
            o_cuoi = d.rstrip(" |").split("|")[-1]  # cot "The san" (bang motion) hoac cau lenh mau (bang camera)
            for the in re.findall(r"`([a-z0-9-]+)`", o_cuoi):
                if not the.endswith("md"):
                    self.assertIn(the, co)

    def test_look_py_chi_them_threads_va_ghi_ro(self):
        """Apache 2.0 muc 4(b): file sua phai ghi ro da sua. May hay sap -> moi ffmpeg chay 2 luong."""
        src = (SCRIPTS / "look.py").read_text(encoding="utf-8")
        self.assertIn("[tan-ai-skills] Sua doi", src)
        # Dem lenh chay ffmpeg (["ffmpeg", ...]); dong kiem may co ffmpeg khong ("ffmpeg", "ffprobe") khong tinh.
        self.assertEqual(src.count('["ffmpeg"'), 3)
        self.assertEqual(src.count('["ffmpeg"'), src.count('"-threads", "2"'))


class TestSfx(unittest.TestCase):
    def test_mau_o_hoi_lat_ra_wav_dung_chuan(self):
        cue = SCRIPTS / "sfx" / "cues" / "o_hoi_lat.py"
        moc = json.loads(cue.with_suffix(".json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tam:
            ra = Path(tam) / "a.wav"
            r = subprocess.run([sys.executable, "-m", "sfx", str(cue), "--out", str(ra)], cwd=SCRIPTS,
                               capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("-14.0 LUFS", r.stdout)
            with wave.open(str(ra)) as w:
                self.assertEqual((w.getframerate(), w.getnchannels()), (48000, 2))
                self.assertAlmostEqual(w.getnframes() / 48000, moc["duration"], places=2)
                du_lieu = w.readframes(w.getnframes())
            # Ban da master: dinh mau <= -1,9 dBFS (bo sfx giu true peak <= -2 dBFS).
            mau = struct.unpack(f"<{len(du_lieu) // 2}h", du_lieu)
            self.assertLessEqual(max(abs(v) for v in mau) / 32768, 10 ** (-1.9 / 20))

    def test_tieng_tao_ra_giong_nhau_moi_lan(self):
        sys.path.insert(0, str(SCRIPTS))
        try:
            synth = importlib.import_module("sfx.synth")
            self.assertEqual(synth.pop(800, 400), synth.pop(800, 400))
        finally:
            sys.path.remove(str(SCRIPTS))


if __name__ == "__main__":
    unittest.main()
