"""skills/video-marketing/scripts: neo theo cau noi, vung mat, ghep lop sau nguoi.

TestGhepLopThat render video nho bang ffmpeg (nen + hieu ung trong suot + 'nguoi' trong suot) roi doc
mau diem anh: kiem thu tu lop va kenh alpha that, khong chi kiem chuoi lenh.
"""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "skills" / "video-marketing" / "scripts"))

import ghep_lop  # noqa: E402
import tach_nguoi  # noqa: E402
import tim_cau_noi  # noqa: E402


def _chu(van_ban: str, bat_dau: float = 0.0, moi_chu: float = 0.4):
    return [(w, round(bat_dau + i * moi_chu, 2), round(bat_dau + (i + 1) * moi_chu, 2))
            for i, w in enumerate(van_ban.split())]


class TestTimCauNoi(unittest.TestCase):
    def test_tim_dung_doan_cau(self):
        chu = _chu("xin chào các bạn hôm nay mình giới thiệu điện thoại máy tính bảng hay là máy tính nhé")
        r = tim_cau_noi.tim("điện thoại, máy tính bảng hay là máy tính", chu)
        self.assertEqual(r["do_khop"], 1.0)
        self.assertEqual(r["nghe_duoc"], "điện thoại máy tính bảng hay là máy tính")
        self.assertAlmostEqual(r["bat_dau"], 3.6)   # "điện" la chu thu 10 -> 9 * 0.4
        self.assertAlmostEqual(r["ket_thuc"], 7.2)  # "tính" cuoi la chu thu 18

    def test_whisper_nghe_sai_vai_chu_van_tim_duoc(self):
        chu = _chu("rồi bây giờ mình sẽ chỉ ba bước đăng ký tài khoản rất là đơn giản")
        r = tim_cau_noi.tim("ba bước đăng kí tài khoản", chu)  # "kí" vs whisper nghe "ký"
        self.assertGreaterEqual(r["do_khop"], tim_cau_noi.NGUONG)
        self.assertTrue(r["nghe_duoc"].startswith("ba bước"))

    def test_cau_khong_co_thi_khop_yeu(self):
        r = tim_cau_noi.tim("doanh thu tăng gấp đôi", _chu("hôm nay trời đẹp mình đi chơi công viên"))
        self.assertLess(r["do_khop"], tim_cau_noi.NGUONG)


class TestVungMat(unittest.TestCase):
    def test_gop_hop_mat_va_tren_dau(self):
        v = tach_nguoi.vung([(0.0, [(0.40, 0.30, 0.60, 0.55)]), (0.2, [(0.42, 0.28, 0.62, 0.56)]), (0.4, [])])
        self.assertTrue(v["co_mat"])
        self.assertEqual(v["hop_mat"], [0.4, 0.28, 0.62, 0.56])
        self.assertEqual(v["tren_dau"], 0.28)
        self.assertEqual((v["so_khung_co_mat"], v["so_khung"]), (2, 3))

    def test_khong_co_mat(self):
        self.assertFalse(tach_nguoi.vung([(0.0, []), (0.2, [])])["co_mat"])

    def test_cat_doan_co_du_va_preset_nhe(self):
        cmd = tach_nguoi.lenh_cat(Path("v.mp4"), 0.3, 5.0, Path("d.mp4"))
        self.assertEqual(cmd[cmd.index("-ss") + 1], "0.000")  # khong am
        self.assertEqual(cmd[cmd.index("-to") + 1], "5.500")
        self.assertEqual(cmd[cmd.index("-preset") + 1], "faster")


