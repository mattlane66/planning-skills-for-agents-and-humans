import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class CodexPluginTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        portable = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.public_interface = portable["extensions"]["com.openai"]["interface"]

    def test_plugin_is_explicitly_skill_only(self):
        self.assertEqual("./skills/", self.manifest["skills"])
        self.assertNotIn("apps", self.manifest)
        self.assertNotIn("appTemplates", self.manifest)

    def test_public_listing_metadata_stays_aligned(self):
        self.assertEqual(self.public_interface, self.manifest["interface"])
        prompts = self.manifest["interface"]["defaultPrompt"]
        self.assertEqual(3, len(prompts))
        for prompt in prompts:
            self.assertLessEqual(len(prompt), 128)


if __name__ == "__main__":
    unittest.main()
