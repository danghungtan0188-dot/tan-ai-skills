#!/usr/bin/env python3
"""Test cho script cua hai skill video: song ngu va chuyen-gia-edit-video-tan.

Bat cac loi that da gap: cue qua dai tran 4 dong, banner tran canh, phu de chong lap,
dich thieu thuat ngu/so lieu, do hoa che mat, tuong phan thap, chu qua nho.
"""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SONG_NGU = REPO_ROOT / "skills" / "bien-tap-video-thong-minh-song-ngu-tan" / "scripts"
CHUYEN_GIA = REPO_ROOT / "skills" / "chuyen-gia-edit-video-tan" / "scripts"
for p in (SONG_NGU, CHUYEN_GIA):
    sys.path.insert(0, str(p))

import broadcast_kit  # noqa: E402
import build_bilingual  # noqa: E402
import callouts  # noqa: E402
import check_subtitles  # noqa: E402
import check_translation  # noqa: E402
import export_subtitles  # noqa: E402
import icons  # noqa: E402
import validate_graphics  # noqa: E402

WORDS = [{"s": i * 0.5, "e": i * 0.5 + 0.4, "w": f"w{i}"} for i in range(30)]


class TestBuildBilingual(unittest.TestCase):
    def test_moc_thoi_gian_theo_chi_so_tu(self):
        d = build_bilingual.build(WORDS, [[0, 3, "Xin chao", "Hello"]])
        self.assertEqual(d["segments"][0]["start"], 0.02)
        self.assertEqual(d["segments"][0]["end"], 1.9)
        self.assertTrue(d["meta"]["needs_review"])
        self.assertTrue(d["meta"]["english_above_vietnamese"])

    def test_cue_khong_chong_nhau(self):
        d = build_bilingual.build(WORDS, [[0, 3, "a", "a"], [2, 6, "b", "b"]])
        s = d["segments"]
        self.assertGreaterEqual(s[1]["start"], s[0]["end"])

    def test_chan_cue_qua_dai(self):
        with self.assertRaises(SystemExit):
            build_bilingual.build(WORDS, [[0, 3, "x" * 53, "ok"]])

    def test_chan_chi_so_sai(self):
        with self.assertRaises(SystemExit):
            build_bilingual.build(WORDS, [[5, 2, "a", "b"]])


class TestCheckSubtitles(unittest.TestCase):
    def kiem(self, text, kind="srt", **kw):
        return check_subtitles.check(check_subtitles.parse(text, kind), **kw)

    def test_srt_hop_le(self):
        loi, canh = self.kiem("1\n00:00:01,000 --> 00:00:03,000\nXin chao\n")
        self.assertEqual((loi, canh), ([], []))

    def test_bat_chong_lap_va_cue_rong(self):
        loi, _ = self.kiem("1\n00:00:01,000 --> 00:00:05,000\nA\n\n2\n00:00:03,000 --> 00:00:06,000\nB\n")
        self.assertTrue(any("chồng" in x for x in loi))
        loi, _ = self.kiem("1\n00:00:01,000 --> 00:00:03,000\n")
        self.assertTrue(any("rỗng" in x for x in loi))

    def test_bat_timecode_sai(self):
        loi, _ = self.kiem("1\n00:00:01,000 --> 00:00:61,000\nA\n")
        self.assertTrue(any("timecode sai" in x for x in loi))
        loi, _ = self.kiem("1\n00:00:05,000 --> 00:00:02,000\nA\n")
        self.assertTrue(any("không nhỏ hơn" in x for x in loi))

    def test_canh_bao_ngan_dai_va_toc_do(self):
        _, canh = self.kiem("1\n00:00:01,000 --> 00:00:01,300\nA\n")
        self.assertTrue(any("quá ngắn" in x for x in canh))
        _, canh = self.kiem(f"1\n00:00:01,000 --> 00:00:09,000\n{'x' * 50}\n")
        self.assertTrue(any("ký tự (>" in x for x in canh))
        _, canh = self.kiem(f"1\n00:00:01,000 --> 00:00:02,000\n{'x' * 40}\n")
        self.assertTrue(any("quá nhanh" in x for x in canh))

    def test_vtt_bo_qua_header(self):
        cues = check_subtitles.parse("WEBVTT\n\n00:00:01.000 --> 00:00:03.000\nEN\nVI\n", "vtt")
        self.assertEqual(len(cues), 1)
        self.assertEqual(cues[0]["lines"], ["EN", "VI"])

    def test_song_ngu_tinh_theo_dong_dai_nhat(self):
        hai = "1\n00:00:01,000 --> 00:00:03,000\n" + "x" * 30 + "\n" + "y" * 30 + "\n"
        self.assertTrue(any("quá nhanh" in x for x in self.kiem(hai)[1]))
        self.assertFalse(any("quá nhanh" in x for x in self.kiem(hai, song_ngu=True)[1]))


