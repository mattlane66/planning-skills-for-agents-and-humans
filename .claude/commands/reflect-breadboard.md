---
description: Sync a breadboard to implementation reality, then identify design drift and smells.
argument-hint: [breadboard path, code path, implementation notes, or target reflection file]
allowed-tools: Read, Write, Edit, MultiEdit, Glob, Grep, LS
---

Read `breadboard-reflection/SKILL.md` first and follow it as the primary instruction for this command.

Use this slash command after implementation exists and the team needs to compare reality to the intended breadboard.

User request and source context:

$ARGUMENTS

Work in two phases:

1. Sync the breadboard to implementation reality.
2. Reflect on the design only after reality is accurate.

Return or update a reflection artifact with:

- What was inspected
- Matches
- Drift
- Missing behavior
- Accidental behavior
- Design smells
- Proposed planning updates
- Proposed implementation follow-ups

Do not critique the design before syncing the breadboard to reality.
