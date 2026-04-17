---
name: kickoff-doc
description: Turn kickoff notes or transcripts into a builder-facing reference document organized by system area.
planning: true
---

# Kickoff Document

Use this skill when a project has already been discussed and shaped enough that builders need a durable reference doc.

## Goal

Create a kickoff document that is organized by the product or system being built, not by the order people happened to talk.

## Core principle

A kickoff transcript is chronological. A useful kickoff document is structural.

The reader should be able to jump to one part of the system and understand:
- what it is
- what belongs there
- what decisions were made about it
- what constraints matter there
- how it connects to neighboring parts

## Recommended top-level structure

### Frame
Capture the short version of:
- the problem
- the desired outcome
- the constraints or boundaries that matter most

### Shape
Break the rest of the document into sections based on the shaped territory.

Each section should represent a meaningful area of the product, workflow, or system.

For each area, capture:
- what it is
- what appears there
- how it behaves
- design decisions specific to that area
- edge cases, placeholders, or open questions that still matter

## Writing rules

- Organize by system area, not meeting order.
- Keep decisions next to the area they affect.
- Do not create a generic dump section called `Design Decisions`.
- Do not turn the kickoff doc into an implementation sequence.
- Preserve the team’s real language where it helps recognition.
- Synthesize repeated discussion into one clean statement.

## Recommended template

```md
---
planning: true
---

# [Project] — Kickoff

## Frame

### Problem
- ...

### Outcome
- ...

### Constraints
- ...

## Shape

### [Area 1]
- what this area is
- what belongs here
- important decisions
- constraints or open questions

### [Area 2]
- what this area is
- what belongs here
- important decisions
- constraints or open questions
```

## Rule of thumb

If a builder would need to reread the original transcript to understand one part of the system, the kickoff doc is not finished.
