import copy
import importlib.util
import pathlib
import tempfile
import unittest

BASE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("intent", BASE / "intent.py")
intent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intent)

class IntentTests(unittest.TestCase):
    def setUp(self):
        self.model = intent.load(BASE / "example.json")

    def test_valid(self):
        self.assertEqual(intent.validate(self.model), [])

    def test_requires_human_approval(self):
        m = copy.deepcopy(self.model)
        del m["records"][0]["approved_by"]
        self.assertTrue(any("approved_by" in e for e in intent.validate(m)))

    def test_id_and_binding_validity(self):
        m = copy.deepcopy(self.model)
        m["bindings"][0]["intent_id"] = "UNKNOWN-8"
        self.assertTrue(any("unknown intent ID" in e for e in intent.validate(m)))

    def test_change_fails_review_without_evidence(self):
        r = intent.review(self.model, ["src/profile/Edit.tsx"])
        self.assertEqual(r["verdict"], "REVIEW")
        self.assertEqual(r["findings"][0]["id"], "INV-1")

    def test_pass_with_test_evidence(self):
        r = intent.review(self.model, ["src/profile/Edit.tsx"], evidence={
            "INV-1": {"result": "pass", "tests": ["tests/profile-save.spec.ts"]}
        })
        self.assertEqual(r["verdict"], "PASS")

    def test_accepted_change_is_drift(self):
        after = copy.deepcopy(self.model)
        after["records"][0]["statement"] = "Change accepted contract"
        r = intent.review(after, [], previous=self.model)
        self.assertEqual(r["verdict"], "DRIFT")

    def test_unmapped_requires_review(self):
        self.assertEqual(intent.review(self.model, ["src/unknown.py"])["verdict"], "REVIEW")

    def test_projection(self):
        with tempfile.TemporaryDirectory() as tmp:
            intent.project(self.model, tmp)
            self.assertIn("Draft isolation", (pathlib.Path(tmp)/"qa.md").read_text())
            self.assertIn("Single shared object", (pathlib.Path(tmp)/"decisions.md").read_text())

if __name__ == "__main__":
    unittest.main()
