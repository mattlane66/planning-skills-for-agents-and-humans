---
description: Map current-state behavior or a selected design into places, affordances, stores, consequences, and wiring.
argument-hint:
- existing-system evidence
- selected shape
- requirements
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

Choose and declare one mode: descriptive `current-state` mapping from evidence, or normative `selected-design` mapping after a human has chosen a direction and appetite.

User request and source context:

$ARGUMENTS

Produce or update a breadboard artifact with:

- Places
- UI affordances
- Non-UI affordances
- Stores
- Wiring / Returns To
- Product-relevant branches
- Optional Mermaid diagram
- Slice candidates when the breadboard is concrete enough

Keep tables as the source of truth. Do not turn the breadboard into a service graph unless backend behavior is product-relevant.

Current-state mode must cite evidence and stop before future-design slicing. Selected-design mode must cite the selected shape, appetite, and cut line before proposing slice candidates.
