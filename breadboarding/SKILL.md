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

## Causal story

A breadboard must explain how every required in-scope behavior proceeds from an entry to an observable consequence:

`entry → control path → decision or branch → state/data effect → observable consequence`

Choose the representative behavior or scenarios before mapping. Trace each one through table IDs, and record a gap instead of inventing a missing link. A behavior is not explained if any link is absent.

Trace forward while mapping. Before acceptance, reverse-trace each observable consequence by scanning every table row that points to it; do not rely on the path you remember.

For a nontrivial existing flow, a cross-place or cross-system design, branching behavior, or final selected-design verification, read [behavior tracing and verification](references/behavior-tracing-and-verification.md).

## Operating modes

Choose one mode before mapping. Do not let current evidence or an exploratory candidate silently become accepted future behavior.

### Current-state mapping (descriptive)

Use this when you do not yet understand how an existing system works in concrete detail.

Start from a workflow or effect to explain and direct evidence such as code paths, tests, logs, screenshots, or observed behavior. Record `mode: current-state`, the core tables, behavior traces, evidence references, and unresolved observations.

This mode does not require a selected direction. It records what exists; it cannot select a future direction, define accepted product intent, or produce a buildable slice by itself. If the map suggests a change, send that proposal through shaping and the human selection gate.

### Candidate-shape mapping (exploratory)

Use this during shaping when a named candidate cannot be judged honestly from a mechanism list or sketch alone.

Candidate-shape mode supports both collaborative and gated shaping. Name one candidate, its shape-part IDs, and the specific behavioral or structural uncertainty to resolve. Record the authority of requirements and Appetite, plus relevant current-state evidence when the candidate must connect to an existing system.

In collaborative shaping, accepted requirements or appetite are **not prerequisites for exploratory candidate breadboarding**. If either is provisional or missing, say so explicitly and do not claim final requirement fit, appetite fit, or decision readiness from that evidence.

In a gated/orchestrated profile, the active orchestration policy may require accepted requirements and appetite before candidate breadboarding. Follow the stricter profile when it has been explicitly selected.

Record `mode: candidate-shape` and only the causal structure needed to resolve the named uncertainty. Include supported, missing, or contradictory mechanisms; relevant risks or spikes; supportable fit implications; proposed R/S changes; and unresolved questions.

Candidate-shape breadboarding is a shaping technique. It is subordinate to the shaping artifact and its named candidate. It may be partial, and candidates do not need equal detail. It cannot select itself, become accepted future intent, feed slicing or implementation, produce committed downstream artifacts, or silently change accepted planning material.

When candidate breadboarding reveals a useful change to working R or S, return that change to shaping. When it would change accepted R, appetite, or a selected direction, propose the delta and stop for the applicable human gate.

Read [candidate-shape mode](references/candidate-shape-mode.md) for its complete authority, output, and promotion contract.

### Selected-design mapping (normative)

Use this when shaping has produced a human-selected direction and you need to detail it into concrete affordances and wiring.

Require the human-selected shape and parts, accepted requirements, accepted Appetite and cut line, plus any current-state or candidate breadboard that must be reconciled. Record `mode: selected-design`, the core tables, behavior traces for required in-scope scenarios, product-relevant branches, and only then candidate vertical slices.

A candidate breadboard does not automatically become selected-design. Remove unselected mechanisms, reconcile surviving rows against the accepted shape and cuts, preserve unresolved gaps explicitly, and obtain acceptance.

Selected-design must preserve the lineage from each Accepted requirement to the selected shape part(s) and the smallest set of breadboard IDs that embody it. Record the observable consequence when one exists. Do not tag every low-level affordance, store, or wire with an R merely for completeness; map only the concrete behavior that actually carries the requirement.

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

Translate hand-drawn or whiteboard stacks into the same canonical tables. If a visual may change an accepted shape or breadboard, use `sketch-reconciliation` first and translate only accepted deltas. Read the notation reference for visual conventions and the compact reading procedure.

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
2. Choose representative scenarios from the perspective of someone trying to produce an effect.
3. Trace the actual code or system path for each scenario before naming affordances.
4. List the places, concrete affordances, product-relevant consequences, and stores the trace reaches.
5. Use existing code or domain names where they clarify evidence; do not replace them with invented generic services.
6. Fill control flow with **Wires Out** and data or visible consequence with **Returns To**.
7. Record the causal trace by ID, including meaningful branches and state effects.
8. Cite evidence for non-obvious claims and mark unresolved links instead of guessing.
9. Run forward and reverse graph-integrity checks and confirm that every visible effect reaches all of its actual sources.
10. Stop before treating the map as selected future behavior or slicing it.

