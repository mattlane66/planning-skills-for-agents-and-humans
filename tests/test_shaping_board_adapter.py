import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_shaping_board_data import build


class ShapingBoardAdapterTests(unittest.TestCase):
    def test_existing_accepted_example_remains_read_only(self):
        root = ROOT / "examples/simple-grocery-list"
        before = {p: p.read_bytes() for p in root.glob("*.md")}
        board = build(root)
        self.assertEqual([o["id"] for o in board["options"]], ["A", "B"])
        self.assertEqual(board["pick"], "A")
        self.assertEqual([r["id"] for r in board["reqs"]][:2], ["R0", "R1"])
        self.assertEqual(board["reqs"][0]["status"], "Core goal")
        self.assertIn("A1", board["reqs"][0]["part_refs"].get("A", []))
        self.assertEqual(board["reqs"][0]["auth"], "Accepted")
        self.assertEqual(board["appetiteAuthority"], "Accepted")
        self.assertTrue(board["options"][1]["placeholder"])
        self.assertFalse(board["options"][1]["dsl"])
        self.assertIn("review changes", board["import_note"])
        self.assertEqual(before, {p: p.read_bytes() for p in root.glob("*.md")})

    def test_current_baseline_is_preserved_as_descriptive_evidence(self):
        import shutil
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            source=ROOT/"examples/simple-grocery-list"
            for filename in ("01-frame.md","02-shaping.md"):
                shutil.copy(source/filename,folder/filename)
            shaping=folder/"02-shaping.md"
            shaping.write_text(shaping.read_text(encoding="utf-8").replace(
                "## Fit Check",
                "### CURRENT: Existing manual list\n\n| Part | Mechanism |\n|---|---|\n| CURRENT1 | Handwritten list |\n\n## Fit Check"
            ),encoding="utf-8")
            original=(source/"03-breadboard.md").read_text(encoding="utf-8")
            (folder/"03-current-breadboard.md").write_text(original.replace(
                "mode: selected-design","mode: current-state").replace(
                "Mode: `selected-design`","Mode: `current-state`"),encoding="utf-8")
            board=build(folder)
            baseline=next(o for o in board["options"] if o["id"]=="CURRENT")
            self.assertTrue(baseline["baseline"])
            self.assertFalse(baseline["placeholder"])
            self.assertIn("P1 | place",baseline["dsl"])
            self.assertEqual(board["pick"],"A")

    def test_incomplete_project_fails_without_inventing_shapes(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(SystemExit):
                build(tmp)


if __name__ == "__main__":
    unittest.main()
