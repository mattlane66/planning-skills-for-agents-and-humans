#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${1:-$ROOT_DIR/dist/claude-skills}"
INVENTORY="$ROOT_DIR/skill-inventory.txt"

command -v zip >/dev/null 2>&1 || {
  echo "zip is required to build Claude skill packages." >&2
  exit 1
}

bash "$ROOT_DIR/scripts/validate-claude-skill-descriptions.sh"

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

count=0
while IFS= read -r skill || [[ -n "$skill" ]]; do
  [[ -n "$skill" ]] || continue
  [[ -f "$ROOT_DIR/$skill/SKILL.md" ]] || {
    echo "Missing canonical skill: $skill/SKILL.md" >&2
    exit 1
  }

  # Claude expects the ZIP to contain the named skill folder as its root.
  # Package canonical folders directly so there is no second hand-edited copy.
  (
    cd "$ROOT_DIR"
    zip -qr "$OUT_DIR/$skill.zip" "$skill" \
      -x '*/.DS_Store' '*/__pycache__/*' '*/.git/*'
  )
  count=$((count + 1))
done < "$INVENTORY"

echo "Built $count uploadable Claude skill ZIPs in $OUT_DIR"
