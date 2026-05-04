# Start Here: 10-Minute Path

Use this page when you are new to the repo and want to know which planning move to make first.

The goal is not to create every artifact. The goal is to create the next artifact that makes the work clearer for both humans and agents.

## Choose the next move

| Situation | Use | Output |
|---|---|---|
| You have messy notes, messages, or transcripts | `/frame` or `framing-doc/SKILL.md` | Frame |
| You know the problem but not the best solution direction | `/shape` or `shaping/SKILL.md` | Shaping doc with requirements, alternatives, fit check, and selected direction |
| You have a chosen direction but the behavior is still abstract | `/breadboard` or `breadboarding/SKILL.md` | Places, affordances, stores, wiring, and slices |
| You have too much planning context to feed an implementation agent | `/feed-context` or `feed-planning-context/SKILL.md` | Compact context packet |
| You have implementation and want to check whether it still matches the plan | `/reflect-breadboard` or `breadboard-reflection/SKILL.md` | Breadboard reflection with drift and follow-ups |
| You need a clean handoff doc after the team has converged | `/kickoff` or `kickoff-doc/SKILL.md` | Builder-facing kickoff doc |

## Minimal path

```text
messy source material
  -> frame
  -> shaping
  -> breadboard
  -> selected slice
  -> context packet
  -> implementation
  -> reflection
```

## First prompt to try

```text
Use the framing skill on these notes. Keep source evidence separate from interpretation. Produce a short frame with Source, Problem, Outcome, and Boundaries.
```

Then:

```text
Use the shaping skill on the frame. Separate requirements from mechanisms, compare at least two directions, run a fit check, and recommend the next human decision.
```

Then:

```text
Use the breadboarding skill on the selected shape. Map places, UI affordances, non-UI affordances, stores, and wiring. Then suggest demoable slices.
```

## Stop points

Stop and ask for a human decision when:

- the frame changes the problem or outcome
- requirements are still contested
- alternatives trade off meaningfully
- appetite is unclear
- a slice boundary would cut or include meaningful scope
- implementation reality conflicts with the plan

See [`human-decision-gates.md`](./human-decision-gates.md) for the full gate list.
