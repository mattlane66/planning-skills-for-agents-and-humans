---
description: Set the bounded time or scope budget and cut line before selecting a solution shape.
argument-hint:
- accepted criteria
- shaping file
- budget
- team shape
- or review point
allowed-tools:
- Read
- Write
- Edit
- Glob
- Grep
disable-model-invocation: true
---

Read `shaping/SKILL.md` first and follow it as the primary instruction for this command.

Also read `docs/human-decision-gates.md` and apply Gate 2A: Appetite set. Use `templates/appetite-card.md` when this decision needs a separate durable artifact; otherwise update the Appetite section of the shaping document.

User request and source context:

$ARGUMENTS

Record:

- the time budget or other fixed scope budget
- team shape and review point
- explicit cut line
- uncertainty the team accepts
- unknowns that require a spike before selection or build
- decision owner and revisit condition when known

Treat appetite as a constraint on candidate shapes, not as an estimate derived from a preferred shape.

Do not select a direction.
Do not breadboard.
Do not write production code.

End with a Gate 2A status:

- `Appetite set — ready for /sketch-shapes` when the budget and cut line are explicit
- `Needs human appetite decision` when the budget, cut line, or accepted uncertainty remains open