class TestExportSubtitles(unittest.TestCase):
    segs = [{"start": 1.0, "end": 3.0, "vi": "Xin chao", "en": "Hello"}]

    def test_srt_va_vtt(self):
        self.assertIn("00:00:01,000 --> 00:00:03,000", export_subtitles.srt(self.segs, "vi"))
        self.assertTrue(export_subtitles.vtt(self.segs).startswith("WEBVTT"))
        self.assertIn("Hello\nXin chao", export_subtitles.vtt(self.segs))

    def test_ngat_dong_dai(self):
        self.assertEqual(export_subtitles.wrap("a b", 42), ["a b"])
        self.assertEqual(len(export_subtitles.wrap(" ".join(["dai"] * 30), 42)), 2)

    def test_bon_che_do_ra_du_file(self):
        with tempfile.TemporaryDirectory() as t:
            src = Path(t) / "bi.json"
            src.write_text(json.dumps({"segments": self.segs}), encoding="utf-8")
            subprocess.run([sys.executable, str(SONG_NGU / "export_subtitles.py"), str(src),
                            "--out-dir", t, "--stem", "x"], check=True, capture_output=True)
            ten = {p.name for p in Path(t).iterdir()}
            self.assertTrue({"x.song-ngu.ass", "x.vi_VN.srt", "x.en_US.srt", "x.song-ngu.vtt"} <= ten)
            self.assertIn("Arial", (Path(t) / "x.song-ngu.ass").read_text(encoding="utf-8"))


class TestCheckTranslation(unittest.TestCase):
    def setUp(self):
        self.g = check_translation.doc_glossary(SONG_NGU.parent / "references" / "glossary-vi-en.csv")

    def test_bat_thieu_thuat_ngu(self):
        canh = check_translation.check(
            [{"vi": "UBND xã An Thạnh Thủy", "en": "An Thanh Thuy commune"}], self.g)
        self.assertTrue(any("thuật ngữ" in x for x in canh))

    def test_cum_dai_khop_truoc(self):
        canh = check_translation.check(
            [{"vi": "Phó Chủ tịch UBND xã", "en": "Vice Chairwoman of the People's Committee"}], self.g)
        self.assertEqual(canh, [])

    def test_bat_thieu_so_lieu(self):
        canh = check_translation.check([{"vi": "2.500 người", "en": "many people"}], self.g)
        self.assertTrue(any("số liệu" in x for x in canh))

    def test_thang_va_so_viet_chu(self):
        self.assertEqual(check_translation.check(
            [{"vi": "ngày 7 và 8/9/2026", "en": "September 7 and 8, 2026"}], self.g), [])
        self.assertEqual(check_translation.check(
            [{"vi": "trong 2 ngày", "en": "over two days"}], self.g), [])

    def test_bat_chua_dich(self):
        self.assertTrue(any("chưa dịch" in x for x in check_translation.check(
            [{"vi": "Xin chao", "en": "Xin chao"}], self.g)))


