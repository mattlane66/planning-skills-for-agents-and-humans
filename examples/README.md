# Examples

This folder contains end-to-end examples showing how to use the skills in this repo in realistic situations.

The goal is to make it obvious:
- what to start with
- which skill to use next
- what each output should look like
- when a skill is optional
- how the artifacts relate to one another

## Examples in this folder

### 1. Simple Grocery List

The `simple-grocery-list/` example is the simplest greenfield path.

It demonstrates:
- framing from messy notes
- shaping with two directions
- breadboarding a chosen shape
- post-implementation breadboard reflection
- optional kickoff handoff

Recommended reading order:
1. `simple-grocery-list/README.md`
2. `simple-grocery-list/00-source-notes.md`
3. `simple-grocery-list/01-frame.md`
4. `simple-grocery-list/02-shaping.md`
5. `simple-grocery-list/04-breadboard.md`
6. `simple-grocery-list/05-breadboard-reflection.md`
7. `simple-grocery-list/03-kickoff.md`

### 2. Brownfield Member Admin Search

The `brownfield-member-admin-search/` example shows how to shape a change against an existing system.

It demonstrates:
- `CURRENT` as the baseline
- shaping a change against existing behavior
- breadboarding existing and new affordances together
- a brownfield flow where the new mechanism must preserve the old system’s structure

Recommended reading order:
1. `brownfield-member-admin-search/README.md`
2. `brownfield-member-admin-search/00-current-system-notes.md`
3. `brownfield-member-admin-search/01-frame.md`
4. `brownfield-member-admin-search/02-shaping.md`
5. `brownfield-member-admin-search/03-breadboard.md`

### 3. Spike-Driven Time Window Filter

The `spike-driven-time-window-filter/` example shows how to use shaping when a promising direction still contains a real unknown.

It demonstrates:
- a flagged unknown (`⚠️`)
- a standalone spike file
- refining the chosen shape after the spike
- breadboarding the now-concrete shape

Recommended reading order:
1. `spike-driven-time-window-filter/README.md`
2. `spike-driven-time-window-filter/00-source-notes.md`
3. `spike-driven-time-window-filter/01-frame.md`
4. `spike-driven-time-window-filter/02-shaping-initial.md`
5. `spike-driven-time-window-filter/03-spike-natural-language-window.md`
6. `spike-driven-time-window-filter/04-shaping-after-spike.md`
7. `spike-driven-time-window-filter/05-breadboard.md`

## Suggested workflow

Use the examples as patterns, not templates to copy blindly.

1. Start with raw notes, requests, or transcripts.
2. Create a frame.
3. Shape the problem and compare options.
4. Choose a direction.
5. Breadboard the chosen shape.
6. After implementation exists, use reflection to compare the breadboard to reality.
7. Optionally create a kickoff doc if handing off to another builder.
