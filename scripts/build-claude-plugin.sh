#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist/claude-code-plugin"

bash "$ROOT_DIR/scripts/sync-packaged-skills.sh" --check

SKILLS=()
while IFS= read -r skill || [[ -n "$skill" ]]; do
  [[ -n "$skill" ]] && SKILLS+=("$skill")
done < "$ROOT_DIR/skill-inventory.txt"

rm -rf "$DIST_DIR"
mkdir -p \
  "$DIST_DIR/.claude-plugin" \
  "$DIST_DIR/skills" \
  "$DIST_DIR/commands" \
  "$DIST_DIR/docs" \
  "$DIST_DIR/templates" \
  "$DIST_DIR/hooks"

cp "$ROOT_DIR/.claude-plugin/plugin.json" "$DIST_DIR/.claude-plugin/plugin.json"
cp "$ROOT_DIR/LICENSE" "$DIST_DIR/LICENSE"
cp "$ROOT_DIR/.agent-orchestration.yaml" "$DIST_DIR/.agent-orchestration.yaml"
cp "$ROOT_DIR/docs/agent-context-feeding.md" "$DIST_DIR/docs/agent-context-feeding.md"
cp "$ROOT_DIR/docs/agent-run-records.md" "$DIST_DIR/docs/agent-run-records.md"
cp "$ROOT_DIR/docs/human-decision-gates.md" "$DIST_DIR/docs/human-decision-gates.md"
cp "$ROOT_DIR/docs/lifecycle-hooks.md" "$DIST_DIR/docs/lifecycle-hooks.md"
cp "$ROOT_DIR/docs/loop-prompting.md" "$DIST_DIR/docs/loop-prompting.md"
cp "$ROOT_DIR/templates/"*.md "$DIST_DIR/templates/"
cp "$ROOT_DIR/hooks/"*.sh "$DIST_DIR/hooks/"

rewrite_args=(
  -e 's#AGENTS\.md#${CLAUDE_PLUGIN_ROOT}/AGENTS.md#g'
  -e 's#\.agent-orchestration\.yaml#${CLAUDE_PLUGIN_ROOT}/.agent-orchestration.yaml#g'
  -e 's#docs/agent-context-feeding\.md#${CLAUDE_PLUGIN_ROOT}/docs/agent-context-feeding.md#g'
  -e 's#docs/agent-run-records\.md#${CLAUDE_PLUGIN_ROOT}/docs/agent-run-records.md#g'
  -e 's#docs/human-decision-gates\.md#${CLAUDE_PLUGIN_ROOT}/docs/human-decision-gates.md#g'
  -e 's#docs/lifecycle-hooks\.md#${CLAUDE_PLUGIN_ROOT}/docs/lifecycle-hooks.md#g'
  -e 's#docs/loop-prompting\.md#${CLAUDE_PLUGIN_ROOT}/docs/loop-prompting.md#g'
  -e 's#templates/#${CLAUDE_PLUGIN_ROOT}/templates/#g'
  -e 's#hooks/#${CLAUDE_PLUGIN_ROOT}/hooks/#g'
)
for skill in "${SKILLS[@]}"; do
  rewrite_args+=(
    -e "s#$skill/SKILL.md#\${CLAUDE_PLUGIN_ROOT}/skills/$skill/SKILL.md#g"
  )
done

sed "${rewrite_args[@]}" "$ROOT_DIR/AGENTS.md" > "$DIST_DIR/AGENTS.md"

for skill in "${SKILLS[@]}"; do
  source_file="$ROOT_DIR/$skill/SKILL.md"
  target_dir="$DIST_DIR/skills/$skill"

  if [[ ! -f "$source_file" ]]; then
    echo "Missing skill file: $source_file" >&2
    exit 1
  fi

  mkdir -p "$target_dir"
  sed "${rewrite_args[@]}" "$source_file" > "$target_dir/SKILL.md"
done

for command_file in "$ROOT_DIR"/.claude/commands/*.md; do
  command_name="$(basename "$command_file" .md)"
  duplicates_skill=false

  for skill in "${SKILLS[@]}"; do
    if [[ "$command_name" == "$skill" ]]; then
      duplicates_skill=true
      break
    fi
  done

  # Claude gives a directory skill precedence over a flat command with the
  # same name. Omit redundant wrappers so the generated bundle has one clear
  # implementation for /planning-skills:statechart and :dumplink.
  if [[ "$duplicates_skill" == "true" ]]; then
    continue
  fi

  sed "${rewrite_args[@]}" "$command_file" > "$DIST_DIR/commands/$command_name.md"
done

cat > "$DIST_DIR/README.md" <<'EOF'
# Planning Skills Claude Code Plugin Bundle

This generated bundle mirrors the canonical Planning Skills `SKILL.md` files from the repository root. Skills, command wrappers, and shared agent instructions use bundle-local references. The orchestration manifest, reusable docs, templates, hooks, and license they depend on are included.

Claude namespaces plugin skills and commands with the manifest name. For example:

- `/planning-skills:framing-doc` invokes the canonical Framing skill.
- `/planning-skills:frame` invokes the shorter framing command wrapper.
- `/planning-skills:statechart` invokes the canonical Statechart skill.

Canonical source repo:
https://github.com/mattlane66/planning-skills-for-agents-and-humans
EOF

echo "Built Claude Code plugin bundle at: $DIST_DIR"
