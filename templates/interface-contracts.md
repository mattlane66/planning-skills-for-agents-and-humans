---
planning: true
shaping: true
artifact_type: interface-contracts
status: draft
source_of_truth: true
feeds:
  - executable-breadboard
  - context-packet
  - implementation
---

# [Project] — Plain-Language Interface Contracts

# Context Card

## Use this when
A selected slice crosses meaningful boundaries and the builder needs exact input, output, branch, and error details.

## Relationship to executable breadboards

An interface contract is boundary detail.

An executable breadboard is the full build handoff for a selected slice: structure plus interface contracts, fixtures, example runs, expected outputs, edge cases, and tests.

Use this artifact separately when boundary detail is complex. Otherwise, include the same contract table directly inside the executable breadboard.

## Must preserve
- contract IDs
- boundary names
- field names
- required vs optional distinctions
- enum values
- nullability
- error cases
- open decisions

## Ignore unless asked
- production schemas
- framework-specific implementation details
- full OpenAPI / JSON Schema output

## Source references
- Breadboard artifact:
- Selected slice:
- Executable breadboard, if present:
- Related shaping artifact:

## Contract summary

| ID | Boundary | Why this contract matters | Related breadboard IDs | Related slice |
|---|---|---|---|---|
| C1 | ... | ... | U1 -> N1 | V1 |

## Contracts

### C1 — [Boundary name]

**Trigger / wire**
- ...

**From**
- ...

**To**
- ...

**Input shape**
- ...

**Output shape**
- ...

**Branches / errors**
- ...

**Open decisions**
- ...

**Verification target**
- ...

## Formalization prompt, if moving to implementation

```text
Turn these plain-language interface contracts into the smallest useful formal contract for the selected slice.

Use OpenAPI 3.1, JSON Schema, TypeScript types, validators, or tests only if useful for the current implementation step.

Before writing code, report:
1. decisions that are fully specified
2. decisions that are missing
3. assumptions you would otherwise have to invent
4. tests that would prove the implementation satisfies the contract

Do not invent missing field names, nullability, enum values, or error cases. Flag them.
```

## Self-check
- [ ] Each contract names a meaningful boundary.
- [ ] Inputs and outputs are written in plain language.
- [ ] Required vs optional fields are clear where known.
- [ ] Nullable fields are explicit where known.
- [ ] Enum values are explicit where known.
- [ ] Branches and errors are named.
- [ ] Open decisions are flagged instead of invented.
- [ ] Verification targets are concrete.
- [ ] The contract can be embedded inside an executable breadboard or referenced by one.
