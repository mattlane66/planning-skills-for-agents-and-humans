# Full modern agent workflow

This is the complete path for using the repo as a modern planning and harness layer.

Use it when work is large enough that a coding agent should not jump directly from a fuzzy request to implementation.

## Flow

Messy notes → frame → criteria → sketch shapes → fit check → select shape → breadboard → interface contracts → executable breadboard → Dumplink → context packet with execution contract → build with drift checks → run log → reflection.

## Stages

| Stage | Purpose | Output |
| --- | --- | --- |
| Frame | Name the problem, outcome, forces, and boundaries. | `planning/frame.md` |
| Criteria | Define the standards for judging fit before mechanisms take over. | requirements / criteria table |
| Sketch shapes | Make multiple solution shapes visible without selecting one. | candidate shapes |
| Fit check | Compare shapes against criteria and reverse-check mechanisms. | fit check + reverse fit check |
| Select shape | Record the human-selected direction. | selected direction + rejected alternatives |
| Breadboard | Map places, affordances, stores, wiring, and slice candidates. | `planning/breadboard.md` |
| Interface contracts | Define boundary-crossing data exchanges before agents guess field-level details. | `planning/interface-contracts.md` |
| Executable breadboard | Add fixtures, examples, expected outputs, edge cases, and acceptance tests. | `planning/executable-breadboard.md` |
| Dumplink | Create vertical task groups, dependency sequence, risk states, scope cuts, and an agent handoff packet. | `planning/dumplink.md` |
| Context packet | Feed only the relevant context to the implementation agent. | `planning/context-packet.md` |
| Drift check | Keep implementation inside the selected slice and active task group. | strict drift-check output |
| Run log | Leave a durable audit trail after meaningful agent work. | `planning/runs/YYYY-MM-DD-short-task.md` |
| Reflection | Compare implementation reality to the intended breadboard and repair drift. | `planning/breadboard-reflection.md` |

## Context packet must include

- active task
- source artifacts
- authority order
- must-preserve constraints
- current slice
- relevant contracts, executable examples, and Dumplink task group
- execution contract
- verification target

## Drift check output

A drift check must return only one of these two forms:

`No planning drift found.`

or:

`Planning drift found:` followed by selected artifact, current implementation direction, risk, and recommended move.

## Done standard

A modern agent workflow is complete when:

- requirements stayed separate from mechanisms
- the human-selected shape is explicit
- breadboard structure is preserved
- boundary contracts are explicit where needed
- executable examples and edge cases exist where needed
- Dumplink task groups are vertical and risk-aware
- context packet includes an execution contract
- drift checks use the strict output format
- meaningful agent work leaves a run log
- implementation reality is reflected back into planning artifacts
