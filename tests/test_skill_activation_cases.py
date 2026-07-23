import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class SkillActivationCaseTests(unittest.TestCase):
    def setUp(self):
        self.inventory = [
            line.strip()
            for line in (ROOT / "skill-inventory.txt").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.cases = json.loads((ROOT / "evals/skill-activation-cases.json").read_text(encoding="utf-8"))

    def test_every_skill_has_activation_cases(self):
        self.assertEqual(set(self.inventory), set(self.cases["skills"]))
        for skill, entry in self.cases["skills"].items():
            self.assertGreaterEqual(len(entry["positive"]), 2, skill)
            self.assertGreaterEqual(len(entry["negative"]), 2, skill)

    def test_cases_are_unique_and_concrete(self):
        seen = set()
        for skill, entry in self.cases["skills"].items():
            for polarity in ("positive", "negative"):
                for case in entry[polarity]:
                    self.assertGreaterEqual(len(case.split()), 8, f"{skill}: {case}")
                    self.assertNotIn(case, seen, case)
                    seen.add(case)

    def test_confusion_pairs_are_valid_and_bidirectionally_covered(self):
        for left, right in self.cases["confusion_pairs"]:
            self.assertIn(left, self.cases["skills"])
            self.assertIn(right, self.cases["skills"])
            self.assertTrue(self.cases["skills"][left]["negative"])
            self.assertTrue(self.cases["skills"][right]["negative"])


if __name__ == "__main__":
    unittest.main()
