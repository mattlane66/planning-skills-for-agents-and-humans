---
name: breadboarding
description: Map a chosen solution into places, affordances, consequences, stores, and wiring.
planning: true
shaping: true
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

The tables are the source of truth. Mermaid diagrams are optional visualizations for humans.

## Use cases

Breadboarding serves three common functions:

### 1. Mapping an existing system

Use this when you do not yet understand how an existing system works in concrete detail.

Input:
- codebase or systems to analyze
- a workflow description from the perspective of someone trying to make an effect happen

Output:
- Places table
- UI affordances table
- Non-UI affordances table
- Stores table
- optional Mermaid diagram

### 2. Designing from shaped parts

Use this when shaping has already produced mechanisms and you need to detail them into concrete affordances and wiring.

Input:
- chosen shape and parts
- the requirements or outcomes those parts must satisfy
- optionally the existing system they need to connect to

Output:
- Places table
- UI affordances table
- Non-UI affordances table
- Stores table
- optional Mermaid diagram

### 3. Mixtures of existing and new

Often you need both: existing affordances that remain, plus new affordances from the chosen shape. Breadboard them together so the full story is visible.

## Reading a whiteboard breadboard

Hand-drawn or whiteboard breadboards use a visual stacking format rather than tables. The same concepts still apply: places, affordances, wiring, and hidden system consequences.

Common visual conventions:
- place block at the top of a stack
- affordances stacked under the place they belong to
- code affordances often floating between place stacks
- solid arrows for control flow
- dashed arrows for returns or data flow
- indented or colored blocks for conditional branches
- containing boxes for larger system boundaries
- notes or annotations for open questions and rationale

How to read one:
1. identify the places first
2. read each place stack top to bottom
3. trace solid arrows for what triggers what
4. trace dashed arrows for where output or data flows
5. note conditionals and boundaries
6. translate the stacks into standard tables

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

### The blocking test

The simplest test for whether something is a different place: can you interact with what is behind it?

- **No** → different place
- **Yes** → same place with local state changes

### Local state vs place navigation

When a control changes state, ask whether everything changed or only a subset while the surroundings stayed the same.

- local state = same place, changed subset
- place navigation = the user is now somewhere else in a meaningful sense

### Modes as places

When a mode changes the whole perceptual context — for example read mode vs edit mode — model it as a different place.

Examples:
- `PLACE: CMS Page (Read Mode)`
- `PLACE: CMS Page (Edit Mode)`

### Make meaningful user-visible states first-class

If a state changes what the user can do next or what they can see, consider representing it as its own place.

Examples:
- empty state
- duplicate warning shown
- bought items hidden
- restored-on-launch state

Do not hide important user-visible states inside only non-UI affordances.

### Place IDs

Places are first-class elements in the model and should get IDs such as `P1`, `P2`, `P3`.

Use place IDs so navigation wires can point to places directly.

### Subplaces

Use subplaces when a place contains a distinct widget or section that needs its own local scope.

Examples:
- `P2.1`
- `P2.2`

Subplaces help show what is in scope inside a larger place without pretending it is a separate top-level destination.

### Place references

When a nested place has many internal affordances and would clutter the parent, use a place reference.

Pattern:
- `_letter-browser`
- `_settings-panel`

The reference appears in the parent place as a UI affordance and wires to the full place definition elsewhere.

### Affordances
Affordances are the things that can be acted upon or that produce effects.

Use these prefixes:
- `U` for user-facing affordances
- `N` for non-UI/code affordances
- `S` for stores or state
- `P` for places

Keep non-UI affordances close to product-relevant consequences.

### Containment vs wiring

Containment and wiring are different relationships.

- **Containment** = which place an affordance belongs to
- **Wiring** = what an affordance triggers or feeds

The Place column answers: where does this affordance live?
The Wires Out and Returns To columns answer: what does it trigger and where does its output go?

### Wiring
Wiring explains behavior.

Track two kinds:
- **Wires Out** for control flow: what triggers what
- **Returns To** for data flow or visible consequence: where outputs or state are consumed

A good breadboard should help answer:
- what can the user do here?
- what happens next?
- what changes in the product?

### Navigation wiring

When an affordance causes navigation, wire to the **place itself**, not to an affordance inside that place.

Good:
- `N1 → P2`

Less useful:
- `N1 → U7`

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

## Procedures

### Mapping an existing system

1. Identify the workflow or effect to explain.
2. List the places involved.
3. Trace the code or system to find all components touched by that flow.
4. Identify the concrete affordances in each place.
5. Name real things that exist in the code or design — not abstractions.
6. Add the hidden system consequences that matter to product behavior.
7. Add the stores that shape the behavior.
8. Fill in control flow with **Wires Out**.
9. Fill in data flow and visible consequence with **Returns To**.
10. Verify that every visible effect can be explained by the wiring.

