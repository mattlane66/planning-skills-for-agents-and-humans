---
description: Shape a fuzzy request into requirements, solution directions, fit checks, and a selected direction.
argument-hint: [problem, notes, constraints, or existing shaping file]
allowed-tools: Read, Write, Edit, Glob, Grep
---

Read `shaping/SKILL.md` first and follow it as the primary instruction for this command.

Also read `docs/human-decision-gates.md`. Set or confirm Gate 2A before recording any selection, and never invent the Gate 3 human choice.

Use this slash command when the user wants to compare directions before implementation or needs a durable shaping document.

User request and source context:

$ARGUMENTS

Produce or update a shaping artifact that separates but connects:

- requirements / criteria
- appetite and cut line, set before selection
- current baseline, when applicable
- alternative shapes
- shape parts and flagged unknowns
- fit check
- reverse fit check
- appetite fit and required cuts
- decision
- next sketch-reconciliation, breadboarding, or spike handoff

Default to planning mode. Do not write production code unless the user explicitly selects a slice to build.