class TestLowerThirdScenes(unittest.TestCase):
    def chay(self, rows, cuts):
        with tempfile.TemporaryDirectory() as t:
            j, s = Path(t) / "lt.json", Path(t) / "scenes.json"
            j.write_text(json.dumps(rows), encoding="utf-8")
            s.write_text(json.dumps({"cuts": cuts}), encoding="utf-8")
            return subprocess.run([sys.executable, str(SONG_NGU / "make_lower_thirds_ass.py"), str(j),
                                   str(Path(t) / "o.ass"), "--scenes", str(s)],
                                  capture_output=True, text=True, encoding="utf-8")

    def test_banner_trong_canh_thi_qua(self):
        self.assertEqual(self.chay([{"start": 6, "end": 9, "name": "A"}], [5.0, 20.0]).returncode, 0)

    def test_banner_tran_canh_bi_chan(self):
        r = self.chay([{"start": 3, "end": 7, "name": "B"}], [5.0, 20.0])
        self.assertEqual(r.returncode, 1)
        self.assertIn("tràn", r.stdout + r.stderr)

    def test_khong_de_dong_phu_de_tieng_anh(self):
        """Hop banner phai ket thuc tren dinh dong EN (~876px o 1080p)."""
        with tempfile.TemporaryDirectory() as t:
            j, o = Path(t) / "lt.json", Path(t) / "o.ass"
            j.write_text(json.dumps([{"start": 1, "end": 3, "name": "A", "detail": "B"}]), encoding="utf-8")
            subprocess.run([sys.executable, str(SONG_NGU / "make_lower_thirds_ass.py"), str(j), str(o)],
                           check=True, capture_output=True)
            ys = [int(v) for v in __import__("re").findall(r"\\pos\(\d+,(\d+)\)", o.read_text(encoding="utf-8"))]
            self.assertLess(max(ys), 876, "hop banner cham dong phu de tieng Anh")


class TestIcons(unittest.TestCase):
    def test_moi_icon_ra_svg_va_png(self):
        self.assertGreaterEqual(len(icons.ICONS), 20)
        import xml.etree.ElementTree as ET
        for name in icons.ICONS:
            with self.subTest(icon=name):
                ET.fromstring(icons.to_svg(name))
                self.assertEqual(icons.to_png(name, 32).size, (32, 32))

    def test_svg_da_xuat_ra_assets(self):
        thu_muc = CHUYEN_GIA.parent / "assets" / "broadcast" / "icons"
        co = {p.stem for p in thu_muc.glob("*.svg")}
        self.assertEqual(co, set(icons.ICONS), "assets icon lech voi icons.py — chay lai icons.py")


class TestBroadcastKit(unittest.TestCase):
    def test_moi_component_ra_anh_va_manifest(self):
        kit = broadcast_kit.Kit("national-modern", "16:9")
        goi = [("headline_strap", {"title": "Tieu de", "sub": "phu"}), ("topic_slug", {"text": "Y te"}),
               ("lower_third", {"name": "Ten", "title": "Chuc danh"}),
               ("chip", {"kind": "location", "text": "Xa"}), ("label_chip", {"kind": "ai"}),
               ("status_bar", {"text": "Cap nhat"}), ("source_strap", {"text": "UBND xa"}),
               ("quote_card", {"quote": "Mot cau", "author": "A"}),
               ("fact_card", {"number": "2.500", "label": "nguoi"}),
               ("comparison", {"left": ("A", "1"), "right": ("B", "2")}),
               ("timeline", {"events": [("7/9", "Bat dau"), ("8/9", "Ket thuc")]}),
               ("end_card", {"title": "Cam on", "cta": "Theo doi", "handles": ["@att"]}),
               ("ticker_strip", {"items": ["tin 1", "tin 2"]})]
        for ten, args in goi:
            with self.subTest(component=ten):
                im, meta = getattr(kit, ten)(**args)
                self.assertGreater(im.width, 0)
                self.assertTrue({"x", "y", "w", "h", "fg", "bg", "font_px"} <= set(meta))

    def test_tin_khan_chua_xac_minh_bi_tu_choi(self):
        kit = broadcast_kit.Kit("urgent-alert", "16:9")
        with self.assertRaises(SystemExit):
            kit.breaking_bar("Canh bao")
        im, meta = kit.breaking_bar("Canh bao", verified=True, source="UBND")
        self.assertTrue(meta["verified"])

    def test_chu_tren_nen_nhan_du_tuong_phan(self):
        for ten in ("national-modern", "community-live", "urgent-alert", "newsroom-digital", "editorial-premium"):
            kit = broadcast_kit.Kit(ten, "16:9")
            _, meta = kit.topic_slug("Y te")
            with self.subTest(style=ten):
                self.assertGreaterEqual(validate_graphics.contrast(meta["fg"], meta["bg"]), 4.5)

    def test_demo_moi_phong_cach_va_khung_hinh_deu_dat(self):
        with tempfile.TemporaryDirectory() as t:
            for style in broadcast_kit.STYLES:
                if style.startswith("_") or style == "chung":
                    continue
                for aspect in broadcast_kit.FRAMES:
                    with self.subTest(style=style, aspect=aspect):
                        d = Path(t) / f"{style}_{aspect.replace(':', 'x')}"
                        broadcast_kit.demo(style, aspect, d)
                        man = json.loads((d / "manifest.json").read_text(encoding="utf-8"))
                        loi, _, _ = validate_graphics.validate(man)
                        self.assertEqual(loi, [], f"{style} {aspect}: {loi}")