### Designing from shaped parts

1. List the mechanisms from the chosen shape.
2. Translate each mechanism into UI and non-UI affordances.
3. Identify whether each affordance lives in an existing place or a new place.
4. Add the stores and hidden consequences those affordances need.
5. Wire the affordances together.
6. If there is an existing system, add the existing affordances the new ones must connect to.
7. Check that every displayed effect has a source and every important mechanism is represented.

## Quality checks

- Every displayed UI element that depends on data should have an incoming source.
- Every code affordance should either trigger something, return something, or both.
- Avoid vague affordance names like `database`, `logic`, or `handler stuff`.
- Prefer real names that point to a thing someone can find in code or design.
- Prefer product-facing hidden behavior over abstract service decomposition.
- Make important user-visible consequences first-class.
- Make product-relevant branches explicit when they change what the user sees next.

## Rules for real affordances

### Not every mechanism is an affordance

Some things are just implementation mechanisms and should not get their own node unless they are truly meaningful at breadboard level.

Examples often better omitted:
- wrapper elements
- internal transforms that do not matter to the product behavior
- low-level navigation plumbing when wiring directly to the destination place is clearer

### Every displayed UI needs a source

If a UI affordance displays data, the breadboard should show where that data comes from.

### Every N must connect

If a non-UI affordance has no Wires Out and no Returns To, something is probably missing or the affordance may not deserve its own row.

### Side effects need stores

If a hidden consequence affects external state, represent that state as a store when it matters.

Examples:
- browser URL
- local storage
- clipboard
- browser history

### Place stores where they enable behavior

A store belongs where its data enables behavior, not merely where it gets written.

### Backend is a place when it matters

Resolvers, APIs, and database behavior are not just floating infrastructure. When they are part of the story of how the product works, model them as a place with their own affordances and stores.

## Catalog of elements and relationships

### Elements

| Element | ID pattern | Meaning |
|---------|------------|---------|
| Place | P1, P2 | bounded context of interaction |
| Subplace | P2.1, P2.2 | scoped area inside a larger place |
| Place reference | _name | detached nested place reference |
| UI affordance | U1, U2 | something the user can see or interact with |
| Non-UI affordance | N1, N2 | hidden mechanism with meaningful identity |
| Store | S1, S2 | state that is written and read |
| Chunk | freeform | collapsed subsystem in a larger diagram |

### Relationships

| Relationship | Meaning | Where captured |
|--------------|---------|----------------|
| Containment | affordance belongs to a place | Place column |
| Wires Out | control flow | Wires Out column |
| Returns To | data flow / visible consequence | Returns To column |

## Chunking

Chunking collapses a subsystem into a single node in the main diagram when it has one clear entry, one clear output, and too many internals to keep the main view readable.

Use chunking when:
- the subsystem has many internals
- the main diagram is becoming unreadable
- you still need to preserve the boundary signal between the main system and the subsystem

A chunk should have its own separate detailed view when needed.

## Recommended output structure

```md
---
planning: true
shaping: true
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

### Diagram rules

If you add a diagram:
- group nodes by place first
- make affordances under each place visible
- keep IDs consistent with the tables
- show product consequences, not only internal calls
- treat the diagram as a rendering of the tables, not the other way around

### Visualization conventions

- solid arrows = control flow / Wires Out
- dashed arrows = returns / data flow / visible consequence
- wire navigation to places directly
- use place IDs as subgraph IDs when possible
- use place references for detached nested places
- use chunks when a subsystem would otherwise overwhelm the main diagram

### Optional workflow annotations

For teaching or walkthrough diagrams, you may add numbered workflow step annotations to guide the reader through the main path.

## Transition to slicing

Slice only after the breadboard is concrete enough that you can group affordances into demoable vertical increments.

## Slicing

A vertical slice is a group of UI and non-UI affordances that does something demo-able.

### Core rule

Every slice must end in visible, demo-able UI. A slice without an observable output is a horizontal layer, not a vertical slice.

### Good slicing questions

- What is the smallest subset that demonstrates the core mechanism working?
- What can I show a stakeholder to prove this mechanism exists?
- Does this slice have both an entry point and an observable result?

### Slice size

- too small = no meaningful demo
- too big = multiple unrelated journeys tangled together
- right size = one coherent mechanism with a clear demo

### Slicing procedure

1. Identify the smallest demo-able increment.
2. Layer additional mechanisms as later slices.
3. Assign affordances to the slice where they are first needed.
4. Allow wires to future slices if they reflect the eventual system and are not implemented yet.
5. Write a demo statement and `Produces:` line for each slice.

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
