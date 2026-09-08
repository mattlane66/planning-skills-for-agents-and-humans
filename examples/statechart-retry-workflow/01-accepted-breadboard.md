---
planning: true
mode: selected-design
---

# Background Import — Accepted Breadboard

## Mode and accepted sources

- Mode: `selected-design`
- Accepted project boundary: one background import job lifecycle
- Accepted requirements: start a valid import, observe progress, see a terminal result, cancel an active import, and retry a failed import
- Accepted Appetite: one reviewable lifecycle with explicit success, failure, retry, cancellation, and timeout behavior
- Accepted cut line: no retry limits, backoff policy, concurrent imports, resumable uploads, or recovery after browser closure
- Human-selected shape: one background job with progress updates and explicit terminal results
- Human-selected slice: V1 — Import job lifecycle

This compact example carries its accepted inputs inline so the derived statechart can cite a complete selected-design source.

## Places

| ID | Place | Description |
| --- | --- | --- |
| P1 | Import setup | User selects a file and starts an import. |
| P2 | Import progress | User sees active progress and may cancel. |
| P3 | Import result | User sees success or failure and may retry a failed import. |

## UI affordances

| ID | Place | Affordance | Control | Wires Out | Returns To |
| --- | --- | --- | --- | --- | --- |
| U1 | P1 | Select import file | choose file | → S1 | — |
| U2 | P1 | Start import | click | → N1 | — |
| U3 | P2 | Cancel import | click | → N5 | — |
| U4 | P3 | Retry failed import | click | → N2 | — |
| U5 | P2 | Show progress | display | — | ← N3 |
| U6 | P3 | Show import result | display | — | ← N4, N6 |

## Non-UI affordances

| ID | Place | Affordance | Control | Wires Out | Returns To |
| --- | --- | --- | --- | --- | --- |
| N1 | P1 | Validate selected file | call | → N2 or P3 | → U6 on validation failure |
| N2 | P1 / P3 | Start background import | call | → S2, P2 | — |
| N3 | P2 | Receive progress update | message | → S2 | → U5 |
| N4 | P2 | Receive completion result | message | → S2, P3 | → U6 |
| N5 | P2 | Cancel active import | call | → S2, P3 | → U6 |
| N6 | P2 | Detect import timeout | timer | → S2, P3 | → U6 |

## Stores

| ID | Store | Description |
| --- | --- | --- |
| S1 | Selected file | File chosen for the current import attempt. |
| S2 | Import job state | Current job ID, status, progress, and result. |

## Product-relevant branches

- `N1`: valid file → `N2`; invalid file → `P3` failure result.
- `N4`: completed successfully → `P3` success result; completed with error → `P3` failure result.
- `N5`: cancellation confirmed → `P3` canceled result.
- `N6`: timeout reached → `P3` failure result.
- `U4`: retry starts a new attempt using `S1`.

## Behavior traces

| Scenario | Entry | Control path | Decision / branch | State / data effect | Observable consequence | Status |
|---|---|---|---|---|---|---|
| Reject invalid file | U1, U2 | U1 → S1; U2 → N1 | N1: invalid | no job created | N1 → P3 → U6 failure | supported |
| Start and show progress | U1, U2 | U1 → S1; U2 → N1 → N2; N3 | N1: valid | N2/N3 → S2 | N3 → U5 in P2 | supported |
| Complete import | N4 | N4 → S2, P3 | success or failure | terminal result stored in S2 | N4 → U6 | supported |
| Cancel import | U3 | U3 → N5 → S2, P3 | cancellation confirmed | canceled state stored in S2 | N5 → U6 | supported |
| Retry failure | U4 | U4 → N2 → S2, P2 | new attempt | new job state stored in S2 | later N3 → U5 or N4 → U6 | supported |
| Time out import | N6 | N6 → S2, P3 | timeout reached | failed terminal state stored in S2 | N6 → U6 | supported |

## Reverse-trace audit

| Observable consequence | Direct incoming sources | Upstream entries / writers | Unresolved predecessors | Status |
|---|---|---|---|---|
| U5 progress | N3 | U2 via N1/N2, or U4 via N2 | none | supported |
| U6 terminal result | N1, N4, N5, N6 | U2, U3, U4, active-job timer | none | supported |

## Selected slice

| ID | Slice | Demo | Exclusions |
| --- | --- | --- | --- |
| V1 | Import job lifecycle | Start an import, observe progress, complete successfully, then demonstrate failure, retry, cancellation, and timeout. | Retry limits, backoff policy, concurrent imports, and resumable uploads. |
