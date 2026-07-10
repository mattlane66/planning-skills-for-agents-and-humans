# Codex usage

Codex should use `AGENTS.md` as the shared repo-level instruction surface and `.agent-orchestration.yaml` as the machine-readable workflow contract when a harness or agent wrapper can consume structured planning metadata.

That means Codex should follow the same planning defaults, authority order, shaping gates, context-feeding rules, stable ID rules, drift protocol, run-log expectations, and completion standard as other agents.

## What carries over directly

Codex should honor the workflow in `AGENTS.md`:

1. Frame the problem.
2. Define criteria.
3. Sketch alternative shapes.
4. Fit-check the alternatives.
5. Record the selected shape only when the human chooses one.
6. Breadboard the selected shape.
7. Slice into demoable increments.
8. Add interface contracts when the selected slice crosses meaningful boundaries.
9. Add an executable breadboard when the build handoff needs examples, fixtures, expected outputs, edge cases, or tests.
10. Use Dumplink when selected work needs vertical task groups, dependency-aware sequence, risk states, or appetite-based cuts.
11. Feed only the relevant planning context to implementation.
12. Check drift during implementation.
13. Reflect against implementation and repair drift.

The important behavior is the gate discipline:

- do not one-shot from fuzzy request to selected shape when the user asks for alternatives, sketches, or fit checks
- do not write production code unless the user explicitly selects a slice to build or asks for implementation
- preserve planning artifacts and update them when implementation discoveries change the plan
- create a run log or handoff note after meaningful implementation work

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

### Interface contract

```text
Use AGENTS.md and interface-contracts/SKILL.md.
Create plain-language interface contracts only for the selected slice boundaries in [breadboard or slice artifact].
Do not create production schemas, OpenAPI files, database schemas, or tests unless I explicitly ask.
```

### Executable breadboard

```text
Use AGENTS.md and executable-breadboards/SKILL.md.
Create an executable breadboard for [selected slice].
Include fixtures, example runs, expected visible results, expected state changes, edge cases, and acceptance tests.
Flag missing expected outputs or edge cases instead of inventing them.
Do not implement yet.
```

### Dumplink

```text
Use AGENTS.md and dumplink/SKILL.md.
Create a Dumplink plan for [selected shaped work] only if it needs vertical task groups, dependency-aware sequence, risk states, or scope cuts.
Preserve the selected shape, appetite, and non-goals. Do not create a horizontal discipline backlog or implement code.
```

## Context packet before implementation

Before using Codex for build work, use the context-feeding protocol instead of pasting the whole planning stack.

```text
Use AGENTS.md and feed-planning-context/SKILL.md.
Create a compact context packet for implementing [selected slice].
Include only the relevant frame, shaping decision, breadboard rows, contracts, examples, Dumplink task group when present, non-goals, execution contract, and verification target.
Do not implement yet.
```

Then give Codex the packet and explicitly name the selected slice to build.

## Drift check during implementation

Use this prompt before commits, after meaningful code changes, or whenever the agent may have drifted from the selected slice:

```text
Use AGENTS.md, docs/loop-prompting.md, and templates/drift-check.md.
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
Use templates/agent-run-log.md and docs/agent-run-records.md.
Create a concise agent run log for this session.
Include task, mode, source artifacts used, files inspected, files changed, decisions made, drift checks, verification run, planning updates needed, and handoff notes.
Do not make the run log the source of truth for product decisions; point to any planning artifacts that need updates.
```
