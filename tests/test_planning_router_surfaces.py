import json
import pathlib
import unittest

import tomllib
import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]


class PlanningRouterSurfaceTests(unittest.TestCase):
    def test_router_is_registered_everywhere(self):
        inventory = {
            line.strip()
            for line in (ROOT / "skill-inventory.txt").read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        metadata = json.loads((ROOT / "skill-metadata.json").read_text(encoding="utf-8"))
        cases = json.loads((ROOT / "evals" / "skill-activation-cases.json").read_text(encoding="utf-8"))

        self.assertIn("planning-router", inventory)
        self.assertIn("planning-router", metadata)
        self.assertIn("planning-router", cases["skills"])
        self.assertTrue((ROOT / "planning-router" / "SKILL.md").is_file())
        self.assertTrue((ROOT / "skills" / "planning-router" / "SKILL.md").is_file())

    def test_claude_router_is_manual_only(self):
        text = (ROOT / ".claude" / "commands" / "plan.md").read_text(encoding="utf-8")
        _, raw, _ = text.split("---", 2)
        data = yaml.safe_load(raw)
        self.assertIs(data["disable-model-invocation"], True)
        self.assertIn("Skill", data["allowed-tools"])

    def test_gemini_router_is_valid_toml(self):
        data = tomllib.loads((ROOT / ".gemini" / "commands" / "plan.toml").read_text(encoding="utf-8"))
        self.assertIn("description", data)
        self.assertIn("planning-router/SKILL.md", data["prompt"])

    def test_router_can_recommend_no_planning(self):
        text = (ROOT / "planning-router" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("No planning skill", text)
        self.assertIn("exactly one next move", text)


if __name__ == "__main__":
    unittest.main()
