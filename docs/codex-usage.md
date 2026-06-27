# Codex usage

Codex should use `AGENTS.md` as the shared repo-level instruction surface.

That means Codex should follow the same planning defaults, authority order, shaping gates, context-feeding rules, stable ID rules, drift protocol, and completion standard as other agents.

## What carries over directly

Codex should honor the workflow in `AGENTS.md`:

1. Frame the problem.
2. Define criteria.
3. Sketch alternative shapes.
4. Fit-check the alternatives.
5. Record the selected shape only when the human chooses one.
6. Breadboard the selected shape.
7. Slice into demoable increments.
8. Feed only the relevant planning context to implementation.
9. Reflect against implementation and repair drift.

The important behavior is the gate discipline:

- do not one-shot from fuzzy request to selected shape when the user asks for alternatives, sketches, or fit checks
- do not write production code unless the user explicitly selects a slice to build or asks for implementation
- preserve planning artifacts and update them when implementation discoveries change the plan

## Equivalent Codex prompts

Codex does not need Claude's `.claude/commands/` files to use the method. Use these prompt forms instead.

### Criteria

```text
Use AGENTS.md and shaping/SKILL.md.
Run the criteria gate only.
Create or update the requirements / criteria table for: [source context].
Do not propose shapes, select a direction, breadboard, or implement.
```

### Sketch shapes

```text
Use AGENTS.md and shaping/SKILL.md.
Run the shape-sketch gate only.
Starting from these accepted criteria: [source context], sketch 2-4 alternative shapes.
Include CURRENT if this touches an existing system.
Do not fit-check, select a direction, breadboard, or implement.
```

### Fit check

```text
Use AGENTS.md and shaping/SKILL.md.
Run the fit-check gate only.
Compare the existing criteria and candidate shapes in [shaping file or source context].
Include the main fit check and reverse fit check.
Do not select a direction unless I explicitly choose one.
Do not breadboard or implement.
```

### Select shape

```text
Use AGENTS.md and shaping/SKILL.md.
Run the shape-selection gate only.
Record this human decision: [chosen shape].
Preserve rejected shapes as rejected and identify the next handoff.
Do not breadboard or implement unless the selected shape is explicit and I ask for it.
```

### Breadboard

```text
Use AGENTS.md and breadboarding/SKILL.md.
Breadboard only the selected shape in [shaping file or decision note].
Map places, affordances, stores, wiring, branches, and slice candidates.
Do not implement.
```

## Context packet before implementation

Before using Codex for build work, use the context-feeding protocol instead of pasting the whole planning stack.

```text
Use AGENTS.md and feed-planning-context/SKILL.md.
Create a compact context packet for implementing [selected slice].
Include only the relevant frame, shaping decision, breadboard rows, contracts, examples, edge cases, non-goals, and verification target.
Do not implement yet.
```

Then give Codex the packet and explicitly name the selected slice to build.
