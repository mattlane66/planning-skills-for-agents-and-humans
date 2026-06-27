#!/usr/bin/env bash
set -euo pipefail

failures=0

fail() {
  echo "✗ $1" >&2
  failures=$((failures + 1))
}

pass() {
  echo "✓ $1"
}

check_file_exists() {
  local file="$1"
  if [[ -f "$file" ]]; then
    pass "Found: $file"
  else
    fail "Missing: $file"
  fi
}

check_json() {
  local file="$1"
  check_file_exists "$file"
  python3 -m json.tool "$file" >/dev/null
  pass "Valid JSON: $file"
}

check_toml() {
  local file="$1"
  check_file_exists "$file"
  python3 - "$file" <<'PY'
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
try:
    import tomllib
except ModuleNotFoundError:
    if "description" not in text or "prompt" not in text:
        raise SystemExit(f"missing required TOML keys in {path}")
else:
    tomllib.loads(text)
PY
  pass "Valid TOML: $file"
}

check_skill_frontmatter() {
  local file="$1"
  check_file_exists "$file"
  python3 - "$file" <<'PY'
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
lines = text.splitlines()
if not lines or lines[0].strip() != "---":
    raise SystemExit(f"missing opening frontmatter marker: {path}")
if "name:" not in text or "description:" not in text:
    raise SystemExit(f"missing required frontmatter keys: {path}")
PY
  pass "Valid skill frontmatter: $file"
}

SKILLS=(
  framing-doc
  shaping
  breadboarding
  interface-contracts
  executable-breadboards
  dumplink
  kickoff-doc
  feed-planning-context
  breadboard-reflection
)

CLAUDE_COMMANDS=(
  frame
  shape
  criteria
  sketch-shapes
  fit-check
  select-shape
  breadboard
  dumplink
  kickoff
  feed-context
  check-drift
  reflect-breadboard
)

GEMINI_COMMANDS=(
  criteria
  sketch-shapes
  fit-check
  select-shape
  dumplink
  check-drift
)

TEMPLATES=(
  frame
  shaping
  breadboard
  interface-contracts
  executable-breadboard
  slices
  context-packet
  kickoff
  breadboard-reflection
  drift-check
  agent-run-log
  spike
  decision-log
  appetite-card
)

echo "Checking manifests..."
check_json .claude-plugin/plugin.json
check_json .codex-plugin/plugin.json
check_json .agents/plugins/marketplace.json
check_file_exists .agent-orchestration.yaml

echo
echo "Checking skills..."
for skill in "${SKILLS[@]}"; do
  check_skill_frontmatter "$skill/SKILL.md"
  check_skill_frontmatter "skills/$skill/SKILL.md"
done

echo
echo "Checking command wrappers..."
for command in "${CLAUDE_COMMANDS[@]}"; do
  check_file_exists ".claude/commands/$command.md"
done
for command in "${GEMINI_COMMANDS[@]}"; do
  check_toml ".gemini/commands/$command.toml"
done

echo
echo "Checking templates..."
for template in "${TEMPLATES[@]}"; do
  check_file_exists "templates/$template.md"
done

echo
echo "Checking key docs..."
check_file_exists README.md
check_file_exists AGENTS.md
check_file_exists GEMINI.md
check_file_exists docs/start-here.md
check_file_exists docs/agent-workflow.md
check_file_exists docs/agent-context-feeding.md
check_file_exists docs/agent-loop-design.md
check_file_exists docs/full-modern-agent-workflow.md
check_file_exists docs/dumplink-usage.md
check_file_exists docs/claude-slash-commands.md
check_file_exists docs/gemini-usage.md
check_file_exists docs/codex-usage.md
check_file_exists docs/agent-run-records.md
check_file_exists docs/lifecycle-hooks.md

echo
echo "Checking hooks..."
check_file_exists hooks/planning-ripple.sh
check_file_exists hooks/pre-build-context-check.sh
check_file_exists hooks/planning-drift-check.sh

echo
echo "Checking eval fixtures..."
check_file_exists evals/README.md
check_file_exists evals/golden/context-packet-execution-contract.md
check_file_exists evals/golden/dumplink-vertical-groups.md
check_file_exists evals/golden/drift-check-strict-output.md
check_file_exists scripts/check-golden-evals.sh

echo
echo "Checking parity rules..."
if grep -q '^## Execution contract' templates/context-packet.md && grep -q 'Execution contract' mcp-server/src/index.ts; then
  pass "Context packet templates include execution contracts"
else
  fail "Context packet templates must include execution contracts"
fi

if grep -q 'dumplink' AGENTS.md && grep -q 'dumplink' .agent-orchestration.yaml && grep -q 'dumplink' mcp-server/src/index.ts; then
  pass "Dumplink is discoverable from AGENTS, orchestration, and MCP"
else
  fail "Dumplink is missing from one or more discovery surfaces"
fi

if [[ -f scripts/check-golden-evals.sh ]]; then
  bash scripts/check-golden-evals.sh
else
  fail "scripts/check-golden-evals.sh is missing"
fi

echo
if [[ "$failures" -eq 0 ]]; then
  echo "Repo health check passed."
else
  echo "Repo health check failed with $failures issue(s)." >&2
  exit 1
fi
