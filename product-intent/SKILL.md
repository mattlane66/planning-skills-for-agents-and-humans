---
name: product-intent
description: Compile accepted planning into a machine-readable product intent model, bootstrap intent for an existing codebase, bind intent to implementation, and detect drift without letting code silently redefine the product.
license: MIT
---

# Product Intent

Use this skill when a team needs a durable answer to:

> What is this product supposed to do, what must remain true, and did this change alter that intent?

This is not another planning stage. It is the runtime contract produced from accepted planning.

## Core rule

**Intent and implementation are different information.**

Accepted planning artifacts own human decisions. `product-intent.json` is a deterministic compiled projection for agents and CI. Do not hand-edit the compiled model.

## Modes

### 1. Compile accepted intent

Use when accepted shaping and selected-design artifacts already exist.

1. Read the accepted frame, shaping artifact, selected-design breadboard, selected slice, contracts, and executable breadboard when present.
2. Require the normal authority and promotion gates.
3. Record explicit product invariants in the accepted selected-design breadboard when a behavior must survive future implementation changes.
4. Record implementation bindings separately in `planning/implementation-bindings.json`; bindings say where intent is currently realized, not how the code must be written.
5. Compile with:

```bash
python3 scripts/product_intent.py \
  --planning-dir planning \
  --output planning/product-intent.json
```

6. Never patch the generated JSON to make a check pass. Change the owning accepted artifact or binding, then recompile.

### 2. Bootstrap an existing codebase

Use when code exists but accepted product intent does not.

The goal is to create a reviewable proposal, not pretend code reveals intent.

1. Inspect user-visible flows, tests, routes, persistent state, public interfaces, support docs, and recent implementation evidence.
2. Build a `current-state` breadboard from what can be observed.
3. Separate:
   - **VERIFIED CURRENT BEHAVIOR** — directly supported by code/tests/runtime evidence.
   - **INFERRED INTENT** — behavior that appears deliberate but has not been accepted by a human.
   - **UNKNOWN** — decisions the code cannot explain.
4. Do not turn current behavior into normative intent automatically.
5. Ask a human to accept, reject, or revise the requirements, selected behavior, invariants, and important decision rationale.
6. Only after acceptance, promote to selected-design intent and compile the model.
7. Preserve rejected alternatives and reasons when known. Never reconstruct a rationale you cannot support.

A bootstrap that has not passed the human gate is descriptive evidence, not product truth.

### 3. Bind intent to implementation

Create `planning/implementation-bindings.json` with stable `BIND#` records.

Each binding must name:
- one or more intent IDs
- the file paths or globs where that intent is currently realized
- important symbols when useful
- tests that verify it when available

Bindings are allowed to move as code is refactored. The intent IDs should remain stable unless the product decision changes.

### 4. Check drift

For a code diff:

```bash
python3 scripts/check_intent_drift.py \
  --intent planning/product-intent.json \
  --base-ref origin/main \
  --head-ref HEAD
```

Interpretation:
- `PASS` — no bound product intent was touched by the supplied diff.
- `REVIEW_REQUIRED` — bound intent may be affected, or product code changed without a binding.
- `VIOLATION` — a supplied verification result says an affected invariant failed.

A static diff can identify risk. It cannot prove that product semantics are preserved. Use executable breadboards, acceptance tests, or runtime checks for that.

### 5. Change intent intentionally

When the product should change:

1. Name the affected accepted IDs.
2. Propose the intent delta before changing the implementation.
3. Re-run fit/reverse-fit where the changed decision affects requirements or the selected mechanism.
4. Record the new decision, rationale, rejected alternatives, and `Reopen when` condition.
5. Supersede old IDs only when meaning materially changes; otherwise preserve identity.
6. Update affected invariants and bindings.
7. Recompile `product-intent.json`.
8. Then implement against the new intent.

Do not let a code diff silently become a product decision.

## Product invariants

Use an `INV#` only for behavior or constraints that future implementers could plausibly remove while still producing code that looks locally reasonable.

Good invariant:
- `INV1 — Editing a draft must not mutate the persisted profile before Save.`

Weak invariant:
- `INV2 — Use React state for the draft.`

The first preserves product behavior. The second freezes implementation.

Each invariant should name:
- the statement
- `must` or `should`
- the product IDs it protects
- what evidence would justify reopening it
- how it can be verified

## Generated projections

The compiled model may feed:
- agent context
- acceptance and regression scenarios
- QA plans
- support documentation
- product documentation
- diagrams
- release-change summaries
- sales or onboarding explanations

These are projections. They never become competing sources of truth.

## Stop conditions

Stop and return to planning when:
- code contradicts accepted intent
- the model exposes an unresolved product decision
- an invariant cannot be verified
- a binding points to implementation that no longer exists
- a requested change would alter accepted intent without an explicit decision
