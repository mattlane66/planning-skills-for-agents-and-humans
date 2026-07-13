#!/bin/bash
set -euo pipefail

payload="$(cat 2>/dev/null || true)"
tool_name=""
command_text=""
file_path=""

if command -v jq >/dev/null 2>&1 && [[ -n "$payload" ]]; then
  tool_name="$(printf '%s' "$payload" | jq -r '.tool_name // empty' 2>/dev/null || true)"
  command_text="$(printf '%s' "$payload" | jq -r '.tool_input.command // empty' 2>/dev/null || true)"
  file_path="$(printf '%s' "$payload" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null || true)"
fi

has_context_packet=false
for candidate in \
  planning/context-packet.md \
  planning/agent-context-packet.md \
  planning/context.md \
  .agent-context.md; do
  if [[ -f "$candidate" ]] && grep -Eiq 'context packet|agent context packet|selected slice|verification target' "$candidate"; then
    has_context_packet=true
    break
  fi
done

looks_like_build=false
if [[ "$tool_name" =~ ^(Write|Edit)$ ]] && [[ -n "$file_path" ]] && [[ ! "$file_path" =~ (^planning/|^docs/|\.md$) ]]; then
  looks_like_build=true
fi

if [[ "$tool_name" == "Bash" ]] && [[ "$command_text" =~ (npm[[:space:]]+(run|test|exec)|pnpm[[:space:]]+(run|test|exec)|yarn[[:space:]]+(run|test)|bun[[:space:]]+(run|test)|pytest|python[[:space:]]+-m[[:space:]]+pytest|cargo[[:space:]]+(build|test|run)|go[[:space:]]+(build|test|run)|make([[:space:]]|$)|gradle|mvn[[:space:]]+(test|package|verify)|swift[[:space:]]+(build|test)|xcodebuild|tsc([[:space:]]|$)|vite([[:space:]]|$)|next[[:space:]]+(build|dev)|rails[[:space:]]+(test|server)) ]]; then
  looks_like_build=true
fi

if [[ "$looks_like_build" == true && "$has_context_packet" == false ]]; then
  cat >&2 <<'MSG'
Pre-build context check:
- Implementation appears to be starting, but no compact context packet was found.
- Create one with the feed-planning-context skill before build work when the task has shaped planning artifacts.
- Expected paths include planning/context-packet.md, planning/agent-context-packet.md, planning/context.md, or .agent-context.md.
- If this is a tiny unshaped change, continue intentionally.
MSG
  if [[ "${PLANNING_HOOK_STRICT:-0}" == "1" ]]; then
    exit 2
  fi
fi

exit 0
