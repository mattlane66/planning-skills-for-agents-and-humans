# Agent Instructions

Use this repository to preserve product intent from unclear evidence through bounded implementation.

These instructions are tool-neutral and apply across Claude Code, Codex, Gemini CLI, Cursor, and other agent environments. Load the active skill for detailed procedure instead of loading the whole planning stack.

## Default behavior

Use the smallest planning move that prevents an important misunderstanding.

For a small, obvious, low-risk change with clear behavior and scope, make the change directly. For ambiguous or consequential work, start with `planning-router/SKILL.md` or the runtime's `/plan` equivalent.

Do not write production code unless the user asks for implementation and a selected slice or equally clear boundary exists.

## Minimal route

```text
frame
→ shape
→ breadboard
→ select a demoable slice
→ add only the supporting detail that slice requires
→ feed bounded context
→ build and check drift
```

The three core planning moves are:

- `framing-doc` — clarify the real problem, desired outcome, evidence, and boundary
- `shaping` — define criteria and Appetite, compare solution directions, and stop for human selection
- `breadboarding` — make current or selected behavior concrete as places, affordances, stores, and wiring

Advanced moves are conditional, not a checklist:

- `sketch-reconciliation` when visual evidence may change accepted intent
- `statechart` when selected stateful behavior is hard to reason about from wiring alone
- `interface-contracts` when a meaningful boundary remains ambiguous
- `executable-breadboards` when a selected slice needs fixtures, examples, edge cases, or acceptance tests
- `dumplink` when work inside a selected slice needs vertical task groups, dependencies, risk, sequence, or cuts
- `kickoff-doc` when builders need a durable orientation reference
- `feed-planning-context` when an implementation agent needs only the authoritative subset
- `breadboard-reflection` when implementation reality may have drifted from accepted intent

## Human decision gates

Agents may gather facts, expose alternatives, and prepare decision-ready material. Humans decide:

- which problem or opportunity becomes the active frame
- which criteria are accepted
- what Appetite and cut line the bet deserves
- which shape is selected
- which slice is active
- whether drift changes the code, the plan, or the scope

Do not infer a decision from enthusiasm, recency, visual polish, or the fact that one option has more detail.

## Core discipline

Keep these distinctions intact:

- source evidence versus interpretation
- current approach versus desired future state
- problem versus solution
- requirements versus mechanisms
- current-state behavior versus selected-design intent
- accepted scope versus rejected or deferred ideas
- planning truth versus implementation reality

Requirements describe needs, outcomes, constraints, and quality bars. Shapes describe mechanisms. A selected slice governs active scope.

## Project language and decisions

When planning inside an existing product repository, inspect relevant sources before introducing terminology or seams:

- project `AGENTS.md`
- `CONTEXT.md`, `GLOSSARY.md`, or equivalent domain documentation
- `ARCHITECTURE.md`
- ADR or decision directories
- existing tests and public interfaces

Reuse established product language. Name existing architectural seams rather than inventing parallel abstractions. State whether selected work preserves or intentionally changes those seams. Propose glossary or ADR updates when an accepted decision introduces durable new language, but do not create or modify them without authorization.

Existing product-specific instructions remain authoritative unless the team explicitly changes them.

## Artifact authority

Use this default order when artifacts disagree:

1. user's latest explicit instruction
2. selected slice
3. executable breadboard, for expected examples and results within that slice
4. selected interface contract, for its named boundary
5. selected Dumplink task group, for grouping and sequence inside the slice
6. selected breadboard
7. selected shaping direction
8. kickoff document, for orientation only
9. framing document
10. raw notes and transcripts
11. rejected alternatives and brainstorming

Authority is concern-specific. No lower artifact may expand the selected slice.

A statechart is derived from the selected breadboard and never outranks it. A sketch-reconciliation record becomes authoritative only after accepted deltas are applied to the relevant source artifact. Run logs are audit records, not product truth.

Read `docs/agent-operating-reference.md` when resolving a complex authority conflict or preserving advanced artifact detail.

## Context feeding

Do not paste or load the whole planning stack by default.

Before implementation, provide a compact context packet containing only what the active task requires:

- current task and selected slice
- source artifacts and authority order
- accepted requirements, Appetite, cut line, and non-goals
- relevant places, affordances, stores, and wires
- relevant statechart rows, contracts, examples, or task group when present
- canonical project terms and relevant architectural decisions
- execution contract
- verification target

Keep raw notes and rejected alternatives out unless the task is discovery or reconstruction.

## Drift

If implementation reality conflicts with accepted planning intent, do not silently patch around the plan.

Return either:

```text
No planning drift found.
```

or:

```md
## Planning drift found

The selected artifact says:
- ...

The implementation reality is:
- ...

Options:
1. Update the code to match the artifact.
2. Update the artifact because the assumption was wrong.
3. Cut or split the slice.
4. Create a new bet.

Recommended move:
- ...
```

Do not implement inside a drift check. Apply only an explicit human decision.

## Stable IDs

Preserve established IDs. Do not rename them for style. When meaning changes materially, create a planning update or new ID.

Common defaults:

- `R0` requirements
- `P1` places
- `U1` and `N1` UI and non-UI affordances
- `S1` stores
- `ST1` and `TR1` states and transitions
- `C1` contracts
- `RUN1` and `E1` example runs and edge cases
- `SP1`, `TG1`, and `CUT1` spikes, task groups, and cuts
- `OBS1` and `D1` visual observations and reconciliation deltas
- `V1` vertical slices

Read `docs/stable-ids.md` for the complete reference and import rules.

## Orchestration and runtime adapters

`.agent-orchestration.yaml` is the machine-readable workflow and harness contract. It defines modes, gates, allowed outputs, forbidden moves, artifacts, and hooks.

Runtime wrappers are adapters to the canonical skills. Keep the product repository's own instructions authoritative. Use lifecycle hooks as visible reminders and guardrails, not as a hidden planning method.

## Artifact roles

- Frame — why the problem matters
- Shaping document — criteria, Appetite, alternatives, fit, and selection
- Appetite card — fixed budget, cut line, accepted uncertainty, and revisit conditions when those need a separate record
- Breadboard — structure and observable behavior
- Statechart — optional derived view of selected stateful behavior
- Interface contract — what crosses a meaningful boundary
- Executable breadboard — selected behavior plus fixtures, examples, expected results, and tests
- Dumplink — vertical task grouping and dependency-aware sequence inside a selected slice
- Kickoff document — human-readable orientation, not build scope
- Context packet — exact subset handed to the implementation agent
- Breadboard reflection — explicit comparison of accepted intent and implementation reality

## Completion standard

Planning is complete enough for the next move when:

- the active uncertainty has been resolved or made decision-ready
- the authoritative artifact is clear
- human gates have not been crossed implicitly
- advanced artifacts exist only when their triggering complexity is present
- the next agent receives bounded context and a verification target
