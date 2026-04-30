---
name: shaping
description: Collaboratively shape a problem and compare solution directions before implementation.
planning: true
shaping: true
---

# Shaping

Use this skill when a request is still ambiguous, multiple solution directions are possible, or the team needs a durable planning artifact before building.

## Goal

Turn a fuzzy request into a concrete shaping document that keeps three things separate but connected:

- the requirements
- the solution directions
- the evidence that a chosen direction actually fits

## Document hierarchy

Planning artifacts live at different levels of abstraction. Truth has to stay consistent across those levels.

From high to low:

1. **Frame** — the why: source, problem, outcome, boundaries
2. **Shaping doc** — the what and candidate how: requirements, shapes, fit checks, selected direction
3. **Breadboard or slices doc** — the concrete behavior and increments: places, affordances, stores, wiring, slice boundaries
4. **Slice plans** — the per-slice implementation detail

Each lower level adds detail. Each higher level is a designed view into the levels below.

Changes ripple both ways:

- change at a higher level may require downstream updates
- a discovery at a lower level may require updates upstream

Whenever making a change:

1. identify which level you are touching
2. ask whether it affects artifacts above or below
3. update affected layers in the same operation when possible

## Core idea

Shaping is iterative. Requirements sharpen the shape. Shapes reveal missing requirements. The work is to keep both visible at the same time without collapsing them into each other.

## Starting points

You can start from either side:

- **Start from requirements** — describe the problem, constraints, or pain points first, then let shapes emerge
- **Start from a shape** — capture a solution already in mind, then extract or revise requirements as you go

There is no required order. Requirements and shapes inform each other throughout.

## Requirements

Requirements describe what must be true of the solution. They should be stated independently of any one implementation approach.

Use identifiers like `R0`, `R1`, `R2`.

Recommended statuses:

- Core goal
- Must-have
- Nice-to-have
- Undecided
- Out

Keep the top level scannable. Prefer no more than 9 top-level requirements. If requirements proliferate, group related ones into chunks and use sub-requirements such as `R3.1`, `R3.2` rather than letting the top level grow without structure.

### Requirement smell test

Before keeping a line in `R`, ask:

1. Would this still need to be true if we built the solution in a completely different way?
2. Does it name a specific UI, runtime, vendor, protocol, storage method, or architecture?
3. Is this describing an underlying need or constraint, or just one proposed way to satisfy it?
4. Can this be rewritten as a capability, outcome, or constraint instead of an implementation choice?

If a line names a mechanism, it probably belongs in the shape, not the requirements.

Examples:

- ❌ `Use a TUI`
- ✅ `User can inspect and change the current state from one interaction surface`

- ❌ `Fetch timezone data from the internet on every load`
- ✅ `Timezone data must be accurate at runtime for the requested locale`

## Shapes

Shapes are competing or composable solution directions.

Use letters for alternative directions:

- `A`, `B`, `C`
- `CURRENT` should be used as the standard baseline when describing the existing system before proposing alternatives

Use numbered parts for mechanisms inside a chosen direction:

- `B1`, `B2`, `B3`

If a part has internal alternatives, use nested notation:

- `B3-A`, `B3-B`

Give each serious shape a short title that characterizes the approach.

### CURRENT as baseline

When the work touches an existing system, model that existing behavior as `CURRENT` first. Treat it as the standard baseline shape, not an optional flourish.

Use `CURRENT` to:

- show what exists today
- anchor proposed changes against reality
- make deltas legible before introducing `A`, `B`, or `C`

Then compare alternatives against `CURRENT` rather than shaping in a vacuum.

### Notation persistence

Keep notation stable throughout the conversation as an audit trail.

When refining or composing later directions, reference earlier parts rather than silently renaming everything. Stable notation helps the user track what changed and why.

## Shape parts and flagged unknowns

Shape parts should describe mechanisms, not intentions.

- ✅ `Persist filter state in the URL and restore it on load`
- ❌ `State should work better`

Use a flag when a mechanism is described at a high level but is not yet concretely understood.

| Part | Mechanism | Flag |
|------|-----------|:----:|
| B1 | Save state in URL | |
| B2 | Integrate local LLM command parser | ⚠️ |

Meaning:

- empty flag = mechanism is concretely understood enough to count as known
- `⚠️` = described in outline, but the how is still unresolved

