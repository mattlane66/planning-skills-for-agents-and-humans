# Stable IDs

Stable IDs keep decisions, deltas, diagrams, contracts, examples, and implementation evidence traceable across planning levels.

## Defaults

| Prefix | Meaning | Example |
|---|---|---|
| `WF` | local Wayfinding ticket within one map | `WF-003` |
| `R` | requirement or criterion | `R2` |
| `P` | place | `P1` |
| `U` | user-facing affordance | `U4` |
| `N` | non-UI affordance or product-relevant hidden behavior | `N3` |
| `S` | store or state | `S2` |
| `ST` | state | `ST1` |
| `TR` | transition | `TR4` |
| `C` | interface contract | `C2` |
| `RUN` | example run | `RUN1` |
| `E` | edge case | `E3` |
| `SP` | spike | `SP1` |
| `T` | task | `T4` |
| `TG` | task group | `TG2` |
| `CUT` | explicit scope cut | `CUT1` |
| `OBS` | visual observation | `OBS2` |
| `D` | proposed reconciliation delta | `D3` |
| `V` | vertical slice | `V1` |

Use sub-identifiers such as `R3.1` or `P2.1` when grouping improves legibility.

## Preservation rules

- Preserve IDs already used by accepted artifacts, implementation references, or review comments.
- Do not renumber items merely to remove gaps.
- Do not rename IDs for style consistency.
- When wording changes but meaning remains, retain the ID and record the edit when material.
- A requirement or criterion keeps the same `R##` from evidence-backed candidate through Working, Accepted, selected-mechanism mapping, implementation handoff, and realized-fit assessment; those transitions change authority or evidence state, not identity.
- When meaning changes substantially, create a new ID or an explicit supersession record.
- Derived views should retain source IDs so readers can trace them back to the authoritative table.

## Imported conventions

Existing projects may use forms such as:

- `REQ-01`
- `AFF-03`
- `STATE-CANCELLED`
- `SLICE-02`

Preserve established project conventions when they are clear and internally consistent. Do not translate them solely to match this repository's defaults.

## Rejected and deferred items

Keep rejected or deferred IDs visible when they matter to the audit trail. Mark status explicitly rather than deleting or recycling the identifier.

## Generated diagrams

Tables remain authoritative. Mermaid or other generated views should show stable IDs in labels whenever doing so keeps the diagram traceable without making it unreadable.
