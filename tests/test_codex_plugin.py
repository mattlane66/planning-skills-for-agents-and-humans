import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class CodexPluginTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))

    def test_plugin_is_explicitly_skill_only(self):
        self.assertEqual("./skills/", self.manifest["skills"])
        self.assertEqual(["Read", "Write"], self.manifest["interface"]["capabilities"])
        self.assertNotIn("apps", self.manifest)
        self.assertNotIn("appTemplates", self.manifest)

    def test_default_prompts_cover_every_canonical_skill(self):
        prompt_text = chr(10).join(self.manifest["interface"]["defaultPrompt"]).lower()
        for skill in (
            "framing-doc",
            "shaping",
            "sketch-reconciliation",
            "breadboarding",
            "statechart",
            "interface-contracts",
            "executable-breadboards",
            "dumplink",
            "feed-planning-context",
            "breadboard-reflection",
            "kickoff-doc",
        ):
            self.assertIn(skill, prompt_text)


if __name__ == "__main__":
    unittest.main()
