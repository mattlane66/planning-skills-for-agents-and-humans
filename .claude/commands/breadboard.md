---
description: Map a selected shape into places, affordances, stores, consequences, and wiring.
argument-hint: [selected shape, requirements, notes, or target breadboard file]
allowed-tools: Read, Write, Edit, MultiEdit, Glob, Grep, LS
---

Read `breadboarding/SKILL.md` first and follow it as the primary instruction for this command.

Use this slash command after a direction has been chosen and the team needs concrete behavior before implementation.

User request and source context:

$ARGUMENTS

Produce or update a breadboard artifact with:

- Places
- UI affordances
- Non-UI affordances
- Stores
- Wiring / Returns To
- Product-relevant branches
- Optional Mermaid diagram
- Slice candidates when the breadboard is concrete enough

Keep tables as the source of truth. Do not turn the breadboard into a service graph unless backend behavior is product-relevant.
