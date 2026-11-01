#!/usr/bin/env python3
"""Bai hoc trong memory phai co chot chan that, khong chi ghi chu.

Chay: python -m unittest tests.test_bai_hoc_chot_chan -v

- Ban do docs/bai-hoc-va-chot-chan.md: moi dong loai "may" phai tro toi
  test/hook/code CO THAT (test:TenClass, hook:ten.py, code:duong/dan).
- Bai hoc remotion.exe bi Windows chan: mau Remotion moi khong dung OffthreadVideo.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BAN_DO = REPO_ROOT / "docs" / "bai-hoc-va-chot-chan.md"
LOAI = {"máy", "người"}


def dong_bang(text: str) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        if not line.startswith("|") or set(line) <= set("|-: "):
            continue
        o = [c.strip() for c in line.strip("|").split("|")]
        if len(o) == 4 and o[0] != "Bài học":
            rows.append(o)
    return rows


def lop_test_co_that() -> set[str]:
    ten = set()
    for path in (REPO_ROOT / "tests").glob("test_*.py"):
        ten |= set(re.findall(r"^class (\w+)\(", path.read_text(encoding="utf-8"), re.M))
    return ten


class TestBanDoBaiHoc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = dong_bang(BAN_DO.read_text(encoding="utf-8"))

    def test_co_bai_hoc(self):
        self.assertGreaterEqual(len(self.rows), 10)

    def test_loai_hop_le(self):
        for bai, loai, _, _ in self.rows:
            with self.subTest(bai=bai):
                self.assertIn(loai, LOAI)

    def test_bai_hoc_may_co_cho_neo_that(self):
        lop = lop_test_co_that()
        for bai, loai, _, neo in self.rows:
            if loai != "máy":
                continue
            cac_neo = re.findall(r"`(test|hook|code):([^`]+)`", neo)
            with self.subTest(bai=bai):
                self.assertTrue(cac_neo, "Bai hoc loai 'may' phai co cho neo")
            for dang, gia_tri in cac_neo:
                with self.subTest(bai=bai, neo=f"{dang}:{gia_tri}"):
                    if dang == "test":
                        self.assertIn(gia_tri, lop, "Khong co class test nay")
                    elif dang == "hook":
                        self.assertTrue((REPO_ROOT / ".claude" / "hooks" / gia_tri).is_file())
                    else:
                        self.assertTrue((REPO_ROOT / gia_tri).exists())


class TestRemotionKhongDungOffthreadVideo(unittest.TestCase):
    """remotion.exe bi Windows chan -> OffthreadVideo loi spawn UNKNOWN."""

    MAU_CU = {"NguoiNoiPip.tsx", "PhuNu96.tsx"}

    def test_mau_moi_dung_video_cua_remotion_media(self):
        dung = re.compile(r"import\s*\{[^}]*\bOffthreadVideo\b[^}]*\}|<OffthreadVideo\b")
        for goc in ("do-hoa/src", "remotion-studio/src"):
            for path in sorted((REPO_ROOT / goc).rglob("*.tsx")):
                if path.name in self.MAU_CU:
                    continue
                with self.subTest(file=path.relative_to(REPO_ROOT).as_posix()):
                    self.assertIsNone(
                        dung.search(path.read_text(encoding="utf-8")),
                        "Dung Video cua @remotion/media thay cho OffthreadVideo")


if __name__ == "__main__":
    unittest.main()
