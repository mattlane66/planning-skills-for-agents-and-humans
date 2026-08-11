# Claude Code Instructions

Use [`AGENTS.md`](./AGENTS.md) as the primary repo-level instruction surface.

This file is intentionally thin so Claude Code gets the same cross-agent workflow as Cursor, Codex, Gemini, and other tools without duplicating or drifting from the canonical instructions.

## Claude-specific usage

- Use the native skill folders in this repo when installed under `~/.claude/skills/`.
- Keep `AGENTS.md` as the source of truth for collaborative versus gated shaping, promotion gates, authority order, context feeding, stable IDs, drift protocol, and completion standards.
- Use `/shape` as the broad collaborative front door; `/criteria`, `/appetite`, `/sketch-shapes`, `/fit-check`, `/spike`, and `/breadboard` are focused moves, not required stages.
- Keep Claude-specific hook setup aligned with [`docs/lifecycle-hooks.md`](./docs/lifecycle-hooks.md).

## Reminder

Default interactive mode is collaborative shaping: start from R, S, evidence, or the current uncertainty and move fluidly while material is Working.

Do not select a direction until accepted requirements, accepted Appetite, decision-ready evidence, and an explicit human choice exist. Do not implement code unless the user explicitly selects a slice to build or asks for implementation.
