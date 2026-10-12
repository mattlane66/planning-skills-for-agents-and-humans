import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "product-intent"))
from board_report import build

PACKAGE = {"product_intent":{
    "product": "Example profile editor",
    "planning_records": [{"id":"R3","uid":"requirement:R3","kind":"requirement","status":"accepted",
        "data":{"Requirement":"Failed saves cannot overwrite persisted data"}}],
    "extension_records":[{"id":"INV-1","uid":"extension:INV-1","kind":"invariant","title":"Draft isolation",
        "statement":"Failed saves leave the original profile unchanged","status":"accepted",
        "resolved_refs":["requirement:R3"]}],
    "bindings":[{"intent_id":"INV-1","resolved_intent_uid":"extension:INV-1","confidence":"confirmed",
                 "paths":["src/profile.py"]}],
}}
GATE = {"verdict":"DRIFT","affected":{"INV-1":{"paths":["src/profile.py"],"confirmed":True}},
        "accepted_contract_changes":[],"unmapped_changed_paths":[],
        "bindings_changed":False,"trusted_baseline_missing":False,
        "behavior_checks":{"verdict":"DRIFT","results":[{"scenario":"SC-1","case":"failed-save","status":"DRIFT","intent_ids":["INV-1"]}]}}


class BoardReportTests(unittest.TestCase):
    def test_reports_behavioral_drift_at_product_intent_level(self):
        report = build(PACKAGE, GATE)
        self.assertEqual(report["kind"], "ShapingBoardProductStatus")
        self.assertEqual(report["verdict"], "DRIFT")
        item, = report["impacts"]
        self.assertEqual(item["status"], "DRIFT")
        self.assertEqual(item["id"], "INV-1")
        self.assertEqual(item["refs"], ["R3"])
        self.assertEqual(item["changed_paths"], ["src/profile.py"])
        self.assertEqual(item["scenarios"][0]["case"], "failed-save")

    def test_incomplete_coverage_never_passes(self):
        gate = {**GATE, "verdict":"REVIEW", "behavior_checks":{"verdict":"REVIEW","results":[]}}
        self.assertEqual(build(PACKAGE, gate)["impacts"][0]["status"], "REVIEW")

    def test_changed_accepted_contract_requires_review_even_if_tests_pass(self):
        gate = {**GATE, "verdict":"REVIEW","accepted_contract_changes":["extension:INV-1"],
                "behavior_checks":{"verdict":"PASS","results":[{"scenario":"SC-1","case":"passed",
                    "status":"PASS","intent_ids":["INV-1"]}]}}
        report = build(PACKAGE, gate)
        self.assertIn("REVIEW", {x["status"] for x in report["impacts"]})

    def test_unmapped_changes_remain_visible(self):
        gate = {**GATE, "verdict":"REVIEW","affected":{},"unmapped_changed_paths":["src/unknown.py"],
                "behavior_checks":{"verdict":"REVIEW","results":[]}}
        report = build(PACKAGE, gate)
        self.assertEqual(report["unmapped_changed_paths"], ["src/unknown.py"])
        self.assertEqual(report["verdict"], "REVIEW")

    def test_never_accepts_an_uncompiled_or_fabricated_pass(self):
        with self.assertRaises(ValueError):
            build({}, GATE)
        with self.assertRaises(ValueError):
            build(PACKAGE, {"verdict":"SURELY_FINE"})

if __name__=="__main__":
    unittest.main()
