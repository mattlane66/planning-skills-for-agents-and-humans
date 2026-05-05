---
description: Package planning artifacts into a compact context packet for implementation agents.
argument-hint: "[planning artifact paths or active task]"
---

Use the canonical planning skill at `feed-planning-context/SKILL.md`.

Prepare a compact context packet from the user's input or referenced planning artifacts.

Default behavior:
- identify the current task
- list source artifacts and authority order
- include only the sections needed for the next move
- preserve stable IDs for requirements, places, affordances, stores, and slices
- keep rejected alternatives and raw notes out unless needed
- name explicit non-goals and exclusions
- add a verification target
- stop after preparing the context packet; do not implement code

Input:
$ARGUMENTS
