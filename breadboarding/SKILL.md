---
name: breadboarding
description: Map a system into places, affordances, stores, and wiring.
planning: true
---

# Breadboarding

Use this skill when the team needs to understand how a system behaves, where changes land, and how UI and non-UI elements connect.

## Goal

Produce a legible system map that shows:
- the places a person or operator can be in
- the affordances available in those places
- the stores or state that matter
- the wiring between all of them

## Core concepts

### Places
A place is a bounded context of interaction. It is where someone is, in practical terms, because it determines what they can do next.

Examples:
- a page
- a blocking modal
- a full-screen edit mode
- a backend boundary when mapping a cross-system flow

### Affordances
Affordances are the things that can be acted upon or that produce effects.

Use these prefixes:
- `U` for user-facing affordances
- `N` for non-UI/code affordances
- `S` for stores or state
- `P` for places

### Wiring
Wiring explains behavior.

Track two kinds:
- **Wires Out** for control flow: what triggers what
- **Returns To** for data flow: where outputs or state are consumed

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
4. Add the stores that shape the behavior.
5. Fill in control flow with **Wires Out**.
6. Fill in data flow with **Returns To**.
7. Check that every visible effect can be explained by the wiring.

## Quality checks

- Every displayed UI element that depends on data should have an incoming source.
- Every code affordance should either trigger something, return something, or both.
- Avoid vague affordance names like `database`, `logic`, or `handler stuff`.
- Prefer real names that point to a thing someone can find in code or design.

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
- keep IDs consistent with the tables
- treat the diagram as a rendering of the tables, not the other way around

## Transition to slicing

Slice only after the breadboard is concrete enough that you can group affordances into demoable vertical increments.
