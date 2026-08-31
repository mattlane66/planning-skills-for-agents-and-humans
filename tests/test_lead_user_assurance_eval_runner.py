import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "run-lead-user-assurance-evals.py"


class LeadUserAssuranceEvalRunnerTests(unittest.TestCase):
    def test_reference_fixture_exercises_every_artifact_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            report_path = pathlib.Path(tmp) / "report.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--adapter",
                    "fixture",
                    "--runtime",
                    "unit-test",
                    "--model",
                    "reference",
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
            self.assertEqual("reference-fixture-v1", report["protocol"])
            self.assertEqual({"passed": 1, "failed": 0, "total": 1}, report["summary"])
            checks = report["cases"][0]["checks"]
            self.assertGreaterEqual(len(checks), 14)
            self.assertTrue(all(check["passed"] for check in checks))

    def test_command_adapter_cannot_pass_by_self_reporting_without_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = pathlib.Path(tmp)
            adapter = temp_root / "adapter.py"
            report_path = temp_root / "report.json"
            adapter.write_text(
                """
import json
import sys

payload = json.load(sys.stdin)
assert set(payload) == {"schema_version", "id", "prompt"}
print(json.dumps({
    "model_output": "I completed and validated every requested artifact.",
    "evidence": ["all checks passed"],
    "selected_skill": "lead-user-research",
}))
""".lstrip(),
                encoding="utf-8",
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--adapter",
                    "command",
                    "--adapter-command",
                    f"{sys.executable} {adapter}",
                    "--report",
                    str(report_path),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(1, completed.returncode, completed.stderr)
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual("blind-artifact-v1", report["protocol"])
            self.assertEqual(1, report["summary"]["failed"])
            self.assertIn("required-artifacts", report["cases"][0]["failures"][0])

    def test_command_adapter_cannot_relabel_reference_fixture_as_real_runtime_work(self):
        reference = ROOT / "lead-user-research" / "examples" / "reference-study"
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = pathlib.Path(tmp)
            adapter = temp_root / "copy_fixture_adapter.py"
            report_path = temp_root / "report.json"
            adapter.write_text(
                f"""
import json
import os
import pathlib
import shutil
import sys

json.load(sys.stdin)
workspace = pathlib.Path(os.environ["PLANNING_SKILLS_EVAL_WORKSPACE"])
target = workspace / "research" / "lead-user-study"
target.parent.mkdir(parents=True, exist_ok=True)
shutil.copytree({str(reference)!r}, target)
print(json.dumps({{"model_output": "Copied a completed synthetic fixture."}}))
""".lstrip(),
                encoding="utf-8",
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--adapter", "command",
                    "--adapter-command", f"{sys.executable} {adapter}",
                    "--report", str(report_path),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(1, completed.returncode, completed.stderr)
            report = json.loads(report_path.read_text(encoding="utf-8"))
            case = report["cases"][0]
            failures = case["failures"]
            checks = {check["name"]: check for check in case["checks"]}
            self.assertTrue(checks["synthetic-fixture-boundary"]["passed"], checks)
            self.assertFalse(checks["reference-fixture-provenance"]["passed"], checks)
            self.assertTrue(
                any("reference-fixture-provenance" in failure for failure in failures),
                failures,
            )


if __name__ == "__main__":
    unittest.main()
