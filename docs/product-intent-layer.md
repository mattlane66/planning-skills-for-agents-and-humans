# Product intent layer

Planning Skills can act as a product-intent layer for AI-built software.

The problem it solves is not simply whether code passes tests. It is whether a change accidentally alters a product decision that the team already made.

## Architecture

```text
evidence + human decisions
          ↓
accepted planning artifacts
          ↓ compile
 ProductIntentModel
          ↕
implementation bindings
          ↓
diff impact + verification
          ↓
PASS / REVIEW_REQUIRED / VIOLATION
```

The accepted planning artifacts remain the authoring source of truth. The generated `product-intent.json` is the canonical machine-readable contract consumed by agents and CI.

That distinction avoids a second hand-maintained specification that can drift.

## What the model contains

The v1 model contains:

- frame: problem, outcome, and operating model
- accepted requirements
- product decisions, including selected and rejected directions
- selected design: places, UI affordances, hidden behavior, stores, and behavior traces
- product invariants
- implementation bindings
- acceptance tests when an executable breadboard exists
- source provenance and authority

Stable IDs connect those layers.

## Decisions

A selected direction should record a `DEC#`, its rationale, rejected alternatives, and the condition under which the team would reopen the decision.

This is what prevents a future agent from rediscovering an apparently simpler rejected solution and treating it as an improvement.

## Product invariants

An invariant is a behavior or constraint that must survive implementation changes.

Add invariants to the accepted selected-design breadboard:

```markdown
## Product invariants — selected-design mode

| ID | Invariant | Severity | Protects | Reopen when | Verification |
|---|---|---|---|---|---|
| INV1 | Editing a draft never mutates persisted data before Save. | must | R3, U7, S4, N8 | Product intentionally moves to autosave. | RUN2 / browser acceptance test |
```

Do not use invariants to freeze framework or code structure.

## Implementation bindings

Bindings answer: **where is this intent currently realized?**

They do not duplicate the behavior or dictate implementation.

Create `planning/implementation-bindings.json`:

```json
{
  "schema_version": 1,
  "bindings": [
    {
      "id": "BIND1",
      "intent_refs": ["R3", "U7", "S4", "N8", "INV1"],
      "paths": ["src/profile/EditForm.tsx", "src/profile/draftStore.ts"],
      "symbols": ["EditForm", "draftProfileStore", "saveProfile"],
      "tests": ["tests/profile-edit.spec.ts"],
      "notes": "Draft/persisted separation."
    }
  ]
}
```

Path globs are allowed.

## Compile

```bash
python3 scripts/product_intent.py \
  --planning-dir planning \
  --output planning/product-intent.json
```

To fail if the checked-in model is stale:

```bash
python3 scripts/product_intent.py \
  --planning-dir planning \
  --output planning/product-intent.json \
  --check
```

Never edit the generated file directly.

## Drift checks

```bash
python3 scripts/check_intent_drift.py \
  --intent planning/product-intent.json \
  --base-ref origin/main \
  --head-ref HEAD
```

The checker maps changed files through `BIND#` records to affected intent IDs and invariants.

It is intentionally conservative:

- touching bound intent requires review
- changing product code with no binding requires review
- a failing verification result can produce a definite violation
- static diff analysis never claims that semantics are preserved merely because syntax or tests look reasonable

Optional verification report:

```json
{
  "checks": [
    {"intent_ref": "INV1", "status": "pass"},
    {"intent_ref": "INV2", "status": "failed"}
  ]
}
```

Pass it with `--verification-report`.

## Existing products

Do not infer normative intent straight from code.

Bootstrap in two phases:

1. inspect the implementation and produce a `current-state` model with evidence
2. have a human explicitly accept or revise the intended requirements, behavior, decisions, and invariants

Only then promote the artifact to selected-design authority and compile the intent model.

The code can tell you what exists. It cannot reliably tell you why rejected alternatives were rejected or which accidental behavior should be preserved.

## Intent changes

A product change and an implementation change are different operations.

If accepted intent changes, update the owning artifact first, preserve or supersede stable IDs correctly, recompile the model, and then implement.

If only implementation changes, the accepted intent model should remain the same.

## Generated uses

The same model can drive agent context, executable QA, support docs, release notes, onboarding, diagrams, and other projections. Those outputs should always point back to the same stable intent IDs and remain derived.
