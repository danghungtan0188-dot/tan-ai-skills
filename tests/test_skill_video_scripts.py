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
import assemble  # noqa: E402
import build_edit_plan  # noqa: E402
import cut_silence  # noqa: E402
import find_clips  # noqa: E402
import khuon_mau  # noqa: E402
import survey_rushes  # noqa: E402

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


def _shot(sid, t0, t1):
    return {"id": sid, "start": t0, "end": t1, "dur": round(t1 - t0, 2),
            "net": 150.0, "sang": 120.0, "dong": 4.0, "thumb": ""}


RUSHES = {"clips": [
    {"idx": 0, "file": "A.mp4", "name": "A.mp4", "duration": 20.0, "width": 1920, "height": 1080,
     "fps": 30.0, "rotation": 0, "audio": True, "lufs": -26.0,
     "shots": [_shot("0.1", 0.0, 6.0), _shot("0.2", 6.0, 14.0), _shot("0.3", 14.0, 20.0)]},
    {"idx": 1, "file": "B.mp4", "name": "B.mp4", "duration": 30.0, "width": 1920, "height": 1080,
     "fps": 30.0, "rotation": 0, "audio": False, "lufs": None,
     "shots": [_shot("1.1", 0.0, 12.0), _shot("1.2", 12.0, 30.0)]}]}


