#!/usr/bin/env python3
"""One-time migration for runtime-specific skill adapters and validation."""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = [
    line.strip()
    for line in (ROOT / "skill-inventory.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
]

ALIASED_CLAUDE_SKILLS = {
    "framing-doc",
    "shaping",
    "sketch-reconciliation",
    "breadboarding",
    "kickoff-doc",
    "feed-planning-context",
    "breadboard-reflection",
}

DIRECT_CLAUDE_METADATA = {
    "statechart": "[accepted breadboard, selected scope or slice, and optional target statechart file]",
    "interface-contracts": "[selected breadboard or slice, boundary, and optional target contract file]",
    "executable-breadboards": "[selected breadboard, slice, contracts, examples, and optional target file]",
    "dumplink": "[shaping doc, breadboard, selected slice, appetite, or notes]",
}

MANUAL_CLAUDE_COMMANDS = {
    "frame",
    "shape",
    "criteria",
    "appetite",
    "sketch-shapes",
    "fit-check",
    "select-shape",
    "reconcile-sketch",
    "breadboard",
    "statechart",
    "dumplink",
    "kickoff",
    "feed-context",
    "reflect-breadboard",
}


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening frontmatter marker")
    try:
        end = lines[1:].index("---") + 1
    except ValueError as exc:
        raise ValueError("missing closing frontmatter marker") from exc
    raw = "\n".join(lines[1:end])
    data = yaml.safe_load(raw) or {}
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a mapping")
    body = "\n".join(lines[end + 1 :]).lstrip("\n")
    return data, body


def render_frontmatter(data: dict, body: str) -> str:
    header = yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=1000,
    ).rstrip()
    return f"---\n{header}\n---\n\n{body.rstrip()}\n"


