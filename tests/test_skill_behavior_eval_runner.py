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


if __name__ == "__main__":
    unittest.main()
