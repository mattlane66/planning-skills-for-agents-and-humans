#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${1:-$ROOT_DIR/dist/claude-skills}"
INVENTORY="$ROOT_DIR/skill-inventory.txt"
DESCRIPTIONS="$ROOT_DIR/claude-skill-descriptions.tsv"

command -v zip >/dev/null 2>&1 || {
  echo "zip is required to build Claude skill packages." >&2
  exit 1
}
command -v python3 >/dev/null 2>&1 || {
  echo "python3 is required to build Claude skill packages." >&2
  exit 1
}

bash "$ROOT_DIR/scripts/validate-claude-skill-descriptions.sh"

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"
STAGE_DIR="$(mktemp -d)"
trap 'rm -rf "$STAGE_DIR"' EXIT

count=0
while IFS= read -r skill || [[ -n "$skill" ]]; do
  [[ -n "$skill" ]] || continue
  [[ -f "$ROOT_DIR/$skill/SKILL.md" ]] || {
    echo "Missing canonical skill: $skill/SKILL.md" >&2
    exit 1
  }

  description="$(awk -F '\t' -v skill="$skill" '$1 == skill {sub(/^[^\t]*\t/, ""); print; exit}' "$DESCRIPTIONS")"
  rm -rf "$STAGE_DIR/$skill"
  cp -R "$ROOT_DIR/$skill" "$STAGE_DIR/$skill"

  # Keep the canonical method intact while optimizing only the uploaded
  # package metadata for Claude's automatic skill selection.
  python3 - "$STAGE_DIR/$skill/SKILL.md" "$description" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
description = sys.argv[2]
lines = path.read_text(encoding="utf-8").splitlines()
in_frontmatter = False
replaced = False
for index, line in enumerate(lines):
    if line == "---":
        if not in_frontmatter:
            in_frontmatter = True
            continue
        break
    if in_frontmatter and line.startswith("description:"):
        lines[index] = f"description: {description}"
        replaced = True
        break
if not replaced:
    raise SystemExit(f"No frontmatter description found in {path}")
path.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY

  # Claude expects the ZIP to contain the named skill folder as its root.
  (
    cd "$STAGE_DIR"
    zip -qr "$OUT_DIR/$skill.zip" "$skill" \
      -x '*/.DS_Store' '*/__pycache__/*' '*/.git/*'
  )
  count=$((count + 1))
done < "$INVENTORY"

echo "Built $count uploadable Claude skill ZIPs in $OUT_DIR"
