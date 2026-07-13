# Statechart Retry Workflow — Example

This example shows when the optional Statechart skill adds value after breadboarding.

The accepted breadboard describes a background import with success, failure, retry, cancellation, and timeout behavior. The derived statechart makes those transitions easier to review without replacing the breadboard as source of truth.

## Files

- [`01-accepted-breadboard.md`](./01-accepted-breadboard.md) — source places, affordances, stores, wiring, and selected slice
- [`02-derived-statechart.md`](./02-derived-statechart.md) — state inventory, transition table, Mermaid projection, and gaps

## Try it

```text
/statechart examples/statechart-retry-workflow/01-accepted-breadboard.md "Scope: V1 import job lifecycle"
```

What to notice:

- every state and transition points back to source breadboard IDs
- the transition table is primary and Mermaid mirrors it
- the statechart does not invent retry counts, backoff, or concurrent imports
- missing behavior is listed as a breadboard gap rather than silently resolved
