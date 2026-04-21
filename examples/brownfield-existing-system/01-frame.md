---
planning: true
---

# Brownfield Existing System — Frame

## Source

> We already have an admin user list page.
>
> It has basic filters, but they do not persist in the URL.
>
> If I refresh, I lose my place.
>
> If I send someone a link, they do not land in the same filtered state.
>
> Would be nice if search updated live instead of needing a full submit.
>
> Do not redesign the page from scratch.
>
> We want to improve the current page, not replace the current workflow.

## Problem

- The current admin page loses filter/search state on refresh.
- The current URL does not represent the filtered state, so links are not shareable.
- Search interaction is slower than it needs to be because it depends on a more manual submit flow.
- The team needs to improve the current page without disrupting the current admin workflow.

## Outcome

- The current admin page preserves filter and search state on refresh.
- A copied link lands another user in the same state.
- Search feels more immediate on the existing page.
- The current table and bulk actions remain intact.

## Less about

- redesigning the admin page
- creating a separate search page
- replacing the current workflow

## More about

- improving the current page in place
- preserving existing affordances that already work
- making state legible and shareable
