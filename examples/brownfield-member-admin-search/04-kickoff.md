---
planning: true
---

# Brownfield Member Admin Search — Kickoff

## Frame

### Problem
- The existing admin page supports browsing but not fast lookup by member name.
- Admins waste time paging through results to find one known person.
- Current page state is not reliably restored across refresh and back navigation.

### Outcome
- Admin can search by name from the existing admin page.
- Existing status filter and detail-page navigation remain intact.
- Search and filter state can be restored from URL state.

### Constraints
- Preserve the current page structure as much as possible in the first version.
- Do not replace the existing admin page with a separate search tool.

## Shape

### Member admin page
- Keep the existing status filter and member table.
- Add a search input to the current page.
- Search and status filter combine to determine the visible list.

### State restoration
- Query and filter state are written to the URL.
- Page load restores query and filter state from the URL.
- Back navigation should return the admin to the prior search/filter state.

### Detail-page flow
- Existing row click to member detail page remains intact.
- The search enhancement should not change the current detail-page destination.
