---
description: Set, revise, or accept the bounded time or scope budget and cut line without forcing a fixed shaping sequence.
argument-hint:
- working or accepted criteria
- shaping file
- candidate shape
- budget
- team shape
- or review point
allowed-tools:
- Read
- Write
- Edit
- Glob
- Grep
disable-model-invocation: true
---

Read `shaping/SKILL.md` first and follow it as the primary instruction for this command.

Also read `docs/human-decision-gates.md`. Use `templates/appetite-card.md` when the decision needs a separate durable artifact; otherwise update the Appetite section of the shaping document.

Use this focused command when the current useful move is Appetite. In collaborative mode, Appetite may move from `Unset` to `Working` before it becomes `Accepted`; solution exploration may already exist. In gated/orchestrated mode, enforce the stricter prerequisites in `.agent-orchestration.yaml`.

User request and source context:

$ARGUMENTS

Record:

- authority: `Working` or `Accepted`
- time budget or other fixed scope budget
- team shape and review point
- explicit cut line
- uncertainty the team accepts
- unknowns that require a spike before selection or build
- decision owner and revisit condition when known

Treat Appetite as a constraint on selection, not as an estimate reverse-engineered from a preferred shape. Existing candidate shapes may be used to expose the consequences of a tentative budget, but they do not determine the budget automatically.

Do not select a direction, promote candidate evidence, or write production code.

End by naming the smallest next useful shaping move: revise R, revise S, fit-check, spike, candidate breadboard, accept/revisit Appetite, or prepare selection.
