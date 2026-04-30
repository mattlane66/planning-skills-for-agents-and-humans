---
name: kickoff-doc
description: Turn kickoff notes or transcripts into a builder-facing reference document organized by system area.
planning: true
shaping: true
---

# Kickoff Document

Use this skill when a project has already been discussed and shaped enough that builders need a durable reference doc.

## Goal

Create a kickoff document that is organized by the product or system being built, not by the order people happened to talk.

## Before you start

If the source is a kickoff transcript, clarify:
1. who the primary audience is
2. what other inputs exist, such as screenshots, breadboards, mockups, or notes

The transcript is the source material. The document is not a summary of the call. It is a map of the shaped territory.

## Core principle

A kickoff transcript is chronological. A useful kickoff document is structural.

The reader should be able to jump to one part of the system and understand:
- what it is
- what belongs there
- what decisions were made about it
- what constraints matter there
- how it connects to neighboring parts

## Organizing principle: territory, not timeline

Organize by the thing being built, not by the order people talked.

Do not organize by build sequence. If the team identified slices or phased delivery, that belongs in slices or plans, not in this reference document.

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
- how it relates to other areas
- design decisions specific to that area
- edge cases, placeholders, or open questions that still matter

## Voice: use their words

Use the team’s real language where it helps recognition.

Do:
- synthesize scattered discussion into one clean statement
- capture the reasoning behind decisions when it was expressed
- make the territory legible without adding new conclusions

Do not:
- put new ideas in people’s mouths
- add motivational framing they did not express
- editorialize about importance beyond what was actually said

## Writing rules

- Organize by system area, not meeting order.
- Keep decisions next to the area they affect.
- Do not create a generic dump section called `Design Decisions`.
- Do not turn the kickoff doc into an implementation sequence.
- Preserve the team’s real language where it helps recognition.
- Synthesize repeated discussion into one clean statement.

## Process

1. Read the full transcript or full set of notes.
2. Identify the major areas of the system that were discussed.
3. Draft the Frame section from the framing and outcome discussion.
4. Write each Shape section by pulling together all the relevant discussion for that area, even if it was scattered across the conversation.
5. Place design decisions inline in the area they affect.
6. Review against the source and remove anything you cannot support.

## Recommended template

```md
---
planning: true
shaping: true
artifact_type: kickoff
status: draft
source_of_truth: true
feeds:
  - implementation-packet
  - context-packet
---

# [Project] — Kickoff

# Context Card

## Use this when
An agent needs the builder-facing reference after the team has already converged.

## Must preserve
- frame constraints
- shaped territory sections
- decisions attached to the system area they affect
- explicit exclusions or unresolved questions

## Ignore unless asked
- transcript order
- side conversations that did not become shaped territory

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

## Self-check before finishing

- The document is organized by shaped territory, not transcript order.
- Every area explains what it is, what belongs there, how it behaves, and how it connects to neighboring areas.
- Decisions sit next to the area they affect rather than in a generic dump section.
- Build sequence, slice order, and implementation tasks are not mixed into the reference doc unless clearly marked as handoff context.
- Claims are supported by the source or clearly marked as open questions.
- The artifact has planning frontmatter and a Context Card when it will feed downstream agent work.
