---
name: breadboard-reflection
description: Compare accepted intent with implementation reality when code or a prototype exists, preserve both separately, surface drift and design smells, and prepare an explicit correction decision.
license: MIT
---

# Breadboard Reflection

Use this skill after a breadboard exists and implementation has started or already exists.

## Goal

Preserve accepted intent and implementation reality as two explicit views, identify the differences, and let a human decide which truth changes before rewriting authoritative artifacts.

## Three-phase loop

### 1. Record implementation reality

The implementation is ground truth for what the system does now. It does not automatically replace the accepted plan.

Do this first:
- read the relevant implementation
- record actual places, affordances, stores, branches, and wiring
- name hidden state or omitted transitions
- cite concrete files, tests, observations, or runtime evidence
- keep this current-state record separate from the accepted breadboard

Do not repair, remove, or rewrite accepted breadboard nodes during this phase.

### 2. Compare intent with reality and reflect

Compare the accepted breadboard and selected slice with the current-state record. Classify:
- matches
- drift
- missing behavior
- accidental or invented behavior
- design smells visible in either the intended or current design

Once the comparison is factual, inspect the design itself.

Look for:
- hidden state
- unclear boundaries
- steps that resist clear naming
- duplicated responsibility
- missing explanatory links in the wiring
- places that are too broad or too muddled

## Smells to check

| Smell | What it suggests |
|------|-------------------|
| Unexplained behavior | The artifact does not explain how the effect happens |
| Naming resistance | A node may be bundling multiple responsibilities |
| Missing source for displayed data | A store or upstream affordance is absent |
| Wrong causality | The wiring tells the wrong story about what triggers what |
| Place overload | Too many unrelated concerns are packed together |

## Naming test

For any affordance that feels off, ask:
1. Who calls it?
2. What is its direct step-level effect?
3. Can it be named with one clear verb?

If the answer requires two verbs joined by "and" or "or," the boundary may be wrong.

### 3. Prepare or apply the drift decision

Present these options when intent and reality disagree:

1. update implementation to match the accepted plan
2. update the plan because an original assumption was wrong
3. split the slice and defer the conflicting part

Recommend a move with evidence, then stop for the human decision unless the user's current instruction already authorizes one option. After a decision, update only the chosen truth and any affected downstream artifacts; retain the reflection as the audit record.

## Output structure

Use `templates/breadboard-reflection.md`. Include inputs, inspected reality, matches, drift, missing behavior, accidental behavior, design smells, proposed fixes, and the drift decision needed or already authorized.

## Rule

Do not silently rewrite the accepted breadboard to match implementation. Record reality first, compare it with intent, and require an explicit drift decision before changing either truth.

## Self-check before finishing

- Relevant implementation or system reality was inspected before critique.
- Accepted intent and current implementation reality remain separate.
- The reflection separates factual comparison from design critique.
- Missing, stale, or wrong breadboard nodes are named explicitly.
- Design smells are tied to concrete places, affordances, stores, or wiring.
- Proposed fixes explain the expected improvement.
- A human drift decision is recorded before authoritative plan changes are applied, unless the user's instruction already authorized the change.
- Planning updates and implementation follow-ups are separated.
- The artifact has planning frontmatter and a Context Card when it will feed downstream agent work.
