from __future__ import annotations

import importlib.util
import json
import os
import pathlib
import tempfile
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[1]
ADAPTER_PATH = ROOT / "adapters" / "runtime_case_adapter.py"
SPEC = importlib.util.spec_from_file_location("runtime_case_adapter", ADAPTER_PATH)
assert SPEC and SPEC.loader
adapter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(adapter)


class RuntimeCaseAdapterTests(unittest.TestCase):
    def test_model_payload_accepts_bare_or_fenced_json(self):
        payload = {
            "selected_skill": "shaping",
            "artifact_type": "shaping",
            "stopped_at_gate": "shape-selection",
            "implementation_attempted": False,
            "evidence": ["human selection remains explicit"],
            "answer": "I would stop before selecting.",
        }
        rendered = json.dumps(payload)
        self.assertEqual(payload, adapter.parse_model_payload(rendered))
        self.assertEqual(payload, adapter.parse_model_payload(f"```json\n{rendered}\n```"))

    def test_model_payload_rejects_malformed_self_report(self):
        with self.assertRaisesRegex(adapter.AdapterError, "missing keys"):
            adapter.parse_model_payload('{"selected_skill":"shaping"}')
        malformed = {
            "selected_skill": "shaping",
            "artifact_type": "shaping",
            "stopped_at_gate": None,
            "implementation_attempted": "no",
            "evidence": [],
            "answer": "answer",
        }
        with self.assertRaisesRegex(adapter.AdapterError, "must be boolean"):
            adapter.parse_model_payload(json.dumps(malformed))

    def test_prompt_marks_only_staged_decisions_as_human_approval(self):
        case = {
            "schema_version": 1,
            "id": "selection",
            "prompt": "Continue the selected design.",
            "staged_human_decisions": [
                "Human decision: Shape A is explicitly selected after review."
            ],
        }
        prompt = adapter.build_model_prompt(case)
        self.assertIn("TRUSTED STAGED HUMAN DECISIONS", prompt)
        self.assertIn("Shape A is explicitly selected", prompt)
        self.assertIn("Never invent a selection", prompt)
        self.assertIn("Return exactly one JSON object", prompt)

    def test_no_decision_prompt_explicitly_denies_implied_approval(self):
        prompt = adapter.build_model_prompt(
            {"schema_version": 1, "id": "no-gate", "prompt": "Compare these options."}
        )
        self.assertIn("No selection, acceptance, promotion, or build approval is implied", prompt)

    def test_provider_commands_preserve_read_only_boundaries(self):
        prompt = "PUBLIC PROMPT"
        claude = adapter.provider_command("claude-code", "model-a", prompt)
        self.assertEqual("claude", claude[0])
        self.assertEqual(".", claude[claude.index("--plugin-dir") + 1])
        self.assertEqual("plan", claude[claude.index("--permission-mode") + 1])
        self.assertIn("--no-session-persistence", claude)
        self.assertIn("--no-chrome", claude)
        self.assertNotIn("--dangerously-skip-permissions", claude)

        codex = adapter.provider_command("codex", "model-b", prompt)
        self.assertEqual(["codex", "exec"], codex[:2])
        self.assertIn("--ephemeral", codex)
        self.assertIn("--ignore-user-config", codex)
        self.assertEqual("read-only", codex[codex.index("--sandbox") + 1])
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", codex)

        gemini = adapter.provider_command("gemini-cli", "model-c", prompt)
        self.assertEqual("json", gemini[gemini.index("--output-format") + 1])
        self.assertIn("--skip-trust", gemini)
        self.assertEqual("activate_skill", gemini[gemini.index("--allowed-tools") + 1])
        self.assertNotIn("--yolo", gemini)
        self.assertNotIn("yolo", gemini)
        self.assertNotIn("auto_edit", gemini)

    def test_codex_and_gemini_get_copied_workspace_skills(self):
        for provider in ("codex", "gemini-cli"):
            with self.subTest(provider=provider), tempfile.TemporaryDirectory() as temporary:
                root = pathlib.Path(temporary)
                skill = root / "skills" / "example"
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text("---\nname: example\n---\n", encoding="utf-8")
                (root / ".agents").mkdir()
                (root / ".agents" / "marker.txt").write_text("keep\n", encoding="utf-8")
                adapter.prepare_workspace(provider, root)
                installed = root / ".agents" / "skills" / "example" / "SKILL.md"
                self.assertTrue(installed.is_file())
                self.assertFalse(installed.is_symlink())
                self.assertEqual("keep\n", (root / ".agents" / "marker.txt").read_text())

    def test_claude_requires_plugin_surface(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            (root / "skills").mkdir()
            with self.assertRaisesRegex(adapter.AdapterError, "plugin.json"):
                adapter.prepare_workspace("claude-code", root)
            manifest = root / ".claude-plugin" / "plugin.json"
            manifest.parent.mkdir()
            manifest.write_text("{}\n", encoding="utf-8")
            adapter.prepare_workspace("claude-code", root)

    def test_provider_output_extractors_use_final_agent_text(self):
        claude_stream = "\n".join(
            [
                json.dumps({"type": "assistant", "message": {"content": [{"type": "text", "text": "first"}]}}),
                json.dumps({"type": "assistant", "message": {"content": [{"type": "text", "text": "final"}]}}),
                json.dumps({"type": "result", "result": "fallback"}),
            ]
        )
        self.assertEqual("final", adapter.extract_claude_response(claude_stream))

        codex_stream = "\n".join(
            [
                json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": "first"}}),
                json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": "final"}}),
            ]
        )
        self.assertEqual("final", adapter.extract_codex_response(codex_stream))
        self.assertEqual(
            "final",
            adapter.extract_gemini_response(json.dumps({"response": "final", "stats": {}})),
        )

    def test_generic_eval_key_is_mapped_only_to_selected_provider(self):
        with mock.patch.dict(
            os.environ,
            {
                "PLANNING_SKILLS_EVAL_API_KEY": "generic-secret",
                "ANTHROPIC_API_KEY": "old-anthropic",
                "OPENAI_API_KEY": "old-openai",
                "GEMINI_API_KEY": "old-gemini",
                "GH_TOKEN": "old-github",
            },
            clear=True,
        ):
            environment = adapter.sanitized_child_environment("codex")
        self.assertEqual("generic-secret", environment["OPENAI_API_KEY"])
        self.assertNotIn("ANTHROPIC_API_KEY", environment)
        self.assertNotIn("GEMINI_API_KEY", environment)
        self.assertNotIn("PLANNING_SKILLS_EVAL_API_KEY", environment)
        self.assertNotIn("GH_TOKEN", environment)

    def test_public_case_rejects_hidden_scorer_fields(self):
        from io import StringIO

        with self.assertRaisesRegex(adapter.AdapterError, "non-public keys"):
            adapter.load_public_case(
                StringIO(
                    json.dumps(
                        {
                            "schema_version": 1,
                            "id": "leak",
                            "prompt": "task",
                            "expected_skill": "shaping",
                        }
                    )
                )
            )


if __name__ == "__main__":
    unittest.main()
