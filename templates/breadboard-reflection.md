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

## Inputs
- Breadboard artifact:
- Implementation files or system notes:
- Selected slice:

## What was synced
- ...

## Matches

| ID | Planned behavior | Implementation reality |
|---|---|---|
| ... | ... | ... |

## Drift

| ID | Planned artifact says | Implementation reality | Impact |
|---|---|---|---|
| DRIFT-01 | ... | ... | ... |

## Missing behavior

| ID | Missing behavior | Where it should appear | Why it matters |
|---|---|---|---|
| ... | ... | ... | ... |

## Accidental behavior

| ID | Behavior | Evidence | Risk |
|---|---|---|---|
| ... | ... | ... | ... |

## Smells found

| ID | Smell | Where | Why it matters |
|---|---|---|---|
| ... | ... | ... | ... |

## Proposed fixes

| ID | Change | Expected improvement | Type |
|---|---|---|---|
| FIX-01 | ... | ... | Planning update / implementation follow-up |

## Drift decision needed

Options:
1. Update code to match the plan.
2. Update the plan because the original assumption was wrong.
3. Split the slice and defer the conflicting part.

Recommended move:
- ...

## Self-check
- [ ] Implementation reality was inspected before critique.
- [ ] Sync findings are separate from design critique.
- [ ] Proposed fixes are grounded in concrete drift or smells.
- [ ] Planning updates and implementation follow-ups are separated.
