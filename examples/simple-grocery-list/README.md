# Simple Grocery List — Step-by-Step Example

This example shows the foundational Frame → Shape → Breadboard workflow on a tiny, easy-to-understand feature:

> A small same-device grocery list where a user can add items, mark them as bought, hide bought items, and keep the list between sessions.

The point is not the app itself. The point is to make the workflow obvious.

It intentionally stops short of the advanced interface-contract, executable-breadboard, Dumplink, context-packet, drift-check, and run-log steps. It also skips Statechart because this small flow is already legible in the breadboard wiring. Use [`docs/start-here.md`](../../docs/start-here.md) to choose those moves when a larger project needs them.

## Why this example is useful

It is small enough that you can see the whole process without getting lost in implementation detail.

It also includes one important shaping lesson: some early solution ideas belong in the shape, not in the requirements.

## Files in this example

- `00-source-notes.md` — the messy starting point
- `01-frame.md` — output of the `framing-doc` skill
- `02-shaping.md` — output of the `shaping` skill
- `03-kickoff.md` — optional handoff output of the `kickoff-doc` skill
- `04-breadboard.md` — output of the `breadboarding` skill
- `05-breadboard-reflection.md` — post-implementation example of the `breadboard-reflection` skill

## Core workflow

1. Start with messy source material.
2. Create a frame.
3. Shape the problem, set the appetite, and compare solution directions.
4. Choose a direction that fits the appetite.
5. Breadboard the chosen shape.
6. Reflect only after implementation exists.

## Optional handoff step

Create a kickoff doc only if another builder needs a clean reference doc organized by system area.

## Step 1 — Start with messy source material

Open `00-source-notes.md`.

Use the `framing-doc` skill when you have raw notes, requests, or transcript-like material and need a clean statement of the problem and outcome.

Example prompt:

```text
Use the framing-doc skill on examples/simple-grocery-list/00-source-notes.md.
Create a short frame with Source, Problem, Outcome, and Less about / More about if needed.
Keep solution ideas out of the problem statement unless they are true constraints.
```

Compare your output to `01-frame.md`.

## Step 2 — Shape the problem and compare solution directions

Use the `shaping` skill once the problem is clear enough to define requirements, set an appetite, and compare solution directions.

Example prompt:

```text
Use the shaping skill with examples/simple-grocery-list/01-frame.md.
Create requirements, record the small first-version appetite and cut line, then sketch two solution directions.
Keep requirements free of named mechanisms unless they are true constraints.
Then run a fit check and reverse fit check. Stop with a decision-ready summary so the human can choose the direction for V1.
```

Compare your output to `02-shaping.md`.

What to notice:
- the requirements are written as needs, not implementation choices
- the appetite and cut line are explicit before the human selection
- there are two shapes, not one
- the fit check makes trade-offs visible
- the chosen direction is explicit
- the example records a human selection rather than asking the agent to choose

## Step 3 — Breadboard the chosen shape

Use the `breadboarding` skill after a direction is chosen and concrete enough to map.

Example prompt:

```text
Use the breadboarding skill on the selected shape from examples/simple-grocery-list/02-shaping.md.
Create places, UI affordances, non-UI affordances, stores, and wiring.
Then identify likely slices.
```

Compare your output to `04-breadboard.md`.

What to notice:
- the breadboard maps one chosen direction, not all possible directions
- UI, code, and state are visible in one system view
- slices come after the structure is visible

## Step 4 — Reflect only after implementation exists

Use the `breadboard-reflection` skill after code exists and you want to compare the breadboard to reality.

Always sync the breadboard to implementation first, then critique the design.

Example prompt:

```text
Use the breadboard-reflection skill on examples/simple-grocery-list/04-breadboard.md.
Assume the implementation drifted from the chosen shape.
First sync the artifact to reality, then identify smells and propose fixes.
```

Compare your output to `05-breadboard-reflection.md`.

## Optional Step 5 — Create a kickoff doc for handoff

Use the `kickoff-doc` skill when a project has already been discussed and shaped enough that another builder needs a clean reference doc.

If you are working solo, you may not need this step.

Example prompt:

```text
Use the kickoff-doc skill on examples/simple-grocery-list/02-shaping.md.
Create a builder-facing kickoff doc organized by system area, not by conversation order.
Capture the chosen direction only.
```

Compare your output to `03-kickoff.md`.

## Quick rule of thumb

- **Messy notes about the raw idea/strategy/opportunity and/or interview transcript?** → `framing-doc`
- **Need requirements, appetite, and solution options?** → `shaping`
- **Need to make the chosen direction legible as a system?** → `breadboarding`
- **Need to compare implementation to the breadboard later?** → `breadboard-reflection`
- **Need a handoff doc for another builder?** → `kickoff-doc`
