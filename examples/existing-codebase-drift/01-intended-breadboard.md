---
planning: true
shaping: true
artifact_type: breadboard
project: account-settings-display-name
status: selected
source_of_truth: true
feeds:
  - slice-plan
  - implementation
---

# Account Settings — Intended Breadboard

# Context Card

## Use this when
An agent is implementing or checking the display-name settings flow.

## Must preserve
- user sees the saved display name immediately after success
- save failure is visible and recoverable
- unsaved draft value is not confused with saved profile value
- stable IDs for places, affordances, stores, and slice

## Ignore unless asked
- avatar upload
- email-change flow
- profile visibility settings

## Places

| ID | Place | Description |
|---|---|---|
| P-01 | Account settings page | User edits account profile fields. |
| P-02 | Save failure state | Same page with visible error and retry path. |

## UI Affordances

| ID | Place | Component | Affordance | Control | Wires Out | Returns To |
|---|---|---|---|---|---|---|
| AFF-01 | P-01 | Display name field | Edit draft display name | type | -> N-01 | STORE-01 |
| AFF-02 | P-01 | Save button | Save display name | click | -> N-02 | AFF-03 or P-02 |
| AFF-03 | P-01 | Saved-name preview | Show current saved display name | display | — | reads STORE-02 |
| AFF-04 | P-02 | Retry save button | Retry failed save | click | -> N-02 | AFF-03 or P-02 |
| AFF-05 | P-02 | Error message | Explain save failure | display | — | reads STORE-03 |

## Non-UI Affordances

| ID | Place | Component | Affordance | Control | Wires Out | Returns To |
|---|---|---|---|---|---|---|
| N-01 | P-01 | Settings form | Track draft value separately from saved value | change | -> STORE-01 | AFF-01 |
| N-02 | P-01 | Profile mutation | Persist display name | submit | -> N-03 | AFF-03 or P-02 |
| N-03 | P-01 | Save result handler | Branch on success or failure | result | -> STORE-02 or STORE-03 | AFF-03 or AFF-05 |

## Stores

| ID | Place | Store | Description |
|---|---|---|---|
| STORE-01 | P-01 | Draft display name | Unsaved local value in the form. |
| STORE-02 | P-01 | Saved profile display name | Last confirmed value from the profile service. |
| STORE-03 | P-02 | Save error | Error state shown when persistence fails. |

## Behavior traces

| Scenario | Entry | Control path | Decision / branch | State / data effect | Observable consequence | Status |
|---|---|---|---|---|---|---|
| Save display name | AFF-01, AFF-02 | AFF-01 → N-01; AFF-02 → N-02 → N-03 | N-03: success | N-01 → STORE-01; N-03 → STORE-02 | STORE-02 → AFF-03 | supported |
| Show save failure | AFF-02 | AFF-02 → N-02 → N-03 | N-03: failure | N-03 → STORE-03; STORE-02 unchanged | STORE-03 → AFF-05 in P-02 | supported |
| Retry failed save | AFF-04 | AFF-04 → N-02 → N-03 | success or failure | STORE-02 or STORE-03 updated | AFF-03 or AFF-05 | supported |

## Reverse-trace audit

| Observable consequence | Direct incoming sources | Upstream entries / writers | Unresolved predecessors | Status |
|---|---|---|---|---|
| AFF-03 saved preview | STORE-02 from N-03 | AFF-02 or AFF-04 via N-02 | none | supported |
| AFF-05 save error | STORE-03 from N-03 | AFF-02 or AFF-04 via N-02 | none | supported |

## Selected Slice

| ID | Slice | Demo | Produces | Exclusions |
|---|---|---|---|---|
| V1 | Display-name save with failure recovery | Edit name, save successfully, then simulate failed save and retry | A settings flow where success and failure states are visible and recoverable | Avatar upload, email change, profile visibility |

## Verification Target

- After a successful save, the saved-name preview updates from `STORE-02`.
- If saving fails, the user sees `AFF-05` and can retry with `AFF-04`.
- Draft state and saved state remain distinct.
