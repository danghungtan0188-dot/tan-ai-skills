#!/usr/bin/env python3
"""Test cho kien truc: agents, commands, hooks, skills, rules.

Bat cac loi thuc te: frontmatter sai, ten agent lech ten file, hook tro toi
script khong ton tai, lien ket den rules/ hoac data-contracts/ bi hong,
skill chua dong bo.
"""

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTS = REPO_ROOT / ".claude" / "agents"
COMMANDS = REPO_ROOT / ".claude" / "commands"
HOOKS = REPO_ROOT / ".claude" / "hooks"
SETTINGS = REPO_ROOT / ".claude" / "settings.json"
RULES = REPO_ROOT / "rules"

# Thu muc cap repo ma cac file .md duoc phep tro toi (duong dan tinh tu goc repo).
REPO_LEVEL_PREFIXES = ("rules/", "data-contracts/", "scripts/", "skills/", "tests/")

LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    _, _, rest = text.partition("---")
    block, sep, _ = rest.partition("\n---")
    if not sep:
        return {}
    data, key = {}, None
    for line in block.splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            key = match.group(1)
            data[key] = match.group(2).strip()
        elif key and line.strip():
            data[key] = f"{data[key]} {line.strip()}".strip()
    return data


class TestAgents(unittest.TestCase):
    def setUp(self):
        self.files = sorted(AGENTS.glob("*.md"))

    def test_co_agent(self):
        self.assertTrue(self.files, f"Khong co agent nao trong {AGENTS}")

    def test_frontmatter_hop_le(self):
        for path in self.files:
            with self.subTest(agent=path.name):
                data = parse_frontmatter(path)
                self.assertIn("name", data, "Thieu truong name")
                self.assertIn("description", data, "Thieu truong description")
                self.assertEqual(data["name"], path.stem,
                                 "name phai trung ten file")
                self.assertGreater(len(data["description"]), 40,
                                   "description qua ngan de Claude chon dung agent")

    def test_ten_agent_khong_trung(self):
        names = [parse_frontmatter(p).get("name") for p in self.files]
        self.assertEqual(len(names), len(set(names)), "Co agent trung ten")

    def test_co_du_hai_nhanh(self):
        names = {p.stem for p in self.files}
        self.assertIn("orchestrator", names)
        self.assertTrue({"app-planner", "app-builder", "app-tester"} <= names,
                        "Thieu agent nhanh APP")
        self.assertTrue({"video-analyzer", "video-editor", "video-reviewer"} <= names,
                        "Thieu agent nhanh VIDEO")


class TestCommands(unittest.TestCase):
    def setUp(self):
        self.files = sorted(COMMANDS.glob("*.md"))

    def test_co_command(self):
        self.assertTrue(self.files, f"Khong co command nao trong {COMMANDS}")

    def test_frontmatter_co_description(self):
        for path in self.files:
            with self.subTest(command=path.name):
                data = parse_frontmatter(path)
                self.assertIn("description", data,
                              "Command phai co description de hien trong danh sach")
                self.assertGreater(len(data["description"]), 20)

    def test_command_video_goi_dung_agent(self):
        for name, agent in [("video-news.md", "video-analyzer"),
                            ("edit-video.md", "video-editor"),
                            ("review-video.md", "video-reviewer")]:
            with self.subTest(command=name):
                text = (COMMANDS / name).read_text(encoding="utf-8")
                self.assertIn(agent, text, f"{name} phai goi agent {agent}")


class TestHooks(unittest.TestCase):
    def test_settings_hop_le(self):
        self.assertTrue(SETTINGS.is_file(), "Thieu .claude/settings.json")
        json.loads(SETTINGS.read_text(encoding="utf-8"))

    def test_moi_hook_tro_toi_script_co_that(self):
        settings = json.loads(SETTINGS.read_text(encoding="utf-8"))
        commands = [hook["command"]
                    for event in settings.get("hooks", {}).values()
                    for group in event
                    for hook in group.get("hooks", [])]
        self.assertTrue(commands, "settings.json khong khai bao hook nao")
        for command in commands:
            with self.subTest(command=command):
                match = re.search(r"([\w./\\-]+\.py)", command)
                self.assertIsNotNone(match, "Lenh hook phai tro toi mot file .py")
                self.assertTrue((REPO_ROOT / match.group(1)).is_file(),
                                f"Khong tim thay script: {match.group(1)}")

    def test_script_hook_khong_loi_cu_phap(self):
        for path in sorted(HOOKS.glob("*.py")):
            with self.subTest(hook=path.name):
                result = subprocess.run(
                    [sys.executable, "-m", "py_compile", str(path)],
                    capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)


class TestRules(unittest.TestCase):
    def test_co_du_bon_rule(self):
        names = {p.name for p in RULES.glob("*.md")}
        self.assertTrue({"global.md", "security.md", "coding.md", "video.md"} <= names,
                        f"Thieu rule, hien co: {sorted(names)}")

    def test_rule_global_co_quy_tac_no_test_no_pass(self):
        text = (RULES / "global.md").read_text(encoding="utf-8")
        self.assertIn("NO TEST = NO PASS", text)


class TestLienKet(unittest.TestCase):
    """Lien ket toi file cap repo phai ton tai va phai tinh tu goc repo.

    Agent va command duoc nap nhu prompt; khi Claude doc file, cwd la goc repo.
    Dung ../../ se tro ra ngoai repo.
    """

    def markdown_files(self):
        return (sorted(AGENTS.glob("*.md")) + sorted(COMMANDS.glob("*.md"))
                + sorted((REPO_ROOT / "skills" / "phat-trien-app").rglob("*.md")))

    def test_khong_dung_duong_dan_len_cap_tren(self):
        for path in self.markdown_files():
            for target in LINK.findall(path.read_text(encoding="utf-8")):
                with self.subTest(file=path.name, link=target):
                    self.assertFalse(
                        target.startswith("../"),
                        "Phai dung duong dan tinh tu goc repo, khong dung ../")

    def test_lien_ket_cap_repo_ton_tai(self):
        for path in self.markdown_files():
            for target in LINK.findall(path.read_text(encoding="utf-8")):
                if not target.startswith(REPO_LEVEL_PREFIXES):
                    continue
                with self.subTest(file=path.name, link=target):
                    self.assertTrue((REPO_ROOT / target).exists(),
                                    f"Lien ket hong: {target}")

    def test_lien_ket_trong_skill_ton_tai(self):
        skill_root = REPO_ROOT / "skills" / "phat-trien-app"
        for path in sorted(skill_root.rglob("*.md")):
            for target in LINK.findall(path.read_text(encoding="utf-8")):
                if target.startswith(REPO_LEVEL_PREFIXES) or "://" in target:
                    continue
                with self.subTest(file=path.name, link=target):
                    self.assertTrue((path.parent / target).exists(),
                                    f"Lien ket noi bo skill bi hong: {target}")


class TestSkills(unittest.TestCase):
    def test_ten_skill_trung_ten_thu_muc(self):
        for skill in sorted((REPO_ROOT / "skills").iterdir()):
            manifest = skill / "SKILL.md"
            if not manifest.is_file():
                continue
            with self.subTest(skill=skill.name):
                data = parse_frontmatter(manifest)
                self.assertIn("name", data)
                self.assertEqual(data["name"], skill.name,
                                 "name trong SKILL.md phai trung ten thu muc")

    def test_da_dong_bo(self):
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "sync_skills.py"), "--check"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            cwd=REPO_ROOT)
        self.assertEqual(result.returncode, 0,
                         f"Skill chua dong bo:\n{result.stdout}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
