import pathlib
import tomllib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPECTED = {
    "plan",
    "wayfind",
    "shape",
    "criteria",
    "appetite",
    "sketch-shapes",
    "fit-check",
    "spike",
    "breadboard",
    "select-shape",
    "reconcile-sketch",
    "statechart",
    "dumplink",
    "check-drift",
    "lead-user",
    "lead-user-frame",
    "lead-user-discover",
    "lead-user-evidence",
    "lead-user-freeze",
    "lead-user-interpret",
    "lead-user-shape",
    "lead-user-decide",
    "lead-user-deliver",
}


class GeminiCommandTests(unittest.TestCase):
    def test_command_inventory_and_prompt_contracts(self):
        files = {path.stem: path for path in (ROOT / ".gemini/commands").glob("*.toml")}
        self.assertEqual(EXPECTED, set(files))
        for name, path in files.items():
            data = tomllib.loads(path.read_text(encoding="utf-8"))
            self.assertIsInstance(data.get("description"), str, name)
            prompt = data.get("prompt")
            self.assertIsInstance(prompt, str, name)
            self.assertIn("{{args}}", prompt, name)
            self.assertIn("@{", prompt, name)

    def test_human_gates_and_boundaries_are_explicit(self):
        prompts = {
            path.stem: tomllib.loads(path.read_text(encoding="utf-8"))["prompt"].lower()
            for path in (ROOT / ".gemini/commands").glob("*.toml")
        }
        self.assertIn("exactly one next move", prompts["plan"])
        self.assertIn("multi-session", prompts["wayfind"])
        self.assertIn("do not create production code", prompts["wayfind"])
        self.assertIn("human", prompts["select-shape"])
        self.assertIn("selected project", prompts["dumplink"])
        self.assertIn("vertical implementation slices", prompts["dumplink"])
        self.assertIn("do not implement", prompts["statechart"])
        self.assertIn("do not implement", prompts["check-drift"])
        self.assertIn("one next move", prompts["lead-user"])
        self.assertIn("real sources", prompts["lead-user-evidence"])
        self.assertIn("human acceptance", prompts["lead-user-deliver"])


if __name__ == "__main__":
    unittest.main()