class TestBuildEditPlan(unittest.TestCase):
    def chay(self, canh, target=20.0):
        bang = build_edit_plan.nap(RUSHES)
        doan, loi = build_edit_plan.dung_doan({"muc": [{"id": "m", "canh": canh}]}, bang)
        loi += build_edit_plan.kiem_luat(doan, bang)
        doan, loi_dai = build_edit_plan.co_gian(doan, target)
        loi += build_edit_plan.kiem_do_dai(doan)
        if loi_dai:
            loi.append(loi_dai)
        return doan, loi

    def ba_doan(self, **kw):
        c = [{"shot": "0.1", "co": "toan", "in": 0.0, "out": 3.0, "ly_do": "toan canh"},
             {"shot": "0.2", "co": "trung", "in": 6.0, "out": 9.0, "ly_do": "trung canh"},
             {"shot": "1.2", "co": "can", "loai": "phat_bieu", "in": 12.0, "out": 22.0, "ly_do": "phat bieu"}]
        for i, v in kw.items():
            c[int(i[-1])].update(v)
        return c

    def test_chan_shot_khong_co_that(self):
        _, loi = self.chay([{"shot": "9.9", "co": "toan", "ly_do": "x"}])
        self.assertTrue(any("khong co trong" in x or "không có trong" in x for x in loi))

    def test_chan_in_out_ra_ngoai_clip(self):
        _, loi = self.chay([{"shot": "0.1", "co": "toan", "in": 0.0, "out": 99.0, "ly_do": "x"}])
        self.assertTrue(any("ra ngoài clip" in x for x in loi))

    def test_chan_broll_trum_qua_moc_cat(self):
        _, loi = self.chay(self.ba_doan(c0={"in": 4.0, "out": 9.0}))
        self.assertTrue(any("trùm qua mốc cắt cảnh" in x for x in loi))

    def test_phat_bieu_duoc_phep_vuot_moc_cat(self):
        _, loi = self.chay(self.ba_doan(c2={"in": 10.0, "out": 20.0}))
        self.assertFalse([x for x in loi if "trùm qua" in x])

    def test_chan_phat_bieu_qua_ngan(self):
        _, loi = self.chay(self.ba_doan(c2={"in": 12.0, "out": 15.0}), target=11.0)
        self.assertTrue(any("câu nói bị cụt" in x for x in loi))

    def test_chan_hai_doan_lien_nhau_cung_clip_cung_co(self):
        _, loi = self.chay(self.ba_doan(c1={"co": "toan"}))
        self.assertTrue(any("nhảy hình" in x for x in loi))

    def test_doan_dau_phai_la_canh_toan(self):
        _, loi = self.chay(self.ba_doan(c0={"co": "can"}))
        self.assertTrue(any("mở đầu phải có cảnh toàn" in x for x in loi))

    def test_chan_loai_go_sai(self):
        _, loi = self.chay(self.ba_doan(c2={"loai": "phatbieu"}))
        self.assertTrue(any("phải là broll/phat_bieu" in x for x in loi))

    def test_thieu_ly_do_bi_chan(self):
        _, loi = self.chay(self.ba_doan(c1={"ly_do": "  "}))
        self.assertTrue(any("thiếu lý do" in x for x in loi))

    def test_co_gian_khop_do_dai_va_khong_dung_phat_bieu(self):
        doan, loi = self.chay(self.ba_doan(), target=20.0)
        self.assertEqual(loi, [])
        self.assertAlmostEqual(sum(d["dur"] for d in doan), 20.0, places=1)
        pb = [d for d in doan if d["loai"] == "phat_bieu"][0]
        self.assertEqual((pb["in"], pb["out"]), (12.0, 22.0), "phat bieu khong duoc co gian")
        self.assertEqual([d["pos"] for d in doan], [0.0, doan[0]["dur"], round(doan[0]["dur"] + doan[1]["dur"], 2)])

    def test_khong_keo_broll_vuot_ranh_gioi_canh(self):
        doan, loi = self.chay(self.ba_doan(), target=60.0)
        self.assertLessEqual(doan[0]["out"], 6.0, "khong duoc keo sang canh sau")
        self.assertLessEqual(doan[1]["out"], 14.0)
        self.assertTrue(any("lệch" in x for x in loi), "phai bao thieu bao nhieu giay")

    def test_bang_duyet_co_du_cot(self):
        doan, _ = self.chay(self.ba_doan())
        bang = build_edit_plan.bang_duyet({"segments": doan, "tong": 20.0, "target": 20.0})
        self.assertIn("phat bieu", bang)
        self.assertIn("Tổng 20.0s / yêu cầu 20.0s", bang)

    def test_tim_clip_de_quy_va_bo_qua_output(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            (root / "ngay-1").mkdir()
            (root / "outputs").mkdir()
            (root / "A.mp4").touch()
            (root / "ngay-1" / "B.MOV").touch()
            (root / "outputs" / "da-dung.mp4").touch()
            found = survey_rushes.tim_clip(root, recursive=True)
            self.assertEqual({p.name for p in found}, {"A.mp4", "B.MOV"})


class TestAssemble(unittest.TestCase):
    PLAN = {"target": 12.0, "tong": 12.0, "segments": [
        {"n": 1, "file": "A.mp4", "in": 0.0, "out": 4.0, "dur": 4.0},
        {"n": 2, "file": "B.mp4", "in": 2.0, "out": 6.0, "dur": 4.0},
        {"n": 3, "file": "A.mp4", "in": 8.0, "out": 12.0, "dur": 4.0}]}

    def cmd(self, **kw):
        from argparse import Namespace
        goc = dict(out=Path("o.mp4"), rushes=None, voice=None, nat_db=-12.0,
                   size="1920x1080", fps=30, preview=False)
        tieng = kw.pop("tieng", {"A.mp4": True, "B.mp4": False})
        gain = kw.pop("gain", {})
        return " ".join(assemble.build_cmd(self.PLAN, Namespace(**{**goc, **kw}), tieng, gain))

    def test_chi_so_input_dung_khi_co_clip_cam(self):
        c = self.cmd()
        self.assertIn("[0:v]scale=1920:1080", c)
        self.assertIn("[3:v]scale=1920:1080", c, "clip cam chen them input, clip sau phai doi chi so")
        self.assertIn("[2:a]aresample=48000[a1]", c, "im lang phai lay tu input anullsrc")
        self.assertIn("anullsrc", c)
        self.assertIn("concat=n=3:v=1:a=1[vc][ac]", c)

    def test_moi_doan_cat_dung_vao_ra(self):
        c = self.cmd()
        self.assertIn("-ss 0.000 -t 4.000 -i A.mp4", c)
        self.assertIn("-ss 8.000 -t 4.000 -i A.mp4", c)

    def test_can_muc_tung_clip_bang_gain_tinh(self):
        c = self.cmd(gain={"A.mp4": 6.0})
        self.assertIn("volume=6.00dB", c)
        self.assertNotIn("compand", c)
        self.assertNotIn("sidechain", c)

    def test_long_tieng_ha_tieng_hien_truong_bang_gain_co_dinh(self):
        c = self.cmd(voice=Path("vo.wav"))
        self.assertIn("[ac]volume=-12.0dB[nat]", c)
        self.assertIn("amix=inputs=2:duration=first:normalize=0[ao]", c)
        self.assertNotIn("sidechaincompress", c, "khong duoc ducking dong")

    def test_gain_clip_gioi_han_va_bo_qua_clip_cam(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "r.json"
            p.write_text(json.dumps(RUSHES), encoding="utf-8")
            g = assemble.gain_clip(p)
        self.assertEqual(g, {"A.mp4": 6.0})


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "khong co ffmpeg")
class TestDungTuVideoTho(unittest.TestCase):
    """Chay that: khao sat clip tho -> chon canh -> ghep -> do lai thoi luong."""

    def tao_clip(self, path, nguon, giay, tieng):
        cmd = ["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", nguon]
        if tieng:
            cmd += ["-f", "lavfi", "-i", f"sine=f=440:d={giay}", "-c:a", "aac"]
        cmd += ["-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", str(path)]
        subprocess.run(cmd, check=True)

    def test_duong_chay_chinh(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            a, b = t / "A.mp4", t / "B.mp4"
            subprocess.run(["ffmpeg", "-v", "error", "-y",
                            "-f", "lavfi", "-i", "color=c=0x1a3a8a:s=320x180:r=30:d=5",
                            "-f", "lavfi", "-i", "testsrc2=s=320x180:r=30:d=5",
                            "-f", "lavfi", "-i", "sine=f=440:d=10",
                            "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p[v]",
                            "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-preset", "ultrafast",
                            "-c:a", "aac", str(a)], check=True)
            self.tao_clip(b, "smptebars=s=320x180:r=30:d=8", 8, False)

            data = survey_rushes.khao_sat([a, b], 0.12, 1.2, t / "thumbs", 4.0)
            ids = [s["id"] for c in data["clips"] for s in c["shots"]]
            self.assertIn("0.1", ids)
            self.assertIn("0.2", ids)
            self.assertIn("1.1", ids)
            self.assertTrue(any("câm" in x for x in data["canh_bao"]))
            survey_rushes.contact_sheet(data, t / "sheet.jpg")
            self.assertTrue((t / "sheet.jpg").exists())
            dai = [s for c in data["clips"] for s in c["shots"] if s["dur"] >= 4.0]
            self.assertTrue(dai, "phai co canh dai de kiem anh phu")
            self.assertEqual(len(dai[0]["them"]), 2, "canh dai phai co them 2 anh dai dien")
            self.assertTrue(all(Path(x).exists() for x in dai[0]["them"]))

            bang = build_edit_plan.nap(data)
            chon = {"muc": [{"id": "m", "canh": [
                {"shot": "0.1", "co": "toan", "in": 0.5, "out": 3.5, "ly_do": "toan canh"},
                {"shot": "1.1", "co": "trung", "in": 0.5, "out": 3.5, "ly_do": "clip cam"},
                {"shot": "0.2", "co": "can", "in": 5.5, "out": 8.5, "ly_do": "can canh"}]}]}
            doan, loi = build_edit_plan.dung_doan(chon, bang)
            loi += build_edit_plan.kiem_luat(doan, bang)
            doan, loi_dai = build_edit_plan.co_gian(doan, 12.0)
            loi += build_edit_plan.kiem_do_dai(doan)
            self.assertEqual((loi, loi_dai), ([], None))

            from argparse import Namespace
            plan = {"target": 12.0, "tong": 12.0, "segments": doan}
            out = t / "rough.mp4"
            ns = Namespace(out=out, rushes=None, voice=None, nat_db=-12.0,
                           size="640x360", fps=30, preview=True)
            tieng = {str(a.resolve()): True, str(b.resolve()): False}
            subprocess.run(assemble.build_cmd(plan, ns, tieng, {}), check=True)
            d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                "-of", "csv=p=0", str(out)], text=True, capture_output=True,
                               check=True).stdout.strip()
            self.assertAlmostEqual(float(d), 12.0, delta=0.3, msg="ghep xong phai dung do dai yeu cau")

            pj = t / "edit-plan.json"
            pj.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
            r = subprocess.run([sys.executable, str(SONG_NGU / "qa.py"), str(out), "--plan", str(pj),
                                "--cut-authorized", "yes"], text=True, capture_output=True,
                               encoding="utf-8", errors="replace")
            self.assertEqual(r.returncode, 0, f"qa --plan phai PASS:\n{r.stdout}\n{r.stderr}")
            self.assertEqual(json.loads(r.stdout)["ke_hoach"]["so_doan"], 3)

            plan_sai = {**plan, "tong": 30.0}
            pj.write_text(json.dumps(plan_sai, ensure_ascii=False), encoding="utf-8")
            r2 = subprocess.run([sys.executable, str(SONG_NGU / "qa.py"), str(out), "--plan", str(pj),
                                 "--cut-authorized", "yes"], text=True, capture_output=True,
                                encoding="utf-8", errors="replace")
            self.assertEqual(r2.returncode, 1, "lech ke hoach phai FAIL")
            self.assertTrue(any("kế hoạch" in e for e in json.loads(r2.stdout)["errors"]))


