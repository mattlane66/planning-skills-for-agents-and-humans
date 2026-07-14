# Gemini CLI Instructions

Use the shared repo-level agent instructions below as the primary context for Gemini CLI sessions.

@./AGENTS.md

Gemini CLI users can also use project-local custom commands in `.gemini/commands/` for planning gates, optional state modeling, task grouping, and drift checks:

- `/criteria`
- `/appetite`
- `/sketch-shapes`
- `/fit-check`
- `/select-shape`
- `/reconcile-sketch`
- `/statechart`
- `/dumplink`
- `/check-drift`

These commands are Gemini-native wrappers around the same planning workflow. They should preserve the same decision gates and authority order as `AGENTS.md` rather than creating a parallel method.
