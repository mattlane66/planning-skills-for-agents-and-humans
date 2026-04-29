# Claude Code Instructions

Use [`AGENTS.md`](./AGENTS.md) as the primary repo-level instruction surface.

This file is intentionally thin so Claude Code gets the same cross-agent workflow as Cursor, Codex, and other tools without duplicating or drifting from the canonical instructions.

## Claude-specific usage

- Use the native skill folders in this repo when installed under `~/.claude/skills/`.
- Keep `AGENTS.md` as the source of truth for mode discipline, authority order, context feeding, stable IDs, drift protocol, and completion standards.
- Keep Claude-specific hook setup in the README under `Optional Claude Code hook`.

## Reminder

Default mode is planning/shaping. Do not implement code unless the user explicitly selects a slice to build or asks for implementation.