class TestAssembleTuChoi(unittest.TestCase):
    """Chan chay nham: ke hoach chua duyet, ke hoach con loi, thieu file."""

    def chay(self, plan, extra=()):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "plan.json"
            p.write_text(json.dumps(plan), encoding="utf-8")
            return subprocess.run([sys.executable, str(SONG_NGU / "assemble.py"), str(p),
                                   "--out", str(Path(t) / "o.mp4"), *extra],
                                  text=True, capture_output=True, encoding="utf-8", errors="replace")

    GOC = {"target": 6.0, "tong": 6.0, "cut_authorized": True, "valid": True,
           "segments": [{"n": 1, "file": "khong-co.mp4", "in": 0.0, "out": 6.0, "dur": 6.0}]}

    def test_chua_duyet_thi_khong_cat(self):
        r = self.chay({**self.GOC, "cut_authorized": False})
        self.assertEqual(r.returncode, 1)
        self.assertIn("cut_authorized", r.stderr)

    def test_ke_hoach_con_loi_thi_tu_choi(self):
        r = self.chay({**self.GOC, "valid": False})
        self.assertIn("valid=false", r.stderr)

    def test_ke_hoach_rong_thi_tu_choi(self):
        r = self.chay({**self.GOC, "segments": []})
        self.assertIn("không có đoạn nào", r.stderr)

    def test_thieu_file_voice_bao_truoc_khi_goi_ffmpeg(self):
        r = self.chay(self.GOC, ["--voice", "khong-co.wav"])
        self.assertIn("--voice", r.stderr)

    def test_thieu_clip_thi_bao(self):
        r = self.chay(self.GOC)
        self.assertIn("Không thấy clip", r.stderr)


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "khong co ffmpeg")
class TestAssembleLoiDoc(unittest.TestCase):
    """Loi doc ngan hay dai hon phim deu phai ra dung do dai ke hoach."""

    def dung(self, t, giay_voice):
        v, vo = Path(t) / "v.mp4", Path(t) / f"vo{giay_voice}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y",
                        "-f", "lavfi", "-i", "testsrc2=s=160x90:r=15:d=8",
                        "-f", "lavfi", "-i", "sine=f=200:d=8",
                        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", str(v)], check=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi",
                        "-i", f"sine=f=600:d={giay_voice}", str(vo)], check=True)
        return v, vo

    def do_tieng(self, f):
        r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
                            "stream=duration", "-of", "csv=p=0", str(f)],
                           text=True, capture_output=True, check=True)
        return float(r.stdout.strip())

    def chay(self, giay_voice):
        from argparse import Namespace
        with tempfile.TemporaryDirectory() as t:
            v, vo = self.dung(t, giay_voice)
            out = Path(t) / "o.mp4"
            plan = {"target": 6.0, "tong": 6.0, "segments": [
                {"n": 1, "file": str(v), "in": 0.0, "out": 3.0, "dur": 3.0},
                {"n": 2, "file": str(v), "in": 4.0, "out": 7.0, "dur": 3.0}]}
            ns = Namespace(out=out, rushes=None, voice=vo, nat_db=-12.0,
                           size="160x90", fps=15, preview=True)
            subprocess.run(assemble.build_cmd(plan, ns, {str(v): True}, {}), check=True)
            return self.do_tieng(out), assemble.kiem_dau_ra(out, 6.0, 160, 90, 15)

    def test_loi_doc_ngan_hon_thi_bu_im_lang(self):
        dai, loi = self.chay(2)
        self.assertAlmostEqual(dai, 6.0, delta=0.3, msg="tieng phai dai bang phim")
        self.assertEqual(loi, [])

    def test_loi_doc_dai_hon_thi_cat_bot(self):
        dai, loi = self.chay(12)
        self.assertAlmostEqual(dai, 6.0, delta=0.3, msg="tieng khong duoc dai hon ke hoach")
        self.assertEqual(loi, [])

    def test_kiem_dau_ra_bat_duoc_sai_lech(self):
        from argparse import Namespace
        with tempfile.TemporaryDirectory() as t:
            v, vo = self.dung(t, 2)
            out = Path(t) / "o.mp4"
            plan = {"target": 6.0, "tong": 6.0, "segments": [
                {"n": 1, "file": str(v), "in": 0.0, "out": 6.0, "dur": 6.0}]}
            ns = Namespace(out=out, rushes=None, voice=None, nat_db=-12.0,
                           size="160x90", fps=15, preview=True)
            subprocess.run(assemble.build_cmd(plan, ns, {str(v): True}, {}), check=True)
            loi = assemble.kiem_dau_ra(out, 20.0, 320, 180, 30)
            self.assertTrue(any("thời lượng thật" in x for x in loi))
            self.assertTrue(any("khung" in x for x in loi))
            self.assertTrue(any("fps" in x for x in loi))


