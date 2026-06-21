# Start here: 10-minute path

Use this guide when you are new to the repo and want to know which planning move to make first.

## Pick the current state

| Current state | Use | Output |
|---|---|---|
| You have messy notes, a transcript, or a fuzzy request | `/frame` or `framing-doc/SKILL.md` | A frame with source, problem, outcome, and boundaries |
| You know the problem but not the right solution | `/shape` or `shaping/SKILL.md` | Requirements, alternative shapes, fit check, selected direction |
| You selected a direction and need to make it concrete | `/breadboard` or `breadboarding/SKILL.md` | Places, affordances, stores, wiring, and slice candidates |
| Your selected slice crosses a meaningful boundary and field-level guessing would cause rework | `interface-contracts/SKILL.md` | Plain-language contracts for inputs, outputs, branches, errors, and open decisions |
| You have too much planning context for an implementation agent | `/feed-context` or `feed-planning-context/SKILL.md` | A compact context packet with authority order and verification target |
| You have code and need to compare it to the plan | `/reflect-breadboard` or `breadboard-reflection/SKILL.md` | Drift, synced reality, design smells, and follow-ups |
| You need a builder-facing handoff reference | `/kickoff` or `kickoff-doc/SKILL.md` | A kickoff doc organized by shaped territory |

## Minimal flow

```text
messy notes
  -> frame
  -> shape
  -> breadboard
  -> select slice
  -> add plain-language interface contracts, when boundary detail matters
  -> feed context
  -> build
  -> reflect
```

## Before asking an agent to build

Check that you have:

- a selected shape, not just brainstorming
- requirements separated from mechanisms
- explicit non-goals
- a breadboard or slice boundary
- plain-language interface contracts for meaningful boundary crossings, when field-level detail matters
- a verification target
- a human decision on what is in scope now

## If you are stuck

Use this default prompt:

```text
Use this repo's planning workflow. First decide whether we should frame, shape, breadboard, create an interface contract, feed context, build, or reflect. Do not implement code until a slice is selected and the verification target is clear.
```
