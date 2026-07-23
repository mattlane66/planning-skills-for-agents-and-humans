---
description: Record or prepare a human shape-selection decision after alternatives and fit checks are visible.
argument-hint:
- shaping file
- fit check
- human choice
- or decision note
allowed-tools:
- Read
- Write
- Edit
- Glob
- Grep
disable-model-invocation: true
---

Read `shaping/SKILL.md` first and follow it as the primary instruction for this command.

Use this slash command when the team is ready to choose a direction, record that choice, and prepare the next breadboarding or spike handoff.

Also read `docs/human-decision-gates.md`. Confirm Gate 2A: Appetite set before applying Gate 3: Shape selected. If appetite is missing, stop and recommend `/appetite`.

User request and source context:

$ARGUMENTS

Produce or update the Decision section of a shaping artifact.

If the user has explicitly chosen a shape:

- record the chosen direction
- preserve rejected shapes as rejected, not deleted
- summarize why the selected shape fits the accepted criteria
- record how the selected shape fits the accepted appetite and which cuts remain binding
- list any known trade-offs
- list flagged unknowns that still require spikes
- identify the next handoff: `/reconcile-sketch` when a visual needs review, `/breadboard`, spike, or criteria revision

If the user has not explicitly chosen a shape:

- summarize the fit-check result
- show the viable choices
- state any recommendation separately as `Recommended`, not `Selected`
- stop before recording a final selection

Do not silently choose for the human.
Do not invent missing fit-check evidence.
Do not select a shape against an undecided appetite.
Do not breadboard unless the selected shape is explicit.
Do not write production code.

End with a Gate 3 status:

- `Shape selected` when the human choice is explicit and recorded
- `Needs human selection` when the choice is still open
