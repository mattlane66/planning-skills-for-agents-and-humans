# Example

This folder contains a simple, end-to-end example showing how to use the skills in this repo in a realistic order.

The example is intentionally much simpler than your real world situation. The goal is to make it obvious:
- what to start with
- which skill to use next
- what each output should look like
- when a skill is optional
- how the artifacts relate to one another

## Example: Simple Grocery List

The `simple-grocery-list/` example walks through a tiny feature from messy notes to shaped direction to breadboard.

Recommended reading order:

1. `simple-grocery-list/README.md`
2. `simple-grocery-list/00-source-notes.md`
3. `simple-grocery-list/01-frame.md`
4. `simple-grocery-list/02-shaping.md`
5. `simple-grocery-list/04-breadboard.md`
6. `simple-grocery-list/05-breadboard-reflection.md`
7. `simple-grocery-list/03-kickoff.md`

## What this example demonstrates

- **`/framing-doc`** turns messy source material into a frame.
- **`/shaping`** separates requirements from solution choices and compares solution directions.
- **`/breadboarding`** maps the selected shape into places, affordances, stores, and wiring.
- **`/breadboard-reflection`** is used later, after code exists, to sync the breadboard to implementation and find drift or design smells.
- - **`/kickoff-doc`** creates a builder-facing reference doc after the direction is chosen.

## Suggested workflow

Use the example as a pattern, not a template to copy blindly.

1. Start with raw notes, requests, or transcripts.
2. Create a frame.
3. Shape the problem and compare options.
4. Choose a direction.
5. Breadboard the chosen shape.
6. After implementation exists, use reflection to compare the breadboard to reality.
7. Optionally create a kickoff doc if handing off to another builder.
