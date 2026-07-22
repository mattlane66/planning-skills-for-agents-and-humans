#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INVENTORY="$ROOT_DIR/skill-inventory.txt"
DESCRIPTIONS="$ROOT_DIR/claude-skill-descriptions.tsv"

fail() {
  echo "Claude skill description validation failed: $*" >&2
  exit 1
}

[[ -f "$INVENTORY" ]] || fail "missing skill-inventory.txt"
[[ -f "$DESCRIPTIONS" ]] || fail "missing claude-skill-descriptions.tsv"

count=0
while IFS= read -r skill || [[ -n "$skill" ]]; do
  [[ -n "$skill" ]] || continue
  file="$ROOT_DIR/$skill/SKILL.md"
  [[ -f "$file" ]] || fail "missing $skill/SKILL.md"

  name="$(awk 'BEGIN{fm=0} /^---$/{fm++; next} fm==1 && /^name:[[:space:]]*/{sub(/^name:[[:space:]]*/, ""); print; exit}' "$file")"
  [[ "$name" == "$skill" ]] || fail "$skill frontmatter name must match its folder"

  description="$(awk -F '\t' -v skill="$skill" '$1 == skill {sub(/^[^\t]*\t/, ""); print; exit}' "$DESCRIPTIONS")"
  [[ -n "$description" ]] || fail "$skill has no Claude upload description"
  [[ ${#description} -le 200 ]] || fail "$skill Claude upload description exceeds 200 characters"

  lower="$(printf '%s' "$description" | tr '[:upper:]' '[:lower:]')"
  [[ "$lower" =~ (create|produce|map|shape|compare|reconcile|model|define|plan|prepare|feed|inspect|reflect|turn|derive) ]] \
    || fail "$skill description does not clearly state what the skill does"
  [[ "$lower" =~ (when|for|from|into|before|after|needs|need|selected|existing|implementation|handoff|notes|transcript|request|slice|system|code) ]] \
    || fail "$skill description does not clearly signal when or in what context to use it"

  count=$((count + 1))
done < "$INVENTORY"

mapped_count="$(awk -F '\t' 'NF >= 2 {count++} END {print count+0}' "$DESCRIPTIONS")"
[[ "$mapped_count" -eq "$count" ]] || fail "description map has $mapped_count entries for $count skills"

echo "Validated Claude upload trigger descriptions for $count skills."
