#!/usr/bin/env python3
"""Test cho data-contracts/.

Kiem tra schema hop le va cac vi du trong examples/ khop schema.
Ten file vi du (kebab-case) anh xa sang ten $defs (PascalCase):
test-report.json -> TestReport.

Can jsonschema. Khong co thi test tu skip.
"""

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = REPO_ROOT / "data-contracts"
EXAMPLES = CONTRACTS / "examples"

try:
    import jsonschema
except ImportError:
    jsonschema = None


def def_name_from(filename: str) -> str:
    return "".join(part.capitalize() for part in Path(filename).stem.split("-"))


def load_schemas() -> dict[str, dict]:
    return {path.name: json.loads(path.read_text(encoding="utf-8"))
            for path in sorted(CONTRACTS.glob("*.schema.json"))}


class TestSchemas(unittest.TestCase):
    def test_co_du_hai_schema(self):
        self.assertEqual(sorted(load_schemas()), ["app.schema.json", "video.schema.json"])

    def test_schema_hop_le(self):
        if jsonschema is None:
            self.skipTest("khong co jsonschema")
        for name, schema in load_schemas().items():
            with self.subTest(schema=name):
                jsonschema.Draft202012Validator.check_schema(schema)

    def test_co_du_cac_buoc_trong_chuoi(self):
        schemas = load_schemas()
        self.assertEqual(
            sorted(schemas["app.schema.json"]["$defs"]),
            ["FeatureRequest", "ImplementationPlan", "ImplementationResult",
             "ReviewReport", "TestReport"])
        self.assertEqual(
            sorted(schemas["video.schema.json"]["$defs"]),
            ["EditPlan", "RenderResult", "VideoAnalysis", "VideoInput",
             "VideoQAReport"])


class TestExamples(unittest.TestCase):
    def setUp(self):
        self.schemas = load_schemas()
        self.examples = sorted(EXAMPLES.glob("*.json"))

    def test_co_vi_du(self):
        self.assertTrue(self.examples, "Phai co it nhat mot vi du")

    def test_vi_du_khop_schema(self):
        if jsonschema is None:
            self.skipTest("khong co jsonschema")
        for path in self.examples:
            with self.subTest(example=path.name):
                target = def_name_from(path.name).lower()
                found = next(
                    ((s, key) for s in self.schemas.values() for key in s["$defs"]
                     if key.lower() == target), None)
                self.assertIsNotNone(
                    found, f"Khong schema nao dinh nghia $defs cho '{path.name}'")
                schema, def_name = found
                jsonschema.validate(
                    instance=json.loads(path.read_text(encoding="utf-8")),
                    schema={"$ref": f"#/$defs/{def_name}", "$defs": schema["$defs"]})


class TestQuyTacKhongPassGia(unittest.TestCase):
    """Schema phai ep buoc rule 'NO TEST = NO PASS'."""

    def setUp(self):
        if jsonschema is None:
            self.skipTest("khong co jsonschema")
        self.defs = load_schemas()["app.schema.json"]["$defs"]

    def validate_report(self, instance):
        jsonschema.validate(instance=instance,
                            schema={"$ref": "#/$defs/TestReport", "$defs": self.defs})

    def test_pass_thieu_command_bi_tu_choi(self):
        with self.assertRaises(jsonschema.ValidationError):
            self.validate_report({"results": [{"stage": "build", "status": "PASS"}]})

    def test_not_run_thieu_ly_do_bi_tu_choi(self):
        with self.assertRaises(jsonschema.ValidationError):
            self.validate_report({"results": [{"stage": "build", "status": "NOT_RUN"}]})

    def test_trang_thai_la_khong_hop_le(self):
        with self.assertRaises(jsonschema.ValidationError):
            self.validate_report({"results": [{"stage": "build", "status": "ALL_PASS"}]})

    def test_pass_du_thong_tin_thi_hop_le(self):
        self.validate_report({"results": [
            {"stage": "build", "status": "PASS",
             "command": "npm run build", "exit_code": 0}]})


class TestVideoQAReportKhopScript(unittest.TestCase):
    """VideoQAReport do scripts/video_qa.py sinh ra phai khop schema."""

    def test_vi_du_that_tu_script(self):
        if jsonschema is None:
            self.skipTest("khong co jsonschema")
        path = EXAMPLES / "video-qa-report.json"
        if not path.exists():
            self.skipTest("chua co vi du video-qa-report.json")
        defs = load_schemas()["video.schema.json"]["$defs"]
        report = json.loads(path.read_text(encoding="utf-8"))
        jsonschema.validate(instance=report,
                            schema={"$ref": "#/$defs/VideoQAReport", "$defs": defs})
        self.assertIn(report["status"], ("PASS", "WARN", "FAIL"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