ASS_CU = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, Outline, Alignment, MarginV
Style: EN,Arial,42,&H0000E7FF,&H0012263E,2,2,158
Style: VI,Arial,46,&H00FFFFFF,&H0012263E,2,2,100

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
Dialogue: 0,0:00:00.00,0:00:02.00,EN,,0,0,0,,Hello
"""


class TestKhuonMau(unittest.TestCase):
    """Chep kieu chu, logo, tham so tu project cu sang project moi."""

    def khuon(self, t):
        p = Path(t) / "cu.ass"
        p.write_text(ASS_CU, encoding="utf-8")
        lenh = Path(t) / "lenh.txt"
        lenh.write_text('python scripts/render_att.py in.mp4 --card-pos 889,231 '
                        '--extra-logo yte.png --lufs -14 --tp -1.0 --out ra.mp4', encoding="utf-8")
        return khuon_mau.trich([p], lenh, "ATT NEWS")

    def test_trich_doc_dung_style_va_kich_thuoc(self):
        with tempfile.TemporaryDirectory() as t:
            k = self.khuon(t)
        a = k["ass"][0]
        self.assertEqual((a["width"], a["height"]), (1920, 1080))
        self.assertEqual(a["ten_style"], ["EN", "VI"])
        self.assertIn("Arial,42", a["styles"][0])

    def test_trich_nhat_tham_so_tu_lenh_cu(self):
        with tempfile.TemporaryDirectory() as t:
            k = self.khuon(t)
        self.assertEqual(k["lenh"]["--card-pos"], "889,231")
        self.assertEqual(k["lenh"]["--extra-logo"], "yte.png")
        self.assertEqual(k["lenh"]["--lufs"], "-14")
        self.assertNotIn("--out", k["lenh"], "duong dan ra khong phai khuon")

    def test_ap_giu_nguyen_khoi_style_cu(self):
        with tempfile.TemporaryDirectory() as t:
            k = self.khuon(t)
        ass = khuon_mau.ap(k, [{"start": 1.0, "end": 3.0, "vi": "Xin chào", "en": "Hello"}])
        self.assertIn("Style: EN,Arial,42,&H0000E7FF,&H0012263E,2,2,158", ass)
        self.assertIn("Style: VI,Arial,46", ass)
        self.assertIn("PlayResX: 1920", ass)
        self.assertIn("Dialogue: 0,0:00:01.00,0:00:03.00,EN,,0,0,0,,Hello", ass)
        self.assertIn("Dialogue: 1,0:00:01.00,0:00:03.00,VI,,0,0,0,,Xin chào", ass)

    def test_ap_chan_cue_hong(self):
        with tempfile.TemporaryDirectory() as t:
            k = self.khuon(t)
        with self.assertRaises(SystemExit):
            khuon_mau.ap(k, [{"start": 3.0, "end": 1.0, "vi": "a", "en": "b"}])
        with self.assertRaises(SystemExit):
            khuon_mau.ap(k, [{"start": 1.0, "end": 3.0, "vi": "a", "en": ""}])

    def test_lenh_dung_lai_tham_so_cu(self):
        with tempfile.TemporaryDirectory() as t:
            k = self.khuon(t)
        c = " ".join(khuon_mau.lenh_render(k, "moi.mp4", "ra.mp4", ["--scenes", "s.json"]))
        self.assertIn("--card-pos 889,231", c)
        self.assertIn("--lufs -14", c)
        self.assertIn("--scenes s.json", c)
        self.assertTrue(c.endswith("--out ra.mp4"))


class TestKhuonHinh(unittest.TestCase):
    """Toc do, zoom, day khung — luu san trong khuon, goi ten moi ap."""

    K = {"hinh": khuon_mau.HINH_SAN}

    def test_tinh_thi_khong_them_loc_nao(self):
        self.assertEqual(khuon_mau.loc_hinh(khuon_mau.lay_hinh(self.K, "tinh"), 5, 1920, 1080, 30), "")
        self.assertEqual(khuon_mau.loc_tieng(khuon_mau.lay_hinh(self.K, "tinh")), "")

    def test_zoom_sinh_zoompan_tang_dan(self):
        f = khuon_mau.loc_hinh(khuon_mau.lay_hinh(self.K, "zoom_cham"), 5, 1920, 1080, 30)
        self.assertIn("zoompan=", f)
        self.assertIn("on/150", f, "150 khung = 5 giay x 30fps")
        self.assertIn("s=1920x1080", f)

    def test_day_ngang_doi_bieu_thuc_x(self):
        f = khuon_mau.loc_hinh(khuon_mau.lay_hinh(self.K, "day_phai"), 4, 1920, 1080, 25)
        self.assertIn("x='(iw-iw/zoom)*on/100'", f)
        self.assertIn("x='(iw-iw/zoom)*(1-on/100)'",
                      khuon_mau.loc_hinh(khuon_mau.lay_hinh(self.K, "day_trai"), 4, 1920, 1080, 25))

    def test_toc_do_doi_ca_hinh_lan_tieng(self):
        k = khuon_mau.lay_hinh(self.K, "nhanh_12")
        self.assertIn("setpts=PTS/1.2", khuon_mau.loc_hinh(k, 5, 1920, 1080, 30))
        self.assertEqual(khuon_mau.loc_tieng(k), "atempo=1.2")

    def test_chan_ten_la_va_toc_do_ngoai_khoang(self):
        with self.assertRaises(SystemExit):
            khuon_mau.lay_hinh(self.K, "khong-co")
        with self.assertRaises(SystemExit):
            khuon_mau.lay_hinh({"hinh": {"x": {"toc_do": 4.0}}}, "x")

    def test_assemble_lay_them_vat_lieu_khi_tang_toc(self):
        from argparse import Namespace
        plan = {"target": 5.0, "tong": 5.0, "segments": [
            {"n": 1, "file": "A.mp4", "in": 1.0, "out": 6.0, "dur": 5.0, "hinh": "nhanh_12"}]}
        ns = Namespace(out=Path("o.mp4"), rushes=None, voice=None, nat_db=-12.0,
                       size="1920x1080", fps=30, preview=False)
        c = " ".join(assemble.build_cmd(plan, ns, {"A.mp4": True}, {}, self.K))
        self.assertIn("-ss 1.000 -t 6.000 -i A.mp4", c, "5s hinh o toc do 1.2 can 6s nguon")
        self.assertIn("setpts=PTS/1.2", c)
        self.assertIn("atempo=1.2", c)
        self.assertIn("atrim=0:5.000", c, "tieng van phai dai dung 5s")

    def test_plan_co_kieu_hinh_ma_thieu_khuon_thi_bao(self):
        bang = build_edit_plan.nap(RUSHES)
        _, loi = build_edit_plan.dung_doan(
            {"muc": [{"id": "m", "canh": [{"shot": "0.1", "co": "toan", "ly_do": "x",
                                           "hinh": "zoom_cham"}]}]}, bang)
        self.assertTrue(any("chưa đưa --khuon" in x for x in loi))

    def test_tang_toc_thi_vat_lieu_dung_duoc_ngan_lai(self):
        bang = build_edit_plan.nap(RUSHES)
        canh = [{"shot": "0.1", "co": "toan", "in": 0.0, "ly_do": "x", "hinh": "nhanh_12"}]
        doan, _ = build_edit_plan.dung_doan({"muc": [{"id": "m", "canh": canh}]}, bang, self.K)
        self.assertAlmostEqual(doan[0]["_max"], 5.0, places=2, msg="canh 6s o toc do 1.2 chi ra 5s hinh")


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "khong co ffmpeg")
class TestKhuonHinhChayThat(unittest.TestCase):
    def test_zoom_va_tang_toc_van_ra_dung_do_dai(self):
        from argparse import Namespace
        with tempfile.TemporaryDirectory() as t:
            v = Path(t) / "v.mp4"
            subprocess.run(["ffmpeg", "-v", "error", "-y",
                            "-f", "lavfi", "-i", "testsrc2=s=320x180:r=15:d=12",
                            "-f", "lavfi", "-i", "sine=f=300:d=12",
                            "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-shortest", str(v)], check=True)
            out = Path(t) / "o.mp4"
            plan = {"target": 7.0, "tong": 7.0, "segments": [
                {"n": 1, "file": str(v), "in": 0.0, "out": 4.0, "dur": 4.0, "hinh": "zoom_cham"},
                {"n": 2, "file": str(v), "in": 5.0, "out": 8.0, "dur": 3.0, "hinh": "nhanh_12"}]}
            ns = Namespace(out=out, rushes=None, voice=None, nat_db=-12.0,
                           size="320x180", fps=15, preview=True)
            subprocess.run(assemble.build_cmd(plan, ns, {str(v): True}, {},
                                              {"hinh": khuon_mau.HINH_SAN}), check=True)
            self.assertEqual(assemble.kiem_dau_ra(out, 7.0, 320, 180, 15), [],
                             "zoom va tang toc khong duoc lam lech do dai ke hoach")


class TestCutSilence(unittest.TestCase):
    """De xuat bo khoang lang va tu dem — de xuat, khong tu cat."""

    def test_giu_lai_mot_phan_khoang_lang(self):
        c = cut_silence.de_xuat([(10.0, 12.0)], [], 0.4, cut_silence.TU_DEM)
        self.assertEqual((c[0]["start"], c[0]["end"]), (10.2, 11.8), "phai chua lai 0.4s")

    def test_bo_qua_khoang_lang_ngan_hon_muc_giu(self):
        self.assertEqual(cut_silence.de_xuat([(10.0, 10.2)], [], 0.4, cut_silence.TU_DEM), [])

    def test_bat_tu_dem_nhung_bo_qua_tu_dai(self):
        w = [{"s": 1.0, "e": 1.2, "w": "ờ"}, {"s": 2.0, "e": 2.3, "w": "xã"},
             {"s": 3.0, "e": 5.0, "w": "à"}]
        c = cut_silence.de_xuat([], w, 0.4, cut_silence.TU_DEM)
        self.assertEqual(len(c), 1, "chi cat tu dem ngan")
        self.assertIn("từ đệm", c[0]["ly_do"])

    def test_gop_doan_cat_chong_nhau(self):
        c = cut_silence.gop([{"start": 1.0, "end": 3.0, "ly_do": "a"},
                             {"start": 2.0, "end": 4.0, "ly_do": "b"}])
        self.assertEqual(len(c), 1)
        self.assertEqual((c[0]["start"], c[0]["end"]), (1.0, 4.0))

    def test_doan_giu_la_phan_bu(self):
        giu = cut_silence.doan_giu([{"start": 2.0, "end": 3.0}], 10.0)
        self.assertEqual(giu, [(0.0, 2.0), (3.0, 10.0)])

    def test_doi_moc_phu_de_sau_khi_cat(self):
        ax = cut_silence.anh_xa([(0.0, 2.0), (3.0, 10.0)])
        self.assertEqual(cut_silence.doi_moc(1.0, ax), 1.0)
        self.assertEqual(cut_silence.doi_moc(4.0, ax), 3.0, "bo 1s thi moc lui 1s")
        self.assertEqual(cut_silence.doi_moc(2.5, ax), 2.0, "moc roi vao doan cat thi don ve mep")
        self.assertEqual(cut_silence.doi_moc(99.0, ax), 9.0)

    def test_khong_cat_khi_chua_duyet(self):
        with tempfile.TemporaryDirectory() as t:
            v = Path(t) / "v.mp4"
            v.write_bytes(b"0")
            dx = Path(t) / "dx.json"
            dx.write_text(json.dumps({"cat": [{"start": 1.0, "end": 2.0, "ly_do": "x"}]}),
                          encoding="utf-8")
            r = subprocess.run([sys.executable, str(SONG_NGU / "cut_silence.py"), str(v),
                                "--de-xuat", str(dx), "--ap", str(Path(t) / "o.mp4")],
                               text=True, capture_output=True, encoding="utf-8", errors="replace")
        self.assertEqual(r.returncode, 1)
        self.assertIn("--approved", r.stderr)


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "khong co ffmpeg")
class TestCutSilenceChayThat(unittest.TestCase):
    def test_do_duoc_khoang_lang_va_cat_dung(self):
        with tempfile.TemporaryDirectory() as t:
            v = Path(t) / "v.mp4"
            subprocess.run(["ffmpeg", "-v", "error", "-y",
                            "-f", "lavfi", "-i", "color=c=black:s=160x90:r=15:d=6",
                            "-f", "lavfi", "-i",
                            "sine=f=440:d=6,volume=enable='between(t,2,4)':volume=0",
                            "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-shortest", str(v)], check=True)
            lang = cut_silence.do_lang(str(v), -35.0, 1.0)
            self.assertTrue(lang, "phai do duoc khoang lang 2-4s")
            self.assertAlmostEqual(lang[0][0], 2.0, delta=0.3)

            cat = cut_silence.de_xuat(lang, [], 0.35, cut_silence.TU_DEM)
            giu = cut_silence.doan_giu(cat, 6.0)
            out = Path(t) / "gon.mp4"
            subprocess.run(cut_silence.cat_video(str(v), giu, out, True), check=True)
            moi = cut_silence.thoi_luong(str(out))
            bo = sum(c["end"] - c["start"] for c in cat)
            self.assertAlmostEqual(moi, 6.0 - bo, delta=0.3)
            self.assertLess(moi, 6.0, "phai ngan hon ban goc")

            ax = cut_silence.anh_xa(giu)
            self.assertEqual(cut_silence.doi_moc(0.5, ax), 0.5, "phan truoc cho cat giu nguyen moc")
            self.assertLess(cut_silence.doi_moc(5.0, ax), 5.0, "phan sau cho cat phai lui lai")


class TestCuesTuAsr(unittest.TestCase):
    def test_ngat_cue_khi_nguoi_noi_nghi(self):
        w = [{"s": 0.0, "e": 0.3, "w": "Xin"}, {"s": 0.3, "e": 0.6, "w": "chào"},
             {"s": 2.0, "e": 2.3, "w": "Hôm"}, {"s": 2.3, "e": 2.6, "w": "nay"}]
        c = build_bilingual.cues_tu_asr(w)
        self.assertEqual(len(c), 2)
        self.assertEqual(c[0][:3], [0, 1, "Xin chào"])
        self.assertEqual(c[1][3], "", "tieng Anh de trong cho nguoi dich")

    def test_ngat_cue_khi_qua_dai(self):
        w = [{"s": i * 0.3, "e": i * 0.3 + 0.2, "w": "chữ"} for i in range(40)]
        c = build_bilingual.cues_tu_asr(w, max_chars=20)
        self.assertGreater(len(c), 1)
        self.assertTrue(all(len(x[2]) <= 20 for x in c))

    def test_cue_nhap_dung_duoc_voi_build(self):
        w = [{"s": i * 0.5, "e": i * 0.5 + 0.4, "w": f"w{i}"} for i in range(10)]
        c = build_bilingual.cues_tu_asr(w)
        for x in c:
            x[3] = "en"
        d = build_bilingual.build(w, c)
        self.assertTrue(d["meta"]["needs_review"])


class TestFindClips(unittest.TestCase):
    def kho(self, t):
        t = Path(t)
        (t / "Khám sức khỏe 20-09").mkdir(parents=True)
        (t / "outputs").mkdir()
        (t / "le hoi").mkdir()
        for p, n in ((t / "Khám sức khỏe 20-09" / "A.mp4", 3), (t / "le hoi" / "B.MOV", 3),
                     (t / "outputs" / "da_dung.mp4", 3), (t / "le hoi" / "nho.mp4", 0),
                     (t / "le hoi" / "ghi_chu.txt", 3)):
            p.write_bytes(b"0" * (n * 1024 * 1024 + 1))
        return t

    def test_bo_thu_muc_dau_ra_va_duoi_la(self):
        with tempfile.TemporaryDirectory() as t:
            ten = {p.name for p in find_clips.quet(self.kho(t))}
        self.assertEqual(ten, {"A.mp4", "B.MOV", "nho.mp4"}, "phai bo outputs/ va file khong phai video")

    def test_bo_file_qua_nho(self):
        with tempfile.TemporaryDirectory() as t:
            ra = find_clips.loc(find_clips.quet(self.kho(t)), None, None, None, 2.0)
        self.assertEqual({x["name"] for x in ra}, {"A.mp4", "B.MOV"})

    def test_tim_theo_ten_bo_dau_va_khop_ca_thu_muc_cha(self):
        with tempfile.TemporaryDirectory() as t:
            ra = find_clips.loc(find_clips.quet(self.kho(t)), "suc khoe", None, None, 0.0)
        self.assertEqual([x["name"] for x in ra], ["A.mp4"])

    def test_loc_theo_ngay_sua(self):
        with tempfile.TemporaryDirectory() as t:
            files = find_clips.quet(self.kho(t))
            mai = find_clips.ngay("2099-01-01")
            self.assertEqual(find_clips.loc(files, None, mai, None, 0.0), [])
            self.assertTrue(find_clips.loc(files, None, None, mai, 0.0))

    def test_khong_dau(self):
        self.assertEqual(find_clips.khong_dau("Khám Sức Khỏe"), "kham suc khoe")


@unittest.skipUnless(shutil.which("ffmpeg"), "khong co ffmpeg")
class TestKiemTiengTaiMoc(unittest.TestCase):
    def test_bat_duoc_moc_cat_dang_co_tieng(self):
        with tempfile.TemporaryDirectory() as t:
            v = Path(t) / "v.mp4"
            subprocess.run(["ffmpeg", "-v", "error", "-y",
                            "-f", "lavfi", "-i", "color=c=black:s=160x90:r=15:d=4",
                            "-f", "lavfi", "-i", "sine=f=440:d=4",
                            "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", str(v)], check=True)
            doan = [{"n": 1, "shot": "0.1", "file": str(v), "in": 1.0, "out": 3.0}]
            canh = build_edit_plan.kiem_tieng_tai_moc(doan, -30.0)
            self.assertEqual(len(canh), 2, "ca moc vao va moc ra deu dang co tieng")
            self.assertIn("nghe lại", canh[0])
            self.assertEqual(build_edit_plan.kiem_tieng_tai_moc(doan, 0.0), [],
                             "nguong cao thi khong canh bao")


if __name__ == "__main__":
    unittest.main(verbosity=2)
