---
description: Define plain-language interface contracts for meaningful boundaries in the selected slice.
argument-hint:
- selected slice or active task group
- breadboard boundary or wire
- existing contract artifact, if any
allowed-tools:
- Read
- Write
- Edit
- Glob
- Grep
disable-model-invocation: true
---

Read `interface-contracts/SKILL.md` first and follow it as the primary instruction for this command.

Use `templates/interface-contracts.md` when a separate durable artifact is warranted.

User request and source context:

$ARGUMENTS

Define only the meaningful boundary contracts needed by the selected slice. Preserve stable IDs and accepted planning authority. Make inputs, outputs, required/optional fields, nullability, enum values, branches, errors, and open decisions explicit where known.

Do not invent missing field names or product decisions. Do not create production schemas or implementation code unless the user explicitly asks to move beyond planning.
