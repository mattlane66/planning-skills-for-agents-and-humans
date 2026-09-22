---
name: breadboard-reflection
description: Compare accepted intent with implementation reality, assess realized conformance and effect separately, diagnose failures backward, and prepare explicit correction decisions.
license: MIT
---

# Breadboard Reflection

Use this skill after a breadboard exists and implementation has started or already exists.

## Goal

Preserve accepted intent and implementation reality as separate views, then keep three questions distinct:

1. **Implementation drift:** did implementation realize the selected design?
2. **Realized conformance:** does the built artifact actually satisfy Accepted R under the relevant operating model M?
3. **Effect** (the older repo term was **realized fit**): does outcome evidence support that deployment moved reality from x toward y?

A pass at one altitude is not a pass at the next. A build can match selected intent and satisfy written requirements yet still fail to create the intended effect in reality.

## Reflection loop

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

### 4. Assess realized conformance

Realized conformance is post-build and pre-effect. Ask whether the thing that was actually made still satisfies each relevant Accepted R under the relevant M.

Use implementation and runtime evidence appropriate to the requirement: tests, inspection, benchmarks, traces, screenshots, measured behavior of the built system, or other direct verification. Record one status per relevant R: `NOT_ASSESSED | CONFORMS | UNCERTAIN | DOES_NOT_CONFORM`.

If implementation drift exists, distinguish it from conformance. A built artifact can differ from the selected design yet still satisfy R, or match the design exactly and still fail R because the design-conformance judgment was wrong or M changed.

When relevant operating conditions may have changed during implementation, revisit M before declaring realized conformance.

### 5. Assess effect separately

Effect asks what outcome evidence supports about whether deployment actually moved reality from x toward y. The existing phrase **realized fit** remains a routing/search alias, but the canonical evaluation is effect.

Use real outcome evidence such as observed user behavior, field observation, telemetry, support evidence, research, or experiments. Preserve the evidence and one status: `NOT_ASSESSED | SUPPORTED | WEAKENED | CONTRADICTED`. Requirement-level outcome observations may help diagnose the result, but effect is judged against the frame's x and y, not inferred merely because implementation or realized conformance passed.

Realized conformance does not prove effect. If no outcome evidence exists, record `NOT_ASSESSED` explicitly.

If effect evidence would change accepted planning, stop at an `effect-decision` before changing the frame, M, R, selected design, implementation direction, or bet.

### 6. Diagnose backward when effect is surprising

When effect is weakened, contradicted, or unexpectedly successful, walk backward instead of assuming execution is the cause:

1. **Effect inference:** is the evidence, measurement window, comparison, and interpretation sound?
2. **Realized conformance:** did the built artifact actually satisfy R under the relevant M?
3. **Implementation:** did implementation realize the selected design?
4. **Design conformance / selection:** was the selected design's fit judgment sound, and was selection reasonable among the viable candidates?
5. **Requirements:** was R complete and correctly derived?
6. **Operating model:** did M describe the operating world and relevant dynamics correctly, or did it become stale?
7. **Frame:** were x and y still the right representations of the situation and desired outcome?

Do not automatically change every upstream artifact. The backward walk locates the smallest defensible correction and makes correlated errors visible.

## Output structure

Use `templates/breadboard-reflection.md`. Include drift comparison when drift is in scope, realized conformance when build validity is in scope, and effect whenever outcome validity is being assessed—even if the effect status is `NOT_ASSESSED` because outcome evidence is absent.

## Rule

Do not silently rewrite the accepted breadboard to match implementation. Record reality first, compare it with intent, and require an explicit drift decision before changing either truth. Never infer effect from implementation conformance or realized conformance alone.

## Self-check before finishing

- Relevant implementation or system reality was inspected before critique.
- Accepted intent and current implementation reality remain separate.
- Implementation drift, realized conformance, and effect are not collapsed into one verdict.
- Missing, stale, or wrong breadboard nodes are named explicitly.
- Design smells are tied to concrete places, affordances, stores, or wiring.
- Proposed fixes explain the expected improvement.
- A human drift decision is recorded before authoritative plan changes are applied, unless the user's instruction already authorized the change.
- Realized-conformance statuses use direct build/runtime evidence and reconsider M when relevant.
- Effect statuses use outcome evidence from actual use, or remain `NOT_ASSESSED`.
- Surprising effect triggers backward diagnosis before an upstream rewrite.
- Planning updates and implementation follow-ups are separated.
- The artifact has planning frontmatter and a Context Card when it will feed downstream agent work.
