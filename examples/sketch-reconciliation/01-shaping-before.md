# Availability Board - Shaping Before Visual Review

## Requirements

| ID | Requirement | Status |
|---|---|---|
| R0 | A user can compare working hours across selected locations. | Core goal |
| R1 | A user can change locations and the selected date through natural-language input. | Must-have |
| R2 | A user can tell which date the displayed hours belong to. | Must-have |

## Selected shape

### A: Single comparison surface with natural-language control

| Part | Mechanism | Flag |
|---|---|:---:|
| A1 | Render one comparison table with one column per location. | |
| A2 | Parse the input into location and date changes, then refresh the table. | |

## Fit check

| Req | Requirement | Status | A |
|---|---|---|:---:|
| R0 | A user can compare working hours across selected locations. | Core goal | ✅ |
| R1 | A user can change locations and the selected date through natural-language input. | Must-have | ✅ |
| R2 | A user can tell which date the displayed hours belong to. | Must-have | ❌ |

R2 is not yet backed by an explicit visible mechanism.
