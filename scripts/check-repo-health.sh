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

check_claude_command_frontmatter() {
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
    if line[0].isspace() or ":" not in line:
        raise SystemExit(f"invalid frontmatter line in {path}: {line!r}")
    key, value = line.split(":", 1)
    keys[key.strip()] = value.strip()

if not keys.get("description"):
    raise SystemExit(f"missing command description: {path}")

allowed_keys = {"description", "argument-hint", "allowed-tools"}
unexpected = sorted(set(keys) - allowed_keys)
if unexpected:
    raise SystemExit(f"unexpected command frontmatter keys in {path}: {', '.join(unexpected)}")

known_tools = {"Read", "Write", "Edit", "Glob", "Grep", "Bash"}
tools = {item.strip() for item in keys.get("allowed-tools", "").split(",") if item.strip()}
unknown = sorted(tools - known_tools)
if unknown:
    raise SystemExit(f"unknown or retired Claude tools in {path}: {', '.join(unknown)}")
PY
  then
    pass "Valid Claude command frontmatter: $file"
  else
    fail "Invalid Claude command frontmatter: $file"
  fi
}

SKILLS=()
while IFS= read -r skill || [[ -n "$skill" ]]; do
  [[ -n "$skill" ]] && SKILLS+=("$skill")
done < skill-inventory.txt

CLAUDE_COMMANDS=(
  frame shape criteria sketch-shapes fit-check select-shape breadboard statechart dumplink
  kickoff feed-context check-drift reflect-breadboard
)

BUNDLED_CLAUDE_COMMANDS=(
  frame shape criteria sketch-shapes fit-check select-shape breadboard
  kickoff feed-context check-drift reflect-breadboard
)

GEMINI_COMMANDS=(criteria sketch-shapes fit-check select-shape statechart dumplink check-drift)

TEMPLATES=(
  frame shaping breadboard statechart interface-contracts executable-breadboard dumplink
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
  docs/statechart-usage.md implementation-context.md skill-inventory.txt
  examples/existing-codebase-drift/02-implementation-reality.md
  examples/existing-codebase-drift/03-breadboard-reflection.md
  examples/statechart-retry-workflow/01-accepted-breadboard.md
  examples/statechart-retry-workflow/02-derived-statechart.md
)

echo "Checking manifests and licensing..."
check_json .claude-plugin/plugin.json
check_json .codex-plugin/plugin.json
check_json .agents/plugins/marketplace.json
check_file_exists .agent-orchestration.yaml
check_file_exists LICENSE
if python3 - <<'PY'
import json
import pathlib

