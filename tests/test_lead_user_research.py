import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
LEAD = ROOT / "lead-user-research"


class LeadUserResearchInputTests(unittest.TestCase):
    def test_canonical_input_contract_is_visible_at_every_front_door(self):
        labels = [
            "Research Domain / Problem Space",
            "Target Market",
            "What do we want to understand?",
            "What human decision should this research help inform?",
            "Desired innovation altitude",
            "Optional hypotheses",
        ]
        for relative in ["SKILL.md", "QUICKSTART.md", "PORTABLE_PROMPT.md", "study-templates/research-input.md"]:
            body = (LEAD / relative).read_text(encoding="utf-8")
            for label in labels:
                self.assertIn(label, body, f"{relative} missing {label}")

    def test_initializer_preserves_full_research_brief(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = pathlib.Path(tmp) / "study"
            subprocess.run(
                [
                    sys.executable,
                    str(LEAD / "scripts" / "init_study.py"),
                    "--mode", "standard",
                    "--domain", "AI-assisted design workflows",
                    "--target-market", "Professional designers",
                    "--understand", "Which future-facing needs are advanced users already solving?",
                    "--decision", "Should we fund a validation sprint?",
                    "--innovation-altitude", "workflow",
                    "--hypothesis", "Context recovery has unusually high expected benefit",
                    "--hypothesis", "Cross-tool portability may matter",
                    "--workspace", str(workspace),
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            decision = json.loads((workspace / "decision.json").read_text(encoding="utf-8"))
            self.assertEqual("AI-assisted design workflows", decision["domain"])
            self.assertEqual("Professional designers", decision["target_market"])
            self.assertEqual("Which future-facing needs are advanced users already solving?", decision["what_to_understand"])
            self.assertEqual("Should we fund a validation sprint?", decision["decision"])
            self.assertEqual("workflow", decision["innovation_altitude"])
            self.assertEqual(
                ["Context recovery has unusually high expected benefit", "Cross-tool portability may matter"],
                decision["starting_hypotheses"],
            )

    def test_fresh_full_brief_workspace_validates(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = pathlib.Path(tmp) / "study"
            subprocess.run(
                [
                    sys.executable,
                    str(LEAD / "scripts" / "init_study.py"),
                    "--domain", "AI-assisted design workflows",
                    "--target-market", "Professional designers",
                    "--understand", "Which future-facing needs are advanced users already solving?",
                    "--decision", "Should we fund a validation sprint?",
                    "--innovation-altitude", "workflow",
                    "--workspace", str(workspace),
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            result = subprocess.run(
                [sys.executable, str(LEAD / "scripts" / "validate_study.py"), str(workspace)],
                text=True,
                capture_output=True,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("structural validation passed", result.stdout.lower())


if __name__ == "__main__":
    unittest.main()
