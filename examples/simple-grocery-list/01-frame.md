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

## Problem

- The current list lives in ad hoc messages, so the state of what is still needed is easy to lose.
- Adding items is lightweight, but the resulting list is not easy to use while shopping.
- The current setup does not preserve a clean, reusable grocery list state on the same device.

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
