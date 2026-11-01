"""scripts/kiem_brief.py: ban yeu cau /dung-video phai khop VideoBrief; sai thi bao ro truong nao."""

import json
import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import kiem_brief  # noqa: E402

VI_DU = json.loads((REPO_ROOT / "data-contracts" / "examples" / "video-brief.json").read_text(encoding="utf-8"))
LENH = (REPO_ROOT / ".claude" / "commands" / "dung-video.md").read_text(encoding="utf-8")


class TestKiemBrief(unittest.TestCase):
    def test_vi_du_hop_le(self):
        self.assertEqual(kiem_brief.loi(VI_DU), [])

    def test_bat_kieu_loi_haiku_tung_mac(self):
        """Lan thu that 01/11: Haiku tu dat ten truong va de source la object."""
        sai = {**VI_DU, "loai": "ban_tin", "source": {"folder": "kho"}}
        del sai["video_type"]
        loi = " | ".join(kiem_brief.loi(sai))
        self.assertIn("'video_type' is a required property", loi)
        self.assertIn("'loai' was unexpected", loi)
        self.assertIn("not of type 'string'", loi)

    def test_khuon_trong_lenh_dung_ten_truong_cua_hop_dong(self):
        khuon = json.loads(re.search(r"```json\n(.*?)```", LENH, re.S).group(1))
        truong = json.loads((REPO_ROOT / "data-contracts" / "video.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(list(khuon), list(truong["$defs"]["VideoBrief"]["properties"]))

    def test_lenh_co_hai_cong_duyet(self):
        self.assertIn("CỔNG DUYỆT 1", LENH)
        self.assertIn("CỔNG DUYỆT 2", LENH)
        self.assertIn("kiem_brief.py", LENH)


if __name__ == "__main__":
    unittest.main()