A flagged unknown should not be treated as confidently solved in a fit check. Resolve it or spike it.

## Working rules

1. Requirements state needs, not mechanisms.
2. Shape parts state mechanisms, not wishes.
3. Keep the notation stable as the conversation evolves.
4. When a fit check fails, either improve the shape or add the missing requirement.
5. When a shape is selected, detail it rather than inventing a new sibling shape unless it is truly an alternative.
6. If a requirement names a mechanism, rewrite it as a need or move it into the shape.
7. Avoid tautologies where the shape merely repeats the requirement in different words.
8. Prefer vertical mechanisms over horizontal buckets where possible.
9. If a shape passes visible checks but still feels wrong, there is probably a missing requirement.
10. Model the existing system as `CURRENT` when the change is not greenfield.

## Possible actions

These can happen in any order as the shaping evolves:

- populate requirements
- sketch a shape at a high level
- detail a shape into parts or affordances
- explore alternatives for a part
- test a shape with a fit check
- extract new requirements revealed by the fit check
- spike an unknown
- decide among alternatives
- breadboard the selected shape
- slice the breadboarded shape

## Recommended document structure

```md
---
planning: true
shaping: true
---

# [Project] — Shaping

## Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| R0 | ... | Core goal |

## Shapes

### CURRENT: [Existing system baseline]

| Part | Mechanism | Flag |
|------|-----------|:----:|
| CURRENT1 | ... | |

### A: [Short title]

| Part | Mechanism | Flag |
|------|-----------|:----:|
| A1 | ... | |

### B: [Short title]

| Part | Mechanism | Flag |
|------|-----------|:----:|
| B1 | ... | |

## Fit Check

| Req | Requirement | Status | CURRENT | A | B |
|-----|-------------|--------|---------|---|---|
| R0 | ... | Core goal | ✅ | ✅ | ❌ |

## Reverse Fit Check

| Shape Part | Mechanism | Requirement(s) Served | Justified? |
|------------|-----------|------------------------|:----------:|
| B1 | ... | R2, R4 | ✅ |

## Decision

Chosen direction: B

## Detail B

[Optional deeper breakdown or breadboard handoff]
```

## Fit checks

Use one table to compare requirements against the available shapes.

Rules:

- Use full requirement text in the table
- Use binary values only: `✅` or `❌`
- Put explanations below the table, not inside shape cells
- If something is still unknown, it is not yet a pass

If something passes every visible check but still feels wrong, there is probably a missing requirement. Articulate it, add it, and re-run the fit check.

### Reverse fit check: shape parts against requirements

After checking requirements against shapes, also check whether every selected shape part is justified by at least one requirement.

Use this to catch unjustified mechanisms, accidental scope creep, or parts that exist because they sounded useful rather than because they satisfy the shaped problem.

| Shape Part | Mechanism | Requirement(s) Served | Justified? |
|------------|-----------|------------------------|:----------:|
| B1 | Persist filter state in the URL | R2, R4 | ✅ |
| B2 | Add export-to-CSV action | — | ❌ |

Rules:

- Use binary values only: `✅` or `❌`
- If a part is not justified, remove it, mark it Cut, or add the missing requirement and rerun the fit check.
- Do not let implementation convenience create untracked scope.
- A flagged unknown can be justified by a requirement but still not understood enough to pass the main fit check.

## Spikes

A spike is an investigation task used when a part is still uncertain and you need objective information about how something works or what concrete steps would be required.

Use a spike to:

- learn how the current system works in the relevant area
- identify what would need to change to achieve the mechanism
- surface constraints that affect the solution
- reduce uncertainty before pretending a flagged part is understood

Minimal spike structure:

```md
## [Part] Spike: [Title]

### Context
Why this needs investigation.

### Goal
What we are trying to learn.

### Questions
| # | Question |
|---|----------|
| Q1 | ... |
| Q2 | ... |

### Acceptance
Spike is complete when all questions are answered and the mechanism can be described concretely.
```

## Transition to breadboarding

Move from shaping to breadboarding when:

- one direction is chosen
- its mechanisms are concrete enough to map
- you need to show places, affordances, stores, and wiring

## Output standard

Always leave behind a document that someone else could read later and understand without replaying the entire conversation.
