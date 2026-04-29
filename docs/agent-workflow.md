# Agent Workflow

This repo is planning-first. Use it to keep agents in the uphill shaping lane until the team intentionally selects a buildable slice.

The workflow is tool-neutral. Claude Code, Cursor, Codex, and similar tools can all use the same artifacts; only the invocation mechanics differ.

## Modes

### 1. Explore

Use when the codebase, problem, or source material is not yet understood.

Good outputs:
- source notes
- current-state summary
- open questions
- risks and unknowns

Do not jump to implementation in Explore mode.

### 2. Frame

Use when the team needs to know what problem is worth solving and why.

Good outputs:
- `planning/frame.md`
- source, problem, outcome, and boundaries
- less-about / more-about distinctions

The frame is the why, not the how.

### 3. Shape

Use when multiple solution directions are possible.

Good outputs:
- `planning/shaping.md`
- requirements or criteria
- alternative shapes
- fit check
- reverse fit check
- selected direction
- known unknowns or spikes

Keep requirements separate from mechanisms.

### 4. Detail

Use after a direction is selected and the team needs concrete behavior.

Good outputs:
- `planning/breadboard.md`
- places
- UI affordances
- non-UI affordances
- stores
- wiring
- product-relevant branches

The tables are the source of truth. Diagrams are renderings.

### 5. Slice

Use when the breadboard is concrete enough to become demoable increments.

Good outputs:
- `planning/slices.md`
- slice names
- demo statement
- `Produces:` line
- dependencies
- unknowns
- cut/deferred scope

Every slice must end in visible, demoable UI.

### 6. Build

Use only after a slice has been selected.

Good outputs:
- implementation plan
- files likely affected
- verification target
- changed files mapped back to requirement, affordance, store, or slice IDs

Build only the selected slice unless the user explicitly expands scope.

### 7. Reflect

Use after implementation exists.

Good outputs:
- `planning/breadboard-reflection.md`
- synced implementation reality
- drift
- missing behavior
- accidental behavior
- planning updates
- implementation follow-ups

Do not critique the design until the breadboard has first been synced to reality.

## Default authority order

When artifacts disagree, use this order unless the user says otherwise:

1. latest explicit user instruction
2. selected slice or kickoff doc
3. selected breadboard
4. selected shaping direction
5. frame
6. raw notes and transcripts
7. rejected alternatives and brainstorming

## Context handoff

Before Build mode, use a compact context packet instead of loading the whole planning stack.

A good context packet includes:
- task
- source artifacts
- authority order
- sections to use first
- sections to ignore unless needed
- must-preserve constraints
- selected requirements
- relevant places, affordances, stores, and wiring
- current slice
- non-goals and exclusions
- verification target

See `docs/agent-context-feeding.md` and `feed-planning-context/SKILL.md` for the full protocol.

## Completion check

Before an agent says the work is done, it should verify:

- it stayed in the requested mode
- requirements are still separate from mechanisms
- rejected alternatives are still marked as rejected
- non-goals were preserved
- stable IDs were preserved
- planning artifacts were updated if implementation discoveries changed the plan
- implementation work maps back to requirement, affordance, store, or slice IDs when applicable
