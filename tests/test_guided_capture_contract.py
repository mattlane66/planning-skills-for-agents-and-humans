"""Regression checks for guided whiteboard capture's authority contracts."""
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")

class GuidedCaptureTests(unittest.TestCase):
    def test_discoverability_and_no_extra_skill(self):
        for path in ("README.md", "docs/start-here.md", "planning-router/SKILL.md"):
            self.assertIn("guided-whiteboard-capture.md", read(path), path)
        self.assertNotIn("guided-whiteboard-capture", read("skill-inventory.txt"))

    def test_provenance_and_authority(self):
        recipe = read("docs/guided-whiteboard-capture.md")
        for term in ("VISIBLE", "NARRATED", "CODE/OBSERVED", "INFERRED/OPEN",
                     "canonical", "candidate-shape", "selected-design", "private", "human"):
            self.assertIn(term, recipe)

    def test_audio_optional_without_fake_transcription(self):
        recipe = read("docs/guided-whiteboard-capture.md")
        self.assertIn("typed", recipe)
        self.assertIn("Do **not** claim to have heard speech", recipe)

    def test_mirrored_skill_contracts(self):
        for skill in ("planning-router", "shaping", "breadboarding",
                      "sketch-reconciliation", "planning-change-reconciliation"):
            canonical = read(f"{skill}/SKILL.md")
            self.assertIn("guided whiteboard", canonical.lower(), skill)
            self.assertEqual(canonical, read(f"skills/{skill}/SKILL.md"), skill)

    def test_example_ids_and_unknowns(self):
        text = read("examples/guided-whiteboard-capture/02-candidate-breadboard.md")
        for item in ("P1", "P2", "U1", "U2", "N1", "S1", "U3", "UNKNOWN", "TOUR-2"):
            self.assertIn(item, text)
        self.assertIn("candidate-shape", text)

    def test_revision_is_pending(self):
        text = read("examples/guided-whiteboard-capture/03-private-review.md")
        for item in ("PENDING", "new U4", "accept / revise / reject / defer",
                     "No decision was recorded"):
            self.assertIn(item, text)

    def test_coordinated_version(self):
        for path in ("plugin.json", ".claude-plugin/plugin.json",
                     ".codex-plugin/plugin.json", "mcp-server/package.json",
                     "mcp-server/package-lock.json"):
            self.assertEqual("1.7.0", json.loads(read(path))["version"], path)
        lock = json.loads(read("mcp-server/package-lock.json"))
        self.assertEqual("1.7.0", lock["packages"][""]["version"])
        self.assertEqual(1, read("CHANGELOG.md").count("## v1.7.0 —"))

if __name__ == "__main__":
    unittest.main()
