"""Nhat ky harness (observability/): ghi dung, khong lo noi dung lenh, khong bao gio lam hong hook."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
HOOKS = REPO_ROOT / ".claude" / "hooks"
sys.path.insert(0, str(REPO_ROOT))

from observability import nhat_ky, xem  # noqa: E402


class CoThuMuc(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)
        self.cu = os.environ.get("TAN_NHAT_KY_DIR")
        os.environ["TAN_NHAT_KY_DIR"] = str(self.dir)
        self.addCleanup(self.tra_lai)

    def tra_lai(self):
        if self.cu is None:
            os.environ.pop("TAN_NHAT_KY_DIR", None)
        else:
            os.environ["TAN_NHAT_KY_DIR"] = self.cu

    def chay_hook(self, script, payload):
        return subprocess.run([sys.executable, str(HOOKS / script)], input=json.dumps(payload),
                              text=True, capture_output=True, encoding="utf-8", cwd=REPO_ROOT)


class TestNhatKy(CoThuMuc):
    def test_ghi_va_doc_lai(self):
        nhat_ky.ghi_hook("guard_bash", "chan", "DROP DATABASE", {"tool_name": "Bash", "cwd": "C:/du-an/ban-hang",
                                                                  "session_id": "abcdef123456"})
        dong = nhat_ky.doc(1)
        self.assertEqual(len(dong), 1)
        self.assertEqual((dong[0]["hook"], dong[0]["du_an"], dong[0]["phien"]), ("guard_bash", "ban-hang", "abcdef12"))

    def test_bo_dong_trung_lien_tiep(self):
        for _ in range(2):  # trong repo nay hook chay 2 lan: settings repo + toan cuc
            nhat_ky.ghi_hook("guard_app", "hoi", "cai thu vien moi")
        nhat_ky.ghi_hook("guard_app", "hoi", "chay migration")
        self.assertEqual([d["ly_do"] for d in nhat_ky.doc(1)], ["cai thu vien moi", "chay migration"])

    def test_khong_bao_gio_nem_loi(self):
        (self.dir / "chan").write_text("la file, khong phai thu muc", encoding="utf-8")
        os.environ["TAN_NHAT_KY_DIR"] = str(self.dir / "chan" / "con")
        nhat_ky.ghi_hook("x", "chan", "y")
        nhat_ky.ghi_su_dung("skill", "z")

    def test_hook_chan_thi_co_dong_nhat_ky_khong_co_noi_dung_lenh(self):
        lenh = "rm -rf / ; echo matkhau-bi-mat-123"
        ra = self.chay_hook("guard_bash.py", {"tool_name": "Bash", "tool_input": {"command": lenh}, "cwd": "D:/abc"})
        self.assertEqual(ra.returncode, 2)
        dong = nhat_ky.doc(1)
        self.assertEqual((dong[-1]["hook"], dong[-1]["quyet_dinh"]), ("guard_bash", "chan"))
        self.assertNotIn("matkhau", json.dumps(dong, ensure_ascii=False))

    def test_ghi_su_dung_skill_agent_lenh(self):
        self.chay_hook("ghi_su_dung.py", {"tool_name": "Skill", "tool_input": {"skill": "video-use"}})
        self.chay_hook("ghi_su_dung.py", {"tool_name": "Agent", "tool_input": {"subagent_type": "video-editor"}})
        self.chay_hook("ghi_su_dung.py", {"prompt": "/dung-tu-kho D:/kho --dai 60 noi dung rieng tu"})
        self.chay_hook("ghi_su_dung.py", {"prompt": "loi nhan thuong khong ghi"})
        dong = nhat_ky.doc(1)
        self.assertEqual([(d["loai"], d["ten"]) for d in dong],
                         [("skill", "video-use"), ("agent", "video-editor"), ("lenh", "/dung-tu-kho")])
        self.assertNotIn("rieng tu", json.dumps(dong, ensure_ascii=False))

    def test_ghi_su_dung_khong_bao_gio_chan(self):
        for payload in ({}, {"tool_name": "Skill"}, {"prompt": 5}):
            ra = self.chay_hook("ghi_su_dung.py", payload)
            self.assertEqual((ra.returncode, ra.stdout), (0, ""))

    def test_xem_tom_tat_va_skill_chua_dung(self):
        nhat_ky.ghi_su_dung("skill", "video-use")
        nhat_ky.ghi_hook("guard_video", "chan", "x264 thieu preset")
        t = xem.tom_tat(nhat_ky.doc(1), ["video-use", "marketing"])
        self.assertEqual(t["dung"]["skill"]["video-use"], 1)
        self.assertEqual(t["skill_chua_dung"], ["marketing"])
        self.assertEqual(t["hook"][("guard_video", "chan", "x264 thieu preset")], 1)


if __name__ == "__main__":
    unittest.main()
