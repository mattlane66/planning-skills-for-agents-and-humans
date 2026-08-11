---
description: Create, extract, or revise requirements / criteria without requiring solution exploration to stop.
argument-hint:
- problem
- notes
- transcript
- proposed solution
- prototype
- frame
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

Use this focused command when the user wants to work on R only for the current move. It is **not** evidence that R had to come before S.

Also read `docs/human-decision-gates.md`.

User request and source context:

$ARGUMENTS

Produce or update the requirements / criteria portion of a shaping artifact.

Requirements may come from a problem statement, research, an existing shape, a prototype, a fit failure, or a spike. When extracting R from S, restate the underlying need or constraint independently of the mechanism.

Include:

- requirement IDs such as `R0`, `R1`, `R2`
- requirement text stated as needs, outcomes, constraints, or quality bars
- status values such as Core goal, Must-have, Nice-to-have, Undecided, or Out
- authority as Working or Accepted when known
- source notes or assumptions when useful

Do not delete or suppress existing shapes merely because this command is focused on R. Do not silently change accepted requirements; propose the delta and stop for the human decision.

Do not select a direction, promote a candidate breadboard, or write production code.

End by naming the smallest next useful shaping move, which may be revise S, fit-check, spike, candidate breadboard, Appetite, or acceptance of R.
