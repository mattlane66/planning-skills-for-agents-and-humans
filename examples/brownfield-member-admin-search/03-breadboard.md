---
planning: true
---

# Brownfield Member Admin Search — Breadboard

## Places

| ID | Place | Description |
|----|-------|-------------|
| P1 | Member admin page | Existing admin page with status filter and member table |
| P2 | Member detail page | Existing member detail destination |
| P3 | Browser URL boundary | External state used to restore query and filter |

## UI Affordances

| ID | Place | Component | Affordance | Control | Wires Out | Returns To |
|----|-------|-----------|------------|---------|-----------|------------|
| U1 | P1 | filters | status filter | change | → N2 | — |
| U2 | P1 | member-search | search input | type | → N1 | — |
| U3 | P1 | member-table | member list | display | — | ← N6 |
| U4 | P1 | member-row | row click | click | → P2 | — |

## Non-UI Affordances

| ID | Place | Component | Affordance | Control | Wires Out | Returns To |
|----|-------|-----------|------------|---------|-----------|------------|
| N1 | P1 | member-search | update query state | call | → N4 | — |
| N2 | P1 | filters | update status filter state | call | → N4 | — |
| N3 | P1 | page-init | initialize state from URL | call | → N4 | ← S1, S2 |
| N4 | P1 | member-query | compute current member query | call | → N5, → N7 | ← S1, S2 |
| N5 | P1 | member-service | fetch filtered member list | call | → N6 | — |
| N6 | P1 | member-table | show current member list | call | — | ← S3 |
| N7 | P3 | url-state | write query and filter state to URL | call | — | ← S1, S2 |
| N8 | P3 | url-state | read query and filter state from URL | call | → N3 | → S1, S2 |

## Stores

| ID | Place | Store | Description |
|----|-------|-------|-------------|
| S1 | P1 | query | Current search text |
| S2 | P1 | statusFilter | Current selected status filter |
| S3 | P1 | members | Current visible member list |

## Notes

- This breadboard keeps the existing page as the main place rather than introducing a separate search page.
- The new behavior is added into the current workflow.
- URL state is modeled as an external boundary because refresh and back navigation are part of the requirement.

## Likely slices

### V1 — Add search input and filtered member list
Demo:
- admin types a member name and the list narrows on the existing page

Produces:
- fast lookup inside the current workflow

### V2 — Add URL-backed state restoration
Demo:
- refresh and back navigation restore the query and filter state

Produces:
- reliable state restoration across navigation
