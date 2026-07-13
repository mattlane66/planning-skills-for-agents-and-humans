# Lifecycle Hooks

Lifecycle hooks are optional guardrails for agentic implementation sessions.

They do not replace planning artifacts, tests, reviews, or human judgment. They nudge the agent to keep the active implementation aligned with the selected planning context.

## Included hooks

```text
hooks/planning-ripple.sh
hooks/pre-build-context-check.sh
hooks/planning-drift-check.sh
```

### `planning-ripple.sh`

Use when planning artifacts change.

It reminds the agent to check downstream artifacts when frames, requirements, selected shapes, breadboards, or slices change.

### `pre-build-context-check.sh`

Use before or during implementation.

It warns when implementation appears to start without a compact context packet in one of the expected locations:

```text
planning/context-packet.md
planning/agent-context-packet.md
planning/context.md
.agent-context.md
```

This is intentionally a non-blocking reminder by default, not a complete policy engine. Small unshaped changes may not need a context packet.

### `planning-drift-check.sh`

Use during implementation, before commits, or after meaningful code changes.

It reminds the agent to run `/check-drift` against the active context packet and changed files.

The expected result is only one of:

```text
No planning drift found.
```

or

```text
Planning drift found:
- Selected artifact says:
- Current implementation direction is:
- Risk:
- Recommended move:
```

## Example Claude Code setup

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/pre-build-context-check.sh",
            "timeout": 5
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit|Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/planning-drift-check.sh",
            "timeout": 5
          },
          {
            "type": "command",
            "command": "~/.claude/hooks/planning-ripple.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

## Installing the hooks

```bash
mkdir -p ~/.claude/hooks
ln -s ~/.local/share/planning-skills-for-agents-and-humans/hooks/planning-ripple.sh ~/.claude/hooks/planning-ripple.sh
ln -s ~/.local/share/planning-skills-for-agents-and-humans/hooks/pre-build-context-check.sh ~/.claude/hooks/pre-build-context-check.sh
ln -s ~/.local/share/planning-skills-for-agents-and-humans/hooks/planning-drift-check.sh ~/.claude/hooks/planning-drift-check.sh
```

If symlinks do not preserve executable bits in your environment, run:

```bash
chmod +x ~/.claude/hooks/planning-ripple.sh
chmod +x ~/.claude/hooks/pre-build-context-check.sh
chmod +x ~/.claude/hooks/planning-drift-check.sh
```

The repository commits these hook files as executable. The `chmod` commands are only a fallback for filesystems or copy operations that discard executable modes.

## Optional strict mode

By default the hooks print guidance and exit successfully. To make a matched reminder block with exit code 2, set `PLANNING_HOOK_STRICT=1` in the hook command environment. Use strict mode deliberately: a PreToolUse exit code 2 blocks the matched tool call.

## Design principle

Hooks should stay small and conservative.

They should remind, pause, or route the agent back to the correct planning artifact. They should not become a hidden planning method or a second implementation harness.
