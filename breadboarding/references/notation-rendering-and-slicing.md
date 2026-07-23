# Breadboarding notation, rendering, and slicing reference

Load this reference only when the work needs the complete element catalog, chunking rules, output template, Mermaid conventions, or selected-design slicing procedure.

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

## Mode and authority
- Mode: current-state | selected-design
- Authority: descriptive current-state evidence | accepted selected intent
- Selected shape and appetite: required for selected-design only
- Evidence: required for non-obvious current-state claims

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

This section applies only to an accepted `selected-design` breadboard. A `current-state` breadboard stops at descriptive mapping and must return proposed changes through shaping before any slice is selected.

Slice only after the breadboard is concrete enough that you can group affordances into demoable vertical increments.

Before proposing slices, optionally run an affinity-grouping pass over the selected shape:

1. Inventory the breadboard elements implied by the selected shape.
2. Affinitize them into groups that can be completed together.
3. Name each group as a stable scope handle.
4. Flag the biggest unknown per group.

Use those groups as raw material for slice boundaries, not as an implementation sequence or substitute for vertical slices.

## Slicing

A vertical slice is a group of UI and non-UI affordances that does something demo-able.

### Core rule

Every slice must end in an observable, judgeable result across the relevant product surface. That evidence may be UI, API output, CLI behavior, a processed event, a background-job result, or another end-to-end consequence appropriate to the product. A slice without observable evidence is a horizontal layer, not a vertical slice.

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
