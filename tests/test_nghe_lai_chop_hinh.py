"""Test nghe lai sau cat, kiem chop hinh va cac noi dung lay tu skill CapCut, Seedance."""

import sys
import unittest
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC / "scripts"))

import kiem_chop_hinh as ch  # noqa: E402
import nghe_lai_sau_cat as nl  # noqa: E402


def tu(cau):
    return [(c, float(i)) for i, c in enumerate(cau.split())]


class TestNgheLai(unittest.TestCase):
    def test_bat_cum_lap_lien_tiep_bo_qua_dau_cau(self):
        self.assertEqual(nl.tim_lap(tu("hôm nay mình, mình sẽ nói hôm nay mình rồi")), [])
        self.assertEqual(nl.tim_lap(tu("ví dụ khác, ví dụ khác nhé")), [(0.0, "ví dụ khác")])

    def test_lap_mot_chu_khong_bao(self):
        self.assertEqual(nl.tim_lap(tu("đi từ từ thôi")), [])

    def test_khac_dau_thi_khong_phai_lap(self):
        self.assertEqual(nl.tim_lap(tu("mua bán mùa bàn")), [])

    def test_lap_ba_lan_bao_moi_cap_mot_lan(self):
        self.assertEqual(len(nl.tim_lap(tu("xin chào xin chào xin chào các bạn"))), 1)

    def test_lap_ca_cau_dai_du_whisper_nghe_lech_va_co_chu_xen(self):
        cau = "người dân có thể tiếp cận nhiều tiện ích thiết thực ngay trên ứng dụng"
        lap = nl.tim_lap(tu(f"{cau} vnid đồ 2 {cau} vned"))
        self.assertEqual(len(lap), 1)
        self.assertIn("tiện ích", lap[0][1])

    def test_hai_cau_khac_nhau_khong_bao(self):
        self.assertEqual(nl.tim_lap(tu("hôm nay mình giới thiệu ứng dụng mới ngày mai mình giao sản phẩm thật")), [])

    def test_ghi_loi_co_moc_giay(self):
        self.assertEqual(nl.ghi_loi([(65.2, " xin chào ")]), "[01:05.2] xin chào\n")


class TestChopHinh(unittest.TestCase):
    def test_dung_cu_cat_thi_dat(self):
        self.assertEqual(ch.kiem([10.0], [{"start": 10.0, "end": 12.0}]), [])

    def test_bat_dau_sat_sau_cu_cat(self):
        loi = ch.kiem([10.0], [{"start": 10.3, "end": 12.0}])
        self.assertEqual(len(loi), 1)
        self.assertIn("10.0s", loi[0])

    def test_ket_thuc_sat_truoc_cu_cat(self):
        loi = ch.kiem([12.2], [{"start": 10.0, "end": 12.0}])
        self.assertEqual(len(loi), 1)
        self.assertIn("keo den 12.2s", loi[0])

    def test_hai_do_hoa_sat_nhau(self):
        loi = ch.kiem([], [{"start": 5, "end": 6}, {"start": 1, "end": 4.8}])
        self.assertEqual(len(loi), 1)

    def test_xa_cu_cat_thi_dat_va_doan_sai_bi_tu_choi(self):
        self.assertEqual(ch.kiem([5.0], [{"start": 6.0, "end": 7.0}]), [])
        with self.assertRaises(ValueError):
            ch.kiem([], [{"start": 3, "end": 2}])


class TestNoiDung(unittest.TestCase):
    def test_dung_video_goi_du_buoc_va_nhip_dung(self):
        noi_dung = (GOC / ".claude/commands/dung-video.md").read_text(encoding="utf-8")
        for chu in ("nghe_lai_sau_cat.py", "kiem_chop_hinh.py", "nhip-dung-nguoi-noi.md", "NGHE LẠI:", "CHỚP HÌNH:"):
            self.assertIn(chu, noi_dung)

    def test_nhip_dung_mac_dinh_tat_va_giu_luat_khong_cat_loi(self):
        noi_dung = (GOC / "skills/video-marketing/references/nhip-dung-nguoi-noi.md").read_text(encoding="utf-8")
        self.assertIn("mặc định tắt", noi_dung)
        self.assertIn("cut_authorized", noi_dung)

    def test_skill_prompt_khong_tu_chay_dich_vu_tra_phi(self):
        goc = GOC / "skills/viet-prompt-video-ai"
        noi_dung = (goc / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("trả phí", noi_dung)
        self.assertTrue((goc / "references/character-sheet.md").exists())


if __name__ == "__main__":
    unittest.main()
