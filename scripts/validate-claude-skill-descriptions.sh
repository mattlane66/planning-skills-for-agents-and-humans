#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INVENTORY="$ROOT_DIR/skill-inventory.txt"

fail() {
  echo "Claude skill description validation failed: $*" >&2
  exit 1
}

[[ -f "$INVENTORY" ]] || fail "missing skill-inventory.txt"

count=0
while IFS= read -r skill || [[ -n "$skill" ]]; do
  [[ -n "$skill" ]] || continue
  file="$ROOT_DIR/$skill/SKILL.md"
  [[ -f "$file" ]] || fail "missing $skill/SKILL.md"

  name="$(awk 'BEGIN{fm=0} /^---$/{fm++; next} fm==1 && /^name:[[:space:]]*/{sub(/^name:[[:space:]]*/, ""); print; exit}' "$file")"
  description="$(awk 'BEGIN{fm=0} /^---$/{fm++; next} fm==1 && /^description:[[:space:]]*/{sub(/^description:[[:space:]]*/, ""); print; exit}' "$file")"

  [[ "$name" == "$skill" ]] || fail "$skill frontmatter name must match its folder"
  [[ -n "$description" ]] || fail "$skill has no description"
  [[ ${#description} -le 200 ]] || fail "$skill description exceeds 200 characters"

  # Claude uses this field to decide when to load a skill. Require both an
  # action and a recognizable trigger/context signal without enforcing one
  # exact writing style.
  lower="$(printf '%s' "$description" | tr '[:upper:]' '[:lower:]')"
  [[ "$lower" =~ (create|produce|map|shape|compare|reconcile|model|define|plan|prepare|feed|inspect|reflect|turn|convert|document) ]] \
    || fail "$skill description does not clearly state what the skill does"
  [[ "$lower" =~ (when|for|from|into|before|after|needs|need|selected|existing|implementation|handoff|notes|transcript|request|slice|system|code) ]] \
    || fail "$skill description does not clearly signal when or in what context to use it"

  count=$((count + 1))
done < "$INVENTORY"

echo "Validated Claude trigger descriptions for $count skills."
