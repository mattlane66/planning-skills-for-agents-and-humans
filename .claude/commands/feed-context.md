---
description: Package planning artifacts into a compact context packet for implementation work.
argument-hint: [planning artifact paths, selected slice, or implementation target]
allowed-tools: Read, Write, Edit, MultiEdit, Glob, Grep, LS
---

Read `feed-planning-context/SKILL.md` first and follow it as the primary instruction for this command.

Use this slash command before implementation work when planning artifacts are long, numerous, or easy to misuse.

User request and source context:

$ARGUMENTS

Produce a compact context packet with:

- Task
- Source artifacts
- Authority order
- Sections to use first
- Sections to ignore unless needed
- Must-preserve constraints
- Selected requirements
- Relevant places / affordances / stores
- Current slice
- Open questions
- Required behavior for the implementation agent
- Verification target

Do not implement code. Stop after preparing the context packet unless the user explicitly asks for the next move.
