---
name: interface-contracts
description: Turn selected breadboard wires or slices into plain-language contracts for boundary-crossing data exchanges.
planning: true
shaping: true
---

# Plain-Language Interface Contracts

Use this skill when a selected slice or breadboard wire crosses a meaningful boundary and the agent needs exact data-shape clarity before implementation.

This skill prepares planning context only. It does not write production schemas or code unless the user explicitly asks to move into implementation preparation.

## Goal

Produce a plain-language contract that makes boundary-crossing data exchanges explicit enough for an implementation agent to build and test without inventing field names, nullability, enum values, or error cases.

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

## Output format

```md
# [Project] — Plain-Language Interface Contracts

## Source references
- Breadboard artifact:
- Selected slice:
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
```

## Contract table shorthand

When the contract is still embedded in a breadboard, use this table:

| ID | Trigger / Wire | From | To | Request / Input Shape | Response / Output Shape | Branches / Errors | Open Decisions |
|---|---|---|---|---|---|---|---|
| C1 | U1 -> N1 | UI | API | user_id: string; items: array | order_id: string; status: pending | missing item, invalid quantity | Should promo codes be nullable or omitted? |

## What to specify

### Boundary

Name the two parts exchanging data.

Examples:

- `U1 Submit order -> N2 Create order endpoint`
- `N3 Import file -> N4 Normalize rows`
- `Agent action -> GitHub issue creation tool`

### Input shape

Include:

- field names
- types when known
- required vs optional
- arrays or nested objects
- IDs and references
- nullable fields
- units, such as cents instead of dollars

### Output shape

Include:

- success response
- user-visible result
- state written or updated
- fields the next slice depends on

### Branches and errors

Name the non-happy paths the implementation must handle.

Examples:

- missing required field
- invalid enum value
- duplicate record
- permission denied
- unavailable external service
- partial import success

### Open decisions

List decisions that should not be invented by the implementation agent.

Examples:

- Should a missing optional value be omitted or sent as `null`?
- Is status limited to `pending`, `confirmed`, and `failed`?
- Are prices represented in cents or decimal dollars?
- Who owns the canonical ID: client, server, imported system, or database?

## Formalization prompt

Use this only when moving from planning into implementation preparation:

```text
Turn this plain-language interface contract into the smallest useful formal contract for the selected slice.

Use OpenAPI 3.1, JSON Schema, TypeScript types, validators, or tests only if useful for the current implementation step.

Before writing code, report:
1. decisions that are fully specified
2. decisions that are missing
3. assumptions you would otherwise have to invent
4. tests that would prove the implementation satisfies the contract

Do not invent missing field names, nullability, enum values, or error cases. Flag them.
```

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

## Do not

- create full OpenAPI, JSON Schema, database schema, framework code, or production contract files during planning
- infer missing field names when the source artifacts do not specify them
- invent enum values or nullability rules
- expand the contract beyond the selected slice
- treat the contract as more authoritative than the user's latest instruction or selected slice
