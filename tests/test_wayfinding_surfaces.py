import json
import pathlib
import unittest

import tomllib
import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]


class WayfindingSurfaceTests(unittest.TestCase):
    def test_wayfinding_is_registered_and_packaged(self):
        inventory = {
            line.strip()
            for line in (ROOT / "skill-inventory.txt").read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        metadata = json.loads((ROOT / "skill-metadata.json").read_text(encoding="utf-8"))
        cases = json.loads((ROOT / "evals" / "skill-activation-cases.json").read_text(encoding="utf-8"))

        self.assertIn("wayfinding", inventory)
        self.assertIn("wayfinding", metadata)
        self.assertIn("wayfinding", cases["skills"])
        self.assertTrue((ROOT / "wayfinding" / "SKILL.md").is_file())
        self.assertTrue((ROOT / "skills" / "wayfinding" / "SKILL.md").is_file())
        self.assertTrue((ROOT / "templates" / "wayfinding-map.md").is_file())
        self.assertTrue((ROOT / "templates" / "wayfinding-ticket.md").is_file())
        self.assertTrue((ROOT / "wayfinding" / "NOTICE.md").is_file())

    def test_wayfind_commands_are_manual_and_portable(self):
        text = (ROOT / ".claude" / "commands" / "wayfind.md").read_text(encoding="utf-8")
        _, raw, _ = text.split("---", 2)
        data = yaml.safe_load(raw)
        self.assertIs(data["disable-model-invocation"], True)
        self.assertIn("Skill", data["allowed-tools"])

        gemini = tomllib.loads((ROOT / ".gemini" / "commands" / "wayfind.toml").read_text(encoding="utf-8"))
        self.assertIn("wayfinding/SKILL.md", gemini["prompt"])
        self.assertIn("{{args}}", gemini["prompt"])

    def test_wayfinding_remains_coordination_not_product_truth(self):
        text = (ROOT / "wayfinding" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("coordination artifacts, never product truth", text)
        self.assertIn("Never depend on another skills repository at runtime", text)
        self.assertIn("never back to Wayfinding", text)
        self.assertIn("Dumplink decomposes a selected project into sequenced vertical task groups", text)
        for external_dependency in (
            "/grilling",
            "/domain-modeling",
            "/prototype",
            "/research",
            "/setup-matt-pocock-skills",
        ):
            self.assertNotIn(external_dependency, text)


if __name__ == "__main__":
    unittest.main()
