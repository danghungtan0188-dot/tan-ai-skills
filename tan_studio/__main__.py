"""CLI: python -m tan_studio <lệnh>. Xem tan_studio/README.md."""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import sys
from pathlib import Path

from . import REPO_ROOT, SKILL_DIRS, read_json, write_json

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def _p(obj) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def _project(a):
    from .workflow import load_project
    return load_project(Path(a.du_an))


# ---------- môi trường, chuẩn hoá, TTS ----------

def cmd_kiem_tra(a) -> int:
    rows = [
        ("python >= 3.10", sys.version_info >= (3, 10), "mọi lệnh"),
        ("ffmpeg", bool(shutil.which("ffmpeg")), "dung_video, kiem_tra, mp3"),
        ("ffprobe", bool(shutil.which("ffprobe")), "kiem_tra (QA)"),
        *[(f"skill {k}: {p.relative_to(REPO_ROOT)}", p.exists(), "nạp code dùng lại") for k, p in SKILL_DIRS.items()],
        ("numpy", importlib.util.find_spec("numpy") is not None, "kiểm tra audio (im lặng, vỡ tiếng, tốc độ đọc)"),
        ("vieneu", importlib.util.find_spec("vieneu") is not None, "giọng thật (engine vieneu)"),
        ("soundfile", importlib.util.find_spec("soundfile") is not None, "giọng thật (engine vieneu)"),
        ("python-docx", importlib.util.find_spec("docx") is not None, "kịch bản .docx (tuỳ chọn)"),
        ("faster-whisper", importlib.util.find_spec("faster_whisper") is not None, "danh-gia-tts --asr (tuỳ chọn)"),
        ("jsonschema", importlib.util.find_spec("jsonschema") is not None, "test schema (tuỳ chọn)"),
    ]
    width = max(len(r[0]) for r in rows)
    for name, ok, used in rows:
        print(f"{'OK   ' if ok else 'THIẾU'}  {name.ljust(width)}  ← {used}")
    print("\nChỉ kiểm thư viện đã cài, KHÔNG tải model. Lần đầu chạy vieneu sẽ tải model (cần mạng).")
    return 0 if all(ok for _, ok, _ in rows[:3 + len(SKILL_DIRS)]) else 1


def cmd_chuan_hoa(a) -> int:
    from .normalize import normalize_script
    from .rules import active_pronunciations
    pdir = _project(a)["_dir"] if a.du_an else None
    data = normalize_script(Path(a.kich_ban), a.tat or [], active_pronunciations(pdir))
    if a.out:
        write_json(Path(a.out), data)
        print(f"Đã lưu: {a.out}")
    for s in data["segments"]:
        print(s["normalized"])
        if a.giai_thich:
            for c in s["changes"]:
                print(f"    [{c['quy_tac']}] {c['tu']!r} → {c['thanh']!r} ({c['ly_do']})")
        for f in s["flags"]:
            print(f"    ! {f['loai']}: {f['doan']} — {f['ly_do']}")
    return 0


def cmd_doc(a) -> int:
    from .normalize import normalize_script
    from .rules import active_pronunciations
    from .tts import synthesize
    src = Path(a.dau_vao)
    data = read_json(src) if src.suffix == ".json" else normalize_script(src, phat_am=active_pronunciations(None))
    res = synthesize(data, Path(a.out_dir), a.engine, a.giong, a.phong_cach, 1.0, a.khoang_lang_ms, a.mp3)
    print(f"Audio: {res['audio']} ({res.get('duration')} giây, engine {res['engine']} {res['version']})")
    if res["placeholder"]:
        print("CẢNH BÁO: audio GIẢ (tiếng bíp) — không phải giọng đọc.")
    for f in res["failures"]:
        print(f"LỖI đoạn {f['index']}: {f['loi']}", file=sys.stderr)
    return 1 if res["failures"] else 0


