---
name: breadboard-reflection
description: Use when a breadboard exists and you need to sync it to the implementation, then inspect it for hidden work, weak boundaries, or misleading explanations.
---

# Breadboard Reflection

Reflection has two phases and they must stay in order:
1. sync the breadboard to what the system actually does
2. inspect the synced breadboard for design smells

---

## Phase 1: Sync to Reality

Treat the implementation as ground truth.

Read the code and update the breadboard before making design judgments.

Look for:
- missing functions or handlers
- hidden stores or configuration that shape behavior
- wrong call chains
- places that do not match how the system is actually bounded

Only after the breadboard is accurate should you evaluate whether the design is good.

---

## Phase 2: Reflect on the Design

Once the breadboard is accurate, trace real user stories through it.

Ask:
- does the path tell a coherent story?
- are there hidden transformations or decisions missing from the artifact?
- do the affordance names match their actual step-level effect?
- are unrelated responsibilities collapsed into one node?
- does any place contain work that belongs elsewhere?

---

## Common Smells

| Smell | What it looks like |
|------|---------------------|
| Missing explanation | The system clearly does work the breadboard does not show |
| Naming resistance | You cannot name a node cleanly with one verb |
| Wrong causality | The wire says A calls B but the code shows C calls B |
| Hidden state | Static config or stores shape behavior but are not represented |
| Mixed responsibility | One affordance does several distinct jobs |
| Drift | The artifact still describes a past version of the system |

---

## The Naming Test

For each non-UI affordance:
1. identify its caller
2. identify its direct effect
3. name that effect with one clean verb or verb phrase

If you need `and` or `or`, the boundary may be wrong.

Examples:
- Good: `validate request`
- Good: `append next page`
- Suspicious: `validate and create or update item`

---

## Fix Order

1. fix the implementation understanding
2. update the tables
3. regenerate the diagram
4. retrace the user story
5. optionally refactor the code to match the better design

Never fix only the diagram.

---

## Review Checklist

- every node in the diagram exists in the tables
- every visible output has a source
- every code affordance participates in a real path
- control flow and data flow are not conflated
- the story of the behavior can be explained without handwaving
