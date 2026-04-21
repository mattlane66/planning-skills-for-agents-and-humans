---
planning: true
---

# Spike-Driven Time Window Filter — Shaping After Spike

## Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| R0 | User can set a common analytics time window faster than with the manual picker alone. | Core goal |
| R1 | Existing manual date range picker remains available. | Must-have |
| R2 | Ambiguous input must not silently produce the wrong time window. | Must-have |
| R3 | First version should support only a small, explicit set of expressions. | Must-have |

## Shapes

### A: Keep manual picker only

| Part | Mechanism |
|------|-----------|
| A1 | Existing date range picker remains the only input |

### B: Add narrow natural-language time window input

| Part | Mechanism | Flag |
|------|-----------|:----:|
| B1 | Add text input for time-window phrases | |
| B2 | Support only a narrow allowlist: `last 7 days`, `last 30 days`, `this month`, `previous month`, `this quarter` | |
| B3 | Parse supported phrases into a normalized range object with start date, end date, and display label | |
| B4 | Invalid or ambiguous input shows inline feedback and leaves the current filter unchanged | |
| B5 | Manual date picker remains available alongside text input | |

## Fit Check

| Req | Requirement | Status | A | B |
|-----|-------------|--------|---|---|
| R0 | User can set a common analytics time window faster than with the manual picker alone. | Core goal | ❌ | ✅ |
| R1 | Existing manual date range picker remains available. | Must-have | ✅ | ✅ |
| R2 | Ambiguous input must not silently produce the wrong time window. | Must-have | ✅ | ✅ |
| R3 | First version should support only a small, explicit set of expressions. | Must-have | ✅ | ✅ |

## Notes

- The spike resolved the flagged unknown by narrowing the parser scope.
- Shape B now has a concrete allowlist, a defined parser output, and explicit failure behavior.
- This is now concrete enough to breadboard.

## Decision

Chosen direction: **B**

## Detail B

The first version should include:
- a natural-language text input
- a small safe allowlist of phrases
- normalized range output into the existing analytics filter
- inline feedback for unsupported or ambiguous input
- the existing manual picker kept alongside the new input
