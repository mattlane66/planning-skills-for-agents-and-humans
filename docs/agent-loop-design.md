# Agent Loop Design

Agent loops should not replace planning. They should consume planning artifacts.

A loop is useful when the agent has a bounded goal, clear checks, an explicit Execution Appetite, and enough context to keep working without expanding the slice. It is risky when the agent is asked to "finish the feature" without a selected slice, non-goals, verification target, or stopping boundary.

## Loop inputs

Before starting a loop, feed the agent:

- selected slice
- execution appetite: Worth, Needed by, Protect, Cut first, Stop when
- verification target
- non-goals
- authority order
- allowed files / areas
- out-of-scope changes
- required checks
- return-to-planning conditions
- checkpoint cadence
- verification caveats to report

## Good loop

A good loop keeps working until a verifiable condition is met.

Example:

```text
/goal V1 is implemented, npm test exits 0, no files outside src/planning/* are changed, and the breadboard reflection has no unresolved drift.
```

Why this works:

- `V1` gives the work a boundary.
- `npm test exits 0` gives the work a check.
- `no files outside src/planning/*` limits expansion.
- `no unresolved drift` keeps implementation tied back to the planning artifact.

## Bad loop

A bad loop asks the agent to continue without a boundary or proof of completion.

Example:

```text
/goal finish the feature and make it good
```

Why this fails:

- no selected slice
- no source-of-truth artifact
- no non-goals
- no file boundary
- no required check
- no stop condition when implementation reality conflicts with the plan

## Use planning artifacts as control surfaces

Planning artifacts make loops safer because each artifact answers a different control question:

| Artifact | Control question |
| --- | --- |
| Frame | Why does this matter, and what world are we changing? |
| Shaping doc | Which direction was selected, and what was rejected? |
| Sketch reconciliation | Which visual observations were accepted, rejected, or left ambiguous, and where were accepted deltas applied? |
| Breadboard | What places, affordances, stores, and wiring make the solution work? |
| Interface contract | What crosses a boundary, and what must remain stable? |
| Executable breadboard | What examples, fixtures, expected outputs, edge cases, and tests define the selected slice? |
| Slice plan | What is the bounded unit of build work? |
| Context packet | What subset should the agent read now, and what Execution Appetite governs the run? |
| Run record | What actually happened, where did effort go, and what should the next bet learn? |
| Reflection | Did implementation drift from the shaped intent? |

## Execution appetite and contract template

Use these sections inside a context packet before asking an agent to work in a loop.

```md
## Execution appetite
- Worth:
- Needed by:
- Machine-resource ceiling (optional / runtime-specific):
- Protect:
- Cut first:
- Stop when:

## Execution contract
- Goal condition:
- Required checks:
- Allowed files / areas:
- Out-of-scope changes:
- Return-to-planning conditions:
- Checkpoint cadence:
- Verification caveats:
```

## Return to planning when

Pause the loop and repair the artifact when:

- the selected slice is too broad to verify
- required checks are missing or impossible to run
- implementation reality conflicts with the breadboard, contract, or executable breadboard
- the agent needs to touch files outside the allowed area
- a missing fixture, expected output, edge case, or field-level decision would require invention
- the implementation suggests the selected shape was wrong
- the run cannot clear the quality floor inside the current Execution Appetite

## Record meaningful runs

For meaningful agent loops, write a concise record under `planning/runs/` using `templates/run-record.md`.

Record realized human attention, optional runtime-specific resource evidence, what was verified or cut, where effort went (`figuring it out` versus `executing down`), and the shaping signal. A run record is audit evidence, not product truth.

Do not invent universal token, dollar, turn, or uphill/downhill targets. Calibrate from comparable real runs.

See `docs/agent-execution-appetite.md`.

## Core rule

Use loops for execution pressure, not for deciding what the product should be.

The planning stack should define the boundaries. The Execution Appetite should bound the run. The loop should work inside both, and the run record should return evidence for better shaping next time.