### Candidate-shape mapping

1. Confirm the named candidate and the single decision-relevant question to resolve.
2. Record whether requirements are Working or Accepted and whether appetite is Unset, Working, or Accepted.
3. If the active profile is gated/orchestrated, enforce any additional prerequisites before continuing.
4. Declare `mode: candidate-shape`.
5. Map only enough places, affordances, stores, branches, and causal traces to answer that question.
6. Label every proposed element with its candidate shape-part source.
7. Add current-state elements only when needed and keep them visibly descriptive.
8. Identify unsupported mechanisms, rabbit holes, appetite risks when appetite is known, and spike candidates.
9. Verify the mapped paths without expanding into unrelated design detail.
10. Return proposed R/S changes plus fit and reverse-fit implications to shaping; state when an implication is provisional because R or appetite is not accepted.
11. Stop when the question is clear enough for the next shaping move; do not slice or prepare implementation.

### Selected-design mapping

1. Confirm the human-selected shape, accepted requirements, accepted appetite, and cut line; declare `mode: selected-design`.
2. If a candidate breadboard exists, reconcile it rather than promoting it automatically.
3. List the selected mechanisms and explicit cuts.
4. Create a requirement realization map from each Accepted R to its selected shape part(s), breadboard IDs, and observable consequence when one exists.
5. Translate each selected mechanism into UI and non-UI affordances.
6. Identify whether each affordance belongs in an existing or new place.
7. Add the stores and hidden consequences those affordances need.
8. Wire the affordances together and trace every required behavior from entry to observable consequence.
9. Add existing affordances the new ones must connect to, labeling current versus selected behavior.
10. Make success, meaningful alternatives, failure, recovery, and persistence behavior explicit when relevant.
11. Run forward and reverse graph-integrity checks and confirm that every selected mechanism and every Accepted R are represented or explicitly unresolved.
12. Surface any shaping conflict and stop for an explicit decision.
13. Obtain acceptance before slicing.

## Quality checks

- The breadboard declares `current-state`, `candidate-shape`, or `selected-design` mode.
- Current-state evidence is not presented as selected future intent.
- A candidate-shape breadboard names the candidate and question it resolves.
- A candidate-shape breadboard states the authority status of its requirements and appetite inputs.
- Provisional candidate evidence is not presented as final fit or appetite evidence.
- Candidate evidence does not select a shape, feed slicing, or become build scope.
- A selected-design breadboard cites the selected shape, accepted requirements, appetite, and cut line.
- A selected-design breadboard maps each Accepted R to the selected shape part(s) and concrete breadboard IDs that embody it, or marks the requirement unresolved.
- Candidate rows are explicitly reconciled before becoming selected-design rows.
- Every required behavior has a trace from an entry to an observable consequence.
- Every observable consequence reverse-traces through all incoming wires to valid entries or explicit gaps.
- Every ID referenced by a wire or trace exists in the tables.
- Every displayed UI element that depends on data has an incoming source.
- Every code affordance triggers something, returns something, or both.
- Every meaningful branch has a modeled consequence, and state that affects later behavior has a writer and reader.
- Every selected mechanism is represented; every current-state claim is supported by evidence or marked unresolved.
- Important user-visible consequences and branches are first-class.
- Product-facing hidden behavior is preferred over abstract service decomposition.

## Affordance and seam test

Include a non-UI affordance when it does at least one of these:

- crosses a meaningful boundary
- makes a product-relevant decision
- changes state that affects later behavior
- produces an external side effect
- transforms data visible downstream
- coordinates steps whose order matters

Omit a row when it only forwards, wraps, renames, or exposes plumbing without changing the causal story. For current-state mapping, cite the actual code symbol or evidence even when the affordance uses product-facing wording.

## Structural invariants

- Give every displayed value an incoming source.
- Give every `N` a **Wires Out**, **Returns To**, or both.
- Represent behaviorally meaningful external state such as a URL, local storage, clipboard, browser history, queue, or database.
- Place a store where its data enables behavior, not merely where it is written.
- Model a backend, API, resolver, or external system as a place when it is part of the product story.
- Keep diagrams faithful to the tables; diagram-only nodes, wires, or branches are defects.

## Detailed notation, rendering, and slicing

Read [the notation, rendering, and slicing reference](references/notation-rendering-and-slicing.md) when you need:

- the complete element and relationship catalog
- chunking rules
- the recommended output template
- Mermaid rendering conventions
- selected-design slice creation, sequencing, exit conditions, and appetite cuts

Do not load that reference for a simple current-state or candidate-shape map that stops before slicing.
