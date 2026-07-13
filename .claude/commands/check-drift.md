---
description: Check implementation direction against selected planning artifacts and stop if drift is found.
argument-hint: [context packet, planning artifacts, implementation path, or notes]
allowed-tools: Read, Glob, Grep, Bash
---

Read `AGENTS.md`, `docs/loop-prompting.md`, and `templates/drift-check.md` first.

Use this command during or after implementation work to check whether the current implementation direction still matches the selected planning artifacts.

User request and source context:

$ARGUMENTS

Check against the highest-authority available artifacts, in this order:

1. latest explicit user instruction
2. selected slice or kickoff doc
3. executable breadboard, when present
4. selected interface contract, when present
5. selected Dumplink task group and sequence, when present
6. selected breadboard
7. selected shaping direction
8. framing doc
9. raw notes and transcripts
10. rejected alternatives and brainstorming

A statechart is derived from the selected breadboard and never outranks it.

Inspect only what is needed to answer the drift question. Do not broaden into a full code review.

Pay special attention to:

- selected slice boundary
- must-preserve constraints
- non-goals and exclusions
- selected shape versus rejected alternatives
- breadboard places, affordances, stores, and wiring
- relevant statechart states and transitions with their source breadboard IDs
- interface contracts
- executable breadboard examples, fixtures, expected outputs, edge cases, and tests
- active Dumplink task group, dependency order, risk state, and scope cuts
- verification target

Return only one of these forms:

```text
No planning drift found.
```

or

```text
Planning drift found:
- Selected artifact says:
- Current implementation direction is:
- Risk:
- Recommended move:
```

Do not implement changes.
Do not expand scope.
Do not invent new requirements.
Do not silently update planning artifacts.
If implementation reality conflicts with the plan, recommend a planning update or slice split instead of continuing.
