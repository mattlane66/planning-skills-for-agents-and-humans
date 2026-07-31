# Start here: 10-minute path

Use this guide when you are new to the repository and want the smallest planning move that will help.

> **Invocation note:** Commands beginning with `/` are Claude-oriented shorthand unless the [invocation matrix](./agent-invocation-matrix.md) shows support for your environment. Gemini supports a subset; Codex users can use the equivalent natural-language prompts.

Run the workflow from the product repository you are planning or building. Keep this repository separate unless you are contributing to the skills themselves. See [Using Planning Skills in a product repository](./using-in-a-product-repo.md).

## Start with `/plan`

Most people should start with `/plan` or `planning-router/SKILL.md`.

The router inspects the current evidence and recommends exactly one next move. It may also recommend **No planning skill** for a small, obvious, low-risk change with clear behavior and scope.

It does not run the entire workflow, select a solution, or begin implementation.

## The three core moves

```text
frame → shape ↔ breadboard → selected-design breadboard
```

The arrows are not a conveyor belt. Breadboarding can support shaping before selection when a candidate needs behavioral clarification. After selection, breadboarding reconciles the accepted direction into normative selected-design intent.

| Move | Use it when | Output |
|---|---|---|
| `/frame` or `framing-doc/SKILL.md` | You have raw notes, research, requests, or an unclear problem. | A source-grounded frame with current approach/result, problem, outcome, and boundaries. |
| `/shape` or `shaping/SKILL.md` | The problem is clear enough to define criteria and Appetite, compare paths, use candidate evidence where needed, and make a human selection. | Accepted requirements, Appetite and cut line, alternative shapes, candidate evidence, fit checks, and a selected direction or decision-ready stop. |
| `/breadboard` or `breadboarding/SKILL.md` | You need to understand current behavior, test one candidate shape during shaping, or make a selected design concrete. | A `current-state`, `candidate-shape`, or `selected-design` map with places, affordances, stores, consequences, and wiring. Only an accepted selected-design breadboard can produce slice candidates. |

Start there. Add advanced moves only when the triggering complexity exists.

## Three breadboarding modes

| Mode | Purpose | Authority |
|---|---|---|
| `current-state` | Describe how an existing system behaves. | Descriptive evidence only; cannot define future intent. |
| `candidate-shape` | Resolve a specific behavioral uncertainty about one unselected shape. | Exploratory evidence subordinate to shaping; cannot select itself, feed slices, or become build scope. |
| `selected-design` | Reconcile the human-selected direction into concrete accepted behavior. | Normative after acceptance; may feed slicing and downstream build artifacts. |

A candidate breadboard does not automatically become selected-design. After selection, remove unselected mechanisms, reconcile surviving rows against the accepted shape and cuts, preserve unresolved gaps explicitly, and obtain acceptance.

## Conditional moves

| Current condition | Use | Output |
|---|---|---|
| A bounded planning destination requires multiple dependent decisions or investigations across sessions | `/wayfind` or `wayfinding/SKILL.md` | A shared coordination map with precise tickets, blockers, fog, and an exit check. |
| A sketch, screenshot, wireframe, mockup, or whiteboard may change accepted intent | `/reconcile-sketch` or `sketch-reconciliation/SKILL.md` | Observations mapped to stable IDs, proposed deltas, a human decision gate, and accepted updates. |
| A selected stateful scope has retries, timeouts, approvals, lifecycle stages, or several valid actions per state | `/statechart` or `statechart/SKILL.md` | Transition table, Mermaid projection, and explicit gaps derived from the selected-design breadboard. |
| A selected slice crosses a meaningful boundary and field-level ambiguity could cause rework | `interface-contracts/SKILL.md` | Plain-language inputs, outputs, branches, errors, and open decisions. |
| A selected slice needs fixtures, example runs, expected outputs, edge cases, or tests | `executable-breadboards/SKILL.md` | A buildable, testable behavioral handoff. |
| Work inside a selected slice needs vertical task groups, dependencies, risk, sequence, or scope cuts | `/dumplink` or `dumplink/SKILL.md` | A bounded task-group plan; before slice selection, candidates only. |
| An implementation agent has too much planning context | `/feed-context` or `feed-planning-context/SKILL.md` | A compact context packet with project language, authority order, execution contract, and verification target. |
| Implementation may have drifted from accepted intent | `/check-drift` or `/reflect-breadboard` | A no-drift result or an explicit comparison and correction decision. |
| Builders need a durable orientation reference | `/kickoff` or `kickoff-doc/SKILL.md` | A human-readable map of accepted product territory, not build scope or sequence. |

## Minimal route

```text
messy evidence
  → frame
  → accept criteria and Appetite
  → compare shapes
  ↔ candidate breadboards or focused spikes when a candidate is not judgeable
  → fit check and human selection
  → selected-design breadboard
  ↔ return to shaping if concrete behavior exposes a consequential conflict
  → select a demoable slice
  → add only the supporting detail that slice requires
  → feed bounded context
  → build with drift checks
```

Not every candidate needs a breadboard. Not every project needs every artifact.

Wayfinding is an optional outer loop around this route. Use it only when planning itself must persist across sessions; ordinary shaping remains the smaller move when the current decision fits one session.

## Recommended artifact home

Keep project-specific outputs in the product repository, usually under `planning/`.

A typical starting set is:

```text
planning/
  wayfinding/          # optional maps and tickets for multi-session planning
  frame.md
  shaping.md
  breadboard.md
  slices.md
  context-packet.md
```

Candidate breadboards may live beside `shaping.md` and should be named by candidate, for example `candidate-A-breadboard.md`. Keep them clearly non-authoritative unless and until they are reconciled into an accepted selected-design breadboard.

Add an Appetite card, reconciliation record, statechart, interface contract, executable breadboard, Dumplink plan, kickoff document, or reflection only when its triggering complexity exists.

## Before asking an agent to build

Check that you have:

- an explicitly selected direction
- accepted requirements separated from mechanisms
- an accepted Appetite and cut line
- explicit non-goals
- an accepted selected-design breadboard or equally clear implementation boundary
- a selected slice or equally clear implementation boundary
- no candidate breadboard being treated as build scope
- consequential visuals reconciled with accepted artifacts
- only the advanced detail the selected slice actually requires
- canonical project terms and relevant architectural decisions
- a compact context packet
- an execution contract and verification target
- a human decision on current scope

## During build

Use drift checks when implementation may have moved away from the selected plan.

Expected output is only:

```text
No planning drift found.
```

or:

```text
Planning drift found:
- Selected artifact says:
- Current implementation direction is:
- Risk:
- Recommended move:
```

## Default prompt

```text
Use this repository's planning router. Recommend exactly one next move—or no planning skill—based on the current uncertainty. Treat candidate breadboards as exploratory shaping evidence and selected-design breadboards as accepted intent. Do not run the entire workflow, select a solution, or implement code unless I explicitly authorize that move.
```
