---
planning: true
artifact_type: breadboard-reflection
status: draft
source_of_truth: false
feeds:
  - planning-update
  - implementation-followup
---

# [Project] — Breadboard Reflection

# Context Card

## Use this when
An agent is comparing implementation reality against accepted intent and preparing an explicit decision about what should change.

## Must preserve
- accepted intent and current implementation reality as separate records
- observed drift
- missing behavior
- accidental behavior
- proposed fixes
- the authorized or still-needed drift decision

## Ignore unless asked
- speculative redesigns not grounded in inspected implementation evidence

## Inputs
- Breadboard artifact:
- Implementation files or system notes:
- Selected slice:

## Current implementation reality

Record what the system does now and cite the inspected evidence. Do not rewrite the accepted breadboard in this phase.

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

Decision status:
- Pending / authorized by current user instruction / decided by [name or record]

Artifacts or implementation allowed to change after this decision:
- ...

## Self-check
- [ ] Implementation reality was inspected before critique.
- [ ] Accepted intent and current reality remain separate.
- [ ] Proposed fixes are grounded in concrete drift or smells.
- [ ] Planning updates and implementation follow-ups are separated.
- [ ] No accepted artifact was rewritten before an explicit decision.
