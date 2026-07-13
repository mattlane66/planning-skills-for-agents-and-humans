---
description: Package planning artifacts into a compact context packet for implementation work.
argument-hint: [planning artifact paths, selected slice, or implementation task]
allowed-tools: Read, Write, Edit, Glob, Grep
---

Read `feed-planning-context/SKILL.md` first and follow it as the primary instruction for this command.

Use this slash command when the user wants to give an implementation agent only the planning context needed for the next move.

User request and source context:

$ARGUMENTS

Produce or update a context packet that includes, as applicable:

- Task
- Source artifacts
- Authority order
- Use these sections first
- Do not use unless needed
- Must preserve
- Selected requirements
- Relevant places / affordances / stores
- Current slice
- Open questions
- Required behavior for the implementation agent
- Verification target

Do not implement code. Stop after preparing the context packet unless the user explicitly asks to proceed into implementation.
