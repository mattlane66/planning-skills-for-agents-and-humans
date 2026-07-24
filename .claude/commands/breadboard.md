---
description: Map current behavior, one candidate shape, or a selected design into places, affordances, stores, consequences, and wiring.
argument-hint:
- existing-system evidence
- candidate or selected shape
- requirements and appetite
- decision-relevant uncertainty
- notes
- or target breadboard file
allowed-tools:
- Read
- Write
- Edit
- Glob
- Grep
disable-model-invocation: true
---

Read `breadboarding/SKILL.md` first and follow it as the primary instruction for this command.

Choose and declare one mode:

- descriptive `current-state` mapping from evidence
- exploratory `candidate-shape` mapping for one named unselected shape and one decision-relevant uncertainty
- normative `selected-design` mapping after a human has chosen a direction and appetite

User request and source context:

$ARGUMENTS

Produce or update a breadboard artifact with only the detail appropriate to the mode:

- Places
- UI affordances
- Non-UI affordances
- Stores
- Wiring / Returns To
- Product-relevant branches
- Optional Mermaid diagram
- Fit implications in candidate-shape mode
- Slice candidates only in accepted selected-design mode

Keep tables as the source of truth. Do not turn the breadboard into a service graph unless backend behavior is product-relevant.

Current-state mode must cite evidence and stop before future-design slicing. Candidate-shape mode must name the candidate and uncertainty, remain subordinate to shaping, and stop before selection or slicing. Selected-design mode must cite the selected shape, appetite, and cut line, reconcile any candidate evidence explicitly, and stop for a shaping decision if detailed behavior exposes a consequential conflict.