def normalize_tools(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        return [item for item in re.split(r"[\s,]+", value.strip()) if item]
    return []


def update_skill_frontmatter() -> None:
    for skill in SKILLS:
        path = ROOT / skill / "SKILL.md"
        data, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        data["license"] = "MIT"
        write(path, render_frontmatter(data, body))


def split_breadboarding_reference() -> None:
    path = ROOT / "breadboarding" / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    marker = "## Catalog of elements and relationships"
    if marker not in text:
        return
    prefix, tail = text.split(marker, 1)
    reference = (
        "# Breadboarding notation, rendering, and slicing reference\n\n"
        "Load this reference only when the work needs the complete element catalog, "
        "chunking rules, output template, Mermaid conventions, or selected-design slicing procedure.\n\n"
        f"## Catalog of elements and relationships{tail.rstrip()}\n"
    )
    write(ROOT / "breadboarding" / "references" / "notation-rendering-and-slicing.md", reference)
    replacement = """## Detailed notation, rendering, and slicing

Read [the notation, rendering, and slicing reference](references/notation-rendering-and-slicing.md) when you need:

- the complete element and relationship catalog
- chunking rules
- the recommended output template
- Mermaid rendering conventions
- selected-design slice creation, sequencing, exit conditions, and appetite cuts

Do not load that reference for a simple current-state map that stops before slicing.
"""
    write(path, prefix.rstrip() + "\n\n" + replacement)


def rewrite_sync_script() -> None:
    write(
        ROOT / "scripts" / "sync-packaged-skills.sh",
        """#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

SKILLS=()
while IFS= read -r skill || [[ -n "$skill" ]]; do
  [[ -n "$skill" ]] && SKILLS+=("$skill")
done < skill-inventory.txt

mode="${1:-sync}"

if [[ "$mode" != "sync" && "$mode" != "--check" ]]; then
  echo "Usage: $0 [sync|--check]" >&2
  exit 2
fi

for skill in "${SKILLS[@]}"; do
  source_dir="$skill"
  packaged_dir="skills/$skill"

  if [[ ! -f "$source_dir/SKILL.md" ]]; then
    echo "Missing canonical skill: $source_dir/SKILL.md" >&2
    exit 1
  fi

  if [[ "$mode" == "--check" ]]; then
    if [[ ! -d "$packaged_dir" ]] || ! diff -qr "$source_dir" "$packaged_dir" >/dev/null; then
      echo "Packaged skill directory is out of sync: $packaged_dir" >&2
      diff -qr "$source_dir" "$packaged_dir" || true
      exit 1
    fi
    echo "✓ $packaged_dir matches $source_dir"
  else
    rm -rf "$packaged_dir"
    mkdir -p "$(dirname "$packaged_dir")"
    cp -R "$source_dir" "$packaged_dir"
    echo "Synced $packaged_dir"
  fi
done
""",
    )


def update_claude_commands() -> None:
    for path in sorted((ROOT / ".claude" / "commands").glob("*.md")):
        data, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        tools = normalize_tools(data.get("allowed-tools"))
        if tools:
            data["allowed-tools"] = tools
        if path.stem in MANUAL_CLAUDE_COMMANDS:
            data["disable-model-invocation"] = True
        else:
            data.pop("disable-model-invocation", None)
        write(path, render_frontmatter(data, body))


def add_frontmatter_helpers() -> None:
    write(
        ROOT / "requirements-dev.txt",
        "PyYAML>=6.0.2,<7\n",
    )
    write(
        ROOT / "scripts" / "frontmatter.py",
        '''#!/usr/bin/env python3
"""Shared YAML-frontmatter utilities for repository validation and packaging."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], list[str], int]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"missing opening frontmatter marker: {path}")
    try:
        end = lines[1:].index("---") + 1
    except ValueError as exc:
        raise ValueError(f"missing closing frontmatter marker: {path}") from exc
    raw = "\\n".join(lines[1:end])
    data = yaml.safe_load(raw) or {}
    if not isinstance(data, dict):
        raise ValueError(f"frontmatter must be a mapping: {path}")
    return data, lines, end


def normalize_tools(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        import re

        return [item for item in re.split(r"[\\s,]+", value.strip()) if item]
    raise ValueError("allowed-tools must be a string or YAML list")
''',
    )
    write(
        ROOT / "scripts" / "validate-frontmatter.py",
        '''#!/usr/bin/env python3
"""Validate portable Agent Skills and Claude-specific command frontmatter."""

from __future__ import annotations

import argparse
from pathlib import Path

from frontmatter import normalize_tools, parse_frontmatter

SKILL_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
CLAUDE_KEYS = {
    "name",
    "description",
    "when_to_use",
    "argument-hint",
    "arguments",
    "disable-model-invocation",
    "user-invocable",
    "allowed-tools",
    "model",
    "effort",
    "context",
    "agent",
    "hooks",
    "paths",
    "shell",
}
KNOWN_TOOLS = {"Read", "Write", "Edit", "Glob", "Grep", "Bash", "Skill"}
MANUAL_COMMANDS = {
    "frame",
    "shape",
    "criteria",
    "appetite",
    "sketch-shapes",
    "fit-check",
    "select-shape",
    "reconcile-sketch",
    "breadboard",
    "statechart",
    "dumplink",
    "kickoff",
    "feed-context",
    "reflect-breadboard",
}


def validate_skill(path: Path) -> None:
    data, lines, _ = parse_frontmatter(path)
    unexpected = sorted(set(data) - SKILL_KEYS)
    if unexpected:
        raise ValueError(f"unexpected portable skill keys in {path}: {', '.join(unexpected)}")
    for required in ("name", "description"):
        if not isinstance(data.get(required), str) or not data[required].strip():
            raise ValueError(f"missing required skill field {required!r}: {path}")
    if path.parent.name != data["name"]:
        raise ValueError(f"skill name must match directory for {path}")
    if len(data["description"]) > 1024:
        raise ValueError(f"skill description exceeds 1024 characters: {path}")
    if data.get("license") != "MIT":
        raise ValueError(f"skill must declare license: MIT: {path}")
    if len(lines) >= 500:
        raise ValueError(f"SKILL.md must stay under 500 lines; split references: {path} ({len(lines)} lines)")
    if "allowed-tools" in data:
        normalize_tools(data["allowed-tools"])


def validate_command(path: Path) -> None:
    data, _, _ = parse_frontmatter(path)
    unexpected = sorted(set(data) - CLAUDE_KEYS)
    if unexpected:
        raise ValueError(f"unexpected Claude command keys in {path}: {', '.join(unexpected)}")
    if not isinstance(data.get("description"), str) or not data["description"].strip():
        raise ValueError(f"missing command description: {path}")
    tools = normalize_tools(data.get("allowed-tools"))
    unknown = sorted(tool for tool in tools if tool.split("(", 1)[0] not in KNOWN_TOOLS)
    if unknown:
        raise ValueError(f"unknown Claude tools in {path}: {', '.join(unknown)}")
    if path.stem in MANUAL_COMMANDS and data.get("disable-model-invocation") is not True:
        raise ValueError(f"human gate command must be manual-only: {path}")
    if path.stem == "check-drift" and data.get("disable-model-invocation") is True:
        raise ValueError(f"check-drift should remain model-invocable: {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", choices=("skill", "command"), required=True)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    if args.kind == "skill":
        validate_skill(args.path)
    else:
        validate_command(args.path)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc
''',
    )
    write(
        ROOT / "scripts" / "annotate-claude-skill.py",
        '''#!/usr/bin/env python3
"""Add Claude Code-only operational metadata to a generated skill copy."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from frontmatter import parse_frontmatter

ALIASED = {
    "framing-doc",
    "shaping",
    "sketch-reconciliation",
    "breadboarding",
    "kickoff-doc",
    "feed-planning-context",
    "breadboard-reflection",
}
DIRECT = {
    "statechart": "[accepted breadboard, selected scope or slice, and optional target statechart file]",
    "interface-contracts": "[selected breadboard or slice, boundary, and optional target contract file]",
    "executable-breadboards": "[selected breadboard, slice, contracts, examples, and optional target file]",
    "dumplink": "[shaping doc, breadboard, selected slice, appetite, or notes]",
}
TOOLS = ["Read", "Write", "Edit", "Glob", "Grep"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("skill")
    args = parser.parse_args()
    data, lines, end = parse_frontmatter(args.path)
    if args.skill in ALIASED:
        data["user-invocable"] = False
    if args.skill in DIRECT:
        data["argument-hint"] = DIRECT[args.skill]
        data["allowed-tools"] = TOOLS
    body = "\\n".join(lines[end + 1 :]).lstrip("\\n")
    header = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=1000).rstrip()
    args.path.write_text(f"---\\n{header}\\n---\\n\\n{body.rstrip()}\\n", encoding="utf-8")


if __name__ == "__main__":
    main()
''',
    )


def update_health_script() -> None:
    path = ROOT / "scripts" / "check-repo-health.sh"
    text = path.read_text(encoding="utf-8")
    start = text.index("check_skill_frontmatter() {")
    end = text.index("SKILLS=()", start)
    replacement = '''check_skill_frontmatter() {
  local file="$1"
  check_file_exists "$file" || return
  if python3 scripts/validate-frontmatter.py --kind skill "$file"; then
    pass "Valid skill frontmatter: $file"
  else
    fail "Invalid skill frontmatter: $file"
  fi
}

check_claude_command_frontmatter() {
  local file="$1"
  check_file_exists "$file" || return
  if python3 scripts/validate-frontmatter.py --kind command "$file"; then
    pass "Valid Claude command frontmatter: $file"
  else
    fail "Invalid Claude command frontmatter: $file"
  fi
}

'''
    text = text[:start] + replacement + text[end:]
    text = text.replace(
        "echo \"Checking uploadable Claude skills...\"",
        "check_file_exists requirements-dev.txt\n\necho \"Checking uploadable Claude skills...\"",
        1,
    )
    text = text.replace(
        "  docs/executable-breadboards.md docs/interface-contracts.md docs/loop-prompting.md",
        "  docs/executable-breadboards.md docs/interface-contracts.md docs/loop-prompting.md\n  docs/runtime-adapters.md docs/skill-activation-testing.md",
    )
    text = text.replace(
        "  check_file_exists dist/claude-code-plugin/hooks/planning-drift-check.sh",
        "  check_file_exists dist/claude-code-plugin/hooks/planning-drift-check.sh\n  check_file_exists dist/claude-code-plugin/skills/breadboarding/references/notation-rendering-and-slicing.md\n  check_file_exists dist/claude-code-plugin/examples/sketch-reconciliation/README.md",
    )
    write(path, text)


def update_build_claude_skills() -> None:
    path = ROOT / "scripts" / "build_claude_skills.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace('SUPPORT_DIRS = ("docs", "templates", "hooks")', 'SUPPORT_DIRS = ("docs", "templates", "hooks", "examples")')
    text = text.replace("import zipfile\n", "import zipfile\n\nimport yaml\n")
    old = '''def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise PackagingError(f"missing opening frontmatter marker: {path}")
    try:
        end = lines[1:].index("---") + 1
    except ValueError as exc:
        raise PackagingError(f"missing closing frontmatter marker: {path}") from exc
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#") or line[0].isspace():
            continue
        if ":" not in line:
            raise PackagingError(f"invalid frontmatter line in {path}: {line!r}")
        key, value = line.split(":", 1)
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            value = json.loads(value)
        fields[key.strip()] = value
    return fields, lines
'''
    new = '''def parse_frontmatter(path: Path) -> tuple[dict[str, object], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise PackagingError(f"missing opening frontmatter marker: {path}")
    try:
        end = lines[1:].index("---") + 1
    except ValueError as exc:
        raise PackagingError(f"missing closing frontmatter marker: {path}") from exc
    try:
        fields = yaml.safe_load("\\n".join(lines[1:end])) or {}
    except yaml.YAMLError as exc:
        raise PackagingError(f"invalid YAML frontmatter in {path}: {exc}") from exc
    if not isinstance(fields, dict):
        raise PackagingError(f"frontmatter must be a mapping: {path}")
    return fields, lines
'''
    if old not in text:
        raise RuntimeError("build_claude_skills.py frontmatter parser marker changed")
    text = text.replace(old, new)
    write(path, text)


def update_build_claude_plugin() -> None:
    path = ROOT / "scripts" / "build-claude-plugin.sh"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        '  "$DIST_DIR/hooks"',
        '  "$DIST_DIR/hooks" \\\n  "$DIST_DIR/examples"',
    )
    text = text.replace(
        'cp "$ROOT_DIR/hooks/"*.sh "$DIST_DIR/hooks/"',
        'cp "$ROOT_DIR/hooks/"*.sh "$DIST_DIR/hooks/"\ncp -R "$ROOT_DIR/examples/." "$DIST_DIR/examples/"',
    )
    text = text.replace(
        '  mkdir -p "$target_dir"\n  sed "${rewrite_args[@]}" "$source_file" > "$target_dir/SKILL.md"',
        '  mkdir -p "$target_dir"\n  cp -R "$ROOT_DIR/$skill/." "$target_dir/"\n  sed "${rewrite_args[@]}" "$source_file" > "$target_dir/SKILL.md"\n  python3 "$ROOT_DIR/scripts/annotate-claude-skill.py" "$target_dir/SKILL.md" "$skill"',
    )
    write(path, text)


