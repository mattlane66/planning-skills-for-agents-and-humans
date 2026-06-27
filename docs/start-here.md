# Start here: 10-minute path

Use this guide when you are new to the repo and want to know which planning move to make first.

## Pick the current state

| Current state | Use | Output |
|---|---|---|
| You have messy notes, a transcript, or a fuzzy request | `/frame` or `framing-doc/SKILL.md` | A frame with source, problem, outcome, and boundaries |
| You need criteria before solution ideas | `/criteria` or `shaping/SKILL.md` | Requirements / criteria separated from mechanisms |
| You know the problem but not the right solution | `/sketch-shapes`, `/fit-check`, `/select-shape`, `/shape`, or `shaping/SKILL.md` | Alternative shapes, fit check, selected direction |
| You selected a direction and need to make it concrete | `/breadboard` or `breadboarding/SKILL.md` | Places, affordances, stores, wiring, and slice candidates |
| Your selected slice crosses a meaningful boundary and field-level guessing would cause rework | `interface-contracts/SKILL.md` | Plain-language contracts for inputs, outputs, branches, errors, and open decisions |
| Your selected slice is ready for build handoff and needs examples, fixtures, expected outputs, edge cases, or tests | `executable-breadboards/SKILL.md` | A buildable, testable executable breadboard for the selected slice |
| The selected work needs vertical task groups, dependency-aware sequence, risk states, or scope cuts | `/dumplink` or `dumplink/SKILL.md` | A Dumplink plan with task groups, build sequence, cuts, checks, and agent handoff |
| You have too much planning context for an implementation agent | `/feed-context` or `feed-planning-context/SKILL.md` | A compact context packet with authority order, execution contract, and verification target |
| Implementation is underway and may be drifting | `/check-drift`, `.claude/loop.md`, or `templates/drift-check.md` | No drift found, or a planning drift note with recommended move |
| A meaningful agent run changed code or decisions | `templates/agent-run-log.md` | A concise run record with files, decisions, drift checks, verification, and handoff notes |
| You have code and need to compare it to the plan | `/reflect-breadboard` or `breadboard-reflection/SKILL.md` | Drift, synced reality, design smells, and follow-ups |
| You need a builder-facing handoff reference | `/kickoff` or `kickoff-doc/SKILL.md` | A kickoff doc organized by shaped territory |
| You are wiring a harness or external agent runtime | `.agent-orchestration.yaml` | Machine-readable modes, gates, artifacts, forbidden moves, and hooks |

## Minimal flow

```text
messy notes
  -> frame
  -> criteria
  -> sketch shapes
  -> fit check
  -> select shape
  -> breadboard
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
- explicit non-goals
- a breadboard or slice boundary
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
Use this repo's planning workflow. First decide whether we should frame, define criteria, sketch shapes, fit-check, select a shape, breadboard, create an interface contract, create an executable breadboard, create a Dumplink plan, feed context, check drift, build, record a run log, or reflect. Do not implement code until a slice is selected and the verification target is clear.
```
