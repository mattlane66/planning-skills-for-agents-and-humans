---
description: Sync a breadboard to implementation reality, identify drift, and find design smells.
argument-hint: [breadboard path and implementation paths]
allowed-tools: Read, Write, Edit, Glob, Grep
---

Read `breadboard-reflection/SKILL.md` first and follow it as the primary instruction for this command.

Use this slash command after a breadboard exists and implementation has started or already exists.

User request and source context:

$ARGUMENTS

Run the reflection in two phases:

1. Sync to implementation reality first.
2. Reflect on the design only after the breadboard accurately describes what exists.

Produce or update a reflection artifact that includes, as applicable:

- What was synced
- Matches
- Drift
- Missing behavior
- Accidental behavior
- Design smells
- Proposed planning updates
- Implementation follow-ups
- Self-check

Do not critique the design before syncing the breadboard to reality.
