# Existing Codebase Drift — Example

This example shows how to use the planning workflow when implementation reality has diverged from the intended breadboard.

The point is not to blame the implementation. The point is to make drift visible so humans can decide whether the code should move back toward the plan, the plan should update to match reality, or the slice should be split.

## Scenario

A team shaped a simple account settings improvement:

> Users should be able to update their display name, see the saved value immediately, and recover clearly if saving fails.

A breadboard was created before implementation. Later, code was built quickly. The implementation mostly works, but the failure path and visible state do not match the intended behavior.

## Files

- `01-intended-breadboard.md` — the selected planning artifact before implementation
- `02-implementation-reality.md` — notes from reading the existing code and behavior
- `03-breadboard-reflection.md` — separate intent/reality records, drift, options, and a recommended decision

## How to use this example

Use the reflection skill:

```text
Use /reflect-breadboard on examples/existing-codebase-drift/01-intended-breadboard.md and examples/existing-codebase-drift/02-implementation-reality.md.
First record implementation reality without changing the accepted breadboard. Then compare, identify drift and smells, and prepare the correction decision.
```

Compare your output to `03-breadboard-reflection.md`.

## What to notice

- The reflection does not assume the original plan was automatically right.
- Drift is separated from critique.
- Human decision options are explicit.
- The recommended move explains whether to update code, update the plan, or split scope.
