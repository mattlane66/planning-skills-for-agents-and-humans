---
planning: true
---

# Brownfield Member Admin Search — Shaping

## Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| R0 | Admin can quickly find a known member by name from the current admin page. | Core goal |
| R1 | Existing status filter remains available. | Must-have |
| R2 | Existing member-detail navigation remains intact. | Must-have |
| R3 | Search and filter state can be restored on refresh and back navigation. | Must-have |
| R4 | First version should preserve the current page structure as much as possible. | Must-have |

## Shapes

### CURRENT: Existing paginated browse-only page

| Part | Mechanism |
|------|-----------|
| CURRENT1 | Status filter narrows the member table |
| CURRENT2 | Paginated member table supports browse flow |
| CURRENT3 | Row click opens member detail page |
| CURRENT4 | Current page state is not reliably restored after refresh or back navigation |

### A: Add search and URL-backed state to the current page

| Part | Mechanism |
|------|-----------|
| A1 | Add search input to existing admin page |
| A2 | Search input updates query state |
| A3 | Member table is filtered by query plus existing status filter |
| A4 | Query and filter state are written to URL |
| A5 | Page initializes from URL state on load |

### B: Create a separate search page for member lookup

| Part | Mechanism |
|------|-----------|
| B1 | Add a dedicated member search page |
| B2 | Current admin page links out to the search page |
| B3 | Search results navigate to member detail page |
| B4 | Search page owns its own state restoration |

## Fit Check

| Req | Requirement | Status | CURRENT | A | B |
|-----|-------------|--------|---------|---|---|
| R0 | Admin can quickly find a known member by name from the current admin page. | Core goal | ❌ | ✅ | ❌ |
| R1 | Existing status filter remains available. | Must-have | ✅ | ✅ | ❌ |
| R2 | Existing member-detail navigation remains intact. | Must-have | ✅ | ✅ | ✅ |
| R3 | Search and filter state can be restored on refresh and back navigation. | Must-have | ❌ | ✅ | ✅ |
| R4 | First version should preserve the current page structure as much as possible. | Must-have | ✅ | ✅ | ❌ |

## Notes

- `CURRENT` makes the baseline explicit: the page already works for browsing but not for fast lookup.
- Shape A modifies the existing page in place and best fits the current constraints.
- Shape B could support search, but it breaks the requirement that the first version preserve the current page structure.

## Decision

Chosen direction: **A**

## Detail A

The selected direction keeps the existing admin page and adds:
- search input
- URL-backed query and filter state
- filtered table results
- restore-on-load behavior