class TestLenhGhep(unittest.TestCase):
    def test_webm_giai_ma_bang_libvpx_va_thu_tu_lop(self):
        cmd = ghep_lop.lenh_ghep(Path("n.mp4"), Path("h.webm"), Path("p.webm"), 2, 4, 1.5, 1080, 1920, Path("r.mp4"))
        vao = [i for i, x in enumerate(cmd) if x == "-i"]
        self.assertEqual(len(vao), 3)
        for i in vao[1:]:
            self.assertEqual(cmd[i - 2:i], ["-c:v", "libvpx-vp9"])
        loc = cmd[cmd.index("-filter_complex") + 1]
        self.assertLess(loc.index("[0:v][hu]overlay"), loc.index("[a][ng]overlay"))
        self.assertIn("setpts=PTS-STARTPTS+1.500/TB[ng]", loc)

    def test_khong_tach_nguoi_thi_hieu_ung_len_tren(self):
        loc = ghep_lop.lenh_ghep(Path("n.mp4"), Path("h.mov"), None, 1, 2, 0, 720, 1280, Path("r.mp4"))
        self.assertIn("[0:v][hu]overlay=0:0:eof_action=pass:enable='between(t,1.000,2.000)'[v]",
                      loc[loc.index("-filter_complex") + 1])


@unittest.skipUnless(shutil.which("ffmpeg"), "can ffmpeg")
class TestGhepLopThat(unittest.TestCase):
    W, H = 180, 320

    def ff(self, *a):
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *a], check=True, timeout=120)

    def mau(self, video: Path, giay: float, x: int, y: int):
        import cv2
        cap = cv2.VideoCapture(str(video))
        cap.set(cv2.CAP_PROP_POS_MSEC, giay * 1000)
        ok, fr = cap.read()
        cap.release()
        self.assertTrue(ok)
        b, g, r = (int(v) for v in fr[y, x])
        return r, g, b

    def test_hieu_ung_sau_nguoi_dung_cua_so(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            nen, hu, ng, ra = t / "nen.mp4", t / "hu.webm", t / "ng.webm", t / "ra.mp4"
            self.ff("-f", "lavfi", "-i", f"color=c=0x808080:s={self.W}x{self.H}:r=25:d=4",
                    "-f", "lavfi", "-i", "sine=f=440:d=4", "-c:v", "libx264", "-preset", "faster",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(nen))
            # drawbox KHONG ghi kenh alpha -> dat o mau dac len nen trong suot bang overlay
            def o_trong_suot(ra, mau, x, y, canh, giay):
                self.ff("-f", "lavfi", "-i", f"color=c=black@0.0:s={self.W}x{self.H}:r=25:d={giay},format=rgba",
                        "-f", "lavfi", "-i", f"color=c={mau}:s={canh}x{canh}:r=25:d={giay},format=rgba",
                        "-filter_complex", f"[0][1]overlay={x}:{y}", "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p",
                        "-b:v", "0", "-crf", "20", str(ra))

            o_trong_suot(hu, "0x00ff00", 40, 110, 100, 4)  # hieu ung: o xanh la 100x100 o giua
            o_trong_suot(ng, "0xff0000", 70, 140, 40, 3)   # 'nguoi': o do 40x40 o tam, bat dau giay 0.5
            subprocess.run(ghep_lop.lenh_ghep(nen, hu, ng, 1.0, 3.0, 0.5, self.W, self.H, ra), check=True, timeout=120)

            def gan(m, mong):
                return all(abs(a - b) < 40 for a, b in zip(m, mong))

            self.assertTrue(gan(self.mau(ra, 0.5, 90, 160), (128, 128, 128)), "ngoai cua so: chi co nen")
            self.assertTrue(gan(self.mau(ra, 2.0, 50, 120), (0, 255, 0)), "trong cua so: co hieu ung")
            self.assertTrue(gan(self.mau(ra, 2.0, 90, 160), (255, 0, 0)), "nguoi nam TREN hieu ung")
            self.assertTrue(gan(self.mau(ra, 2.0, 10, 10), (128, 128, 128)), "phan trong suot de lo nen")
            self.assertTrue(gan(self.mau(ra, 3.6, 50, 120), (128, 128, 128)), "het cua so: hieu ung tat")
            r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=codec_name",
                                "-of", "csv=p=0", str(ra)], capture_output=True, text=True)
            self.assertEqual(r.stdout.strip(), "aac", "giu nguyen tieng")


if __name__ == "__main__":
    unittest.main()
