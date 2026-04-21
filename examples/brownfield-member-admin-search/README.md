# Brownfield Member Admin Search — Step-by-Step Example

This example shows how to use the skills on a brownfield change instead of a greenfield feature.

> Add member search to an existing admin page without replacing the current page structure, status filter, pagination, or detail-page flow.

The point of this example is to show how to work from `CURRENT`, shape a change against an existing system, and breadboard old and new affordances together.

## Why this example is useful

It demonstrates a different path than the grocery-list example:
- there is already a system in place
- the existing behavior matters
- the new change must preserve important current structure

## Files in this example

- `00-current-system-notes.md` — the current system and pain points
- `01-frame.md` — output of `/framing-doc`
- `02-shaping.md` — output of `/shaping` using `CURRENT` and two change directions
- `03-breadboard.md` — output of `/breadboarding` showing existing and new affordances together

## Step 1 — Start from the current system

Open `00-current-system-notes.md`.

Use `/framing-doc` when you have notes about what exists today, where the friction is, and what kind of change is wanted.

## Step 2 — Shape against `CURRENT`

Use `/shaping` on `01-frame.md` and capture the current system explicitly.

This example shows:
- `CURRENT` as the baseline
- one selected direction that modifies the current page in place
- one alternative that creates a separate search page

## Step 3 — Breadboard existing and new together

Use `/breadboarding` after the direction is chosen.

This example shows how to map:
- existing affordances that stay
- new affordances being added
- stores and URL state that connect the change to the current system

## What to notice

- `CURRENT` is not just a note; it is part of the shaping logic
- the chosen shape is evaluated against what already exists
- the breadboard tells one story that includes both the current page and the new search behavior
