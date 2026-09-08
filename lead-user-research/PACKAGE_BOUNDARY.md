# Lead User Research package boundary

This document defines ownership between Lead User Research and the product-planning workflow, including the migration path for eventually extracting Lead User Research into a separately versioned package.

## Boundary decision

Lead User Research is an **optional upstream evidence package**. It owns the method for discovering and interpreting future-facing needs. The planning system owns product-planning authority from accepted planning inputs through implementation.

The boundary is:

```text
Lead User Research
  evidence + findings + needs + principles
  + optional research-local concept probes
        |
        | explicit human-accepted handoff
        v
Planning workflow
  framing / shaping / appetite / selection
  -> selected-design behavior
  -> active implementation scope
```

Research may make design implications concrete enough to learn from them. It does not, by itself, create product-planning truth or build scope.

## What Lead User Research owns

Until extraction, `lead-user-research/` in this repository remains the canonical source for:

- the Lead User research methodology and protocol;
- phase prompts A-H;
- research brief, persisted study state, and research schemas;
- research controller and deterministic validators;
- evidence freeze, sufficiency, lineage, coverage, and interpretation rules;
- research-local Phase F concept probing;
- Decision Brief rendering and Lead User-specific assurance tests;
- portable/project onboarding for environments without a shell.

`skills/lead-user-research/` is a packaged mirror, not a second source of truth.

## What the planning package owns

The planning system owns:

- `planning-router`, `framing-doc`, `shaping`, and downstream planning skills;
- accepted project requirements and Appetite;
- product shape selection and selected-design reconciliation;
- selected slices / Dumplink task groups and active implementation scope;
- the repository-wide authority order and human promotion gates;
- the integration contract that converts accepted research implications into planning inputs.

No Lead User state outranks an accepted planning artifact merely because it is more detailed or was created later.

## Phase F authority

Phase F may use Fit Check to make a supported need concrete enough for research learning. Its structured state is **research-local**:

- `SF## status = ACCEPTED` means a human accepted that `x -> f() -> y` frame as a defensible **research concept-evaluation frame**. It is not an accepted `framing-doc` or accepted planning frame.
- `R##` rows in `fit_criteria.json` are **research-local fit criteria**. They must be cited downstream as namespaced research refs such as `LUR:<workspace>:R1`; they do not automatically claim or replace project `R##` identity.
- `M## selection_status = SELECTED` means a human selected or preferred that mechanism **within the research study** for the decision the study is informing. It is not a selected project shape, selected-design breadboard, selected slice, or build authorization.

These legacy field names remain valid for compatibility with existing v1.x study workspaces. Their planning authority is defined here, not inferred from words such as `ACCEPTED` or `SELECTED` inside the research schema.

## Handoff without repeated planning work

The accepted research-to-planning handoff is the only promotion boundary. It remains evidence input, not product truth.

Use the smallest downstream move:

- **No Phase F:** if the study stops at evidence/interpretation, an accepted handoff normally routes to `framing-doc`.
- **Phase F present:** if Phase F already produced a defensible transformation frame, research-local fit criteria, or candidate mechanisms, an accepted handoff normally routes directly to `shaping` in collaborative mode. Import those records as **Working** planning material with their research provenance intact rather than reconstructing them from scratch.

Downstream planning must not ask the human to repeat a Phase F frame or mechanism decision merely because the package boundary was crossed. Revisit the decision only when a planning promotion gate is still unmet or a consequential planning input differs—for example, accepted project requirements, Appetite/cut line, project boundary, material evidence, or viable alternatives.

Research-local human provenance can therefore be reused as decision evidence, but it cannot bypass the planning gates that were not actually satisfied in Phase F.

## Requirement lineage across the boundary

Research-local fit criteria and project requirements live in different namespaces.

When importing Phase F criteria:

1. preserve the research ref, for example `LUR:<workspace>:R3`;
2. map it to an existing project requirement when the meaning is materially the same, preserving that project requirement's existing ID;
3. otherwise create a new **Working** project requirement with a new project-local `R##` and record the research ref as provenance;
4. do not mint a new project ID merely because a Working requirement later becomes Accepted;
5. if meaning changes materially, supersede or split explicitly rather than silently reusing an ID.

This keeps the planning lifecycle's stable requirement identity without pretending a research registry already owns the project's ID namespace.

## Separate-package migration plan

Lead User Research should become separately versioned only after the integration contract is stable enough that extraction is mechanical rather than a redesign.

### Stage 1 — freeze the integration contract

In this repository:

- keep `lead-user-research/` canonical and its packaged mirror byte-aligned;
- make the authority rules above explicit in Phase F and handoff instructions;
- regression-test the package boundary and route selection;
- treat the handoff as `research-to-planning-v1` conceptually, even while the template remains Markdown.

### Stage 2 — create the standalone package

The standalone package becomes canonical owner of:

- Lead User methodology, prompts, state contract, scripts, validators, renderers, and Lead User-specific assurance;
- its own semantic version, release artifacts, checksums, and runtime-install tests.

The first extracted release must preserve the existing v1.x workspace schema or ship an explicit migration tool; extraction must not make historical evidence appear newly verified.

### Stage 3 — invert the dependency

After standalone release validation:

- this planning repository references/pins the standalone Lead User package as an optional upstream integration;
- this repository keeps only the planning-side handoff contract, routing rules, compatibility documentation, and any intentionally vendored adapter;
- do not maintain two independently editable canonical copies.

### Stage 4 — remove the transitional bundle

Remove the bundled Lead User implementation from this repository only after:

- Claude/Codex/Gemini install/use checks pass against the standalone package;
- the planning handoff tests pass against a pinned released version;
- existing users have a documented migration path;
- one release cycle has made the ownership change visible.

## Non-goals

This boundary decision does not:

- extract the package in this change;
- change historical study records;
- make Phase F mandatory;
- turn Lead User evidence into market validation;
- grant research-local concepts implementation authority;
- require a user to repeat decisions whose relevant planning prerequisites are already satisfied and whose provenance is preserved.
