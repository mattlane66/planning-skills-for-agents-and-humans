---
description: Turn the selected slice into a concrete behavioral build handoff with fixtures, runs, edge cases, and tests.
argument-hint:
- selected slice or active task group
- accepted breadboard and contracts
- existing executable breadboard, if any
allowed-tools:
- Read
- Write
- Edit
- Glob
- Grep
disable-model-invocation: true
---

Read `executable-breadboards/SKILL.md` first and follow it as the primary instruction for this command.

Use `templates/executable-breadboard.md` for the durable artifact.

User request and source context:

$ARGUMENTS

Prepare the selected slice for implementation with only the relevant breadboard structure, interface contracts, concrete starting fixtures, example runs, expected visible results and state changes, edge cases, acceptance tests, open decisions, and verification target.

Do not expand beyond the selected slice. Do not invent missing fields, states, error cases, or expected results. Stop after the build handoff unless the user explicitly asks to proceed into implementation.
