# Gemini CLI Instructions

Use the shared repo-level agent instructions below as the primary context for Gemini CLI sessions.

@./AGENTS.md

Gemini CLI users can also use project-local custom commands in `.gemini/commands/` for fluid shaping moves, planning gates, optional state modeling, task grouping, and drift checks:

- `/plan`
- `/wayfind`
- `/shape`
- `/criteria`
- `/appetite`
- `/sketch-shapes`
- `/fit-check`
- `/spike`
- `/breadboard`
- `/select-shape`
- `/reconcile-sketch`
- `/statechart`
- `/dumplink`
- `/check-drift`

Default interactive shaping is collaborative: start from R, S, evidence, or the current uncertainty and move among R/S/fit/spikes/candidate breadboards as useful. Use the gated/orchestrated profile only when explicitly requested.

These commands are Gemini-native wrappers around the same planning workflow. They preserve the same promotion gates and authority order as `AGENTS.md` rather than creating a parallel method.
