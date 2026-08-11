---
description: Capture or revise solution shapes, including a solution-first idea, without selecting one.
argument-hint:
- solution idea
- accepted or working criteria
- frame
- notes
- prototype
- or existing shaping file
allowed-tools:
- Read
- Write
- Edit
- Glob
- Grep
disable-model-invocation: true
---

Read `shaping/SKILL.md` first and follow it as the primary instruction for this command.

Use this focused command when the current useful move is S: capturing, comparing, or revising solution shapes. It may be the **first shaping move** when the user already has a solution in mind.

Also read `docs/human-decision-gates.md`.

User request and source context:

$ARGUMENTS

Produce or update the Shapes section of a shaping artifact.

In collaborative mode:

- accepted requirements are not required merely to capture or refine a candidate shape
- Appetite may be Unset or Working while exploring
- extract any needs or constraints exposed by the shape into a `Possible requirements discovered` section
- label Appetite-dependent judgments provisional until Appetite is accepted

In gated/orchestrated mode, enforce the stricter prerequisites in `.agent-orchestration.yaml`.

Include:

- `CURRENT` when the work touches an existing system
- the user's proposed shape when one already exists; preserve its intent rather than replacing it with invented alternatives
- additional serious alternatives only when they materially help the decision
- short titles and numbered shape parts such as `A1`, `A2`, `B1`
- flagged unknowns with `⚠️`
- candidate-breadboard or spike opportunities when needed

Do not silently turn one option into the selected direction. Do not promote candidate evidence or write production code.

End by naming the smallest next useful move: revise R, revise S, fit-check, spike, candidate breadboard, set/revisit Appetite, or prepare selection.
