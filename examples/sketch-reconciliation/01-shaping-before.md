# Availability Board - Shaping Before Visual Review

## Accepted Appetite and cut line

- Appetite: one comparison surface with natural-language control and enough visible context to interpret the displayed hours
- Cut line: no account system, saved comparison sets, calendar UI, scheduling, or time-zone conversion
- Accepted uncertainty: exact visual placement may change during sketch review without expanding the product boundary

## Accepted Requirements

| ID | Requirement | Status | Authority |
|---|---|---|---|
| R0 | A user can compare working hours across selected locations. | Core goal | Accepted |
| R1 | A user can change locations and the selected date through natural-language input. | Must-have | Accepted |
| R2 | A user can tell which date the displayed hours belong to. | Must-have | Accepted |

## Selected shape

### A: Single comparison surface with natural-language control

| Part | Mechanism | Flag |
|---|---|:---:|
| A1 | Render one comparison table with one column per location. | |
| A2 | Parse the input into location and date changes, keep the accepted date visible in the natural-language control, then refresh the table. | Exact presentation remains open for sketch review. |

## Fit check

| Req | Requirement | Status | A |
|---|---|---|:---:|
| R0 | A user can compare working hours across selected locations. | Core goal | ✅ |
| R1 | A user can change locations and the selected date through natural-language input. | Must-have | ✅ |
| R2 | A user can tell which date the displayed hours belong to. | Must-have | ✅ |

R2 is supported by A2, but its presentation is intentionally left open within the accepted visual-detail uncertainty.

## Human Decision

Recorded human choice: **Shape A**.

The selection accepts the requirements, Appetite, cut line, and the remaining visual-detail uncertainty. A later sketch may propose a clearer mechanism, but it cannot silently replace this accepted shape.
