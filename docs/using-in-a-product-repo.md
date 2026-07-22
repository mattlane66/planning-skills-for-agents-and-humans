# Using Planning Skills in a product repository

Use this guide after installing or referencing the Planning Skills and before starting real project work.

## The basic setup

1. Install the plugin or make the canonical skills available to your agent.
2. Open the repository where the product is actually being designed and built.
3. Run framing, shaping, sketch reconciliation, breadboarding, handoff, and drift checks from that product repository.
4. Save project-specific planning artifacts beside the code they govern, normally under `planning/`.

The Planning Skills repository is the reusable method. Your product repository is where the method is applied.

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
  frame.md
  shaping.md
  appetite.md          # optional when appetite is recorded separately
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

This is a default convention, not a required schema. Small projects may need only a frame, shaping document, breadboard, selected slice, and context packet.

Keep one clearly active artifact at each level unless the project intentionally versions them. Preserve stable IDs across artifacts. Do not delete rejected alternatives merely to make the active plan look cleaner.

## A practical first pass

From the product repository, give the agent the available evidence and ask it to choose the current planning mode:

```text
Use the Planning Skills workflow in this product repository.
First decide whether this work needs framing, shaping, sketch reconciliation, or breadboarding.
Do not implement until a direction and demoable slice are selected.
Set or confirm the appetite and cut line before selecting a shape.

Source material:
[notes, transcript, screenshots, links, or existing files]
```

Save the result under `planning/`, review it at the relevant human gate, and continue only after the decision is explicit.

## When a sketch or prototype already exists

Use the `sketch-reconciliation` skill. Treat the visual as evidence and a design proposal, not as an automatic specification.

Reconcile the visual with the active requirements, selected shape, breadboard, and slices before implementation. The reconciliation should identify:

- what is already covered
- what the visual clarifies
- what is missing from the planning artifacts
- what conflicts with the selected direction
- what remains ambiguous

Resolve changes through the reconciliation human gate, update every affected authoritative artifact as one ripple, and then revise the visual or implementation direction.

## Choose the handoff artifact by the question

| Question | Artifact |
|---|---|
| What is the shaped product territory builders need to understand? | Kickoff document |
| Exactly how should this selected slice behave and be verified? | Executable breadboard |
| How should work inside the selected slice be grouped, sequenced, de-risked, and cut to fit the appetite? | Dumplink plan |
| What exact subset should this implementation agent receive now? | Context packet |

A project may use more than one. Their jobs are different:

- the kickoff document is a durable human reference, not a task sequence
- the executable breadboard is the behavioral and test contract for a selected slice
- Dumplink organizes vertical task groups, dependencies, risk, sequence, and cuts inside the selected slice; pre-slice groups are candidates only
- the context packet packages only the material needed for the active build pass

## Typical handoff sequence

```text
selected shape
  -> accepted breadboard
  -> selected slice
  -> optional kickoff reference
  -> executable breadboard and/or Dumplink when needed
  -> compact context packet
  -> implementation with drift checks
```

Do not create every artifact automatically. Use the smallest set that removes consequential ambiguity.

## Sources of truth

- tables remain authoritative over Mermaid or canvas projections
- the accepted breadboard remains authoritative over a derived statechart
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
