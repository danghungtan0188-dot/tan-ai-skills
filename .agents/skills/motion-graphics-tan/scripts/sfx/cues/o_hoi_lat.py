"""Tieng dong cho the ky thuat `o-hoi-lat` (assets/ky-thuat/o-hoi-lat): moc thoi gian lay tu o_hoi_lat.json, khop timeline GSAP cua the.

    cd skills/motion-graphics-tan/scripts
    python -m sfx sfx/cues/o_hoi_lat.py --out <thu-muc>/o-hoi-lat.wav

Mau de chep cho the khac: moi moc chi doc tu file JSON, khong go so tay trong ham score.
"""

import tempfile
from pathlib import Path

from sfx.synth import chime, envelope, pad, pop, whoosh

TIMELINE = str(Path(__file__).with_suffix(".json"))
OUT = str(Path(tempfile.gettempdir()) / "motion-graphics-tan" / "o-hoi-lat.wav")
TARGET_LUFS = -14.0  # chuan Facebook/TikTok da do o 81 reel (-14 LUFS)

# Mot giong duy nhat (Do truong): nen pad va not pop deu nam trong Do, cao dan theo tung o lat.
NEN = [130.81, 196.0, 261.63, 329.63]
NOT_LAT = [783.99, 987.77, 1174.66]


def score(mix, tl):
    dur = tl["duration"]
    mix.put_stereo(0, *pad(dur, [(0, NEN)], volume=envelope([(0, 0), (0.6, 1), (dur - 0.6, 1), (dur, 0)])), gain=0.03)
    mix.put(tl["vao"], whoosh(0.35, 400, 2200, peak=0.4), 0.12)
    for i, t in enumerate(tl["lat"]):
        # O lat tu tren xuong: pan nhe trai -> phai, cao do tang dan de nghe thay "tien len".
        mix.put(t, whoosh(0.2, 900, 3000, peak=0.35), 0.08, -0.2 + i * 0.2)
        mix.put(t + 0.18, pop(NOT_LAT[i], NOT_LAT[i] * 0.5), 0.28, -0.2 + i * 0.2)
    mix.put(tl["xong"], chime([1046.5, 1318.5, 1568.0], dur=1.0, tau=0.4), 0.12)
