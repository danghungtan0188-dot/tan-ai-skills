"""Test tim nhip nhac, phieu cham tham my va ham chuyen dong lo xo cho the HyperFrames."""

import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import wave
from pathlib import Path

import numpy as np

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC / "scripts"))

import tim_nhip_nhac as tn  # noqa: E402


class TestNhipNhac(unittest.TestCase):
    def test_goi_y_chi_doi_moc_gan_nhip(self):
        nhip = [1.0, 1.5, 2.0]
        self.assertEqual(tn.goi_y([1.1, 1.75, 2.0], nhip), [(1.1, 1.0)])

    def test_khong_co_nhip_thi_khong_goi_y(self):
        self.assertEqual(tn.goi_y([1.0], []), [])

    @unittest.skipUnless(importlib.util.find_spec("librosa"), "can librosa")
    def test_tim_dung_nhip_tieng_go_120_bpm(self):
        sr = 22050
        tin_hieu = np.zeros(sr * 10)
        go = (np.random.default_rng(0).standard_normal(400) * np.hanning(400) * 0.8)
        for k in range(20):
            i = int(k * 0.5 * sr)
            tin_hieu[i:i + 400] += go
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "go.wav"
            with wave.open(str(f), "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(sr)
                w.writeframes((np.clip(tin_hieu, -1, 1) * 32000).astype(np.int16).tobytes())
            bpm, nhip = tn.tim_nhip(f)
        self.assertAlmostEqual(bpm, 120, delta=6)
        khoang = np.diff(nhip)
        self.assertAlmostEqual(float(np.median(khoang)), 0.5, delta=0.05)


class TestLoXo(unittest.TestCase):
    MD = (GOC / "skills/motion-graphics-tan/references/chuyen-dong-lo-xo.md").read_text(encoding="utf-8")

    @unittest.skipUnless(shutil.which("node"), "can node")
    def test_ham_lo_xo_dung_dau_cuoi_va_do_nay(self):
        ham = re.search(r"```js\n(.*?)```", self.MD, re.S).group(1)
        ma = ham + """
const ra = {};
for (const z of [0.3, 0.5, 0.8]) {
  const f = loXo(z); let max = 0;
  for (let i = 0; i <= 1000; i++) max = Math.max(max, f(i / 1000));
  ra[z] = { dau: f(0), cuoi: f(1), gan_cuoi: f(0.999), max };
}
console.log(JSON.stringify(ra));
"""
        kq = json.loads(subprocess.run(["node", "-e", ma], capture_output=True, text=True, check=True).stdout)
        for z, v in kq.items():
            self.assertAlmostEqual(v["dau"], 0, places=6)
            self.assertEqual(v["cuoi"], 1)
            self.assertAlmostEqual(v["gan_cuoi"], 1, delta=0.01)
        self.assertGreater(kq["0.3"]["max"], kq["0.5"]["max"])
        self.assertGreater(kq["0.5"]["max"], 1.05)
        self.assertLess(kq["0.8"]["max"], 1.03)

    def test_skill_tro_toi_va_canh_bao_chu_dai(self):
        self.assertIn("chuyen-dong-lo-xo.md", (GOC / "skills/motion-graphics-tan/SKILL.md").read_text(encoding="utf-8"))
        self.assertIn("chữ dài", self.MD)


class TestPhieuThamMy(unittest.TestCase):
    PHIEU = (GOC / "evaluations/phieu-tham-my.md").read_text(encoding="utf-8")

    def test_khong_diem_tong_va_bat_buoc_bang_chung(self):
        self.assertIn("không có điểm tổng", self.PHIEU)
        self.assertIn("NOT RUN", self.PHIEU)
        self.assertEqual(len(re.findall(r"^\| [1-7] \|", self.PHIEU, re.M)), 7)

    def test_dung_video_dung_phieu_va_nhip_nhac(self):
        noi_dung = (GOC / ".claude/commands/dung-video.md").read_text(encoding="utf-8")
        self.assertIn("evaluations/phieu-tham-my.md", noi_dung)
        self.assertIn("tim_nhip_nhac.py", noi_dung)


if __name__ == "__main__":
    unittest.main()
