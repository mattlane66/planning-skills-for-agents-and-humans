#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

missing=0

require_text() {
  local file="$1"
  local text="$2"
  if grep -Fq "$text" "$file"; then
    echo "✓ $file contains $text"
  else
    echo "✗ $file missing $text" >&2
    missing=$((missing + 1))
  fi
}

require_text templates/context-packet.md "## Execution contract"
require_text templates/context-packet.md "Goal condition"
require_text templates/context-packet.md "Kickoff doc, for builder orientation only"
require_text templates/frame.md "## Current situation"
require_text framing-doc/SKILL.md "current approach, workaround"
require_text templates/dumplink.md "## Task groups"
require_text templates/dumplink.md "## Scope cuts"
require_text templates/statechart.md "## Transition table"
require_text templates/statechart.md "breadboard tables remain authoritative"
require_text mcp-server/src/index.ts "templates/context-packet.md"
require_text mcp-server/src/index.ts "templates/dumplink.md"
require_text dumplink/SKILL.md "Task groups"
require_text dumplink/SKILL.md "Scope cuts"
require_text statechart/SKILL.md "breadboard tables remain the source of truth"
require_text sketch-reconciliation/SKILL.md "observations before interpretations"
require_text sketch-reconciliation/SKILL.md "Stop at the reconciliation gate"
require_text breadboard-reflection/SKILL.md "explicit drift decision"
require_text breadboard-reflection/SKILL.md "Do not silently rewrite the accepted breadboard"
require_text docs/claude-design-workflow.md "## 4. Set the appetite"
require_text docs/claude-design-workflow.md "they are not accepted breadboards"
require_text .github/workflows/repo-health.yml "set -o pipefail"
require_text scripts/build_claude_skills.py "removeprefix"
require_text tests/test_build_claude_skills.py "test_repo_root_is_never_a_valid_output_directory"
require_text visualizer/test/viewer.test.mjs "malformedVendorPath.status, 400"
require_text .claude/commands/check-drift.md "selected Dumplink task group"
require_text .gemini/commands/check-drift.toml "selected Dumplink task group"
require_text evals/golden/context-packet-execution-contract.md "Execution contract"
require_text evals/golden/dumplink-vertical-groups.md "cluster by judgeable"
require_text evals/golden/statechart-derived-authority.md "breadboard remains authoritative"
require_text evals/golden/sketch-reconciliation-authority.md "Record visible observations before interpretations"
require_text evals/golden/drift-check-strict-output.md "No planning drift found"

if [[ "$missing" -gt 0 ]]; then
  echo "Contract fixture checks failed with $missing missing item(s)." >&2
  exit 1
fi

echo "Contract fixture checks passed."
