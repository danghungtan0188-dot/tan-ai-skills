import argparse
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.prepare_project import PrepareError, build_props, parse_srt


class TestSrt(unittest.TestCase):
    def test_parse_srt_sang_caption(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cap.srt"
            path.write_text(
                "1\n00:00:01,250 --> 00:00:03,500\nXin chào.\n\n"
                "2\n00:00:04,000 --> 00:00:05,000\nATT NEWS\n",
                encoding="utf-8",
            )
            cues = parse_srt(path)
        self.assertEqual(len(cues), 2)
        self.assertEqual(cues[0]["startMs"], 1250)
        self.assertEqual(cues[0]["text"], "Xin chào.")

    def test_chan_moc_nguoc(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.srt"
            path.write_text("1\n00:00:03,000 --> 00:00:02,000\nSai\n", encoding="utf-8")
            with self.assertRaises(PrepareError):
                parse_srt(path)


class TestBuildProps(unittest.TestCase):
    def _args(self, **changes):
        values = dict(
            title="Tin",
            subtitle="",
            kicker="ATT NEWS",
            video=None,
            image=None,
            audio=None,
            captions=None,
            duration=8.0,
            width=1920,
            height=1080,
            background_color="#031a3a",
            accent_color="#e31b23",
        )
        values.update(changes)
        return argparse.Namespace(**values)

    def test_chan_hai_loai_nen(self):
        args = self._args(video=Path("a.mp4"), image=Path("b.jpg"))
        with self.assertRaises(PrepareError):
            build_props(args)

    @mock.patch("scripts.prepare_project.probe_duration", return_value=12.5)
    @mock.patch("scripts.prepare_project.copy_asset", return_value="assets/audio.wav")
    def test_lay_thoi_luong_tu_audio(self, _copy, _probe):
        props = build_props(self._args(audio=Path("audio.wav"), duration=None))
        self.assertEqual(props["durationSeconds"], 12.5)
        self.assertEqual(props["voiceover"], "assets/audio.wav")


if __name__ == "__main__":
    unittest.main()
