---
name: shaping
description: Shape ambiguous product work before implementation by defining criteria and appetite, comparing solution directions, and recording the selected shape and cut line.
license: MIT
---

# Shaping

Use this skill when the problem is clear enough to compare solution directions, but the requirements, appetite, tradeoffs, or selected path are not yet explicit.

## Goal

Produce a durable shaping document that keeps four things separate but connected:

- requirements: what must be true
- appetite: the fixed budget and cut line
- shapes: materially different ways to satisfy the requirements
- selection evidence: why a human chose one direction

Shaping ends when a direction is explicitly selected or the work stops at a decision-ready comparison. It does not create implementation tasks or begin coding.

## Inputs

Use whichever sources are available:

- an accepted frame
- research, interviews, notes, or requests
- current product behavior or constraints
- existing sketches or proposed mechanisms
- an existing shaping document

When working in an existing product repository, first inspect the applicable project language and durable decisions. Look for `AGENTS.md`, `CONTEXT.md`, `GLOSSARY.md`, `ARCHITECTURE.md`, ADR or decision folders, existing tests, and public interfaces. Reuse established terms and identify existing seams rather than creating parallel vocabulary. Do not create or change a glossary or ADR without authorization.

## Authority and document hierarchy

From high to low:

1. frame — why this problem matters
2. shaping document — requirements, appetite, alternatives, fit, and selection
3. breadboard or slices — concrete behavior and increments
4. implementation plans — build detail

A lower-level discovery may require an upstream planning update. Do not silently rewrite a higher-authority artifact.

Read [artifact consistency](references/artifact-consistency.md) when changing an existing planning stack or reconciling discoveries across levels.

## Required sequence

The formal decision sequence is fixed even when exploration moves back and forth:

1. confirm the frame
2. define and accept criteria
3. set appetite and cut line
4. make materially different shapes visible
5. run fit and reverse-fit checks
6. stop for human selection
7. record the selected direction and hand it to breadboarding

An early mechanism may be preserved in a parking lot, but it does not bypass criteria, appetite, comparison, or selection.

## Step 1: Confirm the frame

Confirm that the work can state:

- the real situation or struggling moment
- the current approach and current result
- the desired outcome
- the relevant boundary
- the evidence level

If these are not clear enough to judge candidate solutions, return to framing instead of manufacturing certainty.

**Complete when:** the shaping document names the accepted frame source and any unresolved framing gaps.

## Step 2: Define and accept requirements

Requirements describe needs, outcomes, or constraints independently of one implementation approach.

Use stable IDs such as `R0`, `R1`, and `R2`. Prefer no more than nine top-level requirements; use sub-requirements when needed.

Recommended statuses:

- Core goal
- Must-have
- Nice-to-have
- Undecided
- Out

Before keeping a requirement, ask whether it would still need to be true if the interface, vendor, runtime, storage method, or architecture changed completely. If not, it is probably a mechanism and belongs in a shape.

Read [requirements and shapes](references/requirements-and-shapes.md) for smell tests, notation, examples, current-system baselines, and flagged unknowns.

**Complete when:** every accepted requirement is independently stated, traceable to the frame or an explicit human decision, and assigned a status.

## Step 3: Set appetite and cut line

Appetite is the fixed time or scope budget the team is willing to spend on the bet. It constrains the candidate shapes; it is not an estimate produced after a preferred solution has already won.

Record:

- time or fixed scope budget
- team shape and review point
- explicit cut line
- uncertainty the team accepts
- unknowns that require a spike before selection or build
- conditions that would cause the appetite to be revisited

If appetite is undecided, preserve ideas in the mechanism parking lot but stop before comparative selection.

**Complete when:** the budget, cut line, accepted uncertainty, and must-resolve unknowns are explicit and human-accepted.

## Step 4: Make materially different shapes visible

Shapes are competing or composable solution directions. Use `CURRENT` as the baseline for an existing product, then letters such as `A`, `B`, and `C` for alternatives. Use numbered parts such as `B1`, `B2`, and `B3` for mechanisms inside a direction.

