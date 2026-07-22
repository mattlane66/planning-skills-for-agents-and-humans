---
name: interface-contracts
description: Define plain-language inputs, outputs, branches, errors, and open decisions when a selected slice crosses a meaningful data, service, or system boundary.
---

# Plain-Language Interface Contracts

Use this skill when a selected slice or breadboard wire crosses a meaningful boundary and the agent needs exact data-shape clarity before implementation.

This skill prepares planning context only. It does not write production schemas or code unless the user explicitly asks to move into implementation preparation.

## Goal

Produce a plain-language contract that makes boundary-crossing data exchanges explicit enough for an implementation agent to build and test without inventing field names, nullability, enum values, or error cases.

## Relationship to executable breadboards

An interface contract is boundary detail.

An executable breadboard is the build handoff for a selected slice: structure plus interface contracts, fixtures, example runs, expected outputs, edge cases, and tests.

Use this skill separately when boundary detail is complex enough to deserve its own artifact. Otherwise, the contract table can live directly inside an executable breadboard.

## Use this when

Use this after a breadboard or selected slice when the work depends on data moving across a meaningful boundary:

- UI -> backend
- frontend -> API
- service -> store
- agent -> tool
- import -> parser
- parser -> normalized object
- canvas object -> markdown artifact
- MCP server -> client
- app -> external integration

Do not create contracts for every internal helper or tiny function. Use this where the exchange is part of the product behavior or where multiple agents, layers, or systems need to stay aligned.

## Inputs

Use whichever inputs are available:

- selected breadboard
- selected slice
- executable breadboard, if already present
- wires from UI affordances to non-UI affordances
- stores and state affected by the exchange
- product-relevant branches
- implementation constraints
- external API or tool behavior, if known

## Default behavior

1. Identify boundary-crossing wires.
2. Select only the boundaries that matter for the current slice.
3. Assign stable contract IDs such as `C1`, `C2`, or `CONTRACT-01`.
4. For each contract, name the trigger or wire.
5. Name the source and destination.
6. Write the input shape in plain language.
7. Write the output shape in plain language.
8. Name branches and errors.
9. Flag open decisions instead of inventing them.
10. Add a verification target.
11. Note whether the contract should be embedded in the executable breadboard or split out as a separate artifact.

## Output format

# [Project] — Plain-Language Interface Contracts

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

## Contract table shorthand

When the contract is still embedded in a breadboard or executable breadboard, use this table:

| ID | Trigger / Wire | From | To | Request / Input Shape | Response / Output Shape | Branches / Errors | Open Decisions |
|---|---|---|---|---|---|---|---|
| C1 | U1 -> N1 | UI | API | user_id: string; items: array | order_id: string; status: pending | missing item, invalid quantity | Should promo codes be nullable or omitted? |

## What to specify

### Boundary

Name the two parts exchanging data.

### Input shape

Include field names, types when known, required vs optional, arrays or nested objects, IDs and references, nullable fields, and units such as cents instead of dollars.

### Output shape

Include the success response, user-visible result, state written or updated, and fields the next slice depends on.

### Branches and errors

Name the non-happy paths the implementation must handle.

Examples: missing required field, invalid enum value, duplicate record, permission denied, unavailable external service, or partial import success.

### Open decisions

List decisions that should not be invented by the implementation agent.

Examples: whether missing optional values are omitted or null, allowed status values, money units, or who owns the canonical ID.

## Formalization prompt

Use this only when moving from planning into implementation preparation:

Turn this plain-language interface contract into the smallest useful formal contract for the selected slice. Use OpenAPI 3.1, JSON Schema, TypeScript types, validators, or tests only if useful for the current implementation step. Before writing code, report decisions that are fully specified, decisions that are missing, assumptions you would otherwise have to invent, and tests that would prove the implementation satisfies the contract. Do not invent missing field names, nullability, enum values, or error cases. Flag them.

## Quality checks

- Each contract names a meaningful boundary.
- Inputs and outputs are written in plain language.
- Required vs optional fields are clear where known.
- Nullable fields are explicit where known.
- Enum values are explicit where known.
- Branches and errors are named.
- Open decisions are flagged instead of invented.
- Verification targets are concrete.
- The contract stays within the selected slice.
- The contract can be embedded inside an executable breadboard or referenced by one.

## Do not

- create full OpenAPI, JSON Schema, database schema, framework code, or production contract files during planning
- infer missing field names when the source artifacts do not specify them
- invent enum values or nullability rules
- expand the contract beyond the selected slice
- treat the contract as more authoritative than the user's latest instruction, selected slice, or executable breadboard
