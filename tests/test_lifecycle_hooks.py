import json
import pathlib
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class LifecycleHookTests(unittest.TestCase):
    def run_hook(self, name, payload, *, strict=False, cwd=None):
        env = None
        if strict:
            import os

            env = {**os.environ, "PLANNING_HOOK_STRICT": "1"}
        return subprocess.run(
            [str(ROOT / "hooks" / name)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            cwd=cwd or ROOT,
            env=env,
        )

    def test_pre_build_default_emits_claude_visible_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_hook(
                "pre-build-context-check.sh",
                {"tool_name": "Bash", "tool_input": {"command": "npm run build"}},
                cwd=tmp,
            )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("", result.stderr)
        payload = json.loads(result.stdout)
        output = payload["hookSpecificOutput"]
        self.assertEqual("PreToolUse", output["hookEventName"])
        self.assertIn("no compact context packet", output["additionalContext"])

    def test_post_tool_default_emits_claude_visible_json(self):
        result = self.run_hook(
            "planning-drift-check.sh",
            {"tool_name": "Edit", "tool_input": {"file_path": "/tmp/project/src/app.ts"}},
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("", result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual("PostToolUse", payload["hookSpecificOutput"]["hookEventName"])
        self.assertIn("Planning drift check", payload["hookSpecificOutput"]["additionalContext"])

    def test_absolute_planning_paths_do_not_trigger_build_reminders(self):
        payload = {
            "tool_name": "Write",
            "tool_input": {"file_path": "/tmp/project/planning/execution-graph.yaml"},
        }
        for hook in ["pre-build-context-check.sh", "planning-drift-check.sh"]:
            result = self.run_hook(hook, payload)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual("", result.stdout)
            self.assertEqual("", result.stderr)

    def test_strict_mode_blocks_with_stderr_and_no_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_hook(
                "pre-build-context-check.sh",
                {"tool_name": "Bash", "tool_input": {"command": "npm run build"}},
                strict=True,
                cwd=tmp,
            )
        self.assertEqual(2, result.returncode)
        self.assertEqual("", result.stdout)
        self.assertIn("Pre-build context check", result.stderr)


if __name__ == "__main__":
    unittest.main()
