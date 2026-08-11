---
description: Investigate one focused shaping unknown and return explicit implications to requirements, shapes, fit, or Appetite without making the product decision.
argument-hint:
- shaping file
- shape part
- requirement
- fit row
- candidate breadboard
- technical question
- or evidence source
allowed-tools:
- Read
- Write
- Edit
- Glob
- Grep
disable-model-invocation: true
---

Read `shaping/SKILL.md` first and use `templates/spike.md` for the artifact shape.

A spike may be triggered from R, S, fit, a sketch, a candidate breadboard, or implementation reality. It does not require a selected shape.

User request and source context:

$ARGUMENTS

Investigate only the smallest unknown that could materially change the current shaping judgment.

Return:

- the questions answered
- evidence and constraints discovered
- mechanism understanding
- explicit implications for R
- explicit implications for S
- fit rows or candidates to rerun
- Appetite implications when known
- remaining uncertainty
- the smallest next useful shaping move

Do not silently rewrite accepted requirements, Appetite, or a selected shape. Propose consequential deltas and stop for the applicable human gate.

The spike gathers evidence; it does not select a product direction or write production code unless the user explicitly asks for a disposable technical experiment as the evidence-gathering method.
