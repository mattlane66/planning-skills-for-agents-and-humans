---
planning: true
---

# Spike-Driven Time Window Filter — Initial Shaping

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

### B: Add natural-language time window input

| Part | Mechanism | Flag |
|------|-----------|:----:|
| B1 | Add text input for time-window phrases | |
| B2 | Parse phrases such as "last 7 days" and "previous month" into a structured range | ⚠️ |
| B3 | Invalid or ambiguous input shows feedback and does not silently update the filter | |
| B4 | Manual date picker remains available alongside text input | |

## Fit Check

| Req | Requirement | Status | A | B |
|-----|-------------|--------|---|---|
| R0 | User can set a common analytics time window faster than with the manual picker alone. | Core goal | ❌ | ❌ |
| R1 | Existing manual date range picker remains available. | Must-have | ✅ | ✅ |
| R2 | Ambiguous input must not silently produce the wrong time window. | Must-have | ✅ | ❌ |
| R3 | First version should support only a small, explicit set of expressions. | Must-have | ✅ | ⚠️ |

## Notes

- Shape A preserves the current system but does not satisfy the core goal.
- Shape B is promising, but B2 is still a flagged unknown.
- We should not pretend B passes until the parser behavior is made concrete enough to evaluate.

## Next step

Create a spike for B2 before selecting the direction.
