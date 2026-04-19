# Simple Grocery List — Step-by-Step Example

This example shows how to use the skills in this repo on a tiny, easy-to-understand feature:

> A shared grocery list app where a user can add items, mark them as bought, hide bought items, and keep the list between sessions on the same device.

The point is not the app itself. The point is to make the workflow obvious.

## Why this example is useful

It is small enough that you can see the whole process without getting lost in implementation detail.

It also includes one important shaping lesson: some early solution ideas belong in the shape, not in the requirements.

## Files in this example

- `00-source-notes.md` — the messy starting point
- `01-frame.md` — output of `/framing-doc`
- `02-shaping.md` — output of `/shaping`
- `03-kickoff.md` — optional handoff output of `/kickoff-doc`
- `04-breadboard.md` — output of `/breadboarding`
- `05-breadboard-reflection.md` — post-implementation example of `/breadboard-reflection`

## Step 1 — Start with messy source material

Open `00-source-notes.md`.

Use `/framing-doc` when you have raw notes, requests, or transcript-like material and need a clean statement of the problem and outcome.

Example prompt:

```text
Use /framing-doc on examples/simple-grocery-list/00-source-notes.md.
Create a short frame with Source, Problem, Outcome, and Boundaries.
Keep solution ideas out of the problem statement unless they are true constraints.
```

Compare your output to `01-frame.md`.

## Step 2 — Shape the problem and compare solution directions

Use `/shaping` once the problem is clear enough to define requirements and compare solution directions.

Example prompt:

```text
Use /shaping with examples/simple-grocery-list/01-frame.md.
Create requirements, then sketch two solution directions.
Keep requirements free of named mechanisms unless they are true constraints.
Then run a fit check and choose a direction for V1.
```

Compare your output to `02-shaping.md`.

What to notice:
- the requirements are written as needs, not implementation choices
- there are two shapes, not one
- the fit check makes trade-offs visible
- the chosen direction is explicit

## Step 3 — Create a kickoff doc only if you need a handoff

Use `/kickoff-doc` when a project has already been discussed and shaped enough that another builder needs a clean reference doc.

If you are working solo, you may not need this step.

Example prompt:

```text
Use /kickoff-doc on examples/simple-grocery-list/02-shaping.md.
Create a builder-facing kickoff doc organized by system area, not by conversation order.
Capture the chosen direction only.
```

Compare your output to `03-kickoff.md`.

## Step 4 — Breadboard the chosen shape

Use `/breadboarding` after a direction is chosen and concrete enough to map.

Example prompt:

```text
Use /breadboarding on the selected shape from examples/simple-grocery-list/02-shaping.md.
Create places, UI affordances, non-UI affordances, stores, and wiring.
Then identify likely slices.
```

Compare your output to `04-breadboard.md`.

What to notice:
- the breadboard maps one chosen direction, not all possible directions
- UI, code, and state are visible in one system view
- slices come after the structure is visible

## Step 5 — Reflect only after implementation exists

Use `/breadboard-reflection` after code exists and you want to compare the breadboard to reality.

Always sync the breadboard to implementation first. Only then critique the design.

Example prompt:

```text
Use /breadboard-reflection on examples/simple-grocery-list/04-breadboard.md.
Assume the implementation drifted from the chosen shape.
First sync the artifact to reality, then identify smells and propose fixes.
```

Compare your output to `05-breadboard-reflection.md`.

## Quick rule of thumb

- **Messy notes or transcript?** → `/framing-doc`
- **Need requirements and solution options?** → `/shaping`
- **Need a handoff doc for another builder?** → `/kickoff-doc`
- **Need to make the chosen direction legible as a system?** → `/breadboarding`
- **Need to compare implementation to the breadboard later?** → `/breadboard-reflection`
