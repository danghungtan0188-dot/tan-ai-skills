#!/usr/bin/env python3
"""Ket noi CIT Voice Studio dang chay cuc bo de tao giong doc.

Khong cai dat, tai model hay khoi dong CIT Voice Studio. Mac dinh chi cho phep
localhost de tranh gui kich ban/giọng ra ngoai y muon.
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_BASE_URL = "http://127.0.0.1:8001"


class CitVoiceError(RuntimeError):
    pass


def _is_loopback(hostname: str | None) -> bool:
    if not hostname:
        return False
    if hostname.lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(hostname).is_loopback
    except ValueError:
        return False


def validate_base_url(base_url: str, allow_remote: bool, api_key: str | None) -> str:
    parsed = urllib.parse.urlparse(base_url.rstrip("/"))
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise CitVoiceError("Base URL phai la dia chi http(s) hop le.")
    if parsed.username or parsed.password:
        raise CitVoiceError("Khong dat thong tin dang nhap trong URL; dung --api-key.")
    if not _is_loopback(parsed.hostname):
        if not allow_remote:
            raise CitVoiceError(
                "Tu choi gui kich ban ra may khac. Chi dung --allow-remote khi ban "
                "da chu dong bat API LAN cua CIT Voice Studio."
            )
        if not api_key:
            raise CitVoiceError("API tu xa bat buoc co --api-key.")
    return base_url.rstrip("/")


def request(
    base_url: str,
    path: str,
    *,
    payload: dict[str, Any] | None = None,
    api_key: str | None = None,
    timeout: float = 120.0,
) -> tuple[bytes, str]:
    headers = {"Accept": "application/json, audio/wav, audio/mpeg, application/octet-stream"}
    if api_key:
        headers["X-API-Key"] = api_key
    data = None
    method = "GET"
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"
        method = "POST"
    req = urllib.request.Request(base_url + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read(), response.headers.get_content_type()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:1000]
        raise CitVoiceError(f"CIT Voice Studio tra ve HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise CitVoiceError(
            f"Khong ket noi duoc CIT Voice Studio tai {base_url}: {exc.reason}. "
            "Hay mo ung dung va kiem tra cong trong Cai dat."
        ) from exc


def _print_json(body: bytes) -> None:
    try:
        value = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CitVoiceError("May chu khong tra ve JSON hop le.") from exc
    print(json.dumps(value, ensure_ascii=False, indent=2))


def _read_text(path: Path) -> str:
    scripts_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(scripts_dir))
    import read_script

    try:
        return "\n\n".join(read_script.read_script(path))
    except read_script.ScriptReadError as exc:
        raise CitVoiceError(str(exc)) from exc


def _main() -> int:
    parser = argparse.ArgumentParser(description="Goi API cuc bo cua CIT Voice Studio.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--api-key", default=None, help="Khoa API khi goi may khac trong LAN")
    parser.add_argument(
        "--allow-remote",
        action="store_true",
        help="Cho phep goi host khong phai localhost; van bat buoc --api-key",
    )
    parser.add_argument("--timeout", type=float, default=120.0)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("health", help="Kiem tra may chu va kha nang mo hinh")
    sub.add_parser("voices", help="Liet ke cac giong CIT dang co")

    generate = sub.add_parser("generate", help="Tao WAV/MP3 tu TXT/DOCX")
    generate.add_argument("--input", required=True)
    generate.add_argument("--voice", required=True, help="voice_id tra ve tu lenh voices")
    generate.add_argument("--output", required=True, help="File dich .wav hoac .mp3")
    generate.add_argument("--language", default=None, help="Vi du vi, en, ja; bo trong cho VieNeu")

    args = parser.parse_args()
    try:
        base_url = validate_base_url(args.base_url, args.allow_remote, args.api_key)
        if args.command == "health":
            body, _ = request(base_url, "/health", api_key=args.api_key, timeout=args.timeout)
            _print_json(body)
            return 0
        if args.command == "voices":
            body, _ = request(base_url, "/voices", api_key=args.api_key, timeout=args.timeout)
            _print_json(body)
            return 0

        output = Path(args.output)
        if output.suffix.lower() not in {".wav", ".mp3"}:
            raise CitVoiceError("--output phai co duoi .wav hoac .mp3.")
        payload: dict[str, Any] = {
            "text": _read_text(Path(args.input)),
            "voice_id": args.voice,
            "format": output.suffix.lower().lstrip("."),
        }
        if args.language:
            payload["language"] = args.language
        body, content_type = request(
            base_url,
            "/api/tts/generate",
            payload=payload,
            api_key=args.api_key,
            timeout=args.timeout,
        )
        if content_type == "application/json":
            try:
                detail = json.loads(body.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                detail = body.decode("utf-8", errors="replace")[:1000]
            raise CitVoiceError(f"API tra ve JSON thay vi audio: {detail}")
        if not body:
            raise CitVoiceError("API tra ve file rong.")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(body)
        print(f"Da luu audio: {output} ({len(body)} byte)")
        return 0
    except CitVoiceError as exc:
        print(f"LOI: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(_main())
