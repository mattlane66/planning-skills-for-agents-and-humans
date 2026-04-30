#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist/claude-code-plugin"

SKILLS=(
  "framing-doc"
  "shaping"
  "breadboarding"
  "kickoff-doc"
  "feed-planning-context"
  "breadboard-reflection"
)

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR/.claude-plugin" "$DIST_DIR/skills"

cp "$ROOT_DIR/.claude-plugin/plugin.json" "$DIST_DIR/.claude-plugin/plugin.json"

for skill in "${SKILLS[@]}"; do
  source_file="$ROOT_DIR/$skill/SKILL.md"
  target_dir="$DIST_DIR/skills/$skill"

  if [[ ! -f "$source_file" ]]; then
    echo "Missing skill file: $source_file" >&2
    exit 1
  fi

  mkdir -p "$target_dir"
  cp "$source_file" "$target_dir/SKILL.md"
done

cat > "$DIST_DIR/README.md" <<'EOF'
# Planning Skills Claude Code Plugin Bundle

This generated bundle mirrors the canonical Planning Skills `SKILL.md` files from the repository root.

Canonical source repo:
https://github.com/mattlane66/planning-skills-for-agents-and-humans
EOF

echo "Built Claude Code plugin bundle at: $DIST_DIR"
