import pathlib
import tomllib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPECTED = {
    "criteria",
    "appetite",
    "sketch-shapes",
    "fit-check",
    "select-shape",
    "reconcile-sketch",
    "statechart",
    "dumplink",
    "check-drift",
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
        self.assertIn("human", prompts["select-shape"])
        self.assertIn("selected slice", prompts["dumplink"])
        self.assertIn("do not implement", prompts["statechart"])
        self.assertIn("do not implement", prompts["check-drift"])


if __name__ == "__main__":
    unittest.main()
