import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class SkillBehaviorEvalSchemaTests(unittest.TestCase):
    def setUp(self):
        self.inventory = {
            line.strip()
            for line in (ROOT / "skill-inventory.txt").read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        self.payload = json.loads(
            (ROOT / "evals" / "workflow-behavior-cases.json").read_text(encoding="utf-8")
        )
        self.cases = self.payload["cases"]

    def test_schema_version_and_unique_ids(self):
        self.assertEqual(1, self.payload["schema_version"])
        ids = [case["id"] for case in self.cases]
        self.assertEqual(len(ids), len(set(ids)))

    def test_every_skill_has_behavior_coverage(self):
        covered = {case["expected_skill"] for case in self.cases if case["expected_skill"]}
        self.assertEqual(self.inventory, covered)

    def test_corpus_includes_no_planning_case(self):
        self.assertTrue(any(case["expected_skill"] is None for case in self.cases))

    def test_every_human_gate_case_forbids_implementation(self):
        for case in self.cases:
            if case["expected_gate"] is not None:
                self.assertFalse(case["implementation_allowed"], case["id"])

    def test_required_fields_are_concrete(self):
        required = {
            "id",
            "prompt",
            "expected_skill",
            "expected_artifact_type",
            "expected_gate",
            "implementation_allowed",
            "required_evidence",
            "forbidden_evidence",
        }
        for case in self.cases:
            self.assertEqual(required, set(case), case["id"])
            self.assertGreaterEqual(len(case["prompt"].split()), 8, case["id"])
            self.assertTrue(case["required_evidence"], case["id"])
            self.assertTrue(case["forbidden_evidence"], case["id"])


if __name__ == "__main__":
    unittest.main()
