---
planning: true
---

# Simple Grocery List — Frame

## Source

> I keep texting my partner grocery items and then we lose track of what is still needed.
>
> Need to be able to add an item quickly when I remember it.
>
> At the store, I need to see what is still not bought without scanning a bunch of crossed-out stuff.
>
> Would be nice if bought items could be hidden but not deleted.
>
> I do not want accounts, sign-in, prices, recipes, categories, or store-specific logic.
>
> It should keep the list when I come back later on the same device.
>
> If I add "milk" twice by accident, it should probably stop me or at least make that obvious.

## Current situation

- Trigger or context: One partner remembers grocery items at different moments, then both need a dependable list while shopping.
- Current approach: Items are sent through ad hoc text messages.
- Current result: The messages are easy to add but hard to treat as a shared, current list of what is still needed.
- Struggle or compromise: The pair loses state, scans crossed-out items, and cannot reliably distinguish pending from bought items.
- Evidence and confidence: Directly supported by the source notes; shared-device and multi-user behavior remain unknown.

## Problem

- The current list lives in ad hoc messages, so the state of what is still needed is easy to lose.
- Adding items is lightweight, but the resulting list is not easy to use while shopping.
- The current setup does not preserve a clean, reusable grocery list state on the same device.

## Transformation frame (x → f() → y)

- x — trigger/context: Grocery items arise at different moments and both partners later need a current list while shopping.
- x — current approach: Send items through ad hoc text messages.
- x — current result / breakdown: Capture is quick, but messages accumulate without a durable pending/bought state that is easy to recover and scan.
- f() — solution / shape variable: intentionally unspecified
- y — desired outcome: Quickly capture items and later see a persistent, legible view of what is still needed.
- Gap: Preserve low-friction capture while adding clear, reversible grocery state.
- Boundaries: Same-device, small first version; no accounts, pricing, recipes, categories, or store logic.

## Operating model (M, optional)
- Authority: Accepted
- Relevant operating conditions: the first version runs on one device with local state available between ordinary sessions
- Causal assumptions / projected dynamics: same-device state remains available across ordinary returns unless storage is explicitly cleared or unavailable
- Evidence refs / confidence: product constraint plus ordinary local-runtime behavior; verify during implementation
- Revisit conditions: cross-device use, accounts, or a runtime without dependable local persistence enters scope

## Outcome

- A user can add grocery items quickly.
- A user can clearly see which items are still needed while shopping.
- Bought items can be hidden without being lost.
- The list persists on the same device between sessions.

## Less about

- meal planning
- shared accounts or permissions
- pricing, recipes, or store-specific features
- broad household management

## More about

- fast capture
- clear in-store use
- simple persistent state
- a small first version with one clear job
