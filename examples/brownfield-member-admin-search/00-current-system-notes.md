# Brownfield Member Admin Search — Current System Notes

These are intentionally rough notes about an existing system.

Use them as the input to `/framing-doc`.

---

Today there is already a Member Admin page.

It has:
- a status filter
- a paginated member table
- row click into a member detail page

What is missing:
- no text search on the page
- admins keep clicking through many pages just to find one person
- when they refresh or use the back button, the page often loses the state they were just using

Important constraints:
- do not replace the whole page with a separate admin tool unless that is clearly better
- keep the current status filter
- keep the current detail-page flow
- first version should change the current page as little as possible while still making lookup faster