def cmd_long_tieng(a) -> int:
    from .long_tieng import dub
    from .rules import active_pronunciations
    src = Path(a.phu_de)
    out = Path(a.out_dir) if a.out_dir else src.with_name(f"{src.stem}-long-tieng")
    res = dub(src, out, a.engine, a.giong, a.phong_cach, a.toc_do_toi_da, active_pronunciations(None))
    print(f"Audio: {res['audio']} ({res['duration']} giây, {len(res['cau'])} câu, engine {res['engine']})")
    print(f"Đọc nhanh hơn: {res['so_cau_doc_nhanh']} câu · bị lùi: {res['so_cau_bi_lui']} câu")
    if res["phu_de_da_chinh"]:
        print(f"Có câu bị lùi — dùng phụ đề đã chỉnh mốc: {res['phu_de_da_chinh']}")
    if res["placeholder"]:
        print("CẢNH BÁO: audio GIẢ (tiếng bíp) — không phải giọng đọc.")
    return 0


def cmd_do_hoa(a) -> int:
    from . import do_hoa, subtitles, video
    props = read_json(Path(a.props)) if a.props else {}
    for kv in a.dat or []:
        k, _, v = kv.partition("=")
        try:
            props[k] = json.loads(v)
        except json.JSONDecodeError:
            props[k] = v
    props = do_hoa.camel(props)
    comp = do_hoa.comp_id(a.mau)
    public = None
    if a.tu_lan_chay:
        if comp != "ChuDong":
            print("--tu-lan-chay chỉ dùng với mẫu chu-dong", file=sys.stderr)
            return 2
        run = Path(a.tu_lan_chay)
        audio = run / "giong-doc" / "giong-doc.wav"
        public = run / "do-hoa-public"
        public.mkdir(exist_ok=True)
        shutil.copy2(audio, public / "giong-doc.wav")
        props = {"tiLe": "9:16", "amThanh": "giong-doc.wav", "thoiLuong": video.video_qa.duration_of(audio),
                 "cau": [{"chu": c["vi"].replace("\n", " "), "start": c["start"], "end": c["end"]}
                         for c in subtitles.read_srt(run / "phu-de.srt")], **props}
    props.setdefault("tiLe", a.ti_le)
    props.setdefault("thoiLuong", a.thoi_luong or do_hoa.GIAY_MAC_DINH.get(comp, 5.0))
    ext = ".png" if a.anh is not None else (".mov" if comp in do_hoa.TRONG_SUOT else ".mp4")
    out = Path(a.out) if a.out else (Path(a.tu_lan_chay) if a.tu_lan_chay else Path("outputs/do-hoa")) / f"{comp}{ext}"
    res = do_hoa.render(comp, props, out, a.anh, public)
    print(f"Đã xuất: {res}")
    if ext == ".mov":
        print("(.mov ProRes 4444 có nền trong suốt — đắp lên video bằng mục \"do_hoa\" trong file dự án hoặc CapCut)")
    return 0


# ---------- workflow ----------

def _print_run(report) -> int:
    print(f"\nLần chạy {report['run_id']}: kỹ thuật {report['status']} — nội dung: chưa đánh giá (cần bạn xem/nghe)")
    print(f"Báo cáo: {Path(report['run_dir']) / 'bao-cao.md'}")
    for w in report.get("canh_bao_chay_lai", []):
        print(f"⚠ {w}")
    return 1 if report["status"] in ("FAILED", "INCOMPLETE") else 0


def cmd_chay(a) -> int:
    from .workflow import run
    return _print_run(run(Path(a.du_an), a.buoc.split(",") if a.buoc else None, a.lan_chay,
                          xem_truoc=a.xem_truoc))


def cmd_chay_lai(a) -> int:
    from .workflow import rerun
    return _print_run(rerun(Path(a.du_an), a.lan_chay))


