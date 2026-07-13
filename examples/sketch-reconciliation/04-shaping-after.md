# Availability Board - Shaping After Visual Review

## Selected shape

### A: Single comparison surface with natural-language control

| Part | Mechanism | Flag |
|---|---|:---:|
| A1 | Render one comparison table with one column per location. | |
| A2 | Parse the input into location and date changes, then refresh the table. | |
| A3 | 🟡 Display the selected date persistently above the table and refresh the label with accepted date changes. | |

## Fit check

| Req | Requirement | Status | A |
|---|---|---|:---:|
| R0 | A user can compare working hours across selected locations. | Core goal | ✅ |
| R1 | A user can change locations and the selected date through natural-language input. | Must-have | ✅ |
| R2 | 🟡 A user can tell which date the displayed hours belong to. | Must-have | ✅ |

## Reverse fit check

| Shape part | Mechanism | Requirement(s) served | Justified? |
|---|---|---|:---:|
| A3 | Persistent selected-date label | R2 | ✅ |
