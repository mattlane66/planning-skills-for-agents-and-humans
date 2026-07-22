# [Project] — Dumplink Plan

## Project boundary

- Mode: `standard` or `pre-slice-exploration`
- Selected shape:
- Appetite:
- Non-goals:
- Selected slice:
- Slice exclusions:

The selected slice is required for a committed build sequence or agent handoff. All task groups, dependencies, cuts, and sequence stay within it. If it is absent, label every group as a candidate and stop before the Build sequence, Acceptance checks, and Agent handoff packet sections become commitments.

## Task dump

| ID | Task | Type | Known / unknown | Notes |
| --- | --- | --- | --- | --- |

## Task groups

| ID | Name | Included tasks | Judgeable behavior produced | Risk state | Cuttable? | Notes |
| --- | --- | --- | --- | --- | --- | --- |

## Dependency map

| From | To | Why this dependency exists | Risk if delayed |
| --- | --- | --- | --- |

## Build sequence

| Order | Task group | Why now | Demo / checkpoint | Exit condition |
| --- | --- | --- | --- | --- |

## Scope cuts

| Cut option | Remove or defer | Preserved behavior | Cost of cutting | Later decision |
| --- | --- | --- | --- | --- |

## Acceptance checks

| Check ID | Proves | How to verify |
| --- | --- | --- |

## Agent handoff packet

- Active slice:
- Source artifacts:
- Must preserve:
- Do not build:
- Task group to implement:
- Relevant tasks:
- Known unknowns:
- Acceptance check:
- Stop condition:
