# Start here: 10-minute path

Use this guide when you are new to the repository and want the smallest planning move that will help.

> **Invocation note:** Commands beginning with `/` are Claude-oriented shorthand unless the [invocation matrix](./agent-invocation-matrix.md) shows support for your environment. Gemini supports a focused subset; Codex users can use the equivalent natural-language prompts.

Run the workflow from the product repository you are planning or building. Keep this repository separate unless you are contributing to the skills themselves. See [Using Planning Skills in a product repository](./using-in-a-product-repo.md).

## Start with what you actually have

You do **not** need to begin with a completed frame or requirements list.

Valid entry points include:

- **R-first** — you have needs, constraints, pain points, or requirements
- **S-first** — you already have a solution in your head
- **evidence-first** — you have a prototype, sketch, current workflow, or code behavior
- **uncertainty-first** — one fit question, spike, or candidate breadboard is the smallest useful move

The default interactive model is:

> **Exploration is fluid. Commitment is gated.**

During shaping, R, S, fit checks, focused spikes, sketches, and candidate breadboards may iterate in any useful order while they remain working material.

```text
requirements (R) ↔ shapes (S) ↔ fit checks
      ↑                ↕             │
      └── discoveries ← spikes / candidate breadboards / sketches
```

What stays strict is what becomes accepted truth or build scope.

## Start with `/plan` when you do not know the move

Most people can start with `/plan` or `planning-router/SKILL.md`.

The router inspects the current evidence and recommends exactly one next move. It may also recommend **No planning skill** for a small, obvious, low-risk change with clear behavior and scope.

It respects the user's useful entry point. It should not force S-first work back through framing or criteria merely because those artifacts are not yet finalized.

It does not run the entire workflow, select a solution, or begin implementation.

## Start with `/shape` when you want one collaborative surface

Use `/shape` or `shaping/SKILL.md` when the user wants to work fluidly across the problem and solution.

Examples:

```text
/shape "I have a rough idea for a timezone app. Capture it as Shape A, tease out the requirements it implies, and help me test/refine both."
```

```text
/shape planning/notes.md "Start from these requirements, but move into shapes, fit checks, spikes, or candidate breadboarding whenever useful. Do not select for me."
```

The broad shaping surface may move among R, S, fit, Appetite, spikes, and candidate evidence without pretending those moves are mandatory stages.

## Focused shaping moves

Use the smaller commands when you want to constrain the **current move**, not the whole process:

| Move | Use it when | What it means |
|---|---|---|
| `/criteria` | Work on requirements now | R may be first, or may have been extracted from an existing S. |
| `/appetite` | Work on budget/cut line now | Appetite may be Working before it is Accepted; selection waits for acceptance. |
| `/sketch-shapes` | Work on solution shapes now | Can be an S-first entry point. |
| `/fit-check` | Compare what is currently visible | May be a Working fit check if R or Appetite is provisional. |
| `/spike` | Resolve one technical or empirical unknown | May be triggered from R, S, fit, a sketch, or a breadboard. |
| `/breadboard` | Map current, candidate, or selected behavior | Candidate mode may use provisional R/Appetite in collaborative shaping. |
| `/select-shape` | Record the human decision | Requires the hard selection gate. |

These moves can repeat and move backward or sideways.

## The hard promotion gates

### Before selecting a shape

Require:

- a clear-enough frame or intentionally lightweight problem boundary
- **Accepted** requirements good enough to judge fit
- **Accepted** Appetite and cut line
- decision-ready alternatives and evidence
- fit, reverse-fit, and Appetite implications
- explicit human selection

### Before selected-design breadboarding

Require:

- selected shape
- accepted requirements
- accepted Appetite and cuts
- explicit reconciliation of any candidate evidence

### Before slicing or implementation

Require:

- accepted selected-design behavior or an equally clear accepted behavior boundary
- explicit human slice selection
- bounded context and verification target before build

These are promotion gates, not navigation locks.

## Collaborative versus gated/orchestrated profile

### Collaborative — default for interactive human shaping

Use when a person is actively guiding the work.

- provisional inputs are allowed
- exploration order is flexible
- R and S may revise each other
- working fit checks are allowed
- candidate breadboards may run before R/Appetite are accepted
- final selection and build gates remain strict

### Gated/orchestrated — for stronger automation or policy control

Use when a team, CI harness, or multi-agent planner wants deterministic prerequisites.

The controlled default is:

```text
accepted frame
→ accepted requirements
→ accepted Appetite
→ candidate shapes
↔ focused spikes / candidate breadboards
→ decision-ready fit
→ human selection
→ selected-design breadboard
→ selected slice
→ bounded build
```

The machine-readable contract is `.agent-orchestration.yaml`.

## Three breadboarding modes

| Mode | Purpose | Authority |
|---|---|---|
| `current-state` | Describe how an existing system behaves. | Descriptive evidence only; cannot define future intent. |
| `candidate-shape` | Resolve a specific behavioral uncertainty about one unselected shape. | Exploratory evidence subordinate to shaping; may use provisional judging inputs in collaborative mode; cannot select itself, feed slices, or become build scope. |
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
| A selected project needs vertical task groups, dependencies, risk, sequence, or scope cuts | `/dumplink` or `dumplink/SKILL.md` | A project-wide plan whose task groups are judgeable vertical slices; one becomes active after human selection. |
| An implementation agent has too much planning context | `/feed-context` or `feed-planning-context/SKILL.md` | A compact context packet with authority order, execution contract, and verification target. |
| Implementation may have drifted from accepted intent | `/check-drift` or `/reflect-breadboard` | A no-drift result or an explicit comparison and correction decision. |
| Builders need a durable orientation reference | `/kickoff` or `kickoff-doc/SKILL.md` | A human-readable map of accepted product territory, not build scope or sequence. |

## Recommended artifact home

Keep project-specific outputs in the product repository, usually under `planning/`.

```text
planning/
  wayfinding/          # optional maps and tickets for multi-session planning
  frame.md
  shaping.md
  candidate-A-breadboard.md  # optional exploratory evidence
  breadboard.md        # accepted selected-design intent
  slices.md
  context-packet.md
  spikes/
```

Add an Appetite card, reconciliation record, statechart, interface contract, executable breadboard, Dumplink plan, kickoff document, or reflection only when its triggering complexity exists.

## Before asking an agent to build

Check that you have:

- explicitly selected direction
- accepted requirements separated from mechanisms
- accepted Appetite and cut line
- explicit non-goals
- accepted selected-design breadboard or equally clear implementation boundary
- selected project boundary and active task group, selected slice, or equally clear implementation boundary
- no working shape or candidate breadboard being treated as build scope
- consequential visuals reconciled with accepted artifacts
- only the advanced detail the active implementation slice actually requires
- canonical project terms and relevant architectural decisions
- compact context packet
- execution contract and verification target
- human decision on current scope

## Default collaborative prompt

```text
Use this repository's planning workflow in collaborative mode.
Start from whatever is already concrete in my material: requirements, a proposed solution, a prototype, current-system evidence, or a specific unknown.
Move among R, S, fit checks, focused spikes, sketches, and candidate-shape breadboards whenever that is the smallest useful move.
Keep Working material separate from Accepted intent.
Do not force a fixed exploration sequence.
Do not select a shape until requirements and Appetite are accepted and the comparison is decision-ready.
Do not treat candidate evidence as selected intent or build scope.
Do not implement until a selected-design boundary and demoable slice are explicitly selected.
```

## Default gated prompt

```text
Use this repository's gated/orchestrated planning profile.
Enforce the prerequisites in .agent-orchestration.yaml and stop at every human promotion gate.
Do not relax the sequence unless I explicitly switch back to collaborative mode.
```
