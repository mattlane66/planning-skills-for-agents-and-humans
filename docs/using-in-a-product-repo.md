# Using Planning Skills in a product repository

Use this guide after installing or referencing the Planning Skills and before starting real project work.

## The basic setup

1. Install the plugin or make the canonical skills available to your agent.
2. Open the repository where the product is actually being designed and built.
3. Start from the material you really have: requirements, a proposed solution, evidence/prototype, or a focused uncertainty.
4. Use framing, shaping, sketch reconciliation, breadboarding, handoff, and drift checks only when their current question makes them useful.
5. Save project-specific planning artifacts beside the code they govern, normally under `planning/`.

The Planning Skills repository is the reusable method. Your product repository is where the method is applied.

## Default shaping profile

For interactive human-guided work, use **collaborative shaping**:

> **Exploration is fluid. Commitment is gated.**

Requirements (R), shapes (S), Working Appetite, fit checks, focused spikes, sketches, and candidate breadboards may inform one another in any useful order while they remain Working.

Use the **gated/orchestrated profile** only when the user, team policy, CI harness, or multi-agent workflow explicitly requires deterministic prerequisites.

Both profiles preserve the same hard promotion gates before shape selection, selected-design authority, slice selection, and build.

## Do not overwrite project instructions

If the product repository already has `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Cursor rules, or other local instructions, preserve them.

Prefer one of these approaches:

- use the installed Planning Skills plugin while working in the product repository
- point the agent explicitly at the relevant canonical `SKILL.md`
- selectively merge compatible planning rules into the product's existing instruction surface

Do not copy this repository's root `AGENTS.md` over a product repository's existing file. Product-specific build, test, security, and architecture rules still govern that codebase.

## Recommended planning directory

```text
planning/
  wayfinding/          # optional maps and tickets for multi-session planning
  frame.md
  shaping.md
  appetite.md          # optional when Appetite is recorded separately
  candidate-A-breadboard.md
  breadboard.md
  sketch-reconciliation.md
  statechart.md
  slices.md
  interface-contracts.md
  executable-breadboard.md
  dumplink.md
  kickoff.md
  context-packet.md
  spikes/
  runs/
```

This is a default convention, not a required schema. Small projects may need only a shaping document, accepted behavior boundary, selected slice, and context packet. A separate frame is useful when the actual problem boundary is unclear, not merely because it appears first in a diagram.

Keep one clearly active artifact at each accepted authority level unless the project intentionally versions them. Preserve stable IDs across artifacts. Do not delete rejected alternatives merely to make the active plan look cleaner.

## A practical first pass

From the product repository, give the agent the material that already exists:

```text
Use the Planning Skills workflow in collaborative mode in this product repository.
Start from whatever is already most concrete: requirements, a proposed solution, a prototype, current-system evidence, or a focused unknown.
Choose the smallest planning move that resolves the current uncertainty.
Move among R, S, fit checks, focused spikes, sketches, and candidate breadboards as useful while material remains Working.
Keep Working material separate from Accepted intent.
Do not select a shape until requirements and Appetite are Accepted and the comparison is decision-ready.
Do not implement until selected-design behavior or an equally clear accepted boundary and a demoable slice are explicitly selected.

Source material:
[notes, solution idea, transcript, screenshots, prototype, links, or existing files]
```

If you need stricter automation, switch explicitly:

```text
Use the gated/orchestrated profile from .agent-orchestration.yaml and stop at every human promotion gate.
```

## When a solution already exists in someone's head

Do not force the person to rewrite the idea as a complete problem statement first.

Use `shaping` in S-first collaborative mode:

1. capture the proposed solution as candidate Shape A
2. extract the provisional requirements it appears to serve
3. separate needs from mechanisms
4. run Working fit/reverse-fit when useful
5. spike or candidate-breadboard only the consequential unknowns
6. revise Working R and S as evidence appears
7. accept R and Appetite before final selection

A solution-first entry point is not an automatic selection.

## When a sketch or prototype already exists

If the visual is still exploratory, treat it as candidate evidence. Use shaping to extract Working R/S or candidate breadboarding to understand behavior.

Use `sketch-reconciliation` when a visual may **change already accepted planning**. Then identify:

- what is already covered
- what the visual clarifies
- what is missing from accepted artifacts
- what conflicts with the selected direction
- what remains ambiguous

Resolve accepted changes through the reconciliation human gate, update every affected authoritative artifact as one ripple, and then revise the visual or implementation direction.

A polished prototype never becomes selected intent merely because it is concrete.

## Choose the handoff artifact by the question

| Question | Artifact |
|---|---|
| Which dependent planning questions remain open across sessions, and what is currently unblocked? | Wayfinding map and tickets |
| What is the shaped product territory builders need to understand? | Kickoff document |
| Exactly how should this selected slice behave and be verified? | Executable breadboard |
| How should this selected project be divided into vertical implementation slices, sequenced, de-risked, and cut to fit the Appetite? | Dumplink plan |
| What exact subset should this implementation agent receive now? | Context packet |

A project may use more than one. Their jobs are different:

- the kickoff document is a durable human reference, not a task sequence
- the executable breadboard is the behavioral and test contract for a selected slice
- Dumplink turns the selected project into vertical task groups with dependencies, risk, sequence, and cuts; a human-selected group becomes the active implementation slice
- the context packet packages only accepted material needed for the active build pass

## Typical handoff sequence after selection

```text
accepted R + Appetite
  -> explicit human-selected shape
  -> reconciled accepted selected-design breadboard
  -> selected project boundary
  -> optional Dumplink task groups
  -> human-selected active task group or other demoable slice
  -> optional kickoff reference
  -> executable breadboard and contracts when needed
  -> compact context packet
  -> implementation with drift checks
```

Do not create every artifact automatically. Use the smallest set that removes consequential ambiguity.

## Sources of truth

- Working shaping material is editable exploratory material, not build scope
- Accepted R/Appetite/selection outrank exploratory alternatives
- tables remain authoritative over Mermaid or canvas projections within their artifact authority
- candidate breadboards remain evidence until reconciled after explicit selection
- the accepted selected-design breadboard remains authoritative over a derived statechart
- a sketch reconciliation record documents evidence and accepted deltas; it does not outrank the artifacts it updates
- run logs record what happened but do not replace product decisions
- the user's latest explicit instruction remains highest authority
- when code reality invalidates the plan, surface drift and decide which truth changes

## If you are contributing to Planning Skills itself

The top-level skill folders in this repository are canonical. Do not hand-edit generated copies under `skills/`. After changing a canonical skill, run:

```bash
bash scripts/sync-packaged-skills.sh
bash scripts/check-repo-health.sh
```
