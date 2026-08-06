---
name: dumplink
description: Turn a selected, bounded project into sequenced vertical task groups with dependencies, risks, appetite-based cuts, acceptance checks, and a bounded handoff.
license: MIT
---

# Dumplink

Use this skill after a project has been framed, shaped, selected, and given a fixed appetite. The project is the discrete unit of work Dumplink ingests. Dumplink discovers the implementation slices by turning that project into vertical task groups; it does not require a slice to be selected first.

The selected project is the hard outer boundary. Each task group is a vertical slice of that project: a judgeable increment that cuts through the necessary disciplines and produces observable behavior or a meaningful project state. A task group may divide the project, but it may not redefine or enlarge it.

## Goal

Produce a Dumplink plan that shows:

- the selected project and its explicit boundary
- the raw task dump inside that project
- vertical task groups that Dumplink derived from the project
- unknowns, knowns, and done states at the task-group level
- causal dependencies between task groups
- a build sequence that starts with risky and dependency-unlocking work
- possible cuts if the appetite runs out
- acceptance checks for the project and each task group
- the human decision required before one task group becomes the active implementation slice

## Required input and gate

Full Dumplink planning requires an explicit selected project with:

- a desired outcome
- a fixed appetite or time budget
- a selected approach
- non-goals and boundary exclusions
- enough accepted behavior or design evidence to identify judgeable increments

If the project is not selected or its boundary is missing, do not invent task groups, a build sequence, or a handoff. State what project decision is missing and return to framing, shaping, or the appropriate human gate.

After the plan is created, stop for approval of the task-group plan and selection of the first active task group. That selected task group becomes the active implementation slice for downstream contracts, executable examples, context packaging, and build work.

## Source concept

Dumplink uses three core moves:

1. **DUMP** — list everything the team thinks must happen to build the selected project.
2. **CLUSTER** — group tasks into isolated vertical task groups that can produce judgeable behavior.
3. **SEQUENCE** — connect task groups by dependency and risk so the team knows what to solve first.

The source tool and concept are from Dumplink: https://github.com/klausbreyer/dump.link.

## When to use

Use this when:

- a selected, bounded project has been bet on
- the team has an appetite, usually 2–6 weeks
- the project needs more than one judgeable implementation increment
- horizontal task planning would lose the project's intent
- the team needs vertical task groups, risk states, dependencies, sequence, or appetite-based cuts

Do not use this when:

- the work is reactive support, bugs, or interrupt-driven operations
- the problem or project boundary is still unframed
- no project has been selected
- the team already has one small, obvious implementation slice and no grouping decision remains
- the team needs an exact file-by-file coding plan rather than project decomposition

## Inputs

Ask for or infer from available artifacts:

- selected project pitch or shaping document
- appetite / time budget
- desired outcome and demo target
- selected approach and non-goals
- explicit project boundary and exclusions
- accepted breadboard or other behavioral evidence, when available
- known risks, rabbit holes, constraints, and dependencies
- existing codebase or implementation context, when available

Proceed within the declared project boundary and label assumptions. If that boundary is missing or contested, stop at the project-selection gate.

## Output

Create these sections:

1. Project boundary
2. Task dump
3. Vertical task groups
4. Unknowns / knowns / done states
5. Dependency map
6. Build sequence
7. Scope cuts
8. Acceptance checks
9. Task-group approval gate
10. Active task-group handoff, only after human selection

## Method

### 1. Preserve the project intent

Restate the selected project in compact form:

- desired outcome
- appetite
- target user / operator
- selected approach
- project boundary and exclusions
- non-goals
- what must remain true
- demo target

Do not immediately turn everything into implementation tickets. First preserve the project's intent and hard boundary.

### 2. Dump tasks

Create an unordered list of likely tasks. Include design, product, data, content, migration, technical, QA, and launch work when relevant.

Rules:

- keep tasks rough at first
- do not sequence while dumping
- include unknowns as tasks to investigate
- do not hide design or decision work
- do not over-split into microscopic chores

Use IDs such as `T1`, `T2`, `T3`.

| ID | Task | Type | Known/Unknown | Notes |
|---|---|---|---|---|
| T1 |  | product / design / code / data / QA / launch | unknown |  |

### 3. Cluster tasks into vertical task groups

Derive task groups from the project by grouping tasks that can be completed together and judged as one vertical slice.

A good task group:

