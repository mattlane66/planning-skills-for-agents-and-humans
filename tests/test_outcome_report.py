"""Validate scorecard rendering from real report-shaped data, including escaping."""
from __future__ import annotations
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "evals"))
from render_report import generate  # noqa: E402


class OutcomeReportTests(unittest.TestCase):
    def test_html_report_renders_auditable_and_escaped_rows(self):
        arm = {
            "safe_task_success_rate": 0.5,
            "invariant_preservation_rate": 1.0,
            "critical_violations": 0,
            "mean_wall_seconds": 2,
            "human_review_minutes_per_success": None,
        }
        report = {
            "protocol": "paired-hidden-artifact-v1",
            "runtime": "codex",
            "model": "fixture",
            "generated_at": "2026-10-07",
            "repeats": 1,
            "summary": {
                "baseline": arm, "skills": arm,
                "absolute_success_rate_difference": 0,
                "mean_wall_time_difference_seconds": 0,
            },
            "results": [
                {"case_id": "<malicious>", "trial": 1, "arm": "baseline",
                 "grade": {"passed": False, "passed_checks": 0, "total_checks": 1,
                           "checks": [{"path": "product/page", "passed": False,
                                      "reason": "<script>alert(1)</script>"}]},
                 "error": None, "wall_seconds": 2}
            ],
            "caveats": ["Only synthetic task outcomes."],
        }
        html = generate(report)
        self.assertIn("Not measured", html)
        self.assertIn("&lt;malicious&gt;", html)
        self.assertNotIn("<script>", html)
        self.assertIn("Only synthetic task outcomes.", html)
        with self.assertRaises(ValueError):
            generate({"protocol": "fixture", "summary": report["summary"]})


if __name__ == "__main__":
    unittest.main()
