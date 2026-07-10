#!/usr/bin/env bash
set -uo pipefail

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

check_file_exists() {
  local file="$1"
  if [[ -f "$file" ]]; then
    pass "Found: $file"
    return 0
  fi
  fail "Missing: $file"
  return 1
}

check_json() {
  local file="$1"
  check_file_exists "$file" || return
  if python3 -m json.tool "$file" >/dev/null; then
    pass "Valid JSON: $file"
  else
    fail "Invalid JSON: $file"
  fi
}

check_toml() {
  local file="$1"
  check_file_exists "$file" || return
  if python3 - "$file" <<'PY'
import pathlib
import sys
import tomllib

path = pathlib.Path(sys.argv[1])
tomllib.loads(path.read_text(encoding="utf-8"))
PY
  then
    pass "Valid TOML: $file"
  else
    fail "Invalid TOML: $file"
  fi
}

check_skill_frontmatter() {
  local file="$1"
  check_file_exists "$file" || return
  if python3 - "$file" <<'PY'
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
lines = path.read_text(encoding="utf-8").splitlines()
if not lines or lines[0].strip() != "---":
    raise SystemExit(f"missing opening frontmatter marker: {path}")
try:
    end = lines[1:].index("---") + 1
except ValueError as exc:
    raise SystemExit(f"missing closing frontmatter marker: {path}") from exc

keys = {}
for line in lines[1:end]:
    if not line.strip() or line.lstrip().startswith("#"):
        continue
    if line[0].isspace():
        continue
    if ":" not in line:
        raise SystemExit(f"invalid frontmatter line in {path}: {line!r}")
    key, value = line.split(":", 1)
    keys[key.strip()] = value.strip()

for required in ("name", "description"):
    if not keys.get(required):
        raise SystemExit(f"missing required frontmatter key {required!r}: {path}")

allowed = {"name", "description", "allowed-tools", "license", "metadata"}
unexpected = sorted(set(keys) - allowed)
if unexpected:
    raise SystemExit(f"unexpected frontmatter keys in {path}: {', '.join(unexpected)}")
PY
  then
    pass "Valid skill frontmatter: $file"
  else
    fail "Invalid skill frontmatter: $file"
  fi
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
  frame shape criteria sketch-shapes fit-check select-shape breadboard dumplink
  kickoff feed-context check-drift reflect-breadboard
)

GEMINI_COMMANDS=(criteria sketch-shapes fit-check select-shape dumplink check-drift)

TEMPLATES=(
  frame shaping breadboard interface-contracts executable-breadboard dumplink
  slices context-packet kickoff breadboard-reflection drift-check agent-run-log
  orchestration-plan spike decision-log appetite-card
)

DOCS=(
  README.md AGENTS.md GEMINI.md CHANGELOG.md LICENSE
  docs/start-here.md docs/agent-workflow.md docs/agent-context-feeding.md
  docs/agent-loop-design.md docs/full-modern-agent-workflow.md
  docs/dumplink-usage.md docs/claude-slash-commands.md docs/gemini-usage.md
  docs/codex-usage.md docs/agent-invocation-matrix.md docs/agent-run-records.md
  docs/lifecycle-hooks.md docs/human-decision-gates.md docs/plan-quality-rubric.md
)

echo "Checking manifests and licensing..."
check_json .claude-plugin/plugin.json
check_json .codex-plugin/plugin.json
check_json .agents/plugins/marketplace.json
check_file_exists .agent-orchestration.yaml
check_file_exists LICENSE

echo
echo "Checking canonical and packaged skills..."
for skill in "${SKILLS[@]}"; do
  check_skill_frontmatter "$skill/SKILL.md"
  check_skill_frontmatter "skills/$skill/SKILL.md"
done
if bash scripts/sync-packaged-skills.sh --check; then
  pass "All packaged skills match their canonical root skills"
else
  fail "One or more packaged skills differ from their canonical root skills"
fi

echo
echo "Checking command wrappers..."
for command in "${CLAUDE_COMMANDS[@]}"; do
  check_file_exists ".claude/commands/$command.md"
done
for command in "${GEMINI_COMMANDS[@]}"; do
  check_toml ".gemini/commands/$command.toml"
done

echo
echo "Checking templates and orchestration references..."
for template in "${TEMPLATES[@]}"; do
  check_file_exists "templates/$template.md"
done
if python3 - <<'PY'
import pathlib
import re

manifest = pathlib.Path(".agent-orchestration.yaml").read_text(encoding="utf-8")
artifacts = manifest.split("\nartifacts:\n", 1)[1].split("\nhooks:\n", 1)[0]
paths = re.findall(r"^  [a-z_]+:\s+([^\s]+)$", artifacts, flags=re.MULTILINE)
missing = [path for path in paths if not pathlib.Path(path).is_file()]
if missing:
    raise SystemExit("Missing orchestration artifacts: " + ", ".join(missing))
PY
then
  pass "Every orchestration artifact reference resolves"
else
  fail "One or more orchestration artifact references are broken"
fi

echo
echo "Checking documentation and discovery surfaces..."
for file in "${DOCS[@]}"; do
  check_file_exists "$file"
done
for required in "docs/start-here.md" "dumplink" "MIT"; do
  if grep -q "$required" README.md; then
    pass "README includes $required"
  else
    fail "README is missing $required"
  fi
done
if python3 scripts/check-local-links.py; then
  pass "Local Markdown links resolve"
else
  fail "One or more local Markdown links are broken"
fi

echo
echo "Checking version parity..."
if python3 - <<'PY'
import json

with open(".claude-plugin/plugin.json", encoding="utf-8") as f:
    claude = json.load(f)["version"]
with open(".codex-plugin/plugin.json", encoding="utf-8") as f:
    codex = json.load(f)["version"]
with open("mcp-server/package.json", encoding="utf-8") as f:
    mcp = json.load(f)["version"]
if len({claude, codex, mcp}) != 1:
    raise SystemExit(f"Version mismatch: Claude={claude}, Codex={codex}, MCP={mcp}")
PY
then
  pass "Claude, Codex, and MCP versions match"
else
  fail "Claude, Codex, and MCP versions do not match"
fi

echo
echo "Checking hooks and contract fixtures..."
check_file_exists hooks/planning-ripple.sh
check_file_exists hooks/pre-build-context-check.sh
check_file_exists hooks/planning-drift-check.sh
if bash scripts/check-golden-evals.sh; then
  pass "Contract fixture checks passed"
else
  fail "Contract fixture checks failed"
fi

echo
echo "Building generated Claude bundle..."
if bash scripts/build-claude-plugin.sh >/dev/null; then
  for skill in "${SKILLS[@]}"; do
    check_file_exists "dist/claude-code-plugin/skills/$skill/SKILL.md"
  done
  check_json dist/claude-code-plugin/.claude-plugin/plugin.json
else
  fail "Claude plugin bundle failed to build"
fi

echo
echo "Checking MCP server..."
if command -v npm >/dev/null 2>&1; then
  if (cd mcp-server && npm ci --ignore-scripts && npm run check); then
    pass "MCP server installs, builds, and passes tests"
  else
    fail "MCP server verification failed"
  fi
else
  fail "npm is required to verify the MCP server"
fi

echo
if [[ "$failures" -eq 0 ]]; then
  echo "Repo health check passed."
else
  echo "Repo health check failed with $failures issue(s)." >&2
  exit 1
fi