class TestValidateGraphics(unittest.TestCase):
    def muc(self, **kw):
        goc = {"id": "a", "type": "lower_third", "style": "national-modern", "start": 0, "end": 5,
               "x": 100, "y": 700, "w": 600, "h": 120, "text": "x", "fg": "#FFFFFF", "bg": "#0B2A6B",
               "font_px": 48}
        return {**goc, **kw}

    def kiem(self, items, **kw):
        return validate_graphics.validate({"aspect": "16:9", "items": items}, **kw)[0]

    def test_dat_khi_hop_le(self):
        self.assertEqual(self.kiem([self.muc()]), [])

    def test_bat_ngoai_vung_an_toan(self):
        self.assertTrue(any("an toàn" in x for x in self.kiem([self.muc(x=10)])))

    def test_bat_tuong_phan_thap(self):
        self.assertTrue(any("tương phản" in x for x in self.kiem([self.muc(fg="#111111", bg="#0B2A6B")])))

    def test_bat_chu_qua_nho(self):
        self.assertTrue(any("tối thiểu" in x for x in self.kiem([self.muc(font_px=12)])))

    def test_bat_trung_id_va_de_nhau(self):
        loi = self.kiem([self.muc(), self.muc()])
        self.assertTrue(any("trùng id" in x for x in loi))
        self.assertTrue(any("đè nhau" in x for x in loi))

    def test_bat_che_vung_bao_ve(self):
        self.assertTrue(any("che vùng bảo vệ" in x for x in
                            self.kiem([self.muc()], protect=[(150, 720, 100, 100)])))

    def test_bat_logo_meo_va_tin_khan_chua_xac_minh(self):
        self.assertTrue(any("kéo méo" in x for x in self.kiem([self.muc(src_w=100, src_h=100)])))
        self.assertTrue(any("chưa xác minh" in x for x in self.kiem(
            [self.muc(type="breaking_bar", style="urgent-alert", x=0, y=900, w=1920, h=100)])))

    def test_bat_banner_tran_canh(self):
        self.assertTrue(any("tràn qua mốc cắt" in x for x in self.kiem([self.muc()], cuts=[3.0])))


class TestCallouts(unittest.TestCase):
    def test_hinh_ve_dung_co_khung(self):
        kit = broadcast_kit.Kit("national-modern", "16:9")
        for im in (callouts.arrow(kit.W, kit.H, (10, 10), (200, 200), kit.m["phu"]),
                   callouts.circle_mark(kit.W, kit.H, (500, 500), 80, kit.m["phu"]),
                   callouts.bracket(kit.W, kit.H, (100, 100, 200, 200), kit.m["phu"]),
                   callouts.spotlight(kit.W, kit.H, (500, 500), 120),
                   callouts.pin(kit, (400, 400), 3)):
            self.assertEqual(im.size, (kit.W, kit.H))
        self.assertGreater(callouts.bar_chart(kit, [1, 2], ["a", "b"], "T").width, 0)
        self.assertGreater(callouts.steps_card(kit, ["mot", "hai"], active=0).height, 0)

    def test_sendcmd_bo_diem_mat_dau(self):
        txt = callouts.sendcmd([{"t": 0.0, "x": 1, "y": 2}, {"t": 0.1, "lost": True}])
        self.assertEqual(txt.strip().count("\n"), 0)
        self.assertIn("overlay@co x 1", txt)


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "khong co ffmpeg")
class TestQaTail(unittest.TestCase):
    def clip(self, path: Path, giay: float):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=black:s=64x64:d={giay}",
                        "-f", "lavfi", "-i", f"sine=d={giay}", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-shortest", str(path)], check=True)

    def test_outro_noi_them_can_tail(self):
        with tempfile.TemporaryDirectory() as t:
            src, out = Path(t) / "src.mp4", Path(t) / "out.mp4"
            self.clip(src, 1), self.clip(out, 2)
            lenh = [sys.executable, str(SONG_NGU / "qa.py"), str(out), "--source", str(src)]
            self.assertEqual(subprocess.run(lenh, capture_output=True).returncode, 1)
            self.assertEqual(subprocess.run(lenh + ["--tail", "1"], capture_output=True).returncode, 0)


