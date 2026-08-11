---
name: breadboarding
description: Map current behavior, candidate shapes, or a selected design into places, affordances, stores, consequences, and wiring when concrete behavior needs clarification.
license: MIT
---

# Breadboarding

Use this skill when the team needs to understand how an existing system behaves, test the behavioral structure of a candidate shape during shaping, or make a human-selected design concrete enough to review and slice.

## Goal

Produce a legible system map that shows:

- the places a person, operator, or system caller interacts through
- the affordances available in those places
- the important hidden system consequences
- the stores or state that matter
- the wiring between all of them

Every breadboard must declare one mode:

- `current-state` — descriptive evidence about what exists
- `candidate-shape` — exploratory evidence about one unselected shape
- `selected-design` — normative accepted future intent

The tables are the source of truth within the authority of the declared mode. Mermaid diagrams are optional visualizations for humans.

## Operating modes

Choose one mode before mapping. Do not let current evidence or an exploratory candidate silently become accepted future behavior.

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

This mode does not require a selected direction. It records what exists; it cannot select a future direction, define accepted product intent, or produce a buildable slice by itself. If the map suggests a change, send that proposal through shaping and the human selection gate.

### Candidate-shape mapping (exploratory)

Use this during shaping when a named candidate cannot be judged honestly from a mechanism list or sketch alone.

Candidate-shape mode supports both collaborative and gated shaping.

Minimum input:

- one named candidate shape and its shape-part IDs
- the specific behavioral or structural uncertainty to resolve
- whatever requirements currently exist, clearly marked `Working` or `Accepted`
- appetite and cut line when they exist, clearly marked `Unset`, `Working`, or `Accepted`
- relevant current-state evidence when the candidate must connect to an existing system

In collaborative shaping, accepted requirements or appetite are **not prerequisites for exploratory candidate breadboarding**. If either is provisional or missing, say so explicitly and do not claim final requirement fit, appetite fit, or decision readiness from that evidence.

In a gated/orchestrated profile, the active orchestration policy may require accepted requirements and appetite before candidate breadboarding. Follow the stricter profile when it has been explicitly selected.

Output:

- `mode: candidate-shape`
- input authority status for requirements and appetite
- only the places, affordances, stores, consequences, branches, and wiring needed to resolve the named uncertainty
- supported, missing, or contradictory mechanisms
- rabbit holes, appetite risks when appetite is known, and focused spike candidates
- implications for requirement fit, reverse fit, and appetite fit where those judgments are supportable
- proposed R/S changes revealed by the mapping
- unresolved questions

Candidate-shape breadboarding is a shaping technique. It is subordinate to the shaping artifact and its named candidate. It may be partial and candidates do not need equal detail.

It cannot:

- select its own candidate
- become accepted future intent
- feed slice selection or implementation
- produce committed contracts, task groups, or build handoffs
- silently change accepted requirements, appetite, or the candidate shape

When candidate breadboarding reveals a useful change to working R or S, return that change to shaping. When it would change accepted R, appetite, or a selected direction, propose the delta and stop for the applicable human gate.

Read [candidate-shape mode](references/candidate-shape-mode.md) for its complete authority, output, and promotion contract.

### Selected-design mapping (normative)

Use this when shaping has produced a human-selected direction and you need to detail it into concrete affordances and wiring.

Input:

- human-selected shape and parts
- accepted appetite and cut line
- the accepted requirements or outcomes those parts must satisfy
- optionally an existing or candidate-shape breadboard to reconcile
- optionally the existing system the selected design must connect to

Output:

- `mode: selected-design`
- Places table
- UI affordances table
- Non-UI affordances table
- Stores table
- product-relevant branches and candidate vertical slices
- optional Mermaid diagram

A candidate breadboard does not automatically become selected-design. Remove unselected mechanisms, reconcile surviving rows against the accepted shape and cuts, preserve unresolved gaps explicitly, and obtain acceptance.

Only an accepted selected-design breadboard can feed slice selection and downstream build artifacts.

### Combining current and proposed behavior

Often you need existing affordances that remain and new affordances from a candidate or selected shape. Keep authority legible: use separate artifacts or clearly label current and proposed rows, cite the source shape for every proposed mechanism, and do not treat observed current behavior as selected future intent unless a human explicitly accepts it.

## Relationship to shaping

