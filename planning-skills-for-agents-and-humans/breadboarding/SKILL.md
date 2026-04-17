---
name: breadboarding
description: Use when you need to map a system into places, affordances, stores, and wiring so humans and agents can see how behavior is produced.
---

# Breadboarding

Breadboarding turns a workflow or shaped solution into a visible system map.

The tables are the source of truth. Diagrams are only a rendering of those tables.

---

## What to Capture

### Places
A place is a bounded interaction context.

Ask: can the user still interact with what is behind this state?
- If no, it is probably a different place.
- If yes, it is probably local state within the same place.

Examples of places:
- a page
- a full-screen mode
- a blocking modal
- a backend boundary when needed for explanation

### Affordances
Affordances are the things that can act or be acted upon.

Use these categories:
- `U` for UI affordances
- `N` for non-UI or code affordances
- `S` for stores or persistent state

Examples:
- `U1: Search input`
- `N3: performSearch()`
- `S1: results`

### Wiring
Capture two distinct flows:
- `Wires Out` for control flow: what triggers what
- `Returns To` for data flow: where outputs are consumed

Keep them separate.

---

## Required Tables

### Places

| # | Place | Description |
|---|-------|-------------|
| P1 | Search Page | Main search view |

### UI Affordances

| # | Place | Component | Affordance | Control | Wires Out | Returns To |
|---|-------|-----------|------------|---------|-----------|------------|
| U1 | P1 | search-panel | search input | type | → N1 | — |

### Non-UI Affordances

| # | Place | Component | Affordance | Control | Wires Out | Returns To |
|---|-------|-----------|------------|---------|-----------|------------|
| N1 | P1 | search-panel | `query$.next()` | call | → N2 | — |

### Stores

| # | Place | Store | Description |
|---|-------|-------|-------------|
| S1 | P1 | results | Search results array |

---

## Procedure

1. Name the workflow you are trying to explain.
2. Identify the places involved.
3. List the visible affordances in each place.
4. List the handlers, queries, subscriptions, services, or other non-UI affordances.
5. Add stores for state that matters to the behavior.
6. Fill in control flow with `Wires Out`.
7. Fill in data flow with `Returns To`.
8. Check that every visible output has a source and every code affordance participates in a real path.

---

## Good Breadboard Hygiene

### Name real things
When mapping an existing system, name functions, stores, or components that actually exist.

### Do not confuse navigation with implementation detail
When something causes navigation, wire to the destination place.

### Every visible display needs a source
If a UI affordance renders data, the breadboard should show where that data comes from.

### Every non-UI affordance must connect
If it has no outgoing or returning relationship, it may be missing context or may not deserve its own row.

---

## Slicing

Once a breadboard is stable, group affordances into vertical slices.

A vertical slice must:
- have an entry point
- have an observable result
- demonstrate a meaningful mechanism working

Avoid slices that are only schema, only services, or only plumbing with nothing demoable.

---

## Minimal Template

```markdown
---
planning: true
---

# [Project] — Breadboard

## Places
| # | Place | Description |
|---|-------|-------------|
| P1 | ... | ... |

## UI Affordances
| # | Place | Component | Affordance | Control | Wires Out | Returns To |
|---|-------|-----------|------------|---------|-----------|------------|
| U1 | P1 | ... | ... | click | → N1 | — |

## Non-UI Affordances
| # | Place | Component | Affordance | Control | Wires Out | Returns To |
|---|-------|-----------|------------|---------|-----------|------------|
| N1 | P1 | ... | ... | call | → N2 | — |

## Stores
| # | Place | Store | Description |
|---|-------|-------|-------------|
| S1 | P1 | ... | ... |
```
