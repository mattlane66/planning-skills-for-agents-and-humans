# Agent Execution Appetite

Product Appetite answers **how much human/team time a product bet is worth before selection**.

Execution Appetite answers a narrower question after a slice is selected:

> **How much human attention, delay, and machine resource is this implementation run worth before it should stop and return evidence?**

Do not replace Product Appetite with token math. Model prices, token accounting, context limits, tool runtimes, and billing models will change. Human time remains the durable scarcity.

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
What scope + approach fits?
   ↓
RUN
Work inside the boundaries. Stop before exceeding them.
   ↓
LEARN
What did the run teach us about the shape?
```

The governing rule is:

> **Decide what the outcome is worth. Define good enough. Shape the work to fit. When it does not, reshape the work—not the appetite.**

A larger appetite is allowed only as an explicit new bet, not an automatic top-up.

## What belongs in Execution Appetite

Keep the human-facing contract small:

- **Worth** — the human attention this run deserves: steering, review, correction, and decision time
- **Needed by** — a latency or deadline boundary only when delay matters
- **Machine-resource ceiling** — optional and runtime-specific: money, tokens, credits, compute, turns, or another meter
- **Protect** — MUST scope and the quality floor
- **Cut first** — explicitly optional scope
- **Stop when** — the condition that ends execution or returns it to planning

Machine-resource controls are implementation details. A runtime may compile the same appetite into a dollar cap today and a compute-credit or local-runtime limit later.

## Agent operating rule

Work to the outcome, not to exhaustion.

1. Protect the MUSTs and the quality floor. Treat NICE scope as expendable.
2. Use the smallest context, model effort, tooling, and number of steps that can reliably complete the active slice.
3. Resolve only uncertainty that could change the result. Do not explore merely because exploration is possible.
4. As the execution appetite narrows, drop optional scope and preserve verified state.
5. Do not silently broaden scope, increase a machine budget, or continue into another session.
6. If the quality floor cannot be reached inside the accepted appetite, stop at a coherent state and report what is known, verified, unresolved, and why.
7. Carry decisions and state forward, not the history used to discover them.
8. Treat a breaker trip as evidence. Diagnose the shape before changing the bet.
9. Another run requires either a reshaped execution plan or an explicit new bet.

## Product Appetite versus Execution Appetite

| Question | Product Appetite | Execution Appetite |
| --- | --- | --- |
| When? | Before shape selection | Before an implementation run or meaningful agent loop |
| Unit | Human/team time and cut line | Human attention first; latency when relevant; optional runtime-specific machine ceiling |
| Governs | Which product shape fits the bet | How one selected slice may be executed |
| Variable | Product scope and solution shape | Optional scope and execution architecture |
| Failure response | Cut, reshape, or stop the product bet | Land verified state, stop, inspect, reshape, or make a new bet |

Execution Appetite cannot expand the selected project or active slice.

## Carry state, not history

Long-running or multi-session work should preserve a bounded state artifact rather than replaying the entire discovery path.

Carry forward:

- resolved decisions
- verified invariants
- active blockers
- accepted boundaries and non-goals
- current slice and next objective
- evidence that could change the next decision

Do not carry raw history merely because it exists. One continuous session may use compaction when that is cheaper and clearer; multi-slice work should prefer fresh contexts with bounded handoffs.

## Figuring it out versus executing down

Dumplink already distinguishes `figuring-it-out` from `executing-down`.

Use the same language for run learning:

- **figuring it out** — reading, searching, experimenting, resolving uncertainty
- **executing down** — implementing, testing, verifying, packaging

High figuring-it-out effort is not automatically bad. It may represent necessary discovery. Repeated avoidable rediscovery is a shaping signal: the pitch, context packet, pre-solved decision, or slice boundary may be weak.

Do not impose a universal percentage target. Compare similar work over time.

## Runtime-neutral breakers

Planning should state behavior, not vendor APIs:

```text
Near limit:
- protect MUST
- cut NICE
- checkpoint verified state

At limit:
- stop

After:
- report what happened
- do not auto-extend
```

A runtime or harness may translate that policy into whatever controls it supports. The planning artifact remains vendor-neutral.

## Learn from runs

Meaningful agent runs should leave a concise record under `planning/runs/` using `templates/run-record.md`.

The run record is evidence, not product truth. It should answer:

- Did the run clear the quality floor?
- How much human attention did it consume?
- What optional scope was cut?
- Where did the work spend effort?
- Which uncertainty was necessary, and which was avoidable rediscovery?
- Should the next move continue, reshape, make a new bet, or stop?

Over time, use actual traces to calibrate execution policies. Do not invent universal token, turn, dollar, or uphill/downhill thresholds.

## Core loop

```text
selected slice
   ↓
set execution appetite
   ↓
execute
   ↓
verify or land cleanly
   ↓
record the run
   ↓
continue | reshape | new bet | stop
```

> **Shape the product before you build it. Shape the run before you execute it. Learn from both.**
