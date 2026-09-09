#!/bin/bash
set -euo pipefail

if ! command -v jq >/dev/null 2>&1; then
  message="Planning drift hook is unavailable because jq is not installed. Install jq before relying on this guardrail."
  if [[ "${PLANNING_HOOK_STRICT:-0}" == "1" ]]; then
    printf '%s\n' "$message" >&2
    exit 2
  fi
  printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"Planning drift hook is unavailable because jq is not installed. Install jq before relying on this guardrail."}}'
  exit 0
fi

payload="$(cat 2>/dev/null || true)"
tool_name=""
file_path=""
command_text=""

if [[ -n "$payload" ]]; then
  tool_name="$(printf '%s' "$payload" | jq -r '.tool_name // empty' 2>/dev/null || true)"
  file_path="$(printf '%s' "$payload" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null || true)"
  command_text="$(printf '%s' "$payload" | jq -r '.tool_input.command // empty' 2>/dev/null || true)"
fi

should_remind=false

if [[ "$tool_name" =~ ^(Write|Edit)$ ]] && [[ -n "$file_path" ]]; then
  is_planning_material=false
  if [[ "$file_path" =~ (^|/)(planning|docs)(/|$) ]] || [[ "$file_path" == *.md ]]; then
    is_planning_material=true
  fi
  if [[ "$is_planning_material" == false ]]; then
    should_remind=true
  fi
fi

if [[ "$tool_name" == "Bash" ]] && [[ "$command_text" =~ (git[[:space:]]+commit|git[[:space:]]+push|npm[[:space:]]+run|pnpm[[:space:]]+|yarn[[:space:]]+|pytest|cargo[[:space:]]+test|go[[:space:]]+test|make[[:space:]]+test) ]]; then
  should_remind=true
fi

if [[ "$should_remind" == true ]]; then
  message="$(cat <<'MSG'
Planning drift check:
- If this work is implementing a shaped slice, run /check-drift against the active context packet and changed files before continuing.
- Return only "No planning drift found." or the Planning drift found block.
- Do not silently expand scope, change the selected shape, or implement rejected alternatives.
MSG
  )"
  if [[ "${PLANNING_HOOK_STRICT:-0}" == "1" ]]; then
    printf '%s\n' "$message" >&2
    exit 2
  fi
  jq -cn --arg context "$message" '{hookSpecificOutput:{hookEventName:"PostToolUse",additionalContext:$context}}'
fi

exit 0
