"""Tests for paired benchmark corpus, graders, and metrics (no model credentials)."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "evals"))
from graders.outcome import grade_case, load_cases, validate_cases, within  # noqa: E402
from metrics import compare  # noqa: E402


class OutcomeBenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = load_cases(ROOT / "evals/benchmarks/cases.json")

    def test_twelve_cases_four_per_category(self):
        self.assertEqual(len(self.cases), 12)
        counts = {category: sum(c["category"] == category for c in self.cases)
                  for category in ("contained", "decision", "handoff")}
        self.assertEqual(counts, {"contained": 4, "decision": 4, "handoff": 4})
        self.assertTrue(all(c["checks"] for c in self.cases))

    def test_duplicate_case_and_unsafe_path_rejected(self):
        with self.assertRaises(ValueError):
            validate_cases(self.cases + [copy.deepcopy(self.cases[0])])
        altered = copy.deepcopy(self.cases[0])
        altered["seed_files"]["../private"] = "secret"
        with self.assertRaises(ValueError):
            validate_cases([altered])

    def test_artifact_not_self_report_is_scored(self):
        case = next(c for c in self.cases if c["id"] == "contained-save-copy")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = within(root, "product/button.txt")
            target.parent.mkdir(parents=True)
            target.write_text("Save item\n")
            self.assertFalse(grade_case(case, root)["passed"])
            target.write_text("Save\n")
            self.assertTrue(grade_case(case, root)["passed"])
            (root / "planning").mkdir()
            result = grade_case(case, root)
            self.assertFalse(result["passed"])
            self.assertTrue(result["critical_violation"])

    def test_json_checks_respect_bool_not_numeric(self):
        case = next(c for c in self.cases if c["id"] == "contained-config-title")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = within(root, "product/config.json")
            target.parent.mkdir(parents=True)
            target.write_text(json.dumps({"tab_title": "Your profile", "analytics_enabled": 0, "retry_limit": 3}))
            grade = grade_case(case, root)
            self.assertFalse(grade["passed"])
            self.assertEqual(grade["passed_invariants"], 1)
            target.write_text(json.dumps({"tab_title": "Your profile", "analytics_enabled": False, "retry_limit": 3}))
            self.assertTrue(grade_case(case, root)["passed"])

    def test_real_python_behavior_and_exceptions(self):
        case = next(c for c in self.cases if c["id"] == "handoff-discount-boundary")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = within(root, "product/logic.py")
            target.parent.mkdir(parents=True)
            target.write_text(
                "def subtotal_cents(items):\n    return sum(items)\n\n"
                "def apply_discount(cents, percent):\n"
                "    if not 0 <= percent <= 20: raise ValueError('limit')\n"
                "    return cents * (100 - percent) // 100\n"
            )
            self.assertTrue(grade_case(case, root)["passed"])
            target.write_text("def subtotal_cents(items): return sum(items)\n"
                              "def apply_discount(cents, percent): return cents\n")
            self.assertFalse(grade_case(case, root)["passed"])

    def test_symlink_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "product").symlink_to(Path(temp).parent, target_is_directory=True)
            with self.assertRaises(ValueError):
                within(root, "product/external.py")

    def test_metrics_require_real_human_review_inputs(self):
        def row(arm, passed, wall):
            return {
                "arm": arm, "trial": 1, "case_id": "case-a",
                "wall_seconds": wall, "human_review_minutes": None,
                "grade": {
                    "passed": passed, "critical_violation": not passed,
                    "total_invariants": 2, "passed_invariants": 2 if passed else 1,
                },
                "error": None,
            }
        summary = compare([row("baseline", False, 5), row("skills", True, 7)])
        self.assertEqual(summary["paired_net_successes"], 1)
        self.assertEqual(summary["absolute_success_rate_difference"], 1)
        self.assertEqual(summary["mean_wall_time_difference_seconds"], 2)
        self.assertIsNone(summary["human_effort_difference_minutes_per_success"])
        with self.assertRaises(ValueError):
            compare([row("baseline", False, 5)])

    def test_cli_validation_without_adapter(self):
        result = subprocess.run([sys.executable, str(ROOT / "evals/compare.py"), "--validate"],
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["cases"], 12)

    def test_paired_runner_uses_fixture_command_and_reports_provenance(self):
        # Mechanical adapter exercise ONLY; does not invoke or prove any model quality.
        with tempfile.TemporaryDirectory() as temp:
            temp_path = Path(temp)
            adapter = temp_path / "adapter.py"
            adapter.write_text(
                "import json, pathlib, sys\n"
                "case = json.load(sys.stdin)\n"
                "assert set(case) == {'schema_version', 'id', 'arm', 'prompt'}\n"
                "assert 'checks' not in case and 'expected' not in case\n"
                "p = pathlib.Path('product/button.txt')\n"
                "assert p.read_text() == 'Save item\\n'\n"
                "p.write_text('Save\\n')\n"
            )
            report = temp_path / "report.json"
            result = subprocess.run(
                [sys.executable, str(ROOT / "evals/compare.py"),
                 "--case-id", "contained-save-copy", "--repeats", "1",
                 "--adapter-command", f"{sys.executable} {adapter}",
                 "--report", str(report)],
                text=True, capture_output=True, timeout=90,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(report.read_text())
            self.assertEqual(data["protocol"], "paired-hidden-artifact-v1")
            self.assertEqual(data["summary"]["baseline"]["safe_task_success_rate"], 1)
            self.assertEqual(data["summary"]["skills"]["safe_task_success_rate"], 1)
            self.assertIsNone(data["summary"]["skills"]["human_review_minutes_per_success"])


if __name__ == "__main__":
    unittest.main()