Breadboarding is a distinct capability that shaping may invoke at any useful point in the exploratory loop.

- Shaping owns requirements, appetite, candidate comparison, and human selection.
- Candidate-shape breadboarding supplies exploratory evidence to shaping and may reveal changes to working R or S.
- Selected-design breadboarding makes the accepted direction concrete after selection.
- Breadboarding never selects a shape or silently changes accepted planning truth.

A detailed selected-design breadboard may expose a conflict with the selected shape, requirements, or appetite. When that happens, stop and return:

```md
## Breadboarding exposed a shaping issue

- Selected shape says:
- Concrete behavioral implication:
- Conflict or appetite risk:
- Evidence:
- Options:
  1. Revise the selected shape.
  2. Cut the conflicting behavior.
  3. Run a focused spike.
  4. Reopen shape selection.
  5. Stop the bet.
```

Apply only an explicit human decision before continuing.

## Reading a whiteboard breadboard

Hand-drawn or whiteboard breadboards use a visual stacking format rather than tables. The same concepts still apply: places, affordances, wiring, and hidden system consequences.

If the visual is being compared with an existing selected shape or breadboard and may change behavior or scope, use the `sketch-reconciliation` skill first. Translate only accepted deltas into canonical tables.

Common visual conventions:

- place block at the top of a stack
- affordances stacked under the place they belong to
- code affordances often floating between place stacks
- solid arrows for control flow
- dashed arrows for returns or data flow
- indented or colored blocks for conditional branches
- containing boxes for larger system boundaries
- notes for open questions and rationale

How to read one:

1. identify the places first
2. read each place stack top to bottom
3. trace solid arrows for what triggers what
4. trace dashed arrows for where output or data flows
5. note conditionals and boundaries
6. translate the stacks into standard tables

## What breadboarding is

Breadboarding is a lightweight behavioral mapping notation for interactive products, operator workflows, APIs, CLIs, and background processes.

It separates observable entry points and effects from the hidden system behavior that makes them happen. Because it uses words instead of detailed pictures, you can quickly play out an idea and judge whether the sequence of actions actually serves the use case.

## Center of gravity

A breadboard is mainly about:

- place
- affordance
- visible consequence
- the hidden system behavior that matters to product behavior

It is **not** mainly a service graph.

If the diagram starts to read like:

- service → service → store → render

then it is probably too implementation-heavy.

Prefer product-relevant wording such as:

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

Can you interact with what is behind it?

- **No** → different place
- **Yes** → same place with local state changes

### Local state, modes, and visible states

When only a subset changes while the surroundings remain available, keep it in the same place. When a mode changes the whole perceptual context, model it as a different place.

Make user-visible states first-class when they change what the user can do next or see, such as empty states, warnings, hidden-item states, or restored-on-launch states.

### Place IDs and subplaces

Use IDs such as `P1`, `P2`, and `P3`. Use subplaces such as `P2.1` when a distinct widget or section needs local scope without becoming a top-level destination.

When a nested place would clutter its parent, use a detached place reference such as `_settings-panel` and wire to the full definition elsewhere.

### Affordances

Affordances are things that can be acted upon or produce effects.

Use these prefixes:

- `U` for user-facing affordances
- `N` for non-UI or code affordances
- `S` for stores or state
- `P` for places

Keep non-UI affordances close to product-relevant consequences.

### Containment and wiring

Containment and wiring are different relationships:

- **Containment** = which place an affordance belongs to
- **Wires Out** = control flow, or what it triggers
- **Returns To** = data flow or visible consequence

When an affordance causes navigation, wire to the destination place itself rather than an arbitrary affordance inside it.

### Product-relevant branches

When a hidden rule can lead to different user-visible outcomes, represent the split explicitly.

Examples:

- duplicate → show duplicate message
- not duplicate → add item and show updated list
- hide-bought on → bought item disappears
- hide-bought off → bought item remains visible with updated state

## Required tables

### Places

| ID | Place | Description |
|---|---|---|
| P1 | Search page | Main search experience |

### UI affordances

| ID | Place | Component | Affordance | Control | Wires Out | Returns To |
|---|---|---|---|---|---|---|
| U1 | P1 | search | input field | type | → N1 | — |

### Non-UI affordances

| ID | Place | Component | Affordance | Control | Wires Out | Returns To |
|---|---|---|---|---|---|---|
| N1 | P1 | search | query handler | call | → N2 | — |

