"""docs/harness-video.md: moi duong dan trong dau backtick phai co that.

Ban do kien truc ma tro toi file khong ton tai = tai lieu dang bia. Thanh phan
"sẽ tạo" viet khong co backtick nen khong bi kiem.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "harness-video.md"
DUONG_DAN = re.compile(r"`([A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-]*)+|[A-Za-z0-9_.\-]+\.(?:md|py|json))`")


class TestHarnessVideoDoc(unittest.TestCase):
    def test_moi_duong_dan_deu_co_that(self):
        tim_thay = DUONG_DAN.findall(DOC.read_text(encoding="utf-8"))
        self.assertGreater(len(tim_thay), 20, "ban do phai dan nguon cu the")
        thieu = sorted({p for p in tim_thay if not (REPO_ROOT / p.rstrip("/")).exists()})
        self.assertEqual(thieu, [], f"docs/harness-video.md tro toi duong dan khong co: {thieu}")

    def test_thanh_phan_thieu_khong_ghi_nhu_da_co(self):
        for ten in ("evaluations", "observability"):
            if not (REPO_ROOT / ten).exists():
                self.assertNotIn(f"`{ten}/", DOC.read_text(encoding="utf-8"),
                                 f"{ten}/ chua co: phai ghi 'sẽ tạo', khong dat trong backtick")


if __name__ == "__main__":
    unittest.main()
