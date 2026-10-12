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
        self.assertEqual(board["reqs"][0]["auth"], "Accepted")
        self.assertEqual(board["appetiteAuthority"], "Accepted")
        self.assertTrue(board["options"][1]["placeholder"])
        self.assertFalse(board["options"][1]["dsl"])
        self.assertIn("review changes", board["import_note"])
        self.assertEqual(before, {p: p.read_bytes() for p in root.glob("*.md")})

    def test_incomplete_project_fails_without_inventing_shapes(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(SystemExit):
                build(tmp)


if __name__ == "__main__":
    unittest.main()
