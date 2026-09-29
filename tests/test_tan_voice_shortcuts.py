import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "skills" / "tan-giong-doc-ban-tin" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import voices_store  # noqa: E402


class TestATTVoiceShortcuts(unittest.TestCase):
    def test_mc_an_thanh_thuy(self):
        self.assertEqual(
            voices_store.resolve_voice_name("mc-an-thanh-thuy"),
            "MC Đài An Thạnh Thủy",
        )
        self.assertEqual(
            voices_store.resolve_voice_name("MC-ATT"),
            "MC Đài An Thạnh Thủy",
        )

    def test_hung_tan_chan_that(self):
        self.assertEqual(
            voices_store.resolve_voice_name("hung-tan-chan-that"),
            "Giọng Hùng Tân chân thật",
        )


if __name__ == "__main__":
    unittest.main()
