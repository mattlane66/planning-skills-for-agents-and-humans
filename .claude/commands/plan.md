---
description: Choose the smallest planning move that resolves the current uncertainty, including no planning skill when the work is already clear.
argument-hint:
- request
- notes
- artifacts
- or repository context
allowed-tools:
- Read
- Glob
- Grep
- Skill
disable-model-invocation: true
---

Read `planning-router/SKILL.md` first and follow it as the primary instruction for this command.

Use `$ARGUMENTS` and available repository context to recommend exactly one next move. Invoke only the selected canonical skill when appropriate. Do not run the full workflow, make a human decision, or begin implementation.
