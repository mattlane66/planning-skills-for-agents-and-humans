---
name: breadboarding
description: Map current-state behavior or a selected design into places, affordances, stores, consequences, and wiring when concrete behavior or candidate slices need clarification.
license: MIT
---

# Breadboarding

Use this skill when the team needs to understand how an existing system behaves or make a human-selected design concrete enough to review and slice.

## Goal

Produce a legible system map that shows:
- the places a person, operator, or system caller interacts through
- the affordances available in those places
- the important hidden system consequences
- the stores or state that matter
- the wiring between all of them

Every breadboard must declare whether it is a descriptive `current-state` map or a normative `selected-design` map. The tables are the source of truth within that declared authority. Mermaid diagrams are optional visualizations for humans.

## Operating modes

Choose one mode before mapping. Do not let evidence about current behavior silently become accepted future behavior.

### Current-state mapping (descriptive)

Use this when you do not yet understand how an existing system works in concrete detail.

Input:
- codebase or systems to analyze
- a workflow description from the perspective of someone trying to make an effect happen
- direct evidence such as code paths, tests, logs, screenshots, or observed behavior

Output:
- `mode: current-state`
- Places table
- UI affordances table
- Non-UI affordances table
- Stores table
- evidence references and unresolved observations
- optional Mermaid diagram

This mode does not require a selected direction. It records what exists; it cannot select a future direction, define accepted product intent, or produce a buildable slice by itself. If the current-state map suggests a change, send that proposal back through shaping and the human selection gate.

### Selected-design mapping (normative)

Use this when shaping has already produced mechanisms and you need to detail them into concrete affordances and wiring.

Input:
- human-selected shape and parts
- accepted appetite and cut line
- the requirements or outcomes those parts must satisfy
- optionally the existing system they need to connect to

Output:
- `mode: selected-design`
- Places table
- UI affordances table
- Non-UI affordances table
- Stores table
- product-relevant branches and candidate vertical slices
- optional Mermaid diagram

Only an accepted selected-design breadboard can feed slice selection and downstream build artifacts.

### Combining current and proposed behavior

Often you need both existing affordances that remain and new affordances from the selected shape. Keep their authority legible: use separate artifacts or clearly label current and proposed rows, cite the selected shape for every proposed mechanism, and do not treat an observed current behavior as selected future intent unless the human explicitly accepts it.

## Reading a whiteboard breadboard

Hand-drawn or whiteboard breadboards use a visual stacking format rather than tables. The same concepts still apply: places, affordances, wiring, and hidden system consequences.

If the visual is being compared with an existing selected shape or breadboard and may change behavior or scope, use the `sketch-reconciliation` skill first. Translate only accepted deltas into the canonical breadboard tables.

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

Breadboarding is a lightweight behavioral mapping notation for interactive products, operator workflows, APIs, CLIs, and background processes.

It separates observable entry points and effects from the hidden system behavior that makes them happen.

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

### Current-state mapping

1. Declare `mode: current-state` and identify the workflow or effect to explain.
2. List the places involved.
3. Trace the code or system to find all components touched by that flow.
4. Identify the concrete affordances in each place.
5. Name real things that exist in the code or design — not abstractions.
6. Add the hidden system consequences that matter to product behavior.
7. Add the stores that shape the behavior.
8. Fill in control flow with **Wires Out**.
9. Fill in data flow and visible consequence with **Returns To**.
10. Cite the evidence for non-obvious behavior and mark unresolved observations.
11. Verify that every visible effect can be explained by the wiring.
12. Stop before treating this map as selected future behavior or slicing it for implementation.

### Selected-design mapping

1. Confirm the human-selected shape, accepted appetite, and cut line; declare `mode: selected-design`.
2. List the mechanisms from the selected shape.
3. Translate each mechanism into UI and non-UI affordances.
4. Identify whether each affordance lives in an existing place or a new place.
5. Add the stores and hidden consequences those affordances need.
6. Wire the affordances together.
7. If there is an existing system, add the existing affordances the new ones must connect to and label current versus proposed behavior.
8. Check that every displayed effect has a source and every important selected mechanism is represented.

## Quality checks

- The breadboard declares `current-state` or `selected-design` mode.
- Current-state evidence is not presented as selected future intent.
- A selected-design breadboard cites the selected shape, appetite, and cut line.
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

## Detailed notation, rendering, and slicing

Read [the notation, rendering, and slicing reference](references/notation-rendering-and-slicing.md) when you need:

- the complete element and relationship catalog
- chunking rules
- the recommended output template
- Mermaid rendering conventions
- selected-design slice creation, sequencing, exit conditions, and appetite cuts

Do not load that reference for a simple current-state map that stops before slicing.
