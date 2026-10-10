"""Cat gon mot ban doc TTS truoc khi ghep giong.

VieNeu thinh thoang phat them mot tieng ngan SAU mot quang lang o cuoi cau (video6: c28 lang 0,8 s roi
bat ra tieng 0,2 s — nguoi xem nghe "doc la"). Cat lang theo bien do > 0,01 khong bo duoc tieng do.
Ham nay: cat lang dau/cuoi nhu cu, roi bo doan tieng cuoi neu no ngan (< 0,6 s) va nam sau quang
lang that (>= 0,35 s, RMS khung 20 ms < 0,02). Nguong 0,02 bat dung 3/33 cau loi, khong dong cau nao khac.

    python cat_gon_tts.py vao.wav ra.wav
"""
import sys

import numpy as np

F = 0.02  # giay / khung do RMS


def cat_gon(a: np.ndarray, sr: int, lang: float = 0.35, ngan: float = 0.6, nen: float = 0.02):
    """Tra ve (am thanh da cat, so giay duoi la da bo)."""
    k = np.where(np.abs(a) > 0.01)[0]
    x = a[max(0, k[0] - int(0.04 * sr)): k[-1] + int(0.04 * sr)]
    n = int(F * sr)
    env = np.array([np.sqrt(np.mean(x[i:i + n] ** 2)) for i in range(0, len(x) - n + 1, n)])
    bo = 0.0
    while True:
        im, het = env < nen, len(env)
        j = het - 1
        while j >= 0 and im[j]:
            j -= 1
        cuoi = j
        while j >= 0 and not im[j]:
            j -= 1
        dau = j + 1
        g = j
        while g >= 0 and im[g]:
            g -= 1
        if (j - g) * F >= lang and (cuoi - dau + 1) * F < ngan and g > 0:
            bo += (het - g - 1) * F
            env = env[:g + 1 + int(0.1 / F)]
            x = x[:len(env) * n]
        else:
            break
    f = int(0.01 * sr)
    x = x.copy()
    x[:f] *= np.linspace(0, 1, f)
    x[-f:] *= np.linspace(1, 0, f)
    return x, bo


if __name__ == "__main__":
    import soundfile as sf

    a, sr = sf.read(sys.argv[1], dtype="float32")
    x, bo = cat_gon(a if a.ndim == 1 else a.mean(1), sr)
    sf.write(sys.argv[2], x, sr)
    print(f"bo duoi la {bo:.2f} s, con {len(x) / sr:.2f} s")
