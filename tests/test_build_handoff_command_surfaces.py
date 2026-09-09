import pathlib
import tomllib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class BuildHandoffCommandSurfaceTests(unittest.TestCase):
    def test_claude_build_handoff_commands_route_to_canonical_skills(self) -> None:
        expected = {
            "contracts.md": ("interface-contracts/SKILL.md", "templates/interface-contracts.md"),
            "executable-breadboard.md": (
                "executable-breadboards/SKILL.md",
                "templates/executable-breadboard.md",
            ),
        }
        for filename, required_refs in expected.items():
            path = ROOT / ".claude" / "commands" / filename
            self.assertTrue(path.is_file(), path)
            text = path.read_text(encoding="utf-8")
            self.assertIn("disable-model-invocation: true", text)
            for reference in required_refs:
                self.assertIn(reference, text)

    def test_gemini_build_handoff_commands_parse_and_route_to_canonical_skills(self) -> None:
        expected = {
            "contracts.toml": ("@{interface-contracts/SKILL.md}", "@{templates/interface-contracts.md}"),
            "executable-breadboard.toml": (
                "@{executable-breadboards/SKILL.md}",
                "@{templates/executable-breadboard.md}",
            ),
        }
        for filename, required_refs in expected.items():
            path = ROOT / ".gemini" / "commands" / filename
            self.assertTrue(path.is_file(), path)
            payload = tomllib.loads(path.read_text(encoding="utf-8"))
            self.assertIsInstance(payload.get("description"), str)
            prompt = payload.get("prompt")
            self.assertIsInstance(prompt, str)
            self.assertIn("@{AGENTS.md}", prompt)
            for reference in required_refs:
                self.assertIn(reference, prompt)

    def test_commands_preserve_planning_only_boundary(self) -> None:
        paths = [
            ROOT / ".claude" / "commands" / "contracts.md",
            ROOT / ".claude" / "commands" / "executable-breadboard.md",
            ROOT / ".gemini" / "commands" / "contracts.toml",
            ROOT / ".gemini" / "commands" / "executable-breadboard.toml",
        ]
        for path in paths:
            text = path.read_text(encoding="utf-8").lower()
            self.assertIn("do not", text)
            self.assertTrue(
                "implementation code" in text
                or "proceed into implementation" in text
                or "implementation is explicitly requested" in text,
                path,
            )


if __name__ == "__main__":
    unittest.main()
