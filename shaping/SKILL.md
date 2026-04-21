---
name: shaping
description: Collaboratively shape a problem and compare solution directions before implementation.
planning: true
---

# Shaping

Use this skill when a request is still ambiguous, multiple solution directions are possible, or the team needs a durable planning artifact before building.

## Goal

Turn a fuzzy request into a concrete shaping document that keeps three things separate but connected:
- the requirements
- the solution directions
- the evidence that a chosen direction actually fits

## Core idea

Shaping is iterative. Requirements sharpen the shape. Shapes reveal missing requirements. The work is to keep both visible at the same time without collapsing them into each other.

## Starting points

You can start from either side:
- **Start from requirements** — describe the problem, constraints, or pain points first, then let shapes emerge
- **Start from a shape** — capture a solution already in mind, then extract or revise requirements as you go

There is no required order. Requirements and shapes inform each other throughout.

## Main artifacts

### Requirements
Requirements describe what must be true of the solution. They should be stated independently of any one implementation approach.

Use identifiers like `R0`, `R1`, `R2`.

Recommended statuses:
- Core goal
- Must-have
- Nice-to-have
- Undecided
- Out

Keep the top level scannable. If requirements proliferate, group related ones rather than letting the top level grow without structure.

### Requirement smell test

Before keeping a line in `R`, ask:

1. Would this still need to be true if we built the solution in a completely different way?
2. Does it name a specific UI, runtime, vendor, protocol, storage method, or architecture?
3. Is this describing an underlying need or constraint, or just one proposed way to satisfy it?
4. Can this be rewritten as a capability, outcome, or constraint instead of an implementation choice?

If a line names a mechanism, it probably belongs in the shape, not the requirements.

Common signs that an `R` is really a solution choice:
- names a specific interface like TUI, modal, web app, or input field
- names a specific implementation like local LLM, cron job, REST API, SQLite, or queue
- names a specific provider or dependency
- describes how the system should work internally rather than what must be true

Examples:
- ❌ `Use a TUI`
- ✅ `User can inspect and change the current state from one interaction surface`

- ❌ `Fetch timezone data from the internet on every load`
- ✅ `Timezone data must be accurate at runtime for the requested locale`

- ❌ `Use a local LLM to change locales and dates`
- ✅ `User can change locales and time window through natural-language input`

### Shapes
Shapes are competing or composable solution directions.

Use letters for alternative directions:
- `A`, `B`, `C`
- `CURRENT` may be used to describe the existing system as a baseline

Use numbered parts for mechanisms inside a chosen direction:
- `B1`, `B2`, `B3`

If a part has internal alternatives, use nested notation:
- `B3-A`, `B3-B`

Give each serious shape a short title that characterizes the approach.

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
---

# [Project] — Shaping

## Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| R0 | ... | Core goal |

## Shapes

### A: [Short title]

| Part | Mechanism |
|------|-----------|
| A1 | ... |

### B: [Short title]

| Part | Mechanism |
|------|-----------|
| B1 | ... |

## Fit Check

| Req | Requirement | Status | A | B |
|-----|-------------|--------|---|---|
| R0 | ... | Core goal | ✅ | ❌ |

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

## Communication

### Show full tables

When displaying requirements, shapes, or fit checks, show the full table rather than a summary whenever practical. Shaping is collaborative negotiation. Partial views hide what matters.

### Keep changes visible

When revising tables, make changed lines easy to spot. The user should not have to mentally diff a whole table to understand what moved.

## Spikes

A spike is an investigation task used when a part is still uncertain and you need objective information about how something works or what concrete steps would be required.

### Purpose

Use a spike to:
- learn how the current system works in the relevant area
- identify what would need to change to achieve the mechanism
- surface constraints that affect the solution
- reduce uncertainty before pretending a flagged part is understood

### File management

Create spikes in their own file when the investigation is substantial.

Examples:
- `spike-llm-runtime.md`
- `spike-search-index.md`

### Good spike questions

Ask questions about mechanics, for example:
- Where is the current logic?
- How does this behavior actually happen today?
- What would need to change to support the proposed mechanism?
- What constraints or dependencies affect this part?

Avoid vague yes/no questions and avoid using the spike only to guess effort.

### Minimal spike structure

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

## Detailing a selected shape

When a shape is chosen, detail it rather than turning it into a new sibling shape.

Use `Detail B` to show that the work is a deeper breakdown of shape `B`, not a new alternative.

Detailing usually produces:
- places
- UI affordances
- non-UI affordances
- stores
- wiring

At that point, use the breadboarding skill.

## Kick-off: From selected shape to slices

Use this as an optional exercise before handing work off to breadboarding or slice planning.

The purpose is to make the full implied scope visible and externalize the grouping and sequencing work that strong builders often do in their heads.

### Step 1 — Dump
List every task implied by the selected shape.

Do not organize yet. Prioritize completeness over structure.

### Step 2 — Affinitize
Group tasks by asking: which tasks can be completed together, in isolation from the rest?

Use unnamed groups first. Do not name them until they are filled.

This helps the grouping emerge from the actual work rather than from pre-conceived categories.

Constraints:
- maximum 10 groups
- groups remain unnamed until populated
- a task belongs in a group when it can be completed in isolation alongside the others in that group

### Step 3 — Name
Once groups are filled, give each one a name.

Names should reflect what the group does. These names become scope handles — shorthand for the mechanisms being built.

### Step 4 — Flag unknowns
Look across the named groups and ask: which are more unknown than the others?

Start by identifying what is routine and familiar. What remains are the unknowns.

Flag unknown groups explicitly before sequencing.

Output from this exercise:
- named groups
- unknown groups flagged

This output feeds naturally into breadboarding and then into slice sequencing.

## Documents and ripple consistency

Shaping usually leaves behind multiple planning artifacts at different levels.

Typical stack:
- frame
- shaping doc
- breadboard or slices doc
- slice plans

Truth has to stay consistent across levels. If a mechanism changes in the shaping doc, downstream artifacts may need updates. If implementation planning reveals a new mechanism, the shaping doc may need to reflect it.

Whenever making a change:
1. identify which artifact level you are touching
2. ask whether it affects artifacts above or below
3. update affected layers in the same operation when possible

## Good prompts for the shaping conversation

- What problem is worth solving here?
- What constraints are actually non-negotiable?
- What solution directions are meaningfully different?
- What requirement is this part satisfying?
- What requirement is still not accounted for?
- Are we missing a requirement because the current options all feel wrong?
- Is this requirement actually a solution choice in disguise?
- If we changed the interface or implementation completely, would this still need to be true?
- Which parts are still flagged unknowns?
- What should we spike next?

## Transition to breadboarding

Move from shaping to breadboarding when:
- one direction is chosen
- its mechanisms are concrete enough to map
- you need to show places, affordances, stores, and wiring

## Output standard

Always leave behind a document that someone else could read later and understand without replaying the entire conversation.
