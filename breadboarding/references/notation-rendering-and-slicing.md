# Breadboarding notation, rendering, and slicing reference

Load this reference only when the work needs the complete element catalog, chunking rules, output template, visual composition grammar, targeted sketches, Mermaid fallback conventions, or selected-design slicing procedure.

## Contents

- [Catalog of elements and relationships](#catalog-of-elements-and-relationships)
- [Chunking](#chunking)
- [Recommended output structure](#recommended-output-structure)
- [Reading a whiteboard breadboard](#reading-a-whiteboard-breadboard)
- [Producing a visual breadboard](#producing-a-visual-breadboard)
- [Targeted sketches and mixed fidelity](#targeted-sketches-and-mixed-fidelity)
- [Mermaid diagrams](#mermaid-diagrams)
- [Transition to slicing](#transition-to-slicing)
- [Slicing](#slicing)
- [Sequencing slices](#sequencing-slices-two-passes)
- [Exit conditions](#exit-conditions-are-defined-right-to-left)
- [Cutting](#cutting)

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
- Mode: current-state | candidate-shape | selected-design
- Authority: descriptive current-state evidence | exploratory candidate evidence | accepted selected intent
- Requirements and Appetite authority: required for candidate-shape and selected-design
- Candidate shape and decision-relevant uncertainty: required for candidate-shape
- Selected shape and accepted Appetite/cut line: required for selected-design
- Evidence: required for non-obvious current-state claims

## Places
[table]

## UI Affordances
[table]

## Non-UI Affordances
[table]

## Stores
[table]

## Behavior traces
[table]

## Visual breadboard
[derived spatial projection for nontrivial interactive work]

## Targeted sketches
[SK# mappings only where spatial interaction needs more fidelity]

## Notes
- [important constraints, open questions, or assumptions]
```

## Reading a whiteboard breadboard

Hand-drawn breadboards use visual stacks rather than tables, but the same places, affordances, stores, causal traces, and authority rules apply.

Common conventions:

- place block at the top of a stack
- affordances beneath the place they belong to
- non-UI affordances between place stacks
- solid arrows for control flow
- dashed arrows for data flow, returns, or visible consequences
- indented or colored groups for conditional branches
- containing boxes for larger system boundaries
- notes for open questions and rationale

Read one by:

1. identifying the places and boundaries
2. reading each stack top to bottom
3. tracing control arrows from an entry
4. tracing data or return arrows to the observable consequence
5. recording decisions, branches, stores, and unresolved links
6. translating the result into canonical tables and behavior traces

If the visual may change accepted behavior or scope, use `sketch-reconciliation` first and translate only accepted deltas.

## Producing a visual breadboard

A visual breadboard is a **spatial explanation of behavior**, not a generic graph rendering.

The canonical tables answer "what exists and how is it wired?" The visual should answer "how does a person experience this sequence, and where do consequential system decisions intervene?"

For nontrivial interactive work, compose the visual after the canonical model is structurally sound.

### Composition grammar

Default to these rules unless the product's interaction suggests a clearer arrangement:

1. **Primary journey left to right.** Put the representative entry on the left and its observable consequence to the right.
2. **Places as loose stacks.** Put a place/context label at the top, with its visible affordances immediately below. A place need not be boxed if whitespace communicates containment more clearly.
3. **Visible layer above, system rail below.** Keep user-facing controls, content, and states visually dominant. Put validation, stores, APIs, background work, and external systems beneath or between the visible places they explain.
4. **Local branches.** Let a branch leave from the decision that causes it. Keep its consequence nearby and rejoin the primary path only when the behavior actually rejoins.
5. **Consequences near causes.** Avoid sending a wire across the entire board merely to reach a visible outcome that can be shown locally.
6. **Whitespace before boxes.** Group with spacing and alignment first. Use containing boxes only for real boundaries.
7. **Few crossings.** Reroute, reorder, or duplicate a clearly labeled reference rather than accepting a thicket of crossing lines.
8. **Annotations at the point of uncertainty.** Put a short note beside the decision, risk, cut, or unresolved behavior it describes.
9. **Stable IDs remain visible.** Every place, affordance, store, system action, and targeted sketch should remain traceable to the canonical model.
10. **Do not optimize for compactness.** Optimize for play-through clarity.

The visual may be SVG, HTML/canvas, Excalidraw, TLDraw, FigJam, Miro, or another surface that supports deliberate placement.

### Finger-trace test

Before calling the visual done, ask:

> Can a reviewer trace the representative scenario with a finger, see each meaningful branch and visible state change, and understand why the next step happens without reading every table row?

If not, change the composition. Do not solve a visual-composition problem by adding more boxes.

### Visual hierarchy

A useful visual hierarchy generally reads in this order:

1. place or screen context
2. user-facing affordance or visible state
3. causal movement / branch
4. hidden system consequence
5. store or external boundary
6. annotation

If stores and internal actions become the most visually prominent objects, the breadboard has drifted toward a service graph.

## Targeted sketches and mixed fidelity

Breadboards should not have uniform fidelity.

Use this principle:

> **Use the lowest fidelity that resolves the question. Raise fidelity locally, not globally.**

Add a targeted sketch when a textual affordance label does not make the important interaction legible because the behavior depends on:

- spatial arrangement or hierarchy
- what remains visible while a local state changes
- selection, editing, comparison, or before/after state
- direct manipulation such as drag/drop
- interaction among several controls in one place
- a dense control whose action would otherwise be ambiguous

A targeted sketch should:

- cover the smallest region needed to explain the behavior
- remain rough enough that reviewers focus on mechanism rather than styling
- carry a stable `SK#` identifier
- name the canonical IDs it elaborates
- show only states or controls already represented in the canonical model

Example:

`SK1 → P3 / U7 / U8 / S2`

Do not sketch an entire product merely because one interaction needs clarification. Do not introduce hidden persistence, validation, navigation, or new actions in a sketch unless they are first added to the canonical tables through the appropriate planning authority.

### Mixed-fidelity composition

One board may legitimately combine:

- a low-detail place stack for routine navigation
- explicit hidden logic for a consequential branch
- a tiny wireframe for a difficult editor or merge interaction
- a store or API marker where persistence materially changes later behavior
- short handwritten-style rationale or risk notes

That mixture is a feature. Fidelity should follow uncertainty, not visual consistency.

## Mermaid diagrams

Mermaid remains a useful compact or machine-portable fallback. It is not the preferred visual language when deliberate spatial composition or targeted sketches materially improve comprehension.

The tables remain the source of truth.

### Diagram rules

If you add a Mermaid diagram:
- group nodes by place first
- make affordances under each place visible
- keep IDs consistent with the tables
- show product consequences, not only internal calls
- treat the diagram as a rendering of the tables, not the other way around
- represent every diagram node and relationship in the tables
- treat diagram-only behavior, wires, or branches as defects

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

This section applies only to an accepted `selected-design` breadboard. A `current-state` or `candidate-shape` breadboard stops before slicing and must return proposed changes or evidence through shaping.

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
