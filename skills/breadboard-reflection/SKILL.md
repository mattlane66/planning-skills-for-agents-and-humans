---
name: breadboard-reflection
description: Reflect on a breadboard by syncing it to implementation and finding design smells.
planning: true
---

# Breadboard Reflection

Use this skill after a breadboard exists and implementation has started or already exists.

## Goal

Bring the breadboard back into alignment with reality, then use it to spot design problems that are otherwise easy to miss.

## Two-phase loop

### 1. Sync to reality
The code or implementation is the ground truth.

Do this first:
- read the relevant implementation
- repair missing or wrong nodes
- add hidden stores or omitted transitions
- remove stale affordances
- fix incorrect wiring

At the end of this phase, the breadboard should show what the system actually does.

### 2. Reflect on the design
Once the breadboard is accurate, inspect the design itself.

Look for:
- hidden state
- unclear boundaries
- steps that resist clear naming
- duplicated responsibility
- missing explanatory links in the wiring
- places that are too broad or too muddled

## Smells to check

| Smell | What it suggests |
|------|-------------------|
| Unexplained behavior | The artifact does not explain how the effect happens |
| Naming resistance | A node may be bundling multiple responsibilities |
| Missing source for displayed data | A store or upstream affordance is absent |
| Wrong causality | The wiring tells the wrong story about what triggers what |
| Place overload | Too many unrelated concerns are packed together |

## Naming test

For any affordance that feels off, ask:
1. Who calls it?
2. What is its direct step-level effect?
3. Can it be named with one clear verb?

If the answer requires two verbs joined by "and" or "or," the boundary may be wrong.

## Output structure

```md
---
planning: true
artifact_type: breadboard-reflection
status: draft
source_of_truth: true
feeds:
  - planning-update
  - implementation-followup
---

# [Project] — Breadboard Reflection

# Context Card

## Use this when
An agent is comparing implementation reality against the intended breadboard and deciding what planning artifacts or implementation follow-ups need repair.

## Must preserve
- distinction between synced reality and design critique
- observed drift
- missing behavior
- accidental behavior
- proposed fixes

## Ignore unless asked
- speculative redesigns not grounded in the synced implementation

## What was synced
- ...

## Smells found
| ID | Smell | Where | Why it matters |
|----|-------|-------|----------------|

## Proposed fixes
| ID | Change | Expected improvement |
|----|--------|----------------------|

## Updated breadboard notes
- ...
```

## Rule

Do not start critiquing the design until the breadboard has first been made accurate.

## Self-check before finishing

- Relevant implementation or system reality was inspected before critique.
- The reflection separates sync-to-reality findings from design critique.
- Missing, stale, or wrong breadboard nodes are named explicitly.
- Design smells are tied to concrete places, affordances, stores, or wiring.
- Proposed fixes explain the expected improvement.
- Planning updates and implementation follow-ups are separated.
- The artifact has planning frontmatter and a Context Card when it will feed downstream agent work.