Each serious shape should:

- have a short title that characterizes the approach
- name concrete mechanisms rather than wishes
- expose meaningful tradeoffs
- fit or declare conflict with the appetite
- flag mechanisms that are still only understood in outline

Do not create nominal variations that differ only in cosmetic detail.

**Complete when:** the current baseline is legible when relevant, materially different options are visible, and every unknown mechanism is flagged.

## Step 5: Run fit and reverse-fit checks

Run three checks:

1. requirements against shapes
2. selected shape parts against requirements
3. each viable shape against appetite

Use binary `✅` or `❌` values for requirement fit. Unknown is not a pass. Put explanations below the table rather than weakening the cells with prose.

The reverse-fit check asks whether every mechanism is justified by at least one accepted requirement. Remove, cut, or explicitly justify mechanisms that have no requirement.

Read [fit checks](references/fit-checks.md) for tables, local component comparisons, failure handling, and decision-ready summaries.

**Complete when:** every candidate has visible requirement fit, appetite fit, cuts, and unresolved spikes; every selected mechanism is justified.

## Step 6: Stop for human selection

Present the comparison and ask the human to:

- select one direction
- request another iteration
- change criteria or appetite
- run a focused spike
- stop the bet

Do not infer selection from enthusiasm, recency, visual polish, or the fact that one shape was explored in more detail.

**Complete when:** the human has made an explicit decision or the artifact clearly states that selection is pending.

## Step 7: Record the decision and hand off

When a direction is selected, record:

- chosen direction and relevant parts
- rationale tied to requirements and appetite
- explicit cuts and non-goals
- accepted uncertainty
- spikes or decisions still required
- any established project terms, ADRs, interfaces, or seams that the selected direction must preserve or intentionally change

Then stop shaping and hand the selected mechanisms to breadboarding. Do not create task groups, select implementation sequence, or write production code inside this skill.

**Complete when:** another person can understand what was selected, what was rejected, why it fits, and what remains unresolved without replaying the conversation.

## Minimal shaping document

```md
# [Project] — Shaping

## Frame source
- ...

## Project language and decisions
- Canonical terms:
- Relevant ADRs or decisions:
- Existing interfaces or seams:
- Terms or decisions this work may introduce:

## Requirements
| ID | Requirement | Status |
|---|---|---|
| R0 | ... | Core goal |

## Appetite
- Budget:
- Team / review point:
- Cut line:
- Accepted uncertainty:
- Must-resolve unknowns:
- Revisit conditions:

## Mechanism parking lot
- ...

## Shapes
### CURRENT: [baseline, when relevant]
| Part | Mechanism | Flag |
|---|---|:---:|
| CURRENT1 | ... | |

### A: [short title]
| Part | Mechanism | Flag |
|---|---|:---:|
| A1 | ... | |

## Fit check
| Req | Requirement | Status | CURRENT | A |
|---|---|---|:---:|:---:|
| R0 | ... | Core goal | ✅ | ✅ |

## Reverse fit check
| Shape part | Mechanism | Requirement(s) served | Justified? |
|---|---|---|:---:|
| A1 | ... | R0 | ✅ |

## Appetite fit
| Shape | Fits? | Required cuts | Uncertainty / spike |
|---|:---:|---|---|
| A | ✅ | ... | ... |

## Decision
- Status: pending | selected | stopped
- Chosen direction:
- Rationale:
- Cuts / non-goals:
- Remaining unknowns:
```

## Guardrails

- Keep requirements separate from mechanisms.
- Set appetite before selection.
- Compare more than one serious path when alternatives genuinely exist.
- Treat `CURRENT` as evidence, not automatically as future intent.
- Preserve stable IDs and rejected alternatives as an audit trail.
- Use a focused spike only for an unknown that blocks a decision.
- Reconcile consequential sketches through `sketch-reconciliation` before silently changing accepted artifacts.
- Stop at the human selection gate.
- Do not create implementation tasks or code.
