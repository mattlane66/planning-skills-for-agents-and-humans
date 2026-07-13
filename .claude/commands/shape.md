---
description: Shape a fuzzy request into requirements, solution directions, fit checks, and a selected direction.
argument-hint: [problem, notes, constraints, or existing shaping file]
allowed-tools: Read, Write, Edit, Glob, Grep
---

Read `shaping/SKILL.md` first and follow it as the primary instruction for this command.

Use this slash command when the user wants to compare directions before implementation or needs a durable shaping document.

User request and source context:

$ARGUMENTS

Produce or update a shaping artifact that separates but connects:

- requirements / criteria
- current baseline, when applicable
- alternative shapes
- shape parts and flagged unknowns
- fit check
- reverse fit check
- decision
- next sketch-reconciliation, breadboarding, or spike handoff

Default to planning mode. Do not write production code unless the user explicitly selects a slice to build.
