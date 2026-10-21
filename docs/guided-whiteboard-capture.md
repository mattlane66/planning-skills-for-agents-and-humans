# Guided whiteboard capture

**Purpose:** Turn a rough whiteboard and a person's explanation into a durable, reviewable breadboard in one focused pass. This is an **optional entry recipe** for existing `shaping` and `breadboarding` skills, not a sixteenth skill, new authority level, or mandatory stage.

**Authority:** Canonical places/affordances/stores/wiring tables are authoritative **within the declared mode**. A deliberately spatial visual is the primary *human review surface*, and prose follows the same places, behaviors, and IDs. Neither the visual nor the prose is a separate source of product truth.

[Worked synthetic example](../examples/guided-whiteboard-capture/README.md).

## Input: what the person already has

- A photo/screenshot of a rough whiteboard, wireframe, or sketches mixed with screenshots; multiple images may be unfinished.
- A **top-to-bottom guided tour** of what each region means, what the user does, where controls lead, what data changes, and what is undecided. Spoken audio, an available transcript, typed notes, or annotations are equally valid; speech is **not required**.
- Optionally: current product evidence, a named candidate, requirements, Appetite, an accepted plan, or a particular behavior to inspect.

Do **not** claim to have heard speech, transcribed audio, or inspected an image that is unavailable. Request only the missing explanation needed for the current decision. Keep private raw images, recordings, transcripts, secrets, or client data out of public repos and release assets unless explicitly authorized.

### Fast starting instruction

> Use the existing shaping/breadboarding skills with the guided whiteboard capture recipe. This screenshot is rough solution thinking, not accepted product intent. Here is my top-to-bottom guided tour: [explanation]. Capture the proposal as candidate A. Separate what is visible from what I said, observed behavior, and your assumptions. Produce ID-stable canonical tables, a legible spatial breadboard, and short prose in the same place order. Highlight gaps and contradictions; don't invent hidden behavior, select a solution, or begin implementation.

## Route to the smallest existing move

| Context | Owner | Permitted authority |
| --- | --- | --- |
| Rough solution, unclear needs or alternative directions | `shaping`, S-first | Working requirements and candidate shape |
| Named candidate and concrete flow to inspect | `breadboarding`, `candidate-shape` | Exploratory candidate evidence |
| Map existing observed behavior | `breadboarding`, `current-state` | Descriptive evidence, not future design |
| Selected direction with accepted R, Appetite, and cuts | `breadboarding`, `selected-design` | Normative **only after** reconciliation and acceptance |
| New sketch changes accepted design | `sketch-reconciliation` | Proposed deltas until accepted |
| Narrated post-kickoff corrections or decisions | `planning-change-reconciliation` | Proposed deltas until accepted |
| Demo/code differs from accepted behavior | `breadboard-reflection` | Implementation evidence, not a rewritten plan |

If a specific skill/mode was selected by the user, respect it. The media type does not itself determine the route. A whiteboard alone cannot satisfy a selection or scope gate.

## One-pass bootstrap

1. **Label source provenance.** Identify images/regions and transcript segments/timestamps. Distinguish `VISIBLE`, `NARRATED`, `CODE/OBSERVED`, and `INFERRED/OPEN`. The person's words outrank guesses about intended behavior from the picture. Runtime evidence outranks an unverified description of what the current product actually does. Surface conflicts; do not silently merge them.
2. **Declare candidate and authority.** Name the shape if unselected, the mode, current requirements and Appetite status (Working/Accepted/Unset), and the concrete behavior question.
3. **Extract causal structure.** Identify places P, visible affordances U, consequential hidden mechanisms N, stores/state S, branches, wires, and observable consequences. Preserve IDs when reconciling prior material. No static sketch proves persistence, permissions, navigation, validation, errors, or state transitions.
4. **Make the canonical tables.** Trace representative scenarios from entry through consequence. Mark missing connections `UNKNOWN`; do not synthesize evidence, validation, or a passing Fit Check.
5. **Compose a hard-line spatial visual.** Arrange place stacks and visible affordances for finger tracing, with local branches and a lower system rail. Keep stable IDs. Avoid auto-layout graph clutter and decorative UI speculation. If rendering is unavailable, supply a legible text-spatial diagram and say so.
6. **Mirror with structured prose.** Explain the same places and flows in the visual's order. Use the same IDs and distinguish narrated intent from inspected behavior and unresolved inference. Prose must not invent a mechanism missing from the model.
7. **Show for correction.** Ask for feedback on the representation. Accepting that the map accurately reflects candidate A **does not select A** or authorize build. Requirements, Appetite, selection, promotion, and slicing gates remain active.

## Continuous CAD-style revisions

Once a breadboard exists, the human can point to a flaw, describe an alternative, annotate a screenshot, dictate a new issue, or compare a demo.

1. Fix the applicable baseline/version and authority; keep existing IDs.
2. Classify incoming evidence as editorial, clarification, substantive behavior/scope change, or implementation finding.
3. Create a **private model-first proposal** (modified tables / semantic ID inventory); do not overwrite accepted material.
4. Render a proposed visual for human review, then prose in the same territory order. Show before/after visuals and readable highlighted **semantic** and text diffs. A visual diff alone cannot classify a decision.
5. Obtain an explicit trusted human accept/revise/reject/defer decision for consequential deltas. Spoken narration is input, not approval; approving one delta does not approve its neighbors.
6. Apply authorized changes only to the owning canonical artifacts; rerun relevant traces, fit checks, scope, slice, contracts and demo checks. Mark downstream artifacts `updated`, `stale`, `not affected`, or `not assessed`, then republish read-only projections.

For visual changes use `sketch-reconciliation`; for narrated decisions use `planning-change-reconciliation`; for implementation drift use `breadboard-reflection`. Use their existing human gates and private-diff facilities. Do not replace their ownership with this recipe.

## Audit checklist

- Each visual node maps to a canonical ID; important behavior can be finger-traced to an observable consequence.
- The prose follows the visual's place/flow order and introduces no unmodeled behavior.
- Image observations, narration, actual observations, and inferences are distinguishable, including conflicts and `UNKNOWN` hidden effects.
- Candidate/current-state/selected-design authority, provisional requirements/Appetite, and human selection are never conflated.
- Accepted baselines remain intact during private review; meaningful revisions are ID-linked, classified, and gated.
- Audio is optional; confidential source material is not silently published; the smallest useful move is chosen.

**Do not add planning ceremony where a small, clear, low-risk change needs none.**
