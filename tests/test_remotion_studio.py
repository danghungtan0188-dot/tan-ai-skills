#!/usr/bin/env python3
"""Gom test cua remotion-studio/tests vao lenh test chung.

Chay: python -m unittest discover -s tests
Test cua remotion-studio import `scripts.prepare_project`, nen phai them thu muc
remotion-studio vao sys.path truoc khi nap.
"""

import sys
import unittest
from pathlib import Path

STUDIO = Path(__file__).resolve().parents[1] / "remotion-studio"


def load_tests(loader, tests, pattern):
    if str(STUDIO) not in sys.path:
        sys.path.insert(0, str(STUDIO))
    tests.addTests(unittest.TestLoader().discover(str(STUDIO / "tests")))
    return tests
