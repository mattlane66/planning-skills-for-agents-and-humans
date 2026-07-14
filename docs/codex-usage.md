# Codex usage

When maintaining this repository, Codex should use its `AGENTS.md` and `.agent-orchestration.yaml`. When the plugin is installed and Codex is working in a product repository, invoke the installed skills and keep that product repository's own `AGENTS.md` authoritative; the recipes below do not assume Planning Skills source paths exist beside the product code.

That means Codex should follow the same planning defaults, authority order, shaping gates, context-feeding rules, stable ID rules, drift protocol, run-log expectations, and completion standard as other agents.

## What carries over directly

Codex should honor this workflow while also following the active product repository's instructions:

1. Frame the problem.
2. Define criteria.
3. Set a bounded appetite and cut line.
4. Sketch alternative shapes.
5. Fit-check the alternatives against criteria and appetite.
6. Record the selected shape only when the human chooses one.
7. Reconcile sketches or screenshots explicitly whenever they reveal missing or conflicting detail.
8. Breadboard the selected shape.
9. Optionally derive a statechart when a selected stateful scope is hard to reason about from wiring alone.
10. Slice into demoable increments.
11. Add interface contracts when the selected slice crosses meaningful boundaries.
12. Add an executable breadboard when the build handoff needs examples, fixtures, expected outputs, edge cases, or tests.
13. Use Dumplink when selected work needs vertical task groups, dependency-aware sequence, risk states, or appetite-based cuts.
14. Feed only the relevant planning context to implementation.
15. Check drift during implementation.
16. Reflect against implementation and repair drift.

The important behavior is the gate discipline:

- do not one-shot from fuzzy request to selected shape when the user asks for alternatives, sketches, or fit checks
- do not write production code unless the user explicitly selects a slice to build or asks for implementation
- preserve planning artifacts and update them when implementation discoveries change the plan
- create a run log or handoff note after meaningful implementation work

## Equivalent Codex prompts

Codex does not need Claude's `.claude/commands/` files to use the method. Use these prompt forms instead.

### Criteria

```text
Use the installed `shaping` skill and follow this product repository's instructions.
Run the criteria gate only.
Create or update the requirements / criteria table for: [source context].
Do not propose shapes, select a direction, breadboard, or implement.
```

### Appetite

```text
Use the installed `shaping` skill and follow this product repository's instructions.
Run the appetite gate only.
Using these accepted criteria: [source context], record the fixed time or scope budget, team shape, review point, cut line, accepted uncertainty, and must-resolve unknowns.
Do not derive the appetite from a preferred shape. Do not select a direction, breadboard, or implement.
```

### Sketch shapes

```text
Use the installed `shaping` skill and follow this product repository's instructions.
Run the shape-sketch gate only.
Starting from these accepted criteria and appetite: [source context], sketch 2-4 alternative shapes.
Include CURRENT if this touches an existing system.
Do not fit-check, select a direction, breadboard, or implement.
```

### Fit check

```text
Use the installed `shaping` skill and follow this product repository's instructions.
Run the fit-check gate only.
Compare the existing criteria and candidate shapes in [shaping file or source context].
Include the main fit check, reverse fit check, and appetite-fit comparison with required cuts.
Do not select a direction unless I explicitly choose one.
Do not breadboard or implement.
```

### Select shape

```text
Use the installed `shaping` skill and follow this product repository's instructions.
Run the shape-selection gate only.
Record this human decision: [chosen shape].
Confirm that the choice fits the accepted appetite and name its binding cuts.
Preserve rejected shapes as rejected and identify the next handoff.
Do not breadboard or implement unless the selected shape is explicit and I ask for it.
```

### Reconcile a sketch or screenshot

```text
Use the installed `sketch-reconciliation` skill and follow this product repository's instructions.
Reconcile the attached visual with [frame, shaping, breadboard, or slice artifacts].
Separate visible observations from interpretations and map each observation to stable planning IDs.
Show proposed deltas and their fit/scope impact. Do not change selected behavior or scope until I accept them unless this prompt explicitly authorizes the update.
After acceptance, update every affected artifact and rerun fit checks when requirements or shape parts changed.
```

### Breadboard

```text
Use the installed `breadboarding` skill and follow this product repository's instructions.
Breadboard only the selected shape in [shaping file or decision note].
Map places, affordances, stores, wiring, branches, and slice candidates.
Do not implement.
```

### Interface contract

```text
Use the installed `interface-contracts` skill and follow this product repository's instructions.
Create plain-language interface contracts only for the selected slice boundaries in [breadboard or slice artifact].
Do not create production schemas, OpenAPI files, database schemas, or tests unless I explicitly ask.
```

### Statechart

```text
Use the installed `statechart` skill and follow this product repository's instructions.
Derive a statechart for [selected stateful scope] from [accepted breadboard].
Preserve source breadboard IDs and mark unsupported behavior as inferred or missing.
Treat the breadboard as authoritative and do not implement code.
```

### Executable breadboard

```text
Use the installed `executable-breadboards` skill and follow this product repository's instructions.
Create an executable breadboard for [selected slice].
Include fixtures, example runs, expected visible results, expected state changes, edge cases, and acceptance tests.
Flag missing expected outputs or edge cases instead of inventing them.
Do not implement yet.
```

### Dumplink

```text
Use the installed `dumplink` skill and follow this product repository's instructions.
Create a Dumplink plan for [selected shaped work] only if it needs vertical task groups, dependency-aware sequence, risk states, or scope cuts.
Preserve the selected shape, appetite, and non-goals. Do not create a horizontal discipline backlog or implement code.
```

## Context packet before implementation

Before using Codex for build work, use the context-feeding protocol instead of pasting the whole planning stack.

```text
Use the installed `feed-planning-context` skill and follow this product repository's instructions.
Create a compact context packet for implementing [selected slice].
Include only the relevant frame, shaping decision, accepted appetite and cut line, breadboard rows, statechart rows when present, contracts, examples, Dumplink task group when present, non-goals, execution contract, and verification target.
Do not implement yet.
```

Then give Codex the packet and explicitly name the selected slice to build.

## Drift check during implementation

Use this prompt before commits, after meaningful code changes, or whenever the agent may have drifted from the selected slice:

```text
Check drift between [context packet / selected planning artifacts] and [changed files or implementation direction].
Return only one of:

No planning drift found.

or

Planning drift found:
- Selected artifact says:
- Current implementation direction is:
- Risk:
- Recommended move:

Do not implement changes inside this drift check.
```

## Agent run log after meaningful work

Use this prompt after a meaningful implementation run:

```text
Create a concise agent run log for this session.
Include task, mode, source artifacts used, files inspected, files changed, decisions made, drift checks, verification run, planning updates needed, and handoff notes.
Do not make the run log the source of truth for product decisions; point to any planning artifacts that need updates.
```
