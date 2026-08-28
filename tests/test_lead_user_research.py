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


    def test_episode_tracing_contract_is_explicit(self):
        protocol = (LEAD / "PROTOCOL.md").read_text(encoding="utf-8")
        phase_c = (LEAD / "prompts" / "phase-c-evidence.md").read_text(encoding="utf-8")
        phase_e = (LEAD / "prompts" / "phase-e-interpret.md").read_text(encoding="utf-8")
        state = (LEAD / "references" / "state-contract.md").read_text(encoding="utf-8")

        self.assertIn("Trace pivotal Lead User episodes", protocol)
        self.assertIn("Episode tracing", phase_c)
        self.assertIn("OBSERVED behavior", phase_c)
        self.assertIn("traced sequence", phase_e)
        self.assertIn("NOT_ASSESSED | PARTIAL | SUFFICIENT", state)

    def test_validator_checks_trace_evidence_references(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = pathlib.Path(tmp) / "study"
            subprocess.run(
                [
                    sys.executable,
                    str(LEAD / "scripts" / "init_study.py"),
                    "--domain", "AI-assisted design workflows",
                    "--decision", "Should we fund a validation sprint?",
                    "--workspace", str(workspace),
                ],
                check=True,
                text=True,
                capture_output=True,
            )

            (workspace / "trends.json").write_text(
                json.dumps([
                    {
                        "trend_id": "T1",
                        "statement": "Workflows span more AI tools",
                        "direction": "increasing",
                        "evidence_refs": ["E1"],
                        "observable_indicators": [],
                        "importance": "material",
                        "status": "VERIFIED",
                    }
                ]),
                encoding="utf-8",
            )
            (workspace / "sources.json").write_text(
                json.dumps([
                    {
                        "source_id": "SRC1",
                        "title": "Primary artifact",
                        "creator": "Example user",
                        "url": "https://example.com",
                        "source_type": "artifact",
                        "coverage": "FULL",
                        "coverage_note": "",
                        "access_date": "2026-08-28",
                    }
                ]),
                encoding="utf-8",
            )
            (workspace / "evidence.json").write_text(
                json.dumps([
                    {
                        "evidence_id": "E1",
                        "source_id": "SRC1",
                        "exact_location": "README",
                        "evidence_type": "behavior",
                        "verbatim_excerpt": "Example",
                        "user_entity": "Example user",
                        "trend_id": "T1",
                        "lu_id": "LU1",
                        "caveat": "",
                    }
                ]),
                encoding="utf-8",
            )

            episode = {
                "lu_id": "LU1",
                "user_entity": "Example user",
                "trend_id": "T1",
                "need_statement": "Recover context across tools",
                "context": "Multi-tool workflow",
                "status": "QUALIFIED",
                "lu1_evidence": ["E1"],
                "lu2_evidence": ["E1"],
                "baseline": "Manual reconstruction",
                "alternatives": [],
                "user_response": "Built a workaround",
                "desired_progress": "Resume work without reconstruction",
                "observed_result": "Workaround used",
                "trace": {
                    "status": "SUFFICIENT",
                    "initiating_condition": "Context was missing",
                    "prior_approach": "Manual reconstruction",
                    "switch_or_change_trigger": "Repeated loss",
                    "expected_improvement": "Faster resumption",
                    "sequence": [
                        {
                            "step_id": "S1",
                            "action": "Reconstruct context",
                            "context": "New session",
                            "result": "Repeated effort",
                            "evidence_refs": ["E1"],
                        }
                    ],
                    "fit_points": [
                        {
                            "step_ref": "S1",
                            "observed_behavior": "Manual reconstruction",
                            "compensating_behavior": "Persistent context artifact",
                            "stated_purpose": None,
                            "inferred_purpose": "Reduce repeated reconstruction",
                            "unknowns": ["Exact time cost"],
                            "evidence_refs": ["E1"],
                        }
                    ],
                    "actual_outcome": "Workaround used",
                    "evidence_refs": ["E1"],
                    "unknowns": [],
                },
                "unknowns": [],
            }
            (workspace / "lu_episodes.json").write_text(
                json.dumps([episode]),
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(LEAD / "scripts" / "validate_study.py"), str(workspace)],
                text=True,
                capture_output=True,
            )
            self.assertEqual(0, result.returncode, result.stderr)

            episode["trace"]["fit_points"][0]["evidence_refs"] = ["E999"]
            (workspace / "lu_episodes.json").write_text(
                json.dumps([episode]),
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(LEAD / "scripts" / "validate_study.py"), str(workspace)],
                text=True,
                capture_output=True,
            )
            self.assertEqual(1, result.returncode)
            self.assertIn("E999", result.stderr)


if __name__ == "__main__":
    unittest.main()
