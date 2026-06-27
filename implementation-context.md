# Implementation Context

A canonical handoff packet for turning selected planning artifacts into production implementation work.

Use this after a direction and slice have been selected, and before asking a coding agent, Spec Kit workflow, or implementation harness to edit code. The goal is to preserve shaped intent while giving the builder enough concrete context to produce verifiable code.

This file is intentionally not a full PRD, full transcript, or full planning archive. It is the smallest implementation-facing packet that can support the next build move.

## When to use this

Use `implementation-context.md` when:

- a slice is selected for implementation
- the agent needs enough context to edit code safely
- planning artifacts exist, but should not all be pasted into context
- you want to hand shaped work to Spec Kit, Claude Code, Codex, Cursor, HumanLayer, or another coding workflow
- the team needs an authority order for resolving conflicts between code, tests, mocks, and planning docs

Do not use this to replace framing, shaping, breadboarding, or slicing. This is the bridge from selected planning work into implementation.

## How to use this

1. Copy this file into the target project, usually as `planning/implementation-context.md`.
2. Fill it for one selected slice only.
3. Keep source artifacts referenced by path instead of pasting every upstream document.
4. Feed this packet to the coding agent before implementation.
5. If implementation reality conflicts with the packet, use the drift protocol instead of silently changing intent.

## Template

```md
# Implementation Context

## Selected slice

### Slice ID
`SLICE-__`

### Build now
What is being implemented in this pass.

### Do not build now
Explicit exclusions and non-goals for this pass.

### Demo path
The smallest user-visible path that proves the slice works.

## Source artifacts

List only the source artifacts needed for this implementation pass.

- `planning/frame.md`
- `planning/shaping.md`
- `planning/breadboard.md`
- `planning/slices.md`
- `planning/kickoff.md`
- `planning/breadboard-reflection.md`

## Authority order

When artifacts disagree, use this order unless the user explicitly changes it.

1. User's latest explicit instruction
2. Existing production code and tests
3. This implementation context packet
4. Selected slice or kickoff doc
5. Selected breadboard
6. Selected shaping direction
7. Framing doc
8. Raw notes and transcripts
9. Rejected alternatives and brainstorming

## Must preserve

The implementation must preserve:

- selected requirement IDs: `REQ-__`
- selected place IDs: `P-__`
- selected affordance IDs: `AFF-__`
- selected store IDs: `STORE-__`
- selected slice ID: `SLICE-__`
- explicit non-goals
- visible demo path
- user-facing language or behavior that is already approved

## System objects

Name the domain objects, records, stores, services, external systems, or data structures this slice touches.

| ID | Object | Responsibility | Notes |
|---|---|---|---|
| `OBJ-01` |  |  |  |

## Affordances and system responses

Map each user/system action to the system response it must trigger.

| Affordance ID | Actor | Action | System response | Visible consequence |
|---|---|---|---|---|
| `AFF-01` | User |  |  |  |

## State rules

Define the states the implementation must handle.

| State | Expected behavior | Notes |
|---|---|---|
| Loading |  |  |
| Empty |  |  |
| Success |  |  |
| Error |  |  |
| Disabled |  |  |
| Permission denied |  |  |

## Data and API contracts

Define any required data shape, API payload, event, command, query, migration, or schema change.

```ts
// Add types, payloads, or schemas here when useful.
```

## Acceptance criteria

Use behavior-level criteria that can be checked by tests or manual QA.

```gherkin
Given ...
When ...
Then ...
```

## Tests to add or preserve

### Existing tests to preserve

- `path/to/existing.test.ts`

### New tests to add

- `path/to/new.test.ts` — expected behavior

### Manual QA

- [ ] Demo path works
- [ ] Empty state works
- [ ] Error state works
- [ ] Permission boundary works
- [ ] Non-goals were not accidentally built

## Implementation hints

Likely files, modules, components, services, or commands. These are hints, not authority over the existing codebase.

- `path/to/file`
- `path/to/module`

## Verification commands

Commands to run before calling the work complete.

```bash
# examples
npm test
npm run lint
npm run typecheck
```

## Rollout and safety notes

Document anything needed to ship safely.

- migration or backfill needed:
- feature flag needed:
- observability/logging needed:
- analytics/event tracking needed:
- accessibility requirements:
- security/privacy considerations:

## Drift protocol

If implementation reality conflicts with this packet, do not silently patch around the plan.

Return:

```md
## Planning drift found

The selected artifact says:
- ...

The implementation reality is:
- ...

Options:
1. Update the code to match the artifact.
2. Update the artifact because the original assumption was wrong.
3. Split the slice and defer the conflicting part.

Recommended move:
- ...
```

## Done standard

Before declaring work complete, verify:

- [ ] implementation stayed inside the selected slice
- [ ] code maps back to requirement, affordance, store, and slice IDs
- [ ] acceptance criteria pass
- [ ] relevant tests were added or preserved
- [ ] non-goals were not implemented
- [ ] planning drift was reported or repaired
- [ ] follow-up planning changes are noted
```
