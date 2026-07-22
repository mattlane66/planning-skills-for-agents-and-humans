---
name: sketch-reconciliation
description: Reconcile a screenshot, wireframe, mockup, whiteboard, or sketch with existing planning artifacts when visual evidence may change the frame, criteria, scope, or shape.
---

# Sketch Reconciliation

Use a visual to find missing detail, contradictions, and clarifications while preserving the planning record.

## Core rule

Treat the sketch as evidence and a design proposal, not as an automatic source of truth.

```text
Observable visual detail -> mapped planning IDs -> proposed deltas -> human gate -> accepted artifact updates
```

The user's accompanying words outrank an inference from the image. Existing selected artifacts remain authoritative until the user accepts a change.

## Inputs

Use:

- the attached or referenced visual
- the user's explanation of what to notice
- the current frame, shaping artifact, and selected shape when present
- the accepted breadboard or slices when present

If the visual is unavailable or too unclear to inspect, ask for a readable attachment or a description. Do not pretend to see it.

## Procedure

### 1. Establish scope

State which visual and planning artifacts are being reconciled. Preserve their existing stable IDs.

If the user points to a specific concern, analyze that first before scanning for secondary implications.

### 2. Record observations before interpretations

List only what is visibly present: labels, controls, regions, displayed values, arrows, grouping, hierarchy, and repeated states.

Assign observation IDs such as `OBS1`, `OBS2`, and `OBS3`.

| Observation | Visible evidence | Confidence |
|---|---|:---:|
| OBS1 | Date label appears above the results table | high |

Do not infer hidden behavior from appearance alone. A text field does not prove parsing behavior. An arrow does not prove persistence. A static value does not prove editability.

### 3. Map observations to the plan

Map each observation to existing IDs where possible.

| Observation | Requirement(s) | Shape part(s) | Breadboard IDs | Status by layer |
|---|---|---|---|---|
| OBS1 | R2 | - | - | `R2: covered; Shape: missing` |

Use these statuses:

- `covered` - the current artifacts already express it
- `clarifies` - it makes an existing item more concrete without changing scope
- `missing` - the visual reveals behavior or state absent from the artifacts
- `conflicts` - it disagrees with selected behavior or a boundary
- `ambiguous` - the visual supports more than one interpretation

Status is layer-specific. When one observation is covered in one layer but missing in another, say so in the same cell (`R2: covered; Shape A: missing`) or use separate rows. Do not collapse a cross-layer difference into one status.

### 4. Separate needs from mechanisms

For each missing or conflicting item, decide which layer it belongs in:

- requirement - a need or constraint that should survive a different solution
- shape part - a mechanism chosen to satisfy requirements
- breadboard - a place, affordance, store, branch, or wire
- slice - a boundary, demo path, exclusion, dependency, or verification target

Do not turn every drawn control into a requirement. Do not hide a newly discovered need only inside a UI mechanism.

### 5. Propose a delta set

Show proposed changes before applying them unless the user explicitly asked to update the artifacts immediately.

| Delta | Target | Proposed change | Evidence | Fit / scope impact | Decision |
|---|---|---|---|---|---|
| D1 | A1 | Add a persistent date-state affordance | OBS1 + user note | clarifies R2; no scope expansion | pending / accept / revise / reject / defer |

For ambiguous observations, ask a focused question or present mutually exclusive interpretations. Never choose product behavior from visual guesswork.

### 6. Stop at the reconciliation gate

Ask the human to accept, revise, reject, or defer the proposed deltas when they would change requirements, selected mechanisms, scope, or behavior. Mark an undecided proposal as `pending`; never make it look accepted by omission.

You may skip a separate confirmation turn only when the user explicitly instructs the change, for example: "Add a requirement that the date is always visible and update the shape."

### 7. Apply accepted changes as one ripple

When changes are accepted:

1. update requirements as needs, not UI choices
2. update the selected shape as mechanisms
3. update affected breadboard places, affordances, stores, branches, and wires
4. update slice boundaries, demos, exclusions, or tests when affected
5. preserve stable IDs; add new IDs rather than repurposing old meanings
6. mark changed or added rows with `🟡` during review
7. rerun the fit check and reverse fit check when requirements or shape parts change
8. list downstream artifacts that are now stale or were updated

Do not silently update only one layer when the accepted delta affects several.

Use ripple statuses consistently:

- `current` - inspected and already aligned with accepted decisions
- `updated` - changed during this reconciliation
- `stale` - an accepted delta requires a later update
- `not affected` - inspected and no update is needed for this delta
- `not provided` - absent from the reconciliation inputs
- `not assessed` - may exist, but was outside the inspected scope

## Output

Create or update a reconciliation record using `templates/sketch-reconciliation.md` when the visual produces durable decisions.

The record must include:

- source visual and related artifacts
- observation inventory
- observation-to-plan mapping
- ambiguity and conflict notes
- proposed deltas and decisions
- accepted changes
- fit-check impact
- downstream ripple status

For a small clarification, the same structure may be shown in chat without creating a file.

## Quality checks

Before finishing, verify:

- every claimed visual fact is actually visible
- every interpretation is labeled as interpretation when not explicit
- every proposed change maps to an observation or the user's words
- requirements remain independent of one solution mechanism
- selected artifacts did not change without authorization
- accepted changes were applied across every affected layer
- fit checks were rerun when requirements or shape parts changed
- unresolved ambiguity remains visible
- undecided or deferred deltas remain visibly distinct from accepted changes

## Do not

- treat visual polish as a requirement
- infer hidden state, persistence, validation, or navigation from a static image
- overwrite a selected shape because a sketch looks newer
- invent interactions not shown or described
- renumber stable IDs for cosmetic consistency
- leave the shaping and breadboard artifacts contradictory after an accepted change
