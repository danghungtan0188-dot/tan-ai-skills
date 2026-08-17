#!/usr/bin/env python3
"""Kiem tra file video da render, xuat VideoQAReport (data-contracts/video.schema.json).

Day la lop kiem tra dung chung cua repo: hook check_render.py goi che do
--lenient, command /review-video va agent video-reviewer goi che do --strict.

Vi du:
  python scripts/video_qa.py out.mp4 --strict --audio
  python scripts/video_qa.py out.mp4 --source raw.mp4 --cut-authorized

Exit 0 = PASS (hoac WARN), exit 1 = FAIL, exit 2 = khong chay duoc ffprobe.
"""

import argparse
import json
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
        }
    if audio:
        summary["audio"] = {
            "codec": audio.get("codec_name", ""),
            "sample_rate": int(audio.get("sample_rate", 0) or 0),
            "channels": int(audio.get("channels", 0) or 0),
        }
    return summary


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

    if args.audio and "audio" in summary:
        mean = mean_volume_db(artifact)
        if mean is None:
            report.add("audio_level", "WARN", "Khong do duoc muc am")
        elif mean <= -70:
            report.add("audio_level", "FAIL",
                       f"mean_volume {mean} dB — track tieng im lang")
        else:
            report.add("audio_level", "PASS", f"mean_volume {mean} dB")

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