class TestRenderSpec(unittest.TestCase):
    """Duong chay chinh cua broadcast_kit: spec.json -> chuoi khung + manifest."""

    def test_render_spec_ra_khung_va_manifest_dat(self):
        spec = {"style": "national-modern", "aspect": "16:9", "items": [
            {"id": "lt1", "type": "lower_third", "start": 1.0, "end": 3.0,
             "args": {"name": "Ten", "title": "Chuc danh"}},
            {"id": "tk1", "type": "ticker_strip", "start": 0.0, "end": 1.0,
             "args": {"items": ["tin mot", "tin hai"]}}]}
        with tempfile.TemporaryDirectory() as t:
            out = Path(t) / "gfx"
            man = broadcast_kit.render_spec(spec, out)
            self.assertEqual(len(man), 2)
            self.assertEqual(len(list((out / "lt1").glob("f_*.png"))), 60)   # 2 s x 30 fps
            self.assertEqual(len(list((out / "tk1").glob("f_*.png"))), 30)
            luu = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(validate_graphics.validate(luu)[0], [])

    def test_component_khong_co_thi_bao_loi(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(SystemExit):
                broadcast_kit.render_spec(
                    {"style": "national-modern", "items": [{"id": "x", "type": "khong_co",
                                                            "start": 0, "end": 1}]}, Path(t))

    def test_spec_mau_dung_dinh_dang(self):
        p = CHUYEN_GIA.parent / "assets" / "broadcast" / "spec.example.json"
        spec = json.loads(p.read_text(encoding="utf-8"))
        kit = broadcast_kit.Kit(spec["style"], spec["aspect"])
        for it in spec["items"]:
            with self.subTest(item=it["id"]):
                self.assertTrue(hasattr(kit, it["type"]))
                self.assertLess(it["start"], it["end"])


class TestMotion(unittest.TestCase):
    def khung(self, kieu):
        from PIL import Image
        with tempfile.TemporaryDirectory() as t:
            im = Image.new("RGBA", (200, 50), (255, 0, 0, 255))
            info = broadcast_kit.animate(im, Path(t), 1.0, kieu, .3, .3)
            return info, sorted(Path(t).glob("f_*.png"))

    def test_truot_bu_lai_khoang_dich(self):
        info, files = self.khung("slide")
        self.assertEqual(len(files), 30)
        self.assertEqual(info["dx"], -60)

    def test_mo_dan_va_lo_dan_khong_doi_vi_tri(self):
        for kieu in ("fade", "mask"):
            with self.subTest(kieu=kieu):
                info, files = self.khung(kieu)
                self.assertEqual(info["dx"], 0)
                self.assertEqual(len(files), 30)

    def test_bo_dem_va_ticker(self):
        kit = broadcast_kit.Kit("national-modern", "16:9")
        with tempfile.TemporaryDirectory() as t:
            n = callouts.counter_frames(kit, 2500, "nguoi dan", 1.0, Path(t) / "dem")
            self.assertEqual(n, 30)
            self.assertEqual(len(list((Path(t) / "dem").glob("f_*.png"))), 30)
            strip, _ = kit.ticker_strip(["a", "b"])
            self.assertEqual(broadcast_kit.ticker_frames(strip, kit.W, Path(t) / "tk", 0.5), 15)


class TestMcQaFrames(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, str(CHUYEN_GIA))
        import mc_qa_frames
        self.m = mc_qa_frames

    def test_chon_tu_co_am_moi_khep(self):
        words = [{"s": 1.0, "e": 1.2, "w": "bà"}, {"s": 2.0, "e": 2.2, "w": "phát"},
                 {"s": 3.0, "e": 3.2, "w": "mẹ"}, {"s": 4.0, "e": 4.2, "w": "ăn"}]
        tu = [w for _, w in self.m.pick(words, every=99, limit=99)]
        self.assertIn("bà", tu)
        self.assertIn("mẹ", tu)
        self.assertNotIn("phát", tu, "ph la am /f/, moi khong khep")
        self.assertNotIn("ăn", tu)

    def test_gioi_han_so_khung(self):
        words = [{"s": i * 0.5, "e": i * 0.5 + .2, "w": "ba"} for i in range(50)]
        self.assertLessEqual(len(self.m.pick(words, every=1, limit=12)), 12)


class TestMakeOutroGuard(unittest.TestCase):
    def test_outro_duoi_3_giay_bi_chan(self):
        with tempfile.TemporaryDirectory() as t:
            logo = Path(t) / "logo.png"
            from PIL import Image
            Image.new("RGBA", (268, 78)).save(logo)
            r = subprocess.run([sys.executable, str(SONG_NGU / "make_outro.py"), "--title", "A",
                                "--sub", "B", "--logo", str(logo), "--out-dir", str(Path(t) / "o"),
                                "--seconds", "1"], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(r.returncode, 1)
            self.assertIn("3 giây", r.stdout + r.stderr)


class TestTvCard(unittest.TestCase):
    def test_the_dung_kich_thuoc_khung_tv(self):
        import make_tv_card
        from PIL import Image
        with tempfile.TemporaryDirectory() as t:
            anh = Path(t) / "a.jpg"
            Image.new("RGB", (900, 600), (200, 120, 60)).save(anh)
            card = make_tv_card.make_card(anh, "NHAN", ["Dong mot", "Dong hai"], ["chan"])
            self.assertEqual(card.size, (1000, 394))
            self.assertEqual(make_tv_card.CARD_POS, (900, 240))


class TestRenderAttLopHinh(unittest.TestCase):
    """Thu tu lop: thay-hinh phai nam DUOI logo/icon, khong thi no che mat."""

    def cmd(self, **kw):
        import render_att
        from argparse import Namespace
        with tempfile.TemporaryDirectory() as t:
            goc = dict(input=Path("in.mp4"), captions=None, lower_thirds=None, card=None,
                       card_video=None, card_pos="900,240", extra_logo=None, overlay=[],
                       replace=[], outro_dir=None, bugs_dir=t, preview=False, out=Path("o.mp4"))
            return " ".join(render_att.build_cmd(Namespace(**{**goc, **kw}), 26.0, 100.0, "anull"))

    def test_lop_thay_hinh_nam_duoi_logo_va_icon(self):
        c = self.cmd(replace=["sach.mp4,26.267"])
        self.assertIn("sach.mp4", c)
        self.assertLess(c.index("[rp"), c.index("[ic]"), "thay hinh phai dat truoc icon")
        self.assertLess(c.index("[rp"), c.index("[att]"), "thay hinh phai dat truoc logo ATT")

    def test_overlay_dung_toa_do_va_khung_gio(self):
        c = self.cmd(overlay=["bn.png,46,843,1.5,26.0"])
        self.assertIn("overlay=46:843:enable='between(t,1.5,26.0)'", c)

    def test_khong_co_captions_thi_khong_thua_dau_phay(self):
        self.assertIn("]trim=0:100.0", self.cmd())
        self.assertIn("subtitles=", self.cmd(captions="cap.ass"))

    def test_card_pos_doi_duoc(self):
        self.assertIn("overlay=889:231", self.cmd(card=Path("c.png"), card_pos="889,231"))


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "khong co ffmpeg")
class TestDetectScenes(unittest.TestCase):
    def test_tim_dung_moc_cat_va_studio_end(self):
        import detect_scenes
        with tempfile.TemporaryDirectory() as t:
            v = Path(t) / "v.mp4"
            subprocess.run(["ffmpeg", "-v", "error", "-y",
                            "-f", "lavfi", "-i", "color=c=0x1a3a8a:s=320x180:r=30:d=2",
                            "-f", "lavfi", "-i", "testsrc2=s=320x180:r=30:d=2",
                            "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p[v]",
                            "-map", "[v]", "-c:v", "libx264", "-preset", "ultrafast", str(v)], check=True)
            d = detect_scenes.detect(v)
            self.assertAlmostEqual(d["duration"], 4.0, delta=0.2)
            self.assertIsNotNone(d["studio_end"])
            self.assertAlmostEqual(d["studio_end"], 2.0, delta=0.2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
