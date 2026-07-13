#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

missing=0

require_text() {
  local file="$1"
  local text="$2"
  if grep -q "$text" "$file"; then
    echo "✓ $file contains $text"
  else
    echo "✗ $file missing $text" >&2
    missing=$((missing + 1))
  fi
}

require_text templates/context-packet.md "## Execution contract"
require_text templates/context-packet.md "Goal condition"
require_text templates/dumplink.md "## Task groups"
require_text templates/dumplink.md "## Scope cuts"
require_text templates/statechart.md "## Transition table"
require_text templates/statechart.md "breadboard tables remain authoritative"
require_text mcp-server/src/index.ts "templates/context-packet.md"
require_text mcp-server/src/index.ts "templates/dumplink.md"
require_text dumplink/SKILL.md "Task groups"
require_text dumplink/SKILL.md "Scope cuts"
require_text statechart/SKILL.md "breadboard tables remain the source of truth"
require_text .claude/commands/check-drift.md "selected Dumplink task group"
require_text .gemini/commands/check-drift.toml "selected Dumplink task group"
require_text evals/golden/context-packet-execution-contract.md "Execution contract"
require_text evals/golden/dumplink-vertical-groups.md "cluster by judgeable"
require_text evals/golden/statechart-derived-authority.md "breadboard remains authoritative"
require_text evals/golden/drift-check-strict-output.md "No planning drift found"

if [[ "$missing" -gt 0 ]]; then
  echo "Contract fixture checks failed with $missing missing item(s)." >&2
  exit 1
fi

echo "Contract fixture checks passed."
