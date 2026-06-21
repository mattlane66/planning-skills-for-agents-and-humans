# Plain-Language Interface Contracts

A plain-language interface contract describes what crosses a boundary before code is written.

It is not the implementation. It is the agreement between parts of the system: what one side sends, what the other side returns, what can fail, and which decisions are still unresolved.

Use this after a breadboard or selected slice when the work depends on data moving across a meaningful boundary.

## Where this fits

```text
Framing
  -> Shaping
  -> Breadboard
  -> Slices
  -> Plain-language interface contract, when boundary detail matters
  -> Feed planning context
  -> Spec Kit / Build agent
```

The breadboard says what exists.

The slice says what is being built now.

The interface contract says what must move across the boundary.

The context packet tells the agent what to preserve while building.

## Use this when

Use an interface contract when a wire crosses a boundary where guessing would cause rework:

- UI -> backend
- frontend -> API
- service -> store
- agent -> tool
- import -> parser
- parser -> normalized object
- canvas object -> markdown artifact
- MCP server -> client
- app -> external integration

Do not create a contract for every internal helper or tiny function. Use it where the data shape is part of the product behavior or where multiple agents, layers, or systems need to stay in sync.

## What to specify

### 1. Boundary

Name the two parts exchanging data.

Examples:

- `U1 Submit order -> N2 Create order endpoint`
- `N3 Import file -> N4 Normalize rows`
- `Agent action -> GitHub issue creation tool`

### 2. Input shape

Write what must be sent in plain language.

Include:

- field names
- types when known
- required vs optional
- arrays or nested objects
- IDs and references
- nullable fields
- units, such as cents instead of dollars

### 3. Output shape

Write what comes back.

Include:

- success response
- user-visible result
- state written or updated
- fields the next slice depends on

### 4. Branches and errors

Name the non-happy paths the implementation must handle.

Examples:

- missing required field
- invalid enum value
- duplicate record
- permission denied
- unavailable external service
- partial import success

### 5. Open decisions

List decisions that should not be invented by the implementation agent.

Examples:

- Should a missing optional value be omitted or sent as `null`?
- Is status limited to `pending`, `confirmed`, and `failed`?
- Are prices represented in cents or decimal dollars?
- Who owns the canonical ID: client, server, imported system, or database?

## Contract candidate table

Use this inside a breadboard or as the starting point for a separate contract artifact.

| ID | Trigger / Wire | From | To | Request / Input Shape | Response / Output Shape | Branches / Errors | Open Decisions |
|---|---|---|---|---|---|---|---|
| C1 | U1 -> N1 | UI | API | user_id: string; items: array of product_id + quantity; promo_code optional | order_id: string; status: pending; total_cents: integer | missing item, invalid quantity, invalid promo code | Should promo_code be nullable or omitted? |

## Example

### Plain-language version

```text
When creating an order, the UI sends:
- user_id: string, required
- items: array, required
  - product_id: string, required
  - quantity: integer, required
- promo_code: string, optional

When it succeeds, the API returns:
- order_id: string
- status: pending
- total_cents: integer
- estimated_delivery: ISO date or null

Branches:
- missing user_id -> validation error
- empty items -> validation error
- invalid quantity -> validation error
- invalid promo_code -> promo error, order not created

Open decisions:
- Should promo_code be omitted when absent, or sent as null?
- Should estimated_delivery be nullable at creation?
```

### Agent formalization prompt

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

## Planning-mode rule

During planning, keep the contract in plain language.

Do not create full OpenAPI, JSON Schema, database schema, framework code, or production contract files unless the user explicitly asks or the selected slice has moved into implementation preparation.

During build preparation, a coding agent can turn the plain-language contract into OpenAPI, JSON Schema, TypeScript types, validators, tests, API clients, fixtures, or mocks.

## Agent rules

When an agent receives an interface contract, it should:

1. preserve field names exactly unless asked to rename them
2. preserve required vs optional distinctions
3. preserve enum values and nullability
4. generate validation and tests from the contract where useful
5. flag missing decisions before coding
6. avoid expanding the contract beyond the selected slice
7. propose a planning update if implementation reality contradicts the contract

## Quality check

A good plain-language interface contract should let a builder answer:

- What boundary is being crossed?
- What exactly goes in?
- What exactly comes back?
- What can fail?
- Which fields, types, IDs, units, enum values, and nullability rules are decided?
- Which decisions remain open?
- What tests would prove the contract was satisfied?
