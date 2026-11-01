"""scripts/cai_skill_ngoai.py + skills-ngoai.json: danh sach skill ngoai repo dung, kiem dung, lenh cai dung.

Khong cai gi that: phan cai chi ghi lai lenh se chay.
"""

import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import cai_skill_ngoai as csn  # noqa: E402

DS = csn.doc_danh_sach()
TRONG_REPO = {p.name for p in (REPO_ROOT / "skills").iterdir() if (p / "SKILL.md").is_file()}


class TestDanhSach(unittest.TestCase):
    def test_skill_cli_khong_trung_skill_trong_repo(self):
        """Skill do CLI quan ma cung co trong skills/ = hai ban, se lech nhau."""
        cli = {t for g in DS["skills_cli"]["goi"] for t in g["skill"]}
        self.assertEqual(cli & TRONG_REPO, set())

    def test_lien_ket_va_cai_rieng_deu_la_skill_cua_repo(self):
        for ten in DS["lien_ket_repo"]["skill"] + DS["ban_cai_rieng"]["skill"]:
            self.assertIn(ten, TRONG_REPO, ten)

    def test_phien_ban_ghim_cung(self):
        self.assertRegex(DS["skills_cli"]["phien_ban"], r"^\d+\.\d+\.\d+$")
        for goi in DS["npm"]:
            self.assertRegex(goi["phien_ban"], r"^\d+\.\d+\.\d+$", goi["goi"])

    def test_video_editor_tro_toi_danh_sach(self):
        agent = (REPO_ROOT / ".claude" / "agents" / "video-editor.md").read_text(encoding="utf-8")
        self.assertIn("scripts/skills-ngoai.json", agent)
        self.assertIn("gsap-timeline", agent)


class TestKiemVaCai(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.home = Path(tmp.name)
        (self.home / ".claude" / "skills").mkdir(parents=True)

    def co_skill(self, ten):
        d = self.home / ".claude" / "skills" / ten
        d.mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text("---\nname: x\n---\n", encoding="utf-8")

    def test_bao_thieu_va_phan_biet_ban_chep_rieng(self):
        self.co_skill("gsap-core")
        self.co_skill("remotion-markup")  # thu muc that, khong phai junction ve repo
        kq = {(m["loai"], m["ten"]): m for m in csn.kiem(DS, self.home, REPO_ROOT, co_lenh=lambda _: None)}
        self.assertTrue(kq[("skills-cli", "gsap-core")]["dat"])
        self.assertFalse(kq[("skills-cli", "gsap-timeline")]["dat"])
        self.assertFalse(kq[("npm", "playwright-cli")]["dat"])
        self.assertEqual(kq[("lien-ket", "remotion-markup")]["ghi_chu"], "ban chep rieng")
        self.assertEqual(kq[("lien-ket", "remotion-docs")]["ghi_chu"], "thieu")

    def test_cai_chi_chay_lenh_cho_phan_thieu(self):
        for g in DS["skills_cli"]["goi"]:
            for t in g["skill"]:
                if t != "gsap-timeline":
                    self.co_skill(t)
        thieu = [m for m in csn.kiem(DS, self.home, REPO_ROOT, co_lenh=lambda _: "co")
                 if not m["dat"] and m["loai"] in ("skills-cli", "npm")]
        da_chay = []
        cu = csn._chay
        csn._chay = lambda cmd, cwd: da_chay.append(cmd) or True
        try:
            csn.cai(DS, thieu, False, self.home, REPO_ROOT)
        finally:
            csn._chay = cu
        self.assertEqual(da_chay, [["npx", "-y", "skills@" + DS["skills_cli"]["phien_ban"], "add",
                                    "https://github.com/greensock/gsap-skills", "--skill", "gsap-timeline",
                                    "-g", "-y"]])


if __name__ == "__main__":
    unittest.main()
