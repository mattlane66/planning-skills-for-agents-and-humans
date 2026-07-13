# Account Settings — Implementation Reality

These notes represent what an agent found by reading the current implementation and exercising the display-name flow.

## Current behavior

- The display-name field is initialized from the profile response.
- Typing updates the same client-side profile value used by the saved-name preview; draft and confirmed values are not stored separately.
- Clicking Save sends the current field value to the profile mutation.
- On success, the mutation result replaces the cached profile and the page remains in place.
- On failure, the error is logged and a short generic toast appears.
- There is no persistent error state or visible Retry action.
- After a failed save, the preview still shows the unsaved draft value because it reads the mutated client cache.

## Current implementation map

| Intended ID | Current implementation reality | Alignment |
| --- | --- | --- |
| `AFF-01` / `STORE-01` | Editing writes directly into the cached profile object. | Drift: no separate draft store. |
| `AFF-02` / `N-02` | Save submits the current field value. | Mostly aligned. |
| `AFF-03` / `STORE-02` | Preview reads the same value changed during typing. | Drift: preview does not prove persistence. |
| `P-02` / `AFF-05` / `STORE-03` | Failure produces a transient generic toast and console log. | Drift: intended persistent failure state is absent. |
| `AFF-04` | No retry control exists. | Missing behavior. |

## Verification evidence

1. Enter `Alexandra` while the saved value is `Alex`.
2. The preview changes to `Alexandra` before Save is clicked.
3. Force the profile request to fail.
4. A generic toast appears briefly.
5. The preview still shows `Alexandra`, although a reload restores `Alex` from the server.

## Unknowns

- Whether the generic toast is an intentional product decision or a temporary implementation shortcut.
- Whether other profile fields depend on mutating the shared cache during editing.
