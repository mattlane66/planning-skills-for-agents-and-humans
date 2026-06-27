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

This is intentionally a reminder, not a complete policy engine. Small unshaped changes may not need a context packet.

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
        "matcher": "Write|Edit|MultiEdit|Bash",
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
        "matcher": "Write|Edit|MultiEdit|Bash",
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

## Design principle

Hooks should stay small and conservative.

They should remind, pause, or route the agent back to the correct planning artifact. They should not become a hidden planning method or a second implementation harness.
