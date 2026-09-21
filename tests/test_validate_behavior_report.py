import importlib.util
import json
import pathlib
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-behavior-report.py"

spec = importlib.util.spec_from_file_location("validate_behavior_report", SCRIPT)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


def make_report(protocol="blind-command-v1", adapter="command"):
    return {
        "schema_version": 1,
        "generated_at": "2026-09-21T19:00:00+00:00",
        "cases_file": "evals/workflow-behavior-cases.json",
        "staged_human_decisions_file": "evals/staged-human-decisions.json",
        "staged_human_decision_cases": [],
        "adapter": adapter,
        "protocol": protocol,
        "runtime": "codex",
        "runtime_version": "1.2.3",
        "model": "gpt-test",
        "commit_sha": "a" * 40,
        "summary": {"passed": 1, "failed": 0, "total": 1},
        "cases": [
            {
                "id": "case-one",
                "passed": True,
                "failures": [],
                "result": {
                    "selected_skill": "shaping",
                    "artifact_type": "shaping",
                    "stopped_at_gate": "shape-selection",
                    "implementation_attempted": False,
                    "evidence": ["accepted requirements"],
                    "model_output": '{"selected_skill":"shaping"}',
                    "runtime_metadata": {
                        "provider": "codex",
                        "model": "gpt-test",
                        "runtime_version_output": "codex-cli 1.2.3",
                        "evidence_source": "answer",
                    },
                },
            }
        ],
    }


def write_retained_evidence(root: pathlib.Path, version="codex-cli 1.2.3"):
    evidence = root / "case-one" / ".runtime-eval"
    evidence.mkdir(parents=True)
    (evidence / "public-case.json").write_text(
        json.dumps({"schema_version": 1, "id": "case-one", "prompt": "test"}) + "\n",
        encoding="utf-8",
    )
    (evidence / "metadata.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "provider": "codex",
                "model": "gpt-test",
                "runtime_version_output": version,
                "command": ["codex", "exec"],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (evidence / "provider-stdout.txt").write_text("runtime stdout\n", encoding="utf-8")
    (evidence / "provider-stderr.txt").write_text("", encoding="utf-8")


class BehaviorReportValidationTests(unittest.TestCase):
    def write_report(self, directory: pathlib.Path, payload):
        path = directory / "report.json"
        path.write_text(json.dumps(payload) + "\n", encoding="utf-8")
        return path

    def test_accepts_blind_command_report_with_retained_runtime_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            report = self.write_report(root, make_report())
            artifacts = root / "artifacts"
            write_retained_evidence(artifacts)
            payload = validator.validate_report(
                report,
                artifacts_dir=artifacts,
                expected_runtime="codex",
                expected_model="gpt-test",
                expected_commit="a" * 40,
            )
            self.assertEqual("blind-command-v1", payload["protocol"])

    def test_rejects_fixture_report_as_real_runtime_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            report = self.write_report(root, make_report("fixture-v1", "fake"))
            with self.assertRaisesRegex(
                validator.ReportValidationError,
                "blind-command-v1",
            ):
                validator.validate_report(report)

    def test_rejects_unknown_runtime_version_or_model(self):
        for field in ("runtime_version", "model"):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temporary:
                root = pathlib.Path(temporary)
                payload = make_report()
                payload[field] = "unknown"
                report = self.write_report(root, payload)
                with self.assertRaises(validator.ReportValidationError):
                    validator.validate_report(report)

    def test_rejects_missing_runtime_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            payload = make_report()
            payload["cases"][0]["result"].pop("runtime_metadata")
            report = self.write_report(root, payload)
            with self.assertRaisesRegex(
                validator.ReportValidationError,
                "runtime_metadata is required",
            ):
                validator.validate_report(report)


    def test_rejects_declared_runtime_version_that_does_not_match_observed_cli(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            payload = make_report()
            payload["runtime_version"] = "9.9.9"
            report = self.write_report(root, payload)
            with self.assertRaisesRegex(
                validator.ReportValidationError,
                "observed runtime version does not contain declared runtime_version",
            ):
                validator.validate_report(report)

    def test_rejects_retained_evidence_that_does_not_match_report(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            report = self.write_report(root, make_report())
            artifacts = root / "artifacts"
            write_retained_evidence(artifacts, version="codex-cli 9.9.9")
            with self.assertRaisesRegex(
                validator.ReportValidationError,
                "retained runtime version differs",
            ):
                validator.validate_report(report, artifacts_dir=artifacts)

    def test_rejects_inconsistent_summary(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            payload = make_report()
            payload["summary"] = {"passed": 0, "failed": 1, "total": 1}
            report = self.write_report(root, payload)
            with self.assertRaisesRegex(
                validator.ReportValidationError,
                "summary counts do not match",
            ):
                validator.validate_report(report)


if __name__ == "__main__":
    unittest.main()
