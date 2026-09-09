import json
import os
import pathlib
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
HOOKS = {
    "planning-ripple.sh": "PostToolUse",
    "planning-drift-check.sh": "PostToolUse",
    "pre-build-context-check.sh": "PreToolUse",
}


class HookDependencyTests(unittest.TestCase):
    def run_without_jq(self, hook_name: str, *, strict: bool = False) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["PATH"] = ""
        if strict:
            env["PLANNING_HOOK_STRICT"] = "1"
        else:
            env.pop("PLANNING_HOOK_STRICT", None)
        return subprocess.run(
            [str(ROOT / "hooks" / hook_name)],
            input='{"tool_name":"Bash","tool_input":{"command":"npm test"}}',
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

    def test_missing_jq_is_visible_in_default_mode(self) -> None:
        for hook_name, event_name in HOOKS.items():
            with self.subTest(hook=hook_name):
                completed = self.run_without_jq(hook_name)
                self.assertEqual(0, completed.returncode, completed.stderr)
                payload = json.loads(completed.stdout)
                output = payload["hookSpecificOutput"]
                self.assertEqual(event_name, output["hookEventName"])
                self.assertIn("jq is not installed", output["additionalContext"])
                self.assertIn("guardrail", output["additionalContext"])

    def test_missing_jq_blocks_in_strict_mode(self) -> None:
        for hook_name in HOOKS:
            with self.subTest(hook=hook_name):
                completed = self.run_without_jq(hook_name, strict=True)
                self.assertEqual(2, completed.returncode)
                self.assertEqual("", completed.stdout)
                self.assertIn("jq is not installed", completed.stderr)
                self.assertIn("guardrail", completed.stderr)


if __name__ == "__main__":
    unittest.main()
