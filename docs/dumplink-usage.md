# Dumplink usage

Dumplink ingests one selected, bounded project and creates the vertical task groups needed to build it. It dumps the work, clusters tasks into judgeable vertical slices, maps dependencies and risk, sequences the groups, defines appetite-based cuts, and stops for approval before one group becomes the active implementation slice.

Do not select a slice before running Dumplink. Creating those slices is Dumplink's job.

## When to use it

Use Dumplink when:

- a shaped project has been selected as a discrete unit of work
- the project boundary, exclusions, outcome, and non-goals are explicit
- there is a fixed appetite or bounded build pass
- the project needs more than one judgeable implementation increment
- horizontal tickets would lose the intended behavior
- risk, dependency order, or scope cuts need to be visible before coding

If no project is selected or its boundary is missing, return to framing, shaping, or the human project-selection gate. Do not invent task groups or a sequence.

## Command forms

Claude Code:

```text
/dumplink planning/shaping.md planning/breadboard.md "Project: accepted onboarding project; Appetite: 4 weeks"
```

Gemini CLI:

```text
/dumplink planning/shaping.md planning/breadboard.md "Project: accepted onboarding project; Appetite: 4 weeks"
```

Codex prompt:

```text
Use AGENTS.md and dumplink/SKILL.md.
Turn this selected project into a Dumplink plan.
Dump the work, create vertical task groups, mark risk states, map dependencies, sequence the build, define appetite-based cuts, and write acceptance checks.
Preserve the project boundary, exclusions, outcome, and non-goals. Treat every task group as a judgeable vertical slice of the project.
Stop for approval of the task-group plan and selection of the first active group. Create a bounded handoff only for the group I select.
Do not implement code.
```

## Output shape

A Dumplink plan should include:

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

## Core rule

The selected project is the input and hard outer boundary. Dumplink creates its implementation slices as task groups. After the human approves the plan and selects a group, that group becomes the active slice for contracts, executable examples, context packaging, and implementation.

Dumplink must not flatten the project into a generic ticket backlog, enlarge the selected project, or treat sequence order as approval of the active task group.
