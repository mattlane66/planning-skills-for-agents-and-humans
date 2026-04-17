---
name: shaping
description: Use when you need to collaboratively define a problem, compare solution directions, and turn the selected approach into a buildable planning artifact.
---

# Shaping

Shaping is the work of making a problem and a solution legible enough to build without pretending uncertainty is gone.

The core move is to keep problem statements separate from solution mechanisms long enough to compare options honestly.

---

## Core Artifacts

### Requirements
Requirements describe what must be true for the work to count as successful.

Use stable identifiers such as `R0`, `R1`, `R2`.

Keep requirements independent from any one proposed solution.

Recommended status labels:
- Core goal
- Must-have
- Nice-to-have
- Undecided
- Out

### Shapes
Shapes are distinct approaches, usually labeled `A`, `B`, `C`.

A shape is not implementation detail. It is the chosen structure of the solution.

Within a shape, break the approach into parts such as `A1`, `A2`, `A3`.

Each part should describe a mechanism, not a wish.

- Good: `Persist filter state in the URL and restore it on load`
- Bad: `State should work better`

### Fit Check
Use a single table to compare requirements against shapes.

| Req | Requirement | Status | A | B | C |
|-----|-------------|--------|---|---|---|
| R0 | User can resume where they left off | Must-have | ✅ | ❌ | ✅ |

Use binary outcomes in the shape columns:
- `✅` = the shape clearly satisfies the requirement
- `❌` = the shape does not yet satisfy it

If something feels wrong even though a shape passes, the missing piece is usually a missing requirement.

---

## Working Sequence

1. Start from the problem or from a proposed shape.
2. Write or refine requirements.
3. Sketch two or more solution directions when useful.
4. Break each serious option into concrete parts.
5. Compare options with a fit check.
6. Select or compose a final direction.
7. Detail the selected shape into affordances or slices.

This is iterative, not linear.

---

## Rules of Good Shaping

### Requirements stay solution-agnostic
Write the need, not the preferred implementation.

### Shape parts must be mechanisms
A part should say what gets built or changed in the system.

### Avoid tautologies
Do not restate the requirement as if it were a solution part.

### Prefer vertical mechanisms
Keep data, logic, and UI close to the feature they support instead of splitting them into horizontal buckets too early.

### Keep the artifact readable
Try not to exceed nine top-level requirements. Group related requirements when needed.

---

## Detailing a Selected Shape

When a shape is chosen, detail it rather than renaming it as a new sibling option.

Use a label such as `Detail B` to show that the work is a breakdown of shape `B`, not a new alternative.

Detailing usually produces:
- places
- UI affordances
- non-UI affordances
- state stores
- wiring

At that point, use the breadboarding skill.

---

## Documents

A practical stack of planning docs usually looks like this:

| Document | Purpose |
|----------|---------|
| Frame | Why this work matters now |
| Shaping doc | Requirements, options, parts, and fit check |
| Breadboard or slices doc | Concrete system structure and build order |
| Slice plans | Implementation-ready steps for one slice at a time |

When one layer changes, check whether the layers above or below also need updates.

---

## Minimal Template

```markdown
---
planning: true
---

# [Project] — Shaping

## Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| R0 | ... | Core goal |

## A: [Approach title]

| Part | Mechanism |
|------|-----------|
| A1 | ... |

## B: [Approach title]

| Part | Mechanism |
|------|-----------|
| B1 | ... |

## Fit Check

| Req | Requirement | Status | A | B |
|-----|-------------|--------|---|---|
| R0 | ... | Core goal | ✅ | ❌ |
```
