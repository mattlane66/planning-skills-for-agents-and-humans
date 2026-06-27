#!/usr/bin/env bash
set -euo pipefail

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
require_text mcp-server/src/index.ts "Execution contract"
require_text mcp-server/src/index.ts "dumplink"
require_text dumplink/SKILL.md "Task groups"
require_text dumplink/SKILL.md "Scope cuts"
require_text evals/golden/context-packet-execution-contract.md "Execution contract"
require_text evals/golden/dumplink-vertical-groups.md "cluster by judgeable"
require_text evals/golden/drift-check-strict-output.md "No planning drift found"

if [[ "$missing" -gt 0 ]]; then
  echo "Golden eval checks failed with $missing missing item(s)." >&2
  exit 1
fi

echo "Golden eval checks passed."
