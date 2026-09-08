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

    def test_command_adapter_cannot_replace_the_scoring_validator(self):
        reference = ROOT / "lead-user-research" / "examples" / "reference-study"
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = pathlib.Path(tmp)
            adapter = temp_root / "tamper_validator_adapter.py"
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
sources_path = target / "sources.json"
sources = json.loads(sources_path.read_text(encoding="utf-8"))
sources[0]["access_date"] = "not-an-iso-date"
sources_path.write_text(json.dumps(sources), encoding="utf-8")
staged_validator = workspace / "skills" / "lead-user-research" / "scripts" / "validate_study.py"
staged_validator.write_text("raise SystemExit(0)\\n", encoding="utf-8")
print(json.dumps({{"model_output": "Attempted to replace the staged validator."}}))
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
            checks = {
                check["name"]: check
                for check in json.loads(report_path.read_text(encoding="utf-8"))["cases"][0]["checks"]
            }
            self.assertTrue(checks["trusted-validator-integrity"]["passed"])
            self.assertFalse(checks["deterministic-validator"]["passed"])
            self.assertIn("access_date", checks["deterministic-validator"]["detail"])

    def test_adapter_timeout_is_bounded(self):
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = pathlib.Path(tmp)
            adapter = temp_root / "slow_adapter.py"
            adapter.write_text(
                "import time\ntime.sleep(1)\n",
                encoding="utf-8",
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--adapter", "command",
                    "--adapter-command", f"{sys.executable} {adapter}",
                    "--adapter-timeout-seconds", "0.05",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, completed.returncode)
            self.assertIn("timed out", completed.stderr)

    def test_fixture_artifacts_can_be_retained(self):
        with tempfile.TemporaryDirectory() as tmp:
            artifacts = pathlib.Path(tmp) / "artifacts"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--adapter", "fixture",
                    "--artifacts-dir", str(artifacts),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertTrue(
                (artifacts / "lead-user-v1-7-end-to-end" / "manifest.json").is_file()
            )

    def test_failed_adapter_retains_partial_study_and_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = pathlib.Path(tmp)
            artifacts = temp_root / "artifacts"
            report_path = temp_root / "report.json"
            adapter = temp_root / "failed_adapter.py"
            adapter.write_text(
                "import pathlib, sys\n"
                "root = pathlib.Path('research/lead-user-study')\n"
                "root.mkdir(parents=True)\n"
                "(root / 'partial.txt').write_text('partial fixture', encoding='utf-8')\n"
                "sys.exit(3)\n",
                encoding="utf-8",
            )
            completed = subprocess.run(
                [
                    sys.executable, str(RUNNER), "--adapter", "command",
                    "--adapter-command", f"{sys.executable} {adapter}",
                    "--artifacts-dir", str(artifacts), "--report", str(report_path),
                ],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(2, completed.returncode)
            self.assertTrue((artifacts / "lead-user-v1-7-end-to-end" / "partial.txt").is_file())
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(1, report["summary"]["failed"])
            self.assertIn("exit 3", report["cases"][0]["failures"][0])


if __name__ == "__main__":
    unittest.main()
