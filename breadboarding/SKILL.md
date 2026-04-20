---
name: breadboarding
description: Map a chosen solution into places, affordances, consequences, stores, and wiring.
planning: true
---

# Breadboarding

Use this skill when the team needs to understand how a chosen solution behaves, where the user is, what they can do there, and what hidden system consequences matter.

## Goal

Produce a legible system map that shows:
- the places a person or operator can be in
- the affordances available in those places
- the important hidden system consequences
- the stores or state that matter
- the wiring between all of them

## What breadboarding is

Breadboarding is a lightweight UI shorthand.

It separates what users can interact with in the interface from what happens in the code or design system underneath.

The places act like interface endpoints or bounded states. The affordances show what the user can do there. The wiring explains what happens between what the user sees.

Because it uses words instead of pictures, and because the important things are the components and their connections, you can quickly play out an idea and judge whether the sequence of actions actually serves the use case.

## Center of gravity

A breadboard is mainly about:
- place
- affordance
- visible consequence
- the hidden system behavior that matters to the product behavior

It is **not** mainly a service graph.

If the diagram starts to read like:
- service → service → store → render

then it is probably too implementation-heavy.

Prefer wording that stays tied to product behavior, such as:
- check duplicate
- save list
- restore saved state on launch
- hide bought items from current view

rather than internal decomposition such as:
- normalize service
- filtering service
- state manager
- renderer pipeline

## Core concepts

### Places
A place is a bounded context of interaction. It is where someone is, in practical terms, because it determines what they can do next.

Examples:
- a page
- a blocking modal
- a full-screen edit mode
- a meaningful system boundary when it affects product behavior

Ask:
- what place is the user in?
- what can they do from here?
- what visibly changes after they do it?

### Make meaningful user-visible states first-class

If a state changes what the user can do next or what they can see, consider representing it as its own place.

Examples:
- empty state
- duplicate warning shown
- bought items hidden
- restored-on-launch state

Do not hide important user-visible states inside only non-UI affordances.

### Affordances
Affordances are the things that can be acted upon or that produce effects.

Use these prefixes:
- `U` for user-facing affordances
- `N` for non-UI/code affordances
- `S` for stores or state
- `P` for places

Keep non-UI affordances close to product-relevant consequences.

### Wiring
Wiring explains behavior.

Track two kinds:
- **Wires Out** for control flow: what triggers what
- **Returns To** for data flow or visible consequence: where outputs or state are consumed

A good breadboard should help answer:
- what can the user do here?
- what happens next?
- what changes in the product?

### Show product-relevant branches explicitly

When a hidden rule can lead to different user-visible outcomes, represent that split in the breadboard.

Examples:
- duplicate → show duplicate message
- not duplicate → add item and show updated list
- hide-bought on → bought item disappears from current view
- hide-bought off → bought item remains visible with updated state

## Required tables

### Places table

| ID | Place | Description |
|----|-------|-------------|
| P1 | Search page | Main search experience |

### UI affordances table

| ID | Place | Component | Affordance | Control | Wires Out | Returns To |
|----|-------|-----------|------------|---------|-----------|------------|
| U1 | P1 | search | input field | type | → N1 | — |

### Non-UI affordances table

| ID | Place | Component | Affordance | Control | Wires Out | Returns To |
|----|-------|-----------|------------|---------|-----------|------------|
| N1 | P1 | search | query handler | call | → N2 | — |

### Stores table

| ID | Place | Store | Description |
|----|-------|-------|-------------|
| S1 | P1 | results | Search results array |

## Procedure

1. Identify the workflow or effect to explain.
2. List the places involved.
3. Identify the concrete affordances in each place.
4. Add the hidden system consequences that matter to product behavior.
5. Add the stores that shape the behavior.
6. Fill in control flow with **Wires Out**.
7. Fill in data flow and visible consequence with **Returns To**.
8. Check that every visible effect can be explained by the wiring.

## Quality checks

- Every displayed UI element that depends on data should have an incoming source.
- Every code affordance should either trigger something, return something, or both.
- Avoid vague affordance names like `database`, `logic`, or `handler stuff`.
- Prefer real names that point to a thing someone can find in code or design.
- Prefer product-facing hidden behavior over abstract service decomposition.
- Make important user-visible consequences first-class.
- Make product-relevant branches explicit when they change what the user sees next.

## Recommended output structure

```md
---
planning: true
---

# [Project] — Breadboard

## Places
[table]

## UI Affordances
[table]

## Non-UI Affordances
[table]

## Stores
[table]

## Notes
- [important constraints, open questions, or assumptions]
```

## Mermaid diagrams

A Mermaid diagram is optional. The tables are the source of truth.

If you add a diagram:
- group nodes by place first
- make affordances under each place visible
- keep IDs consistent with the tables
- show product consequences, not only internal calls
- treat the diagram as a rendering of the tables, not the other way around

## Transition to slicing

Slice only after the breadboard is concrete enough that you can group affordances into demoable vertical increments.

## Sequencing slices: two passes

Slice order is not intuitive. Sequence slices with two passes, in order.

### Pass 1 — Dependencies
Map which slices depend on other slices.

A slice depends on another when it requires affordances, data structures, routes, or stores that the other slice produces.

Start with slices that have no dependencies and work upward through the causal chain. This gives you the minimum valid ordering — constraints you cannot violate.

### Pass 2 — Unknowns
Among slices that are valid starting points, ask: which has the biggest unknown?

An unknown is something where you do not yet know if it is feasible, how it works, or how long it will take.

Move the slice with the biggest unknown as early as possible. This creates the most time to resolve the hard problem before it becomes a crisis.

Start by identifying what is routine and familiar. What remains are the unknowns.

The final sequence is:
- dependencies set the floor
- unknowns break ties within that floor

## Exit conditions are defined right-to-left

A slice is done when it produces the output the next slice needs as input — not when it is abstractly complete.

Before finalizing each slice boundary, look at what comes immediately after it in the sequence.

Ask: what does the next slice need in order to start?

The current slice must deliver exactly that — no more, no less.

This prevents two common failure modes:
- **Scope creep left** — building things that are only needed much later, before the next slice actually needs them
- **Underdelivery** — stopping before the next slice has what it needs to begin

When writing the demo statement for each slice, include what it produces for the next slice to consume.

Use this format:
- `Produces: [what this slice outputs for the next slice]`

If you cannot name what the slice produces for the next one, the slice boundary may be wrong.

## Cutting

When the breadboard implies more than 9 slices, cut — do not compress.

Compressing forces slices that are too large to demo a single mechanism. Cutting removes mechanisms from the current cycle entirely.

Present cut candidates explicitly. Do not silently merge or omit them.

Use this format:
- **In scope (this cycle):** Slices V1–VN demonstrating mechanisms X, Y, Z
- **Cut (not this cycle):** Mechanisms A, B — reason for deferral

The human decides what gets cut. This is an appetite decision. The breadboard's job is to make the trade-off visible, not to make the call.

When a slice is cut, add a **Cut** section at the bottom of the slice summary with a one-line reason. Do not delete it. Deferred work is different from rejected work.

Cutting is also available later at implementation gates. If a slice runs long or reveals unexpected complexity, a later slice can be cut rather than extending the timeline.
