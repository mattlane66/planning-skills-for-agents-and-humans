---
description: Shape product work collaboratively from requirements, a solution idea, evidence, or an existing shaping artifact without forcing a fixed exploration order.
argument-hint:
- requirements
- solution idea
- problem
- notes
- prototype
- constraints
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

Also read `docs/human-decision-gates.md`.

Default to the **collaborative** shaping profile unless the user explicitly asks for gated/orchestrated planning.

User request and source context:

$ARGUMENTS

Start from whatever is already most concrete:

- R-first when the user brings needs, constraints, or requirements
- S-first when the user brings a solution already in mind
- evidence-first when the user brings a prototype, sketch, or current-system behavior
- uncertainty-first when a fit question, spike, or candidate breadboard is the smallest useful move

Allow requirements, shapes, fit checks, focused spikes, sketches, and candidate breadboards to iterate in any useful order while they remain working material. Keep requirements separate from mechanisms and make Working versus Accepted authority visible.

Do not force the user through `/criteria` → `/appetite` → `/sketch-shapes` as a mandatory exploration sequence.

Before recording a selected direction, enforce the hard promotion gate: accepted requirements, accepted Appetite and cut line, decision-ready fit evidence, and an explicit human selection.

Do not automatically promote candidate evidence to selected-design intent. Do not write production code unless the user explicitly selects a slice to build.
