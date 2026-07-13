# Start here: 10-minute path

Use this guide when you are new to the repo and want to know which planning move to make first.

> **Invocation note:** Commands beginning with `/` are Claude-oriented shorthand unless the [invocation matrix](./agent-invocation-matrix.md) shows support for your environment. Gemini supports a subset; Codex users should use the equivalent natural-language prompts.

Run the workflow from the product repository you are planning or building. Keep this repository separate unless you are contributing to the skills themselves. See [Using Planning Skills in a product repository](./using-in-a-product-repo.md).

## Pick the current state

| Current state | Use | Output |
|---|---|---|
| You have messy notes, a transcript, or a fuzzy request | `/frame` or `framing-doc/SKILL.md` | A frame with source, problem, outcome, and boundaries |
| You need criteria before solution ideas | `/criteria` or `shaping/SKILL.md` | Requirements / criteria separated from mechanisms |
| You know the problem but not the right solution | `/sketch-shapes`, `/fit-check`, `/select-shape`, `/shape`, or `shaping/SKILL.md` | Alternative shapes, fit check, selected direction |
| You dropped in a sketch, screenshot, wireframe, mockup, or whiteboard and need to know what it changes | `/reconcile-sketch`, `sketch-reconciliation/SKILL.md`, or the [sketch reconciliation guide](./sketch-reconciliation.md) | Observable visual evidence mapped to planning IDs, proposed deltas, a decision gate, and synchronized accepted updates |
| You selected a direction and need to make it concrete | `/breadboard` or `breadboarding/SKILL.md` | Places, affordances, stores, wiring, and slice candidates |
| A selected stateful scope has retries, timeouts, approvals, lifecycle stages, or several valid actions per state | `/statechart` or `statechart/SKILL.md` | A derived state inventory, transition table, Mermaid projection, and explicit gaps |
| Your selected slice crosses a meaningful boundary and field-level guessing would cause rework | `interface-contracts/SKILL.md` | Plain-language contracts for inputs, outputs, branches, errors, and open decisions |
| Your selected slice is ready for build handoff and needs examples, fixtures, expected outputs, edge cases, or tests | `executable-breadboards/SKILL.md` | A buildable, testable executable breadboard for the selected slice |
| The selected work needs vertical task groups, dependency-aware sequence, risk states, or scope cuts | `/dumplink` or `dumplink/SKILL.md` | A Dumplink plan with task groups, build sequence, cuts, checks, and agent handoff |
| You have too much planning context for an implementation agent | `/feed-context` or `feed-planning-context/SKILL.md` | A compact context packet with authority order, execution contract, and verification target |
| Implementation is underway and may be drifting | `/check-drift`, `.claude/loop.md`, or `templates/drift-check.md` | No drift found, or a planning drift note with recommended move |
| A meaningful agent run changed code or decisions | `templates/agent-run-log.md` | A concise run record with files, decisions, drift checks, verification, and handoff notes |
| You have code and need to compare it to the plan | `/reflect-breadboard` or `breadboard-reflection/SKILL.md` | Drift, synced reality, design smells, and follow-ups |
| You need a builder-facing handoff reference | `/kickoff` or `kickoff-doc/SKILL.md` | A kickoff doc organized by shaped territory |
| You are wiring a harness or external agent runtime | `.agent-orchestration.yaml` | Machine-readable modes, gates, artifacts, forbidden moves, and hooks |

## Recommended artifact home

Keep project-specific outputs in the product repository, usually under `planning/`. A typical starting set is `frame.md`, `shaping.md`, `breadboard.md`, `slices.md`, and `context-packet.md`; add reconciliation records and other advanced artifacts only when their triggering complexity exists.

## Minimal flow

```text
messy notes
  -> frame
  -> criteria
  -> sketch shapes
  -> fit check
  -> reconcile visual evidence whenever a sketch or screenshot changes the understanding
  -> select shape
  -> breadboard
  -> statechart, only when state complexity warrants it
  -> select slice
  -> add interface contracts, when boundary detail matters
  -> create executable breadboard, when ready for build handoff
  -> Dumplink, when task grouping / risk / sequence matters
  -> feed context with execution contract
  -> build with drift checks
  -> record meaningful run log
  -> reflect
```

## Before asking an agent to build

Check that you have:

- a selected shape, not just brainstorming
- requirements separated from mechanisms
- every consequential sketch or screenshot reconciled explicitly, with accepted deltas written back to the authoritative artifacts
- explicit non-goals
- a breadboard or slice boundary
- a statechart only when the selected scope's state behavior is difficult to understand from breadboard wiring alone
- plain-language interface contracts for meaningful boundary crossings, when field-level detail matters
- an executable breadboard when the slice needs examples, fixtures, expected outputs, edge cases, or tests
- a Dumplink plan when the work needs task groups, dependency order, risk states, or scope cuts
- a compact context packet
- an execution contract
- a verification target
- a human decision on what is in scope now

## During build

Use drift checks when the agent may have moved away from the selected plan.

Expected output is only one of:

```text
No planning drift found.
```

or

```text
Planning drift found:
- Selected artifact says:
- Current implementation direction is:
- Risk:
- Recommended move:
```

## If you are stuck

Use this default prompt:

```text
Use this repo's planning workflow. First decide whether we should frame, define criteria, sketch shapes, fit-check, reconcile a visual, select a shape, breadboard, optionally derive a statechart, create an interface contract, create an executable breadboard, create a Dumplink plan, feed context, check drift, build, record a run log, or reflect. Do not implement code until a slice is selected and the verification target is clear.
```
