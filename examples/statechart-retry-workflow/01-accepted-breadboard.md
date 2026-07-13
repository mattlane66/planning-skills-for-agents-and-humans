# Background Import — Accepted Breadboard

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

## Selected slice

| ID | Slice | Demo | Exclusions |
| --- | --- | --- | --- |
| V1 | Import job lifecycle | Start an import, observe progress, complete successfully, then demonstrate failure, retry, cancellation, and timeout. | Retry limits, backoff policy, concurrent imports, and resumable uploads. |
