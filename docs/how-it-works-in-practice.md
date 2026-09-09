# How Planning Skills works in practice

This is an **illustrative walkthrough, not a required sequence**. The point is to show how a person actually moves between everyday tools, the product repository, and individual Planning Skills. In real work, use only the moves that resolve a consequential uncertainty; `/plan` may also tell you that no planning skill is needed.

The example uses the same tiny grocery-list idea as [`examples/simple-grocery-list/`](../examples/simple-grocery-list/), so the product is easy to understand:

> Add grocery items quickly, mark them bought, hide bought items without losing them, and have the list still be there later on the same device.

## Start where the thinking already is

The idea does not begin in Planning Skills.

Maybe you have a note from a conversation with your partner, a few bullets in Slack, a quick Figma sketch, and a half-formed thought that this should be a tiny web page. Keep working there while the idea is cheap to change.

When it becomes important enough to build deliberately, open the **product repository** in the agent you use for code. Planning Skills should already be installed, linked, uploaded, or otherwise available to that agent.

In Claude Code, start with:

```text
/planning-skills:plan
```

In Gemini, use `/plan`. In Codex, Claude, Cursor, or another agent, use the portable form:

```text
Use the planning-router skill on these notes, sketch, prototype, and relevant code. Recommend exactly one smallest useful next move, including no planning skill if appropriate.
```

Point the router at what actually exists. Do not rewrite everything into a special input format first.

## Raw notes are still raw, so frame them

In this example, the starting notes mix a real problem with solution ideas:

- grocery items get lost in text messages
- adding an item should be quick
- bought items should be hideable
- maybe it is a tiny web page
- no accounts, recipes, prices, or store logic

The problem boundary is not yet clean enough to judge solutions honestly, so the router recommends **framing**.

In Claude Code:

```text
/planning-skills:frame planning/notes.md
```

The result becomes `planning/frame.md`: the current situation, problem, desired outcome, boundaries, and candidate criteria. “Tiny web page” stays a possible mechanism rather than quietly becoming the requirement.

That file now lives beside the code. The next session or agent does not need the original conversation to recover the accepted problem boundary.

## The problem is clear enough; now shape it

You already have a solution instinct, so you do not restart from a blank slate. Run shaping on the frame and whatever prototype or idea you already have:

```text
/planning-skills:shape planning/frame.md
```

Shaping works requirements and solution shapes together. It might separate needs such as “restore the list on the same device” from mechanisms such as local storage, compare a single-list design with a two-section design, and record the Appetite and cut line for a deliberately small first version.

The working result goes into `planning/shaping.md`.

Nothing says you must finish shaping in one pass. You keep using the smallest move that answers the question in front of you.

## A question talk cannot answer: spike the code

While shaping, you realize one decision depends on the existing implementation: can the current persistence layer restore the list after refresh without adding a new store?

Do not debate it. Ask the code.

```text
/planning-skills:spike planning/shaping.md "Can the current persistence layer restore the list after refresh without a new store?"
```

The agent inspects the code, records the evidence under `planning/spikes/`, and returns the implications to `planning/shaping.md`.

The important part is the round trip: **the spike is not a side conversation**. What it proves or disproves comes back into the artifact where the product decision is being shaped.

## A behavior is still fuzzy: breadboard only that part

Now the remaining uncertainty is behavioral: when “Hide bought” is on, are bought items deleted, moved somewhere else, or merely excluded from the visible list?

That is concrete enough to inspect without selecting the whole product. Use a candidate-shape breadboard:

```text
/planning-skills:breadboard planning/shaping.md "mode: candidate-shape; question: hide-bought behavior"
```

The breadboard makes the places, affordances, stores, and wiring visible. You can now see that a display-only filter preserves the bought state and supports undo, while deletion would conflict with the requirements.

The candidate breadboard is still **evidence**, not build scope. It feeds what you learned back into shaping.

## A visual changes the plan: reconcile it instead of copying it

Suppose you return to Figma and add a “Clear bought” button. The mockup now contains behavior that is not in the accepted plan.

Bring that screen into an agent that can inspect the visual and invoke sketch reconciliation. In Claude Code with the plugin:

```text
/planning-skills:reconcile-sketch planning/shaping.md planning/breadboard.md /path/to/grocery-list.png
```

The skill identifies what the sketch confirms, clarifies, adds, or contradicts. The visual does not become truth just because it looks finished. You decide whether “Clear bought” belongs in this version; accepted deltas are then written back to the authoritative planning artifacts.

The sketch stays in the design tool. The decision comes back to the repo.

## Now commitment becomes strict

Exploration could move back and forth among requirements, shapes, fit checks, spikes, sketches, and candidate breadboards. Selection cannot.

Before choosing a direction, accept the requirements and Appetite and make sure the comparison is decision-ready. Then make the human choice explicitly.

For example:

```text
/planning-skills:select-shape planning/shaping.md "Choose Shape A"
```

After selection, reconcile the surviving behavior into a **selected-design** breadboard. Candidate evidence does not automatically promote itself.

```text
/planning-skills:breadboard planning/shaping.md "mode: selected-design"
```

Now `planning/breadboard.md` is accepted behavioral intent. Only now can it legitimately feed slicing and implementation.

This is the repo's central rule in action:

> **Exploration is fluid. Commitment is gated.**

## Choose one buildable slice

For this tiny app, the accepted breadboard may already expose an obvious vertical slice: **add an item and restore it after refresh**. If so, select it directly; do not add ceremony because Dumplink exists.

If a larger project needs dependency-aware decomposition, this is where you would run:

```text
/planning-skills:dumplink
```

and then choose one task group or other demoable slice as the active build boundary.

Likewise, add a statechart only if state complexity warrants it, interface contracts only if a boundary is ambiguous, an executable breadboard only if examples and acceptance tests would remove real uncertainty, and a kickoff document only if builders need a durable orientation reference.

The skills are available moves, not required stages.

## Give the builder less context, not more

When the slice is ready, package only what the implementation agent needs:

```text
/planning-skills:feed-context planning/frame.md planning/shaping.md planning/breadboard.md
```

The resulting `planning/context-packet.md` contains the active scope, accepted behavior, relevant constraints, non-goals, and verification target.

That is what the coding agent receives—not the original notes, every rejected shape, all candidate breadboards, the Figma history, or months of chat.

The implementation request can now be simple:

```text
Implement the selected slice in planning/context-packet.md. Preserve the accepted behavior and stop if code reality invalidates the plan.
```

## Build, then compare reality with intent

The agent builds the slice.

Suppose implementation reveals that the browser-storage behavior differs from what the plan assumed. Do not let the implementation silently redefine the product and do not force the old plan onto reality.

First check drift; if there is a real mismatch, reflect explicitly:

```text
/planning-skills:reflect-breadboard
```

Record implementation reality separately, compare it with accepted intent, and decide which should change. If the plan changes, update the accepted artifact. If the implementation is wrong, correct the code. Then continue from the new accepted state.

## The operating loop

The whole example can be reduced to one habit:

**Work where the thinking is happening → open the product repo when a consequential question appears → invoke the one skill that resolves it → save the result beside the code → carry that accepted state into the next tool, session, or agent.**

The repo is the durable layer between the places where product work actually happens.

Two optional moves sit outside this particular walkthrough:

- **Wayfinding** coordinates a bounded planning effort when the planning itself spans multiple dependent questions or sessions.
- **Lead User Research** can run upstream when the opportunity depends on future-facing trends, advanced users, or unusually high-benefit needs.

And if the change is already small, obvious, and low-risk, skip Planning Skills and make the change.
