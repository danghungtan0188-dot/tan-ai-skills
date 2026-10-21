#!/usr/bin/env python3
"""Kiem tra file video da render, xuat VideoQAReport (data-contracts/video.schema.json).

Day la lop kiem tra dung chung cua repo: hook check_render.py goi che do
--lenient, command /review-video va agent video-reviewer goi che do --strict.

Vi du:
  python scripts/video_qa.py out.mp4 --strict --audio
  python scripts/video_qa.py out.mp4 --source raw.mp4 --cut-authorized

--strict --audio con kiem them loi nhin/nghe thay duoc: khung dau den (anh bia), duoi den (reel lap
loe den), doan den giua >= 1 s, do to tong ngoai -18..-12 LUFS, bitrate qua cao.

Exit 0 = PASS (hoac WARN), exit 1 = FAIL, exit 2 = khong chay duoc ffprobe.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

VIDEO_EXT = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v"}
AUDIO_EXT = {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg"}
MIN_BYTES = 1024
DURATION_TOLERANCE = 0.1  # giay
AV_TOLERANCE = 0.5  # giay — hinh lech tieng qua muc nay la mat canh
# Dinh tieng (true peak) do tren file DA ma hoa: AAC day dinh len (tranh giay 20/10: -1,9 truoc AAC
# thanh +0,8 dBTP sau AAC ma QA van PASS). Vuot -1 dBTP la nguy co re khi phat.
TRUE_PEAK_MAX = -1.0
# Nguong chat luong nghe/nhin (chi chay o --strict --audio). Do tren 6 video da giao (10/2026):
# I -16..-13,4 LUFS, bpp 0,056..0,166; den giua video chi la chuyen canh qua den ~0,4 s.
# Khong kiem LRA tuyet doi: giong TTS VieNeu chua qua limiter da chi 1,6 LU. Bop dai dong phai do
# truoc/sau buoc xu ly am thanh, khong do mot con so tren file cuoi.
LUFS_RANGE = (-18.0, -12.0)  # ban tin -16, mang xa hoi -14
BPP_MAX = 0.25  # bit/diem anh/khung: vuot = file nang, Zalo/Facebook nen lai
DEN_GIUA_CANH_BAO, DEN_GIUA_LOI = 1.0, 3.0  # giay


def probe(path: Path) -> dict:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_format", "-show_streams",
         "-of", "json", str(path)],
        text=True, capture_output=True, encoding="utf-8", errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffprobe that bai")
    return json.loads(result.stdout)


def duration_of(path: Path) -> float:
    return float(probe(path).get("format", {}).get("duration", 0.0))


def parse_fps(rate: str) -> float:
    try:
        num, _, den = rate.partition("/")
        return round(float(num) / float(den or 1), 3)
    except (ValueError, ZeroDivisionError):
        return 0.0


def has_faststart(path: Path) -> bool:
    """moov atom nam truoc mdat => phat duoc ngay khi chua tai xong."""
    with path.open("rb") as handle:
        head = handle.read(131072)
    moov, mdat = head.find(b"moov"), head.find(b"mdat")
    if moov == -1:
        return False
    return mdat == -1 or moov < mdat


def mean_volume_db(path: Path) -> float | None:
    """None neu khong do duoc. -91 dB nghia la track im lang hoan toan."""
    result = subprocess.run(
        ["ffmpeg", "-v", "info", "-i", str(path), "-af", "volumedetect",
         "-f", "null", "-"],
        text=True, capture_output=True, encoding="utf-8", errors="replace",
    )
    for line in result.stderr.splitlines():
        if "mean_volume:" in line:
            try:
                return float(line.split("mean_volume:")[1].strip().split()[0])
            except (IndexError, ValueError):
                return None
    return None


def true_peak_db(path: Path) -> float | None:
    """Dinh tieng thuc (dBTP, do ebur128) cua track tieng; None neu khong do duoc."""
    result = subprocess.run(
        ["ffmpeg", "-v", "info", "-nostats", "-i", str(path), "-af", "ebur128=peak=true",
         "-f", "null", "-"],
        text=True, capture_output=True, encoding="utf-8", errors="replace",
    )
    lines = result.stderr.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "True peak:":
            for nxt in lines[i + 1:i + 3]:
                if "Peak:" in nxt:
                    try:
                        return float(nxt.split("Peak:")[1].split()[0])
                    except (IndexError, ValueError):
                        return None
    return None


def quet_chat_luong(path: Path, has_video: bool) -> dict:
    """Mot luot giai ma: doan den (blackdetect) + do to tong (EBU R128)."""
    cmd = ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path)]
    if has_video:
        cmd += ["-vf", "blackdetect=d=0.3:pix_th=0.1"]
    cmd += ["-af", "ebur128", "-f", "null", "-"]
    err = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    den = [(float(a), float(b)) for a, b in re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", err)]
    tong = err[err.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+) LUFS", tong)
    return {"den": den, "lufs": float(i.group(1)) if i else None}


class Report:
    def __init__(self, artifact: Path):
        self.artifact = artifact
        self.checks: list[dict] = []

    def add(self, name: str, status: str, detail: str = "") -> None:
        self.checks.append({"name": name, "status": status, "detail": detail})

    def by_status(self, status: str) -> list[str]:
        return [f"{c['name']}: {c['detail']}" for c in self.checks
                if c["status"] == status]

    def render(self, probe_data: dict | None) -> dict:
        errors, warnings = self.by_status("FAIL"), self.by_status("WARN")
        return {
            "artifact": str(self.artifact),
            "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "status": "FAIL" if errors else ("WARN" if warnings else "PASS"),
            "checks": self.checks,
            "errors": errors,
            "warnings": warnings,
            "probe": probe_data or {},
        }


def summarise_probe(data: dict) -> dict:
    video = next((s for s in data.get("streams", [])
                  if s.get("codec_type") == "video"), {})
    audio = next((s for s in data.get("streams", [])
                  if s.get("codec_type") == "audio"), {})
    summary = {"duration": float(data.get("format", {}).get("duration", 0.0)),
               "size_bytes": int(data.get("format", {}).get("size", 0))}
    if video:
        summary["video"] = {
            "codec": video.get("codec_name", ""),
            "width": int(video.get("width", 0)),
            "height": int(video.get("height", 0)),
            "pix_fmt": video.get("pix_fmt", ""),
            "fps": parse_fps(video.get("r_frame_rate", "0/1")),
            "duration": float(video.get("duration", 0) or 0),
            "bit_rate": int(video.get("bit_rate", 0) or 0),
        }
    if audio:
        summary["audio"] = {
            "codec": audio.get("codec_name", ""),
            "sample_rate": int(audio.get("sample_rate", 0) or 0),
            "channels": int(audio.get("channels", 0) or 0),
            "duration": float(audio.get("duration", 0) or 0),
        }
    return summary


def chat_luong(report: Report, artifact: Path, summary: dict, hard: str) -> None:
    """Loi nhin/nghe thay duoc ma kiem dinh dang khong bat: doan den, do to tong, bitrate qua cao."""
    video, dur = summary.get("video"), summary["duration"]
    q = quet_chat_luong(artifact, bool(video))
    if video:
        dau = [d for d in q["den"] if d[0] <= 0.05]
        duoi = [d for d in q["den"] if d[1] >= dur - 0.1 and d[0] > 0.05]
        giua = [d for d in q["den"] if d not in dau + duoi and d[1] - d[0] >= DEN_GIUA_CANH_BAO]
        if dau:
            report.add("black_start", "WARN", f"Den {dau[0][1]:.1f} s dau — anh bia Facebook/Zalo se den, mat nguoi xem")
        if duoi:
            report.add("black_tail", "WARN", f"Den tu {duoi[0][0]:.1f} s toi het — reel lap lai se loe den; "
                                             "giu khung cuoi (tpad=stop_mode=clone) neu khong co y")
        for a, b in giua:
            report.add("black_middle", hard if b - a >= DEN_GIUA_LOI else "WARN", f"Den {a:.1f}–{b:.1f} s ({b - a:.1f} s)")
        if not (dau or duoi or giua):
            report.add("black_frames", "PASS", "khong co doan den bat thuong")
        if video["bit_rate"] and video["width"] and video["fps"]:
            bpp = video["bit_rate"] / (video["width"] * video["height"] * video["fps"])
            # khong canh bao bitrate thap: ma hoa crf tu ha bitrate khi hinh don gian (nen mot mau 0,1 Mbps
            # van net), nen bitrate thap khong co nghia la vo khoi
            if bpp > BPP_MAX:
                report.add("bitrate", "WARN", f"{video['bit_rate'] / 1e6:.1f} Mbps (bpp {bpp:.3f}) — file nang, "
                                              "nen tang se nen lai; tang crf hoac lam ban _ZALO")
            else:
                report.add("bitrate", "PASS", f"{video['bit_rate'] / 1e6:.1f} Mbps (bpp {bpp:.3f})")
    if q["lufs"] is not None:
        lo, hi = LUFS_RANGE
        report.add("loudness", "PASS" if lo <= q["lufs"] <= hi else "WARN",
                   f"{q['lufs']:.1f} LUFS" + ("" if lo <= q["lufs"] <= hi else
                                               f" ngoai {lo:.0f}..{hi:.0f} — loudnorm 2 luot linear ve -16 (ban tin) / -14 (MXH)"))


def check(args) -> dict:
    artifact = Path(args.artifact)
    report = Report(artifact)
    hard = "FAIL" if args.strict else "WARN"

    if not artifact.exists():
        report.add("file_exists", "FAIL", "File khong ton tai")
        return report.render(None)
    size = artifact.stat().st_size
    if size < MIN_BYTES:
        report.add("file_size", "FAIL", f"Chi {size} byte, coi nhu render hong")
        return report.render(None)
    report.add("file_exists", "PASS", f"{size} byte")

    try:
        data = probe(artifact)
    except (RuntimeError, json.JSONDecodeError) as exc:
        report.add("ffprobe", "FAIL", str(exc))
        return report.render(None)
    summary = summarise_probe(data)

    if summary["duration"] <= 0:
        report.add("duration", "FAIL", "Thoi luong bang 0")
    else:
        report.add("duration", "PASS", f"{summary['duration']:.3f} giay")

    suffix = artifact.suffix.lower()
    if suffix in VIDEO_EXT:
        if "video" not in summary:
            report.add("video_stream", "FAIL", "Khong co luong hinh")
        else:
            video = summary["video"]
            report.add("video_stream", "PASS",
                       f"{video['codec']} {video['width']}x{video['height']} "
                       f"@{video['fps']}fps")
            if video["width"] % 2 or video["height"] % 2:
                report.add("even_dimensions", "FAIL",
                           "Kich thuoc le, H.264 khong ma hoa duoc on dinh")
            if suffix in {".mp4", ".mov"}:
                if video["pix_fmt"] != "yuv420p":
                    report.add("pix_fmt", hard,
                               f"{video['pix_fmt']} thay vi yuv420p "
                               "(nhieu trinh phat se khong mo duoc)")
                else:
                    report.add("pix_fmt", "PASS", "yuv420p")
                if video["codec"] != "h264":
                    report.add("video_codec", hard,
                               f"{video['codec']} thay vi h264")
                if has_faststart(artifact):
                    report.add("faststart", "PASS", "moov nam truoc mdat")
                else:
                    report.add("faststart", hard,
                               "Thieu faststart, video khong phat duoc khi dang tai")

    if suffix in VIDEO_EXT | AUDIO_EXT:
        if "audio" not in summary:
            report.add("audio_stream", hard, "Khong co luong tieng")
        else:
            audio = summary["audio"]
            report.add("audio_stream", "PASS",
                       f"{audio['codec']} {audio['sample_rate']}Hz "
                       f"{audio['channels']}ch")
            if suffix == ".mp4" and audio["codec"] != "aac":
                report.add("audio_codec", hard, f"{audio['codec']} thay vi aac")

    # Hinh va tieng phai dai bang nhau: xfade gap mot canh ngan se lang le bo het hinh phia sau
    # (video6: hinh 172 s, tieng 198 s, cac buoc khac van PASS).
    vd, ad = summary.get("video", {}).get("duration", 0), summary.get("audio", {}).get("duration", 0)
    if vd and ad:
        if abs(vd - ad) > AV_TOLERANCE:
            report.add("av_length", hard, f"Hinh {vd:.2f} s, tieng {ad:.2f} s (lech {vd - ad:+.2f} s)")
        else:
            report.add("av_length", "PASS", f"lech {vd - ad:+.3f} s")

    if args.audio and "audio" in summary:
        mean = mean_volume_db(artifact)
        if mean is None:
            report.add("audio_level", "WARN", "Khong do duoc muc am")
        elif mean <= -70:
            report.add("audio_level", "FAIL",
                       f"mean_volume {mean} dB — track tieng im lang")
        else:
            report.add("audio_level", "PASS", f"mean_volume {mean} dB")
        peak = true_peak_db(artifact)
        if peak is None:
            report.add("true_peak", "WARN", "Khong do duoc dinh tieng")
        elif peak > TRUE_PEAK_MAX:
            report.add("true_peak", hard, f"{peak:+.1f} dBTP > {TRUE_PEAK_MAX} — nguy co re; gioi han dinh truoc khi ma hoa")
        else:
            report.add("true_peak", "PASS", f"{peak:+.1f} dBTP")

    if args.strict and args.audio and summary["duration"] > 0:
        chat_luong(report, artifact, summary, hard)

    if args.source:
        source = Path(args.source)
        if not source.exists():
            report.add("duration_vs_source", "WARN",
                       f"Khong tim thay nguon {source}")
        else:
            try:
                drift = summary["duration"] - duration_of(source)
            except (RuntimeError, ValueError) as exc:
                report.add("duration_vs_source", "WARN", str(exc))
            else:
                if not args.cut_authorized and abs(drift) > DURATION_TOLERANCE:
                    report.add("duration_vs_source", "FAIL",
                               f"Lech {drift:+.3f} giay so voi nguon nhung "
                               "chua duoc phep cat")
                else:
                    report.add("duration_vs_source", "PASS",
                               f"Lech {drift:+.3f} giay")

    return report.render(summary)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("artifact", help="File video/audio da render")
    parser.add_argument("--source", help="File nguon de doi chieu thoi luong")
    parser.add_argument("--cut-authorized", action="store_true",
                        help="Nguoi dung da cho phep cat, bo qua kiem tra lech thoi luong")
    parser.add_argument("--strict", action="store_true",
                        help="Coi cac canh bao dinh dang la loi (dung khi review cuoi)")
    parser.add_argument("--audio", action="store_true",
                        help="Do muc am de phat hien track tieng im lang (cham)")
    parser.add_argument("--quiet", action="store_true",
                        help="Chi in dong tom tat, khong in JSON")
    args = parser.parse_args()

    if not shutil.which("ffprobe"):
        print("Khong tim thay ffprobe tren PATH. "
              "Cai bang: winget install Gyan.FFmpeg", file=sys.stderr)
        return 2

    report = check(args)
    if args.quiet:
        print(f"{report['status']} {report['artifact']}")
        for line in report["errors"] + report["warnings"]:
            print(f"  - {line}")
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
