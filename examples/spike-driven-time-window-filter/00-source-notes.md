# Spike-Driven Time Window Filter — Source Notes

These are intentionally messy notes.

Use them as the input to `/framing-doc`.

---

We already have an analytics page with a normal date filter.

People want to type things like:
- last 7 days
- this quarter
- previous month

This sounds useful, but we do not yet know how the parser should behave.

Important constraints:
- do not break the existing manual date range picker
- ambiguous input should not silently produce the wrong time window
- the first version should focus on a small set of expressions, not every natural-language date expression