### Stores

| ID | Place | Store | Description |
|---|---|---|---|
| S1 | P1 | results | Search results array |

## Procedures

### Current-state mapping

1. Declare `mode: current-state` and identify the workflow or effect to explain.
2. List the places involved.
3. Trace the code or system to find all components touched by that flow.
4. Identify concrete affordances in each place.
5. Name real things that exist in code or design, not abstractions.
6. Add hidden system consequences that matter to product behavior.
7. Add stores that shape behavior.
8. Fill in control flow with **Wires Out**.
9. Fill in data flow and visible consequence with **Returns To**.
10. Cite evidence for non-obvious behavior and mark unresolved observations.
11. Verify that every visible effect can be explained by the wiring.
12. Stop before treating the map as selected future behavior or slicing it.

### Candidate-shape mapping

1. Confirm the named candidate and the single decision-relevant question to resolve.
2. Record whether requirements are Working or Accepted and whether appetite is Unset, Working, or Accepted.
3. If the active profile is gated/orchestrated, enforce any additional prerequisites before continuing.
4. Declare `mode: candidate-shape`.
5. Map only enough places, affordances, stores, branches, and wiring to answer that question.
6. Label every proposed element with its candidate shape-part source.
7. Add current-state elements only when needed and keep them visibly descriptive.
8. Identify unsupported mechanisms, rabbit holes, appetite risks when appetite is known, and spike candidates.
9. Return proposed R/S changes plus fit and reverse-fit implications to shaping; state when an implication is provisional because R or appetite is not accepted.
10. Stop when the question is clear enough for the next shaping move; do not slice or prepare implementation.

### Selected-design mapping

1. Confirm the human-selected shape, accepted requirements, accepted appetite, and cut line; declare `mode: selected-design`.
2. If a candidate breadboard exists, reconcile it rather than promoting it automatically.
3. List the selected mechanisms and explicit cuts.
4. Translate each selected mechanism into UI and non-UI affordances.
5. Identify whether each affordance belongs in an existing or new place.
6. Add the stores and hidden consequences those affordances need.
7. Wire the affordances together and make product-relevant branches explicit.
8. Add existing affordances the new ones must connect to, labeling current versus selected behavior.
9. Check that every displayed effect has a source and every selected mechanism is represented.
10. Surface any shaping conflict and stop for an explicit decision.
11. Obtain acceptance before slicing.

## Quality checks

- The breadboard declares `current-state`, `candidate-shape`, or `selected-design` mode.
- Current-state evidence is not presented as selected future intent.
- A candidate-shape breadboard names the candidate and question it resolves.
- A candidate-shape breadboard states the authority status of its requirements and appetite inputs.
- Provisional candidate evidence is not presented as final fit or appetite evidence.
- Candidate evidence does not select a shape, feed slicing, or become build scope.
- A selected-design breadboard cites the selected shape, accepted requirements, appetite, and cut line.
- Candidate rows are explicitly reconciled before becoming selected-design rows.
- Every displayed UI element that depends on data has an incoming source.
- Every code affordance triggers something, returns something, or both.
- Important user-visible consequences and branches are first-class.
- Product-facing hidden behavior is preferred over abstract service decomposition.

## Rules for real affordances

### Not every mechanism is an affordance

Omit wrappers, invisible transforms, and low-level plumbing unless they materially affect product behavior.

### Every displayed UI needs a source

If a UI affordance displays data, show where that data comes from.

### Every `N` must connect

If a non-UI affordance has no **Wires Out** and no **Returns To**, something is missing or the row may not deserve to exist.

### Side effects need stores

Represent external state such as browser URL, local storage, clipboard, or browser history when it matters to behavior.

### Place stores where they enable behavior

A store belongs where its data enables behavior, not merely where it gets written.

### Backend is a place when it matters

Resolvers, APIs, and database behavior are not floating infrastructure. When they are part of the product story, model them as a place with their own affordances and stores.

## Detailed notation, rendering, and slicing

Read [the notation, rendering, and slicing reference](references/notation-rendering-and-slicing.md) when you need:

- the complete element and relationship catalog
- chunking rules
- the recommended output template
- Mermaid rendering conventions
- selected-design slice creation, sequencing, exit conditions, and appetite cuts

Do not load that reference for a simple current-state or candidate-shape map that stops before slicing.