root = pathlib.Path.cwd().resolve()
codex = json.loads((root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
marketplace = json.loads((root / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))

skills_path = (root / codex["skills"]).resolve()
if not skills_path.is_dir() or root not in (skills_path, *skills_path.parents):
    raise SystemExit("Codex skills path is missing or outside the plugin root")

inventory = [line.strip() for line in (root / "skill-inventory.txt").read_text(encoding="utf-8").splitlines() if line.strip()]
if len(inventory) != len(set(inventory)):
    raise SystemExit("skill-inventory.txt contains duplicates")
packaged = sorted(path.parent.name for path in skills_path.glob("*/SKILL.md"))
if packaged != sorted(inventory):
    raise SystemExit(f"Codex skill inventory mismatch: expected {sorted(inventory)}, found {packaged}")

matching = [plugin for plugin in marketplace["plugins"] if plugin.get("name") == codex["name"]]
if len(matching) != 1:
    raise SystemExit("Marketplace must contain exactly one entry matching the Codex plugin name")
source = matching[0].get("source", {})
if source.get("source") != "local":
    raise SystemExit("Repo marketplace entry must use a local source")
source_value = source.get("path")
if not isinstance(source_value, str) or not source_value.startswith("./"):
    raise SystemExit("Marketplace source path must be an explicit ./-prefixed string")
source_path = (root / source_value).resolve()
if source_path != root:
    raise SystemExit(f"Marketplace source should resolve to plugin root, found {source_path}")
PY
then
  pass "Codex plugin inventory and marketplace paths resolve"
else
  fail "Codex plugin inventory or marketplace paths are invalid"
fi

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
  check_claude_command_frontmatter ".claude/commands/$command.md"
done
if grep -ERq '(^|[^A-Za-z])(MultiEdit|LS)([^A-Za-z]|$)' .claude/commands hooks docs/lifecycle-hooks.md; then
  fail "Retired Claude tool names remain in commands or hooks"
else
  pass "Commands and hooks use current Claude tool names"
fi
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
mcp_source = pathlib.Path("mcp-server/src/index.ts").read_text(encoding="utf-8")
not_exposed = [path for path in paths if path not in mcp_source]
if not_exposed:
    raise SystemExit("Orchestration artifacts missing from MCP: " + ", ".join(not_exposed))
PY
then
  pass "Every orchestration artifact resolves and is exposed through MCP"
else
  fail "One or more orchestration artifacts are missing or absent from MCP"
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
if grep -q "statechart" AGENTS.md \
  && grep -q "skill: statechart" .agent-orchestration.yaml \
  && grep -q "templates/statechart.md" mcp-server/src/index.ts \
  && grep -q "statechart" .codex-plugin/plugin.json \
  && grep -q "statechart" skill-inventory.txt; then
  pass "Statechart is discoverable across canonical consumer surfaces"
else
  fail "Statechart is missing from one or more canonical consumer surfaces"
fi
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
for executable in scripts/*.sh hooks/*.sh; do
  if [[ -x "$executable" ]]; then
    pass "Executable: $executable"
  else
    fail "Not executable: $executable"
  fi
done
hook_payload='{"tool_name":"Bash","tool_input":{"command":"npm run build"}}'
if printf '%s' "$hook_payload" | hooks/pre-build-context-check.sh >/dev/null 2>&1; then
  pass "Pre-build hook is non-blocking by default"
else
  fail "Pre-build hook should be non-blocking by default"
fi
strict_status=0
printf '%s' "$hook_payload" | PLANNING_HOOK_STRICT=1 hooks/pre-build-context-check.sh >/dev/null 2>&1 || strict_status=$?
if [[ "$strict_status" -eq 2 ]]; then
  pass "Pre-build hook blocks with exit 2 only in strict mode"
else
  fail "Pre-build hook strict mode should exit 2"
fi
if bash scripts/check-golden-evals.sh; then
  pass "Contract fixture checks passed"
else
  fail "Contract fixture checks failed"
fi

echo
echo "Building generated Claude bundle..."
if ./scripts/build-claude-plugin.sh >/dev/null; then
  for skill in "${SKILLS[@]}"; do
    check_file_exists "dist/claude-code-plugin/skills/$skill/SKILL.md"
  done
  for command in "${BUNDLED_CLAUDE_COMMANDS[@]}"; do
    check_claude_command_frontmatter "dist/claude-code-plugin/commands/$command.md"
    if grep -q '\${CLAUDE_PLUGIN_ROOT}' "dist/claude-code-plugin/commands/$command.md"; then
      pass "Bundle-local references: commands/$command.md"
    else
      fail "Bundled command lacks a bundle-local source reference: commands/$command.md"
    fi
  done
  for duplicate in statechart dumplink; do
    if [[ -e "dist/claude-code-plugin/commands/$duplicate.md" ]]; then
      fail "Bundled command duplicates the $duplicate directory skill"
    else
      pass "No duplicate bundled command: $duplicate"
    fi
  done
  check_file_exists dist/claude-code-plugin/AGENTS.md
  check_file_exists dist/claude-code-plugin/LICENSE
  check_file_exists dist/claude-code-plugin/docs/human-decision-gates.md
  check_file_exists dist/claude-code-plugin/docs/loop-prompting.md
  check_file_exists dist/claude-code-plugin/templates/drift-check.md
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
