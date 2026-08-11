import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "run-skill-behavior-evals.py"


class SkillBehaviorEvalRunnerTests(unittest.TestCase):
    def test_fake_adapter_passes_complete_corpus(self):
        with tempfile.TemporaryDirectory() as tmp:
            report_path = pathlib.Path(tmp) / "report.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--adapter",
                    "fake",
                    "--runtime",
                    "unit-test",
                    "--runtime-version",
                    "1",
                    "--model",
                    "fixture",
                    "--commit-sha",
                    "test",
                    "--report",
                    str(report_path),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(0, report["summary"]["failed"])
            self.assertEqual(report["summary"]["total"], report["summary"]["passed"])
            self.assertEqual("unit-test", report["runtime"])
            self.assertEqual("fixture-v1", report["protocol"])

    def test_command_adapter_failure_is_reported(self):
        completed = subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--adapter",
                "command",
                "--adapter-command",
                f"{sys.executable} -c 'import sys; sys.exit(3)'",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(2, completed.returncode)
        self.assertIn("adapter command failed", completed.stderr)

    def test_command_adapter_receives_only_public_case_in_isolated_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = pathlib.Path(tmp)
            cases_path = temp_root / "cases.json"
            report_path = temp_root / "report.json"
            adapter_path = temp_root / "adapter.py"
            cases_path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "cases": [
                            {
                                "id": "blind-test",
                                "prompt": "Use the staged breadboarding skill to inspect this causal path.",
                                "expected_skill": "breadboarding",
                                "expected_artifact_type": "breadboard",
                                "expected_gate": "breadboard-verification",
                                "implementation_allowed": False,
                                "required_evidence": ["visible causal trace"],
                                "forbidden_evidence": ["production code"],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            adapter_path.write_text(
                """
import json
import pathlib
import sys

payload = json.load(sys.stdin)
assert set(payload) == {"schema_version", "id", "prompt"}
assert payload["id"] == "blind-test"
assert "expected_skill" not in payload
assert "required_evidence" not in payload
assert not pathlib.Path("evals").exists()
assert not pathlib.Path("tests").exists()
assert not pathlib.Path("docs/skill-behavior-evals.md").exists()
assert not pathlib.Path("docs/claude-design-skill-tests.md").exists()
assert pathlib.Path("skills/breadboarding/SKILL.md").is_file()
assert pathlib.Path("templates/breadboard.md").is_file()

print(json.dumps({
    "selected_skill": "breadboarding",
    "artifact_type": "breadboard",
    "stopped_at_gate": "breadboard-verification",
    "implementation_attempted": False,
    "evidence": ["visible causal trace"],
    "model_output": "The staged skill produced a visible causal trace.",
}))
""".lstrip(),
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--cases",
                    str(cases_path),
                    "--case-id",
                    "blind-test",
                    "--adapter",
                    "command",
                    "--adapter-command",
                    f"{sys.executable} {adapter_path}",
                    "--report",
                    str(report_path),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(0, completed.returncode, completed.stderr)
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual("blind-command-v1", report["protocol"])
            self.assertEqual({"passed": 1, "failed": 0, "total": 1}, report["summary"])

    def test_unknown_case_filter_is_rejected(self):
        completed = subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--case-id",
                "not-a-real-case",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(2, completed.returncode)
        self.assertIn("unknown case id", completed.stderr)


if __name__ == "__main__":
    unittest.main()
