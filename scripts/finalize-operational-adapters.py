#!/usr/bin/env python3
"""Apply final deterministic corrections after the one-time adapter migration."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def write(path: Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


write(
    ROOT / "tests" / "test_codex_plugin.py",
    '''import json
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
''',
)

path = ROOT / "scripts" / "validate-frontmatter.py"
text = path.read_text(encoding="utf-8")
text = text.replace("if len(lines) >= 500:", "if len(lines) > 500:")
text = text.replace("must stay under 500 lines", "must stay at or below 500 lines")
write(path, text)

path = ROOT / "evals" / "skill-activation-cases.json"
text = path.read_text(encoding="utf-8")
text = text.replace(
    "Compare alternative shapes before choosing one.",
    "Compare three alternative solution shapes against accepted requirements before choosing one.",
)
text = text.replace(
    "Create a dependency-aware build sequence.",
    "Create a dependency-aware implementation sequence for the selected slice.",
)
write(path, text)

path = ROOT / ".codex-plugin" / "plugin.json"
data = json.loads(path.read_text(encoding="utf-8"))
data["interface"]["defaultPrompt"][0] = (
    "Use the framing-doc skill to frame this product idea before implementation."
)
write(path, json.dumps(data, indent=2, ensure_ascii=False))
