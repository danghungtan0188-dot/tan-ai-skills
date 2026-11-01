"""Test sync_skills.ban_chep_rieng: bat ban chep rieng o ~/.claude/skills da lech repo."""

import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import sync_skills  # noqa: E402


class TestBanChepRieng(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.home = Path(tmp.name)
        self.nguon = REPO_ROOT / "skills" / "humanizer"

    def chep(self, sua=None, them=None):
        dich = self.home / "humanizer"
        for f in sync_skills.relevant_files(self.nguon):
            ra = dich / f.relative_to(self.nguon)
            ra.parent.mkdir(parents=True, exist_ok=True)
            ra.write_bytes(f.read_bytes())
        if sua:
            (dich / "SKILL.md").write_text(sua, encoding="utf-8")
        for ten in them or []:
            (dich / ten).mkdir(parents=True, exist_ok=True)
            (dich / ten / "x.txt").write_text("cai dat", encoding="utf-8")

    def test_ban_chep_khop_thi_cho_qua_ke_ca_co_moi_truong_cai_dat(self):
        self.chep(them=[".venv", "video_use.egg-info"])
        (self.home / "humanizer" / "uv.lock").write_text("lock", encoding="utf-8")
        self.assertEqual(sync_skills.ban_chep_rieng([self.nguon], self.home), [])

    def test_ban_chep_lech_thi_bao(self):
        self.chep(sua="ban cu")
        self.assertEqual(sync_skills.ban_chep_rieng([self.nguon], self.home), ["humanizer"])

    def test_khong_co_ban_chep_thi_cho_qua(self):
        self.assertEqual(sync_skills.ban_chep_rieng([self.nguon], self.home), [])


if __name__ == "__main__":
    unittest.main()