def cmd_bao_cao(a) -> int:
    from .workflow import render_report, resolve_run
    p = Path(a.dich)
    run_dir = p if p.is_dir() else resolve_run(_project(argparse.Namespace(du_an=p)), a.lan_chay)
    print(render_report(read_json(run_dir / "run.json")))
    print(f"(thư mục: {run_dir})")
    return 0


def cmd_nghiem_thu(a) -> int:
    from .nghiem_thu import run
    res = run(a.engine)
    for c in res["tieu_chi"]:
        print(f"{'ĐẠT     ' if c['dat'] else 'KHÔNG ĐẠT'}  {c['tieu_chi']}  {c['chi_tiet']}")
    print(f"\nKỹ thuật: {res['ket_luan_ky_thuat']} — Nội dung: {res['noi_dung']}\nThư mục: {res['thu_muc']}")
    return 0 if res["ket_luan_ky_thuat"] == "ĐẠT" else 1


# ---------- đánh giá TTS ----------

def cmd_danh_gia_tts(a) -> int:
    from .evaluation import CASES_FILE, run_eval
    run_dir = run_eval(Path(a.out), a.engine, a.giong, a.phong_cach, a.asr, a.luot,
                       Path(a.bo_cau) if a.bo_cau else CASES_FILE)
    print((run_dir / "bao-cao.md").read_text(encoding="utf-8"))
    print(f"Kết quả: {run_dir}")
    return 0


def cmd_cham(a) -> int:
    from .evaluation import grade
    grade(Path(a.lan_chay), a.cau, a.ket_luan, a.ghi_chu or "")
    print(f"Đã ghi chấm tay {a.cau}: {a.ket_luan}. Báo cáo: {Path(a.lan_chay) / 'bao-cao.md'}")
    return 0


# ---------- review ----------

def cmd_xem_lai(a) -> int:
    from . import review
    from .workflow import resolve_run, set_content_verdict
    cfg = _project(a)
    run_dir = resolve_run(cfg, a.lan_chay)
    if a.hanh_dong in ("chap-nhan", "tu-choi"):
        kl = a.hanh_dong.replace("-", "_")
        review.verdict(cfg["_dir"], run_dir, kl, a.ghi_chu or "")
        set_content_verdict(run_dir, kl)
        print(f"Lần chạy {run_dir.name}: {kl}.")
    elif a.hanh_dong == "loi":
        if not a.loai or not a.mo_ta:
            print("LỖI: cần --loai và mô tả (ví dụ: xem-lai du-an.json loi --loai phat_am \"đọc sai VNeID\")",
                  file=sys.stderr)
            return 2
        o = review.add_observation(cfg["_dir"], cfg, run_dir, a.loai, a.mo_ta, a.tu, a.doc_dung, a.doan, a.tai,
                                   a.canh, a.de_xuat or "", a.uu_tien, a.pham_vi)
        print(f"Đã ghi quan sát {o['id']} (lần chạy {run_dir.name}).")
        if o["trung_voi"]:
            print(f"  trùng với {o['trung_voi']} — lỗi này đã gặp ở: {o['lap_lai_tu_lan_chay'] or 'cùng lần chạy'}")
        if o["quy_tac"]:
            print(f"  → quy tắc ĐỀ XUẤT {o['quy_tac']} (chưa áp dụng). Thử: quy-tac thu {a.du_an} {o['quy_tac']}"
                  f"  · Duyệt: quy-tac duyet {a.du_an} {o['quy_tac']}")
    elif a.hanh_dong == "canh-bao":
        if not a.id or a.dung_sai not in ("dung", "sai"):
            print("LỖI: xem-lai du-an.json canh-bao --id <ph-...> --dung-sai dung|sai", file=sys.stderr)
            return 2
        review.finding_verdict(cfg["_dir"], cfg, run_dir, a.id, a.dung_sai == "dung", a.ghi_chu or "")
        print(f"Đã ghi: cảnh báo {a.id} {'ĐÚNG → thành quan sát' if a.dung_sai == 'dung' else 'SAI (cảnh báo nhầm)'}.")
    else:
        found = read_json(run_dir / "phat-hien.json", {"phat_hien": []})["phat_hien"]
        from .checks import describe
        print(f"Lần chạy {run_dir.name} — {len(found)} phát hiện tự động:")
        for f in found:
            print("  " + describe(f))
        obs = [o for o in review.observations(cfg["_dir"]) if o["lan_chay"] == run_dir.name]
        print(f"{len(obs)} quan sát của người dùng:")
        for o in obs:
            print(f"  {o['id']} [{o['loai']}/{o['uu_tien']}] {o['vi_tri']} {o['mo_ta']}")
    return 0


