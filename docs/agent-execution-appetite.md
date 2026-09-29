# Agent Execution Appetite

Product Appetite and execution appetite solve different problems.

- **Product Appetite** asks how much human/team time an opportunity is worth before a shape is selected.
- **Execution appetite** asks how much attention, delay, and machine resource one selected implementation run is worth.

Do not replace Product Appetite with token or model budgets. Pricing, token accounting, context windows, and runtime controls change. Human attention and useful-by time remain durable constraints.

## The simple model

```text
OUTCOME
What must happen?
  ↓
FLOOR
What must be true for it to count?
  ↓
APPETITE
How much human time is this worth?
  ↓
SHAPE
What scope + execution approach fits?
  ↓
RUN
Work inside the boundaries. Stop before exceeding them.
  ↓
LEARN
What did the run teach us about the shape?
```

> **Decide what the outcome is worth. Define good enough. Shape the work to fit. When it does not fit, reshape the work—not the appetite.**

A larger appetite is allowed only as an explicit new bet.

## What an execution appetite contains

Keep the human-facing contract small:

- **Worth** — the human attention the run deserves: steering, review, correction, and decision time.
- **Needed by** — the useful-by time or latency boundary, only when delay matters.
- **Machine-resource ceiling** — optional and runtime-specific. It may be dollars, credits, tokens, turns, compute, or another meter.
- **Protect** — MUST scope and the quality floor.
- **Cut first** — NICE scope that may be removed without violating the quality floor.
- **Stop when** — conditions that end execution or return the work to planning.

Machine-resource ceilings are guardrails derived from the appetite, not the definition of appetite.

## Rules for agents

**Work to the outcome, not to exhaustion.**

1. Protect the MUSTs and the quality floor. Treat NICE scope as expendable.
2. Use the smallest context, model effort, tooling, and number of steps that can reliably complete the active slice.
3. Resolve only uncertainty that could change the result. Do not explore merely because exploration is possible.
4. As the execution appetite narrows, drop optional scope and preserve verified state.
5. Do not silently broaden scope, increase the budget, or continue into another session.
6. If the quality floor cannot be reached inside the accepted appetite, stop at a coherent state and return what is known, verified, unresolved, and why.
7. Carry decisions and state forward, not the history used to discover them.
8. Treat a breaker trip as evidence, not automatic permission to extend the run.
9. Another run requires a reshaped bet or an explicit new bet.

## Small and large runs

A small run can usually stay in one bounded context.

A larger run should prefer bounded slices with durable handoffs when carrying the full execution history would create unnecessary context, rediscovery, or review burden. A handoff should preserve:

- resolved decisions
- verified invariants
- active blockers
- next objective
- no-go boundaries

Do not replay history merely because it exists.

## Runtime-specific controls

Planning states intent. The runtime compiles it into whatever controls exist at the time.

Examples may include spend caps, token/task budgets, turn limits, compute credits, session ceilings, or local-resource limits. Those controls are implementation details and should not appear in the durable planning model unless the active runtime needs them.

Near the limit:
- protect MUST
- cut NICE
- preserve verified work
- checkpoint bounded state

At the limit:
- stop
- do not auto-extend

After the run:
- record what happened
- distinguish necessary discovery from avoidable rediscovery
- decide whether to continue, reshape, make a new bet, or abandon

## Relationship to Dumplink

Dumplink already tracks implementation groups as `figuring-it-out` and `executing-down`. Use that language rather than introducing a second hill-chart vocabulary.

A run record may note where effort went:

- **figuring it out** — reading, searching, experimenting, resolving uncertainty
- **executing down** — building, testing, verifying, packaging

Unexpected figuring-it-out effort is a shaping signal. Diagnose whether it was necessary discovery or avoidable rediscovery; do not apply a universal ratio target.

## Core rule

> **Shape the product before you build it. Shape the run before you execute it. Learn from both.**
