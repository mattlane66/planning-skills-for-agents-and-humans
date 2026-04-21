---
planning: true
---

# Spike-Driven Time Window Filter — Breadboard

## Places

| ID | Place | Description |
|----|-------|-------------|
| P1 | Analytics filter bar | Existing analytics filter area with manual date picker and new text input |
| P2 | Invalid input feedback state | User-visible state where unsupported or ambiguous input is rejected |
| P3 | Analytics results view | View that reflects the currently active time window |

## UI Affordances

| ID | Place | Component | Affordance | Control | Wires Out | Returns To |
|----|-------|-----------|------------|---------|-----------|------------|
| U1 | P1 | time-window-input | natural-language input | type | → N1 | — |
| U2 | P1 | date-picker | manual date picker | change | → N6 | — |
| U3 | P1 | filter-bar | apply / confirm action | click | → N2 | — |
| U4 | P2 | time-window-input | invalid-input message | display | — | ← N4 |
| U5 | P3 | analytics-results | current results view | display | — | ← N7 |

## Non-UI Affordances

| ID | Place | Component | Affordance | Control | Wires Out | Returns To |
|----|-------|-----------|------------|---------|-----------|------------|
| N1 | P1 | time-window-input | update raw input state | call | → N2 | — |
| N2 | P1 | parser | evaluate input against allowlist | call | → N3, → N4 | ← S1 |
| N3 | P1 | parser | normalize supported phrase into range object | call | → N5 | — |
| N4 | P1 | validation | reject invalid or ambiguous input | call | → U4 | — |
| N5 | P1 | filter-state | update active time-window state from normalized range | call | → N7 | ← S2 |
| N6 | P1 | date-picker | update active time-window state from manual picker | call | → N7 | ← S2 |
| N7 | P3 | analytics-query | refresh analytics results for active time window | call | — | ← S2 |

## Stores

| ID | Place | Store | Description |
|----|-------|-------|-------------|
| S1 | P1 | rawInput | Current natural-language text input |
| S2 | P1 | activeTimeWindow | Current normalized active time-window state |

## Notes

- The spike resolved the parser uncertainty by narrowing the input to an explicit allowlist.
- Invalid or ambiguous input is modeled as a visible consequence, not as a silent internal failure.
- The existing manual date picker remains as a parallel path into the same active time-window state.

## Likely slices

### V1 — Support narrow natural-language phrases
Demo:
- user enters `last 7 days` and results refresh using the normalized range

Produces:
- safe first-version natural-language time-window input

### V2 — Preserve manual picker and invalid-input feedback
Demo:
- user can still use the manual picker
- unsupported input shows feedback and leaves the current time window unchanged

Produces:
- safe coexistence of manual and natural-language input paths
