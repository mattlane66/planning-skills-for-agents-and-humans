# Gemini CLI Instructions

Use the shared repo-level agent instructions below as the primary context for Gemini CLI sessions.

@./AGENTS.md

Gemini CLI users can also use project-local custom commands in `.gemini/commands/` for gate-by-gate shaping:

- `/criteria`
- `/sketch-shapes`
- `/fit-check`
- `/select-shape`
- `/dumplink`
- `/check-drift`

These commands are Gemini-native wrappers around the same planning workflow. They should preserve the same decision gates and authority order as `AGENTS.md` rather than creating a parallel method.