- produces one judgeable behavior or meaningful project state
- cuts through every discipline needed for that behavior
- has clear inputs and outputs
- can be demoed or inspected independently
- stays inside the selected project
- avoids categories such as frontend, backend, design, or QA unless the work truly cannot be sliced vertically

Use IDs such as `TG1`, `TG2`, `TG3`. Preserve stable IDs once assigned.

| ID | Name | Included tasks | Vertical slice / behavior produced | Risk state | Cuttable? | Notes |
|---|---|---|---|---|---|---|
| TG1 |  | T1, T4 |  | unknown / known / done | no |  |

### 4. Mark state by risk, not task count

Track state at the task-group level:

- `not-started` — no meaningful learning or execution yet
- `figuring-it-out` — important unknowns remain
- `executing-down` — key unknowns are solved; work is being completed
- `done` — the group produces its intended behavior and passes its checks
- `cut` — the group was intentionally removed to protect the appetite

The state of a task group is the state of its riskiest important task. Do not let a pile of easy completed tasks hide one unresolved unknown.

### 5. Map dependencies

Draw causal links between task groups. Ask:

- what input does this group need before it can be completed?
- what does this group unlock?
- what unknown could cause rework if found late?
- which group has more outgoing than incoming dependencies?

| From | To | Why this dependency exists | Risk if delayed |
|---|---|---|---|
| TG1 | TG3 |  |  |

Use a compact Mermaid diagram when it makes the dependency order easier to judge.

### 6. Sequence the build

Prefer this order:

1. risk-unlocking task groups
2. dependency-unlocking task groups
3. core user-visible behavior
4. finishing, polish, and launch groups

Do not start with easy polish if a hidden unknown can sink the project later.

| Order | Task group | Why now | Demo/checkpoint | Exit condition |
|---|---|---|---|---|
| 1 | TG1 |  |  |  |

### 7. Identify scope cuts

Variable scope protects a fixed appetite. Define cuts before panic.

For each possible cut, state:

- which task group or optional behavior is removed or deferred
- what still works
- what user or business value remains
- what follow-up decision is needed later

A cut may remove optional work while preserving the selected project's promised outcome. If it changes the project outcome, boundary, demo target, or fixed non-goal, present it as a proposed project update and stop for human approval.

| Cut option | Remove/defer | Preserved behavior | Cost of cutting | Later decision |
|---|---|---|---|---|
| C1 |  |  |  |  |

### 8. Write acceptance checks

Write checks at two levels:

- project checks prove the selected project's promised outcome remains achievable
- task-group checks prove each vertical slice is independently judgeable

Use checks such as:

- A user can complete X end-to-end.
- The system preserves Y state after Z.
- The operator can see whether W is unknown, known, done, or cut.
- The project can ship a coherent version without the cut groups.

### 9. Stop for task-group approval

Present the proposed task groups, dependency map, sequence, cuts, and a recommended first group. Ask the human to approve or revise the plan and select the active task group. Do not infer selection from ordering alone.

### 10. Prepare the active task-group handoff

Prepare this packet only after a human selects the active task group:

```text
Selected project:
Active task group (vertical slice):
Source artifacts:
Must preserve:
Do not build:
Included tasks:
Dependencies already satisfied:
Known unknowns:
Acceptance check:
Stop condition:
```

Feed one active task group to an implementation agent at a time. The Dumplink plan retains project-wide sequence; the handoff carries only the active slice and its necessary context.

## Quality bar

A good Dumplink output:

- names one selected project as its input and keeps every task group inside it
- creates the implementation slices instead of asking for one as input
- avoids horizontal task silos
- makes every task group independently judgeable
- reveals unknowns early
- sequences by risk and dependency, not convenience
- names cuts explicitly
- stops for plan approval and active task-group selection
- gives an implementation agent one bounded vertical slice at a time

## Common failure modes

- Asking for a preselected implementation slice before decomposing the project
- Turning the selected project into a flat ticket backlog
- Clustering by discipline instead of judgeable behavior
- Treating task count as progress
- Hiding unknowns inside vague engineering tasks
- Sequencing by ease instead of risk
- Deferring dependency-unlocking work too late
- Treating scope cuts as failure instead of appetite discipline
- Feeding an agent the whole project instead of the active task group
- Letting a task group quietly expand the selected project
- Treating sequence order as human approval of the active task group
