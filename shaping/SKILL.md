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

### Shapes
Shapes are competing or composable solution directions.

Use letters for alternative directions:
- `A`, `B`, `C`

Use numbered parts for mechanisms inside a chosen direction:
- `B1`, `B2`, `B3`

If a part has internal alternatives, use nested notation:
- `B3-A`, `B3-B`

## Working rules

1. Requirements state needs, not mechanisms.
2. Shape parts state mechanisms, not wishes.
3. Keep the notation stable as the conversation evolves.
4. When a fit check fails, either improve the shape or add the missing requirement.
5. When a shape is selected, detail it rather than inventing a new sibling shape unless it is truly an alternative.

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

## Good prompts for the shaping conversation

- What problem is worth solving here?
- What constraints are actually non-negotiable?
- What solution directions are meaningfully different?
- What requirement is this part satisfying?
- What requirement is still not accounted for?
- Are we missing a requirement because the current options all feel wrong?

## Transition to breadboarding

Move from shaping to breadboarding when:
- one direction is chosen
- its mechanisms are concrete enough to map
- you need to show places, affordances, stores, and wiring

## Output standard

Always leave behind a document that someone else could read later and understand without replaying the entire conversation.
