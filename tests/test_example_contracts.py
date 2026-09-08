import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class ExampleContractTests(unittest.TestCase):
    def test_templates_and_shaping_examples_show_transformation_frame(self):
        paths = [
            "templates/frame.md",
            "templates/shaping.md",
            "examples/simple-grocery-list/01-frame.md",
            "examples/simple-grocery-list/02-shaping.md",
            "examples/sketch-reconciliation/01-shaping-before.md",
            "examples/sketch-reconciliation/04-shaping-after.md",
            "examples/solution-first-shaping/README.md",
        ]
        for relative in paths:
            body = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("x → f() → y", body, relative)

    def test_selected_breadboard_examples_include_forward_and_reverse_traces(self):
        paths = [
            "examples/simple-grocery-list/03-breadboard.md",
            "examples/existing-codebase-drift/01-intended-breadboard.md",
            "examples/statechart-retry-workflow/01-accepted-breadboard.md",
        ]
        for relative in paths:
            body = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("## Behavior traces", body, relative)
            self.assertIn("## Reverse-trace audit", body, relative)
            self.assertIn("Observable consequence", body, relative)

    def test_repository_owned_examples_use_canonical_slice_run_and_cut_ids(self):
        self.assertIn("| CUT1 |", (ROOT / "dumplink/SKILL.md").read_text(encoding="utf-8"))
        executable = (ROOT / "templates/executable-breadboard.md").read_text(encoding="utf-8")
        self.assertIn("### RUN1", executable)
        self.assertIn("### RUN2", executable)
        self.assertNotIn("### Run 1", executable)
        intended = (ROOT / "examples/existing-codebase-drift/01-intended-breadboard.md").read_text(encoding="utf-8")
        self.assertIn("| V1 |", intended)


if __name__ == "__main__":
    unittest.main()
