# Start Here: 10-Minute Path

Use this repo when you want AI and humans to create a plan that is clear enough to build from without collapsing too early into implementation.

## Choose your starting point

| If you have... | Start with... | Goal |
|---|---|---|
| Messy notes, transcripts, stakeholder messages, or raw discovery material | `/frame` or `framing-doc/SKILL.md` | Separate source evidence from the problem, outcome, and boundaries. |
| A clear problem but multiple possible solution directions | `/shape` or `shaping/SKILL.md` | Separate requirements from mechanisms, compare alternatives, and choose a direction. |
| A selected direction that still feels abstract | `/breadboard` or `breadboarding/SKILL.md` | Map places, affordances, stores, wiring, and likely slices. |
| Too many planning artifacts to feed into an implementation agent | `/feed-context` or `feed-planning-context/SKILL.md` | Create a compact context packet with authority order, non-goals, slice boundary, and verification target. |
| Code already exists and you need to check whether it matches the plan | `/reflect-breadboard` or `breadboard-reflection/SKILL.md` | Sync the breadboard to implementation reality, identify drift, and decide what to repair. |
| A team has already converged and a builder needs a reference doc | `/kickoff` or `kickoff-doc/SKILL.md` | Produce a builder-facing kickoff doc organized by system area. |

## The default path

```text
raw notes
  -> frame
  -> shaping doc
  -> selected shape
  -> breadboard
  -> slices
  -> context packet
  -> implementation
  -> breadboard reflection
```

## The minimum useful planning stack

For a small feature, do not create every artifact by default. Start with the smallest stack that prevents confusion.

```text
1. Frame
2. Shaping doc
3. Breadboard
4. Context packet for the selected slice
```

Add a kickoff doc only when another builder needs a durable handoff. Add a breadboard reflection only after implementation exists.

## First prompt to try

```text
Use this repo's planning workflow. Start in Explore mode. Tell me whether this source material needs a frame, shaping doc, breadboard, or context packet first. Do not implement code yet.

[source material here]
```

## Good stopping points

Stop and ask for a human decision when:

- the frame names the problem and outcome
- requirements are proposed
- alternatives have been compared
- a shape is ready to select
- appetite or scope must be set
- the breadboard is concrete enough to slice
- implementation reality conflicts with the plan

See `docs/human-decision-gates.md` for the full gate list.
