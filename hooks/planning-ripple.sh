#!/bin/bash
set -euo pipefail

if ! command -v jq >/dev/null 2>&1; then
  exit 0
fi

payload="$(cat 2>/dev/null || true)"
FILE="$(printf '%s' "$payload" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null || true)"
if [[ "$FILE" == *.md && -f "$FILE" ]]; then
  if head -10 "$FILE" 2>/dev/null | grep -Eq '^(planning|shaping): true$'; then
    cat >&2 <<'MSG'
Planning ripple check:
- Changed requirements? Update fit checks and any slice boundaries.
- Changed a breadboard diagram? Update the tables first, then the diagram.
- Changed the selected shape? Re-check downstream slices and plans.
- Changed a frame? Confirm the shaping doc still matches the same problem.
MSG
    if [[ "${PLANNING_HOOK_STRICT:-0}" == "1" ]]; then
      exit 2
    fi
  fi
fi
exit 0
