"""Danh muc chuyen canh GPU kieu CapCut: du 154 goi, khong trung, ghi ro chua chay va khong thay FFmpeg dang dung."""

import re
import unittest
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
DANH_MUC = GOC / "skills/hieu-ung-video/references/chuyen-canh-gpufx.md"


class TestChuyenCanhGpufx(unittest.TestCase):
    NOI_DUNG = DANH_MUC.read_text(encoding="utf-8")

    def test_du_154_goi_khong_trung(self):
        goi = re.findall(r"^\| `([a-z0-9-]+)` \|", self.NOI_DUNG, re.M)
        self.assertEqual(len(goi), 154)
        self.assertEqual(len(set(goi)), 154)

    def test_ghi_ro_chua_chay_va_khong_thay_ffmpeg(self):
        self.assertIn("Chưa chạy trên máy này", self.NOI_DUNG)
        self.assertIn("không thay FFmpeg đang dùng", self.NOI_DUNG)
        self.assertIn("-preset faster", self.NOI_DUNG)

    def test_duoc_noi_tu_hai_skill(self):
        for p in ("skills/hieu-ung-video/SKILL.md", "skills/video-marketing/references/nhip-dung-nguoi-noi.md"):
            self.assertIn("chuyen-canh-gpufx.md", (GOC / p).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
