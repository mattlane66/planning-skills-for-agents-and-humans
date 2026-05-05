# Start Here

Use this repo when you want an AI agent and a human team to create planning artifacts before implementation.

## Fast path

| Situation | Use | Output |
|---|---|---|
| Messy notes, transcript, or vague request | `/frame` or `framing-doc/SKILL.md` | Frame with source, problem, outcome, and boundaries |
| Clear problem but multiple possible approaches | `/shape` or `shaping/SKILL.md` | Requirements, alternative shapes, fit check, selected direction |
| Chosen direction needs concrete behavior | `/breadboard` or `breadboarding/SKILL.md` | Places, affordances, stores, wiring, and slice candidates |
| Too many artifacts for an implementation agent | `/feed-context` or `feed-planning-context/SKILL.md` | Compact context packet with authority order and verification target |
| Implementation exists and may have drifted | `/reflect-breadboard` or `breadboard-reflection/SKILL.md` | Synced reality, drift, smells, planning updates, follow-ups |
| Team needs a handoff reference | `/kickoff` or `kickoff-doc/SKILL.md` | Builder-facing kickoff doc organized by system area |

## Minimal workflow

1. Start with source notes.
2. Create a frame.
3. Shape requirements and alternatives.
4. Choose a direction.
5. Breadboard the selected direction.
6. Slice into demoable increments.
7. Feed only the selected context to the implementation agent.
8. Reflect after implementation and repair drift.

## Human checkpoints

Do not let the agent silently decide the important moments.

At minimum, a human should confirm:

- the frame captures the real problem and outcome
- the requirements are the right standards of fit
- the selected shape is the direction to pursue
- the appetite is appropriate for the bet
- the breadboard behavior is right before slicing
- the selected slice is what should be built first
- any drift should be resolved by changing code, changing the plan, or cutting scope

See `docs/human-decision-gates.md` for the full version.

## First prompt examples

```text
Use /frame on these notes. Keep source evidence separate from interpretation and stop before shaping.
```

```text
Use /shape on this frame. Separate requirements from mechanisms, compare at least two directions, and run a fit check.
```

```text
Use /breadboard on the selected shape. Create places, affordances, stores, wiring, and candidate slices.
```

```text
Use /feed-context to package the selected frame, shape, breadboard, and slice for an implementation agent.
```

## Rule of thumb

If the agent is about to build but cannot name the selected slice, demo path, non-goals, and verification target, it is not ready to build.