# ---------- quy tắc ----------

def cmd_quy_tac(a) -> int:
    from . import rules
    pdir = _project(a)["_dir"] if a.du_an else None
    act = a.hanh_dong
    if act == "danh-sach":
        from .normalize import list_rules
        print("Quy tắc chuẩn hoá cố định:")
        for rid, desc in list_rules():
            print(f"  {rid:15} {desc}")
        print("\nQuy tắc học được:")
        for scope, r in rules.all_rules(pdir):
            print(f"  {r['id']}  {scope:8} {r['trang_thai']:9} {'bật' if r['bat'] else 'tắt'}  v{r['phien_ban']}  "
                  f"'{r['dieu_kien']['tu']}' → '{r['bien_doi']['doc_thanh']}'"
                  + (f"  MÂU THUẪN với {r['mau_thuan_voi']}" if r.get("mau_thuan_voi") else ""))
        return 0
    if act == "kiem":
        res = rules.regression(pdir)
        for r in res:
            print(f"{'PASS' if r['ok'] else 'FAIL'}  {r['id']} ({r['pham_vi']}): {r['dau_vao']!r} → {r['thuc_te']!r}")
        print(f"{sum(r['ok'] for r in res)}/{len(res)} ca kiểm thử hồi quy qua")
        return 0 if all(r["ok"] for r in res) else 1
    if not a.id:
        print("LỖI: cần id quy tắc", file=sys.stderr)
        return 2
    if act == "duyet":
        r = rules.approve(pdir, a.id, a.pham_vi, a.ghi_chu or "")
        print(f"Đã duyệt {r['id']} v{r['phien_ban']} ({r['pham_vi']}): '{r['dieu_kien']['tu']}' → "
              f"'{r['bien_doi']['doc_thanh']}'. Ca kiểm thử: {r['kiem_thu'][0]['dau_vao']!r}")
    elif act == "tu-choi":
        rules.reject(pdir, a.id, a.ghi_chu or "")
        print(f"Đã từ chối {a.id}.")
    elif act in ("tat", "bat"):
        r = rules.set_enabled(pdir, a.id, act == "bat", a.ghi_chu or "")
        print(f"{a.id}: {'bật' if r['bat'] else 'tắt'} (v{r['phien_ban']}).")
    elif act == "hoan-tac":
        r = rules.undo(pdir, a.id)
        print(f"{a.id}: đã hoàn tác → {r['trang_thai']}, {'bật' if r['bat'] else 'tắt'}, {r['pham_vi']} (v{r['phien_ban']}).")
    elif act == "lich-su":
        _, _, r = rules._find(pdir, a.id)
        for h in r["lich_su"]:
            print(f"v{h['phien_ban']}  {h['luc']}  {h['hanh_dong']}  {h.get('ghi_chu', '')}")
    elif act == "thu":
        rep = rules.trial(pdir, a.id, rules.history_samples(pdir))
        print(f"Thử {a.id} trên {rep['so_mau']} câu mẫu + kiểm thử của mọi quy tắc đã duyệt: {rep['ket_luan']}")
        for x in rep["xau_di"]:
            print(f"  XẤU ĐI: hỏng kiểm thử của {x['kiem_thu_cua']}: {x['dau_vao']!r}")
        for x in rep["doi_khac"][:20]:
            print(f"  ĐỔI [{x['nguon']}]: {x['truoc']!r}\n        → {x['sau']!r}")
        print(f"  không đổi: {rep['khong_doi']} câu. (Chưa áp dụng gì — duyệt bằng `quy-tac duyet`.)")
    return 0


