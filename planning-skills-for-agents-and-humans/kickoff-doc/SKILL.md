---
name: kickoff-doc
description: Use when you have a kickoff transcript or notes and need a builder-facing reference document organized by the system being built rather than by conversation order.
---

# Kickoff Document

A kickoff document is a map of the shaped territory, not a chronological recap of the meeting.

Builders should be able to open the doc, jump to an area of the system, and understand what belongs there, what decisions were made, and what constraints matter.

---

## Organizing Principle

Organize by area of the system, not by the order people talked.

The transcript is sequential. The product is structural.

---

## Top-Level Sections

### Frame
Capture:
- the problem
- the desired outcome
- key constraints the builder must keep in mind

### Shape
Create one subsection per meaningful area of the system.

For each area, capture:
- what it is
- what appears there
- how it connects to adjacent areas
- decisions that specifically belong there
- notable edge cases or placeholders

---

## Writing Rules

- use the team’s actual language when possible
- synthesize scattered discussion into a coherent area description
- keep design decisions inline with the area they affect
- do not create a generic dumping-ground section called `Design Decisions`
- do not turn the doc into a build sequence

Build order belongs in slices or plans, not in the kickoff reference.

---

## Minimal Template

```markdown
---
planning: true
---

# [Project] — Kickoff

## Frame

### Problem
- ...

### Outcome
- ...

## Shape

### [Area 1]
- what it is
- what belongs here
- decisions and constraints

### [Area 2]
- what it is
- what belongs here
- decisions and constraints
```
