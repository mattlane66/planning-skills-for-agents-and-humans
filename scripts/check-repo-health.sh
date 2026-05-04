#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

failures=0

fail() {
  echo "✗ $1" >&2
  failures=$((failures + 1))
}

pass() {
  echo "✓ $1"
}

check_json() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    fail "Missing JSON file: $file"
    return
  fi

  python3 -m json.tool "$file" >/dev/null
  pass "Valid JSON: $file"
}

check_skill_frontmatter() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    fail "Missing skill file: $file"
    return
  fi

  python3 - "$file" <<'PY'
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
lines = text.splitlines()

if not lines or lines[0].strip() != "---":
    raise SystemExit(f"missing opening frontmatter marker: {path}")

try:
    end = lines[1:].index("---") + 1
except ValueError:
    raise SystemExit(f"missing closing frontmatter marker: {path}")

frontmatter = lines[1:end]
keys = {}
for line in frontmatter:
    if not line.strip() or line.strip().startswith("#"):
        continue
    if ":" not in line:
        raise SystemExit(f"invalid frontmatter line in {path}: {line!r}")
    key, value = line.split(":", 1)
    keys[key.strip()] = value.strip()

for required in ("name", "description"):
    if required not in keys or not keys[required]:
        raise SystemExit(f"missing required frontmatter key {required!r}: {path}")
PY
  pass "Valid skill frontmatter: $file"
}

check_command_points_to_skill() {
  local command_file="$1"
  local skill_path

  if [[ ! -f "$command_file" ]]; then
    fail "Missing Claude command: $command_file"
    return
  fi

  skill_path="$(grep -Eo '`[A-Za-z0-9_-]+/SKILL\.md`' "$command_file" | head -n 1 | tr -d '`' || true)"
  if [[ -z "$skill_path" ]]; then
    fail "Claude command does not reference a canonical skill: $command_file"
    return
  fi

  if [[ ! -f "$skill_path" ]]; then
    fail "Claude command references missing skill $skill_path from $command_file"
    return
  fi

  pass "Claude command maps to existing skill: $command_file -> $skill_path"
}

check_file_exists() {
  local file="$1"
  if [[ -f "$file" ]]; then
    pass "Found: $file"
  else
    fail "Missing: $file"
  fi
}

SKILLS=(
  "framing-doc"
  "shaping"
  "breadboarding"
  "kickoff-doc"
  "feed-planning-context"
  "breadboard-reflection"
)

COMMANDS=(
  "frame"
  "shape"
  "breadboard"
  "kickoff"
  "feed-context"
  "reflect-breadboard"
)

TEMPLATES=(
  "frame"
  "shaping"
  "breadboard"
  "slices"
  "context-packet"
  "kickoff"
  "breadboard-reflection"
  "spike"
  "decision-log"
  "appetite-card"
)

echo "Checking plugin manifests..."
check_json ".claude-plugin/plugin.json"
check_json ".codex-plugin/plugin.json"
check_json ".agents/plugins/marketplace.json"

echo

echo "Checking canonical skills..."
for skill in "${SKILLS[@]}"; do
  check_skill_frontmatter "$skill/SKILL.md"
done

echo

echo "Checking packaged skills..."
for skill in "${SKILLS[@]}"; do
  check_skill_frontmatter "skills/$skill/SKILL.md"
done

echo

echo "Checking Claude slash commands..."
if [[ -d ".claude/commands" ]]; then
  for command in "${COMMANDS[@]}"; do
    check_command_points_to_skill ".claude/commands/$command.md"
  done
else
  fail "Missing .claude/commands directory"
fi

echo

echo "Checking templates..."
for template in "${TEMPLATES[@]}"; do
  check_file_exists "templates/$template.md"
done

echo

echo "Checking key docs..."
check_file_exists "README.md"
check_file_exists "AGENTS.md"
check_file_exists "docs/start-here.md"
check_file_exists "docs/human-decision-gates.md"
check_file_exists "docs/plan-quality-rubric.md"
check_file_exists "docs/agent-context-feeding.md"
check_file_exists "docs/agent-workflow.md"
check_file_exists "docs/claude-slash-commands.md"

echo

echo "Checking Claude plugin bundle build..."
if [[ -x "scripts/build-claude-plugin.sh" ]]; then
  scripts/build-claude-plugin.sh >/dev/null
  for skill in "${SKILLS[@]}"; do
    check_file_exists "dist/claude-code-plugin/skills/$skill/SKILL.md"
  done
  check_json "dist/claude-code-plugin/.claude-plugin/plugin.json"
else
  fail "scripts/build-claude-plugin.sh is missing or not executable"
fi

echo

echo "Checking MCP server build..."
if [[ -f "mcp-server/package.json" ]]; then
  if command -v npm >/dev/null 2>&1; then
    (cd mcp-server && npm install >/dev/null && npm run build >/dev/null)
    pass "MCP server installs and builds"
  else
    echo "! npm not found; skipped MCP server build"
  fi
else
  fail "Missing mcp-server/package.json"
fi

echo
if [[ "$failures" -eq 0 ]]; then
  echo "Repo health check passed."
else
  echo "Repo health check failed with $failures issue(s)." >&2
  exit 1
fi
