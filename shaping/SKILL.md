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

Shaping may use prose, sketches, candidate breadboards, and focused spikes to make a possible solution clear enough to judge. Those are shaping techniques, not automatic sources of accepted future intent.

Shaping ends when a direction is explicitly selected or the work stops at a decision-ready comparison. It does not create implementation tasks or begin coding.

## Inputs

Use whichever sources are available:

- an accepted frame
- research, interviews, notes, or requests
- current product behavior or constraints
- existing sketches or proposed mechanisms
- current-state or candidate-shape breadboards
- an existing shaping document

When working in an existing product repository, first inspect the applicable project language and durable decisions. Look for `AGENTS.md`, `CONTEXT.md`, `GLOSSARY.md`, `ARCHITECTURE.md`, ADR or decision folders, existing tests, and public interfaces. Reuse established terms and identify existing seams rather than creating parallel vocabulary. Do not create or change a glossary or ADR without authorization.

## Authority and document hierarchy

From high to low:

1. frame — why this problem matters
2. shaping document — requirements, appetite, alternatives, fit, and selection
3. candidate-shape breadboards and focused spikes — exploratory evidence subordinate to one candidate
4. accepted selected-design breadboard or slices — concrete selected behavior and increments
5. implementation plans — build detail

A lower-level discovery may require an upstream planning update. Do not silently rewrite a higher-authority artifact.

Read [artifact consistency](references/artifact-consistency.md) when changing an existing planning stack or reconciling discoveries across levels.

## Required sequence

The formal decision sequence is fixed even when exploration moves back and forth:

1. confirm the frame
2. define and accept criteria
3. set appetite and cut line
4. make materially different shapes visible
5. resolve only the uncertainties needed to compare them, using candidate breadboards or focused spikes when useful
6. run fit and reverse-fit checks
7. stop for human selection
8. record the selected direction and reconcile it into a selected-design breadboard

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

Use the Appetite section in `templates/shaping.md` for a compact record or `templates/appetite-card.md` when ownership, rationale, and revisit conditions need a separate durable artifact.

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

Use the cheapest representation that makes the shape judgeable:

- mechanism tables for a straightforward candidate
- fat-marker or rough sketches when spatial arrangement matters
- a `candidate-shape` breadboard when places, affordances, consequences, stores, or wiring must be understood before comparison
- a focused spike when a technical unknown blocks an honest fit judgment

Candidate breadboards may be partial and may differ in depth. Do not add detail merely to make alternatives look symmetrical. Read `breadboarding/references/candidate-shape-mode.md` and invoke the breadboarding skill in candidate-shape mode when that technique is needed.

Do not create nominal variations that differ only in cosmetic detail.

**Complete when:** the current baseline is legible when relevant, materially different options are visible, and every unknown mechanism is either flagged or resolved enough for comparison.

## Step 5: Resolve candidate uncertainty without selecting

For each candidate, identify the smallest unanswered question that could change its fit, appetite, or viability.

Use candidate breadboarding when the uncertainty is behavioral or structural. Use a focused spike when the uncertainty is technical or empirical. Return the result to the shaping artifact as evidence about:

- requirement fit
- reverse fit
- appetite fit
- cuts or rabbit holes
- assumptions that remain unresolved

A candidate breadboard is subordinate to its named shape. It cannot select itself, feed slice selection, define build scope, or become accepted future intent.

**Complete when:** every decision-relevant uncertainty is resolved, explicitly accepted, or visible as a reason not to select the candidate.

## Step 6: Run fit and reverse-fit checks

Run three checks:

1. requirements against shapes
2. shape parts against requirements
3. each viable shape against appetite

Use binary `✅` or `❌` values for requirement fit. Unknown is not a pass. Put explanations below the table rather than weakening the cells with prose.

The reverse-fit check asks whether every mechanism is justified by at least one accepted requirement. Remove, cut, or explicitly justify mechanisms that have no requirement.

Candidate breadboards and spike results may support the judgment, but they do not outrank the shaping document or decide which shape wins.

Read [fit checks](references/fit-checks.md) for tables, local component comparisons, failure handling, and decision-ready summaries.

**Complete when:** every candidate has visible requirement fit, appetite fit, cuts, and unresolved spikes; every mechanism under consideration is justified or explicitly cut.

## Step 7: Stop for human selection

Present the comparison and ask the human to:

- select one direction
- request another iteration
- change criteria or appetite
- run another focused candidate breadboard or spike
- stop the bet

Do not infer selection from enthusiasm, recency, visual polish, or the fact that one shape was explored in more detail.

**Complete when:** the human has made an explicit decision or the artifact clearly states that selection is pending.

## Step 8: Record the decision and hand off

When a direction is selected, record:

- chosen direction and relevant parts
- rationale tied to requirements and appetite
- explicit cuts and non-goals
- accepted uncertainty
- spikes or decisions still required
- any established project terms, ADRs, interfaces, or seams that the selected direction must preserve or intentionally change

Then reconcile the selected mechanisms into a `selected-design` breadboard. A candidate breadboard does not automatically become authoritative: remove unselected mechanisms, reconcile surviving rows against the accepted shape and cuts, preserve unresolved gaps explicitly, and obtain acceptance before slicing.

Detailed selected-design breadboarding may expose a shaping conflict. When it does, return the conflict to shaping for an explicit decision to revise the shape, cut behavior, run a focused spike, reopen selection, or stop the bet. Do not silently change the selected shape.

Do not dump or cluster implementation tasks, select committed slices, create a build sequence, or write production code inside shaping.

**Complete when:** another person can understand what was selected, what was rejected, why it fits, how any candidate evidence was reconciled, and what remains unresolved without replaying the conversation.

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

## Candidate evidence
| Candidate | Evidence | Question resolved | Fit implication | Remaining uncertainty |
|---|---|---|---|---|
| A | candidate breadboard or spike | ... | ... | ... |

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
- Candidate breadboard promotion/reconciliation:
```

## Guardrails

- Keep requirements separate from mechanisms.
- Set appetite before selection.
- Compare more than one serious path when alternatives genuinely exist.
- Use candidate breadboards only to resolve decision-relevant uncertainty.
- Keep candidate breadboards subordinate to the shaping artifact and named candidate.
- Do not let unequal exploratory depth imply selection.
- Treat `CURRENT` as evidence, not automatically as future intent.
- Preserve stable IDs and rejected alternatives as an audit trail.
- Use a focused spike only for an unknown that blocks a decision.
- Reconcile consequential sketches through `sketch-reconciliation` before silently changing accepted artifacts.
- Stop at the human selection gate.
- Promote or reconcile a candidate breadboard only after explicit selection.
- Do not create implementation tasks or code.