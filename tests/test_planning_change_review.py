"""Regression checks for the publisher's read-only planning-change review."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from planning_change_review import ReviewError, render_review, write_review  # noqa: E402


class ReviewTests(unittest.TestCase):
    def test_changed_lines_and_escaping(self):
        content = render_review(
            "# Plan\nAccepted R1: one click\n",
            "# Plan\nAccepted R1: <script>alert(1)</script> in one click\n",
            [], "old.md", "new.md",
        )
        self.assertIn("&lt;script&gt;", content)
        self.assertNotIn("<script>", content)
        self.assertIn("<ins>", content)
        self.assertIn('Review only.', content)
        self.assertIn('No classified deltas supplied', content)

    def test_additions_and_deletions(self):
        value = render_review("one\ntwo\n", "one\nthree\n", [], "old", "new")
        self.assertIn("<del>", value)
        self.assertIn("<ins>", value)

    def test_read_only_cli_with_record_and_hash_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            dir_ = Path(tmp)
            base, proposed, output, record = (dir_ / name for name in
                                             ("accepted.md", "proposed.md", "review.html", "record.json"))
            base.write_text("R1 remains in scope\n", encoding="utf-8")
            proposed.write_text("R1 remains; R2 is proposed\n", encoding="utf-8")
            import hashlib
            digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
            record.write_text(json.dumps({
                "base_sha256": digest(base),
                "proposal_sha256": digest(proposed),
                "deltas": [{
                    "id": "D1", "kind": "substantive", "decision": "pending",
                    "summary": "Add R2", "source_refs": ["meeting:42"],
                    "targets": ["R2"]
                }]
            }), encoding="utf-8")
            before = (base.read_bytes(), proposed.read_bytes())
            args = [sys.executable, str(ROOT / "scripts" / "publish-shaped-work.py"),
                    "--review-base", str(base), "--review-proposal", str(proposed),
                    "--review-record", str(record), "--review-output", str(output)]
            check = subprocess.run(args + ["--check"], text=True, capture_output=True)
            self.assertEqual(check.returncode, 0, check.stderr)
            self.assertFalse(output.exists())
            result = subprocess.run(args, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("meeting:42", output.read_text(encoding="utf-8"))
            self.assertEqual(before, (base.read_bytes(), proposed.read_bytes()))
            base.write_text("changed after review\n", encoding="utf-8")
            stale = subprocess.run(args, text=True, capture_output=True)
            self.assertEqual(stale.returncode, 2)
            self.assertIn("Stale review", stale.stderr)

    def test_rejects_invalid_metadata_and_overwriting(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            a, b, rec = (directory / n for n in ("a.md", "b.md", "record.json"))
            a.write_text("a", encoding="utf-8")
            b.write_text("b", encoding="utf-8")
            with self.assertRaises(ReviewError):
                write_review(a, b, a)
            rec.write_text(json.dumps({"deltas": [{
                "id": "D1", "kind": "substantive", "decision": "pending",
                "summary": "Not yet supported", "source_refs": [], "targets": ["R1"]
            }]}), encoding="utf-8")
            with self.assertRaisesRegex(ReviewError, "evidence"):
                write_review(a, b, directory / "review.html", rec)
            self.assertFalse((directory / "review.html").exists())


if __name__ == "__main__":
    unittest.main()
