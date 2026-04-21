---
planning: true
---

# Brownfield Member Admin Search — Frame

## Source

> Today there is already a Member Admin page.
>
> It has a status filter, a paginated member table, and row click into a member detail page.
>
> What is missing: no text search on the page.
>
> Admins keep clicking through many pages just to find one person.
>
> When they refresh or use the back button, the page often loses the state they were just using.
>
> Important constraints: keep the current status filter, keep the current detail-page flow, and change the current page as little as possible while still making lookup faster.

## Problem

- The existing admin page supports browsing, but not fast lookup of a known member by name.
- Admins lose time paging through results when they already know who they are trying to find.
- Current page state is not reliably preserved across refresh and back-button flows.
- The team wants to improve lookup without discarding the current page structure that already works.

## Outcome

- Admins can quickly find a member by name from the current admin page.
- The current status filter and member-detail flow continue to work.
- Search and filter state can be restored on refresh and back navigation.
- The first version improves the current page instead of replacing it with a separate admin tool.

## Less about

- building a whole new admin experience
- advanced search syntax
- replacing the current page architecture

## More about

- faster lookup inside the existing workflow
- preserving current behavior that already works
- restoring state so navigation feels reliable
