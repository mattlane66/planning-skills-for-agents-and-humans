import pathlib
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
DRIFT_FIELDS = (
    "Selected artifact says",
    "Current implementation direction is",
    "Risk",
    "Recommended move",
)
STRICT_SURFACES = (
    "AGENTS.md",
    "templates/drift-check.md",
    "docs/agent-context-feeding.md",
    ".claude/commands/check-drift.md",
    ".gemini/commands/check-drift.toml",
    "evals/golden/drift-check-strict-output.md",
)


class DriftContractTests(unittest.TestCase):
    def test_strict_surfaces_match_the_orchestration_manifest(self):
        manifest = yaml.safe_load((ROOT / ".agent-orchestration.yaml").read_text(encoding="utf-8"))
        response_shape = manifest["modes"]["check_drift"]["required_response_shape"]

        self.assertEqual("No planning drift found.", response_shape["no_drift"])
        self.assertEqual(list(DRIFT_FIELDS), response_shape["drift"])

        for relative_path in STRICT_SURFACES:
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            self.assertIn(response_shape["no_drift"], text, relative_path)
            self.assertIn("Planning drift found:", text, relative_path)
            for field in DRIFT_FIELDS:
                self.assertIn(field, text, relative_path)

    def test_strict_surfaces_do_not_use_the_reflection_response(self):
        for relative_path in ("AGENTS.md", "docs/agent-context-feeding.md"):
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            self.assertNotIn("The implementation reality is:", text, relative_path)
            self.assertNotIn("Options:\n1.", text, relative_path)


if __name__ == "__main__":
    unittest.main()
