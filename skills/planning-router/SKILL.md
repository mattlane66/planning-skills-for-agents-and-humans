---
name: planning-router
description: Inspect product-planning context and choose the smallest next planning move when no specific skill is selected or planning may not be needed.
license: MIT
---

# Planning Router

Use this skill when the user wants help planning product work but has not selected a specific planning move, or when it is unclear whether planning ceremony would add value.

## Goal

Recommend exactly one next move—the smallest move that prevents an important misunderstanding—or recommend no planning skill.

The router does not run the full workflow, combine multiple artifacts, select a solution, or begin implementation.

## Inspect before asking

Use available files, repository evidence, conversation context, and attached artifacts to determine the current state. Look facts up instead of asking the user to repeat them. Ask only when a decision or missing scope boundary materially changes the route.

## Routing table

| Current condition | Next move |
|---|---|
| Small, obvious, low-risk change with clear behavior and scope | No planning skill |
| Raw notes, research, requests, or an unclear problem | `framing-doc` |
| Clear problem but unclear criteria, appetite, alternatives, or selected direction | `shaping` |
| A sketch, screenshot, wireframe, mockup, or whiteboard may change accepted intent | `sketch-reconciliation` |
| Current behavior or a selected design needs concrete places, affordances, stores, and wiring | `breadboarding` |
| An accepted stateful scope has retries, timeouts, approvals, lifecycle stages, or multiple valid actions per state | `statechart` |
| A selected slice crosses a meaningful boundary whose inputs, outputs, branches, or errors are ambiguous | `interface-contracts` |
| A selected slice needs fixtures, example runs, expected results, edge cases, and acceptance tests | `executable-breadboards` |
| Work inside a selected slice needs vertical task groups, dependencies, risk states, sequence, or appetite cuts | `dumplink` |
| An implementation agent needs only the authoritative subset for one active slice or task group | `feed-planning-context` |
| Implementation exists and may differ from accepted intent | `breadboard-reflection` |
| Builders need a durable human-readable orientation reference after accepted artifacts converge | `kickoff-doc` |

## Routing rules

1. Prefer no planning skill for a contained copy edit, obvious bug fix, disposable experiment, or already-clear low-risk change.
2. Route to the earliest unresolved decision, not the most advanced artifact that could eventually be useful.
3. Choose one move only. Do not prescribe the entire downstream chain.
4. Do not route to statechart, contracts, executable breadboards, Dumplink, kickoff, or context packaging merely because those skills exist. Their triggering complexity must be present.
5. Do not let an existing sketch bypass shaping and human selection when it introduces a solution that has not been accepted.
6. Do not let current-state breadboarding become selected future intent.
7. Do not begin implementation or make a human scope, appetite, or direction decision.

## Output

Return:

```md
Recommended next move: [skill name | No planning skill]

Why: [one or two sentences naming the current uncertainty]

What it should produce: [artifact or direct change]

Human gate: [decision required, or none]
```

When a skill is selected and the runtime supports skill invocation, hand off to only that skill. Otherwise name the canonical `SKILL.md` path or give the equivalent natural-language instruction.

## Completion criterion

The route is complete when one next move is named, its trigger is evidenced, unnecessary planning is rejected, and no downstream decision has been made prematurely.
