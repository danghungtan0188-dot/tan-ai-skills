"""Test cho tan_studio: chuẩn hoá, TTS adapter, phụ đề, kiểm tra tự động, workflow, review, quy tắc học được,
chỉ số, dữ liệu, nghiệm thu.

Không cần vieneu/whisper: dùng engine `thu-nghiem` (audio giả). Phần dựng video cần ffmpeg,
không có thì bỏ qua (skip) chứ không báo PASS. Quy tắc phạm vi cá nhân ghi vào thư mục tạm
(TAN_STUDIO_HOME), không đụng ~/.tan-studio thật.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import wave
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tan_studio import (checks, do_hoa, du_lieu, evaluation, long_tieng, metrics, nghiem_thu, normalize,  # noqa: E402
                        read_json, review, rules, subtitles, tts, video, workflow)

try:
    import jsonschema
except ImportError:
    jsonschema = None

SCHEMA = json.loads((REPO_ROOT / "data-contracts" / "studio.schema.json").read_text(encoding="utf-8"))
HAS_FFMPEG = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))
QUIET = dict(log=lambda *_: None)


def validate(instance, name):
    if jsonschema is None:
        return
    jsonschema.validate(instance=instance, schema={"$ref": f"#/$defs/{name}", "$defs": SCHEMA["$defs"]})


class TempHome(unittest.TestCase):
    """Mỗi test có thư mục dự án + TAN_STUDIO_HOME riêng."""

    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.d, True)
        old = os.environ.get("TAN_STUDIO_HOME")
        os.environ["TAN_STUDIO_HOME"] = str(self.d / "home")
        self.addCleanup(lambda: os.environ.__setitem__("TAN_STUDIO_HOME", old) if old
                        else os.environ.pop("TAN_STUDIO_HOME", None))

    def project(self, script="Ngày 2/9/2026 xã họp.\n\nNgười dân cài đặt VNeID.", **extra) -> Path:
        (self.d / "kich-ban.txt").write_text(script, encoding="utf-8")
        cfg = {"ten": "thu", "kich_ban": "kich-ban.txt", "ti_le": "9:16", "tts": {"engine": "thu-nghiem"}, **extra}
        (self.d / "du-an.json").write_text(json.dumps(cfg), encoding="utf-8")
        return self.d / "du-an.json"


# ---------------- chuẩn hoá ----------------

class TestChuanHoa(unittest.TestCase):
    def test_giu_ban_goc_va_ghi_vet(self):
        r = normalize.normalize_text("UBND họp lúc 7h30, chi 50.000đ.")
        self.assertEqual(r["original"], "UBND họp lúc 7h30, chi 50.000đ.")
        self.assertEqual(r["normalized"], "Ủy ban nhân dân họp lúc bảy giờ ba mươi phút, chi năm mươi nghìn đồng.")
        self.assertEqual([c["quy_tac"] for c in r["changes"]], ["viet_tat", "gio", "tien_te", "so"])
        self.assertTrue(all(c["ly_do"] for c in r["changes"]))

    def test_tat_quy_tac(self):
        r = normalize.normalize_text("lúc 7h30", tat_quy_tac=["gio"])
        self.assertIn("7h30", r["normalized"])  # số dính chữ -> không đoán
        with self.assertRaises(ValueError):
            normalize.normalize_text("x", tat_quy_tac=["khong-co"])

    def test_unicode_va_dau_cau(self):
        r = normalize.normalize_text("An Thạnh Thủy ,  vui…")
        self.assertEqual(r["normalized"], "An Thạnh Thủy, vui...")

    def test_mo_ho_thi_gan_co_khong_doan(self):
        r = normalize.normalize_text("tăng 2.5 lần, theo 1402/QĐ về VNeID")
        self.assertIn("2.5", r["normalized"])
        flagged = {f["doan"] for f in r["flags"] if f["loai"] == "can_xem_lai"}
        self.assertTrue({"2.5", "VNeID", "QĐ"} <= flagged, flagged)

    def test_tu_kho_tts_chi_gan_co(self):
        r = normalize.normalize_text("Đảng ủy xã")
        self.assertEqual(r["normalized"], "Đảng ủy xã")
        self.assertIn("ủy", {f["doan"] for f in r["flags"] if f["loai"] == "tu_kho_tts"})

    def test_quy_tac_phat_am_chay_truoc_va_ghi_phien_ban(self):
        entry = {"tu": "VNeID", "doc_thanh": "vê en e i đê", "id": "qt-x", "phien_ban": 3, "pham_vi": "du_an"}
        r = normalize.normalize_text("cài VNeID", phat_am=[entry])
        self.assertEqual(r["normalized"], "cài vê en e i đê")
        self.assertIn("qt-x v3", r["changes"][0]["ly_do"])

    def test_script_nhieu_doan_khop_schema(self):
        data = normalize.normalize_script("Đoạn 1 ngày 2/9/2026.\n\nĐoạn 2.")
        self.assertEqual(data["original_text"], "Đoạn 1 ngày 2/9/2026.\n\nĐoạn 2.")
        validate(data, "NormalizedScript")


# ---------------- TTS + phụ đề ----------------

class TestTTS(unittest.TestCase):
    def test_engine_khong_co(self):
        with self.assertRaises(tts.EngineError):
            tts.get_engine("khong-co")

    def test_khong_ho_tro_doi_toc_do(self):
        with self.assertRaises(tts.EngineError):
            tts.synthesize({"segments": []}, Path(tempfile.mkdtemp()), "thu-nghiem", speed=1.2)

    def test_vieneu_bao_ro_khi_thieu_thu_vien(self):
        eng = tts.VieneuEngine()
        orig = tts.importlib.util.find_spec
        tts.importlib.util.find_spec = lambda name: None
        try:
            self.assertIn("chưa cài", eng.check())
            with self.assertRaises(tts.EngineError):
                eng.open("nam", "tin_tuc")
        finally:
            tts.importlib.util.find_spec = orig

    def test_the_nghi_tach_doan_va_dat_khoang_lang(self):
        data = normalize.normalize_script("Phần một. [nghỉ 2s] Phần hai. [Nghỉ 500 ms]\n\nPhần ba.")
        segs = data["segments"]
        self.assertEqual([s["original"] for s in segs], ["Phần một.", "Phần hai.", "Phần ba."])
        self.assertNotIn("nghi_truoc_ms", segs[0])
        self.assertEqual([s.get("nghi_truoc_ms") for s in segs[1:]], [2000, 500])
        self.assertEqual(normalize.split_pauses("[nghỉ 30s] A"), [(10_000, "A")])  # tối đa 10 giây
        self.assertFalse([f for f in checks.check_script(data, checks.thresholds(None))
                          if f["ma"] == "con_danh_dau"])  # thẻ nghỉ không bị coi là chỗ đánh dấu sót
        with tempfile.TemporaryDirectory() as d:
            res = tts.synthesize(data, Path(d), "thu-nghiem", gap_ms=450)
            s1, s2, s3 = res["segments"]
            self.assertAlmostEqual(s2["start"] - s1["end"], 2.0, places=2)
            self.assertAlmostEqual(s3["start"] - s2["end"], 0.5, places=2)

    def test_ghep_doan_va_moc_thoi_gian(self):
        with tempfile.TemporaryDirectory() as d:
            data = normalize.normalize_script("một hai ba bốn năm.\n\nsáu bảy.")
            res = tts.synthesize(data, Path(d), "thu-nghiem", gap_ms=500)
            s1, s2 = res["segments"]
            self.assertAlmostEqual(s2["start"] - s1["end"], 0.5, places=2)
            with wave.open(res["audio"]) as w:
                self.assertAlmostEqual(w.getnframes() / w.getframerate(), s2["end"], places=2)
            mtime = Path(s1["wav"]).stat().st_mtime
            tts.synthesize(data, Path(d), "thu-nghiem", gap_ms=500)
            self.assertEqual(Path(s1["wav"]).stat().st_mtime, mtime)  # đoạn đã có thì không đọc lại


class TestLongTieng(unittest.TestCase):
    def test_lan_khoang_lang_roi_doc_nhanh_roi_lui(self):
        cues = [{"so": 1, "start": 0.0, "end": 2.0, "text": "a"}, {"so": 2, "start": 3.0, "end": 5.0, "text": "b"}]
        p = long_tieng.place(cues, [2.5, 1.0], 1.15)
        self.assertEqual((p[0]["toc_do"], p[0]["end"], p[1]["lui_s"]), (1.0, 2.5, 0.0))  # lấn khoảng lặng
        cues[1]["start"] = 2.2
        p = long_tieng.place(cues, [2.42, 1.0], 1.15)
        self.assertAlmostEqual(p[0]["toc_do"], 1.1, places=3)  # đọc nhanh vừa đủ, không lùi
        self.assertEqual(p[1]["lui_s"], 0.0)
        cues[1]["start"] = 1.0
        p = long_tieng.place(cues, [2.0, 1.0], 1.15)
        self.assertEqual(p[0]["toc_do"], 1.15)  # chạm trần tốc độ
        self.assertAlmostEqual(p[1]["start"], 2.0 / 1.15 + long_tieng.GAP_S, places=3)  # câu sau bị lùi
        self.assertGreater(p[1]["lui_s"], 0)

    @unittest.skipUnless(HAS_FFMPEG, "cần ffmpeg")
    def test_long_tieng_tu_srt(self):
        with tempfile.TemporaryDirectory() as d:
            srt = Path(d) / "phim.srt"
            srt.write_text("1\n00:00:00,000 --> 00:00:01,000\n{\\an8}<i>một hai ba bốn năm sáu bảy tám</i>\n\n"
                           "2\n00:00:01,200 --> 00:00:03,000\nchín mười\n", encoding="utf-8")
            res = long_tieng.dub(srt, Path(d) / "out", "thu-nghiem", max_speed=1.15)
            c1, c2 = res["cau"]
            self.assertEqual(c1["text"], "một hai ba bốn năm sáu bảy tám")  # bỏ thẻ định dạng
            self.assertEqual(c1["toc_do"], 1.15)
            self.assertGreater(c2["lui_s"], 0)
            self.assertTrue(Path(res["phu_de_da_chinh"]).exists())
            self.assertGreaterEqual(tts.wav_duration(Path(res["audio"])), c2["end"] - 0.01)
            cues = subtitles.read_srt(Path(res["phu_de_da_chinh"]))
            self.assertAlmostEqual(cues[1]["start"], c2["start"], places=2)
            self.assertAlmostEqual(cues[0]["end"], c1["end"], places=2)  # câu 1 đọc lấn: chữ hiện tới khi đọc xong
            mtime = Path(d, "out", "cau").stat().st_mtime
            long_tieng.dub(srt, Path(d) / "out", "thu-nghiem", max_speed=1.15)
            self.assertEqual(Path(d, "out", "cau").stat().st_mtime, mtime)  # câu đã có thì không đọc lại

    def test_toc_do_ngoai_khoang_bi_tu_choi(self):
        with self.assertRaises(tts.EngineError):
            long_tieng.dub(Path("x.srt"), Path("."), "thu-nghiem", max_speed=2.0)


class TestPhuDe(unittest.TestCase):
    def test_cat_cue_khong_qua_dai(self):
        text = "Sáng ngày 22-5-2026, UBND xã An Thạnh Thủy tổ chức hội nghị sơ kết công tác 6 tháng đầu năm."
        for line in subtitles.LINE.values():
            for cue in subtitles.split_cues(text, 2 * line - 4):
                self.assertLessEqual(len(cue), 2 * line - 4, cue)

    def test_phu_de_dung_chu_goc_va_qua_kiem_tra(self):
        segs = [{"index": 1, "original": "Họp ngày 2/9/2026. Kết thúc lúc 11h30.", "normalized": "..."}]
        cues = subtitles.cues_from_tts(segs, [{"index": 1, "start": 0.0, "end": 6.0}])
        self.assertEqual([c["vi"] for c in cues], ["Họp ngày 2/9/2026.", "Kết thúc lúc 11h30."])
        with tempfile.TemporaryDirectory() as d:
            p = subtitles.write_srt(cues, Path(d) / "a.srt")
            self.assertEqual(subtitles.validate(p)[0], [])


# ---------------- kiểm tra tự động ----------------

def write_tone(path: Path, seconds: float, amp: float = 0.05, sr: int = 16000, silence_at=None):
    import math
    import struct
    frames = []
    for i in range(int(seconds * sr)):
        t = i / sr
        quiet = silence_at and silence_at[0] <= t < silence_at[1]
        frames.append(struct.pack("<h", 0 if quiet else int(32767 * amp * math.sin(2 * math.pi * 220 * t))))
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(b"".join(frames))


class TestKiemTra(unittest.TestCase):
    def setUp(self):
        self.t = checks.thresholds(None)
        self.d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.d, True)

    def test_script_rong_va_danh_dau_la_loi(self):
        norm = normalize.normalize_script("Tin [CHÈN TÊN] hôm nay.\n\nTODO")
        found = checks.check_script(norm, self.t)
        self.assertIn("con_danh_dau", {f["ma"] for f in found if f["muc_do"] == "loi"})
        f = next(f for f in found if f["ma"] == "con_danh_dau")
        self.assertEqual(f["vi_tri"]["doan"], 1)
        self.assertTrue(f["ly_do"] and f["goi_y"])
        validate(f, "Finding")

    def test_toc_do_doc_bat_thuong_co_thoi_diem(self):
        wav = self.d / "a.wav"
        write_tone(wav, 6.0)  # 4 từ trong 6 giây = 0,7 từ/giây
        found = checks.check_audio({"segments": [{"index": 2, "wav": str(wav), "start": 10.0,
                                                  "text": "một hai ba bốn"}]}, wav, self.t)
        f = next(f for f in found if f["ma"] == "toc_do_doc")
        self.assertEqual((f["vi_tri"]["doan"], f["vi_tri"]["thoi_diem"]), (2, 10.0))

    def test_lang_giua_doan_va_im_lang(self):
        wav, mute = self.d / "a.wav", self.d / "b.wav"
        write_tone(wav, 5.0, silence_at=(2.0, 4.0))
        write_tone(mute, 2.0, amp=0.0)
        found = checks.check_audio({"segments": [
            {"index": 1, "wav": str(wav), "start": 0.0, "text": " ".join(["chữ"] * 20)},
            {"index": 2, "wav": str(mute), "start": 6.0, "text": "a b c"}]}, wav, self.t)
        gap = next(f for f in found if f["ma"] == "lang_bat_thuong")
        self.assertAlmostEqual(gap["vi_tri"]["thoi_diem"], 2.0, delta=0.1)
        self.assertIn("im_lang", {f["ma"] for f in found if f["muc_do"] == "loi"})

    def test_nguong_cau_hinh_duoc(self):
        wav = self.d / "a.wav"
        write_tone(wav, 6.0)
        seg = {"segments": [{"index": 1, "wav": str(wav), "start": 0.0, "text": "một hai ba bốn"}]}
        loose = checks.thresholds({"toc_do_doc": {"min": 0.1}})
        self.assertEqual(loose["toc_do_doc"]["max"], self.t["toc_do_doc"]["max"])
        self.assertNotIn("toc_do_doc", {f["ma"] for f in checks.check_audio(seg, wav, loose)})

    def test_phu_de_dai_hon_giong_la_loi(self):
        srt = subtitles.write_srt([{"start": 0.0, "end": 9.0, "vi": "xin chào"}], self.d / "a.srt")
        found = checks.check_subs(srt, 3.0, 42, self.t)
        self.assertIn("phu_de_qua_dai", {f["ma"] for f in found if f["muc_do"] == "loi"})

    def test_dau_van_tay_on_dinh_giua_cac_lan(self):
        a = checks.finding("phu_de", "canh_bao", "phu_de", "x", "y", key="3:đọc quá nhanh # ký tự")
        b = checks.finding("phu_de", "canh_bao", "phu_de", "x khác", "y", key="3:đọc quá nhanh # ký tự")
        self.assertEqual(a["dau_van_tay"], b["dau_van_tay"])
        self.assertEqual(checks.finding("can_xem_lai", "canh_bao", "chuan_hoa", "x", "y", tu="VNeID")["dau_van_tay"],
                         "tu:VNeID")


# ---------------- workflow ----------------

class TestDoHoa(TempHome):
    def test_doi_ten_khoa_va_kiem_cau_hinh(self):
        self.assertEqual(do_hoa.camel({"tieu_de": "a", "cot": [{"gia_tri": 1}]}), {"tieuDe": "a", "cot": [{"giaTri": 1}]})
        self.assertEqual(do_hoa.check_config({"intro": {"tieu_de": "a"}}), [])
        errs = do_hoa.check_config({"logo": {}, "lower_third": [{"ten": "A"}]})
        self.assertTrue(any("logo" in e for e in errs) and any("tai" in e for e in errs))
        with self.assertRaises(workflow.ProjectError):
            workflow.load_project(self.project(do_hoa={"lower_third": [{"ten": "A"}]}))
        with self.assertRaises(do_hoa.DoHoaError):
            do_hoa.comp_id("khong-co")

    def test_dap_do_hoa_duoi_phu_de(self):
        cmd = video.build_cmd(Path("a.wav"), Path("p.ass"), [], Path("o.mp4"), "16:9", 10.0, "anull",
                              overlays=[{"mau": "LowerThird", "tep": "lt.mov", "tai": 2.0, "thoi_luong": 3.0}])
        graph = cmd[cmd.index("-filter_complex") + 1]
        self.assertIn("lt.mov", cmd)
        self.assertIn("setpts=PTS-STARTPTS+2.000/TB", graph)
        self.assertIn("enable='between(t,2.000,5.000)'", graph)
        self.assertLess(graph.index("overlay="), graph.index("ass="))  # phụ đề nằm trên đồ hoạ

    @unittest.skipUnless(HAS_FFMPEG and do_hoa.check() is None, "cần ffmpeg + do-hoa/node_modules (cd do-hoa && npm i)")
    def test_lower_third_that_vao_video(self):
        r = workflow.run(self.project(do_hoa={"lower_third": [{"tai": 0.5, "ten": "Bà Trần Thị B", "thoi_luong": 1.5}]}),
                         **QUIET)
        st = {s["name"]: s for s in r["steps"]}
        self.assertEqual(st["dung_video"]["status"], "DONE", st["dung_video"].get("error"))
        self.assertEqual(st["dung_video"]["timeline"]["do_hoa"][0]["mau"], "LowerThird")
        clip = next(Path(r["run_dir"], "do-hoa").glob("LowerThird_*.mov"))
        probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=pix_fmt",
                                "-of", "csv=p=0", str(clip)], capture_output=True, text=True).stdout
        self.assertTrue(probe.startswith("yuva"), probe)  # có kênh trong suốt
        props = read_json(clip.with_name(clip.stem + ".props.json"))
        self.assertEqual(props["chucVu"], "")  # không lọt dữ liệu mẫu của Studio
        self.assertEqual(st["kiem_tra"]["qa_ky_thuat"], "PASS")


class TestWorkflow(TempHome):
    def test_du_an_thieu_file_bao_loi_ro(self):
        p = self.project(media=["khong-co.jpg"])
        with self.assertRaises(workflow.ProjectError) as ctx:
            workflow.load_project(p)
        self.assertIn("khong-co.jpg", str(ctx.exception))

    def test_buoc_loi_thi_buoc_sau_not_run(self):
        r = workflow.run(self.project(tts={"engine": "thu-nghiem", "toc_do": 1.3}), **QUIET)
        st = {s["name"]: s["status"] for s in r["steps"]}
        self.assertEqual((st["chuan_hoa"], st["giong_doc"], st["phu_de"]), ("DONE", "FAILED", "NOT_RUN"))
        self.assertEqual(r["status"], "FAILED")
        validate(r, "RunReport")

    def test_ho_so_lan_chay(self):
        r = workflow.run(self.project(), ["chuan_hoa"], **QUIET)
        self.assertEqual(r["status"], "INCOMPLETE")
        self.assertEqual(r["noi_dung"], "chua_danh_gia")
        self.assertEqual(len(r["inputs"]["kich_ban"]["sha256"]), 64)
        self.assertIn("normalize_vi.py", r["versions"]["tep_skill"])
        self.assertIn("duration_s", r["steps"][0])
        self.assertEqual(r["config_hash"], workflow.run(self.project(), ["chuan_hoa"], **QUIET)["config_hash"])
        validate(r, "RunReport")

    def test_loi_chan_xuat_video(self):
        r = workflow.run(self.project(script="Tin [CHÈN TÊN]."), **QUIET)
        st = {s["name"]: s for s in r["steps"]}
        self.assertEqual(st["kiem_truoc"]["status"], "FAILED")
        self.assertIn("chặn xuất", st["kiem_truoc"]["error"])
        self.assertEqual(st["dung_video"]["status"], "NOT_RUN")

    def test_tat_luu_van_ban(self):
        r = workflow.run(self.project(ho_so={"luu_van_ban": False}), ["chuan_hoa", "giong_doc"], **QUIET)
        run_dir = Path(r["run_dir"])
        blob = "".join(f.read_text(encoding="utf-8") for f in run_dir.rglob("*.json"))
        self.assertNotIn("Người dân", blob)
        self.assertFalse((run_dir / "chuan-hoa.txt").exists())
        with self.assertRaises(workflow.ProjectError):
            workflow.run(self.d / "du-an.json", ["phu_de"], r["run_id"], **QUIET)

    @unittest.skipUnless(HAS_FFMPEG, "cần ffmpeg/ffprobe")
    def test_chay_tron_xem_truoc_chay_lai(self):
        p = self.project()
        r = workflow.run(p, **QUIET)
        self.assertEqual(r["status"], "DONE_WITH_WARNINGS", json.dumps(r, ensure_ascii=False)[:1500])
        run_dir = Path(r["run_dir"])
        self.assertTrue((run_dir / "thu.mp4").exists())
        steps = {s["name"]: s for s in r["steps"]}
        self.assertEqual(steps["kiem_tra"]["qa_ky_thuat"], "PASS")
        self.assertEqual(steps["dung_video"]["timeline"]["khung"], "1080x1920")
        self.assertIn("CHƯA ĐÁNH GIÁ", (run_dir / "bao-cao.md").read_text(encoding="utf-8"))
        validate(read_json(run_dir / "run.json"), "RunReport")
        for f in read_json(run_dir / "phat-hien.json")["phat_hien"]:
            validate(f, "Finding")
        # sửa tay SRT rồi chỉ dựng lại video
        srt = run_dir / "phu-de.srt"
        srt.write_text(srt.read_text(encoding="utf-8").replace("Người dân", "NGƯỜI DÂN"), encoding="utf-8")
        workflow.run(p, ["dung_video"], r["run_id"], **QUIET)
        self.assertIn("NGƯỜI DÂN", (run_dir / "thu.ass").read_text(encoding="utf-8"))
        # xem trước: nửa độ phân giải
        pv = workflow.run(p, xem_truoc=True, **QUIET)
        self.assertEqual({s["name"]: s for s in pv["steps"]}["dung_video"]["timeline"]["khung"], "540x960")
        # chạy lại đúng cấu hình
        again = workflow.rerun(p, r["run_id"], **QUIET)
        self.assertEqual(again["chay_lai_tu"], r["run_id"])
        self.assertEqual(again["config_hash"], r["config_hash"])
        self.assertTrue(metrics.compare(p, r["run_id"], again["run_id"])["phat_hien_con"])


# ---------------- review + quy tắc + luồng học ----------------

class TestHocCoKiemSoat(TempHome):
    def test_tu_choi_thong_tin_ca_nhan(self):
        p = self.project()
        cfg = workflow.load_project(p)
        for text in ("gọi 0909123456", "mail a@b.com"):
            with self.assertRaises(review.ReviewError):
                review.add_observation(cfg["_dir"], cfg, None, "script", text)

    def test_mau_thuan_khong_tu_chon(self):
        p = self.project()
        cfg = workflow.load_project(p)
        run_dir = Path(workflow.run(p, ["chuan_hoa"], **QUIET)["run_dir"])
        o1 = review.add_observation(cfg["_dir"], cfg, run_dir, "phat_am", "a", tu="VNeID", doc_dung="vi en i ai đi")
        o2 = review.add_observation(cfg["_dir"], cfg, run_dir, "phat_am", "b", tu="VNeID", doc_dung="vê nê ai đi")
        r2 = rules._find(cfg["_dir"], o2["quy_tac"])[2]
        self.assertEqual(r2["trang_thai"], "mau_thuan")
        self.assertIn(o1["quy_tac"], r2["mau_thuan_voi"])
        rules.approve(cfg["_dir"], o1["quy_tac"], "du_an")
        with self.assertRaises(rules.RuleError):  # cùng phạm vi dự án đã có quy tắc khác cho VNeID
            rules.approve(cfg["_dir"], o2["quy_tac"], "du_an")
        with self.assertRaises(rules.RuleError):  # không đẩy mâu thuẫn lên hệ thống
            rules.approve(cfg["_dir"], o2["quy_tac"], "he_thong")

    def test_trung_lap_duoc_lien_ket(self):
        p = self.project()
        cfg = workflow.load_project(p)
        run_dir = Path(workflow.run(p, ["chuan_hoa"], **QUIET)["run_dir"])
        a = review.add_observation(cfg["_dir"], cfg, run_dir, "phat_am", "x", tu="VNeID", doc_dung="vi en i ai đi")
        b = review.add_observation(cfg["_dir"], cfg, run_dir, "phat_am", "y", tu="VNeID", doc_dung="vi en i ai đi")
        self.assertEqual(b["trung_voi"], a["id"])
        self.assertEqual(a["quy_tac"], b["quy_tac"])  # không sinh đề xuất thứ hai
        self.assertEqual(len([r for _, r in rules.all_rules(cfg["_dir"])]), 1)

    def test_pham_vi_ca_nhan_va_hoan_tac(self):
        p = self.project()
        cfg = workflow.load_project(p)
        run_dir = Path(workflow.run(p, ["chuan_hoa"], **QUIET)["run_dir"])
        o = review.add_observation(cfg["_dir"], cfg, run_dir, "phat_am", "x", tu="VNeID", doc_dung="vi en i ai đi")
        rules.approve(cfg["_dir"], o["quy_tac"], "ca_nhan")
        home_file = self.d / "home" / "quy-tac.json"
        self.assertEqual(read_json(home_file)["quy_tac"][0]["id"], o["quy_tac"])
        self.assertTrue(any(e["id"] == o["quy_tac"] for e in rules.active_pronunciations(None)))
        r = rules.undo(cfg["_dir"], o["quy_tac"])  # hoàn tác duyệt -> về lại đề xuất trong dự án
        self.assertEqual((r["trang_thai"], r["pham_vi"], r["bat"]), ("de_xuat", "du_an", False))
        self.assertEqual(read_json(home_file)["quy_tac"], [])
        validate(r, "Rule")

    def test_quy_tac_he_thong_trong_repo_deu_qua_hoi_quy(self):
        for r in rules.regression(None):
            with self.subTest(rule=r["id"]):
                self.assertTrue(r["ok"], r)
        for r in read_json(rules.SYSTEM_FILE)["quy_tac"]:
            validate(r, "Rule")

    @unittest.skipUnless(HAS_FFMPEG, "cần ffmpeg/ffprobe")
    def test_luong_hoc_day_du(self):
        """Tiêu chí G.8: chạy → phát hiện có vị trí → đánh dấu → đề xuất (chưa áp dụng) → duyệt + kiểm thử
        → chạy lại hết lỗi → lịch sử lỗi cho thấy lỗi giảm."""
        p = self.project()
        cfg = workflow.load_project(p)
        r1 = workflow.run(p, **QUIET)
        d1 = Path(r1["run_dir"])
        f = next(f for f in read_json(d1 / "phat-hien.json")["phat_hien"] if f["dau_van_tay"] == "tu:VNeID")
        self.assertEqual(f["vi_tri"]["doan"], 2)
        review.finding_verdict(cfg["_dir"], cfg, d1, f["id"], True)
        obs = review.add_observation(cfg["_dir"], cfg, d1, "phat_am", "đánh vần khó nghe", tu="VNeID",
                                     doc_dung="vi en i ai đi", doan=2, uu_tien="cao")
        validate(obs, "Observation")
        proposal = rules._find(cfg["_dir"], obs["quy_tac"])[2]
        self.assertEqual((proposal["trang_thai"], proposal["bat"]), ("de_xuat", False))
        self.assertEqual(proposal["vi_du"]["truoc"], "Người dân cài đặt VNeID.")
        r2 = workflow.run(p, **QUIET)
        self.assertIn("VNeID", (Path(r2["run_dir"]) / "chuan-hoa.txt").read_text(encoding="utf-8"))
        trial = rules.trial(cfg["_dir"], obs["quy_tac"], rules.history_samples(cfg["_dir"]))
        self.assertFalse(trial["xau_di"])
        self.assertTrue(trial["tot_len"])
        rule = rules.approve(cfg["_dir"], obs["quy_tac"], "du_an")
        self.assertEqual(rule["kiem_thu"][0]["ky_vong"], "vi en i ai đi")
        self.assertTrue(all(x["ok"] for x in rules.regression(cfg["_dir"])))
        r3 = workflow.run(p, **QUIET)
        d3 = Path(r3["run_dir"])
        self.assertIn("vi en i ai đi", (d3 / "chuan-hoa.txt").read_text(encoding="utf-8"))
        self.assertEqual(r3["versions"]["quy_tac_ap_dung"][0]["id"], rule["id"])
        review.verdict(cfg["_dir"], d3, "chap_nhan")
        workflow.set_content_verdict(d3, "chap_nhan")
        hist = metrics.error_history(p, "VNeID")
        self.assertEqual(hist["dong"][0]["lan_chay"], ["X", "X", "."])
        m = metrics.project_metrics(p)["tat_ca"]
        self.assertEqual(m["so_lan_sua_truoc_khi_duyet"]["danh_sach"], [2])
        self.assertEqual(m["chap_nhan_ngay_lan_dau"]["ket_luan"], "chưa đủ dữ liệu")
        self.assertEqual(m["canh_bao_tu_dong_dung"]["tu_so"], 1)
        cmp = metrics.compare(p, r1["run_id"], r3["run_id"])
        self.assertIn("tu:VNeID", cmp["phat_hien_da_het"])


# ---------------- dữ liệu ----------------

class TestDuLieu(TempHome):
    def test_xem_xuat_xoa(self):
        p = self.project()
        r1 = workflow.run(p, ["chuan_hoa", "giong_doc"], **QUIET)
        workflow.run(p, ["chuan_hoa", "giong_doc"], **QUIET)
        cfg = workflow.load_project(p)
        review.add_observation(cfg["_dir"], cfg, Path(r1["run_dir"]), "script", "lỗi thử")
        self.assertEqual(len(du_lieu.overview(p)["lan_chay"]), 2)
        z = du_lieu.export(p, self.d / "x.zip")
        import zipfile
        self.assertFalse(any(n.endswith(".wav") for n in zipfile.ZipFile(z).namelist()))
        plan = du_lieu.cleanup(p, keep=1, sure=False)
        self.assertEqual(plan["lan_chay"], [r1["run_id"]])
        self.assertTrue(any(Path(r1["run_dir"]).rglob("*.wav")))  # chưa --chac-chan thì chưa xoá
        du_lieu.cleanup(p, keep=1, sure=True)
        self.assertFalse(any(Path(r1["run_dir"]).rglob("*.wav")))
        self.assertTrue((Path(r1["run_dir"]) / "run.json").exists())
        du_lieu.delete_run(p, r1["run_id"], sure=True)
        self.assertFalse(Path(r1["run_dir"]).exists())
        self.assertEqual(review.observations(cfg["_dir"]), [])
        self.assertTrue((self.d / "kich-ban.txt").exists())  # không đụng tư liệu gốc


# ---------------- đánh giá TTS + nghiệm thu ----------------

class TestDanhGiaTTS(unittest.TestCase):
    def test_bo_cau_hop_le(self):
        doc = read_json(evaluation.CASES_FILE)
        ids = [c["id"] for c in doc["cau"]]
        self.assertEqual(len(ids), len(set(ids)))
        for c in doc["cau"]:
            norm = normalize.normalize_text(c["van_ban"])["normalized"]
            for k in c["tu_khoa"]:
                if c["nhom"] not in ("ten_rieng", "tu_kho"):
                    self.assertIn(evaluation._clean(k), evaluation._clean(norm), c["id"])

    def test_cham_transcript_co_chu_so(self):
        self.assertIn(evaluation._clean("hai mươi hai tháng năm"), evaluation._clean("sinh ngày 22 tháng 5 năm 2003"))
        self.assertIn(evaluation._clean("đảng ủy"), evaluation._clean("Đảng uỷ xã"))
        self.assertIn(evaluation._clean("tháng tư"), evaluation._clean("kết thúc tháng 4 năm 2026"))

    def test_moi_lan_chay_khong_ghi_de(self):
        with tempfile.TemporaryDirectory() as d:
            a = evaluation.run_eval(Path(d), "thu-nghiem", "nam", **QUIET)
            r = read_json(a / "ket-qua.json")
            self.assertEqual(r["asr"]["status"], "NOT_RUN")
            self.assertIn("GIẢ", (a / "bao-cao.md").read_text(encoding="utf-8"))
            evaluation.grade(a, r["cases"][0]["id"], "loi", "đọc sai")
            self.assertIn("loi", (a / "ket-qua.csv").read_text(encoding="utf-8-sig"))


@unittest.skipUnless(HAS_FFMPEG, "cần ffmpeg/ffprobe")
class TestNghiemThu(TempHome):
    def test_workflow_mau_dat_tieu_chi(self):
        res = nghiem_thu.run("thu-nghiem", self.d, **QUIET)
        failed = [c for c in res["tieu_chi"] if not c["dat"]]
        self.assertEqual(failed, [])
        self.assertIn("CHƯA ĐÁNH GIÁ", res["noi_dung"])


if __name__ == "__main__":
    unittest.main()