# ---------- đo lường, so sánh, dữ liệu ----------

def cmd_chi_so(a) -> int:
    from .metrics import project_metrics
    for proj in a.du_an:
        print(f"== {proj}")
        _p(project_metrics(Path(proj), a.theo))
    return 0


def cmd_lich_su_loi(a) -> int:
    from .metrics import error_history
    h = error_history(Path(a.du_an), a.loc)
    print("Lần chạy: " + "  ".join(f"{i + 1}={r}" for i, r in enumerate(h["lan_chay"])))
    print("Quy tắc đang bật: " + (", ".join(h["quy_tac_dang_bat"]) or "—"))
    for row in h["dong"]:
        print(f"  {' '.join(row['lan_chay'])}   {row['dau_van_tay']}"
              + ("" if row["con_o_lan_moi_nhat"] else "   (đã hết ở lần mới nhất)"))
    return 0


def cmd_so_sanh(a) -> int:
    from .metrics import compare
    out = Path(a.video) if a.video else None
    _p(compare(Path(a.du_an), a.a, a.b, out))
    return 0


def cmd_du_lieu(a) -> int:
    from . import du_lieu
    act = a.hanh_dong
    if act == "xem":
        _p(du_lieu.overview(Path(a.du_an)))
    elif act == "xuat":
        print(du_lieu.export(Path(a.du_an), Path(a.tep or "du-lieu.zip"), a.lan_chay, a.kem_media))
    elif act == "xoa-lan-chay":
        _p(du_lieu.delete_run(Path(a.du_an), a.lan_chay, a.chac_chan))
    elif act == "don-dep":
        _p(du_lieu.cleanup(Path(a.du_an), a.giu, a.chac_chan))
    elif act == "xoa-du-an":
        _p(du_lieu.delete_project_data(Path(a.du_an), a.chac_chan))
    if act.startswith(("xoa", "don")) and not a.chac_chan:
        print("(chỉ là kế hoạch — thêm --chac-chan để xoá thật; không hoàn tác được)")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="python -m tan_studio", description="Script → giọng đọc → video có phụ đề.")
    sub = p.add_subparsers(dest="lenh", required=True)

    sub.add_parser("kiem-tra", help="kiểm tra công cụ và thư viện").set_defaults(fn=cmd_kiem_tra)

    s = sub.add_parser("chuan-hoa", help="chuẩn hoá một kịch bản .txt/.docx")
    s.add_argument("kich_ban")
    s.add_argument("--du-an", help="dùng thêm quy tắc đã duyệt của dự án")
    s.add_argument("--out")
    s.add_argument("--tat", nargs="*", help="tắt quy tắc theo id")
    s.add_argument("--giai-thich", action="store_true", help="in từng thay đổi và lý do")
    s.set_defaults(fn=cmd_chuan_hoa)

    s = sub.add_parser("doc", help="chỉ tạo giọng đọc")
    s.add_argument("dau_vao")
    s.add_argument("--out-dir", required=True)
    s.add_argument("--engine", default="vieneu")
    s.add_argument("--giong", default="nam")
    s.add_argument("--phong-cach", default="tin_tuc")
    s.add_argument("--khoang-lang-ms", type=int, default=450)
    s.add_argument("--mp3", action="store_true")
    s.set_defaults(fn=cmd_doc)

    s = sub.add_parser("long-tieng", help="lồng tiếng theo file phụ đề .srt/.vtt (đọc đúng mốc thời gian)")
    s.add_argument("phu_de")
    s.add_argument("--out-dir", help="mặc định: <tên file>-long-tieng/ cạnh file phụ đề")
    s.add_argument("--engine", default="vieneu")
    s.add_argument("--giong", default="nam")
    s.add_argument("--phong-cach", default="tin_tuc")
    s.add_argument("--toc-do-toi-da", type=float, default=1.15, help="đọc nhanh tối đa (1.0–1.5)")
    s.set_defaults(fn=cmd_long_tieng)

    s = sub.add_parser("do-hoa", help="đồ hoạ động Remotion: intro, so-lieu, lower-third, chu-dong")
    s.add_argument("mau", help="intro | so-lieu | lower-third | chu-dong")
    s.add_argument("--props", help="file JSON props (snake_case hoặc camelCase)")
    s.add_argument("--dat", action="append", metavar="KHOA=GIA_TRI", help="đặt từng props, vd --dat tieu_de=\"...\"")
    s.add_argument("--ti-le", default="16:9", choices=["16:9", "9:16"])
    s.add_argument("--thoi-luong", type=float, help="giây (mặc định intro 4, so-lieu 5, lower-third 5)")
    s.add_argument("--anh", type=float, metavar="GIAY", help="chỉ xuất 1 khung PNG ở giây này để xem nhanh")
    s.add_argument("--tu-lan-chay", metavar="THU_MUC", help="chu-dong: lấy giọng + phụ đề từ một lần chạy")
    s.add_argument("--out")
    s.set_defaults(fn=cmd_do_hoa)

    s = sub.add_parser("chay", help="chạy workflow theo file dự án")
    s.add_argument("du_an")
    s.add_argument("--buoc", help="chỉ chạy các bước này (phẩy ngăn cách)")
    s.add_argument("--lan-chay", help="chạy tiếp trên lần chạy cũ")
    s.add_argument("--xem-truoc", action="store_true", help="render nửa độ phân giải, mã hoá nhanh")
    s.set_defaults(fn=cmd_chay)

    s = sub.add_parser("chay-lai", help="chạy lại một lần chạy cũ với đúng cấu hình đã lưu")
    s.add_argument("du_an")
    s.add_argument("lan_chay")
    s.set_defaults(fn=cmd_chay_lai)

    s = sub.add_parser("bao-cao", help="in báo cáo (mới nhất, --lan-chay, hoặc thư mục)")
    s.add_argument("dich")
    s.add_argument("--lan-chay")
    s.set_defaults(fn=cmd_bao_cao)

    s = sub.add_parser("nghiem-thu", help="chạy workflow mẫu và kiểm tiêu chí nghiệm thu")
    s.add_argument("--engine", default="thu-nghiem", help="thu-nghiem (nhanh, audio giả) hoặc vieneu")
    s.set_defaults(fn=cmd_nghiem_thu)

    s = sub.add_parser("danh-gia-tts", help="đọc bộ câu mẫu, chấm (tuỳ chọn ASR)")
    s.add_argument("--out", default=str(REPO_ROOT / "outputs" / "tts-eval"))
    s.add_argument("--engine", default="vieneu")
    s.add_argument("--giong", default="nam")
    s.add_argument("--phong-cach", default="tin_tuc")
    s.add_argument("--bo-cau")
    s.add_argument("--asr", action="store_true", help="whisper small trên CPU (nóng máy)")
    s.add_argument("--luot", type=int, default=3, choices=[1, 3, 5])
    s.set_defaults(fn=cmd_danh_gia_tts)

    s = sub.add_parser("cham", help="chấm tay một câu trong lần đánh giá TTS")
    s.add_argument("lan_chay")
    s.add_argument("cau")
    s.add_argument("ket_luan", choices=["dat", "loi"])
    s.add_argument("--ghi-chu")
    s.set_defaults(fn=cmd_cham)

    s = sub.add_parser("xem-lai", help="review lần chạy: chap-nhan | tu-choi | loi | canh-bao | xem")
    s.add_argument("du_an")
    s.add_argument("hanh_dong", choices=["chap-nhan", "tu-choi", "loi", "canh-bao", "xem"])
    s.add_argument("mo_ta", nargs="?", help="mô tả lỗi (với `loi`)")
    s.add_argument("--lan-chay", help="mặc định: lần chạy mới nhất")
    s.add_argument("--loai", choices=["script", "phat_am", "giong_doc", "hinh_anh", "chon_canh", "nhip_dung",
                                      "phu_de", "am_thanh", "thuong_hieu", "ky_thuat"])
    s.add_argument("--tu", help="từ bị lỗi")
    s.add_argument("--doc-dung", help="cách đọc đúng (viết bằng chữ) → sinh quy tắc đề xuất")
    s.add_argument("--doan", type=int, help="số đoạn script")
    s.add_argument("--tai", type=float, help="thời điểm (giây)")
    s.add_argument("--canh", type=int, help="số cảnh")
    s.add_argument("--de-xuat")
    s.add_argument("--uu-tien", default="trung_binh", choices=["cao", "trung_binh", "thap"])
    s.add_argument("--pham-vi", default="du_an", choices=["du_an", "chung"],
                   help="du_an: chỉ dự án này; chung: đề xuất thành quy tắc dùng chung")
    s.add_argument("--id", help="id cảnh báo tự động (với canh-bao)")
    s.add_argument("--dung-sai", choices=["dung", "sai"])
    s.add_argument("--ghi-chu")
    s.set_defaults(fn=cmd_xem_lai)

    s = sub.add_parser("quy-tac", help="danh-sach | duyet | tu-choi | tat | bat | hoan-tac | lich-su | thu | kiem")
    s.add_argument("hanh_dong", choices=["danh-sach", "duyet", "tu-choi", "tat", "bat", "hoan-tac", "lich-su",
                                         "thu", "kiem"])
    s.add_argument("du_an", nargs="?")
    s.add_argument("id", nargs="?")
    s.add_argument("--pham-vi", default="du_an", choices=["du_an", "ca_nhan", "he_thong"])
    s.add_argument("--ghi-chu")
    s.set_defaults(fn=cmd_quy_tac)

    s = sub.add_parser("chi-so", help="chỉ số chất lượng theo thời gian")
    s.add_argument("du_an", nargs="+")
    s.add_argument("--theo", choices=["config_hash", "app_version"])
    s.set_defaults(fn=cmd_chi_so)

    s = sub.add_parser("lich-su-loi", help="một lỗi xuất hiện/biến mất qua các lần chạy")
    s.add_argument("du_an")
    s.add_argument("--loc", help="lọc theo dấu vân tay, ví dụ VNeID")
    s.set_defaults(fn=cmd_lich_su_loi)

    s = sub.add_parser("so-sanh", help="so sánh hai lần chạy")
    s.add_argument("du_an")
    s.add_argument("a")
    s.add_argument("b")
    s.add_argument("--video", help="xuất video đặt cạnh nhau ra file này")
    s.set_defaults(fn=cmd_so_sanh)

    s = sub.add_parser("du-lieu", help="xem | xuat | xoa-lan-chay | don-dep | xoa-du-an")
    s.add_argument("hanh_dong", choices=["xem", "xuat", "xoa-lan-chay", "don-dep", "xoa-du-an"])
    s.add_argument("du_an")
    s.add_argument("--lan-chay")
    s.add_argument("--tep", help="file zip khi xuất")
    s.add_argument("--kem-media", action="store_true")
    s.add_argument("--giu", type=int, default=5, help="don-dep: giữ media của N lần chạy mới nhất")
    s.add_argument("--chac-chan", action="store_true", help="xoá thật")
    s.set_defaults(fn=cmd_du_lieu)

    a = p.parse_args(argv)
    try:
        return a.fn(a)
    except (ValueError, RuntimeError, FileNotFoundError) as exc:
        print(f"LỖI: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