def update_ci_workflow() -> None:
    path = ROOT / ".github" / "workflows" / "repo-health.yml"
    text = path.read_text(encoding="utf-8")
    marker = "      - name: Set up Node\n"
    insertion = '''      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install validation dependencies
        run: python -m pip install -r requirements-dev.txt

'''
    if insertion not in text:
        text = text.replace(marker, insertion + marker)
    write(path, text)


def update_codex_manifest() -> None:
    path = ROOT / ".codex-plugin" / "plugin.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    prompts = data["interface"]["defaultPrompt"]
    additions = [
        "Use the breadboard-reflection skill to compare accepted intent with implementation reality and prepare an explicit correction decision.",
        "Use the kickoff-doc skill to create a builder-facing orientation reference from accepted planning artifacts.",
    ]
    for prompt in additions:
        if prompt not in prompts:
            prompts.append(prompt)
    write(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def add_activation_cases() -> None:
    cases = {
        "confusion_pairs": [
            ["framing-doc", "shaping"],
            ["shaping", "breadboarding"],
            ["breadboarding", "statechart"],
            ["interface-contracts", "executable-breadboards"],
            ["kickoff-doc", "feed-planning-context"],
            ["breadboard-reflection", "feed-planning-context"],
            ["dumplink", "breadboarding"],
        ],
        "skills": {
            "framing-doc": {
                "positive": [
                    "Turn these interview notes into a clear problem, outcome, and boundaries before we discuss solutions.",
                    "We have messy stakeholder requests and need a source-grounded frame.",
                ],
                "negative": [
                    "Compare three solution approaches against accepted requirements and appetite.",
                    "Map the selected design into places, affordances, stores, and wiring.",
                ],
            },
            "shaping": {
                "positive": [
                    "Define criteria and appetite, compare alternative shapes, and stop for my selection.",
                    "We have a framed problem but several plausible solution directions.",
                ],
                "negative": [
                    "Extract the current problem and desired outcome from these raw interviews.",
                    "Turn the accepted shape into concrete user and system behavior.",
                ],
            },
            "sketch-reconciliation": {
                "positive": [
                    "Compare this screenshot with the active requirements and propose explicit deltas.",
                    "Reconcile this whiteboard with the selected shape without silently changing scope.",
                ],
                "negative": [
                    "Generate three alternative solution shapes from the accepted criteria.",
                    "Create fixtures and acceptance tests for the selected slice.",
                ],
            },
            "breadboarding": {
                "positive": [
                    "Map how the current product actually behaves from code and screenshots.",
                    "Make the selected design concrete as places, affordances, stores, branches, and wiring.",
                ],
                "negative": [
                    "Derive a transition table for the retry lifecycle in this accepted breadboard.",
                    "Sequence implementation task groups inside the selected slice.",
                ],
            },
            "statechart": {
                "positive": [
                    "Derive states and transitions for retries, timeouts, cancellation, and failure from this accepted breadboard.",
                    "This selected slice has several valid actions from the same state; make the state model reviewable.",
                ],
                "negative": [
                    "Map the overall product into places and affordances.",
                    "Define the request and response fields crossing this API boundary.",
                ],
            },
            "interface-contracts": {
                "positive": [
                    "Define the plain-language input, output, branches, and errors for this UI-to-API boundary.",
                    "The selected slice crosses an agent-to-tool boundary and field-level ambiguity could cause rework.",
                ],
                "negative": [
                    "Add fixtures, example runs, edge cases, and acceptance tests for the entire slice.",
                    "Create a builder-facing overview of the shaped territory.",
                ],
            },
            "executable-breadboards": {
                "positive": [
                    "Turn this selected slice into fixtures, example runs, expected outputs, edge cases, and acceptance tests.",
                    "Prepare a buildable behavioral handoff without implementing code.",
                ],
                "negative": [
                    "Define only the fields and errors at this service boundary.",
                    "Compare alternative shapes before choosing one.",
                ],
            },
            "dumplink": {
                "positive": [
                    "Organize work inside this selected slice into vertical task groups, risks, dependencies, sequence, and cuts.",
                    "We need a bounded agent handoff for one task group inside the accepted slice.",
                ],
                "negative": [
                    "No slice is selected; decide the build sequence anyway.",
                    "Map the selected product behavior before choosing a vertical slice.",
                ],
            },
            "kickoff-doc": {
                "positive": [
                    "Create a durable builder-facing reference organized by the accepted product territory.",
                    "Turn the accepted frame, shape, breadboard, and slice into an orientation document.",
                ],
                "negative": [
                    "Package only the exact context needed by the implementation agent for its next task.",
                    "Create a dependency-aware build sequence.",
                ],
            },
            "feed-planning-context": {
                "positive": [
                    "Package the authoritative planning subset, execution contract, non-goals, and verification target for this implementation task.",
                    "Give the build agent only the context needed for the selected slice and active task group.",
                ],
                "negative": [
                    "Create a broad human-readable kickoff reference for the whole shaped territory.",
                    "Compare implementation reality with the accepted breadboard and diagnose drift.",
                ],
            },
            "breadboard-reflection": {
                "positive": [
                    "Compare the implemented prototype with the accepted breadboard and surface drift before changing either truth.",
                    "Record implementation reality, design smells, and correction options for a human decision.",
                ],
                "negative": [
                    "Package a compact context packet before implementation begins.",
                    "Derive a statechart from an accepted breadboard that has not been implemented.",
                ],
            },
        },
    }
    write(ROOT / "evals" / "skill-activation-cases.json", json.dumps(cases, indent=2, ensure_ascii=False) + "\n")
    write(
        ROOT / "tests" / "test_skill_activation_cases.py",
        '''import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class SkillActivationCaseTests(unittest.TestCase):
    def setUp(self):
        self.inventory = [
            line.strip()
            for line in (ROOT / "skill-inventory.txt").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.cases = json.loads((ROOT / "evals/skill-activation-cases.json").read_text(encoding="utf-8"))

    def test_every_skill_has_activation_cases(self):
        self.assertEqual(set(self.inventory), set(self.cases["skills"]))
        for skill, entry in self.cases["skills"].items():
            self.assertGreaterEqual(len(entry["positive"]), 2, skill)
            self.assertGreaterEqual(len(entry["negative"]), 2, skill)

    def test_cases_are_unique_and_concrete(self):
        seen = set()
        for skill, entry in self.cases["skills"].items():
            for polarity in ("positive", "negative"):
                for case in entry[polarity]:
                    self.assertGreaterEqual(len(case.split()), 8, f"{skill}: {case}")
                    self.assertNotIn(case, seen, case)
                    seen.add(case)

    def test_confusion_pairs_are_valid_and_bidirectionally_covered(self):
        for left, right in self.cases["confusion_pairs"]:
            self.assertIn(left, self.cases["skills"])
            self.assertIn(right, self.cases["skills"])
            self.assertTrue(self.cases["skills"][left]["negative"])
            self.assertTrue(self.cases["skills"][right]["negative"])


if __name__ == "__main__":
    unittest.main()
''',
    )


def add_runtime_tests() -> None:
    write(
        ROOT / "tests" / "test_gemini_commands.py",
        '''import pathlib
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
''',
    )
    write(
        ROOT / "tests" / "test_codex_plugin.py",
        '''import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class CodexPluginTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))

    def test_plugin_is_explicitly_skill_only(self):
        self.assertEqual("./skills/", self.manifest["skills"])
        self.assertEqual(["Read", "Write"], self.manifest["interface"]["capabilities"])
        self.assertNotIn("apps", self.manifest)
        self.assertNotIn("appTemplates", self.manifest)

    def test_default_prompts_cover_every_canonical_skill(self):
        prompt_text = "\n".join(self.manifest["interface"]["defaultPrompt"]).lower()
        for skill in (
            "framing",
            "shaping",
            "sketch-reconciliation",
            "breadboarding",
            "statechart",
            "interface-contracts",
            "executable-breadboards",
            "dumplink",
            "feed-planning-context",
            "breadboard-reflection",
            "kickoff-doc",
        ):
            self.assertIn(skill, prompt_text)


if __name__ == "__main__":
    unittest.main()
''',
    )


def update_docs() -> None:
    write(
        ROOT / "docs" / "runtime-adapters.md",
        """# Runtime adapters

The canonical `SKILL.md` files are the portable method layer. Runtime-specific invocation, permissions, discovery controls, hooks, and packaging belong in adapters.

| Layer | Owns |
|---|---|
| Canonical Agent Skill | `name`, `description`, `license`, optional compatibility/metadata, method, references, examples |
| Claude Code adapter | command aliases, `disable-model-invocation`, `user-invocable`, argument hints, pre-approved tools, plugin-local paths |
| Codex plugin adapter | plugin discovery, skill inventory, display metadata, optional app dependencies |
| Gemini CLI adapter | native skill installation, `GEMINI.md`, TOML command wrappers, Gemini hooks or extension packaging |
| Claude / Claude Design upload | self-contained ZIPs, visual examples, natural-language invocation, repository fallback |
| MCP adapter | callable tools and resources; it does not replace skill instructions |

## Rules

- Do not put Claude-only fields in canonical skill frontmatter.
- Do not assume a skill grants access to an external system. Codex and ChatGPT plugins need an enabled app for that capability.
- Keep command wrappers thin and manual-only when they represent a human decision gate.
- Keep canonical descriptions model-discoverable so compatible runtimes can route to the right method.
- Generate runtime copies from canonical sources and test that they do not drift.
""",
    )
    write(
        ROOT / "docs" / "skill-activation-testing.md",
        """# Skill activation testing

`evals/skill-activation-cases.json` is the shared routing corpus for Claude, Codex, Gemini, Claude Design, and MCP clients.

Each skill has positive requests that should activate it and negative requests that distinguish it from adjacent skills. The automated tests validate inventory coverage and fixture quality. Runtime evaluations should additionally confirm that the actual client:

1. selects the intended skill for every positive case;
2. does not select it for its negative cases;
3. stops at the documented human gate;
4. produces the expected artifact type;
5. does not continue into implementation unless explicitly requested.

Use the same corpus after changing a skill description, renaming a skill, or changing plugin discovery metadata. Record runtime/version and failures rather than treating one client result as universal.
""",
    )

    gemini = ROOT / "docs" / "gemini-usage.md"
    text = gemini.read_text(encoding="utf-8")
    old = "For product work, copy or symlink the needed skill folders into the product repository, or use the MCP adapter."
    new = "For product work, prefer Gemini CLI's native skill management. Install from Git with `gemini skills install https://github.com/mattlane66/planning-skills-for-agents-and-humans`, or link a local checkout with `gemini skills link /path/to/planning-skills-for-agents-and-humans`. Use `gemini skills list`, `enable`, `disable`, and `/skills reload` to inspect or refresh discovery. Copying folders or using the MCP adapter remains a fallback."
    text = text.replace(old, new)
    text = text.replace(
        "## Project commands",
        "## Native skill installation\n\nGemini Agent Skills load the canonical `SKILL.md` instructions and bundled resources on demand. The `.gemini/commands/` files remain focused aliases for explicit gates; they do not replace native skill discovery. Package the repository as a Gemini extension only when you also need Gemini-specific hooks, commands, or MCP configuration.\n\n## Project commands",
    )
    write(gemini, text)

    codex = ROOT / "docs" / "codex-plugin.md"
    text = codex.read_text(encoding="utf-8")
    text = text.replace(
        "## Repo-local marketplace",
        "## Operational boundary\n\nThis is intentionally a skill-only plugin. It guides Codex's existing repository tools but does not grant access to external systems. Add required or optional apps only when the workflow must reach a separate repository service, document store, issue tracker, design system, or other connected source. App permissions and source-system permissions remain authoritative. The optional MCP server in this repository is a separate adapter and is not silently activated by installing the Codex plugin.\n\n## Repo-local marketplace",
    )
    write(codex, text)

    claude_plugin = ROOT / "docs" / "claude-code-plugin.md"
    text = claude_plugin.read_text(encoding="utf-8")
    text = text.replace(
        "Slash commands in `.claude/commands/`, `.claude/loop.md`, lifecycle hooks, and orchestration docs are invocation surfaces around the skills.",
        "Slash commands in `.claude/commands/`, `.claude/loop.md`, lifecycle hooks, and orchestration docs are invocation surfaces around the skills. Human-facing aliases are manual-only, while generated canonical skills remain model-discoverable. Alias-backed canonical skills are hidden from the slash menu to avoid duplicate entries; direct-only skills receive Claude-specific argument hints and conservative file tools during packaging.",
    )
    write(claude_plugin, text)

    install = ROOT / "docs" / "claude-skills-installation.md"
    text = install.read_text(encoding="utf-8")
    text = text.replace(
        "From the repository root, run:\n\n```bash\npython3 scripts/build_claude_skills.py\n```",
        "From the repository root, install the validation dependency and build:\n\n```bash\npython3 -m pip install -r requirements-dev.txt\npython3 scripts/build_claude_skills.py\n```",
    )
    text = text.replace(
        "- includes shared templates, documentation, hooks, and orchestration references used by the skill;",
        "- includes shared templates, documentation, examples, hooks, and orchestration references used by the skill;",
    )
    write(install, text)

    design_tests = ROOT / "docs" / "claude-design-skill-tests.md"
    text = design_tests.read_text(encoding="utf-8")
    if "evals/skill-activation-cases.json" not in text:
        text += "\n## Shared activation corpus\n\nRun the positive and negative cases in `evals/skill-activation-cases.json` after changing descriptions or upload packaging. Claude Design should select the same canonical skill as Claude and should fall back to Claude Code when repository access is required.\n"
    write(design_tests, text)

    ci = ROOT / "docs" / "ci-health-workflow.md"
    text = ci.read_text(encoding="utf-8")
    if "requirements-dev.txt" not in text:
        text += "\n## Validation dependency\n\nThe health workflow installs `requirements-dev.txt` so canonical and Claude-specific frontmatter are parsed as YAML rather than with an ad hoc line parser. Run `python3 -m pip install -r requirements-dev.txt` before `bash scripts/check-repo-health.sh` locally.\n"
    write(ci, text)


def update_changelog() -> None:
    path = ROOT / "CHANGELOG.md"
    text = path.read_text(encoding="utf-8")
    marker = "## Unreleased"
    addition = """

### Improved

- Declared the MIT license in every canonical skill and split breadboarding's detailed notation and slicing material into an on-demand reference.
- Separated portable Agent Skills metadata from Claude Code, Codex, Gemini CLI, Claude Design, and MCP adapter behavior.
- Made Claude human-gate aliases manual-only, hid alias-backed generated skills from duplicate slash-menu discovery, and added operational metadata to direct-only Claude skills.
- Added native Gemini skill installation guidance, Codex skill-only boundary checks, Claude Design example packaging, and shared activation fixtures across all skills.
- Replaced ad hoc frontmatter parsing with YAML validation and added runtime adapter regression tests.
"""
    if "Declared the MIT license in every canonical skill" not in text:
        text = text.replace(marker, marker + addition, 1)
    write(path, text)


def main() -> None:
    update_skill_frontmatter()
    split_breadboarding_reference()
    rewrite_sync_script()
    update_claude_commands()
    add_frontmatter_helpers()
    update_health_script()
    update_build_claude_skills()
    update_build_claude_plugin()
    update_ci_workflow()
    update_codex_manifest()
    add_activation_cases()
    add_runtime_tests()
    update_docs()
    update_changelog()


if __name__ == "__main__":
    main()
