# Tracker adapters

Load this reference when creating, querying, claiming, or resolving a Wayfinding map.

## Required operations

Every adapter must support:

1. create and read one map
2. create and read tickets related to that map
3. record blockers
4. list open tickets
5. identify claims
6. resolve or close a ticket
7. link canonical planning artifacts

The **frontier** is the set of open, unclaimed tickets whose blockers are all resolved.

Prefer native child, dependency, assignment, and status relationships when the selected tracker exposes them. Fall back to the conventions below without pretending unsupported relationships are native.

## Local Markdown

Use this default when no external tracker is selected:

```text
planning/
  wayfinding/
    <map-name>/
      map.md
      tickets/
        WF-001-<descriptive-name>.md
        WF-002-<descriptive-name>.md
```

Use `templates/wayfinding-map.md` for `map.md` and `templates/wayfinding-ticket.md` for every ticket.

### Operations

- **Create:** allocate the next stable `WF-###` id within this map.
- **Block:** list ticket ids in `blocked_by`.
- **Claim:** set `claimed_by` and `claimed_at` before substantive work.
- **Query:** find tickets whose `status` is `open`, then exclude claimed tickets and any ticket with an unresolved blocker.
- **Resolve:** write the resolution summary, canonical update links, and resolved date; set `status: resolved`.
- **Rule out:** set `status: out-of-scope`, link it from the map's Out of scope section, and do not add it to Decisions so far.

Use stable filenames after creation. Change the title inside a ticket when its wording improves; do not break links by renaming files casually.

## GitHub Issues

Use GitHub only when the user or repository selects it and issue read/write access has been verified.

### Representation

- map issue label: `wayfinding:map`
- ticket label: `wayfinding:ticket`
- type label: `wayfinding:decision`, `wayfinding:evidence`, `wayfinding:prototype`, or `wayfinding:prerequisite`
- claim: issue assignee
- resolution: issue comment followed by closure

Use native sub-issues and blocked-by relationships when the available GitHub surface exposes them. Otherwise put this metadata near the top of each ticket body:

```markdown
Parent map: #123
Blocked by: #124, #125
Route: `shaping`
Canonical target: `planning/shaping.md#Decision`
Human gate: shape selection
```

Do not describe body links as native dependencies. To calculate the frontier, query open issues carrying both `wayfinding:ticket` and the map relationship, skip assigned issues, and inspect every fallback Blocked by link.

### Resolution comment

```markdown
## Resolution

<concise answer or outcome>

Canonical updates:
- <artifact link and stable IDs>

Human gate:
- <passed, not applicable, or still pending>
```

Do not close a decision ticket while its required human gate is pending. After closure, append a one-line linked gist to the map issue's Decisions so far section.

## Other issue trackers

Map the required operations to the tracker's native concepts. Record the chosen mapping in the map's Notes section.

If an adapter cannot express blockers, claims, or canonical links reliably, use local Markdown instead. Tracker convenience must not weaken the concurrency or authority contract.
