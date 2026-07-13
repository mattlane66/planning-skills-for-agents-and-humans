# Availability Board - Sketch Reconciliation

## Sources

- Visual: `02-availability-sketch.svg`
- User instruction: the selected date must always be clear while commands change the view
- Shaping artifact: `01-shaping-before.md`

## Observation inventory

| Observation | Visible evidence | Confidence |
|---|---|:---:|
| OBS1 | A date label is displayed above the comparison table. | high |
| OBS2 | A natural-language field appears below the table. | high |

## Observation-to-plan mapping

| Observation | Requirement(s) | Shape part(s) | Breadboard IDs | Status by layer | Notes |
|---|---|---|---|---|---|
| OBS1 | R2 | - | - | R2: covered; Shape A: missing | R2 has no explicit visible mechanism in Shape A. |
| OBS2 | R1 | A2 | - | covered | The image does not prove the parser's internal behavior. |

## Proposed deltas

| Delta | Target | Proposed change | Evidence | Fit / scope impact | Decision |
|---|---|---|---|---|---|
| D1 | Shape A | Add A3: display the selected date persistently above the table and refresh it with accepted date changes. | OBS1 + explicit user instruction | Makes R2 pass; clarifies the selected UI mechanism. | accepted |

## Accepted changes

| Delta | Artifact and IDs updated | Result |
|---|---|---|
| D1 | Shape A: A3; Fit check: R2 | R2 is backed by an explicit visible mechanism. |

## Fit-check impact

- Shape part added: A3
- Fit check rerun: yes
- Reverse fit check rerun: yes; A3 serves R2
- Result: all must-have requirements pass for Shape A

## Ripple status

| Artifact | Status | Update or follow-up |
|---|---|---|
| Shaping | updated | See `04-shaping-after.md`. |
| Breadboard | stale | Add a visible date affordance and wire it to accepted date-state changes. |
| Slices | not affected yet | Slice planning has not started. |
