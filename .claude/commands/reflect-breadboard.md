---
description: Compare accepted breadboard intent with implementation reality and prepare an explicit drift decision.
argument-hint:
- breadboard path and implementation paths
allowed-tools:
- Read
- Write
- Edit
- Glob
- Grep
disable-model-invocation: true
---

Read `breadboard-reflection/SKILL.md` first and follow it as the primary instruction for this command.

Use this slash command after a breadboard exists and implementation has started or already exists.

User request and source context:

$ARGUMENTS

Run the reflection in three phases:

1. Record implementation reality without rewriting accepted intent.
2. Compare intent and reality, then reflect on concrete design smells.
3. Present correction options and stop for a human drift decision unless the user already authorized one.

Produce or update a reflection artifact that includes, as applicable:

- What was synced
- Matches
- Drift
- Missing behavior
- Accidental behavior
- Design smells
- Proposed planning updates
- Implementation follow-ups
- Drift decision needed or already authorized
- Self-check

Do not silently update the accepted breadboard to match the implementation.
