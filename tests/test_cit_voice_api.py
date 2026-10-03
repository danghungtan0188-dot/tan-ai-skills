import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "skills" / "tan-giong-doc-ban-tin" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import cit_voice_api  # noqa: E402


class FakeHeaders:
    def __init__(self, content_type):
        self.content_type = content_type

    def get_content_type(self):
        return self.content_type


class FakeResponse:
    def __init__(self, body=b"ok", content_type="application/json"):
        self.body = body
        self.headers = FakeHeaders(content_type)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.body


class TestURLSafety(unittest.TestCase):
    def test_localhost_duoc_phep(self):
        self.assertEqual(
            cit_voice_api.validate_base_url("http://127.0.0.1:8001", False, None),
            "http://127.0.0.1:8001",
        )

    def test_host_khac_bi_chan_mac_dinh(self):
        with self.assertRaises(cit_voice_api.CitVoiceError):
            cit_voice_api.validate_base_url("http://192.168.1.5:8001", False, None)

    def test_remote_bat_buoc_co_khoa(self):
        with self.assertRaises(cit_voice_api.CitVoiceError):
            cit_voice_api.validate_base_url("http://192.168.1.5:8001", True, None)
        self.assertEqual(
            cit_voice_api.validate_base_url("http://192.168.1.5:8001", True, "secret"),
            "http://192.168.1.5:8001",
        )


class TestRequest(unittest.TestCase):
    @mock.patch("urllib.request.urlopen")
    def test_post_gui_json_utf8_va_api_key(self, urlopen):
        urlopen.return_value = FakeResponse(b"wav", "audio/wav")
        body, content_type = cit_voice_api.request(
            "http://127.0.0.1:8001",
            "/api/tts/generate",
            payload={"text": "Xin chào", "voice_id": "Minh Đức"},
            api_key="abc",
        )
        self.assertEqual(body, b"wav")
        self.assertEqual(content_type, "audio/wav")
        req = urlopen.call_args.args[0]
        self.assertEqual(req.method, "POST")
        self.assertEqual(req.headers["X-api-key"], "abc")
        sent = json.loads(req.data.decode("utf-8"))
        self.assertEqual(sent["text"], "Xin chào")

    @mock.patch("urllib.request.urlopen")
    def test_get_health(self, urlopen):
        urlopen.return_value = FakeResponse(b'{"status":"ok"}')
        body, _ = cit_voice_api.request("http://127.0.0.1:8001", "/health")
        self.assertEqual(json.loads(body), {"status": "ok"})


class TestInput(unittest.TestCase):
    def test_doc_txt_duoc_gop_giu_nguyen_doan(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "script.txt"
            path.write_text("Đoạn một.\n\nĐoạn hai.", encoding="utf-8")
            self.assertEqual(cit_voice_api._read_text(path), "Đoạn một.\n\nĐoạn hai.")


if __name__ == "__main__":
    unittest.main()
