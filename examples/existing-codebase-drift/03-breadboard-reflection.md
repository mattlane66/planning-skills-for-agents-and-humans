# Account Settings — Breadboard Reflection

## Current implementation reality recorded

The intended and current views are recorded side by side rather than silently overwriting either one.

| Source ID | Intended behavior | Current behavior |
| --- | --- | --- |
| `STORE-01`, `STORE-02` | Draft and confirmed display names remain distinct. | Typing mutates the cached profile value used by the preview. |
| `AFF-03` | Preview shows the last confirmed saved value. | Preview shows the current draft before persistence succeeds. |
| `P-02`, `AFF-05`, `STORE-03` | Failure remains visible in a recoverable state. | Failure produces a transient generic toast. |
| `AFF-04` | User can explicitly retry. | No Retry action exists. |

## Drift found

| ID | Drift | Risk | Recommended move |
| --- | --- | --- | --- |
| `D1` | Draft and saved state are conflated. | A failed save can look successful until reload. | Restore a separate draft value or change the approved behavior explicitly. |
| `D2` | The persistent failure place was replaced by a transient toast. | Users may miss the error and have no durable recovery path. | Implement the selected failure state unless the human chooses a revised interaction. |
| `D3` | Retry is missing. | Recovery requires another implicit Save attempt with unclear state. | Add the selected Retry affordance or record a human-approved alternative. |

## Decision options

1. Update the implementation to match the selected breadboard: separate draft and saved values, show persistent failure feedback, and provide Retry.
2. Update the breadboard after a human decision that optimistic preview plus transient failure feedback is acceptable.
3. Split recovery into a later slice and explicitly narrow the current slice and verification target.

## Recommended move

Choose option 1. The original requirement says failure must be visible and recoverable, and the current implementation can display unsaved data as though it were confirmed. If product constraints have changed, stop for a human decision before changing the selected breadboard.

## Planning updates

- Keep this current-state record alongside the accepted-intent breadboard until the decision is made.
- If option 1 is selected, retain the intended breadboard and link the implementation follow-ups to `STORE-01`, `STORE-02`, `P-02`, `AFF-04`, and `AFF-05`.
- If option 2 or 3 is selected, update the selected slice and verification target explicitly; do not silently rewrite them.
