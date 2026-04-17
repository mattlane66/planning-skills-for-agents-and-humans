#!/bin/bash
FILE=$(jq -r '.tool_input.file_path // empty')
if [[ "$FILE" == *.md && -f "$FILE" ]]; then
  if head -10 "$FILE" 2>/dev/null | grep -Eq '^(planning|shaping): true$'; then
    cat >&2 <<'MSG'
Planning ripple check:
- Changed requirements? Update fit checks and any slice boundaries.
- Changed a breadboard diagram? Update the tables first, then the diagram.
- Changed the selected shape? Re-check downstream slices and plans.
- Changed a frame? Confirm the shaping doc still matches the same problem.
MSG
    exit 2
  fi
fi
exit 0
